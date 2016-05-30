import sys,os

from makeYieldPlots import *

_batchMode = False

if __name__ == "__main__":

    CMS_lumi.lumi_13TeV = str(2.3) + " fb^{-1}"
    CMS_lumi.extraText = "Simulation"

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

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
    ydsEle = YieldStore("Ele")
    ydsEle.addFromFiles(pattern,("ele","sele"))

    ydsMu = YieldStore("Mu")
    ydsMu.addFromFiles(pattern,("mu","sele"))

    #ydsMuAnti = YieldStore("MuAnti")
    #ydsMuAnti.addFromFiles(pattern,("mu","anti"))

    # Category
    cats = ["CR_MB","CR_SB"]
    #cats = ["CR_SB"]

    canvs = []

    for cat in cats:

        # ele
        colorDict["QCD_Ele_"+cat] = kRed
        hEle = makeSampHisto(ydsEle,"QCD_poisson",cat,"QCD_Ele_"+cat)
        hEle.SetTitle("QCD (ele)")

        # muons
        colorDict["QCD_Mu_"+cat] = kBlue
        hMu = makeSampHisto(ydsMu,"QCD_poisson",cat,"QCD_Mu_"+cat)
        hMu.SetTitle("QCD (#mu)")

        '''
        # muons
        colorDict["QCD_AntiMu_"+cat] = kCyan
        hMuAnti = makeSampHisto(ydsMuAnti,"QCD",cat,"QCD_AntiMu_"+cat)
        hMuAnti.SetTitle("QCD (anti-#mu) x0.1")
        hMuAnti.Scale(1/10.)
        '''

        ## MC
        colorDict["MC_Ele_"+cat] = kOrange-3
        hMCele = makeSampHisto(ydsEle,"background_poisson",cat,"MC_Ele_"+cat)
        hMCele.SetTitle("QCD+EWK (ele)")

        colorDict["MC_Mu_"+cat] = kCyan
        hMCmu = makeSampHisto(ydsMu,"background_poisson",cat,"MC_Mu_"+cat)
        hMCmu.SetTitle("QCD+EWK (#mu)")

        # ratios and plots
        ratMu = getRatio(hMu,hMCmu)
        ratMu.GetYaxis().SetRangeUser(0,0.105)

        '''
        canv = plotHists("QCD_vs_MC_Mu_"+cat,[hMCmu,hMu],ratMu)
        canv.SetName("Selected_poisson_QCD_vs_MC_Mu_"+cat)
        canvs.append(canv)
        '''

        ratEle = getRatio(hEle,hMCele)
        ratEle.GetYaxis().SetRangeUser(0,0.35)

        '''
        canv = plotHists("QCD_vs_MC_Ele_"+cat,[hMCele,hEle],ratEle)
        canv.SetName("Selected_poisson_QCD_vs_MC_Ele_"+cat)
        canvs.append(canv)
        '''

        ## combined
        ratEle.SetLineColor(hEle.GetLineColor())
        ratEle.SetMarkerColor(hEle.GetMarkerColor())

        ratMu.SetLineColor(hMu.GetLineColor())
        ratMu.SetMarkerColor(hMu.GetMarkerColor())

        #canv = plotHists("QCD_vs_MC_"+cat,[hMCele,hMCmu,hEle,hMu],[ratEle,ratMu],logY=True)
        canv = plotHists("QCD_vs_MC_"+cat,[hMCele,hMCmu,hEle,hMu],[ratEle,ratMu],"TM", 1200, 600, logY = False)
        canv.SetName("Selected_poisson_QCD_vs_MC_"+cat)
        canvs.append(canv)

        '''
        # Mu/Ele
        ratEM = getRatio(hMu,hEle)
        ratEM.GetYaxis().SetRangeUser(0,0.35)

        canv = plotHists("QCD_Ele_vs_Mu_"+cat,[hEle, hMu],ratEM)
        canv.SetName("Selected_QCD_Ele_vs_Mu_"+cat)
        canvs.append(canv)
        '''

        #ratio = getRatio(hMu,hEle)
        #ratio = getPull(hSele,hEle)
        #ratio = getRatio(hEle,hMCele)
        #ratio = getRatio(hMu,hMuAnti)
        #ratio.GetYaxis().SetRangeUser(-0.45,0.45)
        #ratio.GetYaxis().SetRangeUser(0,1.5)

        #canv = plotHists("Sele_Vs_HE_New_EleMu_"+cat,[hEle,hSele],ratio)
        #canv = plotHists("Sele_Vs_New_EleMu_"+cat,[hEle,hSele],ratio)
        #canv = plotHists("Sele_QCDvsMC_Mu_"+cat,[hMCSele,hSele],ratio)
        #canv = plotHists("Sele_QCD_EleVsMu_"+cat,[hEle,hMu],ratio)

        #canv = plotHists("Sele_QCDvsMC_Ele_"+cat,[hMCele,hEle],ratio)
        #canv = plotHists("QCD_Mu_Sele_vs_Anti"+cat,[hMuAnti,hMu],ratio)
        #canv = plotHists("Sele_QCDvsMC_Lep_"+cat,[hMCele,hMCmu,hEle,hMu])

        if not _batchMode: raw_input("Enter any key to exit")

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]

    odir = "BinPlots/QCD/lumi2p2fb/MCCompare/" + cat + "/"
    if not os.path.isdir(odir): os.makedirs(odir)

    for canv in canvs:
        for ext in exts:
            canv.SaveAs(odir+mask+canv.GetName()+ext)
