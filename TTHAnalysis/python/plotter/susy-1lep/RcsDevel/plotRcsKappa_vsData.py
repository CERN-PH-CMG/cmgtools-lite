import sys,os

#from makeYieldPlots import *
import makeYieldPlots as yp

yp._batchMode = False
yp._alpha = 0.35

if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = str(2.2) + " fb^{-1}"
    yp.CMS_lumi.extraText = "Simulation"

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

    nBs = ["NB"]#"NB1","NB2","NB3"]
    #nBs = ["NB1","NB2","NB3"]
    nJs = ["NJ"]#"NJ68","NJ9i"]
    #nJs = ["NJ68","NJ9i"]

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

                canvs = []

                # Samples
                samps = ["EWK"]#,"TT","TTdiLep","TTsemiLep","WJets"]

                for samp in samps:

                    # RCS MB
                    yp.colorDict[samp+"_Rcs_MB"] = yp.kBlue
                    hRcsMB = yp.makeSampHisto(yds,samp,"Rcs_MB",samp+"_Rcs_MB")
                    #hRcsMB.SetTitle("R_{CS} (MB)")
                    hRcsMB.SetTitle("R_{CS}^{MC}(n_{b-tag}, n_{jet}^{SR}, EWK)")

                    # RCS SB
                    yp.colorDict[samp+"_Rcs_SB"] = yp.kRed
                    hRcsSB = yp.makeSampHisto(yds,samp,"Rcs_SB",samp+"_Rcs_SB")
                    #hRcsSB.SetTitle("R_{CS} (SB)")
                    hRcsSB.SetTitle("R_{CS}^{MC}(n_{b-tag}, n_{jet}#in [4,5], EWK)")

                    # Kappa
                    yp.colorDict[samp+"_Kappa"] = yp.kRed
                    hKappa = yp.makeSampHisto(yds,samp,"Kappa",samp+"_Kappa")
                    hKappa.SetTitle("#kappa_{MC}")

                    yp.prepKappaHist(hKappa)
                    yp.prepRatio(hKappa)

                    hRcsMB.GetYaxis().SetRangeUser(0,0.2)

                    ## DATA
                    yp.colorDict["data_QCDsubtr_Rcs_SB"] = yp.kBlack
                    hDataSB = yp.makeSampHisto(yds,"data_QCDsubtr","Rcs_SB","data_QCDsubtr_Rcs_SB")
                    hDataSB.SetTitle("R_{CS} (Data SB)")

                    canv = yp.plotHists(samp+"_RcsKappa_",[hRcsMB,hRcsSB,hDataSB],hKappa, legPos = "TRC", width = 1200, height = 600)
                    #canv = yp.plotHists(samp+"_RcsKappa_",[hRcsMB,hRcsSB],hKappa, legPos = "TM", width = 1200, height = 600)
                    #canv = yp.plotHists(samp+"_RcsKappa_",[hRcsMB,hRcsSB],hKappa, legPos = "TM")
                    #canv = yp.plotHists(samp+"_RcsKappa_",[hDataSB, hRcsSB],None, legPos = "TMR", width = 1200, height = 600)

                    hRcsMB.GetYaxis().SetTitle("R_{CS}")
                    hRcsMB.GetYaxis().SetTitleSize(0.07)
                    hRcsMB.GetYaxis().SetTitleOffset(0.5)

                    hKappa.GetYaxis().SetTitleSize(0.2)
                    hKappa.GetYaxis().SetTitleOffset(0.15)
                    hKappa.GetYaxis().SetTitle("#kappa_{MC}")

                    canvs.append(canv)

                    if not yp._batchMode: raw_input("Enter any key to exit")

                    exts = [".pdf",".png",".root"]

                    odir = "BinPlots/RcsKappa/MCvsData/all/"+mask+"/"
                    if not os.path.exists(odir): os.makedirs(odir)

                    for ext in exts:
                        canv.SaveAs(odir+canv.GetName()+ext)

                '''
                # Save canvases
                exts = [".pdf",".png"]
                #exts = [".pdf"]

                odir = "BinPlots/Rcs/test/"

                for canv in canvs:
                    for ext in exts:
                        canv.SaveAs(odir+mask+canv.GetName()+ext)

                '''
