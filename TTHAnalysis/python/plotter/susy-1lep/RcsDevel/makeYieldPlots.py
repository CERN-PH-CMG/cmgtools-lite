#!/usr/bin/env python
import sys, math

from yieldClass import *
from ROOT import *

## ROOT STYLE
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadTopMargin(0.075)
gStyle.SetPadLeftMargin(0.05)
gStyle.SetPadRightMargin(0.025)
gStyle.SetPadBottomMargin(0.25)
gStyle.SetLegendBorderSize(0)

## CMS LUMI
import CMS_lumi

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
#iPos = 11
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.05


## Global vars
_alpha = 0.55
colorList = [2,4,7,9,8,3,6] + range(10,50)
_histStore = {}
_lines = []

_batchMode = True#False

colorDict = {'TTJets': kBlue-4,'TTdiLep':kBlue-4,'TTsemiLep':kBlue-2,'WJets':kGreen-2,
             'QCD':kCyan-6,'SingleT':kViolet+5,'DY':kRed-6,'TTV':kOrange-3,'data':1,'background':2,'EWK':3}

# from CMGTools.TTHAnalysis.plotter.mcPlots import getDataPoissonErrors
def getDataPoissonErrors(h, drawZeroBins=False, drawXbars=False):
    xaxis = h.GetXaxis()
    q=(1-0.6827)/2.;
    points = []
    errors = []
    for i in xrange(h.GetNbinsX()):
        N = h.GetBinContent(i+1);
        dN = h.GetBinError(i+1);
        if drawZeroBins or N > 0:
            if N > 0 and dN > 0 and abs(dN**2/N-1) > 1e-4: 
                #print "Hey, this is not Poisson to begin with! %.2f, %.2f, neff = %.2f, yscale = %.5g" % (N, dN, (N/dN)**2, (dN**2/N))
                yscale = (dN**2/N)
                N = (N/dN)**2
            else:
                yscale = 1
            x = xaxis.GetBinCenter(i+1);
            points.append( (x,yscale*N) )
            EYlow  = (N-Math.chisquared_quantile_c(1-q,2*N)/2.) if N > 0 else 0
            EYhigh = Math.chisquared_quantile_c(q,2*(N+1))/2.-N;
            EXhigh, EXlow = (xaxis.GetBinUpEdge(i+1)-x, x-xaxis.GetBinLowEdge(i+1)) if drawXbars else (0,0)
            errors.append( (EXlow,EXhigh,yscale*EYlow,yscale*EYhigh) )
    ret = TGraphAsymmErrors(len(points))
    ret.SetName(h.GetName()+"_graph")
    for i,((x,y),(EXlow,EXhigh,EYlow,EYhigh)) in enumerate(zip(points,errors)):
        ret.SetPoint(i, x, y)
        ret.SetPointError(i, EXlow,EXhigh,EYlow,EYhigh)
    ret.SetLineWidth(h.GetLineWidth())
    ret.SetLineColor(h.GetLineColor())
    ret.SetLineStyle(h.GetLineStyle())
    ret.SetMarkerSize(h.GetMarkerSize())
    ret.SetMarkerColor(h.GetMarkerColor())
    ret.SetMarkerStyle(h.GetMarkerStyle())
    return ret

