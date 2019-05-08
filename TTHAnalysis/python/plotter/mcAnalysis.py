#!/usr/bin/env python
#from tree2yield import *
from CMGTools.TTHAnalysis.plotter.tree2yield import *
from CMGTools.TTHAnalysis.plotter.projections import *
from CMGTools.TTHAnalysis.plotter.figuresOfMerit import FOM_BY_NAME
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import *
import pickle, re, random, time
from copy import copy, deepcopy
from collections import defaultdict
from glob import glob

_T0 = long(ROOT.gSystem.Now())

## These must be defined as standalone functions, to allow runing them in parallel
def _runYields(args):
    key,tty,cuts,noEntryLine,fsplit = args
    return (key, tty.getYields(cuts,noEntryLine=noEntryLine,fsplit=fsplit))

def _runPlot(args):
    key,tty,plotspec,cut,closeTree,fsplit = args
    #timer = ROOT.TStopwatch()
    #print "Starting plot %s for %s, %s" % (plotspec.name,key,tty._cname)
    ret = (key,tty.getPlot(plotspec,cut,fsplit=fsplit,closeTreeAfter=closeTree))
    #print "Done plot %s for %s, %s, fsplit %s in %s s, at %.2f; entries = %d, time/entry = %.3f ms" % (plotspec.name,key,tty._cname,fsplit,timer.RealTime(), 0.001*(long(ROOT.gSystem.Now()) - _T0), ret[1].GetEntries(), (long(ROOT.gSystem.Now()) - _T0)/float(ret[1].GetEntries()))
    return ret

def _runApplyCut(args):
    key,tty,cut,fsplit = args
    return (key, tty.cutToElist(cut,fsplit=fsplit))

def _runGetEntries(args):
    key,tty = args
    return (key, tty.getEntries())

def _runSumW(args):
    key, tty, genWName = args
    return (key, tty.getSumW(genWName))


