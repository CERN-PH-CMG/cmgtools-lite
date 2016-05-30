#!/usr/bin/env python

import sys
import os
from math import hypot

#tmpArg = sys.argv
#sys.argv = ['-b']
from ROOT import *
#sys.argv = tmpArg

## STYLE
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetPadTopMargin(0.06)
gStyle.SetPadRightMargin(0.075)

#gStyle.SetLabelFont(62)
#gStyle.SetTitleFont(62)

## CMS Lumi
#from CMGTools.TTHAnalysis.plotter.CMS_lumi import CMS_lumi
#import CMGTools.TTHAnalysis.plotter.CMS_lumi
#sys.path.append("$CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/")
import CMS_lumi

CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.1

## Canvas sizes
cwidth = 800
cheigth = 800

## DICTS for storage
_dhStore = {}
_pdfStore = {}
_varStore = {}
_hStore = {}
_canvStore = {}

def decryptBinName(binname):

    #print 'Binname before', binname
    binname = binname.replace("_"," ")
    binname = binname.replace('NJ34','')
    #binname = binname.replace('NJ34','N_{jet} #in [3,4] ')

    if "LT" not in binname: binname += "L_{T} #geq 250"
    elif "LTi" in binname: binname = binname.replace("LTi","L_{T} #geq 250")
    elif "LT1i" in binname: binname = binname.replace("LT1i","L_{T} #geq 250")
    elif "LT1" in binname: binname = binname.replace("LT1","L_{T} #in [250,350]")
    elif "LT2i" in binname: binname = binname.replace("LT2i","L_{T} #geq 350")
    elif "LT2" in binname: binname = binname.replace("LT2","L_{T} #in [350,450]")
    elif "LT3i" in binname: binname = binname.replace("LT3i","L_{T} #geq 450")
    elif "LT3" in binname: binname = binname.replace("LT3","L_{T} #in [450,600]")
    elif "LT4" in binname: binname = binname.replace("LT4","L_{T} #geq 600")

    #print 'Binname after', binname
    return binname

def doLegend():

    #leg = TLegend(0.63,0.525,0.87,0.875)
    leg = TLegend(0.6,0.525,0.9,0.875)
    leg.SetBorderSize(1)
    leg.SetTextFont(62)
    leg.SetTextSize(0.03321678)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(1001)

    return leg

def getHistIntError(hist):
    # rebin hist to 1 bin and get the error

    htmp = hist.Clone('tmp')
    htmp.Rebin(htmp.GetNbinsX())

    return htmp.GetBinError(1)

def getVarFromHist(hist, varname):

    minX = hist.GetXaxis().GetXmin();
    maxX = hist.GetXaxis().GetXmax();
    nBins = hist.GetNbinsX();

    # Create observable
    var = RooRealVar(varname, varname, minX, maxX)
    var.setBins(nBins);

    return var

def getPDFfromHist(hist, var):

    hname = hist.GetName()

    # binned dataset
    dh = RooDataHist('dh'+hname,'dh'+hname,RooArgList(var),hist)
    _dhStore[dh.GetName()] = dh # store dh
    # pdf from dh
    pdf = RooHistPdf('pdf'+hname,'pdf'+hname,RooArgSet(var),dh,0)
    _pdfStore[pdf.GetName()] = pdf

    return pdf

def getDataFromHist(hist, var, mcData = True):

    hname = hist.GetName()

    # binned dataset
    dh = RooDataHist('dh'+hname,'dh'+hname,RooArgList(var),hist)
    _dhStore[dh.GetName()] = dh # store dh

    if mcData:
        nevents = hist.Integral()
        # pdf from dh
        pdf = RooHistPdf('pdf'+hname,'pdf'+hname,RooArgSet(var),dh,0)
        _pdfStore[pdf.GetName()] = pdf

        # generate toys
        data = pdf.generateBinned(RooArgSet(var),nevents,RooFit.Name("pseudoData"))

        return data

    else:
        return dh

