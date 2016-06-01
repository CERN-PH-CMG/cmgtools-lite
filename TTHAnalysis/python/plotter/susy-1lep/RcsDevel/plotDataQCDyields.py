import sys,os

#from makeYieldPlots import *
import makeYieldPlots as yp

yp._batchMode = False

if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = str(2.3) + " fb^{-1}"
    yp.CMS_lumi.extraText = "Preliminary"

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
    mask = basename.replace("*","X_")

        ## Create Yield Storage
    #ydsAntiEle = yp.YieldStore("EleAnti")
    #ydsAntiEle.addFromFiles(pattern,("ele","anti"))

    ydsSele = yp.YieldStore("Sele")
    ydsSele.addFromFiles(pattern,("lep","sele"))

    ydsSeleEle = yp.YieldStore("EleSele")
    ydsSeleEle.addFromFiles(pattern,("ele","sele"))

    ydsSeleMu = yp.YieldStore("MuSele")
    ydsSeleMu.addFromFiles(pattern,("mu","sele"))

    ydsAntiMu = yp.YieldStore("MuAnti")
    ydsAntiMu.addFromFiles(pattern,("mu","anti"))

    # Category
    cats = ["CR_MB"]#,"CR_SB"]

    for cat in cats:

        # ele
        yp.colorDict["Data_QCD_Ele_"+cat] = yp.kRed
        hEleQCDpred = yp.makeSampHisto(ydsSeleEle,"data_QCDpred",cat,"Data_QCD_Ele_"+cat)
        hEleQCDpred.SetTitle("QCD pred. (ele)")

        # muons
        '''
        yp.colorDict["Data_QCD_Mu_"+cat] = yp.kBlue
        hMuAnti = yp.makeSampHisto(ydsAntiMu,"data",cat,"Data_QCD_Mu_"+cat)
        hMuAnti.SetTitle("Anti-Sele (#mu)")

        # apply "F-ratio" = 10%
        hMuAnti.Scale(1/10.); hMuAnti.SetTitle("Anti-Sele (#mu) x0.1")
        '''
        # mu
        yp.colorDict["Data_QCD_Mu_"+cat] = yp.kBlue
        hMuQCDpred = yp.makeSampHisto(ydsSeleMu,"data_QCDpred",cat,"Data_QCD_Mu_"+cat)
        hMuQCDpred.SetTitle("QCD pred. (#mu)")

        # Data
        yp.colorDict["Data_"+cat] = yp.kBlack
        hData = yp.makeSampHisto(ydsSele,"data",cat,"Data_"+cat)
        hData.SetTitle("Data (sele)")

        # Data Ele
        yp.colorDict["DataEle_"+cat] = yp.kOrange-3
        hDataEle = yp.makeSampHisto(ydsSeleEle,"data",cat,"DataEle_"+cat)
        hDataEle.SetTitle("Data (ele)")

        # Data Ele
        yp.colorDict["DataMu_"+cat] = yp.kCyan-3
        hDataMu = yp.makeSampHisto(ydsSeleMu,"data",cat,"DataMu_"+cat)
        hDataMu.SetTitle("Data (#mu)")

       # ratios and plots
        ratMu = yp.getRatio(hMuQCDpred,hDataMu)
        ratMu.GetYaxis().SetRangeUser(0,0.105)

        ratEle = yp.getRatio(hEleQCDpred,hDataEle)
        ratEle.GetYaxis().SetRangeUser(0,0.35)

        ## combined
        ratEle.SetLineColor(hEleQCDpred.GetLineColor())
        ratEle.SetMarkerColor(hEleQCDpred.GetMarkerColor())

        ratMu.SetLineColor(hMuQCDpred.GetLineColor())
        ratMu.SetMarkerColor(hMuQCDpred.GetMarkerColor())

        '''
        #ratio = yp.getRatio(hMuAnti,hEleQCDpred)
        ratio = yp.getRatio(hMuAnti,hDataMu)
        #ratio.GetYaxis().SetRangeUser(-0.45,0.45)
        #ratio.GetYaxis().SetRangeUser(0,0.95)
        ratio.GetYaxis().SetRangeUser(0,0.105)
        '''

        #canv = yp.plotHists("Sele_QCDvsMC_Lep_"+cat,[hMCele,hMCmu,hEle,hMu])
        #canv = yp.plotHists("Data_vs_QCD_"+cat,[hDataEle,hDataMu,hEleQCDpred,hMuAnti],ratio,'TM', 1200, 600, logY = False)
        canv = yp.plotHists("Data_vs_QCD_"+cat,[hDataEle,hDataMu,hEleQCDpred,hMuQCDpred],[ratEle,ratMu],'TM', 1200, 600, logY = False)
        #canv = yp.plotHists("Data_vs_QCD_Mu_"+cat,[hDataMu,hMuAnti],ratio)

        if not yp._batchMode: raw_input("Enter any key to exit")

        exts = [".pdf",".png"]
        #exts = [".pdf"]
        for ext in exts:
            canv.SaveAs("BinPlots/QCD/lumi2p3fb/DataCompare/"+mask+canv.GetName()+ext)
