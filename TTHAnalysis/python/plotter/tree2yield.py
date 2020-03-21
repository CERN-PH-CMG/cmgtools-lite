#!/usr/bin/env python
from math import ceil, hypot, sqrt
import re
import os, os.path
from array import array

## safe batch mode
import sys
args = sys.argv[:]
sys.argv = ['-b']
import ROOT
sys.argv = args
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gSystem.Load("libpng") # otherwise we may end up with a bogus version

import copy

from CMGTools.TTHAnalysis.plotter.cutsFile import CutsFile
from CMGTools.TTHAnalysis.plotter.mcCorrections import *
from CMGTools.TTHAnalysis.plotter.fakeRate import *
from CMGTools.TTHAnalysis.plotter.uncertaintyFile import *
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import HistoWithNuisances, cropNegativeBins

if "/functions_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

def scalarToVector(x):
    x0 = x
    x = re.sub(r"(LepGood|Lep|JetFwd|Jet|GenTop|SV|PhoGood|TauGood|Tau|Muon|Electron)(\d)_(\w+)", lambda m : "%s_%s[%d]" % (m.group(1),m.group(3),int(m.group(2))-1), x)
    x = re.sub(r"\bmet\b", "met_pt", x)
    return x

class PlotSpec:
    def __init__(self,name,expr,bins,opts,extracut=None):
        self.name = name
        self.expr = expr
        self.bins = bins
        self.opts = opts
        self.extracut = extracut
        self.logs = {}
    def hasOption(self,name):
        return (name in self.opts)
    def getOption(self,name,default=None):
        return self.opts[name] if (name in self.opts) else default
    def setOption(self,name,value):
        self.opts[name] = value
    def setLog(self,name,value):
        self.logs[name] = value
    def allLogs(self):
        return self.logs.iteritems()

def stylePlot(plot,spec,getOption):
        ## Sample specific-options, from self
        if getOption('FillColor',None) != None:
            plot.SetFillColor(getOption('FillColor',0))
            plot.SetFillStyle(getOption('FillStyle',1001))
        else:
            plot.SetFillStyle(0)
            plot.SetLineWidth(getOption('LineWidth',1))
        plot.SetLineColor(getOption('LineColor',1))
        plot.SetLineStyle(getOption('LineStyle',1))
        plot.SetMarkerColor(getOption('MarkerColor',1))
        plot.SetMarkerStyle(getOption('MarkerStyle',20))
        plot.SetMarkerSize(getOption('MarkerSize',1.1))
        ## Plot specific-options, from spec
        if "TH3" not in plot.ClassName():
            plot.GetYaxis().SetTitle(spec.getOption('YTitle',"Events"))
            plot.GetXaxis().SetTitle(spec.getOption('XTitle',spec.name))
            plot.GetXaxis().SetNdivisions(spec.getOption('XNDiv',510))
            plot.GetXaxis().SetMoreLogLabels(True)

def makeBinningProductString(xbins,ybins):
    if xbins[0] == "[":
        if ybins[0] != "[":
            (nbins,ymin,ymax) = map(float, ybins.split(','))
            ybins = "[" + ",".join(map(str, [ymin+i*(ymax-ymin)/nbins for i in xrange(0,int(nbins+1))])) + "]"
        return xbins+"*"+ybins
    elif ybins[0] == "[":
        if xbins[0] != "[":
            (nbins,xmin,xmax) = map(float, xbins.split(','))
            xbins = "[" + ",".join(map(str, [xmin+i*(xmax-xmin)/nbins for i in xrange(0,int(nbins+1))])) + "]"
        return xbins+"*"+ybins
    else:
        return xbins+","+ybins
    
def makeHistFromBinsAndSpec(name,expr,bins,plotspec):
        profile1D      = plotspec.getOption('Profile1D',False) if plotspec != None else False
        profile2D      = plotspec.getOption('Profile2D',False) if plotspec != None else False
        nvars = expr.replace("::","--").count(":")+1
        if nvars == 1 or (nvars == 2 and profile1D):
            if bins[0] == "[":
                edges = [ float(f) for f in bins[1:-1].split(",") ]
                if profile1D: 
                    histo = ROOT.TProfile(name,name,len(edges)-1,array('f',edges))
                else:
                    histo = ROOT.TH1D(name,name,len(edges)-1,array('f',edges))
            else:
                (nb,xmin,xmax) = bins.split(",")
                if profile1D:
                    histo = ROOT.TProfile(name,name,int(nb),float(xmin),float(xmax))
                else:
                    histo = ROOT.TH1D(name,name,int(nb),float(xmin),float(xmax))
        elif nvars == 2 or (nvars == 3 and profile2D):
            if bins[0] == "[":
                xbins, ybins = bins.split("*")
                xedges = [ float(f) for f in xbins[1:-1].split(",") ]
                yedges = [ float(f) for f in ybins[1:-1].split(",") ]
                if profile2D:
                    histo = ROOT.TProfile2D(name,name,len(xedges)-1,array('d',xedges),len(yedges)-1,array('d',yedges))
                else:
                    histo = ROOT.TH2D(name,name,len(xedges)-1,array('f',xedges),len(yedges)-1,array('f',yedges))
            else:
                (nbx,xmin,xmax,nby,ymin,ymax) = bins.split(",")
                if profile2D:
                    histo = ROOT.TProfile2D(name,name,int(nbx),float(xmin),float(xmax),int(nby),float(ymin),float(ymax))
                else:
                    histo = ROOT.TH2D(name,name,int(nbx),float(xmin),float(xmax),int(nby),float(ymin),float(ymax))
        elif nvars == 3:
            ez,ey,ex = [ e.replace("--","::") for e in expr.replace("::","--").split(":") ]
            if bins[0] == "[":
                xbins, ybins, zbins = bins.split("*")
                xedges = [ float(f) for f in xbins[1:-1].split(",") ]
                yedges = [ float(f) for f in ybins[1:-1].split(",") ]
                zedges = [ float(f) for f in zbins[1:-1].split(",") ]
                histo = ROOT.TH3D(name,name,len(xedges)-1,array('f',xedges),len(yedges)-1,array('f',yedges),len(zedges)-1,array('f',zedges))
            else:
                (nbx,xmin,xmax,nby,ymin,ymax,nbz,zmin,zmax) = bins.split(",")
                histo = ROOT.TH3D(name,name,int(nbx),float(xmin),float(xmax),int(nby),float(ymin),float(ymax),int(nbz),float(zmin),float(zmax))
            histo.GetXaxis().SetTitle(ex)
            histo.GetYaxis().SetTitle(ey)
            histo.GetZaxis().SetTitle(ez)
        else:
            raise RuntimeError, "Can't make a plot with %d dimensions" % nvars
        histo.Sumw2()
        return histo

