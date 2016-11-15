#!/usr/bin/python

import sys

from array import array
from ROOT import *

from triggTools import *

_canvStore = []
_histStore = {}
_hEffStore = {}

_fitrStore = []

_colorList = [2,8,4,9,7,3,6] + range(10,50)

def get2DHistsFromTree(tree, tvar = ('MET','HT'), refTrig = '', cuts = '', testTrig = '', maxEntries = -1, lumi = -1):

    # decipher var tuple
    (var1,var2) = tvar
    var = var1+'vs'+var2

    # maximum number of entries to process
    if maxEntries == -1:
        maxEntries = tree.GetEntries()

    # histogram name prefix
    histPrefix = 'h' + var + '_'

    # plot option
    plotOpt = 'colz'

    # histogram list
    histList = []

    # prepend HLT name
    testTrig = ['HLT_'+name.replace('HLT_','') for name in testTrig]

    # names
    if refTrig != '':
        refName = refTrig.replace('HLT_','')
    else:
        refName = 'PreSel'

    ## name replacement
    refName = renameTrig(refName)

    rname = histPrefix + refName

    cname = var + '_' + refName
    ctitle = 'Plots for reference:' + refName

    if cuts != '':
        ctitle += ' cut: ' + cuts

    if refTrig != '':
        cuts += ' && HLT_' + refTrig.replace('HLT_','')
        htitle = refTrig.replace('HLT_','')#'Ref: ' + refTrig
    else:
        htitle = 'Preselection'

    print 'Going to draw', ctitle

    # make canvas
    canv = TCanvas(cname,ctitle,800,800)

    # make hist
    nbins = 50

    if var1 == 'MET' and var2 == 'HT':
        hRef = TH2F(rname,htitle,nbins,0,1500,nbins,0,600)
        hRef = TH2F(rname,htitle,len(ht_bins_2d)-1,array('f',ht_bins_2d),len(met_bins_2d)-1,array('f',met_bins_2d))
    elif var1 == 'HT' and var2 == 'MET':
        hRef = TH2F(rname,htitle,len(met_bins_2d)-1,array('f',met_bins_2d),len(ht_bins_2d)-1,array('f',ht_bins_2d))
    elif 'pt' in var2 and var1 == 'MET':
        hRef = TH2F(rname,htitle,len(pt_bins_2d)-1,array('f',pt_bins_2d),len(met_bins_2d)-1,array('f',met_bins_2d))
    elif 'pt' in var2 and var1 == 'HT':
        hRef = TH2F(rname,htitle,len(pt_bins_2d)-1,array('f',pt_bins_2d),len(ht_bins_2d)-1,array('f',ht_bins_2d))
    elif 'pt' in var2 and 'eta' in var1:
        hRef = TH2F(rname,htitle,len(pt_bins_2d)-1,array('f',pt_bins_2d),len(eta_bins_2d)-1,array('f',eta_bins_2d))
    else:
        hRef = TH2F(rname,htitle,nbins,0,1500,nbins,0,600)

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
    varstr = var1 + ':' + var2

    if not doLumi:
        tree.Draw(varstr + '>>' + hRef.GetName(),cuts,plotOpt, maxEntries)
        print 'Drawing', hRef.GetName(), 'with cuts', cuts
    else:
        hRef.Sumw2()

        wt = 600*lumi/float(maxEntries)
        print 'Weight for %2.2f lumi and maxEntries %10.f is %f' %(lumi, maxEntries,wt)
        weight = str(wt) + ' * Xsec'
        if cuts != '': wcuts = weight + '*(' + cuts + ')'
        else: wcuts = weight
        print 'Drawing', hRef.GetName(), 'with cuts', wcuts

        tree.Draw(varstr + '>>' + hRef.GetName(),wcuts,plotOpt, maxEntries)
        hRef.SetMaximum(hRef.GetMaximum() * 2)

    print '#Found', hRef.Integral(), 'events'

    hRef.GetZaxis().SetRangeUser(0,1)
    hRef.SetLineColor(1)
    # axis set up
    hRef.SetStats(0)
    hRef.GetXaxis().SetTitle(varToLabel(var2))
    hRef.GetYaxis().SetTitle(varToLabel(var1))
    hRef.GetYaxis().SetTitleOffset(1.2)
    #canv.SetLogy()

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
                trigName += 'OR' + name
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

        print 'Drawing', hTest.GetName(), 'with cuts', tcuts

        # lumi scale
        if not doLumi:
            tree.Draw(varstr + '>>' + hTest.GetName(),tcuts,plotOpt+'same', maxEntries)
        else:
            #hTest.Sumw2()
            if tcuts != '': wtcuts = weight + '*(' + tcuts + ')'
            else: wtcuts = weight
            tree.Draw(varstr + '>>' + hTest.GetName(),wtcuts,plotOpt+'same', maxEntries)

        print '#Found', hTest.Integral(), 'events'

        gPad.Update()

        #hTest.Divide(hRef)
        #hTest.Draw("colz")

        gPad.Update()

        _histStore[hTest.GetName()] = hTest
        histList.append(hTest)

    # legend
    leg = canv.BuildLegend()
    leg.SetFillColor(0)
    #leg.SetHeader(ctitle.replace('&&','\n'));

    #CMS lumi
    CMS_lumi.CMS_lumi(canv, 4, iPos)

    gPad.Update()

    #_canvStore.append(canv)

    return histList

