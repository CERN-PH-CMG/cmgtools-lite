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

    ## Create Yield Storage
    yds = YieldStore("lepYields")
    yds.addFromFiles(pattern,("ele","anti"))
    yds.showStats()

    #mcSamps = ['DY','TTV','SingleT','WJets','TT','QCD']
    mcSamps = ['WJets','TT','QCD']

    # Category
    #cat = "CR_MB"
    cats = ["CR_SB","SR_SB","CR_MB","SR_MB"]

    for cat in cats:
        # MC samps
        samps = [(samp,cat) for samp in mcSamps]

        # Totals
        #tots = [("data",cat)]
        tots = [("background",cat)]

        hists = makeSampHists(yds,samps)
        stack = getStack(hists)
        total = getTotal(hists)

        hTot = makeSampHists(yds,tots)[0]

        #ratio = getRatio(hTot,total)
        ratio = getRatio(hists[2],total)
        ratio.GetYaxis().SetRangeUser(0,1.25)

        #canv = plotHists("AntiEle_"+cat,[stack,total,hTot],ratio)
        canv = plotHists("HE_New_AntiEle_"+cat,[stack,total],ratio)
        #canv = plotHists("New_AntiEle_"+cat,[stack,total])

        if not _batchMode:
            if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)

        exts = [".pdf",".png"]
        for ext in exts:
            canv.SaveAs("BinPlots/MCstacks/"+mask+canv.GetName()+ext)