class TreeToYield:
    def __init__(self,root,basepath,options,scaleFactor='1.0',name=None,cname=None,settings={},objname=None,variation_inputs=[],nanoAOD=False):
        self._name  = name  if name != None else root
        self._cname = cname if cname != None else self._name
        self._fname = root
        self._basepath = basepath
        self._isNano = nanoAOD
        self._isInit = False
        self._options = options
        self._objname = objname if objname else options.obj
        self._weight  = (options.weight and 'data' not in self._name )
        self._isdata = 'data' in self._name
        self._weightStringAll  = options.weightStringAll
        self._weightString0  = options.weightString if not self._isdata else "1"
        self._scaleFactor0  = scaleFactor
        self._varScaleFactor = {} 
        self._varScaleFactor0 = {}
        self._fullYield = 0 # yield of the full sample, as if it passed the full skim and all cuts
        self._fullNevt = 0 # number of events of the full sample, as if it passed the full skim and all cuts
        self._settings = settings
        self._isVariation = None
        self._maintty = None
        self._variations = []
        self._ttyVariations = None
        loadMCCorrections(options)            ## make sure this is loaded
        self._mcCorrSourceList = []
        self._FRSourceList = []
        if 'SkipDefaultMCCorrections' in settings: ## unless requested to 
            self._mcCorrSourceList = []            ##  skip them
        else:
            self._mcCorrSourceList = [('_default_',x) for x in globalMCCorrections()]            
        if 'MCCorrections' in settings:
            self._mcCorrs = getattr(self, '_mcCorrs', [])[:] # make copy
            for cfile in settings['MCCorrections'].split(','): 
                self._mcCorrSourceList.append( (cfile,MCCorrections(cfile)) )            
        if 'FakeRate' in settings:
            self._FRSourceList.append( (settings['FakeRate'], FakeRate(settings['FakeRate'],float(self._options.lumi),year=self._options.year) ) )
        for macro in self._options.loadMacro:
            libname = macro.replace(".cc","_cc.so").replace(".cxx","_cxx.so")
            if libname not in ROOT.gSystem.GetLibraries():
                ROOT.gROOT.ProcessLine(".L %s+" % macro);
        self._appliedCut = None
        self._elist = None
        self._entries = None
        self._sumweights = {} if self._isNano else None
        #print "Done creation  %s for task %s in pid %d " % (self._fname, self._name, os.getpid())
        for _var in variation_inputs:
            if _var.isDummy(): continue
            self._variations.append(_var)
        self._makeMCCAndScaleFactor()
    def _makeMCCAndScaleFactor(self):
        self._scaleFactor = self._scaleFactor0 # before any MCC
        mcCorrs = []
        for (fname,mcc) in self._mcCorrSourceList:
            mcCorrs.append(mcc)
        self._mcCorrsInit = mcCorrs[:]
        self._mcCorrs     = mcCorrs
        if mcCorrs and self._scaleFactor and self._scaleFactor != '1.0':
            self._scaleFactor = self.adaptExpr(self._scaleFactor, cut=True)
        self._weightString = self.adaptExpr(self._weightString0, cut=True)
        for (fname,FR) in self._FRSourceList:
            self.applyFR(FR)
        if self._options.forceunweight: self._weight = False
    def getVariations(self):
        return self._variations
    def clearVariations(self):
        self._variations = []
        if hasattr(self, '_ttyVariations'):
            self._ttyVariations = {}
    def getTTYVariations(self):
        if not getattr(self, '_ttyVariations'):
            self.makeTTYVariations()
        ttys = []
        for (var,direction),tty in self._ttyVariations.iteritems():
            ttys.append((var,direction,tty))
        return ttys
    def makeTTYVariations(self):
        ttyVariations = {}
        for var in self.getVariations():
            for direction in (['up','down'] if var.unc_type != "envelope" else ['var%d'%x for x in range(len(var.fakerate))]):
                tty2 = copy.copy(self)
                tty2._name = tty2._name + '_%s_%s'%(var.name,direction)
                tty2._isVariation = (var,direction)
                tty2._variations = []
                if not tty2._isdata:
                    if (var.name,direction) in self._varScaleFactor0: 
                        tty2.setScaleFactor( self._varScaleFactor0[(var.name,direction)])
                if var.getFRToRemove() != None:
                    #print "Passa di qui"
                    tty2._FRSourceList = []
                    found = False
                    for fname,FR in self._FRSourceList:
                        if fname == var.getFRToRemove():
                            found = True
                            continue
                        tty2._FRSourceList.append((fname,FR))
                    if not found: 
                        raise RuntimeError, "Variation %s%s for %s %s would want to remove a FR %s which is not found" % (var.name,direction,self._name,self._cname,var.getFRToRemove())
                    tty2._makeMCCAndScaleFactor()
                tty2.applyFR(var.getFR(direction))
                tty2._maintty = self
                ttyVariations[(var,direction)] = tty2
        self._ttyVariations = ttyVariations
    def variationName(self):
        return "%s %s" % (self._isVariation[0].name,self._isVariation[1]) if self._isVariation else "-"
    def isVariation(self):
        return self._isVariation
    def applyFR(self,FR):
        if FR==None: return
        self._ttyVariations = None # invalidate
        ## add additional weight correction.
        ## note that the weight receives the other mcCorrections, but not itself
        frweight = self.adaptExpr(FR.weight(), cut=True, mcCorrList=self._mcCorrsInit)
        ## modify cuts to get to control region. order is important
        self._weightString = self.adaptExpr(self._weightString, cut=True, mcCorrList=(FR.cutMods()+FR.mods())) + "* (" + frweight + ")"
        self._mcCorrs = self._mcCorrs[:] + FR.cutMods()  + FR.mods()
        self._weight = True
        if self._options.forceunweight: self._weight = False
    def setScaleFactor(self,scaleFactor,mcCorrs=True):
        if (not self._options.forceunweight) and scaleFactor != 1: 
            self._weight = True
        if mcCorrs and self._mcCorrs and scaleFactor and scaleFactor != 1.0:
            # apply MC corrections to the scale factor
            self._scaleFactor0 = scaleFactor
            self._scaleFactor  = self.adaptExpr(scaleFactor, cut=True)
        else:
            self._scaleFactor = scaleFactor
        self._ttyVariations = None # invalidate ttys
                        
    def setVarScaleFactor(self,var,scaleFactor,mcCorrs=True):
        if (not self._options.forceunweight) and scaleFactor != 1: 
            self._weight = True
        if mcCorrs and self._mcCorrs and scaleFactor and scaleFactor != 1.0:
            # apply MC corrections to the scale factor
            self._varScaleFactor0[var] = scaleFactor
            self._varScaleFactor[var]  = self.adaptExpr(scaleFactor, cut=True)
        else:
            self._varScaleFactor[var] = scaleFactor
        self._ttyVariations = None # invalidate ttys
    def getScaleFactor(self):
        return self._scaleFactor
    def setFullYield(self,fullYield):
        self._fullYield = fullYield
    def setFullNevt(self,fullNevt):
        self._fullNevt = fullNevt
    def name(self):
        return self._name
    def cname(self):
        return self._cname
    def fname(self):
        return self._fname
    def basepath(self):
        return self._basepath
    def hasOption(self,name):
        return (name in self._settings)
    def getOption(self,name,default=None):
        if name in self._settings: return self._settings[name]
        return default
    def setOption(self,name,value):
        self._settings[name] = value
    def adaptDataMCExpr(self,expr):
        ret = expr
        if self._isdata:
            ret = re.sub(r'\$MC\{.*?\}', '', re.sub(r'\$DATA\{(.*?)\}', r'\1', expr));
        else:
            ret = re.sub(r'\$DATA\{.*?\}', '', re.sub(r'\$MC\{(.*?)\}', r'\1', expr));
        return ret
    def adaptExpr(self,expr,cut=False,mcCorrList=None):
        _mcCorrList = mcCorrList if mcCorrList != None else self._mcCorrs
        ret = self.adaptDataMCExpr(expr)
        for mcc in _mcCorrList:
            ret = mcc(ret,self._name,self._cname,cut,self._isdata, self._options.year)
        return ret
    def _init(self):
        if "root://" in self._fname:
            ROOT.gEnv.SetValue("TFile.AsyncReading", 1);
