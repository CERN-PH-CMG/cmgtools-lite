#!/usr/bin/python

import sys

from math import *
from array import array
from ROOT import *

from triggTools import *

# global storages
_canvStore = []
_histStore = {}
_hEffStore = {}

_fitrStore = []

_colorList = [2,4,8,9,7,3,6] + range(10,50)

def getLumiFromName(name):

    if 'pb' in name or 'fb' in name:
        pass
    else:
        print 'No lumi in name!'
        return 666

def getHistsFromTree(tree, var = 'MET', refTrig = '', cuts = '', testTrig = '', maxEntries = -1, lumi = -1):

    # maximum number of entries to process
    if maxEntries == -1:
        maxEntries = tree.GetEntries()

    # histogram name prefix
    histPrefix = 'h' + var + '_'

    # plot option
    plotOpt = 'e1'

    # histogram list
    histList = []

    # prepend HLT name
    testTrig = ['HLT_'+name.replace('HLT_','') for name in testTrig]

    # names
    if 'HLT' in refTrig:
        refName = refTrig.replace('HLT_','')
    elif refTrig != '':
        refName = refTrig#'PreSel'
        refTrig = ''
    else:
        refName = 'PreSel'

    ## name replacement
    refName = renameTrig(refName)

    # for OR and AND test triggers
    if '||' in refTrig:
        tnames = refTrig.replace('HLT_','').split('||')
        refTrigName = tnames[0]
        refTrig = '(' + 'HLT_'+tnames[0].replace('HLT_','')

        for name in tnames[1:]:
            refTrigName += '||' + name
            refTrig += '||' + 'HLT_'+name.replace('HLT_','')
        refTrig += ')'

        print refTrigName
        print refTrig
    else:
        refTrigName = refTrig.replace('HLT_','')

    refTrigName = renameTrig(refTrigName)

