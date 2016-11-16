from CMGTools.TTHAnalysis.plotter.mcPlots import *
from math import *

## Utilities

def _plotsToReport(mca,pf,outfile):
    from collections import defaultdict
    yields = defaultdict(list)
    for pspec in pf.plots():
        if pspec.getOption('Density',False): continue
        for proc in mca.listProcesses(allProcs=True):
            hist = outfile.Get(pspec.name + "_" + proc)
            if hist: yields[proc].append((hist.Integral(0, hist.GetNbinsX()+1),
                                          sqrt(sum([hist.GetBinError(b)**2 for b in xrange(1,hist.GetNbinsX()+1)]))))
            else:    yields[proc].append((0,0))
    ret = {}
    for p,ys in yields.iteritems():
        if sum(y[0] for y in ys) == 0: continue
        ret[p] = [ ('all', [ sum(y[0] for y in ys)/len(ys), sum(y[1] for y in ys)/len(ys), 0 ]) ]
    return ret

## Main


from optparse import OptionParser
parser = OptionParser(usage="%prog [options] tree.root cuts.txt IVFCUT MUCUT")
addPlotMakerOptions(parser)
parser.add_option("-i", "--in",  dest="inf",  type="string", default=None, help="in pickle file") 
parser.add_option("-o", "--out", dest="out", type="string", default=None, help="out pickle file") 
parser.add_option("--bgsyst", dest="bgsyst", type="float", default=1.0, help="Background uncertainty");
parser.add_option("--plots", dest="plots", type="string", default=None, help="Also make plots");
(options, args) = parser.parse_args()
userSignal = options.processesAsSignal[:]
options.txtfmt = "tsv"
options.fractions = False

# don't make plots if --pdir is not specified (faster)
if "--pdir" not in sys.argv:
    options.printPlots = ""

if options.inf:
    print "Reading from", options.inf
    import pickle
    (report_ivf, report_mu) = pickle.load(open(options.inf))
else:
    options.allProcesses = True
    options.final = True
    userExcludes = options.processesToExclude[:]
    userEnables  = options.cutsToEnable[:]
    userPlotsSel  = options.plotselect[:]
    userPlotsExcl = options.plotexclude[:]

    if options.plots or options.preFitData:
        options.processesAsSignal = [ "^T[TW].*" ]

        if options.printPlots: 
            mainPrintDir = options.printDir
            for sub in "/ivf", "/softMu", "":
                if not os.path.exists(mainPrintDir+sub): os.system("mkdir -p "+mainPrintDir+sub)
                if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/g/gpetrucc/php/index.php "+mainPrintDir+sub+"/")
        else:
            print "Will not print plots."

        if options.preFitData:
            options.processesToExclude = userExcludes + [ "T[TW]_ivf.*", "T[TW]_softMu.*" ]
            options.plotselect  += [ options.preFitData ]
            options.plotexclude += [ "^SV_.*", "^LepOtherGood_.*" ]
            if not options.processesToFloat:
                print "Will do the default fit, floating TT+TW vs DY"
                options.processesToFloat = [ "T[TW]","DY","VV","WJets" ]
                options.processesToPeg  = [ ("TW","TT"), ("VV","DY"), ("WJets","DY") ]
            mca_all = MCAnalysis(args[0], options)
            cf_all  = CutsFile(args[1], options)
            pf_all  = PlotFile(options.plots, options)

            scales0 = dict((p,mca_all.getScales(p)) for p in mca_all.listSignals() + mca_all.listBackgrounds()) 

            outfile  = ROOT.TFile(options.printDir+"/plots.root" if options.printDir else "plots.root","RECREATE")
            plotter = PlotMaker(outfile,options).run(mca_all,cf_all,pf_all)
            outfile.Close()

            scales2 = dict((p,mca_all.getScales(p)) for p in mca_all.listSignals() + mca_all.listBackgrounds()) 

            inclusiveScales = []
            for p in scales0.iterkeys():
                scale0 = scales0[p][0]
                scale2 = scales2[p][0]
                if scale2 == scale0: continue
                if scale0 not in scale2: raise RuntimeError, "Unparsable scale for %s: %r -> %r" % (p, scale0, scale2) 
                m = re.match(r"\(\(unity\) \* \(([0-9\.e+\-]+)\)\)$", scale2.replace(scale0, "unity"))
                if not m: raise RuntimeError, "Unparsable scale for %s: %r -> %r" % (p, scale0, scale2)
                sf = m.group(1)
                if p in ("TT","TW"): inclusiveScales.append((p+"_.*",sf))
                else:                inclusiveScales.append((p,      sf))
            print "Fit results in the following scale factors: %s" % inclusiveScales
            options.processesToScale += inclusiveScales[:]
            options.preFitData = None

    print "\n === Running IVF Selection (cuts: %r) === " % args[2]
    options.processesToExclude = userExcludes + [ "T[TW]$", "T[TW]_softMu.*" ]
    options.cutsToEnable = userEnables + [ args[2] ]
    mca_ivf = MCAnalysis(args[0],options)
    cf_ivf  = CutsFile(args[1],options)
    if options.plots and options.printPlots:
        options.printDir = mainPrintDir + "/ivf/"
        options.plotselect  = userPlotsSel if userPlotsSel else [ "SV_.*" ]
        options.plotexclude = userPlotsExcl + [ "^LepOtherGood_.*" ]
        pf_ivf  = PlotFile(options.plots, options)
        outfile  = ROOT.TFile(options.printDir+"/plots.root","RECREATE")
        PlotMaker(outfile,options).run(mca_ivf,cf_ivf,pf_ivf)
        report_ivf = _plotsToReport(mca_ivf,pf_ivf,outfile)
        outfile.Close()
    else: # just get yields
        report_ivf = mca_ivf.getYields(cf_ivf)
    mca_ivf.prettyPrint(report_ivf)

    print "\n === Running Soft Mu Selection (cuts: %r) === " % args[3]
    options.processesToExclude = userExcludes + [ "T[TW]$", "T[TW]_ivf.*" ]
    options.cutsToEnable = userEnables + [ args[3] ]
    mca_mu = MCAnalysis(args[0],options)
    cf_mu  = CutsFile(args[1],options)
    if options.plots and options.printPlots:
        options.printDir = mainPrintDir + "/softMu/"
        options.plotselect  = userPlotsSel if userPlotsSel else [ "LepOtherGood_.*" ]
        options.plotexclude = userPlotsExcl + [ "^SV_.*" ]
        pf_mu  = PlotFile(options.plots, options)
        outfile  = ROOT.TFile(options.printDir+"/plots.root","RECREATE")
        PlotMaker(outfile,options).run(mca_mu,cf_mu,pf_mu)
        report_mu = _plotsToReport(mca_mu,pf_mu,outfile)
        outfile.Close()
    else: # just get yields
        report_mu = mca_mu.getYields(cf_mu)
    mca_mu.prettyPrint(report_mu)

    if options.out:
        import pickle
        if "{PD}" in options.out and options.printPlots: 
            options.out = options.out.replace("{PD}", mainPrintDir)
        pickle.dump((report_ivf, report_mu), open(options.out, 'w'))
        print "Saved to", options.out