#            ROOT.gEnv.SetValue("XNet.Debug", -1); # suppress output about opening connections
            #self._tfile = ROOT.TFile.Open(self._fname+"?readaheadsz=200000") # worse than 65k
            #self._tfile = ROOT.TFile.Open(self._fname+"?readaheadsz=32768") # worse than 65k
            self._tfile = ROOT.TFile.Open(self._fname+"?readaheadsz=65535") # good
            #self._tfile = ROOT.TFile.Open(self._fname+"?readaheadsz=0") #worse than 65k
        else:
            self._tfile = ROOT.TFile.Open(self._fname)
        if not self._tfile: raise RuntimeError, "Cannot open %s\n" % self._fname
        t = self._tfile.Get(self._objname)
        if not t: raise RuntimeError, "Cannot find tree %s in file %s\n" % (self._objname, self._fname)
        self._tree  = t
        #self._tree.SetCacheSize(10*1000*1000)
        if "root://" in self._fname: self._tree.SetCacheSize()
        self._friends = []
        for tf_tree, tf_filename in self._listFriendTrees():
            if not os.path.isfile(tf_filename):
                tf_filename = tf_filename.replace('/pool/ciencias/','/pool/cienciasrw/')
                print '[WARNING]: Falling back to ', tf_filename
            tf = self._tree.AddFriend(tf_tree, tf_filename),
            self._friends.append(tf)
        self._isInit = True
    def _close(self):
        self._isInit = False
        self._tree = None
        self._friends = []
        if self._tfile: self._tfile.Close()
        self._tfile = None
    def _listFriendTrees(self):
        friendOpts = self._options.friendTrees[:]
        friendOpts += (self._options.friendTreesData if self._isdata else self._options.friendTreesMC)
        if 'Friends' in self._settings: friendOpts += self._settings['Friends']
        friendSimpleOpts = self._options.friendTreesSimple[:]
        friendSimpleOpts += (self._options.friendTreesDataSimple if self._isdata else self._options.friendTreesMCSimple)
        if 'FriendsSimple' in self._settings: friendSimpleOpts += [self._settings['FriendsSimple']]
        if self._isNano:
            friendOpts += [ ('Friends', d+"/{cname}_Friend.root") for d in friendSimpleOpts]
        else:
            friendOpts += [ ('sf/t', d+"/evVarFriend_{cname}.root") for d in friendSimpleOpts]
        return [ (tname,fname.format(name=self._name, cname=self._cname, P=self._basepath)) for (tname,fname) in friendOpts ]
    def checkFriendTrees(self, checkFiles=False):
        ok = True
        for (tn,fn) in self._listFriendTrees():
            if not os.path.exists(fn): 
                print "Missing friend for %s %s: %s" % (self._name, self._cname, fn)
                ok = False
            elif checkFiles:
                tftest = ROOT.TFile.Open(fn)
                ftree  = tftest.Get(tn)
                if not ftree:
                    print "Missing friend for %s %s: %s [ tree %s not found ]" % (self._name, self._cname, fn)
                    ok = False
                tftest.Close()
        return ok
    def getTree(self,treeName=None):
        if not self._isInit: self._init()
        if treeName is None:
            return self._tree
        else:
            t = self._tfile.Get(treeName)
            if not t: raise RuntimeError, "Cannot find tree %s in file %s\n" % (treeName, self._fname)
            return t
    def getSumW(self,expr="genEventSumw",closeFileAfterwards=True):
        if self._maintty != None: print "WARNING: getSumW called on a non-main TTY"
        varNormList = []
        for var in [None] + self.getVariations():
            if var == None: 
                exprs = [(expr,0)]
            else: 
                exprs = [('(%s)*(%s)'%(fr._altNorm if (fr and fr._altNorm) else '1',expr), idx) for idx,fr in enumerate(var.fakerate) ]
            for theExpr, idx in exprs:
                if var: 
                    if var.unc_type == 'envelope':
                        sign = 'var%d'%(idx ) 
                    else: 
                        sign = 'up' if idx == 0 else 'down'
                if theExpr == None: theExpr = expr
                if theExpr not in self._sumweights:
                    if self._isNano:
                        if closeFileAfterwards and (not self._isInit):
                            if "root://" in self._fname: ROOT.gEnv.SetValue("XNet.Debug", -1); # suppress output about opening connections
                            tfile = ROOT.TFile.Open(self._fname)
                            if not tfile: raise RuntimeError, "Cannot open %s\n" % self._fname
                            t = tfile.Get("Runs")
                            if not t: raise RuntimeError, "Cannot find tree %s in file %s\n" % ("LuminosityBlocks", self._fname)
                            self._sumweights[theExpr] = _treeSum(t, theExpr)
                            tfile.Close()
                        else:
                            self._sumweights[theExpr] = _treeSum(self.getTree("Runs"), theExpr)
                    else:
                        raise RuntimeError, "getSumW implemented only for NanoAOD for now"
                if var != None: 
                    varNormList.append( ((var.name, sign), theExpr) )
        return self._sumweights[expr], dict( (k,self._sumweights[v]) for (k,v) in varNormList )
    def getEntries(self,useEList=True,closeFileAfterwards=True):
        if useEList and self._elist: 
            return self._elist.GetN()
        if self._entries is None:
            if self._maintty != None:
                self._entries = self._maintty.getEntries()
                return self._entries
            if closeFileAfterwards and (not self._isInit):
                if "root://" in self._fname: ROOT.gEnv.SetValue("XNet.Debug", -1); # suppress output about opening connections
                tfile = ROOT.TFile.Open(self._fname)
                if not tfile: raise RuntimeError, "Cannot open %s\n" % self._fname
                t = tfile.Get(self._objname)
                if not t: raise RuntimeError, "Cannot find tree %s in file %s\n" % (self._objname, self._fname)
                self._entries = t.GetEntries()
            else:
                self._entries = self.getTree().GetEntries()
        return self._entries
    def hasEntries(self,useEList=True):
        if useEList and self._elist:
            return True
        return (self._entries != None)
    def isEmpty(self,useEList=True):
        if useEList and self._elist:
            return self._elist.GetN() == 0
        return self._entries != None and self._entries == 0
    def setEntries(self,entries):
        self._entries = entries
    def getYields(self,cuts,noEntryLine=False,fsplit=None):
        if not self._isInit: self._init()
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
            report.append((cn,self._getYield(self._tree,cut,fsplit=fsplit)))
        return report
    def prettyPrint(self,report):
        # maximum length of the cut descriptions
        clen = max([len(cut) for cut,yields in report]) + 3
        cfmt = "%%-%ds" % clen;

        fmtlen = 12
        nfmtL = "    %8d"
        nfmtS = "    %8.3f" if self._weight else nfmtL

        if self._options.errors:
            nfmtS+=u"%8.3f"
            nfmtL+=u"%8.3f"
            fmtlen+=8
        if self._options.fractions:
            nfmtS+="%7.1f%%"
            nfmtL+="%7.1f%%"
            fmtlen+=8

        print "cut".center(clen),"yield".center(fmtlen)
        print "-"*((fmtlen+1)+clen)
        for i,(cut,(nev,err)) in enumerate(report):
            print cfmt % cut,
            den = report[i-1][1][0] if i>0 else 0
            fraction = nev/float(den) if den > 0 else 1
            if self._options.nMinusOne or self._options.nMinusOneInverted: 
                fraction = report[-1][1][0]/nev if nev > 0 else 1
            toPrint = (nev,)
            if self._options.errors:    toPrint+=(err,)
            if self._options.fractions: toPrint+=(fraction*100,)
            if self._weight and nev < 1000: print nfmtS % toPrint,
            else                          : print nfmtL % toPrint,
            print ""
    def _getCut(self,cut,noweight=False):
        if self._weight and not noweight:
            if self._isdata: cut = "(%s)     *(%s)*(%s)" % (self._weightString,                    self._scaleFactor, self.adaptExpr(cut,cut=True))
            else:            cut = "(%s)*(%s)*(%s)*(%s)" % (self._weightString,self._options.lumi, self._scaleFactor, self.adaptExpr(cut,cut=True))
        else: 
            cut = self.adaptExpr(cut,cut=True)
        if self._options.doS2V:
            cut  = scalarToVector(cut)
        if self._weightStringAll != "1":
            cut = "(%s)*(%s)" % (self._weightStringAll, cut)
        return cut
    def _getYield(self,tree,cut,fsplit=None,cutNeedsPreprocessing=True):
        cut = self._getCut(cut) if cutNeedsPreprocessing else cut
        if self._weight or (self._weightStringAll != "1"):