def setHistRange(hist, maxX = 2.0, minX = 0.5):
    # modifies range by setting bins to zero

    for ibin in range(hist.GetNbinsX()):
        if hist.GetBinCenter(ibin) < minX or hist.GetBinCenter(ibin) > maxX:
            hist.SetBinContent(ibin,0)

def getQCDfromFit(dhData, hQCD, hEWK, var):

    # modify range of QCD
    #setHistRange(hQCD)

    # get PDFs for QCD and EWK
    pdfQCD = getPDFfromHist(hQCD, var)
    pdfEWK = getPDFfromHist(hEWK, var)

    _pdfStore[pdfQCD.GetName()] = pdfQCD
    _pdfStore[pdfEWK.GetName()] = pdfEWK

    # Number of (pseudo)data events for limits
    nevents = dhData.sumEntries()

    # Number of EWK and QCD events as variables
    nEWK = RooRealVar("nEWK","#EWK events",nevents,0,2*nevents)
    nQCD = RooRealVar("nQCD","#QCD events",nevents,0,2*nevents)

    _varStore['nEWK'] = nEWK
    _varStore['nQCD'] = nQCD

    pdfTemplate = RooAddPdf("pdfTemplate","EWK + QCD template",RooArgList(pdfEWK,pdfQCD),RooArgList(nEWK,nQCD));

    pdfTemplate.fitTo(dhData,RooFit.PrintLevel(-1))#,RooFit.SumW2Error(kTRUE))
    #pdfTemplate.chi2FitTo(dhData,RooLinkedList())#RooFit.SumW2Error(kTRUE))

    _pdfStore[pdfTemplate.GetName()] = pdfTemplate

    return nQCD#(nQCD.getValV(),nQCD

def getHistsFromFile(tfile, binname = 'incl', mcData = True):

    # get full BKG, QCD and EWK histos
    QCDseleName = 'Lp_sel_'+binname+'_QCD'

    if mcData:
        QCDantiName = 'Lp_anti_'+binname+'_QCD' # anti shape from MC
    else:
        QCDantiName = 'Lp_anti_'+binname+'_data' # anti shape from DATA
    #QCDantiName = 'Lp_anti_incl_QCD'

    hQCDsele = tfile.Get(QCDseleName).Clone('QCDsel_'+binname)
    hQCDanti = tfile.Get(QCDantiName).Clone('QCDanti_'+binname)

    _hStore[hQCDsele.GetName()] = hQCDsele
    _hStore[hQCDanti.GetName()] = hQCDanti

    EWKselName = 'Lp_sel_'+binname+'_background'
    hEWKsele = tfile.Get(EWKselName).Clone('EWKsel_'+binname)

    _hStore[hEWKsele.GetName()] = hEWKsele

    if mcData:
        # Create ~DATA~ hist from selected QCD and EWK
        hData = hEWKsele.Clone('DataSel_'+binname)
        hData.Add(hQCDsele)
    else:
        # take data histogram
        hData = tfile.Get('Lp_sel_'+binname+'_data').Clone('DataSel_'+binname)

    _hStore[hData.GetName()] = hData

    # return data hist, EWK and QCD templates
    return (hData,hEWKsele,hQCDsele,hQCDanti)

