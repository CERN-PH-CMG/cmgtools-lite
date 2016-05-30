import sys,os

import makeYieldPlots as yp

yp.gStyle.SetPadTopMargin(0.1)

yp._batchMode = False
yp._alpha = 0.8

def setPoisErr(hist):

    from ROOT import TH1

    hist.SetBinErrorOption(TH1.kPoisson);

    #example: lower /upper error for bin 20
    for ibin in xrange(hist.GetNbinsX()):
        err_low = hist.GetBinErrorLow(ibin);
        err_up = hist.GetBinErrorUp(ibin);

def scaleToHist(hists, hRef):

    hTotal = yp.getTotal(mcHists)

    for hist in hists:
        hist.Divide(hTotal)
        hist.Multiply(hRef)

if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = str(2.3) + " fb^{-1}"
    yp.CMS_lumi.extraText = "Preliminary"

    #yp.CMS_lumi.lumi_13TeV = "MC"
    #yp.CMS_lumi.extraText = "Simulation"

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        #pattern = ""
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")

    # canvs and hists
    systHists = []
    canvs = []

    ###########################
    ## Get Kappa Systematics ##
    ###########################

    ## Store dict in pickle file
    storeDict = True
    pckname = "pickles/bkgSysts"+mask+".pck"
    pcksig = "pickles/sigCentral"+mask+".pckz"

    if storeDict == True and os.path.exists(pckname):

        print "#Loading saved yields from pickle!"

        import cPickle as pickle
        ydsSyst = pickle.load( open( pckname, "rb" ) )
        #ydsSyst.showStats()
    else:

        print "#Reading yields from files!"

        # Define storage
        ydsSyst = yp.YieldStore("Sele")
        paths = []

        # Add files
        tptPath = "Yields/systs/topPt/MC/allSF_noPU/meth1A/merged/"; paths.append(tptPath)
        puPath = "Yields/systs/PU/MC/allSF/meth1A/merged/"; paths.append(puPath)
        wxsecPath = "Yields/systs/wXsec/MC/allSF_noPU/meth1A/merged/"; paths.append(wxsecPath)
        ttvxsecPath = "Yields/systs/TTVxsec/MC/allSF_noPU/meth1A/merged/"; paths.append(ttvxsecPath)
        wpolPath = "Yields/systs/Wpol/MC/allSF_noPU/meth1A/merged/"; paths.append(wpolPath)
        dlConstPath = "Yields/systs/DLConst/merged/"; paths.append(dlConstPath)
        dlSlopePath = "Yields/systs/DLSlope/merged/"; paths.append(dlSlopePath)
        jerPath = "Yields/systs/JER/merged/"; paths.append(jerPath)
        jerNoPath = "Yields/systs/JER_YesNo/merged/"; paths.append(jerNoPath)
        btagPath = "Yields/systs/btag/hadFlavour/fixXsec/allSF_noPU/meth1A/merged/"; paths.append(btagPath)
        jecPath = "Yields/systs/JEC/MC/allSF_noPU/meth1A/merged/"; paths.append(jecPath)

        for path in paths: ydsSyst.addFromFiles(path+basename,("lep","sele"))

        ydsSyst.showStats()

        print "#Saving yields to pickle"

        # save to pickle
        import cPickle as pickle
        pickle.dump( ydsSyst, open( pckname, "wb" ) )

    ## LOAD SIGNAL

    if storeDict == True and os.path.exists(pcksig):

        print "#Loading saved yields from pickle!"

        import cPickle as pickle
        import gzip
        ydsSig = pickle.load( gzip.open( pcksig, "rb" ) )

    else:

        ydsSig = yp.YieldStore("Signal")
        #pathSig = "Yields/signal/fixSR/lumi2p25fb/allSF_noPU/mainNJ/merged/"
        pathSig = "Yields/signal/fixSR/lumi2p3fb/jPt3TeV/merged/"
        ydsSig.addFromFiles(pathSig+basename,("lep","sele"))

        print "#Saving yields to pickle:", pcksig

        import gzip
        pickle.dump( ydsSig, gzip.open( pcksig, "wb" ) )

    # Sys types