#            print cut
            ROOT.gROOT.cd()
            if ROOT.gROOT.FindObject("dummy") != None: ROOT.gROOT.FindObject("dummy").Delete()
            histo = ROOT.TH1D("dummy","dummy",1,0.0,1.0); histo.Sumw2()
            (firstEntry, maxEntries) = self._rangeToProcess(fsplit)
            nev = tree.Draw("0.5>>dummy", cut, "goff", maxEntries, firstEntry)
            self.negativeCheck(histo)
            return [ histo.GetBinContent(1), histo.GetBinError(1), nev ]
        else: 
            if self._options.doS2V:
                cut  = scalarToVector(cut)
            (firstEntry, maxEntries) = self._rangeToProcess(fsplit)
            npass = tree.Draw("1",self.adaptExpr(cut,cut=True),"goff", maxEntries, firstEntry);
            return [ npass, sqrt(npass), npass ]
    def _stylePlot(self,plot,spec):
        return stylePlot(plot,spec,self.getOption)
    def getPlot(self,plotspec,cut,fsplit=None,closeTreeAfter=False,noUncertainties=False):
        if self._isVariation == None and noUncertainties == False:
            _wasclosed = not self._isInit
            nominal = self.getPlot(plotspec,cut,fsplit=fsplit,closeTreeAfter=False,noUncertainties=True)
            ret = HistoWithNuisances( nominal )
            variations = {}
            for var,sign,tty2 in self.getTTYVariations():
                if var.name not in variations: variations[var.name] = [var,{}]
                if not var.isTrivial(sign):
                    tty2._isInit = True; tty2._tree = self.getTree()
                    variations[var.name][1][sign] = tty2.getPlot(plotspec,cut,fsplit=fsplit,closeTreeAfter=False,noUncertainties=True)
                    tty2._isInit = False; tty2._tree = None
            for (var,variations) in variations.itervalues():
                if var.unc_type != 'envelope': 
                    if 'up'   not in variations: variations['up']    = var.getTrivial("up",  [nominal,None,None])
                    if 'down' not in variations: variations['down']  = var.getTrivial("down",  [nominal,variations['up'],None])
                    var.postProcess(nominal, [variations['up'], variations['down']])
                else: 
                    var.postProcess(nominal, [v for k,v in variations.iteritems()])
                for k,v in variations.iteritems(): 
                    ret.addVariation(var.name, k, v)

            if closeTreeAfter and _wasclosed: self._close()
            return ret
        ret = self.getPlotRaw(plotspec.name, plotspec.expr, plotspec.bins, cut, plotspec, fsplit=fsplit, closeTreeAfter=closeTreeAfter)
        # fold overflow
        if ret.ClassName() in [ "TH1F", "TH1D" ] :
            n = ret.GetNbinsX()
            if plotspec.getOption('IncludeOverflows',True) and ("TProfile" not in ret.ClassName()):
                ret.SetBinContent(1,ret.GetBinContent(0)+ret.GetBinContent(1))
                ret.SetBinContent(n,ret.GetBinContent(n+1)+ret.GetBinContent(n))
                ret.SetBinError(1,hypot(ret.GetBinError(0),ret.GetBinError(1)))
                ret.SetBinError(n,hypot(ret.GetBinError(n+1),ret.GetBinError(n)))
                ret.SetBinContent(0,0)
                ret.SetBinContent(n+1,0)
                ret.SetBinContent(0,0)
                ret.SetBinContent(n+1,0)
            if plotspec.getOption('IncludeOverflow',False) and ("TProfile" not in ret.ClassName()):
                ret.SetBinContent(n,ret.GetBinContent(n+1)+ret.GetBinContent(n))
                ret.SetBinError(n,hypot(ret.GetBinError(n+1),ret.GetBinError(n)))
                ret.SetBinContent(n+1,0)
                ret.SetBinContent(n+1,0)
            if plotspec.getOption('IncludeUnderflow',False) and ("TProfile" not in ret.ClassName()):
                ret.SetBinContent(1,ret.GetBinContent(0)+ret.GetBinContent(1))
                ret.SetBinError(1,hypot(ret.GetBinError(0),ret.GetBinError(1)))
                ret.SetBinContent(0,0)
                ret.SetBinContent(0,0)
            rebin = plotspec.getOption('rebinFactor',0)
            if plotspec.bins[0] != "[" and rebin > 1 and n > 5:
                while n % rebin != 0: rebin -= 1
                if rebin != 1: ret.Rebin(rebin)
            if plotspec.getOption('Density',False):
                for b in xrange(1,n+1):
                    ret.SetBinContent( b, ret.GetBinContent(b) / ret.GetXaxis().GetBinWidth(b) )
                    ret.SetBinError(   b, ret.GetBinError(b) / ret.GetXaxis().GetBinWidth(b) )
        self._stylePlot(ret,plotspec)
        ret._cname = self._cname
        return ret
    def getWeightForCut(self,cut):
        if self._weight:
            if self._isdata: cut = "(%s)     *(%s)*(%s)" % (self._weightString,                    self._scaleFactor, self.adaptExpr(cut,cut=True))
            else:            cut = "(%s)*(%s)*(%s)*(%s)" % (self._weightString,float(self._options.lumi), self._scaleFactor, self.adaptExpr(cut,cut=True))
        else:
            cut = self.adaptExpr(cut,cut=True)
        if self._weightStringAll != "1":
            cut = "(%s)*(%s)" % (self._weightStringAll, cut)
        return cut
    def getPlotRaw(self,name,expr,bins,cut,plotspec,fsplit=None,closeTreeAfter=False):
        unbinnedData2D = plotspec.getOption('UnbinnedData2D',False) if plotspec != None else False
        perPlotCut = plotspec.getOption('CutString',None) if plotspec != None else None
        if not self._isInit: self._init()
        if self._appliedCut != None:
            if cut != self._appliedCut: 
                print "WARNING, for %s:%s, cut was set to '%s' but now plotting with cut '%s'." % (self._name, self._cname, self._appliedCut, cut)
                #self.clearCut()
            else:
                #print "INFO, for %s:%s, cut was already set to '%s', will use elist for plotting (%d entries)" % (self._name, self._cname, cut, self._elist.GetN())
                self._tree.SetEntryList(self._elist)
                #self._tree.SetEventList(self._elist)
        #print "for %s, %s, does my tree have an elist? %s " % ( self._name, self._cname, "yes" if self._tree.GetEntryList() else "no" )
        cut = self.getWeightForCut('(%s)*(%s)'%(cut,perPlotCut) if perPlotCut else cut)
        expr = self.adaptExpr(expr)
        if self._options.doS2V:
            cut  = scalarToVector(cut)
            expr = scalarToVector(expr)
        #print "DEBUG: ",self._name, self._cname, cut, expr
        (firstEntry, maxEntries) = self._rangeToProcess(fsplit)
        if ROOT.gROOT.FindObject("dummy") != None: ROOT.gROOT.FindObject("dummy").Delete()
        histo = makeHistFromBinsAndSpec("dummy",expr,bins,plotspec)
        canKeys = (histo.ClassName() == "TH1D" and bins[0] != "[")
        if histo.ClassName != "TH2D" or self._name == "data": unbinnedData2D = False
        if unbinnedData2D:
            nent = self._tree.Draw("%s" % expr, cut, "", maxEntries, firstEntry)
            if nent == 0: return ROOT.TGraph(0)
            graph = ROOT.gROOT.FindObject("Graph").Clone(name) #ROOT.gPad.GetPrimitive("Graph").Clone(name)
            return graph
        drawOpt = "goff"
        if plotspec.extracut : 
            cut = '(%s)*(%s)'%(cut, self.adaptExpr(plotspec.extracut ))
        if "TProfile" in histo.ClassName(): drawOpt += " PROF";
        self._tree.Draw("%s>>%s" % (expr,"dummy"), cut, drawOpt, maxEntries, firstEntry)
        if canKeys and histo.GetEntries() > 0 and histo.GetEntries() < self.getOption('KeysPdfMinN',2000) and not self._isdata and self.getOption("KeysPdf",False):
            #print "Histogram for %s/%s has %d entries, so will use KeysPdf " % (self._cname, self._name, histo.GetEntries())
            if "/TH1Keys_cc.so" not in ROOT.gSystem.GetLibraries(): 
                ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/TH1Keys.cc+" % os.environ['CMSSW_BASE']);
            (nb,xmin,xmax) = bins.split(",")
            histo = ROOT.TH1KeysNew("dummyk","dummyk",int(nb),float(xmin),float(xmax),"a",1.0)
            self._tree.Draw("%s>>%s" % (expr,"dummyk"), cut, "goff", maxEntries, firstEntry)
            self.negativeCheck(histo)
            histo = histo.Clone(name)
            histo.SetDirectory(None)
            if closeTreeAfter: self._close()
            return histo
        #elif not self._isdata and self.getOption("KeysPdf",False):
        #else:
        #    print "Histogram for %s/%s has %d entries, so won't use KeysPdf (%s, %s) " % (self._cname, self._name, histo.GetEntries(), canKeys, self.getOption("KeysPdf",False))
        self.negativeCheck(histo)
        histo = histo.Clone(name)
        histo.SetDirectory(None)
        if closeTreeAfter: self._close()
        return histo
    def negativeCheck(self,histo):
        if not self._options.allowNegative and not any([re.match(regexp+'$',self._name) for regexp in self._options.negAllowed]):
            cropNegativeBins(histo)
    def __str__(self):
        mystr = ""
        mystr += str(self._fname) + '\n'
        mystr += str(self._tfile) + '\n'
        mystr += str(self._weight) + '\n'
        mystr += str(self._scaleFactor)
        return mystr
    def processEvents(self,eventLoop,cut):
        if not self._isInit: self._init()
        cut = self.adaptExpr(cut,cut=True)
        if self._options.doS2V:
            cut  = scalarToVector(cut)
            self._tree.vectorTree = True 
        eventLoop.beginComponent(self)
        eventLoop.loop(self._tree, getattr(self._options, 'maxEvents', -1), cut=cut)
        eventLoop.endComponent(self)
    def applyCutAndElist(self,cut,elist):
        if self._appliedCut != None and self._appliedCut != cut: 
            print "WARNING: changing applied cut from %s to %s\n" % (self._appliedCut, cut)
        self._appliedCut = cut
        self._elist = elist
    def cutAndElist(self):
        return (self._appliedCut,self._elist)
    def cutToElist(self,cut,fsplit=None):
        _wasclosed = not self._isInit
        if not self._isInit: self._init()
        if self._weight:
            if self._isdata: cut = "(%s)     *(%s)*(%s)" % (self._weightString,                    self._scaleFactor, self.adaptExpr(cut,cut=True))
            else:            cut = "(%s)*(%s)*(%s)*(%s)" % (self._weightString,float(self._options.lumi), self._scaleFactor, self.adaptExpr(cut,cut=True))
        else: cut = self.adaptExpr(cut,cut=True)
        if self._options.doS2V: cut  = scalarToVector(cut)
        if self._weightStringAll != "1": cut = "(%s)*(%s)" % (self._weightStringAll, cut)
        (firstEntry, maxEntries) = self._rangeToProcess(fsplit)
        self._tree.Draw('>>elist', cut, 'entrylist', maxEntries, firstEntry)
        elist = ROOT.gDirectory.Get('elist')
        if self._tree.GetEntries()==0 and elist==None: elist = ROOT.TEntryList("elist",cut) # empty list if tree is empty, elist would be a ROOT.nullptr TObject otherwise
        elist = ROOT.TEntryList(elist)    
        elist.SetDirectory(None)
        if _wasclosed: self._close()
        return elist
    def clearCut(self):
        #if not self._isInit: raise RuntimeError, "Error, clearing a cut on something that wasn't even initialized"
        self._appliedCut = None
        self._elist = None
        if self._isInit: self._tree.SetEntryList(None)
    def _rangeToProcess(self,fsplit):
        if fsplit != None and fsplit != (0,1):
            allEntries = min(self.getEntries(), self._options.maxEntries)
            chunkSize = int(ceil(allEntries/float(fsplit[1])))
            firstEntry = chunkSize * fsplit[0]
            maxEntries = chunkSize # the last chunk may go beyond the end of the tree, but ROOT stops anyway so we don't care
        else:
            firstEntry = 0
            maxEntries = self._options.maxEntries
        return (firstEntry, maxEntries)