def doLegend(pos = "TM",nEntr = None):

    if pos == "TM":
        if nEntr:
            leg = TLegend(0.4,0.875-(nEntr*0.2),0.6,0.875)
        else:
            #leg = TLegend(0.4,0.5,0.6,0.85)
            leg = TLegend(0.3,0.5,0.45,0.85)
    elif pos == "TMR":
        leg = TLegend(0.35,0.5,0.55,0.85) # Top Middle Right
    elif pos == "Long":
        #leg = TLegend(0.2,0.75,0.85,0.85) # Top
        leg = TLegend(0.2,0.35,0.85,0.45) # Bottom
    elif pos == "Wide":
        leg = TLegend(0.3,0.5,0.55,0.85)
    elif pos == "TRC":
        #leg = TLegend(0.65,0.55,0.925,0.9)
        #leg = TLegend(1-gStyle.GetPadRightMargin()-0.25,0.55,1-gStyle.GetPadRightMargin(),1-gStyle.GetPadTopMargin())
        leg = TLegend(1-gStyle.GetPadRightMargin()-0.35,0.55,1-gStyle.GetPadRightMargin(),1-gStyle.GetPadTopMargin())
        #leg = TLegend(1-gStyle.GetPadRightMargin()-0.35,0.65,1-gStyle.GetPadRightMargin(),1-gStyle.GetPadTopMargin())
        #leg = TLegend(1-gStyle.GetPadRightMargin()-0.4,0.65,1-gStyle.GetPadRightMargin(),1-gStyle.GetPadTopMargin())

    leg.SetBorderSize(1)
    leg.SetTextFont(62)
    #leg.SetTextSize(0.03321678)
    leg.SetTextSize(0.05)

    if pos != "TRC":
        leg.SetLineColor(0)
        leg.SetLineStyle(0)
        leg.SetLineWidth(0)

    if _batchMode == False: leg.SetFillColor(0)
    #else: leg.SetFillColorAlpha(0,_alpha)
    else: leg.SetFillColorAlpha(0,1)

    leg.SetFillStyle(1001)
    #leg.SetFillStyle(0)

    return leg

def getSampLabel(name):

    names = {
        "TT" : "t#bar{t} + jets",
        "TTJets" : "t#bar{t} + jets",
        "TTsemiLep" : "t#bar{t} (1l) + jets",
        "TTdiLep" : "t#bar{t} (2l) + jets",
        "SingleTop" : "t/#bar{t}",
        "SingleT" : "t/#bar{t}",
        "WJets" : "W + jets",
        "DY" : "DY+jets",
        "QCD": "QCD",
        "TTV": "ttV(W/Z)"
        }

    if name in names: return names[name]
    else: return name

def getSampColor(name):

    if "TT_" in name: name = name.replace("TT_","TTJets_")

    for samp in sorted(colorDict.keys()):
        if samp == name:
            return colorDict[samp]

    for samp in sorted(colorDict.keys()):
        if samp in name:
            return colorDict[samp]

    else: return 1

def prepKappaHist(hist):
    # prepare hist to be kappa

    hist.GetYaxis().SetNdivisions(505)
    hist.GetYaxis().SetTitle("#kappa")
    hist.GetYaxis().CenterTitle()
    hist.GetYaxis().SetTitleSize(0.1)
    hist.GetYaxis().SetTitleOffset(0.2)

    hist.GetYaxis().SetLabelSize(0.1)
    hist.GetYaxis().SetRangeUser(0.05,1.95)

    hist.GetXaxis().SetLabelSize(0.1)

def getUniqLabels(labels):

    nbin = len(labels[0].split("_"))

    # Dict that counts labels
    binCnts = {n:set() for n in range(nbin)}

    # Count appearance of bins
    for lab in labels:
        labs = lab.split("_")
        for i in range(len(labs)):
            binCnts[i].add(labs[i])

    #print binCnts

    # Make labels with short names
    newLabs = {}
    for lab in labels:
        labs = lab.split("_")
        newlab = "_".join(bin for i,bin in enumerate(labs) if len(binCnts[i]) > 1)
        newLabs[lab] = newlab

    return newLabs

def getCleanLabel(binLabel):

    # standart replacements
    binLabel = binLabel.replace("_SR","")
    binLabel = binLabel.replace("_CR","")
    binLabel = binLabel.replace("f6","")
    binLabel = binLabel.replace("f9","")

    binLabel = binLabel.replace("LTi","")

    # NB
    #binLabel = binLabel.replace("NB0","")
    #binLabel = binLabel.replace("NB2i","")
    '''
    binLabel = binLabel.replace("_NB1_","_1b_")
    binLabel = binLabel.replace("_NB1i_","_#geq1b_")
    binLabel = binLabel.replace("_NB2_","_2b_")
    binLabel = binLabel.replace("_NB2i_","_#geq2b_")
    binLabel = binLabel.replace("_NB3i_","_#geq3b_")
    '''

    # NJ
    #binLabel = binLabel.replace("_NJ68","")
    binLabel = binLabel.replace("_NJ68","_6-8j")
    binLabel = binLabel.replace("_NJ9i","_#geq9j")
    #binLabel = binLabel.replace("_",",")

    return binLabel