class MCAnalysis:
    def __init__(self,samples,options):
        self._options = options
        self._allData     = {}
        self._data        = []
        self._signals     = []
        self._backgrounds = [] 
        self._isSignal    = {}
        self._rank        = {} ## keep ranks as in the input text file
        self._projection  = Projections(options.project, options) if options.project != None else None
        self._premap = []
        self._optionsOnlyProcesses = {}
        self._groupsToNormalize = [] # list of (gen weight name, list of ttys)
        self.init_defaults = {}
        for premap in options.premap:
            to,fro = premap.split("=")
            if to[-1] == ":": to = to[:-1]
            to = to.strip()
            for k in fro.split(","):
                self._premap.append((re.compile(k.strip()+"$"), to))
        self.variationsFile = UncertaintyFile(options.variationsFile,options) if options.variationsFile else None
        self.readMca(samples,options)

    def readMca(self,samples,options,addExtras={}):
        field_previous = None
        extra_previous = {}
        for line in open(samples,'r'):
            if re.match("\s*#.*", line): continue
            line = re.sub(r"(?<!\\)#.*","",line)  ## regexp black magic: match a # only if not preceded by a \!
            line = line.replace(r"\#","#")        ## and now we just unescape the remaining #'s
            extra = {}
            if ";" in line:
                (line,more) = line.split(";")[:2]
                for setting in [f.replace(';',',').strip() for f in more.replace('\\,',';').split(',')]:
                    if setting == "": continue
                    if "=" in setting: 
                        (key,val) = [f.strip() for f in setting.split("=",1)]
                        extra[key] = eval(val)
                    else: extra[setting] = True
            for k,v in addExtras.iteritems():
                if k in extra: raise RuntimeError, 'You are trying to overwrite an extra option already set'
                extra[k] = v
            field = [f.strip() for f in line.split(':')]
            if len(field) == 1 and field[0] == "*":
                if len(self._allData): raise RuntimeError, "MCA defaults ('*') can be specified only before all processes"
                #print "Setting the following defaults for all samples: "
                for k,v in extra.iteritems():
                    #print "\t%s: %r" % (k,v)
                    self.init_defaults[k] = v
                continue
            else:
                for k,v in self.init_defaults.iteritems():
                    if k not in extra: extra[k] = v
            if len(field) <= 1: continue
            if "SkipMe" in extra and extra["SkipMe"] == True and not options.allProcesses: continue
            if 'PostFix' in extra:
                hasPlus = (field[0][-1]=='+')
                if hasPlus: field[0] = field[0][:-1]
                field[0] += extra['PostFix']
                if hasPlus: field[0]+='+'
            # copy fields from previous component if field is "prev" (careful: does not copy extra)
            if "$prev" in field and not field_previous: raise RuntimeError, "You used a prev directive to clone fields from the previous component, but no previous component exists"
            field = [field_previous[i] if field[i]=="$prev" else field[i] for i in xrange(len(field))]
            field_previous = field[:]
            if "$prev" in extra:
                del extra['$prev']
                new_extra = copy(extra_previous)
                new_extra.update(extra)
                extra = new_extra
            extra_previous = copy(extra)
            signal = False
            pname = field[0]
            if pname[-1] == "+": 
                signal = True
                pname = pname[:-1]
            ## if we remap process names, do it
            for x,newname in self._premap:
                if re.match(x,pname):
                    pname = newname
           ## If we have a user-defined list of processes as signal
            if len(options.processesAsSignal):
                signal = False
                for p0 in options.processesAsSignal:
                    for p in p0.split(","):
                        if re.match(p+"$", pname): signal = True
            ## Options only processes
            if field[1] == "-": 
                self._optionsOnlyProcesses[field[0]] = extra
                self._isSignal[field[0]] = signal
                continue
            if field[1] == "+": # include an mca into another one, usage:   otherprocesses : + ; IncludeMca="path/to/other/mca.txt"
                if 'IncludeMca' not in extra: raise RuntimeError, 'You have declared a component with IncludeMca format, but not included this option'
                extra_to_pass = copy(extra)
                del extra_to_pass['IncludeMca']
                self.readMca(extra['IncludeMca'],options,addExtras=extra_to_pass) # call readMca recursively on included mca files
                continue
            # Customize with additional weight if requested
            if 'AddWeight' in extra:
                if len(field)<2: raise RuntimeError, 'You are trying to set an additional weight, but there is no weight initially defined for this component'
                elif len(field)==2: field.append(extra['AddWeight'])
                else: field[2] = '(%s)*(%s)'%(field[2],extra['AddWeight'])
            ## If we have a selection of process names, apply it
            skipMe = (len(options.processes) > 0)
            for p0 in options.processes:
                for p in p0.split(","):
                    if re.match(p+"$", pname): skipMe = False
            for p0 in options.processesToExclude:
                for p in p0.split(","):
                    if re.match(p+"$", pname): skipMe = True
            for p0 in options.filesToExclude:
                for p in p0.split(","):
                    if re.match(p+"$", field[1]): skipMe = True
            if skipMe: continue

            # Load variations if matching this process name
            variations={}
            if self.variationsFile:
                for var in self.variationsFile.uncertainty():
                    if var.procmatch().match(pname) and var.binmatch().match(options.binname): 
                        #if var.name in variations:
                        #    print "Variation %s overriden for process %s, new process pattern %r, bin %r (old had %r, %r)" % (
                        #            var.name, pname, var.procpattern(), var.binpattern(), variations[var.name].procpattern(), variations[var.name].binpattern())
                        variations[var.name] = var
                if 'NormSystematic' in extra:
                    del extra['NormSystematic']
                    if pname not in getattr(options, '_warning_NormSystematic_variationsFile',[]):
                       options._warning_NormSystematic_variationsFile = [pname] + getattr(options, '_warning_NormSystematic_variationsFile',[])
                       print "Using both a NormSystematic and a variationFile is not supported. Will disable the NormSystematic for process %s" % pname
            if 'NormSystematic' in extra:
                variations['_norm'] = Uncertainty('norm_%s'%pname,pname,options.binname,'normSymm',[1+float(extra['NormSystematic'])])
                if not hasattr(options, '_deprecation_warning_NormSystematic'):
                    print 'Added normalization uncertainty %s to %s, %s. Please migrate away from using the deprecated NormSystematic option.'%(extra['NormSystematic'],pname,field[1])
                    options._deprecation_warning_NormSystematic = False

            cnames = [ x.strip() for x in field[1].split("+") ]
            total_w = 0.; to_norm = False; ttys = [];
            genWeightName = extra["genWeightName"] if "genWeightName" in extra else "genWeight"
            genSumWeightName = extra["genSumWeightName"] if "genSumWeightName" in extra else "genEventSumw"
            is_w = -1
            pname0 = pname
            for cname in cnames:
                skipMe = False
                for p0 in options.filesToExclude:
                    for p in p0.split(","):
                        if re.match(p+"$", cname): skipMe = True
                if skipMe: continue
                if options.useCnames: pname = pname0+"."+cname
                for (ffrom, fto) in options.filesToSwap:
                    if cname == ffrom: cname = fto
                treename = extra["TreeName"] if "TreeName" in extra else options.tree 
                objname  = extra["ObjName"]  if "ObjName"  in extra else options.obj

                basepath = None
                for treepath in options.path:
                    if os.path.exists(treepath+"/"+cname) or (treename == "NanoAOD" and os.path.isfile(treepath+"/"+cname+".root")):
                        basepath = treepath
                        break
                if not basepath:
                    raise RuntimeError("%s -- ERROR: %s process not found in paths (%s)" % (__name__, cname, repr(options.path)))

                rootfile = "%s/%s/%s/%s_tree.root" % (basepath, cname, treename, treename)
                if options.remotePath:
                    rootfile = "root:%s/%s/%s_tree.root" % (options.remotePath, cname, treename)
                elif os.path.exists(rootfile+".url"): #(not os.path.exists(rootfile)) and :
                    rootfile = open(rootfile+".url","r").readline().strip()
                elif (not os.path.exists(rootfile)) and os.path.exists("%s/%s/%s/tree.root" % (basepath, cname, treename)):
                    # Heppy calls the tree just 'tree.root'
                    rootfile = "%s/%s/%s/tree.root" % (basepath, cname, treename)
                elif (not os.path.exists(rootfile)) and os.path.exists("%s/%s/%s/tree.root.url" % (basepath, cname, treename)):
                    # Heppy calls the tree just 'tree.root'
                    rootfile = "%s/%s/%s/tree.root" % (basepath, cname, treename)
                    rootfile = open(rootfile+".url","r").readline().strip()
                pckfile = basepath+"/%s/skimAnalyzerCount/SkimReport.pck" % cname
                if treename == "NanoAOD":
                    objname = "Events"
                    pckfile = None
                    rootfile = "%s/%s" % (basepath, cname)
                    if os.path.isdir(rootfile):
                        rootfiles = glob("%s/%s/*.root" % (basepath, cname))
                    elif os.path.isfile(rootfile):
                        rootfiles = [ rootfile ]
                    elif os.path.isfile(rootfile+".root"):
                        rootfiles = [ rootfile+".root" ]
                    else:
                        raise RuntimeError("%s -- ERROR: cannot find NanoAOD file for %s process in paths (%s)" % (__name__, cname, repr(options.path)))
                else:
                    rootfiles = [ rootfile ]
                
                for rootfile in rootfiles:
                    mycname = cname if len(rootfiles) == 1 else cname + "-" + os.path.basename(rootfile).replace(".root","") 
                    tty = TreeToYield(rootfile, basepath, options, settings=extra, name=pname, cname=mycname, objname=objname, variation_inputs=variations.values(), nanoAOD=(treename == "NanoAOD")); 
                    tty.pckfile = pckfile
                    ttys.append(tty)

            for tty in ttys:
                if signal: 
                    self._signals.append(tty)
                    self._isSignal[pname] = True
                elif pname == "data":
                    self._data.append(tty)
                else:
                    self._isSignal[pname] = False
                    self._backgrounds.append(tty)
                if pname in self._allData: self._allData[pname].append(tty)
                else                     : self._allData[pname] =     [tty]
                if "data" not in pname:
                    if treename != "NanoAOD":
                        pckobj  = pickle.load(open(tty.pckfile,'r'))
                        counters = dict(pckobj)
                    else:
                        counters = { 'Sum Weights':0.0, 'All Events':0 }  # fake
                    if ('Sum Weights' in counters) and options.weight:
                        if (is_w==0): raise RuntimeError, "Can't put together a weighted and an unweighted component (%s)" % cnames
                        is_w = 1; 
                        total_w += counters['Sum Weights']
                        scale = "(%s)*(%s)" % (genWeightName, field[2])
                    else:
                        if (is_w==1): raise RuntimeError, "Can't put together a weighted and an unweighted component (%s)" % cnames
                        is_w = 0;
                        total_w += counters['All Events']
                        scale = "(%s)" % field[2]
                    if len(field) == 4: scale += "*("+field[3]+")"
                    for p0,s in options.processesToScale:
                        for p in p0.split(","):
                            if re.match(p+"$", pname): scale += "*("+s+")"
                    to_norm = True
                elif len(field) == 2:
                    pass
                elif len(field) == 3:
                    tty.setScaleFactor(field[2])
                else:
                    print "Poorly formatted line: ", field
                    raise RuntimeError                    
                # Adjust free-float and fixed from command line
                for p0 in options.processesToFloat:
                    for p in p0.split(","):
                        if re.match(p+"$", pname): 
                            tty.setOption('FreeFloat', True)
                            if 'NormSystematic' in extra: 
                                myvariations = tty.getVariations()
                                if len(myvariations) != 1 or myvariations[0].name != "norm_"+pname or myvariations[0].unc_type != "normSymm":
                                    raise RuntimeError("NormSystematic + FreeFloat from commandline => not supported");
                                tty.clearVariations()
                                tty.setOption('NormSystematic',0)
                for p0 in options.processesToFix:
                    for p in p0.split(","):
                        if re.match(p+"$", pname): tty.setOption('FreeFloat', False)
                for p0, p1 in options.processesToSetNormSystematic:
                    for p in p0.split(","):
                        if re.match(p+"$", pname): tty.setOption('NormSystematic', float(p1))
                thepeg = None
                for p0, p1 in options.processesToPeg:
                    for p in p0.split(","):
                        if re.match(p+"$", pname): 
                            tty.setOption('PegNormToProcess', p1)
                if tty.getOption('PegNormToProcess', pname) != pname and tty.getOption('NormSystematic',0):
                    myvariations = tty.getVariations()
                    if len(myvariations) != 1 or myvariations[0].name != "norm_"+pname or myvariations[0].unc_type != "normSymm":
                        raise RuntimeError("PegNormToProcess + NormSystematic + non-trivial uncertainties => not supported");
                    myvariations[0].name = "norm_"+tty.getOption('PegNormToProcess')
                    print "Overwrite the norm systematic for %s to make it correlated with %s" % (pname, tty.getOption('PegNormToProcess'))
                if pname not in self._rank: self._rank[pname] = len(self._rank)
            if to_norm: 
                if treename != "NanoAOD":
                    if total_w == 0: raise RuntimeError, "Zero total weight for %s" % pname
                    for tty in ttys: tty.setScaleFactor("%s*%g" % (scale, 1000.0/total_w))
                else:
                    if total_w != 0: raise RuntimeError, "Weights from pck file shoulnd't be there for NanoAOD for %s " % pname
                    self._groupsToNormalize.append( (ttys, genSumWeightName if is_w == 1 else "genEventCount", scale) )
                    
            #for tty in ttys: tty.makeTTYVariations()
        #if len(self._signals) == 0: raise RuntimeError, "No signals!"
        #if len(self._backgrounds) == 0: raise RuntimeError, "No backgrounds!"
    def listProcesses(self,allProcs=False):
        ret = self.listSignals(allProcs=allProcs) + self.listBackgrounds(allProcs=allProcs)
        if 'data' in self._allData.keys(): ret.append('data')
        return ret
    def listOptionsOnlyProcesses(self):
        return self._optionsOnlyProcesses.keys()
    def isBackground(self,process):
        return process != 'data' and not self._isSignal[process]
    def isSignal(self,process):
        return self._isSignal[process]
    def listSignals(self,allProcs=False):
        ret = [ p for p in self._allData.keys() if p != 'data' and self._isSignal[p] and (self.getProcessOption(p, 'SkipMe') != True or allProcs) ]
        ret.sort(key = lambda n : self._rank[n])
        return ret
    def listBackgrounds(self,allProcs=False):
        ret = [ p for p in self._allData.keys() if p != 'data' and not self._isSignal[p] and (self.getProcessOption(p, 'SkipMe') != True or allProcs) ]
        ret.sort(key = lambda n : self._rank[n])
        return ret
    def hasProcess(self,process):
        return process in self._allData
    def scaleProcess(self,process,scaleFactor):
        for tty in self._allData[process]: tty.setScaleFactor(scaleFactor)
    def scaleUpProcess(self,process,scaleFactor):
        for tty in self._allData[process]: 
            tty.setScaleFactor( "((%s) * (%s))" % (tty.getScaleFactor(),scaleFactor) )
    def getProcessOption(self,process,name,default=None,noThrow=False):
        if process in self._allData:
            return self._allData[process][0].getOption(name,default=default)
        elif process in self._optionsOnlyProcesses:
            options = self._optionsOnlyProcesses[process]
            return options[name] if name in options else default
        elif noThrow:
            return default
        else: raise RuntimeError, "Can't get option %s for undefined process %s" % (name,process)
    def setProcessOption(self,process,name,value):
        if process in self._allData:
            return self._allData[process][0].setOption(name,value)
        elif process in self._optionsOnlyProcesses:
            self._optionsOnlyProcesses[process][name] = value
        else: raise RuntimeError, "Can't set option %s for undefined process %s" % (name,process)
    def getProcessNuisances(self,process):
        ret = set()
        for tty in self._allData[process]: 
            ret.update([v.name for v in tty.getVariations()])
        return ret
    def getScales(self,process):
        return [ tty.getScaleFactor() for tty in self._allData[process] ] 
    def setScales(self,process,scales):
        for (tty,factor) in zip(self._allData[process],scales): tty.setScaleFactor(factor,mcCorrs=False)
    def getYields(self,cuts,process=None,nodata=False,makeSummary=False,noEntryLine=False):
        if self._groupsToNormalize: self._normalizeGroups()
        ## first figure out what we want to do
        tasks = []
        for key,ttys in self._allData.iteritems():
            if key == 'data' and nodata: continue
            if process != None and key != process: continue
            for tty in ttys:
                tasks.append((key,tty,cuts,noEntryLine,None))
        ## then do the work
        if self._options.splitFactor > 1 or  self._options.splitFactor == -1:
            tasks = self._splitTasks(tasks)
        retlist = self._processTasks(_runYields, tasks,name="yields")
        ## then gather results with the same process
        mergemap = {}
        for (k,v) in retlist: 
            if k not in mergemap: mergemap[k] = []
            mergemap[k].append(v)
        ## and finally merge them
        ret = dict([ (k,mergeReports(v)) for k,v in mergemap.iteritems() ])

        rescales = []
        self.compilePlotScaleMap(self._options.plotscalemap,rescales)
        for p,v in ret.items():
            for regexp in rescales:
                if re.match(regexp[0],p): ret[p]=[v[0], [x*regexp[1] for x in v[1]]]

        regroups = [] # [(compiled regexp,target)]
        self.compilePlotMergeMap(self._options.plotmergemap,regroups)
        for regexp in regroups: ret = self.regroupReports(ret,regexp)

        # if necessary project to different lumi, energy,
        if self._projection:
            self._projection.scaleReport(ret)
        # and comute totals
        if makeSummary:
            allSig = []; allBg = []
            for (key,val) in ret.iteritems():
                if key != 'data':
                    if self._isSignal[key]: allSig.append(ret[key])
                    else: allBg.append(ret[key])
            if self._signals and not ret.has_key('signal') and len(allSig) > 0:
                ret['signal'] = mergeReports(allSig)
            if self._backgrounds and not ret.has_key('background') and len(allBg) > 0:
                ret['background'] = mergeReports(allBg)
        return ret
    def getYieldsHN(self,cuts,process=None,nodata=False,makeSummary=False,noEntryLine=False,addUncertainties=True):
        if self._groupsToNormalize: self._normalizeGroups()
        report = []; cut = ""
        cutseq = [ ['entry point','1'] ]
        if noEntryLine: cutseq = []
        sequential = False
        if self._options.nMinusOne or self._options.nMinusOneInverted: 
            if self._options.nMinusOneSelection:
                cutseq = cuts.nMinusOneSelectedCuts(self._options.nMinusOneSelection,inverted=self._options.nMinusOneInverted)
            else:
                cutseq = cuts.nMinusOneCuts(inverted=self._options.nMinusOneInverted)
            cutseq += [ ['all',cuts.allCuts()] ]
            sequential = False
        elif self._options.final:
            cutseq = [ ['all', cuts.allCuts()] ]
        else:
            cutseq += cuts.cuts();
            sequential = True
        for cn,cv in cutseq:
            if sequential:
                if cut: cut += " && "
                cut += "(%s)" % cv
            else:
                cut = cv
            report.append((cn,self.getPlotsRaw('yield','1','1,0.5,1.5',cut,process,nodata,makeSummary)))
        formatted_report = []
        for cn,ret in report:
            thisret = {}
            for k,h in ret.iteritems():
                thisret[k]=[h.GetBinContent(1),h.GetBinError(1),h.GetEntries()]
                if addUncertainties:
                    unc = {}
                    for var in h.getVariationList():
                        up,dn = h.getVariation(var)
                        unc[var] = (up.Integral(),dn.Integral())
                    thisret[k].append(copy(unc))
            formatted_report.append((cn,copy(thisret)))
        print formatted_report
        return formatted_report
    def getPlotsRaw(self,name,expr,bins,cut,process=None,nodata=False,makeSummary=False,closeTreeAfter=False):
        return self.getPlots(PlotSpec(name,expr,bins,{}),cut,process=process,nodata=nodata,makeSummary=makeSummary,closeTreeAfter=closeTreeAfter)
    def getPlots(self,plotspec,cut,process=None,nodata=False,makeSummary=False,closeTreeAfter=False):
        if self._groupsToNormalize: self._normalizeGroups()
        allSig = []; allBg = []
        tasks = []
        for key,ttys in self._allData.iteritems():
            if key == 'data' and nodata: continue
            if process != None and key != process: continue
            for tty in ttys:
                if tty.isEmpty(): continue
                tasks.append((key,tty,plotspec,cut,closeTreeAfter,None))
        if self._options.splitFactor > 1 or  self._options.splitFactor == -1:
            tasks = self._splitTasks(tasks)
        retlist = self._processTasks(_runPlot, tasks, name="plot "+plotspec.name) # list of pairs (idkey, result)
                                                                                   # note that a key can appear multiple times if a task is split!
        ## then gather results with the same process
        mergemap = {}
        for (k,v) in retlist: 
            if k not in mergemap: mergemap[k] = []
            mergemap[k].append(v)
        ret = dict([ (k,mergePlots(plotspec.name+"_"+k,v)) for k,v in mergemap.iteritems() ])

        rescales = []
        self.compilePlotScaleMap(self._options.plotscalemap,rescales)
        for p,v in ret.items():
            for regexp in rescales:
                if re.match(regexp[0],p): v.Scale(regexp[1])

        regroups = [] # [(compiled regexp,target)]
        self.compilePlotMergeMap(self._options.plotmergemap,regroups)
        for regexp in regroups: ret = self.regroupPlots(ret,regexp,plotspec)

        # if necessary project to different lumi, energy,
        if self._projection:
            self._projection.scalePlots(ret)

        if makeSummary:
            allSig = [v for k,v in ret.iteritems() if k != 'data'and self._isSignal[k] == True  ]
            allBg  = [v for k,v in ret.iteritems() if k != 'data'and self._isSignal[k] == False ]
            if self._signals and not ret.has_key('signal') and len(allSig) > 0:
                ret['signal'] = mergePlots(plotspec.name+"_signal", allSig)
                ret['signal'].summary = True
            if self._backgrounds and not ret.has_key('background') and len(allBg) > 0:
                ret['background'] = mergePlots(plotspec.name+"_background",allBg)
                ret['background'].summary = True

        if self._options.externalFitResult:
            if not getattr(self,'_postFit',None):
                efrfile = ROOT.TFile.Open(self._options.externalFitResult[0])
                if not efrfile: raise IOError("Error, could not open %s" % self._options.externalFitResult[0])
                fitResults = efrfile.Get(self._options.externalFitResult[1])
                if not fitResults: raise IOError("Error, could not find %s in %s" % (self._options.externalFitResult[1], self._options.externalFitResult[0]))
                efrfile.Close()
                self._postFit = PostFitSetup(fitResult=fitResults)
        if self._options.altExternalFitResults:
            if not getattr(self,'_altPostFits',None):
                self._altPostFits = {}
                for i,(fname, resname) in enumerate(self._options.altExternalFitResults):
                    resalias = resname
                    if "=" in resname: (resalias,resname) = resname.split("=")
                    efrfile = ROOT.TFile.Open(fname)
                    if not efrfile: raise IOError("Error, could not open %s" % fname)
                    fitResults = efrfile.Get(resname)
                    if not fitResults: raise IOError("Error, could not find %s in %s" % (fname,resname))
                    efrfile.Close()
                    print "Loaded fit result %s from %s for fit %s " % (resname,fname,resalias)
                    self._altPostFits[resalias] = PostFitSetup(fitResult=fitResults)
                    if self._options.altExternalFitResultLabels:
                        self._altPostFits[resalias].label = self._options.altExternalFitResultLabels[i]
        if getattr(self, '_postFit', None):
            roofit = roofitizeReport(ret)
            addMyPOIs(roofit, ret, self)
            for k,h in ret.iteritems():
                if k != "data" and h.Integral() > 0:
                    h.setPostFitInfo(self._postFit,True)
            if self._options.externalFitResult and not getattr(self._options, 'externalFitResult_checked', False):
                notfound = False
                for nuis in listAllNuisances(ret):
                    if not self._postFit.params.find(nuis):
                        print "WARNING: nuisance %s is not found in the input fitResult %s" % (nuis, self._options.externalFitResult)
                        notfound = True
                if notfound:
                    print "Available nuisances: ",; self._postFit.params.Print("")
                self._options.externalFitResult_checked = True
                # sanity check of the nuisances
        #print "DONE getPlots at %.2f" % (0.001*(long(ROOT.gSystem.Now()) - _T0))
        return ret
    def prepareForSplit(self):
        fname2tty = defaultdict(list)
        fname2entries = {}
        for key,ttys in self._allData.iteritems():
            for tty in ttys:
                if not tty.hasEntries(useEList=False):
                    #print "For tty %s/%s, I don't have the number of entries" % (tty._name, tty._cname)
                    fname2tty[tty.fname()].append(tty)
                else:
                    fname2entries[tty.fname()] = tty.getEntries(useEList=False)
        if len(fname2tty) and len(fname2entries):
            for fname,entries in fname2entries.iteritems():
                if fname not in fname2tty: continue
                for tty in fname2tty[fname]: tty.setEntries(entries)
                del fname2tty[fname]
        if len(fname2tty):
            retlist = self._processTasks(_runGetEntries, [(k,v[0]) for (k,v) in fname2tty.iteritems()], name="GetEntries")
            for fname, entries in retlist:
                for tty in fname2tty[fname]: tty.setEntries(entries)
    def applyCut(self,cut):
        tasks = []; revmap = {}; ttysNotToRun = []
        for key,ttys in self._allData.iteritems():
            for tty in ttys:
                myttys = [tty]
                for (variation,direction,vtty) in tty.getTTYVariations():
                    if variation.isTrivial(direction): continue # these are never run
                    if variation.changesSelection(direction):
                        myttys.append(vtty)
                    else:
                        ttysNotToRun.append((vtty,tty))
                for itty in myttys:
                    revmap[id(itty)] = itty
                    tasks.append( (id(itty), itty, cut, None) )
        if self._options.splitFactor > 1 or self._options.splitFactor == -1:
            tasks = self._splitTasks(tasks)
        retlist = self._processTasks(_runApplyCut, tasks, name="apply cut "+cut)
        if self._options.splitFactor > 1 or self._options.splitFactor == -1:
            aggregated = {}
            for ttid, elist in retlist:
                if ttid not in aggregated: aggregated[ttid] = elist
                else:                      aggregated[ttid].Add(elist)
            retlist = aggregated.items()
        for ttid, elist in retlist:
            tty = revmap[ttid]
            tty.applyCutAndElist(cut, elist)
        for vtty,tty in ttysNotToRun:
            vtty.applyCutAndElist(*tty.cutAndElist())
    def clearCut(self):
        for key,ttys in self._allData.iteritems():
            for tty in ttys:
                tty.clearCut() 
                for (v,d,vtty) in tty.getTTYVariations():
                    vtty.clearCut()
    def prettyPrint(self,reports,makeSummary=True):
        allSig = []; allBg = []
        for key in reports:
            if key != 'data':
                if self._isSignal[key]: allSig.append((key,reports[key]))
                else: allBg.append((key,reports[key]))
        allSig.sort(key = lambda (n,v): self._rank[n])
        allBg.sort( key = lambda (n,v): self._rank[n])
        table = allSig + allBg
        if makeSummary:
            if len(allSig)>1:
                table.append(('ALL SIG',mergeReports([v for n,v in allSig])))
            if len(allBg)>1:
                table.append(('ALL BKG',mergeReports([v for n,v in allBg])))
        if "data" in reports: table += [ ('DATA', reports['data']) ]
        for fomname in self._options.figureOfMerit:
            fom = FOM_BY_NAME[fomname]
            nrows = len(table[0][1])
            table += [ (fomname, [ (None, [fom(self, reports, row), 0, 0]) for row in xrange(nrows) ] ) ]

        # maximum length of the cut descriptions
        clen = max([len(cut) for cut,yields in table[0][1]]) + 3
        cfmt = "%%-%ds" % clen;

        fmtlen = 10
        nfmtL = "  %8d"
        nfmtS = "  %8.2f" if self._options.weight else nfmtL
        nfmtX = "  %8.4f" if self._options.weight else nfmtL

        if self._options.errors:
            if self._options.txtfmt in ("md","jupyter"):
                nfmtS+=u" &plusmn;%.2f"
                nfmtX+=u" &plusmn;%.4f"
                nfmtL+=u" &plusmn;%.2f"
            else:
                nfmtS+=u" %7.2f"
                nfmtX+=u" %7.4f"
                nfmtL+=u" %7.2f"
            fmtlen+=9
        if self._options.fractions:
            nfmtS+=" %7.1f%%"
            nfmtX+=" %7.1f%%"
            nfmtL+=" %7.1f%%"
            fmtlen+=8

        fmttable = []; fmthead = [h for (h,r) in table]
        for i,(cut,dummy) in enumerate(table[0][1]):
            row = []
            for name,report in table:
                (nev,err,nev_run_upon) = report[i][1]
                den = report[i-1][1][0] if i>0 else 0
                fraction = nev/float(den) if den > 0 else 1
                if self._options.nMinusOne: 
                    fraction = report[-1][1][0]/float(nev) if nev > 0 else 1
                elif self._options.nMinusOneInverted: 
                    fraction = float(nev)/report[-1][1][0] if report[-1][1][0] > 0 else 1
                toPrint = (nev,)
                if self._options.errors:    toPrint+=(err,)
                if self._options.fractions: toPrint+=(fraction*100,)
                if self._options.weight and nev < 1000: row.append( ( nfmtS if nev > 0.2 else nfmtX) % toPrint )
                else                                  : row.append( nfmtL % toPrint )
            fmttable.append((cut,row))
        if self._options.txtfmt == "text":
            print "CUT".center(clen),
            for h in fmthead: 
                if len("   "+h) <= fmtlen:
                    print ("   "+h).center(fmtlen),
                elif len(h) <= fmtlen:
                    print h.center(fmtlen),
                else:
                    print h[:fmtlen],
            print ""
            print "-"*((fmtlen+1)*len(table)+clen)
            for (cut,row) in fmttable:
                print cfmt % cut,
                print " ".join(row)
                print ""
        elif self._options.txtfmt in ("tsv","csv","dsv","ssv","md","jupyter"):
            sep = { 'tsv':"\t", 'csv':",", 'dsv':';', 'ssv':' ', 'md':' | ', 'jupyter':' | ' }[self._options.txtfmt]
            ret = []
            procEscape = {}
            for k,r in table:
                if sep in k:
                    if self._options.txtfmt in ("tsv","ssv"):
                        procEscape[k] = k.replace(sep,"_")
                    else:
                        procEscape[k] = '"'+k.replace('"','""')+'"'
                else:
                    procEscape[k] = k
            if len(table[0][1]) == 1:
                headers = [ "process", "yield" ]
                if self._options.errors: headers.append("uncert")
                if self._options.fractions: headers.append("eff[%]")
                for k,r in table:
                    (nev,err,fraction) = r[0][1][0], r[0][1][1], 1.0
                    toPrint = (nev,)
                    if self._options.errors:    toPrint+=(err,)
                    if self._options.fractions: toPrint+=(fraction*100,)
                    if self._options.weight and nev < 1000: ytxt = ( nfmtS if nev > 0.2 else nfmtX) % toPrint
                    else                                  : ytxt = nfmtL % toPrint
                    ret.append([procEscape[k]]+ytxt.split())
                ret.append("\n")
            else:
                headers = [ "CUT" ] + fmthead
                for cut,row in fmttable: ret.append([cut]+row)
            if self._options.txtfmt in ("md","jupyter"):
                ret.insert(0,headers)
                ret.insert(1,(("---:" if i else "---") for i in xrange(len(headers))))
            ret = "\n".join(sep.join(c) for c in ret) 
            if self._options.txtfmt == "jupyter":
                import IPython.display
                IPython.display.display(IPython.display.Markdown(ret))
            else:
                print ret

    def __str__(self):
        mystr = ""
        for a in self._allData:
            mystr += str(a) + '\n' 
        for a in self._data:
            mystr += str(a) + '\n' 
        for a in self._signals:
            mystr += str(a) + '\n' 
        for a in self._backgrounds:
            mystr += str(a) + '\n'
        return mystr[:-1]
    def processEvents(self,eventLoop,cut):
        for p in self.listProcesses():
            for tty in self._allData[p]:
                tty.processEvents(eventLoop,cut)
    def compilePlotMergeMap(self,inlist,relist):
        for m in inlist:
            to,fro = m.split("=")
            if to[-1] == "+": to = to[:-1]
            else: raise RuntimeError, 'Incorrect plotmergemap format: %s'%m
            to = to.strip()
            for k in fro.split(","):
                relist.append((re.compile(k.strip()+"$"), to))
    def compilePlotScaleMap(self,inlist,relist):
        for m in inlist:
            dset,scale = m.split("=")
            if dset[-1] == "*": dset = dset[:-1]
            else: raise RuntimeError, 'Incorrect plotscalemap format: %s'%m
            relist.append((re.compile(dset.strip()+"$"),float(scale)))
    def regroupReports(self,pmap,regexp):
        patt, to = regexp
        mergemap={}
        for (k,v) in pmap.items():
            k2 = k
            if k2 != to and re.match(patt,k2): k2 = to
            if k2 not in mergemap: mergemap[k2]=[]
            mergemap[k2].append(v)
        return dict([ (k,mergeReports(v)) for k,v in mergemap.iteritems() ])
    def regroupPlots(self,pmap,regexp,pspec):
        patt, to = regexp
        mergemap={}
        for (k,v) in pmap.items():
            k2 = k
            if k2 != to and re.match(patt,k2): k2 = to
            if k2 not in mergemap: mergemap[k2]=[]
            mergemap[k2].append(v)
        for k3 in mergemap:
            mergemap[k3].sort(key=lambda x: k3 not in x.GetName())
        return dict([ (k,mergePlots(pspec.name+"_"+k,v)) for k,v in mergemap.iteritems() ])
    def stylePlot(self,process,plot,pspec,mayBeMissing=False):
        if process in self._allData:
            for tty in self._allData[process]: 
                tty._stylePlot(plot,pspec)
                break
        elif process in self._optionsOnlyProcesses:
            opts = self._optionsOnlyProcesses[process]
            stylePlot(plot, pspec, lambda key,default : opts[key] if key in opts else default)
        elif not mayBeMissing:
            raise KeyError, "Process %r not found" % process
    def _processTasks(self,func,tasks,name=None,chunkTasks=200,verbose=False):
        if verbose:
            timer = ROOT.TStopwatch()
            print "Starting job %s with %d tasks, %d threads" % (name,len(tasks),self._options.jobs)
        if self._options.jobs == 0: 
            retlist = map(func, tasks)
        else:
            from multiprocessing import Pool
            retlist = []
            for i in xrange(0,len(tasks),chunkTasks):
                pool = Pool(self._options.jobs)
                retlist += pool.map(func, tasks[i:(i+chunkTasks)], 1)
                pool.close()
                pool.join()
                del pool
        if verbose:
            print "Done %s in %s s at %.2f " % (name,timer.RealTime(),0.001*(long(ROOT.gSystem.Now()) - _T0))
        return retlist
    def _splitTasks(self,tasks):
        nsplit = self._options.splitFactor
        if nsplit == -1: nsplit = self._options.jobs
        if nsplit <= 1: return tasks
        newtasks = []
        if not self._options.splitDynamic:
            for task in tasks:
                for fsplit in [ (i,nsplit) for i in xrange(nsplit) ]:
                    newtasks.append( tuple( (list(task)[:-1]) + [fsplit] ) )
        else:
            self.prepareForSplit() 
            #print "Original task list has %d entries; split factor %d." % (len(tasks), nsplit)
            maxent = max( task[1].getEntries() for task in tasks )
            grain  = maxent / nsplit # may be optimized
            #print "Largest task has %d entries. Will use %d as grain " % (maxent, grain)
            if grain < 10000: grain = 10000 # avoid splitting too finely
            newtasks_wsize = []
            if self._options.splitSort:
                tasks.sort(key = lambda task: task[1].getEntries(), reverse = True)
                #for s,t in newtasks_wsize: print "\t%9d %s/%s %s" % (s,t[1]._name, t[1]._cname, t[-1])
            for task in tasks:
                tty = task[1]; 
                entries = tty.getEntries()
                chunks  = min(max(1, int(round(entries/grain))), nsplit)
                fsplits = [ (i,chunks) for i in xrange(chunks) ]
                #print "    task %s/%s has %d entries. N/g = %.1f, chunks = %d" % (tty._name, tty._cname, entries, entries/float(grain), chunks)
                for fsplit in fsplits:
                    newtasks.append( tuple( (list(task)[:-1]) + [fsplit] ) )
        #print "New task list has %d entries; actual split factor %.2f" % (len(newtasks), len(newtasks)/float(len(tasks)))
        return newtasks
    def _normalizeGroups(self):
        tasks = []
        for igroup, (ttys, genWName, scale) in enumerate(self._groupsToNormalize):
            for tty in ttys: tasks.append( (igroup, tty, genWName) )
        retlist = self._processTasks(_runSumW, tasks, name="sumw")
        mergemap = defaultdict(float)
        for (igroup,w) in retlist:
            mergemap[igroup] += w
        for (igroup,total_w) in mergemap.iteritems():
            ttys, _, scale = self._groupsToNormalize[igroup]
            for tty in ttys: tty.setScaleFactor("%s*%g" % (scale, 1000.0/total_w))
        self._groupsToNormalize = []