def plotHists(binname = 'incl', inclTemplate = False, mcData = True, addHists = True):

    # frame
    frame = _varStore['Lp'].frame(RooFit.Title('Lp distributions and fit in bin '+binname))

    _dhStore['data_'+binname].plotOn(frame,RooFit.Name('data'),RooFit.DataError(RooAbsData.SumW2) )#,RooLinkedList())

    # plot full template fit
    _pdfStore['pdfTemplate'].plotOn(frame,RooFit.LineColor(2),RooFit.Name('FullFit'))
    # plot only QCD component
    if not inclTemplate:
        argset = RooArgSet(_pdfStore['pdfQCDanti_'+binname]) # hack to keep arguments alive
    else:
        import re
        incName = re.sub('LT[0-9]','LTi',binname) # use LTi as inclusive template
        if 'pdfQCDanti_'+incName not in _pdfStore: incName = re.sub('LT[0-9]_','',binname) # remove LTx to get incl template
        argset = RooArgSet(_pdfStore['pdfQCDanti_'+incName]) # hack to keep arguments alive
    _pdfStore['pdfTemplate'].plotOn(frame,RooFit.Components(argset),RooFit.LineColor(kCyan),RooFit.LineStyle(5),RooFit.Name('QCDfit'))
    # plot only EWK
    argset2 = RooArgSet(_pdfStore['pdfEWKsel_'+binname]) # hack to keep arguments alive
    _pdfStore['pdfTemplate'].plotOn(frame,RooFit.Components(argset2),RooFit.LineColor(4),RooFit.LineStyle(2),RooFit.Name('EWKfit'))

    # PLOT
    canv = TCanvas("cQCDfit_"+binname,"canvas for bin "+binname,cwidth, cheigth)

    if cheigth == cwidth:
        frame.GetYaxis().SetTitleOffset(1.3)

    frame.Draw()

    if addHists:

        doTransp = True

        if doTransp:
            alpha = 0.35
            _hStore['EWKsel_'+binname].SetFillColorAlpha(_hStore['EWKsel_'+binname].GetFillColor(),alpha)
            _hStore['QCDsel_'+binname].SetFillColorAlpha(_hStore['QCDsel_'+binname].GetFillColor(),alpha)
        else:
            _hStore['EWKsel_'+binname].SetFillStyle(3001)
            _hStore['QCDsel_'+binname].SetFillStyle(3002)

        stack = THStack('hs','hstack')
        stack.Add(_hStore['QCDsel_'+binname])
        stack.Add(_hStore['EWKsel_'+binname])
        stack.Draw("histsame")
        #_hStore['QCDsel_'+binname].Draw("histsame")

        SetOwnership( stack, 0 )
        #SetOwnership( _hStore['QCDsel_'+binname], 0 )
        #SetOwnership( _hStore['EWKsel_'+binname], 0 )
        #hData.Draw('histsame')

    frame.Draw("same")

    # LEGEND
    leg = doLegend()

    # set legend header = bin name
    #leg.SetHeader("Bin: " + binname.replace("_",", "))
    leg.SetHeader("Bin: " + decryptBinName(binname))

    if mcData:
        leg.AddEntry(frame.findObject('data'),'Pseudo Data','lp')
    else:
        leg.AddEntry(frame.findObject('data'),'Data','lp')

    leg.AddEntry(frame.findObject('FullFit'),'Full fit','l')
    leg.AddEntry(frame.findObject('QCDfit'),'QCD fit (Data)','l')
    leg.AddEntry(frame.findObject('EWKfit'),'EWK fit (MC)','l')


    if addHists:
        leg.AddEntry(0,"From MC:","")
        leg.AddEntry(_hStore['EWKsel_'+binname],'EWK selected','f')
        leg.AddEntry(_hStore['QCDsel_'+binname],'QCD selected','f')


    leg.Draw()

    SetOwnership( leg, 0 )

    #for prim in  canv.GetListOfPrimitives(): print prim

    # Draw CMS Lumi
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()

    if '-b' not in sys.argv:
        # wait for input
        answ = ['c']
        while 'c' not in answ:
            answ.append(raw_input("Enter 'c' to continue: "))

    _canvStore[canv.GetName()] = canv

    return canv

