#!/usr/bin/env python
import ROOT
import re
import sys
import os
import os.path
import math
from itertools import product

from CMGTools.TTHAnalysis.plotter.mcAnalysis import MCAnalysis
from CMGTools.TTHAnalysis.plotter.mcAnalysis import CutsFile
from CMGTools.TTHAnalysis.plotter.mcAnalysis import addMCAnalysisOptions
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import mergePlots
from CMGTools.TTHAnalysis.plotter.tree2yield import makeHistFromBinsAndSpec

def mkOneSpline():
    x_vec,y_vec = ROOT.std.vector('double')(), ROOT.std.vector('double')()
    for x in range(10):
        x_vec.push_back(100*x)
        y_vec.push_back(1)
    spline = ROOT.ROOT.Math.Interpolator(x_vec,y_vec);
    spline._x = x_vec
    spline._y = y_vec
    return spline

SPLINES = {
    'ttH' : mkOneSpline(),
    'hww' : mkOneSpline(),
    'hzz' : mkOneSpline(),
    'htt' : mkOneSpline(),
}
def getYieldScale(mass,process):
    if "ttH_" not in process: return 1.0
    scale = SPLINES['ttH'].Eval(mass)
    for dec in "hww","hzz","htt":
        if dec in process:
            scale *= SPLINES[dec].Eval(mass)
            if 'efficiency_'+dec in SPLINES:
                scale *= SPLINES['efficiency_'+dec].Eval(mass)
            break
    return scale

SYSTEMATICS = {
    "fwdJet"           : "fwdjet_eventWeight_40",
    "jec_Up"           : "eventBTagSF_up_jes",
    "jec_Dn"           : "eventBTagSF_down_jes",
    "bTag_LF_Up"       : "eventBTagSF_up_lf",
    "bTag_LF_Dn"       : "eventBTagSF_down_lf",
    "bTag_HF_Up"       : "eventBTagSF_up_hf",
    "bTag_HF_Dn"       : "eventBTagSF_down_hf",
    "bTag_HFStats1_Up" : "eventBTagSF_up_hfstats1",
    "bTag_HFStats1_Dn" : "eventBTagSF_down_hfstats1",
    "bTag_HFStats2_Up" : "eventBTagSF_up_hfstats2",
    "bTag_HFStats2_Dn" : "eventBTagSF_down_hfstats2",
    "bTag_LFStats1_Up" : "eventBTagSF_up_lfstats1",
    "bTag_LFStats1_Dn" : "eventBTagSF_down_lfstats1",
    "bTag_LFStats2_Up" : "eventBTagSF_up_lfstats2",
    "bTag_LFStats2_Dn" : "eventBTagSF_down_lfstats2",
    "bTag_cErr1_Up"    : "eventBTagSF_up_cferr1",
    "bTag_cErr1_Dn"    : "eventBTagSF_down_cferr1",
    "bTag_cErr2_Up"    : "eventBTagSF_up_cferr2",
    "bTag_cErr2_Dn"    : "eventBTagSF_down_cferr2",
    "elLooseUnc_Up"    : "elLooseUnc_2lss_up",
    "elLooseUnc_Dn"    : "elLooseUnc_2lss_dn",
}

def rebin2Dto1D(h, funcstring):
    nbins,fname = funcstring.split(':',1)
    func = getattr(ROOT,fname)
    nbins = int(nbins)
    goodname = h.GetName()
    h.SetName(goodname+"_oldbinning")
    newh = ROOT.TH1D(goodname,h.GetTitle(),nbins,0.5,nbins+0.5)
    x = h.GetXaxis()
    y = h.GetYaxis()
    allowed = range(1,nbins+1)
    if 'TH2' not in h.ClassName(): raise RuntimeError, "Calling rebin2Dto1D on something that is not TH2"
    for i in xrange(x.GetNbins()):
        for j in xrange(y.GetNbins()):
            ibin = int(func(x.GetBinCenter(i+1),y.GetBinCenter(j+1)))
            if ibin not in allowed:
                raise RuntimeError("Binning function gives not admissible result: bin %d is not in %s" % (ibin, repr(allowed)))
            newh.SetBinContent(ibin,newh.GetBinContent(ibin)+h.GetBinContent(i+1,j+1))
            newh.SetBinError(ibin,math.hypot(newh.GetBinError(ibin),h.GetBinError(i+1,j+1)))
    for ibin in range(1,nbins+1):
        if newh.GetBinContent(ibin)<0:
            print 'Warning: cropping to zero bin %d in %s (was %f)'%(ibin,newh.GetName(),newh.GetBinContent(ibin))
            newh.SetBinContent(ibin,0)
    newh.SetLineWidth(h.GetLineWidth())
    newh.SetLineStyle(h.GetLineStyle())
    newh.SetLineColor(h.GetLineColor())
    return newh

