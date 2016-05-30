import sys,os

from ROOT import *
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
    #basename = basename.replace("_SR","")
    mask = basename.replace("*","X_")

    lumi = 3
    CMS_lumi.lumi_13TeV = str(lumi) + " fb^{-1}"
    CMS_lumi.extraText = "Simulation"

    ## Create Yield Storage
    yds = YieldStore("lepYields")
    yds.addFromFiles(pattern,("lep","sele"))
    yds.showStats()

    # update colors
    colorDict["EWK_exp"] = kBlack
    colorDict["EWK_pred"] = kRed
    colorDict["EWK_pois"] = kBlack
    colorDict["EWK_pois_pred"] = kBlue

    hEWKexp = makeSampHisto(yds,"EWK","SR_MB","EWK_exp"); hEWKexp.SetTitle("EWK (Expected)")
    hEWK_pois = makeSampHisto(yds,"EWK_poisson","SR_MB","EWK_pois"); hEWK_pois.SetTitle("EWK pois (Expected)"); hEWK_pois.SetName("data");
    hEWKpred = makeSampHisto(yds,"EWK","SR_MB_predict","EWK_pred"); hEWKpred.SetTitle("EWK (Predicted)")
    hEWKpred_pois = makeSampHisto(yds,"EWK_poisson","SR_MB_predict","EWK_pois_pred"); hEWKpred_pois.SetTitle("EWK pois (Predicted)")

    #ratio = getRatio(hEWKexp,hEWKpred)
    #ratio = getPull(hEWKpred,hEWKexp)
    #ratio.GetYaxis().SetRangeUser(0,5)

    canv = plotHists("testV2_EWK_pred",[hEWK_pois, hEWKpred_pois,hEWKpred,hEWKexp])#,ratio)

    if not _batchMode:
        if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)

    exts = [".pdf",".png"]
    for ext in exts:
        canv.SaveAs("BinPlots/test/"+mask+canv.GetName()+ext)

