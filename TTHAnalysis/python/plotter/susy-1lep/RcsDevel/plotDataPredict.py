import sys,os

import makeYieldPlots as yp

yp._batchMode = False
yp._alpha = 0.8


yp.CMS_lumi.lumi_13TeV = str(2.24) + " fb^{-1}"
yp.CMS_lumi.extraText = "Preliminary"

doPoisErr = True

def scaleToHist(hists, hRef):

    hTotal = yp.getTotal(hists)

    for hist in hists:
        hist.Divide(hTotal)
        hist.Multiply(hRef)

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    #basename = basename.replace("_SR","")
    mask = basename.replace("*","X_")

    ## Create Yield Storage
    yds = yp.YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    yds.showStats()

    mcSamps = ['DY','TTV','SingleT','WJets','TT']#
    #mcSamps = ['WJets','TT','QCD']

    # update colors
    yp.colorDict["MC_prediction"] = yp.kGreen
    yp.colorDict["Data_prediction"] = yp.kRed

    # Category
    #cat = "CR_MB"
    cats = ["SR_MB_predict"]

    canvs = []

    for cat in cats:

        # Totals
        #hMCpred = yp.makeSampHisto(yds,"background_QCDsubtr",cat,"MC_prediction"); hMCpred.SetTitle("MC (Pred)")
        hDataPred = yp.makeSampHisto(yds,"data_QCDsubtr",cat,"Data_prediction"); hDataPred.SetTitle("Data (Pred)")
        hData = yp.makeSampHisto(yds,"data_QCDsubtr","SR_MB","Data"); hData.SetTitle("Data")

        # Ratio
        #ratio = yp.getRatio(hTotal,hDataPred)
        ratio = yp.getRatio(hData,hDataPred)

        #ratio.GetYaxis().SetRangeUser(0,5)

        if doPoisErr:
            from CMGTools.TTHAnalysis.plotter.mcPlots import getDataPoissonErrors
            hDataPois = getDataPoissonErrors(hData,True,True)
            hDataPois.SetName("DataPois")
            hDataPois.SetTitle("Data")

            ratioPois = yp.getRatio(hDataPois,hDataPred)

            hPredUnc = yp.getRatio(hDataPred,hDataPred)
            col = yp.kGray
            hPredUnc.SetName("PredictionUncertainty")
            hPredUnc.SetLineColor(1)
            hPredUnc.SetFillColor(col)
            hPredUnc.SetFillStyle(3244)
            hPredUnc.SetMarkerColor(col)
            hPredUnc.SetMarkerStyle(0)
            hPredUnc.GetYaxis().SetTitle(ratio.GetYaxis().GetTitle())
            hPredUnc.GetYaxis().SetRangeUser(0,3.9)

            # set error
            for i in xrange(1,hPredUnc.GetNbinsX()+1):
                hPredUnc.SetBinError(i,hDataPred.GetBinError(i)/hDataPred.GetBinContent(i))

        # MC samps
        samps = [(samp,cat) for samp in mcSamps]
        mcHists = yp.makeSampHists(yds,samps)

        # Scale MC hists to Prediction
        scaleToHist(mcHists,hDataPred)

        mcStack = yp.getStack(mcHists)
        hUncert = hDataPred.Clone("uncert")
        hUncert.SetTitle("Pred. Uncertainty")
        yp.setUnc(hUncert)

        #canv = plotHists("DataNJ45_"+cat,[stack,hMCpred,hDataPred,hData,total],ratio)
        if doPoisErr:
            canv = yp.plotHists("SR_MB_Prediction",[mcStack,hUncert,hDataPois],[hPredUnc,ratioPois],'TM', 1200, 600, logY = True)
        else:
            canv = yp.plotHists("SR_MB_Prediction",[mcStack,hUncert,hData],ratio,'TM', 1200, 600, logY = True)

        cname = "Data_2p24fb_"+mask

        if doPoisErr: cname += "poisErr_"

        canv.SetName(cname + canv.GetName())

        canvs.append(canv)

        #print canv.GetName()

        if not yp._batchMode:
            if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]

    odir = "BinPlots/Data/JECv7/NJ4to5/allSF_noPU/"
    if not os.path.isdir(odir): os.makedirs(odir)

    for canv in canvs:
        for ext in exts:
            canv.SaveAs(odir+canv.GetName()+ext)