def addMCAnalysisOptions(parser,addTreeToYieldOnesToo=True):
    if addTreeToYieldOnesToo: addTreeToYieldOptions(parser)
    parser.add_option("-j", "--jobs",           dest="jobs", type="int", default=0, help="Use N threads");
    parser.add_option("--split-factor",         dest="splitFactor", type="int", default=0, help="Use N chunks per sample (-1 means to use the same as what passed to -j, which appears to work well in the average case)");
    #parser.add_option("--split-dynamic",         dest="splitDynamic", action="store_true", default=True, help="Make the splitting dynamic (reduce the chunks for small samples)");
    parser.add_option("--split-static",         dest="splitDynamic", action="store_false", default=True, help="Make the splitting dynamic (reduce the chunks for small samples)");
    #parser.add_option("--split-sort",         dest="splitSort", action="store_true", default=True, help="Make the splitting dynamic (reduce the chunks for small samples)");
    parser.add_option("--split-nosort",         dest="splitSort", action="store_false", default=True, help="Make the splitting dynamic (reduce the chunks for small samples)");
    parser.add_option("-P", "--path", dest="path", action="append", type="string", default=[], help="Path to directory with input trees and pickle files. Can supply multiple paths which will be searched in order. (default: ./") 
    parser.add_option("--RP", "--remote-path",   dest="remotePath",  type="string", default=None,      help="path to remote directory with trees, but not other metadata (default: same as path)") 
    parser.add_option("-p", "--process", dest="processes", type="string", default=[], action="append", help="Processes to print (comma-separated list of regexp, can specify multiple ones)");
    parser.add_option("--pg", "--pgroup", dest="premap", type="string", default=[], action="append", help="Group proceses into one. Syntax is '<newname> := (comma-separated list of regexp)', can specify multiple times. Note tahat it is applied _before_ -p, --sp and --xp");
    parser.add_option("--xf", "--exclude-files", dest="filesToExclude", type="string", default=[], action="append", help="Files to exclude (comma-separated list of regexp, can specify multiple ones)");
    parser.add_option("--xp", "--exclude-process", dest="processesToExclude", type="string", default=[], action="append", help="Processes to exclude (comma-separated list of regexp, can specify multiple ones)");
    parser.add_option("--sf", "--swap-files", dest="filesToSwap", type="string", default=[], nargs=2, action="append", help="--swap-files X Y uses file Y instead of X in the MCA");
    parser.add_option("--sp", "--signal-process", dest="processesAsSignal", type="string", default=[], action="append", help="Processes to set as signal (overriding the '+' in the text file)");
    parser.add_option("--float-process", "--flp", dest="processesToFloat", type="string", default=[], action="append", help="Processes to set as freely floating (overriding the 'FreeFloat' in the text file; affects e.g. mcPlots with --fitData)");
    parser.add_option("--fix-process", "--fxp", dest="processesToFix", type="string", default=[], action="append", help="Processes to set as not freely floating (overriding the 'FreeFloat' in the text file; affects e.g. mcPlots with --fitData)");
    parser.add_option("--peg-process", dest="processesToPeg", type="string", default=[], nargs=2, action="append", help="--peg-process X Y make X scale as Y (equivalent to set PegNormToProcess=Y in the mca.txt)");
    parser.add_option("--scale-process", dest="processesToScale", type="string", default=[], nargs=2, action="append", help="--scale-process X Y make X scale by Y (equivalent to add it in the mca.txt)");
    parser.add_option("--process-norm-syst", dest="processesToSetNormSystematic", type="string", default=[], nargs=2, action="append", help="--process-norm-syst X Y sets the NormSystematic of X to be Y (for plots, etc. Overrides mca.txt)");
    parser.add_option("--AP", "--all-processes", dest="allProcesses", action="store_true", help="Include also processes that are marked with SkipMe=True in the MCA.txt")
    parser.add_option("--use-cnames",  dest="useCnames", action="store_true", help="Use component names instead of process names (for debugging)")
    parser.add_option("--project", dest="project", type="string", help="Project to a scenario (e.g 14TeV_300fb_scenario2)")
    parser.add_option("--plotgroup", dest="plotmergemap", type="string", default=[], action="append", help="Group plots into one. Syntax is '<newname> := (comma-separated list of regexp)', can specify multiple times. Note it is applied after plotting.")
    parser.add_option("--scaleplot", dest="plotscalemap", type="string", default=[], action="append", help="Scale plots by this factor (before grouping). Syntax is '<newname> := (comma-separated list of regexp)', can specify multiple times.")
    parser.add_option("-t", "--tree",          dest="tree", default='ttHLepTreeProducerTTH', help="Pattern for tree name");
    parser.add_option("--fom", "--figure-of-merit", dest="figureOfMerit", type="string", default=[], action="append", help="Add this figure of merit to the output table (S/B, S/sqrB, S/sqrSB)")
    parser.add_option("--binname", dest="binname", type="string", default='default', help="Bin name for uncertainties matching and datacard preparation [default]")
    parser.add_option("--unc", dest="variationsFile", type="string", default=None, help="Uncertainty file to be loaded")
    parser.add_option("--su", "--select-uncertainty", dest="uncertaintiesToSelect", type="string", default=[], action="append", help="Uncertainties to select (comma-separated list of regexp, can specify multiple ones); if not specified, select all");
    parser.add_option("--xu", "--exclude-uncertainty", dest="uncertaintiesToExclude", type="string", default=[], action="append", help="Uncertainties to exclude (comma-separated list of regexp, can specify multiple ones)");
    parser.add_option("--efr", "--external-fitResult", dest="externalFitResult", type="string", default=None, nargs=2, help="External fitResult")
    parser.add_option("--aefr", "--alt-external-fitResults", dest="altExternalFitResults", type="string", default=[], nargs=2, action="append", help="External fitResult")
    parser.add_option("--aefrl", "--alt-external-fitResult-labels", dest="altExternalFitResultLabels", type="string", default=[], nargs=1, action="append", help="External fitResult")

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] tree.root cuts.txt")
    addMCAnalysisOptions(parser)
    (options, args) = parser.parse_args()
    if not options.path: options.path = ['./']
    tty = TreeToYield(args[0],options.path[0],options) if ".root" in args[0] else MCAnalysis(args[0],options)
    cf  = CutsFile(args[1],options)
    for cutFile in args[2:]:
        temp = CutsFile(cutFile,options)
        for cut in temp.cuts():
            cf.add(cut[0],cut[1])
    report = tty.getYields(cf)#, process=options.process)
    tty.prettyPrint(report)