class ShapeCardMaker:
    """docstring for ShapeCardMaker"""
    def __init__(self, mcafile, cutsfile, var, bins, systsfiles, options, ananame="tHq"):
        self.mcafile = mcafile
        self.cutsfile = cutsfile
        self.var = var
        self.bins = bins
        self.systsfiles = systsfiles
        self.options = options

        self.ananame = ananame

        self.truebinname = self.options.outname or os.path.basename(self.cutsfile).replace(".txt","")
        self.binname = self.truebinname if self.truebinname[0] not in "234" else "%s_%s"%(self.ananame, self.truebinname)

        self.mca = MCAnalysis(mcafile, self.options)
        self.cuts = CutsFile(cutsfile, self.options)

        self.systs = {}
        self.systsEnv = {}
        self.report = {}

        for sysfile in systsfiles:
            self.parseSystsFile(sysfile)

    def readReport(self, filename):
        if self.options.verbose > 0:
            print "...reading from %s" % filename
        infile = ROOT.TFile(filename, "read")
        for proc in self.mca.listProcesses(allProcs=True): # ignore SkipMe=True in mca
            histo = infile.Get(proc)
            try:
                histo.SetDirectory(0) # will raise ReferenceError if histo doesn't exist
                if self.options.verbose > 5:
                    print "...read %s (%d entries) from %s" % (histo.GetName(),
                                                               histo.GetEntries(),
                                                               filename)
                self.report[proc] = histo
            except ReferenceError:
                raise RuntimeError("ERROR: Key %s not found in %s" % (proc, filename))

    def saveReport(self, filename):
        tfile = ROOT.TFile(filename, "recreate")
        for n,h in self.report.iteritems():
            tfile.WriteTObject(h,n)
        tfile.Close()
        print "...report written to %s" % filename

    def produceReportFromMCA(self, processes=None):
        processes = processes or self.mca.listProcesses(allProcs=True)
        report = {}
        if self.options.verbose > 0:
            print "...producing report"
            print "...running trees for %d processes" % len(processes)
        
