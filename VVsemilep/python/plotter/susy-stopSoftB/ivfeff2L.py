from CMGTools.TTHAnalysis.plotter.mcPlots import *
from math import *
from collections import defaultdict

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

def fitAndExtractScaleFactors(options,mca,cf,pfname,plot,singlePlot=True):
        oldSelPlots = options.plotselect[:]
        if singlePlot:
            options.plotselect = [ "^"+plot+"$" ]
        else:
            options.plotselect += [ plot ]
        options.preFitData = plot

        scales0 = dict((p,mca.getScales(p)) for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True)) 

        outfile  = ROOT.TFile(options.printDir+"/plot_"+plot+".root" if options.printDir else "plot_"+plot+".root","RECREATE")
        plotter = PlotMaker(outfile,options).run(mca,cf,PlotFile(pfname, options))
        outfile.Close()

        scales2 = dict((p,mca.getScales(p)) for p in mca.listSignals(allProcs=True) + mca.listBackgrounds(allProcs=True)) 

        ret = []
        for p in scales0.iterkeys():
            scale0 = scales0[p][0]
            scale2 = scales2[p][0]
            if scale2 == scale0: continue
            if scale0 not in scale2: raise RuntimeError, "Unparsable scale for %s: %r -> %r" % (p, scale0, scale2) 
            m = re.match(r"\(\(unity\) \* \(([0-9\.e+\-]+)\)\)$", scale2.replace(scale0, "unity"))
            if not m: raise RuntimeError, "Unparsable scale for %s: %r -> %r" % (p, scale0, scale2)
            sf = float(m.group(1))
            ret.append((p,sf,mca.getProcessOption(p,'NormSystematic',0.0)))

        ## Reset old scales
        for p,sc0 in scales0.iteritems(): mca.setScales(p,sc0)
        ## Reset old plots
        options.plotselect = oldSelPlots
        options.preFitData = None
        return ret
 
from optparse import OptionParser
parser = OptionParser(usage="%prog [options] tree.root cuts.txt IVFCUT MUCUT")
addPlotMakerOptions(parser)
parser.add_option("-i", "--in",  dest="inf",  type="string", default=None, help="in pickle file") 
parser.add_option("-o", "--out", dest="out", type="string", default=None, help="out pickle file") 
parser.add_option("--bgsyst", dest="bgsyst", type="float", default=1.0, help="Background uncertainty");
parser.add_option("--plots", dest="plots", type="string", default=None, help="Also make plots");
parser.add_option("--SI", "--sv-insitu", dest="svInSitu", type="string", default=[], action="append", help="Use the following plots to get in situ the heavy and light fractions for the SV case");
parser.add_option("--MI", "--mu-insitu", dest="muInSitu", type="string", default=[], action="append", help="Use the following plots to get in situ the heavy and light fractions for the soft mu case");
(options, args) = parser.parse_args()
userSignal = options.processesAsSignal[:]
options.txtfmt = "tsv"
options.fractions = False

# don't make plots if --pdir is not specified (faster)
if "--pdir" not in sys.argv:
    options.printPlots = ""

reports = {}
inSituSFs = {}
if options.inf:
    print "Reading from", options.inf
    import pickle
    reports = pickle.load(open(options.inf))