def _copyPlotStyle(self,plotfrom,plotto):
        plotto.SetFillStyle(plotfrom.GetFillStyle())
        plotto.SetFillColor(plotfrom.GetFillColor())
        plotto.SetMarkerStyle(plotfrom.GetMarkerStyle())
        plotto.SetMarkerColor(plotfrom.GetMarkerColor())
        plotto.SetMarkerSize(plotfrom.GetMarkerSize())
        plotto.SetLineStyle(plotfrom.GetLineStyle())
        plotto.SetLineColor(plotfrom.GetLineColor())
        plotto.SetLineWidth(plotfrom.GetLineWidth())
        plotto.GetXaxis().SetTitle(plotfrom.GetXaxis().GetTitle())
        plotto.GetYaxis().SetTitle(plotfrom.GetYaxis().GetTitle())
        plotto.GetZaxis().SetTitle(plotfrom.GetZaxis().GetTitle())
        plotto.GetXaxis().SetNdivisions(plotfrom.GetXaxis().GetNdivisions())
        plotto.GetYaxis().SetNdivisions(plotfrom.GetYaxis().GetNdivisions())
        plotto.GetZaxis().SetNdivisions(plotfrom.GetZaxis().GetNdivisions())

def _treeSum(tree,expr):
    if tree.GetEntries() == 0: return 0.
    ROOT.gROOT.cd()
    if ROOT.gROOT.FindObject("dummy") != None: ROOT.gROOT.FindObject("dummy").Delete()
    histo = ROOT.TH1D("dummy","dummy",1,0.0,1.0); histo.Sumw2()
    tree.Draw("0.5>>dummy", expr, "goff")
    return histo.GetBinContent(1)

