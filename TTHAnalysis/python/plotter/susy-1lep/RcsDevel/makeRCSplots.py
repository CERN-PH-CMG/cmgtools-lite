#!/Usr/bin/env python
#Script to read data cards and turn them either into a table that can be copied to Excel/OpenOffice
#1;2cor print out in latex format.

import shutil
import subprocess
import os
import sys
import glob
from multiprocessing import Pool
from ROOT import *
import math
from printTableDataCards import *
from searchBins import *
from array import array

import CMS_lumi
CMS_lumi.lumi_13TeV = "MC"
CMS_lumi.extraText = "Simulation"
CMS_lumi.writeExtraText = 1



gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(kFALSE)
gStyle.SetPaintTextFormat('4.3f')
f = TFile('RCS_kappa_plost.root',"recreate")
f2 = TFile('bkgFrac_plots.root',"recreate")

def getLegend():
    leg = TLegend(0.1500359,0.6448413,0.5294842,0.8556548);
    leg.SetBorderSize(1);
    leg.SetLineColor(1);
    leg.SetLineStyle(1);
    leg.SetLineWidth(1);
    leg.SetFillColor(0);
    leg.SetFillStyle(1001);
    return leg
######################GLOBAL VARIABLES PUT IN OPTIONS############
ignoreEmptySignal = True
def makeRCSPlot(yieldsList, dimension, source = 'EWK'):
    binNames = sorted(yieldsList[0][0].keys())
    graphs = []

    hists = []
    (dim, outname) = dimension.split('_')[0:2]
    for yields in yieldsList:
        h = TH1F("test", "test", 25, 0, 25)
        x = []
        y = []
        name = []
        i = 0
        for bin in binNames:
            (LTbin, HTbin, Bbin ) = bin.split("_")[0:3]
            (LT, HT, B) = (binsLT[LTbin][1].replace('$',''), binsHT[HTbin][1].replace('$',''), binsNB[Bbin][1].replace('$',''))
            if dim in HTbin or dim in LTbin or dim in Bbin:
                i = i+1
                print LTbin, Bbin, HTbin, yields[0][bin][source][0]

                h.SetBinContent(i,yields[0][bin][source][0])
                h.SetBinError(i,yields[0][bin][source][1])

                if 'NB' in dim:h.GetXaxis().SetBinLabel(i, '' + LTbin + ', ' + HTbin)
                if 'LT' in dim:h.GetXaxis().SetBinLabel(i, '' + Bbin + ', ' + HTbin)
                if 'HT' in dim:h.GetXaxis().SetBinLabel(i, '' + Bbin + ', ' + LTbin)
        h.GetXaxis().SetRangeUser(0,i)
        h.GetXaxis().SetLabelSize(0.09)
        h.GetXaxis().SetLabelFont(62)
        mid = ''
        if 'NB' in dim: mid = ', nB ='+ binsNB[dim][1].replace('$\geq$','>=').replace('$=$','=')
        if 'LT' in dim: mid = ', LT ' + binsLT[dim][1].replace('$\geq$','>=').replace('$','')
        if 'HT' in dim: mid = ', HT ' + binsHT[dim][0].replace('$\geq$','>=').replace('$','')
        h.SetTitle(yields[1] + mid + ', '+ source)
        hists.append(h)

    c = TCanvas("canvas", "canvas", 850 , 700)
    c.SetTickx()
    c.SetTicky()
    dummy = hists[0].Clone()
    dummy2= hists[2].Clone()
    dummy.SetTitle('')
    dummy2.SetTitle('')
    c.Divide(0,2)
    c.cd(1)
    dummy.Draw()
    c.cd(2)
    dummy2.Draw()

    leg = getLegend()
    leg2 = getLegend()
    for i,h in enumerate(hists):
        h.SetLineColor(i+1)
        h.SetMarkerStyle(20+i)
        h.SetMarkerColor(i+1)
        h.SetLineWidth(2)
        line = TF1("line","1", 0, 20)
        line.SetLineColor(kRed)
        if i < 2:
            c.cd(1)
            dummy.GetYaxis().SetRangeUser(0,0.2)
            dummy.GetYaxis().SetTitle('R_{CS}')
            dummy.GetYaxis().SetTitleSize(0.055)
            dummy.GetYaxis().SetTitleOffset(0.7)

            if 'TTdi' in source:
                dummy.GetYaxis().SetRangeUser(0.2,1.2)
            if 'TTV' in source:
                dummy.GetYaxis().SetRangeUser(0,0.5)

            h.Draw('same')
            leg.AddEntry(h)
            leg.Draw()
        else:
            h.SetLineColor(1)
            h.SetMarkerColor(1)
            c.cd(2)
            h.Draw('same')
            dummy2.GetYaxis().SetRangeUser(0,2)
            dummy2.GetYaxis().SetTitle('#kappa factor')
            dummy2.GetYaxis().SetTitleSize(0.055)
            dummy2.GetYaxis().SetTitleOffset(0.7)