#def getQCDratio(tfile,binname = 'incl', doPlot = False, mcData = False, doClosure = False, inclTemplate = False):
def getQCDratio(tfile, options, binname = 'incl'):

    if options.verbose > 0:
        print 80*'#'
        print 'Going to calculate F-ratio in bin', binname
        print 80*'#'

    if options.mcData and options.verbose > 0:
        print 'Data is taken from toys!'

    # get full BKG, QCD and EWK histos
    (hData,hEWKsele,hQCDsele,hQCDanti) = getHistsFromFile(tfile, binname,  options.mcData)

    if options.verbose > 1:
        # Print some info
        print 10*'-'
        print 'Number of events in anti-selected bin'
        print 'QCD: %.3f +/- %.3f' % ( hQCDanti.Integral(), getHistIntError(hQCDanti))
        print 10*'-'
        print 'Number of events in selected bin'
        print 'Data: %.3f' % hData.Integral()
        print 'EWK: %.3f' % hEWKsele.Integral()
        print 'QCD: %.3f +/- %.3f' %( hQCDsele.Integral(), getHistIntError(hQCDsele))
        print 10*'-'

    # Create Lp var from hist
    lp = getVarFromHist(hData, "L_{p}")

    _varStore['Lp'] = lp

    # Deal with data (pseudo or real)
    data = getDataFromHist(hData,lp, options.mcData)

    _dhStore['data_'+binname] = data

    # take anti from LT-inclusive QCD:
    if options.inclTemplate:
        import re
        incName = re.sub('LT[0-9]','LTi',binname) # use LTi as inclusive template
        if 'QCDanti_'+incName not in _hStore: incName = re.sub('LT[0-9]_','',binname) # remove LTx to get incl template
        if 'QCDanti_'+incName not in _hStore: print "Didn't find inclusive template!";

        if options.verbose > 0:
            print 'Using template', incName, 'instead of', binname
        hQCDanti = _hStore['QCDanti_'+incName]

    # Get QCD prediction in the selected region
    nQCD = getQCDfromFit(data,hQCDanti,hEWKsele,lp)

    nQCDsel = nQCD.getValV()
    nQCDselErr = nQCD.getError()

    if options.verbose > 0:
        print 'Fit result:'
        print 'QCD: %.3f +/- %.3f ' % (nQCDsel, nQCDselErr)


    # get correct QCD anti
    if options.inclTemplate:
        hQCDanti = _hStore['QCDanti_'+binname]


    if not options.doClosure:
        #determine F ratio as selected(fit)/anti-selected(data/mc)
        fRatio = nQCDsel/hQCDanti.Integral()

        nQCDanti =  hQCDanti.Integral()
        nQCDantiErr = getHistIntError(hQCDanti)

        # calculate error
        #fRatioErr = fRatio*TMath.Sqrt(nQCDselErr/nQCDsel*nQCDselErr/nQCDsel + nQCDantiErr/nQCDanti*nQCDantiErr/nQCDanti)
        fRatioErr = fRatio*hypot(nQCDselErr/nQCDsel,nQCDantiErr/nQCDanti)
    else:
        if options.verbose > 0:
            print '#!CLOSURE: F-ratio is QCD selected(fit)/selected(data/mc)'
        #determine F ratio as selected(fit)/selected(data/mc)
        fRatio = nQCDsel/hQCDsele.Integral()

        nQCDsele =  hQCDsele.Integral()
        nQCDseleErr = getHistIntError(hQCDsele)

        # calculate error
        #fRatioErr = fRatio*TMath.Sqrt(nQCDselErr/nQCDsel*nQCDselErr/nQCDsel + nQCDseleErr/nQCDsele*nQCDseleErr/nQCDsele)
        fRatioErr = fRatio*hypot(nQCDselErr/nQCDsel,nQCDseleErr/nQCDsele)

    if options.verbose > 0:
        print 'F_ratio = %.3f +/- %.3f'%(fRatio,fRatioErr)

    if options.doPlot:
        if options.verbose > 0: print 10*'-'
        canv = plotHists(binname, options.inclTemplate, options.mcData)

    return (fRatio,fRatioErr)