def addTreeToYieldOptions(parser):
    parser.add_option("-l", "--lumi",           dest="lumi",   type="string", default="19.7", help="Luminosity (in 1/fb)");
    parser.add_option("-u", "--unweight",       dest="weight",       action="store_false", default=True, help="Don't use weights (in MC events), note weights are still used if a fake rate file is given");
    parser.add_option("--uf", "--unweight-forced",  dest="forceunweight", action="store_true", default=False, help="Do not use weight even if a fake rate file is given.");
    parser.add_option("-W", "--weightString",   dest="weightString", type="string", default="1", help="Use weight (in MC events)");
    parser.add_option("--WA", "--weightAll",   dest="weightStringAll", type="string", default="1", help="Use this weight on all events (including data)");
    parser.add_option("-f", "--final",  dest="final", action="store_true", help="Just compute final yield after all cuts");
    parser.add_option("-e", "--errors",  dest="errors", action="store_true", help="Include uncertainties in the reports");
    parser.add_option("--tf", "--text-format",   dest="txtfmt", type="string", default="text", help="Output format: text, html");
    parser.add_option("-S", "--start-at-cut",   dest="startCut",   type="string", help="Run selection starting at the cut matched by this regexp, included.") 
    parser.add_option("-U", "--up-to-cut",      dest="upToCut",   type="string", help="Run selection only up to the cut matched by this regexp, included.") 
    parser.add_option("-X", "--exclude-cut", dest="cutsToExclude", action="append", default=[], help="Cuts to exclude (regexp matching cut name), can specify multiple times.") 
    parser.add_option("-E", "--enable-cut", dest="cutsToEnable", action="append", default=[], help="Cuts to enable if they were disabled in the cut file (regexp matching cut name), can specify multiple times.") 
    parser.add_option("-I", "--invert-cut",  dest="cutsToInvert",  action="append", default=[], help="Cuts to invert (regexp matching cut name), can specify multiple times.") 
    parser.add_option("-R", "--replace-cut", dest="cutsToReplace", action="append", default=[], nargs=3, help="Cuts to invert (regexp of old cut name, new name, new cut); can specify multiple times.") 
    parser.add_option("-A", "--add-cut",     dest="cutsToAdd",     action="append", default=[], nargs=3, help="Cuts to insert (regexp of cut name after which this cut should go, new name, new cut); can specify multiple times.") 
    parser.add_option("-N", "--n-minus-one", dest="nMinusOne", action="store_true", help="Compute n-minus-one yields and plots")
    parser.add_option("--select-n-minus-one", dest="nMinusOneSelection", type="string", default=None, help="Select which cuts to do N-1 for (comma separated list of regexps)")
    parser.add_option("--NI", "--inv-n-minus-one", dest="nMinusOneInverted", action="store_true", help="Compute n-minus-one yields and plots")
    parser.add_option("--obj", "--objname",    dest="obj", default='tree', help="Pattern for the name of the TTree inside the file");
    parser.add_option("-G", "--no-fractions",  dest="fractions",action="store_false", default=True, help="Don't print the fractions");
    parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename") 
    parser.add_option("--Fs", "--add-friend-simple",    dest="friendTreesSimple",  action="append", default=[], nargs=1, help="Add friends in a directory. The rootfile must be called evVarFriend_{cname}.root and tree must be called 't' in a subdir 'sf' inside the rootfile.") 
    parser.add_option("--FMC", "--add-friend-mc",    dest="friendTreesMC",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to MC only. Can use {name}, {cname} patterns in the treename") 
    parser.add_option("--FD", "--add-friend-data",    dest="friendTreesData",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to data trees only. Can use {name}, {cname} patterns in the treename") 
    parser.add_option("--FMCs", "--add-friend-mc-simple",    dest="friendTreesMCSimple",  action="append", default=[], nargs=1, help="Add friends in a directory to MC only. The rootfile must be called evVarFriend_{cname}.root and tree must be called 't' in a subdir 'sf' inside the rootfile.") 
    parser.add_option("--FDs", "--add-friend-data-simple",    dest="friendTreesDataSimple",  action="append", default=[], nargs=1, help="Add friends in a directory to data only. The rootfile must be called evVarFriend_{cname}.root and tree must be called 't' in a subdir 'sf' inside the rootfile.") 
    parser.add_option("--mcc", "--mc-corrections",    dest="mcCorrs",  action="append", default=[], nargs=1, help="Load the following file of mc to data corrections") 
    parser.add_option("--s2v", "--scalar2vector",     dest="doS2V",    action="store_true", default=False, help="Do scalar to vector conversion") 
    parser.add_option("--neg", "--allow-negative-results",     dest="allowNegative",    action="store_true", default=False, help="If the total yield is negative, keep it so rather than truncating it to zero") 
    parser.add_option("--neglist", dest="negAllowed", action="append", default=[], help="Give process name regexp where negative values are allowed")
    parser.add_option("--max-entries",     dest="maxEntries", default=1000000000, type="int", help="Max entries to process in each tree") 
    parser.add_option("-L", "--load-macro",  dest="loadMacro",   type="string", action="append", default=[], help="Load the following macro, with .L <file>+");


def mergeReports(reports):
    one = copy.deepcopy(reports[0])
    for i,(c,x) in enumerate(one):
        one[i][1][1] = pow(one[i][1][1], 2)
    for two in reports[1:]:
        for i,(c,x) in enumerate(two):
            one[i][1][0] += x[0]
            one[i][1][1] += pow(x[1],2)
            one[i][1][2] += x[2]
    for i,(c,x) in enumerate(one):
        one[i][1][1] = sqrt(one[i][1][1])
    return one