def makeSampHisto(yds, samp, cat, hname = "", ind = 0):

    # yield dict
    ydict = yds.getSampDict(samp,cat)

    if not ydict:
        print "Could not read dict", samp, cat
        return 0

    # create histo
    #binList = sorted(ydict.keys())
    binList = []
    # sort bins by NJ
    for njbin in ['NJ3','NJ4','NJ5','NJ6','NJ9']:
        binList += [b for b in sorted(ydict.keys()) if njbin in b]

    nbins = len(binList)

    if hname == "": hname = samp + "_" + cat
    if "Rcs" in cat:
        htitle = cat.replace("Rcs_","R_{CS}^{") + "} (%s)" %samp
    else:
        #htitle = cat + " (%s)" %samp
        htitle = "%s" %samp

    #hist = TH1F(hname,hname,nbins,-0.5,nbins+0.5)
    hist = TH1F(hname,htitle,nbins,0,nbins)

    # for bin labels
    labels = []
    for ibin,bin in enumerate(binList):
        label = ydict[bin].label if ydict[bin].label != "" else bin
        labels.append(getCleanLabel(label))

    #ulabs = getUniqLabels(labels)

    # fill histo
    for ibin,bin in enumerate(binList):

        #binLabel = bin
        binLabel = ydict[bin].label
        if binLabel == "": binLabel = bin

        binLabel = getCleanLabel(binLabel)

        #if binLabel in ulabs: binLabel = ulabs[binLabel]

        newLabel = "#splitline"

        splitbins = binLabel.split("_")#[:2]
        nbins = len(splitbins)

        if nbins == 2:
            newLabel = "#splitline{%s}{%s}" %(splitbins[0],splitbins[1])
        elif nbins == 3:
            newLabel = "#splitline{%s}{#splitline{%s}{%s}}" %(splitbins[0],splitbins[1],splitbins[2])
        elif nbins == 4:
            newLabel = "#splitline{%s}{#splitline{%s}{#splitline{%s}{%s}}}" %(splitbins[0],splitbins[1],splitbins[2],splitbins[3])
        else:
            newLabel = binLabel

        hist.GetXaxis().SetBinLabel(ibin+1,newLabel)

        hist.SetBinContent(ibin+1,ydict[bin].val)
        hist.SetBinError(ibin+1,ydict[bin].err)

    # options
    hist.GetXaxis().LabelsOption("h")

    # Style
    if ("Kappa" not in cat) and ("Rcs" not in cat):
    #    col = getSampColor(hist.GetName())
        col = getSampColor(hist.GetName())
    else:
        col = getSampColor(hist.GetName())
    #    col = getSampColor(samp)
    #    col = colorList[ind]
    #print "color for %s  %i" %(hist.GetName(),col)

    if "data" not in hist.GetName():
        if _batchMode == True:
            hist.SetFillColorAlpha(col,_alpha)
        else:
            hist.SetFillColor(col)
            hist.SetFillStyle(3001)

    hist.SetLineColor(col)
    #hist.SetLineColor(1)
    hist.SetMarkerColor(col)
    hist.SetMarkerStyle(20)

    if "Kappa" in cat:
        #hist.GetYaxis().SetRangeUser(0.05,1.95)
        hist.GetYaxis().SetTitle("Kappa")
    elif "Rcs" in cat:
        #hist.GetYaxis().SetRangeUser(0.005,0.35)
        hist.GetYaxis().SetTitle("R_{CS}")
    else:
        hist.GetYaxis().SetTitle("Events")

    #SetOwnership(hist, 0)
    _histStore[hist.GetName()] = hist
    return hist

def makeSampHists(yds,samps):

    histList = []

    for ind,(samp,cat) in enumerate(samps):

        #yd = yds.getSampDict(samp,cat)
        #if yd:
        hist = makeSampHisto(yds,samp,cat,"",ind)

        histList.append(hist)

    return histList