#    refName = refTrigName
#    print 'New', refTrigName, refTrig
#    exit(0)

    rname = histPrefix + refName

    cname = var + '_' + refName
    ctitle = 'Plots for reference:' + refName

    if cuts != '':
        ctitle += ' cut: ' + cuts

    if refTrig != '':
        #cuts += ' && HLT_' + refTrig.replace('HLT_','')
        cuts += ' && ' + refTrig
        htitle = refTrig.replace('HLT_','')#'Ref: ' + refTrig
    else:
        htitle = 'Preselection'

    print 'Going to draw', ctitle

    # make canvas
    canv = TCanvas(cname,ctitle,800,800)

    # make hist
    nbins = 50

    varBinSize = False

    if options.logX:
        global pt_bins, lt_bins, ht_bins
        #pt_bins = getLogBins(30,0.9,1000)
        pt_bins = getLogBins(33,0.9,1500)
        #lt_bins = getLogBins(20,9,1000)
        lt_bins = getLogBins(22,9,3000)
        ht_bins = getLogBins(30,30,2000)

    if 'MET' in var:
        hRef = TH1F(rname,htitle,nbins,0,1000)
        varBinSize = True
        hRef = TH1F(rname,htitle,len(met_bins)-1,array('f',met_bins))
    elif 'HT' in var:
        varBinSize = True
        hRef = TH1F(rname,htitle,len(ht_bins)-1,array('f',ht_bins))
        #hRef = TH1F(rname,htitle,nbins,0,3000)
    elif 'LT' in var:
        hRef = TH1F(rname,htitle,nbins,0,1000)
        varBinSize = True
        hRef = TH1F(rname,htitle,len(lt_bins)-1,array('d',lt_bins))
    elif 'pt' in var:
        varBinSize = True
        hRef = TH1F(rname,htitle,len(pt_bins)-1,array('d',pt_bins))
        #hRef = TH1F(rname,htitle,nbins,0,200)
    elif 'eta' in var:
        #print eta_bins; exit(0)
        #hRef = TH1F(rname,htitle,nbins,-2.5,2.5)
        hRef = TH1F(rname,htitle,len(eta_bins)-1,array('f',eta_bins))
    else:
        hRef = TH1F(rname,htitle,nbins,0,1000)

    ## lumi scaling
    if lumi == 0:
        # don't do lumi scaling on MC
        doLumi = False
        CMS_lumi.lumi_13TeV = "MC"
        CMS_lumi.extraText = "Simulation"
        hRef.GetYaxis().SetTitle('MC counts')
    elif lumi > 0:
        # make lumi label for data
        doLumi = False
        #CMS_lumi.lumi_13TeV = str(lumi) + " pb^{-1}"
        if lumi < 10:
            CMS_lumi.lumi_13TeV = str(lumi) + " fb^{-1}"
        else:
            CMS_lumi.lumi_13TeV = str(lumi) + " fb^{-1}"

        CMS_lumi.extraText = "Preliminary"
        hRef.GetYaxis().SetTitle('Events')
    elif lumi < 0:
        # do lumi scaling for MC
        doLumi = True
        lumi = abs(lumi)
        CMS_lumi.lumi_13TeV = str(lumi) + " fb^{-1}"
        CMS_lumi.extraText = "Simulation"
        hRef.GetYaxis().SetTitle('Events')

    # make reference plot
    if not doLumi:
        #hRef.Sumw2(False)
        tree.Draw(var + '>>' + hRef.GetName(),cuts,plotOpt, maxEntries)
        print '# Drawing', hRef.GetName(), 'with cuts', cuts
    else:
        hRef.Sumw2()

        wt = 1000*lumi/float(maxEntries)
        print '# Weight for %2.2f lumi and maxEntries %10.f is %f' %(lumi, maxEntries,wt)
        weight = str(wt) + ' * Xsec'
        if cuts != '': wcuts = weight + '*(' + cuts + ')'
        else: wcuts = weight
        print '# Drawing', hRef.GetName(), 'with cuts', wcuts

        tree.Draw(var + '>>' + hRef.GetName(),wcuts,plotOpt, maxEntries)
        hRef.SetMaximum(hRef.GetMaximum() * 2)

    ## do overflow
    doOverflow = False#True

    if doOverflow:
        n = hRef.GetNbinsX()
        print hRef.GetBinContent(n+1),hRef.GetBinContent(n)
        hRef.SetBinContent(n,hRef.GetBinContent(n+1)+hRef.GetBinContent(n))
        hRef.SetBinError(n,hypot(hRef.GetBinError(n+1),hRef.GetBinError(n)))
        hRef.SetBinContent(n+1,0)
        hRef.SetBinError(n+1,0)
        hRef.Sumw2(False)

    print '# Found', hRef.Integral(), 'events'

    hRef.SetLineColor(1)
    # axis set up
    hRef.SetStats(0)

    label = varToLabel(var)
    if 'eta' not in label:
        label += ' [GeV]'

    hRef.GetXaxis().SetTitle(label)
    hRef.GetXaxis().SetTitleOffset(1.2)
    hRef.GetXaxis().SetNoExponent(1)
    hRef.GetXaxis().SetMoreLogLabels(1)

    hRef.GetYaxis().SetTitleOffset(1.2)
    canv.SetLogy()
    if options.logX:
        canv.SetLogx()

    gPad.Update()

    _histStore[hRef.GetName()] = hRef
    histList.append(hRef)

    # loop over test triggers:
    for ind, trig in enumerate(testTrig):

        # for OR and AND test triggers
        if '||' in trig:
            tnames = trig.replace('HLT_','').split('||')
            trigName = tnames[0]
            trig = '(' + 'HLT_'+tnames[0].replace('HLT_','')

            for name in tnames[1:]:
                trigName += '||' + name
                trig += '||' + 'HLT_'+name.replace('HLT_','')
            trig += ')'

            print trigName
            print trig
        else:
            trigName = trig.replace('HLT_','')

        trigName = renameTrig(trigName)

        hname = 'h' + var + '_' + trigName

        hTest = hRef.Clone(hname)
        hTest.SetTitle(trigName)

        hTest.SetLineColor(_colorList[ind])

        # cuts

        if cuts != '':
            tcuts = cuts + ' && ' + trig
        else:
            tcuts = trig

        print '# Drawing', hTest.GetName(), 'with cuts', tcuts

        # lumi scale
        if not doLumi:
            tree.Draw(var + '>>' + hTest.GetName(),tcuts,plotOpt+'same', maxEntries)
            #hTest.Sumw2(False)
        else:
            #hTest.Sumw2()
            if tcuts != '': wtcuts = weight + '*(' + tcuts + ')'
            else: wtcuts = weight
            tree.Draw(var + '>>' + hTest.GetName(),wtcuts,plotOpt+'same', maxEntries)

        if doOverflow:
            n = hTest.GetNbinsX()
            hTest.SetBinContent(n,hTest.GetBinContent(n+1)+hTest.GetBinContent(n))
            hTest.SetBinError(n,hypot(hTest.GetBinError(n+1),hTest.GetBinError(n)))
            hTest.SetBinContent(n+1,0)
            hTest.SetBinError(n+1,0)
            hTest.Sumw2(False)

        print '# Found', hTest.Integral(), 'events'

        gPad.Update()

        _histStore[hTest.GetName()] = hTest
        histList.append(hTest)

    # if var bin sizes
    if varBinSize and False: # leave it off for now (strange errors)

        # add /bin in Y axis label
        hRef.GetYaxis().SetTitle(hRef.GetYaxis().GetTitle() + '/bin')

        for hist in histList:
            for bin in range(1,hist.GetNbinsX()+1):
                binC = hist.GetBinContent(bin)
                binE = hist.GetBinError(bin)
                binW = hist.GetBinWidth(bin)

                binV = binC/binW
                binE = binE/binW
                #print binC, binW, binV

                hist.SetBinContent(bin, binV)
                #hist.SetBinError(bin, binE)

        hist.Sumw2(False)

    #hRef.SetTitle(ctitle)

    # legend
    leg = canv.BuildLegend()
    leg.SetFillColor(0)
    #leg.SetHeader(ctitle.replace('&&','\n'));

    # plot CMS info
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()
    gPad.RedrawAxis()
    _canvStore.append(canv)

    return histList

