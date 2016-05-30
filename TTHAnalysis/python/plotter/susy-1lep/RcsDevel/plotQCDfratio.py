import sys,os

from makeYieldPlots import *

_batchMode = False

if __name__ == "__main__":

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

    # Category
    cat = "root"#CR_MB"

    ## Create Yield Storage
    ydsAnti = YieldStore("AntiEle")
    ydsAnti.addFromFiles(pattern,("ele","anti"))

    ydsAnti.showStats()

    colorDict["QCD_Anti_"+cat] = kRed

    ydsSele = YieldStore("SeleEle")
    ydsSele.addFromFiles(pattern,("ele","sele"))
    ydsSele.showStats()

    colorDict["QCD_Sele_"+cat] = kBlue

    hAnti = makeSampHisto(ydsAnti,"QCD",cat,"QCD_Anti_"+cat)
    hAnti.SetTitle("Anti-selected")

    hSele = makeSampHisto(ydsSele,"QCD",cat,"QCD_Sele_"+cat)
    hSele.SetTitle("QCD Selected")

    ratio = getRatio(hSele,hAnti)
    ratio.GetYaxis().SetRangeUser(0,0.35)

    #canv = plotHists("Sele_Vs_HE_New_AntiEle_"+cat,[hAnti,hSele],ratio)
    #canv = plotHists("Sele_Vs_New_AntiEle_"+cat,[hAnti,hSele],ratio)
    #canv = plotHists("Sele_QCDvsMC_Ele_"+cat,[hAnti,hSele],ratio)

    canv = plotHists("SeleVsAnti_Ele_",[hAnti,hSele],ratio)

    if not _batchMode: raw_input("Enter any key to exit")

    exts = [".pdf",".png"]
    for ext in exts:
        canv.SaveAs("BinPlots/QCD/fRatios/"+mask+canv.GetName()+ext)

