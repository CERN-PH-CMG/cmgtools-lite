#!/usr/bin/env python
from CMGTools.TTHAnalysis.plotter.mcPlots import *
from ROOT import TF1


SAFE_COLOR_LIST=[
ROOT.kBlack, ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue, ROOT.kMagenta+1, ROOT.kOrange+7, ROOT.kCyan+1, ROOT.kGray+2, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kAzure+1, ROOT.kPink+7, ROOT.kOrange+3, ROOT.kBlue+3, ROOT.kMagenta+3, ROOT.kRed+2,
]


class DoubleRatioPlotter:
    def plotRatioWithFit(self,ratioHist,canvName,extraLabel,yMin,yMax,ytitle="Ratio",xtitle=""):

#  tdrStyle->SetPadTopMargin(0.05);
#  tdrStyle->SetPadBottomMargin(0.13);
#  tdrStyle->SetPadLeftMargin(0.16);
#  tdrStyle->SetPadRightMargin(0.02);

#        ROOT.gStyle.SetOptTitle(0)
#        ROOT.gStyle.SetOptStat(0)
#        ROOT.gStyle.SetPadTopMargin(0.075)
#        ROOT.gStyle.SetPadLeftMargin(0.05)
#        ROOT.gStyle.SetPadRightMargin(0.025)
#        ROOT.gStyle.SetPadBottomMargin(0.25)
        ROOT.gStyle.SetLegendBorderSize(0)
        
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        ROOT.gStyle.SetPadTopMargin(0.05);
        ROOT.gStyle.SetPadRightMargin(0.03);
        ROOT.gStyle.SetPadBottomMargin(0.15)
        ROOT.gStyle.SetPadLeftMargin(0.17)
        c1 = ROOT.TCanvas(canvName, canvName, 600,600)
#        c1.SetTopMargin(c1.GetTopMargin()*options.topSpamSize);
  
        c1.Draw()
        p1, p2 = c1, None # high and low panes
        # set borders, if necessary create subpads
        
        
#        pspec.setOption('extralabel', options.extraLabel)
#        tmpMin = 0.1 #default log miminum
#        if pspec.hasOption('YMin'):
#            tmpMin = pspec.getOption('YMin',1.0)
#        total.SetMinimum(tmpMin)
#        tmpMax = total.GetMaximum()#total.GetBinContent(total.GetMaximumBin())
#        relHistHeight = 1- (ROOT.gStyle.GetPadTopMargin() + ROOT.gStyle.GetPadBottomMargin() + 0.03*len(pspec.getOption('extralabel',"").split("\\n")))
#        if islog: maximum = tmpMin * pow(tmpMax/tmpMin,1./relHistHeight);
#        else: maximum = (tmpMax-tmpMin)/relHistHeight + tmpMin
#        total.SetMaximum(maximum)

        ratioHist.Draw()
        ratioHist.GetYaxis().SetRangeUser(yMin,yMax)
        ratioHist.GetXaxis().SetRangeUser(3,10)

        ratioHist.GetYaxis().SetTitle(ytitle)
        if xtitle!="":ratioHist.GetXaxis().SetTitle(xtitle)

        from CMGTools.TTHAnalysis.tools.plotDecorations import fitTGraph,histToGraph
        graph = histToGraph(ratioHist)
        fitTGraph(graph,order=1)

        decorrFitGraph = graph.Clone()

        ratioHist.Draw("same")
        
        ypoints = graph.band68.GetY()
        ypoints2 = graph.band68.GetEYhigh()

        print len(ypoints),len(ypoints2), graph.band68.GetN()
        
        sumw = 0
        sumwtimesx=0
        for i in range (0,graph.GetN()):
            x, y, ex, ey = ROOT.Double(0),ROOT.Double(0), 0, 0
            print i,
            graph.GetPoint(i,x,y)
            ex = graph.GetErrorX(i)
            ey = graph.GetErrorY(i)
            print x,y, ex, ey
            w = 1/(ey*ey)
            sumw += w
            sumwtimesx += w*x
        wmean = sumwtimesx/sumw
        print "wmean", wmean

        orthonormLinear = TF1("orthonormLinear","[0] +(x-{})*[1]".format(wmean),0,10)
        print "[0] +(x-{})*[1]".format(wmean)
        fitresult = decorrFitGraph.Fit(orthonormLinear,"SN0 EX0")

        orthonormLinear.SetLineColor(1)
        orthonormLinear.SetLineStyle(2)