def plotEff(histList, var = 'HT', doFit = False):


    ## histList: [hReference, hTest1, hTest2,...]

    # hist prefix
    histPrefix = 'h' + var + '_'

    # reference hist should be first
    #hRef = histList[0].Clone(histList[0].GetName()+"Ref")
    hRef = histList[0]
    hRefEff = hRef.Clone(hRef.GetName()+'Eff')
    # set reference eff to 1
    hRefEff.Divide(hRef)

    hRefEff.GetYaxis().SetTitle("Efficiency")

    if not doFit:
        cname = hRef.GetName().replace('h'+var,var) + '_Eff_'
    else:
        cname = hRef.GetName().replace('h'+var,var) + '_EffFit'

    ctitle = 'Eff for reference:' + hRefEff.GetName()

    ## make canvas
    canv = TCanvas(cname,ctitle,800,800)
    #canv.UseGL()
    #canv.SetSupportGL(True)
    ## style

    ## legend
    leg = getLegend('fit2')

    # set reference eff to 1
    for bin in range(1,hRefEff.GetNbinsX()+1):
        hRefEff.SetBinContent(bin,1)
        hRefEff.SetBinError(bin,0)

    hRefEff.Draw()
    #leg.AddEntry(0,'Reference: ' + hRefEff.GetName(),'')
    pureName = hRef.GetName().replace('h'+var+'_','')
    leg.SetHeader('Reference: ' + cleanName(pureName))
    #leg.AddEntry(hRefEff,hRefEff.GetTitle(),'lp')

    # axis set up
    hRefEff.SetStats(0)
    #hRef.GetXaxis().SetTitle(var)
    hRefEff.GetYaxis().SetRangeUser(0.01,1.5)
    canv.SetTicks(1,0)
    #canv.SetLogy()

    '''
    if len(histList) == 2:
        # add normalized hist shape
        hRef.SetFillColorAlpha(hRef.GetLineColor(),0.35)
        hRef.DrawNormalized("same")
        leg.AddEntry(hRef,varToLabel(var)+' distribution','f')
    '''

    plotOpt = 'same'

    gPad.Update()

    # loop over test
    #for ind,hname in enumerate(nameList):
    for ind,hist in enumerate(histList[1:]):

        #hist = _histStore[hname]
        hname = hist.GetName()

        # filter out hists
        #if histPrefix not in hname: continue
        #if 'Ref' in hname: continue

        htitle = hname.replace(histPrefix,'')
        hname = hname.replace('h','hEff')

        print 'Drawing', hname, 'from', hRef.GetName()

        ## Divide
        hEff = hist.Clone(hname+"Eff")
        hEff.Divide(hRef)

        ## TEfficiency
        tEff = TEfficiency(hist,hRef)
        tEff.SetName(hname);#+';'+var+';Efficiency')
        tEff.SetTitle(htitle)

        # style
        if len(histList) == 2: # for one single curve
            tEff.SetLineColor(1)#kBlue)
            tEff.SetMarkerColor(1)#kBlue)
        else:
            tEff.SetLineColor(hist.GetLineColor())
            tEff.SetMarkerColor(hist.GetLineColor())

        tEff.SetFillColor(0)
        tEff.SetMarkerStyle(20)

        tEff.Draw(plotOpt)
        leg.AddEntry(tEff,tEff.GetTitle(),'lpe')

        if len(histList) == 2:

            # transparent color for hist and axis
            hCol = kBlue #hist.GetLineColor()
            hAlpha = 0.35

            # add normalized hist shape
            hist.SetFillColorAlpha(hCol,hAlpha)
            hist.SetLineColorAlpha(hCol,hAlpha)

            sf = 0.5/hist.GetMaximum()
            hist.Scale(sf)
            #hist.DrawNormalized("samehist")
            hist.Draw("samehist")

            leg.AddEntry(hist,varToLabel(var)+' distribution','f')

            # extra axis
            #scale = 1.5*hist.GetEntries()#/hist.GetMaximum()#*1.1/1.5
            scale = 1/sf#hist.GetEntries()#/hist.GetMaximum()#*1.1/1.5
            #scale = 1.5

            raxis = TGaxis(gPad.GetUxmax(),gPad.GetUymin(),gPad.GetUxmax(), gPad.GetUymax()/1.5,0.01,scale,505,"+L")
            raxis.SetLineColor(hCol)
            raxis.SetLabelColor(hCol)
            raxis.SetTitleColor(hCol)
            raxis.SetTitle("Events")
            raxis.SetMaxDigits(3)
            raxis.Draw()
            SetOwnership(raxis, 0)

        if 'same' not in plotOpt: plotOpt += 'same'

        gPad.Update()

        #SetOwnership(tEff,0)

        if doFit and hEff.GetEntries() > 0 and 'eta' not in var:
            ## Fitting turn on curve
            print 'Fitting...'

            xmin = hEff.GetXaxis().GetXmin()
            xmax = hEff.GetXaxis().GetXmax()

            fturn = TF1("turnon",turnon_func,xmin,xmax,3)
            fturn.SetParNames('halfpoint','width','plateau')
            fturn.SetParLimits(0,0,10000)
            fturn.SetParLimits(1,0.1,10000)
            fturn.SetParLimits(2,0,1)

            fturn.SetLineColor(hEff.GetLineColor())

            ## get painted graph and fit with turn-on
            #print tEff
            gEff = tEff.GetPaintedGraph()
            #print gEff
            #gEff = hEff

            ## get estimate of parameters
            expPlateau = min(hEff.GetMaximum(),0.99)
            expHalfP = max(hEff.GetBinCenter(hEff.FindFirstBinAbove(0.5)),0)
            expWidth = TMath.Sqrt(expHalfP)

            #fturn.SetParameters(300,100,1)
            fturn.SetParameters(expHalfP,expWidth,expPlateau)

            ## do fit
            fitr = gEff.Fit(fturn,'S Q E EX0')#EX0

            SetOwnership(gEff,0)

            halfpoint = fitr.Value(0)
            width = fitr.Value(1)
            plateau = fitr.Value(2)

            print 'Expected values: halfpoint = %5.2f, width = %5.2f, plateau = %5.2f' % (expHalfP, expWidth, expPlateau)
            print 'Fit result: halfpoint = %5.2f, width = %5.2f, plateau = %5.2f' % (halfpoint, width, plateau)

            # get 0.99% of plateau
            xpl = 0
            for x in range(int(xmin),int(xmax)):
                tpl = fturn(x)
                if tpl > 0.98*plateau:
                    xpl = x
                    break

            ## asymmetric errors
            #print 'Upper/Lower error = ', fitr.UpperError(2), fitr.LowerError(2)

            #plattxt = '#varepsilon =  %2.1f#pm%2.1f%%' % (plateau*100, fitr.Error(2)*100) # symmetric errors
            plattxt = '#varepsilon =  %2.1f^{+%2.1f}_{%2.1f} %%' % (plateau*100, fitr.UpperError(2)*100, fitr.LowerError(2)*100) # asymmetric errors

            if xpl > 0:
                plattxt += ' at %s = %3.0f GeV' % (varToLabel(var),xpl)

            #leg.AddEntry(0,"Plateau:","")
            leg.AddEntry(fturn,plattxt,"l")

            gPad.Update()

            # get stat box
            #stats = gEff.GetListOfFunctions().FindObject("stats")
            #stats.SetLineColor(gEff.GetLineColor())

            _fitrStore.append((hname,halfpoint, width, plateau))

        #_hEffStore[hEff.GetName()] = hEff
        _hEffStore[hname] = tEff

    # remove refEff
    #gPad.GetListOfPrimitives().Remove(hRef)

    # legend
    #leg = canv.BuildLegend()
    #leg.SetFillColor(0)
    leg.Draw()
    SetOwnership( leg, 0 )

    #leg.GetListOfPrimitives().Remove(hRefEff)

    ## CMS lumi
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()

    if options.logX:
        canv.SetLogx()

    _hEffStore[hRefEff.GetName] = hRefEff
    _canvStore.append(canv)

    return 1