#    systs = ["btagHF","Wxsec","topPt","PU","DLSlope","DLConst"]#,"JEC"]
#    systs = ["Wxsec","PU","JEC","btagHF","btagLF","topPt"]
#    systs = ["Wxsec","PU","JEC","btagHF","btagLF","topPt","DLConst","DLSlope","JER"]
    systs = ["TTVxsec","Wpol","Wxsec","PU","JEC","btagHF","btagLF","topPt","DLConst","DLSlope"]

    # Kappa systematics
    samp = "EWK";    var = "Kappa"
    systSamps = [(samp+"_"+syst+"_syst",var) for syst in systs]
    systHists = yp.makeSampHists(ydsSyst,systSamps)
    hKappaSysts = yp.getSquaredSum(systHists)

    print "Created syst hist", hKappaSysts

    # MC systematics
    samp = "EWK";    var = "SR_MB"
    systSamps = [(samp+"_"+syst+"_syst",var) for syst in systs]
    systHists = yp.makeSampHists(ydsSyst,systSamps)
    hMCSysts = yp.getSquaredSum(systHists)

    ###########################
    ## Make Prediction plots ##
    ###########################

    ## Create Yield Storage
    yds = yp.YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    #yds.showStats()

    mcSamps = ['DY','TTV','SingleT','WJets','TT']
    #mcSamps = ['EWK']

    # update colors
    yp.colorDict["MC_prediction"] = yp.kRed
    yp.colorDict["Data_prediction"] = yp.kRed

    # Category
    cat = "SR_MB_predict"

    # MC samps
    samps = [(samp,cat) for samp in mcSamps]
    mcHists = yp.makeSampHists(yds,samps)

    # for MC closure
    #mcsamp = "EWK_poisson"
    #mcsamp = "background_poisson_QCDsubtr"
    #hMCpred = yp.makeSampHisto(yds,mcsamp,cat,"MC_prediction"); hMCpred.SetTitle("MC (Pred)")

    # DATA
    hDataPred = yp.makeSampHisto(yds,"data_QCDsubtr",cat,"Data_prediction"); hDataPred.SetTitle("Prediction")
    #hDataPred = yp.makeSampHisto(yds,"data",cat,"Data_prediction"); hDataPred.SetTitle("Prediction")
    hData = yp.makeSampHisto(yds,"data","SR_MB","Data"); hData.SetTitle("Data")

    ## Append Systematics to prediction
    print "Appending syst. unc. to prediction and total MC"
    hDataPred = yp.getHistWithError(hDataPred, hKappaSysts, new = False)

    # Do MC hists
    scaleToHist(mcHists,hDataPred)

    mcStack = yp.getStack(mcHists)
    #hTotal = yp.getTotal(mcHists)
    #hTotal = yp.getHistWithError(hTotal, hMCSysts, new = False)
    hUncert = hDataPred.Clone("uncert")
    hUncert.SetTitle("Pred. Uncertainty")
    yp.setUnc(hUncert)

    # test MC
    #hDataPred = hMCpred

    #hData.SetBinErrorOption(TH1.kPoisson)
    #from CMGTools.TTHAnalysis.plotter.mcPlots import getDataPoissonErrors
    hDataPois = yp.getDataPoissonErrors(hData,True,False)
    hDataPois.SetName("DataPois")
    hDataPois.SetTitle("Data")
    #hDataPois = hData.Clone()
    #setPoisErr(hData)
    #setPoisErr(hDataPois)
    #setPoissonErrors(hData)

    # Ratio
    #ratio = yp.getRatio(hTotal,hDataPred)
    ratio = yp.getRatio(hData,hDataPred)
    ratioPois = yp.getRatio(hDataPois,hDataPred)

    hPredUnc = yp.getRatio(hDataPred,hDataPred)
    col = yp.kGray
    hPredUnc.SetName("PredictionUncertainty")
    hPredUnc.SetLineColor(1)
    hPredUnc.SetFillColorAlpha(col,yp._alpha)
    #hPredUnc.SetFillColorAlpha(col,0.5)
    hPredUnc.SetFillStyle(3244)
    #hPredUnc.SetFillStyle(1001)
    hPredUnc.SetMarkerColor(col)
    hPredUnc.SetMarkerStyle(0)
    #hPredUnc.GetYaxis().SetTitle(ratio.GetYaxis().GetTitle())
    hPredUnc.GetYaxis().SetRangeUser(0,3.9)
    hPredUnc.GetYaxis().SetTitle("Data/Pred.")
    hPredUnc.GetYaxis().SetTitleSize(0.15)
    hPredUnc.GetYaxis().SetTitleOffset(0.15)

    # set error
    for i in xrange(1,hPredUnc.GetNbinsX()+1):
        hPredUnc.SetBinError(i,hDataPred.GetBinError(i)/hDataPred.GetBinContent(i))

    ### Signal
    sighists = []
    sigcat = "SR_MB"

    masses = []
    '''
    mass = "mGo1200_mLSP800"; massName = "(1200,800)"
    masses.append((mass,massName,yp.kYellow-6,1))
    mass = "mGo1500_mLSP100"; massName = "(1500,100)"
    masses.append((mass,massName,yp.kMagenta,1))
    '''

    mass = "mGo1200_mLSP800"; massName = "T1t^{4} 1.2/0.8"
    masses.append((mass,massName,yp.kYellow-6,1))
    mass = "mGo1500_mLSP100"; massName = "T1t^{4} 1.5/0.1"
    masses.append((mass,massName,yp.kMagenta,1))

    for (mass, massName,col,lsty) in masses:
        signame = "T1tttt_Scan_" + mass

        yp.colorDict[signame+"_SigStack_"+sigcat] = col
        hSig = yp.makeSampHisto(ydsSig,signame,sigcat,signame+"_SigStack_"+sigcat)
        #hSig.SetTitle("T1tttt "+massName)
        hSig.SetTitle(massName)
        hSig.SetFillStyle(0)
        hSig.SetLineWidth(2)
        hSig.SetLineStyle(lsty)

        # put signal on top of prediction
        hSig.Add(hDataPred)

        sighists.append(hSig)

    #### Drawing
    logY = True
    #logY = False
    cname = "Data_2p3fb_"+mask
    hists = [mcStack,hUncert] + sighists + [hDataPois]
    ratios = [hPredUnc,ratioPois]

    #canv = yp.plotHists("SR_MB_Prediction",[mcStack,hTotal,hDataPred,hDataPois],[hPredUnc,ratioPois],'TM', 1200, 600, logY = logY)
    canv = yp.plotHists("SR_MB_Prediction",hists,ratios,'TRC', 1200, 600, logY = logY)

    canv.SetName(cname + canv.GetName())

    if logY: canv.SetName(canv.GetName() + "_log")
    canvs.append(canv)

    if not yp._batchMode:
        if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]

    odir = "BinPlots/Data/lumi2p3fb/JECv7/vsSig/allSF_noPU/"
    #odir = "BinPlots/Syst/btag/hadronFlavour/allSF_noPU/Method1B/"
    if not os.path.isdir(odir): os.makedirs(odir)

    for canv in canvs:
        for ext in exts:
            canv.SaveAs(odir+canv.GetName()+ext)
