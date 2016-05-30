import sys,os

#from makeYieldPlots import *
import makeYieldPlots as yp

yp._batchMode = False
yp._alpha = 0.8

if __name__ == "__main__":

    yp.CMS_lumi.lumi_13TeV = str(2.3) + " fb^{-1}"
    #yp.CMS_lumi.lumi_13TeV = "MC"
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

    basename = os.path.basename(pattern)
    mask = basename.replace("*","X_")
    print basename, mask

    ## Store dict in pickle file
    storeDict = True
    pckname = "pickles/sigSysts_fix_"+mask+".pckz"

    if storeDict == True and os.path.exists(pckname):

        print "#Loading saved yields from pickle:", pckname

        import cPickle as pickle
        import gzip
        yds = pickle.load( gzip.open( pckname, "rb" ) )

    else:
        print "#Reading yields from files!"

        # Define storage
        yds = yp.YieldStore("Sele")
        paths = []

        # Add files
        scalePath  = "Yields/signal/systs/scale/T1tttt/normScale2/allSF_noPU/meth1A/merged/"; paths.append(scalePath)
        isrPath  = "Yields/signal/systs/ISR/T1tttt/allSF_noPU_v2/meth1A/merged/"; paths.append(isrPath)
        puPath   = "Yields/signal/systs/pileup/T1tttt/allSF_noPU_fix/meth1A/merged/"; paths.append(puPath)
        btagPath = "Yields/signal/systs/btag/T1tttt/allSF_noPU_fixLepSF/meth1A/merged/"; paths.append(btagPath)
        jecPath  = "Yields/signal/systs/JEC/allSF_noSF/merged/"; paths.append(jecPath)
        # for central values
        normPath  = "Yields/signal/fixSR/lumi2p3fb/jPt3TeV/merged/"; paths.append(normPath)

        for path in paths:
            yds.addFromFiles(path+basename,("lep","sele"))
            #print yds.bins

        print "#Saving yields to pickle:", pckname
        # save to pickle
        import cPickle as pickle
        import gzip
        pickle.dump( yds, gzip.open( pckname, "wb" ) )

    ## Check content
    #yds.showStats()
    print [name for name in yds.samples if ("syst" in name and "mGo1200_mLSP800" in name)]

    ## Sys types
#    systs = ["btagHF","btagLF"]
#    systs = ["PU","btagLF","btagHF","ISR","JEC"]
    systs = ["Scale-Env","PU","btagLF","btagHF","ISR","JEC"]