def makeEffPlots(tree, lumi = -1, maxEntries = -1, doFit = False, varList = [], refTrig = '', testTrig = [], cuts = ''):

    # lumi dir
    if lumi == 0:
        # unscaled MC counts
        lumiDir = 'MC/LumiMC/'
    elif lumi < 0:
        # scaled MC
        lumiDir = 'MC/Lumi'+str(-lumi).replace('.','p')+'fb/'
    elif lumi > 0:
        # data
        if lumi > 10:
            lumiDir = 'Data/Lumi'+str(lumi).replace('.','p')+'pb/'
        else:
            lumiDir = 'Data/Lumi'+str(lumi).replace('.','p')+'fb/'

    # make suffix from testTrigNames
    suffix = 'test'
    for trig in testTrig:
        suffix +=  '_' + trig.replace('||','OR')

    if options.logX: suffix += "_logX"

    # final output dir:
    #lumiDir = 'plots/1d/anti/' + lumiDir
    #lumiDir = 'plots/1d/' + lumiDir
    plotdir = options.pdir
    lumiDir = plotdir + '/' + lumiDir

    print 80*'#'
    print '## Going to save plots to', lumiDir

    for var in varList:

        histList = getHistsFromTree(tree,var,refTrig, cuts, testTrig, maxEntries, lumi)
        plotEff(histList, var, doFit)
        saveCanvases(_canvStore, lumiDir,suffix, _batchMode)

        # empty stores for further use
        del _canvStore[:]
        _histStore.clear()
        _hEffStore.clear()
        del _fitrStore[:]

    return 1