def getMarks(hist):

    if hist.ClassName() == "THStack":
        hist = hist.GetHistogram()
    elif "TGaph" in hist.ClassName():
        hist = hist.GetHistogram()

    # line markers
    marks = []
    ltmark = 0

    for bin in range(1,hist.GetNbinsX()+1):
        # for vertical lines
        binLabel = hist.GetXaxis().GetBinLabel(bin).replace("#splitline{","")
        #print binLabel

        ltbin = binLabel.split("}")[0] # should be LT
        #print ltbin, ltmark
        if ltmark == 0: ltmark = ltbin
        elif ltmark != ltbin:
            ltmark = ltbin
            marks.append(bin)

    return marks

def prepRatio(hist, keepStyle = False):

    hist.GetYaxis().CenterTitle()
    hist.GetYaxis().SetNdivisions(505)
    hist.GetYaxis().SetTitleSize(0.08)
    hist.GetYaxis().SetTitleOffset(0.3)
    hist.GetYaxis().SetLabelSize(0.1)
    hist.GetXaxis().SetLabelOffset(0.018)
    hist.GetXaxis().SetLabelSize(0.1)

    hist.SetFillColor(0)
    hist.SetFillStyle(0)

    if not keepStyle:
        hist.SetLineColor(1)
        hist.SetMarkerColor(1)
        print hist.GetName()
        #if ("SR" not in hist.GetName()) or ("CR" not in hist.GetName()):
        hist.GetYaxis().SetRangeUser(0.05,2.1)

    return hist


def getRatio(histA,histB, keepStyle = False):

    ratio = histA.Clone("ratio_"+histA.GetName()+"_"+histB.GetName())
    if "TGraph" not in histA.ClassName():
        ratio.Divide(histB)
        hRatio = ratio
    else:
        for i in xrange(ratio.GetN()):
            x    = ratio.GetX()[i]
            div  = histB.GetBinContent(histB.GetXaxis().FindBin(x))
            ratio.SetPoint(i, x, ratio.GetY()[i]/div if div > 0 else 0)
            ratio.SetPointError(i, ratio.GetErrorXlow(i), ratio.GetErrorXhigh(i),
                                ratio.GetErrorYlow(i)/div  if div > 0 else 0,
                                ratio.GetErrorYhigh(i)/div if div > 0 else 0)
            #if div > 0:
            #    print i, x, div, ratio.GetY()[i]/div

        hRatio = ratio.GetHistogram()

    #hRatio.GetYaxis().SetTitle("Ratio")
    title = "#frac{%s}{%s}" %(histA.GetTitle(),histB.GetTitle())
    hRatio.GetYaxis().SetTitle(title)
    hRatio.GetYaxis().CenterTitle()
    hRatio.GetYaxis().SetNdivisions(505)
    hRatio.GetYaxis().SetTitleSize(0.08)
    hRatio.GetYaxis().SetTitleOffset(0.3)
    hRatio.GetYaxis().SetLabelSize(0.1)

    ymax = min(2.9,1.3*hRatio.GetMaximum())
    ymin = 0.8*min(hRatio.GetMinimum(),0.85)
    hRatio.GetYaxis().SetRangeUser(ymin,ymax)
    hRatio.SetMaximum(ymax)
    hRatio.SetMinimum(ymin)

    hRatio.GetXaxis().SetLabelSize(0.1)
    hRatio.GetXaxis().SetLabelOffset(0.018)

    if not keepStyle:
        hRatio.SetLineColor(1)
        hRatio.SetMarkerColor(1)
        hRatio.SetMarkerStyle(20)
    hRatio.SetFillColor(0)
    hRatio.SetFillStyle(0)

    _histStore[hRatio.GetName()] = ratio
    return ratio

