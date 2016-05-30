import sys,os

#from makeYieldPlots import *
import makeYieldPlots as yp

yp._batchMode = False
yp._alpha = 0.75
if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = str(2.2) + " fb^{-1}"
    #yp.CMS_lumi.lumi_13TeV = "MC"
    yp.CMS_lumi.extraText = "Simulation"

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True

    '''
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)
    '''
    pattern = ""

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")

    # Define storage
    ydsMC = yp.YieldStore("MC")
    pathMC = "Yields/wData/jecv7_fixSR/lumi2p25fb/unblind/allSF_noPU/meth1A/merged/"
    ydsMC.addFromFiles(pathMC,("lep","sele"))

    ## Store dict in pickle file
    storeDict = True
    pckname = "pickles/allSigCentral.pckz"

    if storeDict == True and os.path.exists(pckname):
        print "#Loading saved yields from pickle:", pckname

        import cPickle as pickle
        import gzip
        ydsSig = pickle.load( gzip.open( pckname, "rb" ) )
    else:
        ydsSig = yp.YieldStore("Signal")
        pathSig = "Yields/signal/fixSR/lumi2p25fb/allSF_noPU/mainNJ/merged/"
        ydsSig.addFromFiles(pathSig,("lep","sele"))

        print "#Saving yields to pickle:", pckname
        # save to pickle
        import cPickle as pickle
        import gzip
        pickle.dump( ydsSig, gzip.open( pckname, "wb" ) )

    sysCols = [2,4,7,8,3,9,6] + range(10,50)#[1,2,3] + range(4,10)

    # canvs and hists
    hists = []
    canvs = []

    ydsMC.showStats()
    #ydsSig.showStats()

    # Samples
    #samps = ["EWK","TT","TTdiLep","TTsemiLep","WJets","TTV","DY","SingleT"]
    #samps = ["TTJets","WJets","TTV","DY","SingleTop"]
    #    mcSamps = ["EWK","TTJets","WJets","SingleTop","DY","TTV"]
    #mcSamps = ['TTdiLep','TTsemiLep','WJets','TTV','SingleT','DY']
    mcSamps = ['DY','TTV','SingleT','WJets','TTdiLep','TTsemiLep']

    cat = "SR_MB"

    #logY = True
    logY = False

    print "Making plot for", cat

    # MC samps
    samps = [(samp,cat) for samp in mcSamps]
    mcHists = yp.makeSampHists(ydsMC,samps)
    hMC = yp.getStack(mcHists)
    hTotal = yp.getTotal(mcHists)

    # Signals

    sighists = []

    masses = []
    mass = "mGo1500_mLSP100"; massName = "(1500,100)"
    masses.append((mass,massName,yp.kMagenta))
    mass = "mGo1200_mLSP800"; massName = "(1200,800)"
    masses.append((mass,massName,yp.kBlack))


    for (mass, massName,col) in masses:

        signame = "T1tttt_Scan_" + mass

        yp.colorDict[signame+"_Sig_"+cat] = col
        hSig = yp.makeSampHisto(ydsSig,signame,cat,signame+"_Sig_"+cat)
        #hSig.SetTitle("T1tttt_"+mass)
        hSig.SetTitle("T1tttt "+massName)

        sighists.append(hSig)

    #print sighists

    ratio = yp.getRatio(hSig,hTotal)
    ratio.SetName("SigOvMC")
    #ratio.GetYaxis().SetRangeUser(0.75,1.25)

    hists += [hMC,hTotal,ratio] + sighists
    #canv = yp.plotHists(cat,[hMC,hSig],ratio,"TM", 1200, 600, logY = True)
    canv = yp.plotHists(cat,[hMC]+sighists,None,"TM", 1200, 600, logY = True)
    yp.gPad.RedrawAxis()

    cname = "MC_vs_T1tttt_" + cat
    canv.SetName(cname)

    canvs.append(canv)

    if not yp._batchMode:
        answ = raw_input("Enter 'q' to exit: ")
        if "q" in answ: exit(0)

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]

    odir = "BinPlots/MCvsSig/allSF_noPU/" + cat + "/"
    if not os.path.isdir(odir): os.makedirs(odir)

    for canv in canvs:
        for ext in exts:
            cname = odir+mask+canv.GetName()
            if logY: cname += "_log"
            canv.SaveAs(cname+ext)