if __name__ == "__main__":

    ## Option parser
    from optparse import OptionParser
    parser = OptionParser()

    parser.usage = '%prog [options]'
    parser.description="""
    Make trigger plots from friend trees
    """

    parser.add_option("-b","--batch", dest="batch",default=False, action="store_true", help="batch mode")
    parser.add_option("-l","--lumi", dest="lumi",type="float",default=0,help="Luminosity: 0 takes MC counts, >0 is data, <0 is for MC scaling")
    parser.add_option("-i","--input", dest="files",default=[], action="append", help="input file names")
    parser.add_option("-p","--plotdir", dest="pdir",default="plots/", help="plot output dir")
    parser.add_option("--noFit", dest="doFit",default=True, action="store_false", help="do not fit")
    parser.add_option("--max-entries", dest="maxEntries",type="int",default=-1,help="Maximum number of entries to process")
    parser.add_option("--logx", dest="logX",default=False, action="store_true", help="Use logX")

    '''
    ## SETTINGS
    # max entries to process
    maxEntries = -1#100000
    # do efficiency fit
    doFit = True
    # luminosity: 0 takes MC counts, >0 is data, <0 is for MC scaling
    #lumi = 0
    '''

    # Read options and args
    (options,args) = parser.parse_args()

    print 80*"#"
    print 80*"#"
    print 10*"#", "Going to scale to lumi:", options.lumi
    print 80*"#"
    print 80*"#"

    #print options.batch, options.lumi
    #print options.files

    # set options
    lumi = options.lumi
    _batchMode = options.batch
    doFit = options.doFit
    maxEntries = options.maxEntries

    fileNames = options.files
    print '#fileName is', fileNames

    if len(fileNames) == 0:
        print "# No filenames given!"
        exit(0)

    '''
    ## remove '-b' option
    _batchMode = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        fileNames = sys.argv[1:]
        print '#fileName is', fileNames
    else:
        print '#No file names given'
        exit(0)
    '''

    if len(fileNames) == 1:
        fileName = fileNames[0]

        tfile  = TFile(fileName, "READ")

        if not tfile:
            print "Couldn't open the file"
            exit(0)

        ## Get tree from file
        #for friend trees
        tree = tfile.Get('sf/t')
        #for cmg trees
        #tree = tfile.Get('tree')

    elif len(fileNames) > 1:

        tree = TChain("sf/t")
        fileName = fileNames[0] #+ "2p1"
        #tree = TChain("tree")
        for fname in fileNames:
            tree.Add(fname)

    nentries = tree.GetEntries()
    print 'Entries in tree:', nentries

    ###################
    ###################
    # DATA
    ###################
    ###################

    basecuts = 'passFilters && nLep == 1 &&'
    #basecuts = 'passFilters && nLep == 1 && Run > 275656 &&'
    #basecuts = 'passFilters && nLep == 1 && LT > 250 &&'
    #basecuts = 'METfilters && nLep == 1 && nVeto == 0 &&'
    basecuts += 'Selected == 1 &&'