#            c.GetPad(2).BuildLegend()
            leg2.AddEntry(h)
            line.Draw("same")
            leg2.Draw()
 #   c.GetPad(1).BuildLegend()

    c.SetName(dim + "_"+outname+'_'+source)
    CMS_lumi.cmsTextSize = 0.65
    CMS_lumi.relPosX = 0.08
    CMS_lumi.CMS_lumi(c.GetPad(1), 4, 0)
    f.cd()

    c.Write()
    c.SaveAs('RCSplots/'+dim + "_"+outname+'_'+source+'.pdf')


    return

def makeSBMBtable(yieldsList, dimension, source = 'EWK'):

    binNames = sorted(yieldsList[0][0].keys())
    graphs = []

    hists = []
    (dim, outname) = dimension.split('_')[0:2]
    for bin in binNames:
        (LTbin, HTbin, Bbin ) = bin.split("_")[0:3]
        if dim in HTbin or dim in LTbin or dim in Bbin:
#            singleSourceNames = ['TTdiLep','TTsemiLep','Wjets']
            singleSourceNames = ['EWK','TT','TTdiLep','TTsemiLep','WJets','TTV','SingleT','DY']
            print bin
            for yields in yieldsList:
                total = yields[0][bin]['EWK'][0]
                for source in singleSourceNames:
                    print source, yields[0][bin][source][0], yields[0][bin][source][0]/total
            print

    return

colorDict = {'TT': kBlue-4,'TTdiLep':kBlue-4,'TTsemiLep':kBlue-2,'WJets':kGreen-2,
'QCD':kCyan-6,'SingleT':kViolet+5,'DY':kRed-6,'TTV':kOrange-3}
def makeFracPlots(yieldsList, dimension, whichsource = 'EWK'):

    binNames = sorted(yieldsList[0][0].keys())
    graphs = []

    hists = []
    xbins = 20
    (dim, outname) = dimension.split('_')[0:2]
    if whichsource == 'EWK':
        singleSourceNames = ['TTdiLep','TTsemiLep','WJets','TTV','SingleT','DY']
    elif whichsource == 'TT':
        singleSourceNames = ['TTdiLep','TTsemiLep']
    leg = getLegend()


    for yields in yieldsList:

        hstack = THStack("hs","")
        for j,source in enumerate(singleSourceNames):
            h = TH1F("test", "test", 25, 0, 25)
            i=0
            for k,bin in enumerate(binNames):
                (LTbin, HTbin, Bbin ) = bin.split("_")[0:3]
                if dim in HTbin or dim in LTbin or dim in Bbin:
                    i = i + 1
                    if whichsource == 'EWK':
                        total = yields[0][bin]['EWK'][0]
                    elif whichsource == 'TT':
                        total = yields[0][bin]['TT'][0]

                    print source, yields[0][bin][source][0], yields[0][bin][source][0]/total
                    h.SetBinContent(i, yields[0][bin][source][0]/total)
                    h.SetTitle(source)
                    if k ==0 : leg.AddEntry(h)
                    if 'NB' in dim:h.GetXaxis().SetBinLabel(i, '' + LTbin + ', ' + HTbin)
                    if 'LT' in dim:h.GetXaxis().SetBinLabel(i, '' + Bbin + ', ' + HTbin)
                    if 'HT' in dim:h.GetXaxis().SetBinLabel(i, '' + Bbin + ', ' + LTbin)
            print 'bins', i
            xbins = i

            h.SetFillColor(colorDict[source])
            h.SetLineColor(kBlack)
            mid = ''
            if 'NB' in dim: mid = ', nB ='+ binsNB[dim][1].replace('$\geq$','>=').replace('$=$','=')
            if 'LT' in dim: mid = ', LT ' + binsLT[dim][1].replace('$\geq$','>=').replace('$','')
            if 'HT' in dim: mid = ', HT ' + binsHT[dim][0].replace('$\geq$','>=').replace('$','')

            hstack.SetTitle(yields[1] + mid + ', '+ ' bkg fractions')
            h.SetMarkerSize(2)
            h.SetMarkerColor(kWhite)
            hstack.Add(h)

        hists.append(hstack)

    c = TCanvas("canvas", "canvas", 850 , 700)
    c.SetTickx()
    c.SetTicky()
    print len(hists)
    for i,h in enumerate(hists):
        name =  h.GetTitle()
        h.SetTitle('')
        h.Draw('')
        h.GetXaxis().SetRangeUser(0,xbins)
        h.GetYaxis().SetRangeUser(0,1.2)
        h.GetXaxis().SetLabelFont(62)
        h.GetXaxis().SetLabelSize(0.05)
        h.SetMinimum(0)
        h.SetMaximum(1)
        gStyle.SetPaintTextFormat('4.3f')
        if whichsource == 'EWK':
            h.Draw('')
        elif whichsource == 'TT':
            h.Draw('TEXT70hist')

        h.GetYaxis().SetTitle(name)
        if whichsource == 'EWK':
            c.BuildLegend(0.8546099,0.2291667,0.9976359,0.6994048, '#splitline{'+yieldsList[i][1] + '}{' + mid.replace(', ','') +'}')
        elif whichsource == 'TT':
            c.BuildLegend(0.8537736,0.4637037,0.9964623,0.7007407, '#splitline{'+yieldsList[i][1] + '}{' + mid.replace(', ','') +'}')
        c.SetName(dim + "_"+outname+'_'+yieldsList[i][1].replace(' ','').replace(',',''))

        CMS_lumi.relPosX = 0.13
        CMS_lumi.cmsTextSize = 0.5
        CMS_lumi.CMS_lumi(c, 4, 0)
        f2.cd()
        c.Write()
        if whichsource == 'EWK':
            c.SaveAs('FracPlots/'+dim + "_"+outname+'_'+yieldsList[i][1].replace(' ','').replace(',','')+'.pdf')
        elif whichsource == 'TT':
            c.SaveAs('FracPlots_TT/'+dim + "_"+outname+'_'+yieldsList[i][1].replace(' ','').replace(',','')+'_ttbar.pdf')
    return