#        orthonormLinear.Draw("same")
#        for i,y in enumerate(ypoints):
#            print y

        retUncUp = ROOT.TGraphErrors()
        retUncDn = ROOT.TGraphErrors()
        nPoints = graph.band68.GetN()
#        xmin = 0
#        xmax = 10
#        points = [ xmin + i*(xmax-xmin)/(nPoints-1) for i in xrange(nPoints) ]



        ywm = orthonormLinear.Eval(wmean)
        print "ywm", ywm
        nPoints = nPoints
        for i in range(0,nPoints):
            retUncUp.Set(retUncUp.GetN()+1)
            retUncDn.Set(retUncDn.GetN()+1)

            x, y, ex, ey = ROOT.Double(0),ROOT.Double(0), 0, 0
#            print i,
            graph.band68.GetPoint(i,x,y)
            ex = graph.band68.GetErrorX(i)
            ey = graph.band68.GetErrorY(i)

            y = orthonormLinear.Eval(x)
            eyup = 0
            if y>ywm:
                eyup = +ey
                eydn = -ey
            else:
                eyup = -ey
                eydn = +ey
#            print eyup
            retUncUp.SetPoint(i, x, eyup)
            retUncDn.SetPoint(i, x, eydn)

#            retUncUp.SetPoint(retUncUp.GetN()-1, x, yvalue)

        print "WeightDict = dict([",
        for i in range (3,12):
            print "( {} , {:.4f}), ".format(i, 1+retUncUp.Eval(i+0.5))
        print "])"
        
            

        retUncUp.SetLineColor(2)
        retUncDn.SetLineColor(1)
#        retUncUp.Draw("same")
#        retUncDn.Draw("same")



#        fitresult = "Fit: \\n const:  %.2f \pm %.2f; \\n slope:  %.2f \pm %.2f; \\n weighted mean %.2f " %(orthonormLinear.GetParameter(0),orthonormLinear.GetParError(0),orthonormLinear.GetParameter(1),orthonormLinear.GetParError(1), wmean)
        fitresult = "Fit: \\n const:  %.2f +/- %.2f; \\n slope:  %.2f +/- %.2f; \\n weighted mean %.2f " %(orthonormLinear.GetParameter(0),orthonormLinear.GetParError(0),orthonormLinear.GetParameter(1),orthonormLinear.GetParError(1), wmean)
# , " slope: ", orthonormLinear.GetParameter(1),"\pm", orthonormLinear.GetParError(1) ,

        if extraLabel!="": printExtraLabel(extraLabel+"\\n"+fitresult,'TR')
        else: printExtraLabel(fitresult,'TR')        
