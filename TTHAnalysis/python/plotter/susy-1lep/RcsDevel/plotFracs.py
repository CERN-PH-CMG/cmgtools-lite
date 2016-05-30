import sys,os

import  makeYieldPlots as yp

yp._batchMode = False
yp._alpha = 0.90

if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = "MC"
    yp.CMS_lumi.extraText = "Simulation"
    yp.iPos = 0
    if( yp.iPos==0 ): yp.CMS_lumi.relPosX = 0.1


    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        yp._batchMode = True

    '''
    doAll = False
    if '-all' in sys.argv:
        sys.argv.remove('-all')
        doAll = True
    '''

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    #BinMask LTX_HTX_NBX_NJX for canvas names

    nBs = ["NB"]#["NB1","NB2","NB3"]
    nJs = ["NJ68","NJ9i"]

    basename = os.path.basename(pattern)
    print basename

    if basename == 'LT':
        for nB in nBs:
            for nJ in nJs:
                patternnew = pattern + "*" + nB + "*" + nJ
                basenamenew = os.path.basename(patternnew)
                mask = basenamenew.replace("*","X_")

                print "Plots for", patternnew

                yds = yp.YieldStore("lepYields")
                yds.addFromFiles(patternnew,("lep","sele"))
                yds.showStats()

                mcSamps = ['TTdiLep','TTsemiLep','WJets','TTV','SingleT','DY']
                #mcSamps = ['TT','WJets','TTV','SingleT','DY']

                cats = ["CR_MB","CR_SB","SR_MB","SR_SB"]


                for cat in cats:
                    # MC samps
                    samps = [(samp,cat) for samp in mcSamps]

                    hists = yp.makeSampHists(yds,samps)
                    total = yp.getTotal(hists)
                    for i,hist in enumerate(hists):
                        hist.Divide(total)
                        hist.GetYaxis().SetTitle("Fraction")
                    stack = yp.getStack(hists)

                    canv = yp.plotHists(cat,[stack],None,"Long")
                    yp.gPad.RedrawAxis()

                    if not yp._batchMode:
                        if "q" in raw_input("Enter any key to exit (or 'q' to stop): "): exit(0)

                    exts = [".pdf",".png",".root"]

                    odir = "BinPlots/MC/Fractions/test/"+mask+"/"
                    if not os.path.exists(odir): os.makedirs(odir)

                    for ext in exts:
                        canv.SaveAs(odir+canv.GetName()+ext)