#    basecuts += 'nJets30Clean >=3 &&'

    doFit = True

    if 'SingleEl' in fileName:
        ## Electrons
        #lumi = 40.03 # SingleEl RunB
        #lumi = 42 # SingleEl RunB
        #lumi = 144 # SingleEl RunD

        if 'golden205pb' in fileName:
            lumi = 205.0
        elif 'golden205p1pb' in fileName:
            lumi = 205.1
        elif '1260pb' in fileName:
            lumi = 1260
        elif '2p1' in fileName:
            lumi = 2.1
        elif '2p6fb' in fileName:
            lumi = 2.57
        elif '6p3fb' in fileName:
            lumi = 6.3
        else:
            lumi = 666

        refTrig = 'HLT_IsoEle23'
        testTrig = ['EleHT350']#,'EleHT350MET50']
        testTrig = ['EleHT350||EleHT400']

        varList = ['HT']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 25'# && MET  > 50'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        '''
        testTrig = ['EleHT350MET50']
        varList = ['MET']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 25 && HT  > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''

        '''
        refTrig = 'HLT_EleHT350'
        testTrig = ['HT800']

        varList = ['HT']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 25'# && MET  > 50'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''
        #varList = ['MET']
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 25 && HT  > 500'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        #varList = ['METNoHF']
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 25 && HT  > 500'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        '''
        #refTrig = 'HLT_IsoEle32'
        testTrig = ['Ele105','EleHT350']

        varList = ['Lep_eta']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 130 && HT > 500'
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 5'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'HLT_IsoEle23'
        testTrig = ['HT800']
        varList = ['HT']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 25'# && MET  > 50'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'HLT_EleHT350'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''

    elif 'SingleMu' in fileName:
        ## Muons

        if lumi == 0:
            if 'golden209pb' in fileName:
                lumi = 209
            elif '133pb' in fileName:
                lumi = 133
            elif '1260pb' in fileName:
                lumi = 1260
            elif '2p1' in fileName:
                lumi = 2.1
            elif '2p3' in fileName:
                lumi = 2.3
            elif '7p0' in fileName:
                lumi = 7.0
            elif '6p1' in fileName:
                lumi = 6.1
            elif 'test' in fileName:
                lumi = 666

        ## measure HT
        varList = ['HT']

        refTrig = 'HLT_IsoMu24' #Mu20