def getPull(histA,histB):

    pull = histA.Clone("pull_"+histA.GetName()+"_"+histB.GetName())
    pull.Add(histB,-1)
    #pull.Divide(histB)

    for ibin in range(1,pull.GetNbinsX()+1):
        err = histB.GetBinError(ibin)
        if err > 0:
            pull.SetBinContent(ibin,pull.GetBinContent(ibin)/err)
            pull.SetBinError(ibin,pull.GetBinError(ibin)/err)
        else:
            pull.SetBinContent(ibin,0)
            pull.SetBinError(ibin,0)

    #pull.GetYaxis().SetTitle("Pull")
    #title = "#frac{%s - %s}{%s}" %(histA.GetTitle(),histB.GetTitle(),histB.GetTitle())
    #title = "#frac{%s - %s}{#sigma(%s)}" %(histA.GetTitle(),histB.GetTitle(),histA.GetTitle())
    title = "#frac{%s - %s}{#sigma(%s)}" %(histA.GetTitle(),histB.GetTitle(),histB.GetTitle())

    pull.GetYaxis().SetTitle(title)
    pull.GetYaxis().CenterTitle()
    pull.GetYaxis().SetNdivisions(505)
    pull.GetYaxis().SetTitleSize(0.1)
    pull.GetYaxis().SetTitleOffset(0.3)

    pull.GetYaxis().SetLabelSize(0.1)
    pull.GetYaxis().SetRangeUser(-5,5)

    pull.GetXaxis().SetLabelSize(0.1)

    pull.SetLineColor(1)
    #pull.SetMarkerColor(1)
    pull.SetFillColor(0)
    pull.SetFillStyle(0)

    return pull

def getStack(histList):

    if len(histList) == 0: return 0

    hname = histList[0].GetName() + "stack"

    #stack = THStack("stack","stack")
    stack = THStack(hname,histList[0].GetTitle())

    for i,hist in enumerate(histList):
        stack.Add(hist)

        #style
        if _batchMode == True:
            hist.SetFillColorAlpha(hist.GetFillColor(),_alpha)
        else:
            hist.SetFillStyle(1001)

    # Options
    #stack.Draw("GOFF") # GOFF doesn't actually draw anything
    #stack.GetXaxis().LabelsOption("v")

    return stack

def getSquaredSum(histList):

    sqHist = histList[0].Clone(histList[0].GetName() + "_sqSum")

    for i,hist in enumerate(histList):
        if i > 0:
            for bin in range(1,hist.GetNbinsX()+1):
                x = sqHist.GetBinContent(bin)
                new = x*x + hist.GetBinContent(bin)*hist.GetBinContent(bin)
                sqHist.SetBinContent(bin, math.sqrt(new))
    sqHist.SetMarkerStyle(34)
    sqHist.SetMarkerSize(2)
    sqHist.SetMarkerColor(kBlack)
    sqHist.SetTitle("sqSum")
    #sqHist.SetName("sqSum")
    return sqHist

def getHistWithError(hCentral, hSyst, new = True):
    if new:
        histWithError = hCentral.Clone(hCentral.GetName() + "wErr")
        histWithError.SetFillColor(kBlue)
        histWithError.SetFillStyle(3002)
    else:
        histWithError = hCentral

    for bin in range(1,hCentral.GetNbinsX()+1):

        #print bin, histWithError.GetBinContent(bin),histWithError.GetBinError(bin), hSyst.GetBinContent(bin), "\t",

        sys = hCentral.GetBinContent(bin)*hSyst.GetBinContent(bin)
        #err = math.sqrt(hCentral.GetBinError(bin)*hCentral.GetBinError(bin) + sys*sys)
        err = math.hypot(hCentral.GetBinError(bin),sys)
        histWithError.SetBinError(bin, err)

        #print sys, histWithError.GetBinError(bin)

    return  histWithError



def getTotal(histList):
    # to be used only for ratio and error band

    total = histList[0].Clone("total")
    total.Reset()
    total.SetTitle("total")
    total.SetName("total")

    for hist in histList:  total.Add(hist)

    total.SetLineColor(0)
    total.SetFillColor(kGray)
    total.SetFillStyle(3244)
    total.SetMarkerStyle(0)
    total.SetMarkerColor(0)

    return total

def setUnc(hist):

    #gStyle.SetHatchesLineWidth(1)

    hist.SetLineWidth(1)
    hist.SetLineColor(0)
    hist.SetFillColor(kGray)
    hist.SetFillStyle(3244)
    hist.SetMarkerStyle(0)
    hist.SetMarkerColor(0)