#        doCMSlumi(c1)
        ROOT.gPad.Update()
        ROOT.gPad.RedrawAxis()
        c1.Print(".png")
        #        c1.Print(".eps")
        c1.Print(".pdf")

    def __init__(self,plotsDiLepton, plotsSingleLepton,pathDiLeptonROOTFile,pathSingleLeptonROOTFile,options):
        self._options = options
        self.plotsDiLepton            = plotsDiLepton            
        self.plotsSingleLepton        = plotsSingleLepton        

        self.diLepFile     = ROOT.TFile(pathDiLeptonROOTFile     ,"READ")
        self.singleLepFile = ROOT.TFile(pathSingleLeptonROOTFile ,"READ")

        pspecs1l = plotsSingleLepton.plots()
        pspecs2l = plotsDiLepton.plots()
        
        islog = False

        for i, pspec in enumerate(pspecs1l):
            print "SingleLep: ", pspec.name
            print "DiLep: ", pspecs2l[i].name
            assert len(pspec.bins) == len(pspecs2l[i].bins)
            assert pspec.bins == pspecs2l[i].bins
            print pspec.bins
            dilepbkg = self.diLepFile.Get(pspecs2l[i].name+"_background")
            singlepbkg = self.singleLepFile.Get(pspec.name+"_background")
            dilepdata = self.diLepFile.Get(pspecs2l[i].name+"_data")
            singlepdata = self.singleLepFile.Get(pspec.name+"_data")
            print pspecs2l[i].name+"_ratio"
            dilepratio = dilepdata.Clone("_dilepbkgratio")
            dilepratio.Divide(dilepbkg)

            singlepratio = singlepdata.Clone("_singlepbkgratio")
            singlepratio.Divide(singlepbkg)

#            dilepratio = self.diLepFile.Get(pspecs2l[i].name+"_ratio")
#            singlepratio = self.singleLepFile.Get(pspec.name+"_ratio")

            DoubleRatio = dilepratio.Clone()
            DoubleRatio.Divide(singlepratio)
            DoubleRatio.SetTitle("")

            extralabel=""
            if pspec.hasOption('extralabel'): extralabel = pspec.getOption('extralabel')


            self.plotRatioWithFit(dilepratio,pspec.name+"_DilepRatio",extralabel,-0.0,2.0)
            self.plotRatioWithFit(singlepratio,pspec.name+"_SinglepRatio",extralabel,-0.0,2.0)
            self.plotRatioWithFit(DoubleRatio,pspec.name+"_DoubleRatio",extralabel,-0.0,2.0,"(Data/MC)_{2l}/(Data/MC)_{1l}", "jet multiplicity")


            


if __name__ == "__main__":
    from optparse import OptionParser
    print "just try... "
    print "python -i plotDoubleRatios.py 2L_ForDL_plots.txt 1L_ForDL_plots.txt plots_2L/2L_ForDL_plots.root plots_1L/1L_ForDL_plots.root"
    print
    parser = OptionParser(usage="%prog [options] plotsDilepton.txt plotsSingleLepton.txt pathDiLeptonROOTFile pathSingleLeptonRootFile")
    parser.add_option("-o", "--out", dest="out", default="DefaultOutput", help="Output file name");
    addPlotMakerOptions(parser)
    (options, args) = parser.parse_args()
    options.lumi=2.3
    plotsDiLepton      = PlotFile(args[0],options)
    plotsSingleLepton  = PlotFile(args[1],options)

    pathDiLeptonROOTFile = args[2]
    pathSingleLeptonROOTFile = args[3]

    outname  = options.out if options.out else (args[1].replace(".txt","")+"DoubleRatio.root")
    if (not options.out) and options.printDir:
        outname = options.printDir + "/"+os.path.basename(args[2].replace(".txt","")+".root")
    if os.path.dirname(outname) and not os.path.exists(os.path.dirname(outname)):
        os.system("mkdir -p "+os.path.dirname(outname))
        if os.path.exists("/afs/desy.de"): os.system("cp /afs/cern.ch/user/a/alobanov/public/php/index.php  "+os.path.dirname(outname))

    print "Will save plots to ",outname

    outfile  = ROOT.TFile(outname,"RECREATE")

#Do the plotting....
#    plotter = PlotMaker(outfile)
#    plotter.run(mca,cuts,plots)

    DoubleRatioPlotter( plotsDiLepton,
                        plotsSingleLepton,
                        pathDiLeptonROOTFile, 
                        pathSingleLeptonROOTFile,
                        options)
    outfile.Close()