def plotFratios(resList, isClosure = False):

    nbins = len(resList)

    if not isClosure:
        hist = TH1F('hRatios','F-Ratios',nbins,0,nbins)
    else:
        hist = TH1F('hClosure','MC/Fit ratios',nbins,0,nbins)

    for i,(bin,val,err) in enumerate(resList):
        #print bin, val
        #binName = bin[:bin.find("_NJ")]
        binName = bin
        hist.GetXaxis().SetBinLabel(i+1,decryptBinName(binName))
        hist.SetBinContent(i+1,val)
        hist.SetBinError(i+1,err)

    _hStore[hist.GetName()] = hist
    hist.SetStats(0)

    canv=TCanvas(hist.GetName(),hist.GetTitle(),cwidth, cheigth)

    # style
    hist.SetMarkerStyle(20)
    hist.Draw('E1p')
    hist.GetYaxis().SetTitleOffset(1.4)

    if not isClosure:
        hist.GetYaxis().SetTitle("F_{sel-to-anti} QCD")

        #hist.GetYaxis().SetRangeUser(0.,0.8)
    else:
        hist.GetYaxis().SetTitle("F_{fit-to-mc} QCD_{selected}")
        #hist.GetYaxis().SetRangeUser(0.4,1.3)

        # unity line
        line = TLine(0,1,hist.GetNbinsX(),1)
        line.SetLineStyle(2)
        line.Draw('same')
        SetOwnership(line,0)

    # Draw CMS Lumi
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()

    _canvStore[canv.GetName()] = canv

    return hist