def getCatLabel(name):

    cname = name
    cname = cname.replace("_"," ")
    cname = cname.replace("SB","N_{j} #in [4,5]")

    #cname = cname.replace("MB","N_{j} #in [6,8]")
    #cname = cname.replace("MB","N_{j} #geq 9")
    cname = cname.replace("MB predict X NJ5X","N_{j} = 5")
    cname = cname.replace("MB predict X NJ68X","N_{j} #in [6,8]")
    cname = cname.replace("MB predict X NJ9X","N_{j} #geq 9")
    #cname = cname.replace("MB","N_{j} == 5")

    # Signal
    cname = cname.replace("T1tttt Scan","T1tttt")
    if "mLSP" in cname:
        cname = cname.replace("mGo","(")
        cname = cname.replace(" mLSP",",")
        cname += ")"

    return cname

def plotHists(cname, histList, ratio = None, legPos = "TM", width = 800, height = 600, logY = False, nCols = 1):

    #canv = TCanvas(cname,cname,1400,600)
    canv = TCanvas(cname,cname,width,height)
    #leg = doLegend(len(histList)+1)
    leg = doLegend(legPos)
    leg2 = doLegend("TM")

    if legPos == "Long":
        nh = 1
        for hist in histList:
            if hist.ClassName() == "THStack":
                nh += len(hist.GetHists())
            else:
                nh += 1
        leg.SetNColumns(nh)

    leg.SetNColumns(nCols)

    if legPos == "Wide":
        leg.SetNColumns(2)
    #if legPos == "TRC":
    #    leg.SetNColumns(2)

    SetOwnership(canv, 0)
    SetOwnership(leg, 0)

    head = getCatLabel(cname)
    #leg.SetHeader(head)

    if ratio != None:

        if type(ratio) == list:
            ratios = ratio
            ratio = ratios[0]
            multRatio = True
        else:
            multRatio = False

        #canv.SetWindowSize(600 + (600 - canv.GetWw()), (750 + (750 - canv.GetWh())));
        p2 = TPad("pad2","pad2",0,0,1,0.31);
        p2.SetTopMargin(0);
        p2.SetBottomMargin(0.31);
        p2.SetFillStyle(0);
        p2.Draw();

        p1 = TPad("pad1","pad1",0,0.31,1,1);
        p1.SetBottomMargin(0.02);
        p1.Draw();

        p2.cd()

        if "Uncert" in ratio.GetName():
            plotOpt = "e2"
        elif "appa" in ratio.GetName():
            plotOpt = "e1"
        else:
            plotOpt = "pe1"

        # 1 - line
        if "TH1" not in ratio.ClassName():
            ratio.Draw(plotOpt+"A")
            hRatio = ratio.GetHistogram()
        else:
            ratio.Draw(plotOpt)
            hRatio = ratio

        rname = hRatio.GetName()
        #xmin = hRatio.GetXaxis().
        if "pull" in rname: line = TLine(0,0,hRatio.GetNbinsX(),0)
        elif "ratio" in rname: line = TLine(0,1,hRatio.GetNbinsX(),1)
        elif "Kappa" in rname: line = TLine(0,1,hRatio.GetNbinsX(),1)
        else: line = None #TLine(0,0,hRatio.GetNbinsX(),0)

        if line != None:
            line.SetLineColor(kGray)
            line.SetLineWidth(1)
            line.Draw()
            SetOwnership(line,0)

        # plot bins separator
        marks = getMarks(hRatio)
        # do vertical lines
        if len(marks) != 0:
            #print marks
            axis = hRatio.GetXaxis()
            ymin = hRatio.GetMinimum(); ymax = hRatio.GetMaximum()
            #ymin = hRatio.GetYaxis().GetXmin(); ymax = hRatio.GetYaxis().GetXmax()
            for i,mark in enumerate(marks):
                pos = axis.GetBinLowEdge(mark)
                line = TLine(pos,ymin,pos,ymax)
                #line.SetName("line_mark_"+str(mark))
                line.SetLineStyle(3)
                if i == 3: line.SetLineStyle(2) # nj6 -> nj9
                line.Draw("same")
                _lines.append(line)

        #redraw ratio on top of lines
        hRatio.Draw("same"+plotOpt)


        if multRatio:
            for rat in ratios[1:]:
                #rat.Draw(plotOpt+"same")
                if "TGraph" in rat.ClassName():
                    rat.Draw("pe1same")
                else:
                    rat.Draw("pe2same")

        p1.cd();
    else:
        canv.SetBottomMargin(0.1)

    # get Y-maximum/minimum
    ymax = max([h.GetMaximum() for h in histList])
