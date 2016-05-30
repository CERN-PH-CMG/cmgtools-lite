import sys,os

from makeYieldPlots import _batchMode as _batch
from makeYieldPlots import *

#_batchMode = False
_batch = False

if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        #_batchMode = True
        _batch = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names
    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")

    lep = "ele"

    canvs = []

    ## Create Yield Storage
    yds = YieldStore(lep+"Yields")
    yds.addFromFiles(pattern,(lep,"sele"))
    yds.showStats()

    lumi = 2.1

    CMS_lumi.lumi_13TeV = str(lumi) + " fb^{-1}"
    CMS_lumi.extraText = "Simulation"

    # Category
    #cat = "CR_MB"
    cats = ["CR_SB","CR_MB"]

    for cat in cats:

        # update colors
        colorDict[cat+"QCD_pred"] = kBlue
        colorDict[cat+"QCD_exp"] = kRed

        hQCDexp = makeSampHisto(yds,"QCD",cat,cat+"QCD_exp"); hQCDexp.SetTitle("QCD_{MC}")
        hQCDpred = makeSampHisto(yds,"QCD_QCDpred",cat,cat+"QCD_pred"); hQCDpred.SetTitle("QCD_{Pred.}")

        ratio = getPull(hQCDexp,hQCDpred)
        #ratio.GetYaxis().SetRangeUser(0,5)

        canv = plotHists("QCD_Closure_"+cat,[hQCDexp,hQCDpred],ratio)
        canv.SetName("QCD_Closure_"+lep+"_"+cat)
        canvs.append(canv)

        #if not _batchMode:
        if not _batch:
            if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)


        # Save
        odir = "BinPlots/QCD/Closure/lumi2p1fb/"
        #exts = [".pdf",".png"]
        exts = [".pdf"]
        for canv in canvs:
            for ext in exts:
                canv.SaveAs(odir+mask+canv.GetName()+ext)

        canvs = []