def hypot3(a,b,c): return sqrt(a**2+b**2+c**2)

signal = userSignal[0] if userSignal else "^T[TW]_.*B$"
sfs = {}
for (what,rep) in ("ivf",report_ivf), ("softMu",report_mu):
    nsig, nbkg, ndata = 0,0,0
    nsige2, nbkge2 = 0,0
    for k,l in rep.iteritems():
        nsel = l[0][1][0]
        if k == "data": ndata += nsel
        elif re.match(signal, k):  
            nsig += nsel
            nsige2 += l[0][1][1]**2
        else: 
            nbkg += nsel
            nbkge2 += l[0][1][1]**2
    sf      = (ndata - nbkg)/nsig
    sf_stat = sqrt(ndata)/nsig
    sf_bkg  = options.bgsyst * nbkg/nsig 
    sf_mcst = sqrt(nsige2+nbkge2)/nsig
    print "SF for %-6s = %.3f +- %.3f (stat) +- %.3f (bg) +- %.3f (mc stat) = %.3f +- %.3f" % (what, sf, sf_stat, sf_bkg, sf_mcst, sf, hypot3(sf_stat, sf_bkg, sf_mcst))
    sfs[what] = (sf, sf_stat, sf_bkg, sf_mcst)

sf_rel  = sfs["ivf"][0]/sfs["softMu"][0]
sf_stat = sf_rel * hypot( sfs["ivf"][1]/sfs["ivf"][0], sfs["softMu"][1]/sfs["softMu"][0] )
sf_bkg  = sf_rel * hypot( sfs["ivf"][2]/sfs["ivf"][0], sfs["softMu"][2]/sfs["softMu"][0] )
sf_mcst = sf_rel * hypot( sfs["ivf"][3]/sfs["ivf"][0], sfs["softMu"][3]/sfs["softMu"][0] )
print "SF ivf norm   = %.3f +- %.3f (stat) +- %.3f (bg) +- %.3f (mc stat) = %.3f +- %.3f" % (sf_rel, sf_stat, sf_bkg, sf_mcst, sf_rel, hypot3(sf_stat, sf_bkg, sf_mcst))