#    ymin = min([h.GetMinimum() for h in histList]);

    extHistList = [] + histList
    for h in histList:
        if h.ClassName() == "THStack":
            extHistList += [h for h in h.GetHists()]

    ymin = min([h.GetMinimum() for h in extHistList]);

    # for fractions set min to 0
    if not logY:
        if ymax < 1.01 and ymax >= 1: ymax == 1; ymin = 0 # for fractions
        else: ymax *= 1.5; ymin *= 0.5; ymin = max(0,ymin)
    else:
        #ymax *= 100; ymin = max(0.05,0.5*ymin)
        ymax *= 10; ymin = max(0.05,0.5*ymin)

    #ymin = 0
    #ymax = min(ymax, 1.5)

    # Common plot option
    plotOpt = ""#X+Y+"

    # make dummy for stack
    if histList[0].ClassName() == "THStack":
        dummy = histList[0].GetHists()[0].Clone("dummy")
        dummy.Reset()
        # draw dymmy first
        _histStore[dummy.GetName()] = dummy
        #histList = [dummy] + histList
        histList.insert(0,dummy)

    for i,hist in enumerate(histList):

        if not hist.ClassName() == 'THStack':

            hist.GetYaxis().SetTitleSize(0.05)
            hist.GetYaxis().SetTitleOffset(0.5)

            if ratio == None: hist.GetYaxis().SetLabelSize(0.04)
            else: hist.GetYaxis().SetLabelSize(0.05)

        # range
        hist.SetMaximum(ymax)
        hist.SetMinimum(ymin)
        #print hist.GetName()
        if "dummy" == hist.GetName():
            hist.Draw(plotOpt)
        elif  hist.ClassName() == 'THStack':
            #continue
            hist.Draw("HISTsame"+plotOpt)
            hist.GetXaxis().LabelsOption("h")
            hist.GetYaxis().SetTitle("Events")
            hist.GetYaxis().SetTitleSize(0.1)
            hist.GetYaxis().SetTitleOffset(0.5)

            for h in reversed(hist.GetHists()):
                leg.AddEntry(h,getSampLabel(h.GetTitle()),"f")
        elif ("data" in hist.GetName()) or ("Data" in hist.GetName()):
            hist.Draw(plotOpt+"pE1")
            leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"pe")
        elif "total" in hist.GetName():
            hist.Draw(plotOpt+"E2")
            leg.AddEntry(hist,"MC Uncertainty","f")
        elif "uncert" in hist.GetName():
            hist.Draw(plotOpt+"E2")
            leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"f")
        elif "Syst" in hist.GetName():
            hist.Draw(plotOpt+"E2")
            leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"f")
        elif "pred" in hist.GetName():
            hist.Draw(plotOpt+"pE1")
            leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"pl")
        elif "SigStack" in hist.GetName():
            hist.Draw(plotOpt+"hist")
            leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"l")
        elif "sqSum" in hist.GetName():
            hist.Draw(plotOpt+"p")
            #leg.AddEntry(hist,"Sum squared uncertainties","p")
            leg.AddEntry(hist,"Total","p")
        else:
            if len(histList) < 3:
                hist.Draw(plotOpt+"pE2")
                leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"pf")
            else:
                hist.Draw(plotOpt+"pE2")
                leg.AddEntry(hist,getSampLabel(hist.GetTitle()),"pf")

        # remove axis label with ratio
        if i == 0 and ratio != None:
            hist.GetXaxis().SetLabelOffset(1)

        if i == 0:
            # do vertical lines
            marks = getMarks(hist)
            if len(marks) != 0:
                #print marks
                axis = hist.GetXaxis()
                for i,mark in enumerate(marks):
                    pos = axis.GetBinLowEdge(mark)
                    line = TLine(pos,ymin,pos,ymax)
                    #line.SetName("line_mark_"+str(mark))
                    line.SetLineStyle(3)
                    if i == 3: line.SetLineStyle(2) # nj6 -> nj9
                    line.Draw("same")
                    _lines.append(line)

        if "same" not in plotOpt: plotOpt += "same"

    #canv.BuildLegend()
    leg.Draw()
    SetOwnership(leg,0)

    '''
    # Add right axis
    raxis = TGaxis(gPad.GetUxmax(),gPad.GetUymin(),gPad.GetUxmax(), gPad.GetUymax(),0,ymax,510,"+L")
    #axis.SetLineColor(kRed);
    #axis.SetTextColor(kRed);
    raxis.SetTitleSize(0.05)
    raxis.SetTitleOffset(0.6)

    if ratio == None: raxis().SetLabelSize(0.4)
    else: raxis.SetLabelSize(0.05)
    raxis.Draw();
    '''

    # draw CMS lumi
    if ratio != None:
        CMS_lumi.CMS_lumi(p1, 4, iPos)
        p2.SetTicks()
        p2.Update()

        # Add ticks
        p1.SetTicks()
        p1.Update()

        if logY: p1.SetLogy()

    else:
        CMS_lumi.CMS_lumi(canv, 4, iPos)

        # Add ticks
        canv.SetTicks()
        canv.Update()

        if logY: canv.SetLogy()


    #gPad.RedrawAxis()

    return canv

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

    '''

    #ydQCD = yds.getSampDict("QCD","CR_SB")
    #hist = makeSampHisto(ydQCD,"QCD_CRSB")

    #yd = yds.getSampDict("EWK","CR_SB")
    #hist = makeSampHisto(yd,"h")

    samps = [
    ("background_QCDsubtr","CR_SB"),
    ("EWK","CR_SB"),
    ("data_QCDsubtr","CR_SB"),
    ]

    yds.printMixBins(samps)

    samps = [
    ("background","CR_SB"),
    ("background_QCDsubtr","CR_SB"),
    ("EWK","CR_SB"),
    #("data_QCDsubtr","CR_SB"),
    ]

    sampsRcs = [
    ("EWK","Rcs_SB"),
    ("EWK","Rcs_MB"),
    ]

    rcsHists = makeSampHists(yds,sampsRcs)
    hKappa = makeSampHists(yds,[("EWK","Kappa")])[0]


    prepKappaHist(hKappa)

    canv = plotHists("bla",rcsHists,hKappa)

    '''
    cat = "SR_MB"


    #mcSamps = [samp for samp in yds.samples if ("backgr" not in samp or "data" not in samp or "EWK" not in samp)]
    mcSamps = ['DY','TTV','SingleT','WJets','TT','QCD']
    #mcSamps = ['WJets','TT','QCD']
    print mcSamps

    samps = [(samp,cat) for samp in mcSamps]
    #add ewk
    #samps["EWK"] = cat

    print samps

    hists = makeSampHists(yds,samps)
    stack = getStack(hists)
    total = getTotal(hists)

    # Totals
    tots = [("background",cat),("data",cat)]
    #tots = [("background",cat),("background",cat)]

    hTot = makeSampHists(yds,tots)

    #stack.Draw("HIST")
    #canv = plotHists(cat,[stack,total]+hTot)
    #canv = plotHists(cat,[stack]+hTot)

    ratio = getRatio(hTot[1],total)

    canv = plotHists("AntiEle_"+cat,[stack,total,hTot[1]],ratio)
    #canv = plotHists("AntiEle_"+cat,[stack,total],ratio)

    #canv = plotHists(cat,[ratio])

    #hist.Draw("p")

    if not _batchMode: raw_input("Enter any key to exit")
    canv.SaveAs("BinPlots/"+mask+canv.GetName()+".pdf")
