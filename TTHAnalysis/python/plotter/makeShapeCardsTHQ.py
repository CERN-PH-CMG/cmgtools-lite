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
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import listAllNuisances
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import readHistoWithNuisances
from CMGTools.TTHAnalysis.plotter.histoWithNuisances import HistoWithNuisances
from CMGTools.TTHAnalysis.plotter.tree2yield import makeHistFromBinsAndSpec

class ShapeCardMaker:
    """docstring for ShapeCardMaker"""
    def __init__(self, mcafile, cutsfile, var, bins, options, ananame="tHq"):
        self.mcafile = mcafile
        self.cutsfile = cutsfile
        self.var = var
        self.bins = bins
        self.options = options

        self.ananame = ananame

        self.truebinname = self.options.outname or os.path.basename(self.cutsfile).replace(".txt","")
        self.binname = self.truebinname if self.truebinname[0] not in "234" else "%s_%s"%(self.ananame, self.truebinname)

        self.mca = MCAnalysis(mcafile, self.options)
        self.cuts = CutsFile(cutsfile, self.options)

        self.systs = {}
        self.report = {}

    def readReport(self, filename):
        if self.options.verbose > 0:
            print "...reading from %s" % filename
        infile = ROOT.TFile(filename, "read")
        for proc in self.mca.listProcesses(allProcs=True): # ignore SkipMe=True in mca
            variations = self.mca.getProcessNuisances(proc) if proc != "data" else []
            histo = readHistoWithNuisances(infile, "x_%s" % proc, variations, mayBeMissing=True)
            try:
                if histo:
                    if self.options.verbose > 5:
                        print "...read %s (%d entries) from %s" % (histo.raw().GetName(),
                                                                   histo.raw().GetEntries(),
                                                                   filename)
                    self.report[proc] = histo
            except ReferenceError:
                raise RuntimeError("ERROR: Key %s not found in %s" % (proc, filename))

        ## FIXME: Somehow the data_obs entry wasn't created? Fix it by hand:
        if not 'data_obs' in self.report:
            self.report['data_obs'] = self.report['data'].Clone("x_data_obs")

        self.updateAllYields()

    def saveReport(self, filename):
        tfile = ROOT.TFile(filename, "recreate")
        for n,h in self.report.iteritems():
            h.writeToFile(tfile, takeOwnership=False)
        tfile.Close()
        print "...report written to %s" % filename

    def produceReportFromMCA(self):
        report = {}
        print "...producing report"
        
        rawplots = self.mca.getPlotsRaw("x", self.var, self.bins, self.cuts.allCuts(), nodata=self.options.asimov)
        for name,histo in rawplots.iteritems():
            histo.cropNegativeBins()
            report[name] = histo.Clone('x_%s' % name)

        if not self.options.asimov: 
            report['data_obs'] = report['data'].Clone("x_data_obs")

        self.report.update(report)
        self.updateAllYields()

    def updateAllYields(self):
        self.allyields = {p:h.raw().Integral() for p,h in self.report.iteritems()}

    def prepareAsimov(self, signals=None, backgrounds=None):
        if not self.options.asimov:
            print "WARNING: overwriting data_obs with asimov dataset without --asimov option"

        signals = signals or self.mca.listSignals()
        backgrounds = backgrounds or self.mca.listBackgrounds()

        if self.options.asimov in ("b", "bkg", "background", "b-only"):
            asimovprocesses = backgrounds
            print "...preparing background-only Asimov"
        else:
            asimovprocesses = signals + backgrounds
            print "...preparing signal+background Asimov with %s" % repr(signals)

        tomerge = None
        for p in asimovprocesses:
            if p in self.report: 
                if tomerge is None: 
                    tomerge = self.report[p].raw().Clone("x_data_obs")
                    tomerge.SetDirectory(None)
                else:
                    tomerge.Add(self.report[p].raw())

        self.report['data_obs'] = HistoWithNuisances(tomerge)
        self.allyields['data_obs'] = self.report['data_obs'].Integral()

        if self.options.verbose > 1:
            print "...merging %s for asimov dataset ('data_obs')" % repr([x.GetName() for x in tomerge])

    def setProcesses(self, signals=None, backgrounds=None):
        signals = signals or self.mca.listSignals()
        backgrounds = backgrounds or self.mca.listBackgrounds()
        self.processes = []
        self.iproc = {}
        for i,s in enumerate(signals):
            if self.allyields.get(s, 0) == 0: continue
            self.processes.append(s)
            self.iproc[s] = i-len(signals)+1

        for i,b in enumerate(backgrounds):
            if self.allyields.get(b, 0) == 0: continue
            self.processes.append(b)
            self.iproc[b] = i+1

    def setSystematics(self):
        # makes a new list with only the ones that have an effect
        nuisances = sorted(listAllNuisances(self.report))

        self.systs = {}
        for name in nuisances:
            effshape = {}
            isShape = False

            for p in self.processes:
                h = self.report[p]
                n0 = h.Integral()
                if h.hasVariation(name):
                    if isShape or h.isShapeVariation(name):
                        if name.endswith("_lnU"): 
                            raise RuntimeError("Nuisance %s should be lnU but has shape effect on %s" % (name,p))
                        isShape = True

                    variants = list(h.getVariation(name))
                    for hv,d in zip(variants, ('up','down')):
                        k = hv.Integral()/n0
                        if k == 0: 
                            print "Warning: underflow template for %s %s %s %s. Will take the nominal scaled down by a factor 2" % (self.binname, p, name, d)
                            hv.Add(h.raw())
                            hv.Scale(0.5)

                        elif k < 0.2 or k > 5:
                            print "Warning: big shift in template for %s %s %s %s: kappa = %g " % (binname, p, name, d, k)

                    effshape[p] = variants 

            if isShape:
                if options.regularize: 
                    for p in self.processes:
                        self.report[p].regularizeVariation(name,binname=binname)
                self.systs[name] = ("shape", dict((p,"1" if p in effshape else "-") for p in self.processes), effshape)

            else:
                effyield = dict((p,"-") for p in self.processes)
                isNorm = False
                for p,(hup,hdn) in effshape.iteritems():
                    i0 = self.allyields[p]
                    kup, kdn = hup.Integral()/i0, hdn.Integral()/i0
                    if abs(kup*kdn-1)<1e-5:
                        if abs(kup-1)>2e-4:
                            effyield[p] = "%.3f" % kup
                            isNorm = True
                    else:
                        effyield[p] = "%.3f/%.3f" % (kdn,kup)
                        isNorm = True
                if isNorm:
                    if name.endswith("_lnU"):
                        self.systs[name] = ("lnU", effyield, {})
                    else:
                        self.systs[name] = ("lnN", effyield, {})

        return sorted(self.systs.keys())

    def writeDataCard(self, ofilename=None, procnames=None):
        if self.options.verbose:
            print ("...writing datacard")

        if not os.path.exists(self.options.outdir):
            os.mkdir(self.options.outdir)

        procnames = procnames or dict() # use custom process names in case

        nuisances = self.setSystematics()

        ofilename = ofilename or self.binname+".card.txt"
        with open(os.path.join(self.options.outdir, ofilename), 'w') as datacard:
            # datacard.write("## Datacard for cut file %s\n" % self.cutsfile)
            datacard.write("shapes *        * %s x_$PROCESS x_$PROCESS_$SYSTEMATIC\n" % 
                                          ofilename.replace('.card.txt','.input.root'))
            datacard.write('##----------------------------------\n')
            datacard.write('bin         %s\n' % self.binname)
            datacard.write('observation %s\n' % self.allyields['data_obs'])
            datacard.write('##----------------------------------\n')

            klen = max([7, len(self.binname)]+map(len, self.processes))
            kpatt = " %%%ds " % klen
            fpatt = " %%%d.%df " % (klen,3)
            hlen = max([7] + map(len, nuisances))
            hpatt = "%%-%ds " % hlen
            datacard.write('##----------------------------------\n')
            datacard.write(hpatt%'bin'     +"     "+(" ".join([kpatt % self.binname  for p in self.processes]))+"\n")
            datacard.write(hpatt%'process' +"     "+(" ".join([kpatt % procnames.get(p,p) for p in self.processes]))+"\n")
            datacard.write(hpatt%'process' +"     "+(" ".join([kpatt % self.iproc[p] for p in self.processes]))+"\n")
            datacard.write(hpatt%'rate'    +"     "+(" ".join([fpatt % self.allyields[p] for p in self.processes]))+"\n")
            datacard.write('##----------------------------------\n')

            for name in nuisances:
                (kind, effmap, effshape) = self.systs[name]
                datacard.write(('%s %5s' % (hpatt % name,kind)) + " ".join([kpatt % effmap[p] for p in self.processes]) +"\n")

                # for p, (hup,hdn) in effshape.iteritems(): ## FIXME?
                #     towrite.append(hup.Clone("x_%s_%sUp"   % (p,name)))
                #     towrite.append(hdn.Clone("x_%s_%sDown" % (p,name)))

            # for name, effmap in self.systs.iteritems():
            #     datacard.write((hpatt%name+'  lnN') + " ".join([kpatt % effmap[p] for p in self.processes]) +"\n")

            # for name, (effmap0,effmap12,mode) in self.systsEnv.iteritems():
            #     if 'templstat' in name: # Throw out systs that don't apply to any in self.processes
            #         if not any([p in name for p in self.processes]):
            #             continue

            #     if mode in ["templates", "alternateShape", "alternateShapeOnly"]:
            #         datacard.write(hpatt%name+'shape')
            #         datacard.write(" ".join([kpatt % effmap0[p] for p in self.processes]))
            #         datacard.write("\n")

            #     if re.match('envelop.*',mode):
            #         datacard.write(hpatt%(name+'0')+'shape')
            #         datacard.write(" ".join([kpatt % effmap0[p] for p in self.processes]))
            #         datacard.write("\n")

            #     if any([re.match(x+'.*',mode) for x in ["envelop", "shapeOnly"]]):
            #         datacard.write(hpatt%(name+'1')+'shape')
            #         datacard.write(" ".join([kpatt % effmap12[p] for p in self.processes]))
            #         datacard.write("\n")
            #         if "shapeOnly2D" not in mode:
            #             datacard.write(hpatt%(name+'2')+'shape')
            #             datacard.write(" ".join([kpatt % effmap12[p] for p in self.processes]))
            #             datacard.write("\n")
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

        hists_to_store = [h.raw() for n,h in self.report.iteritems() if any([n.startswith(p) for p in self.processes])]
        hists_to_store.append(self.report['data_obs'].raw())
        for hist in hists_to_store:
            if self.options.verbose > 2:
                print "      %-60s %8.3f events" % (hist.GetName(),hist.Integral())

            histname = hist.GetName()
            for orig,repl in procnames.iteritems():
                histname = histname.replace(orig, repl, 1)

            try:
                workspace.WriteTObject(hist, histname)
            except TypeError:
                print "ERROR: could not write histo %s" % histname
        workspace.Close()


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins systs.txt ")
    addMCAnalysisOptions(parser)
    parser.add_option("--od", "--outdir", dest="outdir", type="string",
                      default="shapecards/", help="output name")
    parser.add_option("-v", "--verbose", dest="verbose", type="int",
                      default=1, help="Verbosity level (0 = quiet, 1 = verbose, 2+ = more)")
    parser.add_option("--asimov", dest="asimov", action="store_true", help="Asimov")
    parser.add_option("--infile", dest="infile", type="string",
                      default=None, help="File to read histos from")
    parser.add_option("--savefile", dest="savefile", action="store_true", help="Save histos")
    # parser.add_option("--cp", dest="cp", type="string",
    #                   default=None, help="run for cp phase angles")

    # Added
    parser.add_option("--regularize", dest="regularize", action="store_true", default=False,
                      help="Regularize templates")

    (options, args) = parser.parse_args()
    options.weight = True
    options.final  = True
    options.allProcesses = True
    options.outname = options.binname

    if not os.path.isdir(options.outdir):
        os.mkdir(options.outdir)

    if "/functions_cc.so" not in ROOT.gSystem.GetLibraries():
        ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+"
                                % os.environ['CMSSW_BASE']);

    cardMaker = ShapeCardMaker(mcafile=args[0],
                               cutsfile=args[1],
                               var=args[2],
                               bins=args[3],
                               options=options)

    # import pdb; pdb.set_trace()

    if options.infile != None:
        cardMaker.readReport(options.infile)
    else:
        cardMaker.produceReportFromMCA()

    if options.savefile:
        filename = os.path.join(options.outdir, options.binname+".bare.root")
        cardMaker.saveReport(filename)

    # Split the signal processes into different points (using the first '_')
    # and process all of them separately.
    allsignals = cardMaker.mca.listSignals(allProcs=False) # exclude the systematics variations
    points = sorted(list(set([p.split('_',2)[2] for p in allsignals if 'tHq' in p and not 'promptsub' in p])))
    print "...processing the following signal points: %s" % repr(points)
    signal_names = ['tHq_hww', 'tHq_htt', 'tHq_hzz',
                    'tHW_hww', 'tHW_htt', 'tHW_hzz',
                    'ttH_hww', 'ttH_htt', 'ttH_hzz']
                    # 'WH_hww', 'WH_htt', 'WH_hzz', 'ggH_hzz']

    for point in points:
        # Take the correct signals for this point
        signals = ['tHq_hww_%s'%point, 'tHq_htt_%s'%point, 'tHq_hzz_%s'%point,
                   'tHW_hww_%s'%point, 'tHW_htt_%s'%point, 'tHW_hzz_%s'%point,
                   'ttH_hww_%s'%point, 'ttH_htt_%s'%point, 'ttH_hzz_%s'%point]
                   # 'WH_hww', 'WH_htt', 'WH_hzz', 'ggH_hzz']

        if options.asimov:
            cardMaker.prepareAsimov(signals=signals, backgrounds=cardMaker.mca.listBackgrounds())
        cardMaker.setProcesses(signals=signals, backgrounds=cardMaker.mca.listBackgrounds())
        ofilename = "%s_%s.card.txt" % (cardMaker.binname, point)

        # Remove points from process names in card and input file
        procnames = dict(zip(signals,signal_names))
        cardMaker.writeDataCard(ofilename=ofilename, procnames=procnames)

    sys.exit(0)