#        for proc in processes:
#            ret = self.mca.getPlotsRaw("x", self.var, self.bins,
#                                       self.cuts.allCuts(),
#                                       process=proc,
#                                       nodata=self.options.asimov)
#            assert(len(ret.keys())==1)
#            #for n,h in ret.iteritems():
#            #    print "DEBUG", n, h.GetName(), type(n), type(h)
#            report.update(ret)

        for n,h in self.mca.getPlotsRaw("x", self.var, self.bins, self.cuts.allCuts(), nodata=options.asimov).iteritems(): report[n]=h.raw().Clone('x_%s'%n)

        if not self.options.asimov:
            report['data_obs'] = report['data'].Clone("x_data_obs")
            report['data_obs'].SetDirectory(0)

        self.report.update(report)
        self.updateAllYields()

    def produceReportFromNTuples(self, processes=None, inputfolder=None, cp=None):
        report = {}
        def getVariationsFromNtuple(filename, weight, histname):
            tfile = ROOT.TFile.Open(filename, "read")
            tree = tfile.Get("t")
            histo = makeHistFromBinsAndSpec(name=histname, expr=self.var,
                                            bins=self.bins, plotspec=None)
            tree.Draw("%s>>%s" % (self.var,histname), weight)
            histo.SetDirectory(0)
            tfile.Close()
            if self.options.verbose>2: print "(%d entries)" % histo.GetEntries()
            return histo


        def parse(process):
            weight = "_weight_*(GenHiggsDecayMode=={pdgid})"
            filename = "ntuple_{proc}_{point}.root"

            fields = process.split('_')
            proc,dec = fields[:2]
            rest = '_'.join(fields[2:])

            weight = weight.format(pdgid={"hww":24, "hzz":23, "htt":15}.get(dec))

            if proc in ['tHq', 'tHW']: 

                if cp == None:
                    p1,p2,syst = re.match(r'([mp012357]{1,})_([mp012357]{1,})_?([\w]*)', rest).groups()
                    point = '_'.join([p1,p2])
                    filename = "ntuple_{proc}_{point}.root".format(proc=proc, point=point)

                if cp != None:
                    p1,syst = re.match(r'([mp0123456789]{1,})_?([\w]*)', rest).groups()
                    filename = "ntuple_{proc}_{point}.root".format(proc=proc, point=p1)

            else:
                filename = "ntuple_{proc}.root".format(proc=proc)
                syst = rest

            if syst != '':
                weight += '*(%s)' % SYSTEMATICS.get(syst)

            if '2lss' in self.truebinname:
                if self.truebinname == '2lss_mm': weight += '*(channel==%d)'%(13*13)
                if self.truebinname == '2lss_em': weight += '*(channel==%d)'%(11*13)
                if self.truebinname == '2lss_ee': weight += '*(channel==%d)'%(11*11)
            
            return filename, weight

        for proc in processes:
            if self.options.verbose>2: print "...processing %s, " % proc,
            try:
                filename, weight = parse(proc)
            except ValueError:
                raise RuntimeError("Failed to parse %s"%(proc))
            if self.options.verbose>2: print "using %s and %s" % (filename, weight),
            if not os.path.exists(os.path.join(inputfolder, filename)):
                raise RuntimeError("Missing ntuple file: %s" % os.path.join(inputfolder, filename))
            report[proc] = getVariationsFromNtuple(filename=os.path.join(inputfolder,filename),
                                                   weight=weight, histname="x_%s"%proc)

        self.report.update(report)
        self.updateAllYields()

    def updateAllYields(self):
        self.allyields = {p:h.Integral() for p,h in self.report.iteritems()}

    def prepareAsimov(self, signals=None, backgrounds=None):
        if not self.options.asimov:
            print "WARNING: overwriting data_obs with asimov dataset without --asimov option"

        signals = signals or self.mca.listSignals()
        backgrounds = backgrounds or self.mca.listBackgrounds()
        tomerge = []
        for p in signals + backgrounds:
            if p in self.report:
                tomerge.append(self.report[p])
        self.report['data_obs'] = mergePlots("x_data_obs", tomerge)
        self.report['data_obs'].SetDirectory(0)
        self.allyields['data_obs'] = self.report['data_obs'].Integral()

        if self.options.verbose > 1:
            print "...merging %s for asimov dataset ('data_obs')" % repr([x.GetName() for x in tomerge])

    def setProcesses(self, signals=None, backgrounds=None):
        signals = signals or self.mca.listSignals()
        backgrounds = backgrounds or self.mca.listBackgrounds()
        self.processes = []
        self.iproc = {}
        for i,s in enumerate(signals):
            if self.allyields[s] == 0: continue
            self.processes.append(s)
            self.iproc[s] = i-len(signals)+1

        for i,b in enumerate(backgrounds):
            if self.allyields[b] == 0: continue
            self.processes.append(b)
            self.iproc[b] = i+1

    def parseSystsFile(self, filename):
        if self.options.verbose: print ("...parsing systs file from %s" % filename)
        systs = {}
        systsEnv = {}
        with open(filename, 'r') as sysfile:
            for line in sysfile:
                if re.match("\s*#.*", line): continue
                line = re.sub("#.*","",line).strip()
                if len(line) == 0: continue

                field = [f.strip() for f in line.split(':')]
                if len(field) < 4:
                    raise RuntimeError("Malformed line %s in file %s" % (line.strip(), sysfile))

                # Pure normalization
                elif len(field) == 4 or field[4] == "lnN":
                    (name, procmap, binmap, amount) = field[:4]
                    if re.match(binmap+"$", self.truebinname) == None: continue
                    if name not in systs: systs[name] = []
                    systs[name].append( (re.compile(procmap+"$"), amount) )

                # Shape systematics
                elif field[4] in ["envelop","shapeOnly","templates","templatesShapeOnly",
                                  "alternateShape","alternateShapeOnly"] or '2D' in field[4]:
                    (name, procmap, binmap, amount) = field[:4]
                    if re.match(binmap+"$", self.truebinname) == None: continue
                    if name not in systs: systsEnv[name] = []
                    systsEnv[name].append( (re.compile(procmap+"$"), amount, field[4]) )

                # Bin by bin statistics
                elif field[4] in ["stat_foreach_shape_bins"]:
                    (name, procmap, binmap, amount) = field[:4]
                    if re.match(binmap+"$", self.truebinname) == None: continue
                    if name not in systsEnv: systsEnv[name] = []
                    systsEnv[name].append( (re.compile(procmap+"$"), amount, field[4], field[5].split(',')) )

                else:
                    raise RuntimeError("Unknown systematic type %s" % field[4])

            if self.options.verbose:
                print "...loaded %d systematics from %s" % (len(systs), filename)
                print "...loaded %d envelope systematics from %s" % (len(systsEnv), filename)
        self.systs.update(systs)
        self.systsEnv.update(systsEnv)

    def parseSystematicsEffects(self):
        self.parseNormalizationSysts()
        systsEnv1 = self.parseShapeSysts1()

        if options.binfunction:
            self.doRebinning()
            # self.setProcesses() # Do I need this?

        systsEnv2 = self.parseShapeSysts2()

        self.systsEnv = {}
        self.systsEnv.update(systsEnv1)
        self.systsEnv.update(systsEnv2)

    def parseNormalizationSysts(self):
        if self.options.verbose: print ("...parsing normalization systs")
        for name, systentries in self.systs.iteritems():
            effmap = {}
            for proc in self.mca.listProcesses(allProcs=False):
                effect = "-"
                for (procmap, amount) in systentries:
                    if re.match(procmap, proc):
                        effect = amount

                if self.mca._projection != None and effect not in ["-","0","1"]:
                    if "/" in effect:
                        eff_up, eff_down = effect.split("/")
                        effect = "%.3f/%.3f" % (self.mca._projection.scaleSyst(name, float(eff_up)),
                                                self.mca._projection.scaleSyst(name, float(eff_down)))
                    else:
                        effect = str(self.mca._projection.scaleSyst(name, float(effect)))

                effmap[proc] = effect
            self.systs[name] = effmap

    def parseShapeSysts1(self):
        if self.options.verbose: print ("...parsing envelope and shapeOnly systs")
        systsEnv1 = {}

        for name, systentries in self.systsEnv.iteritems():
            modes = [entry[2] for entry in systentries]
            for _m in modes:
                if _m != modes[0]: raise RuntimeError, "Not supported"

            # do only this before rebinning
            if not (any([re.match(x+'.*', modes[0]) for x in ["envelop","shapeOnly"]])): continue
            effmap0  = {}
            effmap12 = {}
            for proc in self.mca.listProcesses(allProcs=False):
                effect = "-"
                effect0  = "-"
                effect12 = "-"
                for entry in systentries:
                    procmap, amount, mode = entry[:3]
                    if re.match(procmap, proc):
                        effect = amount
                        if mode not in ["templates", "templatesShapeOnly", "alternateShape", "alternateShapeOnly"]:
                            effect = float(amount)

                if (self.mca._projection != None and
                    effect not in ["-", "0", "1", 1.0, 0.0] and
                    type(effect) == type(1.0)):
                    effect = self.mca._projection.scaleSyst(name, effect)

                if effect == "-" or effect == "0":
                    effmap0[proc]  = "-"
                    effmap12[proc] = "-"
                    continue

                if any([re.match(x+'.*',mode) for x in ["envelop","shapeOnly"]]):
                    nominal = self.report[proc]
                    p0up = nominal.Clone(nominal.GetName()+"_"+name+"0Up"  )
                    p0up.Scale(effect)
                    p0dn = nominal.Clone(nominal.GetName()+"_"+name+"0Down")
                    p0dn.Scale(1.0/effect)
                    p1up = nominal.Clone(nominal.GetName()+"_"+name+"1Up"  )
                    p1dn = nominal.Clone(nominal.GetName()+"_"+name+"1Down")
                    p2up = nominal.Clone(nominal.GetName()+"_"+name+"2Up"  )
                    p2dn = nominal.Clone(nominal.GetName()+"_"+name+"2Down")
                    nbinx = nominal.GetNbinsX()
                    xmin = nominal.GetXaxis().GetBinCenter(1)
                    xmax = nominal.GetXaxis().GetBinCenter(nbinx)

                    if '2D' in mode:
                        if 'TH2' not in nominal.ClassName():
                            raise RuntimeError, 'Trying to use 2D shape systs on a 1D histogram'

                        nbiny = nominal.GetNbinsY()
                        ymin = nominal.GetYaxis().GetBinCenter(1)
                        ymax = nominal.GetYaxis().GetBinCenter(nbiny)

                    c1def = lambda x: 2*(x-0.5) # straight line from (0,-1) to (1,+1)
                    c2def = lambda x: 1 - 8*(x-0.5)**2 # parabola through (0,-1), (0.5,~1), (1,-1)

                    if '2D' not in mode:
                        if 'TH1' not in nominal.ClassName():
                            raise RuntimeError('Trying to use 1D shape systs on a 2D histogram %s %s'
                                                % (nominal.ClassName(), nominal.GetName()))

                        for b in xrange(1,nbinx+1):
                            x = (nominal.GetBinCenter(bx)-xmin)/(xmax-xmin)
                            c1 = c1def(x)
                            c2 = c2def(x)
                            p1up.SetBinContent(b, p1up.GetBinContent(b) * pow(effect,+c1))
                            p1dn.SetBinContent(b, p1dn.GetBinContent(b) * pow(effect,-c1))
                            p2up.SetBinContent(b, p2up.GetBinContent(b) * pow(effect,+c2))
                            p2dn.SetBinContent(b, p2dn.GetBinContent(b) * pow(effect,-c2))

                    else:
                        # e.g. shapeOnly2D_1.25X_0.83Y with effect == 1 will do an anti-correlated shape
                        # distortion of the x and y axes by 25% and -20% respectively
                        parsed = mode.split('_')
                        if len(parsed) != 3 or parsed[0] != "shapeOnly2D" or effect != 1:
                            raise RuntimeError('Incorrect option parsing for shapeOnly2D: %s %s' % (mode, effect))

                        effectX = float(parsed[1].strip('X'))
                        effectY = float(parsed[2].strip('Y'))
                        for bx in xrange(1,nbinx+1):
                            for by in xrange(1,nbiny+1):
                                x = (nominal.GetXaxis().GetBinCenter(bx)-xmin)/(xmax-xmin)
                                y = (nominal.GetYaxis().GetBinCenter(by)-ymin)/(ymax-ymin)
                                c1X = c1def(x)
                                c2X = c2def(x)
                                c1Y = c1def(y)
                                c2Y = c2def(y)
                                p1up.SetBinContent(bx,by, p1up.GetBinContent(bx,by) * pow(effectX,+c1X) * pow(effectY,+c1Y))
                                p1dn.SetBinContent(bx,by, p1dn.GetBinContent(bx,by) * pow(effectX,-c1X) * pow(effectY,-c1Y))
                                p2up.SetBinContent(bx,by, nominal.GetBinContent(bx,by))
                                p2dn.SetBinContent(bx,by, nominal.GetBinContent(bx,by))

                    try:
                        p1up.Scale(nominal.Integral()/p1up.Integral())
                        p1dn.Scale(nominal.Integral()/p1dn.Integral())
                        p2up.Scale(nominal.Integral()/p2up.Integral())
                        p2dn.Scale(nominal.Integral()/p2dn.Integral())
                    except ZeroDivisionError:
                        print "ERROR: Zero integral for %s %s %s" % (name, proc, repr([x.GetName() for x in [p1up, p1dn, p2up, p2dn]]))

                    if "shapeOnly" not in mode:
                        self.report[proc+"_"+name+"0Up"]   = p0up
                        self.report[proc+"_"+name+"0Down"] = p0dn
                        effect0 = "1"

                    self.report[proc+"_"+name+"1Up"]   = p1up
                    self.report[proc+"_"+name+"1Down"] = p1dn
                    effect12 = "1"

                    # useful for plotting
                    for h in [p0up, p0dn, p1up, p1dn, p2up, p2dn]:
                        h.SetFillStyle(0); h.SetLineWidth(2)
                    for h in p1up, p1dn: h.SetLineColor(4)
                    for h in p2up, p2dn: h.SetLineColor(2)

                effmap0[proc]  = effect0
                effmap12[proc] = effect12
            systsEnv1[name] = (effmap0,effmap12,mode)

        return systsEnv1

    def doRebinning(self):
        if self.options.verbose: print ("...rebinning")
        newhistos = {}
        for histo in self.report.values():
            oldname = histo.GetName()
            newhistos[oldname   ] = rebin2Dto1D(histo, self.options.binfunction)

        for n,h in self.report.iteritems():
            self.report[n] = newhistos[h.GetName().replace('_oldbinning','')]

        # Yields might have changed when cropping bins with
        # negative content to zero
        self.updateAllYields()

    def parseShapeSysts2(self):
        if self.options.verbose: print ("...parsing remaining shape systs")
        systsEnv2 = {}
        for name, systentries in self.systsEnv.iteritems():
            modes = [entry[2] for entry in systentries]
            for _m in modes:
                if _m != modes[0]: raise RuntimeError("Not supported")

            # do only this before rebinning
            if (any([re.match(x+'.*', modes[0]) for x in ["envelop","shapeOnly"]])): continue

            effmap0  = {}
            effmap12 = {}
            for proc in self.mca.listProcesses(allProcs=False):
                effect = "-"
                effect0  = "-"
                effect12 = "-"
                for entry in systentries:
                    procmap,amount,mode = entry[:3]
                    if re.match(procmap, proc):
                        effect = amount
                        if mode not in ["templates", "templatesShapeOnly", "alternateShape", "alternateShapeOnly"]:
                            effect = float(amount)
                        morefields = entry[3:]

                if (self.mca._projection != None and
                    effect not in ["-", "0", "1", 1.0, 0.0] and
                    type(effect) == type(1.0)):
                    effect = self.mca._projection.scaleSyst(name, effect)

                if effect == "-" or effect == "0":
                    effmap0[proc]  = "-"
                    effmap12[proc] = "-"
                    continue

                if mode in ["stat_foreach_shape_bins"]:
                    if self.mca._projection != None:
                        raise RuntimeError('mca._projection.scaleSystTemplate not implemented in '
                                           'the case of stat_foreach_shape_bins')

                    nominal = self.report[proc]
                    if 'TH1' in nominal.ClassName():
                        for binx in xrange(1,nominal.GetNbinsX()+1):
                            for binmatch in morefields[0]:
                                if re.match(binmatch+"$",'%d'%binx):
                                    if (nominal.GetBinContent(binx) == 0 or
                                        nominal.GetBinError(binx) == 0):
                                        if nominal.Integral() != 0:
                                            print ("WARNING: for process %s in truebinname %s, "
                                                   "bin %d has zero yield or zero error." % (proc,self.truebinname,binx))
                                        break

                                    if (effect*nominal.GetBinError(binx) < 0.1*math.sqrt(nominal.GetBinContent(binx)+0.04)):
                                        if self.options.verbose > 2:
                                            print ('    Skipping stat_foreach_shape_bins %s %d '
                                                   'because it is irrelevant'%(proc,binx))
                                        break

                                    p0Up = nominal.Clone("%s_%s_%s_%s_bin%dUp" % (nominal.GetName(),name,self.truebinname,proc,binx))
                                    p0Dn = nominal.Clone("%s_%s_%s_%s_bin%dDown" % (nominal.GetName(),name,self.truebinname,proc,binx))
                                    p0Up.SetBinContent(binx, nominal.GetBinContent(binx)+effect*nominal.GetBinError(binx))
                                    p0Dn.SetBinContent(binx, nominal.GetBinContent(binx)**2/p0Up.GetBinContent(binx))
                                    self.report[str(p0Up.GetName())[2:]] = p0Up
                                    self.report[str(p0Dn.GetName())[2:]] = p0Dn

                                    effmap0  = {_p:"1" if _p==proc else "-" for _p in self.mca.listProcesses(allProcs=False)}
                                    effmap12 = {_p:"1" if _p==proc else "-" for _p in self.mca.listProcesses(allProcs=False)}
                                    systsEnv2["%s_%s_%s_bin%d"%(name,self.truebinname,proc,binx)] = (effmap0, effmap12, "templates")
                                    break # otherwise you apply more than once to the same bin if more regexps match

                    elif 'TH2' in nominal.ClassName():
                        for binx, biny in product(xrange(1, nominal.GetNbinsX()+1),
                                                  xrange(1, nominal.GetNbinsY()+1)):
                            for binmatch in morefields[0]:
                                if re.match(binmatch+"$", '%d,%d' % (binx, biny)):
                                    if (nominal.GetBinContent(binx,biny) == 0 or
                                        nominal.GetBinError(binx,biny) == 0):
                                        if nominal.Integral() != 0:
                                            print ("WARNING: for process %s in truebinname %s, "
                                                   "bin %d,%d has zero yield or zero error." %
                                                       (proc,self.truebinname,binx,biny))
                                        break

                                    if (effect*nominal.GetBinError(binx,biny) <
                                        0.1*math.sqrt(nominal.GetBinContent(binx,biny)+0.04) ):
                                        if self.options.verbose:
                                            print ('skipping stat_foreach_shape_bins %s %d,%d '
                                                   'because it is irrelevant' % (proc, binx, biny))
                                        break
                                    p0Up = nominal.Clone("%s_%s_%s_%s_bin%d_%dUp"% (nominal.GetName(),name,self.truebinname,proc,binx,biny))
                                    p0Dn = nominal.Clone("%s_%s_%s_%s_bin%d_%dDown"% (nominal.GetName(),name,self.truebinname,proc,binx,biny))
                                    p0Up.SetBinContent(binx,biny,nominal.GetBinContent(binx,biny)+effect*nominal.GetBinError(binx,biny))
                                    p0Dn.SetBinContent(binx,biny,nominal.GetBinContent(binx,biny)**2/p0Up.GetBinContent(binx,biny))
                                    self.report[str(p0Up.GetName())[2:]] = p0Up
                                    self.report[str(p0Dn.GetName())[2:]] = p0Dn

                                    effmap0  = {_p:"1" if _p==proc else "-" for _p in self.mca.listProcesses(allProcs=False)}
                                    effmap12 = {_p:"1" if _p==proc else "-" for _p in self.mca.listProcesses(allProcs=False)}
                                    systsEnv2["%s_%s_%s_bin%d_%d"%(name,self.truebinname,proc,binx,biny)] = (effmap0, effmap12, "templates")
                                    break # otherwise you apply more than once to the same bin if more regexps match

                elif mode in ["templates", "templatesShapeOnly"]:
                    nominal = self.report[proc]
                    p0Up = self.report["%s_%s_Up" % (proc, effect)]
                    p0Dn = self.report["%s_%s_Dn" % (proc, effect)]
                    if not p0Up or not p0Dn:
                        raise RuntimeError, "Missing templates %s_%s_(Up,Dn) for %s" % (proc,effect,name)
                    p0Up.SetName("%s_%sUp"   % (nominal.GetName(),name))
                    p0Dn.SetName("%s_%sDown" % (nominal.GetName(),name))
                    if p0Up.Integral()<=0 or p0Dn.Integral()<=0:
                        if p0Up.Integral()<=0 and p0Dn.Integral()<=0:
                            raise RuntimeError('ERROR: both template variations have negative or zero integral: '
                                               '%s, Nominal %f, Up %f, Down %f' % (proc, nominal.Integral(),
                                                                                   p0Up.Integral(), p0Dn.Integral()))
                        print ('Warning: I am going to fix a template prediction that would have '
                               'negative or zero integral: %s, Nominal %f, Up %f, Down %f' % (proc,nominal.Integral(),
                                                                                   p0Up.Integral(),p0Dn.Integral()))
                        for b in xrange(1,nominal.GetNbinsX()+1):
                            y0 = nominal.GetBinContent(b)
                            yA = p0Up.GetBinContent(b) if p0Up.Integral()>0 else p0Dn.GetBinContent(b)
                            yM = y0
                            if (y0 > 0 and yA > 0):
                                yM = y0*y0/yA
                            elif yA == 0:
                                yM = 2*y0
                            if p0Up.Integral()>0: p0Dn.SetBinContent(b, yM)
                            else: p0Up.SetBinContent(b, yM)
                        print 'The integral is now: %s, Nominal %f, Up %f, Down %f'%(proc,nominal.Integral(),p0Up.Integral(),p0Dn.Integral())
                    if mode == 'templatesShapeOnly':
                        p0Up.Scale(nominal.Integral()/p0Up.Integral())
                        p0Dn.Scale(nominal.Integral()/p0Dn.Integral())
                    self.report[str(p0Up.GetName())[2:]] = p0Up
                    self.report[str(p0Dn.GetName())[2:]] = p0Dn
                    effect0  = "1"
                    effect12 = "-"
                    if self.mca._projection != None:
                        self.mca._projection.scaleSystTemplate(name,nominal,p0Up)
                        self.mca._projection.scaleSystTemplate(name,nominal,p0Dn)
                elif mode in ["alternateShape", "alternateShapeOnly"]:
                    nominal = self.report[proc]
                    alternate = self.report["%s_%s"%(proc,effect)]
                    if self.mca._projection != None:
                        self.mca._projection.scaleSystTemplate(name,nominal,alternate)
                    alternate.SetName("%s_%sUp" % (nominal.GetName(),name))
                    if mode == "alternateShapeOnly":
                        alternate.Scale(nominal.Integral()/alternate.Integral())
                    mirror = nominal.Clone("%s_%sDown" % (nominal.GetName(),name))
                    for b in xrange(1,nominal.GetNbinsX()+1):
                        y0 = nominal.GetBinContent(b)
                        yA = alternate.GetBinContent(b)
                        yM = y0
                        if (y0 > 0 and yA > 0):
                            yM = y0*y0/yA
                        elif yA == 0:
                            yM = 2*y0
                        mirror.SetBinContent(b, yM)
                    if mode == "alternateShapeOnly":
                        # keep same normalization
                        mirror.Scale(nominal.Integral()/mirror.Integral())
                    else:
                        # mirror normalization
                        mnorm = (nominal.Integral()**2)/alternate.Integral()
                        mirror.Scale(mnorm/alternate.Integral())
                    self.report[str(alternate.GetName())[2:]] = alternate
                    self.report[str(mirror.GetName())[2:]] = mirror
                    effect0  = "1"
                    effect12 = "-"
                effmap0[proc]  = effect0
                effmap12[proc] = effect12
            if mode not in ["stat_foreach_shape_bins"]: systsEnv2[name] = (effmap0,effmap12,mode)

        return systsEnv2

    def writeDataCard(self, ofilename=None, procnames=None):
        if self.options.verbose: print ("...writing datacard")
        myyields = {k:v for (k,v) in self.allyields.iteritems()} # doesn't this just copy the dict?
        if not os.path.exists(self.options.outdir):
            os.mkdir(self.options.outdir)

        procnames = procnames or dict() # use custom process names in case

        ofilename = ofilename or self.binname+".card.txt"
        with open(os.path.join(self.options.outdir, ofilename), 'w') as datacard:
            datacard.write("## Datacard for cut file %s\n" % self.cutsfile)
            datacard.write("shapes *        * %s x_$PROCESS x_$PROCESS_$SYSTEMATIC\n" % 
                                          ofilename.replace('.card.txt','.input.root'))
            datacard.write('##----------------------------------\n')
            datacard.write('bin         %s\n' % self.binname)
            datacard.write('observation %s\n' % myyields['data_obs'])
            datacard.write('##----------------------------------\n')

            klen = max([7, len(self.binname)]+[len(p) for p in self.processes])
            kpatt = " %%%ds " % klen
            fpatt = " %%%d.%df " % (klen,3)

            hlen = max([7] + [len(n) for n in self.systs.keys()+self.systsEnv.keys()])
            hpatt = "%%-%ds " % hlen
            datacard.write('##----------------------------------\n')
            datacard.write(hpatt%'bin'     +"     "+(" ".join([kpatt % self.binname  for p in self.processes]))+"\n")
            datacard.write(hpatt%'process' +"     "+(" ".join([kpatt % procnames.get(p,p) for p in self.processes]))+"\n")
            datacard.write(hpatt%'process' +"     "+(" ".join([kpatt % self.iproc[p] for p in self.processes]))+"\n")
            datacard.write(hpatt%'rate'    +"     "+(" ".join([fpatt % myyields[p]   for p in self.processes]))+"\n")
            datacard.write('##----------------------------------\n')

            for name, effmap in self.systs.iteritems():
                datacard.write((hpatt%name+'  lnN') + " ".join([kpatt % effmap[p] for p in self.processes]) +"\n")

            for name, (effmap0,effmap12,mode) in self.systsEnv.iteritems():
                if 'templstat' in name: # Throw out systs that don't apply to any in self.processes
                    if not any([p in name for p in self.processes]):
                        continue

                if mode in ["templates", "alternateShape", "alternateShapeOnly"]:
                    datacard.write(hpatt%name+'shape')
                    datacard.write(" ".join([kpatt % effmap0[p] for p in self.processes]))
                    datacard.write("\n")

                if re.match('envelop.*',mode):
                    datacard.write(hpatt%(name+'0')+'shape')
                    datacard.write(" ".join([kpatt % effmap0[p] for p in self.processes]))
                    datacard.write("\n")

                if any([re.match(x+'.*',mode) for x in ["envelop", "shapeOnly"]]):
                    datacard.write(hpatt%(name+'1')+'shape')
                    datacard.write(" ".join([kpatt % effmap12[p] for p in self.processes]))
                    datacard.write("\n")
                    if "shapeOnly2D" not in mode:
                        datacard.write(hpatt%(name+'2')+'shape')
                        datacard.write(" ".join([kpatt % effmap12[p] for p in self.processes]))
                        datacard.write("\n")
            datacard.write("\n")
            datacard.write('* autoMCStats 0 0 1\n')
            datacard.write('param_alphaS param 0 1 [-7,7]\n')
            datacard.write('param_mB param 0 1 [-7,7]\n')
            datacard.write('param_mC param 0 1 [-7,7]\n')
            datacard.write('param_mt param 0 1 [-7,7]\n')
            datacard.write('HiggsDecayWidthTHU_hqq param 0 1 [-7,7]\n')
            datacard.write('HiggsDecayWidthTHU_hvv param 0 1 [-7,7]\n')
            datacard.write('HiggsDecayWidthTHU_hll param 0 1 [-7,7]\n')
            datacard.write('HiggsDecayWidthTHU_hgg param 0 1 [-7,7]\n')
            datacard.write('HiggsDecayWidthTHU_hzg param 0 1 [-7,7]\n')
            datacard.write('HiggsDecayWidthTHU_hgluglu param 0 1 [-7,7]\n')

        self.writeInputRootFile(ofilename=ofilename.replace('.card.txt', '.input.root'),
                                procnames=procnames)

    def writeInputRootFile(self, ofilename=None, procnames=None):
        ofilename = ofilename or self.binname+".input.root"
        procnames = procnames or dict() # use custom process names in case
        if self.options.verbose: print ("...writing input root file to %s" %
                                          os.path.join(self.options.outdir, ofilename))
        workspace = ROOT.TFile.Open(os.path.join(self.options.outdir,
                                                 ofilename),
                                    "RECREATE")

        hists_to_store = [h for n,h in self.report.iteritems() if any([n.startswith(p) for p in self.processes])]
        hists_to_store.append(self.report['data_obs'])
        for hist in hists_to_store:
            if self.options.verbose > 2:
                print "      %-60s %8.3f events" % (hist.GetName(),hist.Integral())

            histname = hist.GetName()
            for orig,repl in procnames.iteritems():
                histname = histname.replace(orig, repl, 1)

            workspace.WriteTObject(hist, histname)
        workspace.Close()