# MAIN
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cardDirectory = sys.argv[1]
    else:
        print "Will stop, give input Dir"
        quit()
    #gROOT.ProcessLine(".x ../../tdrstyle.cc")
    cardDirectory = os.path.abspath(cardDirectory)
    cardDirName = os.path.basename(cardDirectory)

    print 'Using cards from', cardDirName
    inDir = cardDirectory
    cardFnames = glob.glob(inDir+'/merged/*68*.root')
    cardFnames9 = glob.glob(inDir+'/merged/*9i*.root')
    print cardFnames

    for i,cards in enumerate((cardFnames, cardFnames9)):
        dictRcs_MB = getYieldDict(cards,"Rcs_MB","","lep")
        dictRcs_SB = getYieldDict(cards,"Rcs_SB","","lep")
        dictKappa = getYieldDict(cards,"Kappa","","lep")

        dictSR_MB = getYieldDict(cards,"SR_MB","","lep")
        dictSR_SB = getYieldDict(cards,"SR_SB","","lep")
        dictCR_MB = getYieldDict(cards,"CR_MB","","lep")
        dictCR_SB = getYieldDict(cards,"CR_SB","","lep")


        if i==0: jets = '6-8'
        if i==1: jets = '9-i'
        sourceList = ['EWK','TT','TTdiLep','TTsemiLep','WJets','TTV','SingleT']#,'data']
        for source in sourceList:
#            makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'NB0_'+jets+'RCS', source)
            makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'NB1_'+jets+'RCS', source)
            makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'NB2_'+jets+'RCS', source)
            makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'NB3i_'+jets+'RCS', source)
          #  makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'LT1_'+jets+'RCS', source)
          #  makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'LT2_'+jets+'RCS', source)
          #  makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'LT3_'+jets+'RCS', source)
          #  makeRCSPlot(((dictRcs_MB, jets.replace('-',',')+' jets'), (dictRcs_SB , ' 4,5 jets'), (dictKappa, '#kappa')),'LT4i_'+jets+'RCS', source)

        if 1==2:
            makeFracPlot(((dictSR_MB, jets.replace('-',',')+'jets'), (dictSR_SB , ' 4,5 jets'),),'NB0_'+jets+'Frac')
        if 1==1:
            print  ' '
            whichsource = 'TT'
            makeFracPlots(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB1_'+jets+'Frac',whichsource)
            makeFracPlots(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB2_'+jets+'Frac',whichsource)
            makeFracPlots(((dictCR_MB, 'CR '+ jets.replace('-',',' )+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB3i_'+jets+'Frac',whichsource)


            whichsource = 'EWK'
            makeFracPlots(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB1_'+jets+'Frac',whichsource)
            makeFracPlots(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB2_'+jets+'Frac',whichsource)
            makeFracPlots(((dictCR_MB, 'CR '+ jets.replace('-',',' )+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB3i_'+jets+'Frac',whichsource)

        if 1==2 and i==0:
            makeSBMBtable(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB1_'+jets+'Frac')
            makeSBMBtable(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB2_'+jets+'Frac')
            makeSBMBtable(((dictCR_MB, 'CR '+ jets.replace('-',',')+' jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',',')+' jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB3i_'+jets+'Frac')

#        makeSBMBtable(((dictCR_MB, 'CR '+ jets.replace('-',', ')+'jets'), (dictCR_SB , ' CR 4,5 jets'), (dictSR_MB, 'SR '+ jets.replace('-',', ')+'jets'), (dictSR_SB , ' SR 4,5 jets'), ),'NB1_'+jets+'Frac')
        makeSBMBtable(((dictCR_MB, 'CR '+ jets.replace('-',',')+'jets'), (dictCR_SB , ' CR 4,5 jets')),'NB1_'+jets+'Frac')
