#!/usr/bin/env python
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *
import re, sys, os, os.path
systs = {}

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins")
addMCAnalysisOptions(parser)
parser.add_option("--od", "--outdir", dest="outdir", type="string", default=None, help="output directory name") 
parser.add_option("--asimov", dest="asimov", type="string", default=None, help="Use an Asimov dataset of the specified kind: including signal ('signal','s','sig','s+b') or background-only ('background','bkg','b','b-only')")
parser.add_option("--bbb", dest="bbb", type="string", default='standard', help="Options for bin-by-bin statistical uncertainties with the specified nuisance name")
parser.add_option("--infile", dest="infile", action="store_true", default=False, help="Read histograms to file")
parser.add_option("--savefile", dest="savefile", action="store_true", default=False, help="Save histos to file")

(options, args) = parser.parse_args()
options.weight = True
options.final  = True

if "/functions_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

mca  = MCAnalysis(args[0],options)
cuts = CutsFile(args[1],options)

truebinname = os.path.basename(args[1]).replace(".txt","") if options.binname == None else options.binname
binname = truebinname if truebinname[0] not in "234" else "ttH_"+truebinname
print binname
outdir  = options.outdir+"/" if options.outdir else ""
if not os.path.exists(outdir): os.mkdir(outdir)

report={}
if options.infile:
    infile = ROOT.TFile(outdir+binname+".bare.root","read")
    for p in mca.listSignals(True)+mca.listBackgrounds(True)+['data']:
        variations = mca.getProcessNuisances(p) if p != "data" else []
        h = readHistoWithNuisances(infile, "x_"+p, variations, mayBeMissing=True)
        if h: report[p] = h
else:
    report = mca.getPlotsRaw("x", args[2], args[3], cuts.allCuts(), nodata=options.asimov) 
    for p,h in report.iteritems(): h.cropNegativeBins()

if options.bbb:
    for p,h in report.iteritems(): 
        h.addBinByBin(namePattern="%s_%s_%s_bin{bin}" % (options.bbb, truebinname, p), conservativePruning = True)

if options.savefile:
    savefile = ROOT.TFile(outdir+binname+".bare.root","recreate")
    for k,h in report.iteritems(): 
        h.writeToFile(savefile, takeOwnership=False)
    savefile.Close()

nuisances = sorted(listAllNuisances(report))

if options.asimov:
    if options.asimov in ("s","sig","signal","s+b"):
        asimovprocesses = mca.listSignals() + mca.listBackgrounds()
    elif options.asimov in ("b","bkg","background", "b-only"):
        asimovprocesses = mca.listBackgrounds()
    else: raise RuntimeError("the --asimov option requires to specify signal/sig/s/s+b or background/bkg/b/b-only")
    tomerge = None
    for p in asimovprocesses:
        if p in report: 
            if tomerge is None: tomerge = report[p].raw().Clone("x_data_obs")
            else: tomerge.Add(report[p].raw())
    report['data_obs'] = tomerge 
else:
    report['data_obs'] = report['data'].raw().Clone("x_data_obs") 


allyields = dict([(p,h.Integral()) for p,h in report.iteritems()])
procs = []; iproc = {}
for i,s in enumerate(mca.listSignals()):
    if s not in allyields: continue
    if allyields[s] == 0: continue
    procs.append(s); iproc[s] = i-len(mca.listSignals())+1
for i,b in enumerate(mca.listBackgrounds()):
    if b not in allyields: continue
    if allyields[b] == 0: continue
    procs.append(b); iproc[b] = i+1
for p in procs: print "%-10s %10.4f" % (p, allyields[p])

systs = {}
for name in nuisances:
    effshape = {}
    isShape = False
    for p in procs:
        h = report[p]
        if h.hasVariation(name):
            if isShape or h.isShapeVariation(name):
                #print "Nuisance %s has a shape effect on process %s" % (name, p)
                isShape = True
            effshape[p] = h.getVariation(name)
    if isShape:
        systs[name] = ("shape", dict((p,"1" if p in effshape else "-") for p in procs), effshape)
    else:
        effyield = dict((p,"-") for p in procs)
        isNorm = False
        for p,(hup,hdn) in effshape.iteritems():
            i0 = allyields[p]
            kup, kdn = hup.Integral()/i0, hdn.Integral()/i0
            if abs(kup*kdn-1)<1e-5:
                if abs(kup-1)>2e-4:
                    effyield[p] = "%.3f" % kup
                    isNorm = True
            else:
                effyield[p] = "%.3f/%.3f" % (kdn,kup)
                isNorm = True
        if isNorm:
            systs[name] = ("lnN", effyield, {})
# make a new list with only the ones that have an effect
nuisances = sorted(systs.keys())


datacard = open(outdir+binname+".card.txt", "w"); 
datacard.write("## Datacard for cut file %s\n"%args[1])
datacard.write("shapes *        * %s.input.root x_$PROCESS x_$PROCESS_$SYSTEMATIC\n" % binname)
datacard.write('##----------------------------------\n')
datacard.write('bin         %s\n' % binname)
datacard.write('observation %s\n' % allyields['data_obs'])
datacard.write('##----------------------------------\n')
klen = max([7, len(binname)]+[len(p) for p in procs])
kpatt = " %%%ds "  % klen
fpatt = " %%%d.%df " % (klen,3)
npatt = "%%-%ds " % max([len('process')]+map(len,nuisances))
datacard.write('##----------------------------------\n')
datacard.write((npatt % 'bin    ')+(" "*6)+(" ".join([kpatt % binname  for p in procs]))+"\n")
datacard.write((npatt % 'process')+(" "*6)+(" ".join([kpatt % p        for p in procs]))+"\n")
datacard.write((npatt % 'process')+(" "*6)+(" ".join([kpatt % iproc[p] for p in procs]))+"\n")
datacard.write((npatt % 'rate   ')+(" "*6)+(" ".join([fpatt % allyields[p] for p in procs]))+"\n")
datacard.write('##----------------------------------\n')
towrite = [ report[p].raw() for p in procs ] + [ report["data_obs"] ]
for name in nuisances:
    (kind,effmap,effshape) = systs[name]
    datacard.write(('%s %5s' % (npatt % name,kind)) + " ".join([kpatt % effmap[p]  for p in procs]) +"\n")
    for p,(hup,hdn) in effshape.iteritems():
        towrite.append(hup.Clone("x_%s_%sUp"   % (p,name)))
        towrite.append(hdn.Clone("x_%s_%sDown" % (p,name)))

workspace = ROOT.TFile.Open(outdir+binname+".input.root", "RECREATE")
for h in towrite:
    workspace.WriteTObject(h,h.GetName())
workspace.Close()

print "Wrote to ",outdir+binname+".input.root"

