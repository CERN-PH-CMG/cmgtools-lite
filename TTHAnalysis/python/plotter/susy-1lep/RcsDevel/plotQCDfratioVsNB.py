import sys,os

from ROOT import TLine
from makeYieldPlots import *

_batchMode = False
_lines = []

if __name__ == "__main__":

    CMS_lumi.lumi_13TeV = "MC"#str(2.1) + " fb^{-1}"
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

    # Category
    cat = "root"#CR_MB"

    #nbbins = ['NB0','NB1','NB2i']
    nbbins = ['NB2i','NB1','NB0']
    lab = ["N_{b} #geq 2","N_{b} = 1","N_{b} = 0"]

    ratios = []
    #cols = [1,2,4,7,9,8,3,6] + range(10,50)
    cols = [4,2,1,7,9,8,3,6] + range(10,50)

    # Marks for vertical lines
    marks = [2,5,8]

    for i,nbbin in enumerate(nbbins):

        patt = pattern + "*" + nbbin + "*"

        ## Create Yield Storage
        ydsAnti = YieldStore("AntiEle")
        ydsAnti.addFromFiles(patt,("ele","anti"))

        ydsSele = YieldStore("SeleEle")
        ydsSele.addFromFiles(patt,("ele","sele"))

        hAnti = makeSampHisto(ydsAnti,"QCD",cat,"QCD_Anti_"+cat+"_"+nbbin); hAnti.SetTitle("Anti-selected")
        hSele = makeSampHisto(ydsSele,"QCD",cat,"QCD_Sele_"+cat+"_"+nbbin); hSele.SetTitle("QCD Selected")

        ratio = getRatio(hSele,hAnti)
        ratio.GetYaxis().SetRangeUser(0,0.35)

        ratio.SetName("fRatio_"+nbbin)
        #ratio.SetTitle(nbbin)
        ratio.SetTitle(lab[i])

        # customize
        ratio.SetFillColorAlpha(cols[i],0.35)
        ratio.SetFillStyle(1001)
        ratio.SetLineColor(cols[i])
        ratio.SetMarkerColor(cols[i])

        if i == 0:
            ratio.GetYaxis().SetTitleSize(0.06)
            ratio.GetYaxis().SetTitleOffset(0.7)
            ratio.GetYaxis().SetLabelSize(0.06)
            ratio.GetXaxis().SetLabelSize(0.05)
            ratio.GetXaxis().SetLabelSize(0.04)

        ratios.append(ratio)

    ## Mean f-ratio
    mean = 0.1

    ## Systematic error hist
    hSyst = ratios[0].Clone("hSyst")
    hSyst.Reset()
    hSyst.SetTitle("Syst. Error")

    # PUT SYST UNC HERE
    #sysErrs = [0,25,25,50,25,25,50,100,100]
    sysErrs = [0,25,25,50,25,25,50,75,75]

    for bin in range(1,10):
        hSyst.SetBinContent(bin,mean)
        hSyst.SetBinError(bin,mean*sysErrs[bin-1]/100.)

        #print hSyst.GetXaxis().GetBinLabel(bin), sysErrs[bin-1]/100.

    #hSyst.SetFillStyle(3013)
    hSyst.SetFillStyle(3244)
    hSyst.SetFillColorAlpha(16,0.7)
    #hSyst.SetFillColor(16)
    hSyst.SetMarkerStyle(0)
    hSyst.SetLineColor(0)

    canv = plotHists("QCD_Electrons_Systematic",ratios+[hSyst])

    if canv:
        # 1 - line
        line = TLine(0,mean,ratio.GetNbinsX(),mean)
        line.SetLineWidth(1)
        line.SetLineStyle(2)
        line.Draw()
        _lines.append(line)

        if len(marks) > 0:
            axis = ratio.GetXaxis()
            ymin = 0; ymax = 0.35
            for i,mark in enumerate(marks):
                pos = axis.GetBinLowEdge(mark)
                line = TLine(pos,ymin,pos,ymax)
                line.SetLineStyle(3)
                #if i == 3: line.SetLineStyle(2) # nj6 -> nj9
                line.Draw("same")
                _lines.append(line)


    if not _batchMode: raw_input("Enter any key to exit")

    exts = [".pdf",".png"]
    for ext in exts:
        canv.SaveAs("BinPlots/QCD/fRatios/"+mask+canv.GetName()+ext)