def plot2DEff(histList,  tvar = ('MET','HT')):

    ## histList: [hReference, hTest1, hTest2,...]

    # decipher var tuple
    (var1,var2) = tvar
    var = var1+'vs'+var2

    # hist prefix
    histPrefix = 'h' + var + '_'

    # reference hist should be first
    hRef = histList[0]

    # loop over test
    #for ind,hname in enumerate(nameList):
    for ind,hist in enumerate(histList[1:]):

        hname = hist.GetName()
        cname = hname.replace('h'+var,var) + '_Eff_Ref'+ hRef.GetName().replace('h'+var,'')

        ctitle = 'Eff for reference:' + hRef.GetName()

        # make canvas
        canv = TCanvas(cname,ctitle,800,800)
        # style

        # legend
        leg = getLegend('2d')
        leg.SetHeader('Reference: ' + hRef.GetName().replace('h'+var+'_',''))

        htitle = hname.replace(histPrefix,'')
        hname = hname.replace('h','hEff')

        print 'Drawing', hname, 'from', hRef.GetName()

        ## Divide
        hEff = hist.Clone(hname)
        hEff.Divide(hRef)
        hEff.GetZaxis().SetRangeUser(0,1)

        plotOpt = 'colz'
        hEff.Draw(plotOpt)

        leg.AddEntry(hEff,hEff.GetTitle(),'f')
        leg.Draw()
        SetOwnership( leg, 0 )

        # LT LINE
        if 'MET' in var and 'Lep' in var:
            cutline = TLine(0,250,250,0)
            cutline.SetLineWidth(5)
            cutline.SetLineStyle(4)
            cutline.Draw()
            SetOwnership(cutline,0)

        ## CMS lumi
        CMS_lumi.CMS_lumi(canv, 4, iPos)

        gPad.Update()

        _hEffStore[hname] = hEff
        _canvStore.append(canv)

    return 1

def make2DEffPlots(tree, lumi = -1, maxEntries = -1, varList = [], refTrig = '', testTrig = [], cuts = ''):

    # lumi dir
    if lumi == 0:
        # unscaled MC counts
        lumiDir = 'MC/LumiMC/'
    elif lumi < 0:
        # scaled MC
        lumiDir = 'MC/Lumi'+str(-lumi).replace('.','p')+'fb/'
    elif lumi > 0:
        # data
        lumiDir = 'Data/Lumi'+str(lumi).replace('.','p')+'fb/'

    # make suffix from testTrigNames
    #suffix = 'test'
    #for trig in testTrig:
    #    suffix +=  '_' + trig.replace('||','OR')
    suffix = ''

    # final output dir:
    lumiDir = 'plots/2d/' + lumiDir

    print 'Going to save plots to', lumiDir

    for var in varList:

        histList = get2DHistsFromTree(tree,var,refTrig, cuts, testTrig, maxEntries, lumi)
        plot2DEff(histList, var)
        saveCanvases(_canvStore,lumiDir,suffix,_batchMode)

    return 1