#        cuts = basecuts + 'nMu == 1 && Lep_pt > 25'
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && Lep_pt < 50'# && nJets30Clean >=6'

        #testTrig = ['MuHT350']
        testTrig = ['Mu50','MuHT400','Mu50||MuHT400']#,'Mu50||MuHT350MET50']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['PFJet450','Mu50||MuHT400','PFJet450||Mu50||MuHT400']#,'Mu50||MuHT350MET50']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        
        testTrig = ['Mu50||MuHT400','PFJet450||Mu50||MuHT400','PFJet450||Mu50||MuHT400||MET170']#,'Mu50||MuHT350MET50']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''
        testTrig = ['MuHT350MET50']
        varList = ['MET']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT  > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''

        '''
        testTrig = ['HT800']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'HLT_MuHT350'
        testTrig = ['HT800']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''
        '''
        varList = ['MET']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT  > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['METNoHF']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT  > 500'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['MET']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT  > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)


        ## Mu pt
        varList = ['Lep_pt']

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'HLT_MuHT350'
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''

    elif 'JetHT' in fileName:

        # Jet + HT triggers
        if 'dcsonly' in fileName:
            lumi = 50
        elif '2p1' in fileName:
            lumi = 2.1
        elif 'test' in fileName:
            lumi = 666
        elif '804pb' in fileName:
            lumi = 804
        elif '2056pb' in fileName:
            lumi = 2056
        elif '218pbMuonFix' in fileName:
            lumi = 218
        elif '2p6fb' in fileName:
            lumi = 2.57
        elif '7p4fb' in fileName:
            lumi = 7.4
        elif '4fb' in fileName:
            lumi = 3.99
        elif '7fb' in fileName:
            lumi = 7.62
        elif '6p3fb' in fileName:
            lumi = 6.3
        elif '5p9fb' in fileName:
            lumi = 5.9
        else:
            lumi = 147.0
            
        if 'Run274880' in fileName:
            lumi = lumi-2.577


        ### Reference trigger
        refTrig = 'HLT_HT900'
        #refTrig = 'HLT_HT350MET100'
        #refTrig = 'JetHT'#-eleCBID'
        #refTrig = 'HLT_MET170'

        ## LT

        varList = ['LT'] #LTNoHF
        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['MuHT350||MuHT400','MuHT400']#,'Mu50||MuHT350MET50']
        testTrig = ['Mu50','MuHT400','Mu50||MuHT400']#,'Mu50||MuHT350MET50']
        testTrig = ['Mu50||MuHT400','PFJet450||Mu50||MuHT400']#,'Mu50||MuHT350MET50']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        cuts = basecuts + 'nEl == 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['EleHT350||EleHT400','EleHT400']#,'Ele105||EleHT350MET50']
        testTrig = ['Ele115','EleHT400','Ele115||EleHT400']#,'Ele105||EleHT350MET50']
        testTrig = ['EleHT400','Ele115||EleHT400']#,'Ele105||EleHT350MET50']
        testTrig = ['Ele115||EleHT400','Ele115||EleHT400||PFJet450']#,'Ele105||EleHT350MET50']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)


        #### LEPTON LEG

        #refTrig = 'JetHT_EE'#HLT_HT800'#||HLT_HT350MET100'
        #refTrig = 'JetHT'#HLT_HT800'

        ## Lep PT
        '''
        varList = ['Lep_pt']

        testTrig = ['Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 50'# && abs(Lep_eta) < 1.5'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 5'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        ## Lep ETA
        varList = ['Lep_eta']

        testTrig = ['Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 120'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 60'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''

        ## more triggers

        ### LEPTON PT
        varList = ['Lep_pt']

        #testTrig = ['EleHT350']
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && HT > 500'
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && HT > 500 && MET > 50 && nJet > 2 && nBJet > 0'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

#        testTrig = ['Ele115','EleHT400','Ele115||EleHT400']#,'EleHT400']
        testTrig = ['Ele115','EleHT400']#,'Ele115||EleHT400']#,'EleHT400']
#        testTrig = ['Ele105','EleHT350','EleHT400']
        #testTrig = ['Ele105','EleHT350','IsoEle23']
        #testTrig = ['EleHT350MET50||Ele105']
        testTrig = ['Ele115||EleHT400','Ele115||EleHT400||PFJet450']#,'Ele105||EleHT350MET50']

        cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && HT > 0'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        #testTrig = ['Mu50','MuHT350||MuHT400']#,'MuHT400']
#        testTrig = ['Mu50','MuHT350','MuHT400']
        #testTrig = ['Mu50','MuHT350','IsoMu20']
        testTrig = ['Mu50','MuHT400','Mu50||MuHT400']
        testTrig = ['Mu50||MuHT400','PFJet450||Mu50||MuHT400']#,'Mu50||MuHT350MET50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 5 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        ### LEPTON ETA
        varList = ['Lep_eta']

        testTrig = ['Ele115','EleHT400','Ele115||EleHT400']#,'EleHT400']
#        testTrig = ['EleHT350','EleHT400']
#        cuts = basecuts + 'nEl == 1 && Lep_pt > 120 && HT > 500'
        testTrig = ['Ele115||EleHT400','Ele115||EleHT400||PFJet450']#,'Ele105||EleHT350MET50']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 20 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50','MuHT400','Mu50||MuHT400']
        testTrig = ['Mu50||MuHT400','PFJet450||Mu50||MuHT400']#,'Mu50||MuHT350MET50']
        #testTrig = ['MuHT350||MuHT400']#,'MuHT400']
#        testTrig = ['MuHT350','MuHT400']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 20 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        '''
        ## more triggers
        varList = ['Lep_eta']
        testTrig = ['Ele105','EleHT350']

        cuts = basecuts + 'nEl == 1 && Lep_pt > 120 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        ## muons
        testTrig = ['Mu50','MuHT350']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 55 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'HLT_HT350MET100'

        testTrig = ['EleHT350MET50','Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt'# > 5 && MET > 200 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['MuHT350MET50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 5 && MET > 200 && HT > 500'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
        '''

    elif 'HTMHT' in fileName:

        # Jet + HT triggers
        lumi = 40.0

        refTrig = 'HLT_HT350MET100'
        varList = ['Lep_pt']

        testTrig = ['EleHT350MET50','Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && MET > 200'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['MuHT350MET50','Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 5 && MET > 200'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ###################
    ###################
    # MC
    ###################
    ###################

    elif 'WJets' in fileName:

        basecuts = ''

        lumi = 0

        '''
        refTrig = ''#HLT_HT350MET120'
        varList = ['Lep_pt']

        testTrig = ['EleHT400MET50']
        #testTrig = ['EleHT400MET50','Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && HT > 500 && MET > 200'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        ## LT
        varList = ['LTNoHF']
        refTrig = 'JetHT'
        #refTrig = 'HLT_HT800'

        testTrig = ['Mu50||MuHT350MET50||Ele105||EleHT350MET50']
        cuts = basecuts + 'nLep == 1 && nVeto == 0 && Lep_pt > 25 && HT > 400'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['Mu50||MuHT350MET50']
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        cuts = basecuts + 'nEl == 1 && Lep_pt > 25 && HT > 500 && abs(Lep_eta) < 1.5'
        testTrig = ['Ele105||EleHT350MET50']
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['LT']

        cuts = basecuts + 'nMu == 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['Mu50||MuHT350MET50']
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        cuts = basecuts + 'nEl == 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['Ele105||EleHT350MET50']
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        '''

        #### LEPTON LEG
        refTrig = 'WJets'#HLT_HT800'#||HLT_HT350MET100'
        varList = ['Lep_eta']

        testTrig = ['Ele105']
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 50 && abs(Lep_eta) < 0.8'
        cuts = basecuts + 'nEl == 1 && Lep_pt > 120'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 60'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['Lep_pt']

        testTrig = ['Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 5'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 50'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'JetHT'
        testTrig = ['EleHT350MET50','Ele105']
        #testTrig = ['EleHT350MET50||Ele105']

        cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && MET > 150 && HT > 400'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)


    elif 'QCD' in fileName:

        basecuts = ''#ngenLep > 0'

        lumi = -42

        #### LEPTON LEG
        refTrig = 'QCD'#HLT_HT800'#||HLT_HT350MET100'
        varList = ['Lep_eta']

        testTrig = ['Ele105']
        #cuts = basecuts + 'nEl == 1 && Lep_pt > 50 && abs(Lep_eta) < 0.8'
        cuts = basecuts + 'nEl == 1 && Lep_pt > 120'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['EleHT400MET50']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 25  && HT > 500 && MET > 200'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 60'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        varList = ['Lep_pt']

        testTrig = ['Ele105']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 5'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['EleHT400MET50']
        cuts = basecuts + 'nEl == 1 && Lep_pt > 5  && HT > 500 && MET > 200'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        testTrig = ['Mu50']
        cuts = basecuts + 'nMu == 1 && Lep_pt > 50'
        makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

        refTrig = 'JetHT'
        testTrig = ['EleHT350MET50','Ele105']
        #testTrig = ['EleHT350MET50||Ele105']

        cuts = basecuts + 'nEl == 1 && Lep_pt > 5 && MET > 150 && HT > 400'
        #makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    else:
        print 'Nothing to draw for this file!'

    if len(fileNames) == 1:
        tfile.Close()
    #else:
    #    tree.Close()

    #outfile.Close()