if __name__ == '__main__':
    systs = {}

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins systs.txt ")
    addMCAnalysisOptions(parser)
    parser.add_option("-o", "--out", dest="outname", type="string",
                      default=None, help="output name")
    parser.add_option("--od", "--outdir", dest="outdir", type="string",
                      default="shapecards/", help="output name")
    parser.add_option("-v", "--verbose", dest="verbose", type="int",
                      default=0, help="Verbosity level (0 = quiet, 1 = verbose, 2+ = more)")
    parser.add_option("--asimov", dest="asimov", action="store_true", help="Asimov")
    parser.add_option("--2d-binning-function", dest="binfunction", type="string",
                      default=None,
                      help=("Function used to bin the 2D histogram: "
                            "nbins:func, where func(x,y) = bin in [1,nbins]"))
    parser.add_option("--infile", dest="infile", type="string",
                      default=None, help="File to read histos from")
    parser.add_option("--savefile", dest="savefile", type="string",
                      default=None, help="File to save histos to")
    parser.add_option("--ntuple_folder", dest="ntuple_folder", type="string",
                      default=None, help="Read signal trees from ntuples in this directory")
    parser.add_option("--cp", dest="cp", type="string",
                      default=None, help="run for cp phase angles")

    (options, args) = parser.parse_args()
    options.weight = True
    options.final  = True
    options.allProcesses = True

    if not os.path.isdir(options.outdir):
        os.mkdir(options.outdir)

    if "/functions_cc.so" not in ROOT.gSystem.GetLibraries():
        ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+"
                                % os.environ['CMSSW_BASE']);

    cardMaker = ShapeCardMaker(mcafile=args[0],
                               cutsfile=args[1],
                               var=args[2],
                               bins=args[3],
                               systsfiles=args[4:],
                               options=options)

    if options.infile != None:
        cardMaker.readReport(options.infile)
    else:
        all_processes = cardMaker.mca.listProcesses(allProcs=True)
        sig_prods = ['tHq', 'tHW', 'ttH', 'ggH', 'WH']
        sigs_and_systs = [p for p in all_processes if any([p.startswith(x) for x in sig_prods])]
        backgrounds    = [p for p in all_processes if not p in sigs_and_systs]

        if options.ntuple_folder != None:
            cardMaker.produceReportFromNTuples(processes=sigs_and_systs, inputfolder=options.ntuple_folder, cp=options.cp)
            cardMaker.produceReportFromMCA(processes=backgrounds)
        else:
            cardMaker.produceReportFromMCA(processes=all_processes)

    if options.savefile != None:
        cardMaker.saveReport(options.savefile)

    cardMaker.parseSystematicsEffects()

    # import pdb; pdb.set_trace()

    # Split the signal processes into different points (using the first '_')
    # and process all of them separately.
    allsignals = cardMaker.mca.listSignals(allProcs=False) # exclude the systematics variations