if __name__ == "__main__":

    # OPTIONS

    from optparse import OptionParser
    parser = OptionParser()

    parser.usage = '%prog [options]'
    parser.description="""
    Make QCD fits with Lp
    """

    # bools
    parser.add_option("-b","--batch", dest="batch",default=False, action="store_true", help="Batch mode")
    parser.add_option("-c","--closure", dest="doClosure",default=False, action="store_true", help="Do closure of MC/Fit")
    parser.add_option("-p","--plot", dest="doPlot",default=True, action="store_true", help="Make Lp plots")
    parser.add_option("-i","--inclTempl", dest="inclTemplate",default=False, action="store_true", help="Use Lp template from inclusive LT bin")
    parser.add_option("--mc","--mcData", dest="mcData",default=False, action="store_true", help="Use pseudo-data from MC")
    # int/floats
    parser.add_option("-v","--verbose",  dest="verbose",  default=1,  type="int",    help="Verbosity level (0 = quiet, 1 = verbose, 2+ = more)")
    parser.add_option("-l","--lumi",  dest="lumi",  default=1.55,  type="float",    help="Luminosity in /fb")

    # Read options and args
    (options,args) = parser.parse_args()

    # disable RooFit info
    if options.verbose < 3:
        RooMsgService.instance().setGlobalKillBelow(RooFit.WARNING)

    ## Check options
    if options.doClosure and not options.mcData:
        #print "Do you really want to make a closure test with Data? [y/n]"

        answ = []
        answ.append(raw_input("Do you really want to make a closure test with Data? [y/n] "))

        while( 'y' not in answ or 'n' not in answ):
            if 'y' in answ:
                break
            elif 'n' in answ:
                print 'Switching to pseudo-data from MC'
                options.mcData = True
                break
            else:
                answ.append(raw_input("Enter 'y' or 'n'"))

    ## Lumi setup
    if options.mcData:
        #CMS_lumi.lumi_13TeV = "MC"
        CMS_lumi.lumi_13TeV = str(options.lumi) + " fb^{-1}"
        CMS_lumi.extraText = "Simulation"
    else:
        CMS_lumi.lumi_13TeV = str(options.lumi) + " fb^{-1}"
        CMS_lumi.extraText = "Preliminary"

    infileName = "../lp_only_plots.root"

    if len(sys.argv) > 1:
        infileName = sys.argv[1]
        print 'Infile is', infileName
    else:
        print 'No file name is given'
        exit(0)

    tfile = TFile(infileName,"READ")

    # select bin
    binNames = ['incl']
    #binNames += ['HT500toInf','HT500to1000','HT750to1000','HT500to750']
    #binNames = ['incl','NB1','NB2','NB3']
    #binNames = ['incl','NJ34']
    #binNames = ['NJ34']
    #binNames = ['NJ34','LT1_NJ34']

    binNames = ['LTi_NJ34','LT1_NJ34','LT2_NJ34','LT3_NJ34','LT4_NJ34']
    #binNames = ['LTi_NJ34','LT1_NJ34','LT1i_NJ34','LT2_NJ34','LT2i_NJ34','LT3_NJ34','LT3i_NJ34','LT4_NJ34']

    #binNames += ['NJ45','LT0_NJ45','LT1_NJ45','LT2_NJ45','LT3_NJ45','LT4_NJ45']
    #binNames += ['NJ68','LT0_NJ68','LT1_NJ68','LT2_NJ68','LT3_NJ68','LT4_NJ68']
    #binNames += ['NJ6inf','LT0_NJ6inf','LT1_NJ6inf','LT2_NJ6inf','LT3_NJ6inf','LT4_NJ6inf']
    #binNames += ['NJ45','NJ68','LT0_NJ45','LT0_NJ68','LT1_NJ45','LT1_NJ68','LT2_NJ45','LT2_NJ68','LT3_NJ45','LT3_NJ68','LT4_NJ45','LT4_NJ68']

    resList = []

    for binName in binNames:
        #(fRat,err) = getQCDratio(tfile,binName, doPlots, mcData, doClosure, inclTemplate)
        (fRat,err) = getQCDratio(tfile, options, binName)
        resList.append((binName,fRat,err))

    print 80*'='

    # Plot results in one histo
    hRatio = plotFratios(resList,options.doClosure)

    print 'Finished fitting. Saving Canvases...'

    ##### SAVING

    # Suffix for Data/MC
    if options.mcData: suff = "_MC"
    else: suff = "_Data"

    # Get infile dir name
    indir= os.path.dirname(infileName)

    plotDir = indir + "/QCDFits/"

    # label inclusive or not
    if options.inclTemplate: plotDir += "InclTemplate/"
    else: plotDir += "NonInclTemplate/"

    if not os.path.isdir(plotDir): os.makedirs(plotDir)
    print "Saving results to" , plotDir

    # save plots to root file
    pureFname = os.path.basename(infileName).replace(".root","")

    if not options.doClosure:        pureFname += '_f-ratios'
    else:        pureFname += '_closure'

    outfile = TFile(plotDir+pureFname+'_plots'+suff+'.root','RECREATE')
    print 'Saving plots to file', outfile.GetName()

    extList = ['.png','.pdf','.root']

    if options.verbose < 2:
        gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")

    for canvKey in _canvStore:
        canv = _canvStore[canvKey]
        canv.Write()
        # write in different extensions
        for ext in extList:
            canv.SaveAs(plotDir+canv.GetName()+suff+ext)

    # save ratio hist
    hRatio.Write()

    if options.verbose > 0:
        print 40*'/\\'
        print 'Compact results'
        for (bin,fRat,err) in resList:
            #fRat, err) = ratioDict[bin]
            print 'Bin\t %s has F ratio\t %.3f +/- %.3f (%.2f %% error)' %(bin, fRat, err, 100*err/fRat)
            #print '%s\t%.3f\t%.3f' % (bin, fRat, err)
        print 40*'\\/'

    # Write results to txt file
    txtFname = pureFname + suff +".txt"

    with open(plotDir+txtFname,"w") as ftxt:

        headline = "#Bin\tF-Ratio\tError\n"
        ftxt.write(headline)

        print "Writing ratios to txt file", txtFname
        for (bin,fRat,err) in resList:
            line =  '%s\t\t%.3f\t%.3f\n' %(bin, fRat, err)
            ftxt.write(line)

    if '-b' not in sys.argv:
        # wait for input
        answ = []
        while 'q' not in answ:
            answ.append(raw_input("Enter 'q' to exit: "))

    # close
    tfile.Close()
    outfile.Close()