if __name__ == "__main__":

    ## remove '-b' option
    _batchMode = False

    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        fileName = sys.argv[1]
        print '#fileName is', fileName
    else:
        print '#No file names given'
        exit(0)

    tfile  = TFile(fileName, "READ")

    '''
    if len(sys.argv) > 2:
        outName = sys.argv[2]
    else:
        print '#No out file name is given'
        outName = (os.path.basename(fileName)).replace('.root','_plots.root')
        print '#> Out file name is', outName

    outfile = TFile(outName, "RECREATE")
    '''

    if not tfile:
        print "Couldn't open the file"
        exit(0)

    ## Get tree from file
    # for friend trees
    tree = tfile.Get('sf/t')
    # for cmg trees
    #tree = tfile.Get('tree')

    nentries = tree.GetEntries()
    print 'Entries in tree:', nentries

    ## SETTINGS
    # max entries to process
    maxEntries = -1#100000
    # do efficiency fit
    doFit = True#False
    # luminosity scaling, -1 takes MC counts
    lumi = 0

    '''
    # muon
    cuts = 'nTightMu >= 1 && LepGood1_pt > 25'
    refTrig = 'SingleMu'
    testTrig = ['HTMET','MuHT400MET70']
    var = ('MET','HT')
    varList = [var]
    #make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

    # electron
    cuts = 'nEl >= 1 && Lep_pt > 15'
    refTrig = 'SingleEl'
    #testTrig = ['HTMET','EleHT350MET70']
    testTrig = ['EleHT350MET70']
    var = ('MET','HT')
    varList = [var]
    #make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

    #############
    # LT: Muon
    #############

    varList = ['LT']
    cuts = 'nTightMu == 1 && LepGood1_pt > 25 && HT > 500'
    refTrig = ''
    #testTrig = ['Mu50NoIso','MuHT400MET70','Mu50NoIso||MuHT400MET70']
    testTrig = ['Mu50NoIso||MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    #############
    # LT: Electron
    #############

    varList = ['LT']
    cuts = 'nTightEl == 1 && LepGood1_pt > 25 && HT > 500'
    refTrig = ''
    #testTrig = ['ElNoIso','EleHT400MET70','ElNoIso||EleHT400MET70']
    testTrig = ['ElNoIso||EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    #############
    # Lepton legs
    #############

    ## muons
    varList = ['LepGood1_pt']
    cuts = 'nTightMu == 1 && LepGood1_pt > 5 && HT > 500 && MET > 200'
    refTrig = ''
    testTrig = ['Mu50NoIso','MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['LepGood1_pt']
    cuts = 'nTightMu == 1 && LepGood1_pt > 5 && HT > 500 && MET > 200'
    refTrig = 'HTMET'
    testTrig = ['Mu50NoIso','MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ## electrons
    varList = ['LepGood1_pt']
    cuts = 'nTightEl == 1 && LepGood1_pt > 5 && HT > 500 && MET > 200'
    refTrig = ''
    testTrig = ['ElNoIso','EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['LepGood1_pt']
    cuts = 'nTightEl == 1 && LepGood1_pt > 5 && HT > 500 && MET > 200'
    refTrig = 'HTMET'
    testTrig = ['ElNoIso','EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ###############
    # Hadronic legs: Muon
    ###############

    varList = ['HT']
    cuts = 'nTightMu == 1 && LepGood1_pt > 55 && MET > 200'
    refTrig = ''
    testTrig = ['SingleMu','Mu50NoIso', 'MuHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, False, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nTightMu == 1 && LepGood1_pt > 25 && MET > 200'
    refTrig = ''
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nTightMu == 1 && LepGood1_pt > 25 && HT  > 500'
    refTrig = ''
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nTightMu == 1 && LepGood1_pt > 25 && MET > 200'
    refTrig = 'SingleMu'
    #testTrig = ['SingleMu','Mu50NoIso','HLT_MuHT400MET70']
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nTightMu == 1 && LepGood1_pt > 25 && HT  > 500'
    refTrig = 'SingleMu'
    testTrig = ['MuHT400MET70']#,'MuHT600']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    ###############
    # Hadronic legs: Electron
    ###############

    varList = ['HT']
    cuts = 'nTightEl == 1 && LepGood1_pt > 120 && MET > 200'
    refTrig = ''
    testTrig = ['SingleEl','ElNoIso', 'EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, False, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nTightEl == 1 && LepGood1_pt > 25 && MET > 200'
    refTrig = ''
    testTrig = ['EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nTightEl == 1 && LepGood1_pt > 25 && HT  > 500'
    refTrig = ''
    testTrig = ['EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['HT']
    cuts = 'nTightEl == 1 && LepGood1_pt > 25 && MET > 200'
    refTrig = 'SingleEl'
    testTrig = ['EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)

    varList = ['MET']
    cuts = 'nTightEl == 1 && LepGood1_pt > 25 && HT  > 500'
    refTrig = 'SingleEl'
    testTrig = ['EleHT400MET70']
    makeEffPlots(tree, lumi, maxEntries, doFit, varList, refTrig, testTrig, cuts)
    '''

    ###################
    ###################
    # DATA
    ###################
    ###################

    # define base cuts like filters
    #basecut = ''
    basecuts = 'passFilters && nLep == 1 &&'
    basecuts += 'Selected == 1 &&'

    if 'JetHT' in fileName:

        #lumi = 42.0
        if '147pb' in fileName:
            lumi = 147.0
        elif '2p3' in fileName:
            lumi = 2.3

        ## LepPt vs MET
        var = ('MET','Lep_pt')
        varList = [var]
        #refTrig = ''#HT800'
        #refTrig = 'HLT_HT800'
        refTrig = 'HT800'

        ## Muons
        cuts = basecuts + 'nMu >= 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['Mu50||MuHT350MET50','MuHT350']#,'Mu50','MuHT350MET70']
        make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

        ## Electrons
        cuts = basecuts + 'nEl >= 1 && Lep_pt > 25 && HT > 500'
        testTrig = ['Ele105||EleHT350MET50','EleHT350']#,'Ele105','EleHT350MET70']
        make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

        ## LepPt vs LepEta
        #var = ('Lep_eta','Lep_pt')
        #varList = [var]
        refTrig = 'HT350MET100'#HT800'

        ## Electrons
        cuts = basecuts + 'nEl >= 1 && Lep_pt > 25'# && HT > 400'
        #testTrig = ['Ele105']
        testTrig = ['EleHT350']
        #make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

    elif 'HTMHT' in fileName:

        lumi = 40.0

        ## LepPt vs MET
        var = ('MET','Lep_pt')
        varList = [var]
        refTrig = 'HT350MET100'

        ## Muons
        cuts = 'Selected == 1 && nMu >= 1 && Lep_pt > 5 && HT > 400'
        testTrig = ['Mu50||MuHT350MET70','Mu50','MuHT350MET70']
        make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

        ## Electrons
        cuts = 'Selected == 1 && nEl >= 1 && Lep_pt > 5 && HT > 400'
        testTrig = ['Ele105||EleHT350MET70','Ele105','EleHT350MET70']
        make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

    ###################
    ###################
    # MC
    ###################
    ###################

    elif 'TTJets' in fileName:

        lumi = -40.0

        ## LepPt vs MET
        var = ('MET','Lep_pt')
        varList = [var]
        refTrig = ''#HT800'

        ## Muons
        cuts = 'Selected == 1 && nMu >= 1 && Lep_pt > 5 && HT > 400'
        testTrig = ['Mu50NoIso||MuHT400MET70','Mu50NoIso','MuHT400MET70']
        make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

        ## Electrons
        cuts = 'Selected == 1 && nEl >= 1 && Lep_pt > 5 && HT > 400'
        testTrig = ['ElNoIso||EleHT400MET70','ElNoIso','EleHT400MET70']
        make2DEffPlots(tree, lumi, maxEntries, varList, refTrig, testTrig, cuts)

    else:
        print 'Nothing to draw for this file!'

    tfile.Close()
    #outfile.Close()