#    points = sorted(list(set([p.split('_',2)[2] for p in allsignals if 'tHq' in p])))
    points = ["1_m1"]
    print "...processing the following signal points: %s" % repr(points)
    signal_names = ['tHq_hww', 'tHq_htt', 'tHq_hzz',
                    'tHW_hww', 'tHW_htt', 'tHW_hzz',
                    'ttH_hww', 'ttH_htt', 'ttH_hzz']
                    # 'WH_hww', 'WH_htt', 'WH_hzz', 'ggH_hzz']
    for point in points:
        # Take the correct signals for this point
        signals = ['tHq_hww_%s'%point, 'tHq_htt_%s'%point, 'tHq_hzz_%s'%point,
                   'tHW_hww_%s'%point, 'tHW_htt_%s'%point, 'tHW_hzz_%s'%point,
                   'ttH_hww', 'ttH_htt', 'ttH_hzz']
                   # 'WH_hww', 'WH_htt', 'WH_hzz', 'ggH_hzz']

        if options.asimov:
            cardMaker.prepareAsimov(signals=signals, backgrounds=cardMaker.mca.listBackgrounds())
        cardMaker.setProcesses(signals=signals, backgrounds=cardMaker.mca.listBackgrounds())
        ofilename = "%s_%s.card.txt" % (cardMaker.binname, point)

        # Remove points from process names in card and input file
        procnames = dict(zip(signals,signal_names))
        cardMaker.writeDataCard(ofilename=ofilename, procnames=procnames)

    sys.exit(0)