else:
    options.allProcesses = True
    options.final = True
    userExcludes = options.processesToExclude[:]
    userEnables  = options.cutsToEnable[:]
    userPlotsSel  = options.plotselect[:]
    userPlotsExcl = options.plotexclude[:]
    userNormSyst = options.processesToSetNormSystematic[:]

    if options.plots or options.preFitData:
        options.processesAsSignal = [ "^T[TW].*" ]

        if options.printPlots: 
            mainPrintDir = options.printDir
            subs = ["/ivf", "/softMu", ""]
            if options.svInSitu: subs.append("/ivf/postfit")
            if options.muInSitu: subs.append("/softMu/postfit")
            for sub in subs:
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
            inclusiveScales = []
            for (p,sf,err) in fitAndExtractScaleFactors(options,mca_all,cf_all,options.plots,options.preFitData,singlePlot=False):
                if p in ("TT","TW"): inclusiveScales.append((p+"_.*",str(sf)))
                else:                inclusiveScales.append((p,      str(sf)))
            print "Fit results in the following scale factors: %s" % inclusiveScales
            options.processesToScale += inclusiveScales[:]
            options.preFitData = None

    processesToExclude = dict( ivf=[ "T[TW]$", "T[TW]_softMu.*" ], softMu=[ "T[TW]$", "T[TW]_ivf.*" ] )
    cutsToEnable = dict( ivf=args[2], softMu=args[3] )
    plotsPattern = dict( ivf=[ "^SV_.*" ], softMu=[ "^LepOtherGood_.*" ])
    inSitu = dict(ivf = options.svInSitu, softMu=options.muInSitu )

    for task in 'ivf', 'softMu':
        print "\n === Running %s Selection (cuts: %r) === " % (task.upper(), cutsToEnable[task])
        options.processesToExclude = userExcludes +  processesToExclude[task]
        options.cutsToEnable = userEnables + [ cutsToEnable[task] ]
        mca_task = MCAnalysis(args[0],options)
        cf_task  = CutsFile(args[1],options)
        if options.plots and options.printPlots:
            options.printDir = mainPrintDir + "/" + task + "/"
            options.plotselect  = userPlotsSel if userPlotsSel else plotsPattern[task]
            options.plotexclude = userPlotsExcl + plotsPattern["softMu" if task == "ivf" else "ivf"]
        if inSitu[task]:
            if not options.plots: raise RuntimeError, "In-situ possible only with plotting enabled"
            ## configure the proper floating and pegging
            userPegs, userFloats = options.processesToPeg[:], options.processesToFloat[:]
            signal = userSignal[0] if userSignal else "^T[TW]_.*B$"
            options.processesAsSignal = [ signal ]
            #options.processesToFloat = [ ".*" ]
            #options.processesToPeg   = [ ('.*','other'), ('^T[TW]_.*', 'bkg'), (signal, 'signal') ]
            options.processesToFloat = [ "^T[TW]_.*", ]
            options.processesToPeg   = [ ('^T[TW]_.*', 'bkg'), (signal, 'signal') ]
            mca_task_fit = MCAnalysis(args[0],options)
            ## Now, for each plot in inSitu, we plot that and derive a set of scale factors
            his, los, centers = defaultdict(list),defaultdict(list),defaultdict(list)
            for pIS in inSitu[task]:
                print "Fitting "+pIS
                fitresult = fitAndExtractScaleFactors(options,mca_task_fit,cf_task,options.plots,pIS)
                for (p,sf,err) in fitresult:
                    key = p
                    for (patt,what) in options.processesToPeg:
                        if re.match(patt+"$",p):
                            key = what
                    his[key].append(sf+err)
                    los[key].append(sf-err)
                    centers[key].append(sf)
            svInSituSF = [ ]
            for (patt,what) in options.processesToPeg:
                sf = sum(centers[what])/len(centers[what])
                err = max(max(his[what])-sf,sf-min(los[what]))
                print "Extracted SF for %s: %.3f +- %.3f" % (what,sf,err)
                svInSituSF.append((what,patt,sf,err))
            options.processesToPeg = userPegs; options.processesToFloat = userFloats
        if options.plots and options.printPlots:
            pf_task  = PlotFile(options.plots, options)
            outfile  = ROOT.TFile(options.printDir+"/plots.root","RECREATE")
            PlotMaker(outfile,options).run(mca_task,cf_task,pf_task)
            reports[task] = _plotsToReport(mca_task,pf_task,outfile)
            outfile.Close()
        else: # just get yields
            reports[task] = _plotsToReport(mca_task,pf_task,outfile)
        if inSitu[task]: # make post-fit plots
            # backup scales
            scalesBackup = options.processesToScale[:]
            # apply post-fit scales
            ### Attention: processes to scale uses *all* scales that match, not only the last one, so we need a loop
            for p in mca_task.listProcesses(True):
                sf, err = None, None
                for (what,patt,isf,ierr) in svInSituSF:
                    if re.match(patt+"$",p): (sf,err) = (isf,ierr)
                if sf != None:
                    options.processesToScale             += [ (p,str(sf)) ]
                    options.processesToSetNormSystematic += [ (p,err) ] 
            mca_task = MCAnalysis(args[0],options) # remake it with the new options
            # make post-fit plots
            options.printDir = mainPrintDir + "/"+task+"/postfit"
            pf_task  = PlotFile(options.plots, options)
            outfile  = ROOT.TFile(options.printDir+"/plots.root","RECREATE")
            PlotMaker(outfile,options).run(mca_task,cf_task,pf_task)
            reports[task]   = _plotsToReport(mca_task,pf_task,outfile)
            inSituSFs[task] = [ (sf,err) for  (p,patt,sf,err) in svInSituSF if p == 'signal' ][0]
            outfile.Close()
            # reset options to backup
            options.processesToScale = scalesBackup[:]
            options.processesToSetNormSystematic = userNormSyst[:]
            mca_task = MCAnalysis(args[0],options)  
        mca_task.prettyPrint(reports[task])

    if options.out:
        import pickle
        if "{PD}" in options.out and options.printPlots: 
            options.out = options.out.replace("{PD}", mainPrintDir)
        pickle.dump(reports, open(options.out, 'w'))
        print "Saved to", options.out

def hypot3(a,b,c): return sqrt(a**2+b**2+c**2)

signal = userSignal[0] if userSignal else "^T[TW]_.*B$"
sfs = {}
for (what,rep) in reports.iteritems():
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
    if what in inSituSFs:
        # plots are already scaled...
        sf, sf_fit  = inSituSFs[what]
        sf_stat = sqrt(ndata)/nsig
        if sf_fit > sf_stat:
            sf_bkg  = sqrt(sf_fit**2 - sf_stat**2)
        else:
            print "Puzzling: SF fit uncertainty for %s larger than pure stat. uncertainty" % what
            sf_bkg = 0
        sf_mcst = sqrt(nsige2+nbkge2)/nsig
        print "SF for %-6s = %.3f +- %.3f (stat) +- %.3f (bg) +- %.3f (mc stat) = %.3f +- %.3f" % (what, sf, sf_stat, sf_bkg, sf_mcst, sf, hypot3(sf_stat, sf_bkg, sf_mcst))
    else:
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