#    systs = ["btagLF","btagHF","ISR","JEC","PU","Scale-Env"]
#    systs = ["Scale-Env"]
#    systs = ["ISR"]
#    systs = ["btagHF","btagLF","PU"]

    systNames = {
        "btagLF" : "b-mistag (light)",
        "btagHF" : "b-tag (b/c)",
        "JEC" : "JEC",
        "topPt" : "Top p_{T}",
        "PU" : "PU",
        "ISR": "ISR",
        "Scale-Env": "Scale",
        #"Wxsec" : "#sigma_{W}",
        "Wxsec" : "W x-sec",
        "TTVxsec" : "TTV x-sec",
        "Wpol" : "W polar.",
        "JER" : "JER",
        "JERYesNo" : "JER Yes/No",
        "DLSlope" : "DiLep (N_{j} Slope)",
        "DLConst" : "DiLep (N_{j} Const)",
        "lumi" : "Lumi.",
        "trig" : "Trigger",
        "lepSF": "Lepton SF",
        "stat": "Stat.",
        }

    #sysCols = [2,4,7,8,3,9,6] + range(40,50)#[1,2,3] + range(4,10)
    #sysCols = [50] + range(49,0,-2)#range(30,50,2)
    #sysCols = range(40,100,1)#range(30,50,2)
    #sysCols = range(35,100,3)
    sysCols = range(28,100,2)
    #sysCols = range(49,1,-2)
    #sysCols = range(30,40,4) + range(40,100,3)
    #sysCols = range(49,40,-2) + range(40,30,-3) + range(50,100,5)

    # Sample and variable
    samp = "T1tttt_Scan"
    #mass = "mGo1150_mLSP800"
    mass = "mGo1200_mLSP800"
    #mass = "mGo1500_mLSP100"
    #mass = "mGo1000_mLSP100"

    masses = [mass]#"mGo1200_mLSP800"]#,"mGo1500_mLSP100"]
    #masses = ["mGo1200_mLSP800","mGo1500_mLSP100"]

    var = "SR_MB"

    # canvs
    canvs = []
    allhists = []

    for mass in masses:

        hists = []

        # read in central value
        signame = samp+"_"+mass

        hCentral = yp.makeSampHisto(yds,signame,var, signame + "_central")
        #print hCentral
        yp.prepRatio(hCentral,True)
        #hCentral.GetYaxis().SetRangeUser()

        ## Define flat values (i.e. for PU)
        flats = {}
        #flats["PU"] =  0.05

        ### Add flat systs (lumi, lepSF, triggEff, etc.)
        #flats["stat"] = 0.1
        flats["lepSF"] = 0.05
        flats["lumi"] = 0.027
        flats["trig"] = 0.01
        #flats = {}

        for i, syst in enumerate(sorted(flats.keys())):

            if syst in systs: continue

            col = sysCols[i]#+len(syst)]

            sname = samp+"_"+syst+"_syst_"+mass
            print "Making FLAT hist for", sname

            hist = hCentral.Clone(syst+"_syst")
            hist.SetName(sname + syst+"_syst")
            if syst in systNames: hist.SetTitle(systNames[syst])
            else: hist.SetTitle(syst)

            hist.GetYaxis().SetTitle("Relative uncertainty")
            hist.GetYaxis().SetTitleSize(0.04)
            hist.GetYaxis().SetTitleOffset(0.8)

            hist.SetLineColor(col)
            #hist.SetFillColorAlpha(col,yp._alpha)
            hist.SetFillColor(col)
            hist.SetFillStyle(1001)

            for bin in range(1,hist.GetNbinsX()+1):
                if syst == "stat":
                    hist.SetBinContent(bin,hist.GetBinError(bin)/hist.GetBinContent(bin))
                else:
                    hist.SetBinContent(bin,flats[syst])

            # prepend hists
            #hists.insert(0,hist)
            hists.append(hist)

        # Make REAL syst hists
        for i,syst in enumerate(systs):
            yp.colorDict[syst+"_syst"] = sysCols[i+len(flats)]

            sname = samp+"_"+syst+"_syst_"+mass
            print "Making hist for", sname

            hist = yp.makeSampHisto(yds,sname,var,sname+syst+"_syst")
            if syst in systNames: hist.SetTitle(systNames[syst])
            else: hist.SetTitle(syst)

            hist.GetYaxis().SetTitle("Relative uncertainty")
            hist.GetYaxis().SetTitleSize(0.04)
            hist.GetYaxis().SetTitleOffset(0.8)

            #print syst, hist.GetNbinsX()

            # Dummy values
            if syst in flats:
                print "Replacing syst for %s with a flat %2.2f" %(syst, flats[syst])
                for bin in range(1,hist.GetNbinsX()+1):
                    hist.SetBinContent(bin,flats[syst])

            #yp.prepKappaHist(hist)
            #yp.prepRatio(hist)

            # normalize to central value
            #hist.Divide(hCentral)

            hists.append(hist)

        #for hist in hists: print hist.GetName()

        # make stack/total syst hists
        #total = yp.getTotal(hists)
        stack = yp.getStack(hists)
        #sqHist = yp.getSquaredSum(hists)
        sqHist = yp.getSquaredSum(hists[::-1])

        hCentralUncert = yp.getHistWithError(hCentral, sqHist)

        # save hists
        allhists += hists + [hCentral,hCentralUncert,stack, sqHist]

        canv = yp.plotHists(var+"_"+signame,[stack,sqHist],[hCentral,hCentralUncert],"TRC", 1200, 600)
        canv.SetName(canv.GetName()+"_Syst")
    #    canv = yp.plotHists(var+"_"+signame+"_Syst",[sqHist]+hists,[hCentral,hCentralUncert],"TM", 1200, 600)
    #    canv = yp.plotHists(var+"_"+signame+"_Stat",[stack,sqHist],hCentral,"TM", 1200, 600)

        canvs.append(canv)
        if not yp._batchMode: raw_input("Enter any key to exit")

    # Save canvases
    exts = [".pdf",".png",".root"]
    #exts = [".pdf"]

    #odir = "BinPlots/Syst/Combine/test/allSF_noPU_Wpol/Method1A/"
    #odir = "BinPlots/Syst/Combine/allSF_noPU_Wpol/Method1A/"
    odir = "BinPlots/Syst/Signal/allSF_noPU_fixLepSF/lumi2p3fb/"
    #odir = "BinPlots/Syst/Signal/allSF_noPU/Method1A/"
    odir += "/"
    if not os.path.isdir(odir): os.makedirs(odir)

    ## Save hists
    #pattern = "Syst"
    #mask = pattern

    for canv in canvs:
        for ext in exts:
            canv.SaveAs(odir+mask+"_"+canv.GetName()+ext)

