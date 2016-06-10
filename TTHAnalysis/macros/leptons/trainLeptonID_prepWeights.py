#!/usr/bin/env python

# this script will calculate weights the distribution of variableToReweight in signal leptons to the one in background leptons, saving the output as a friend tree
# usage: python trainLeptonID_prepWeights.py tree_sig1.root tree_sig2.root tree_bkg1.root tree_bkg2.root sigCut bkgCut variableToReweight bins outfile.root rel_weight_sig2_sig1 rel_weight_bkg2_bkg1
# like:  python trainLeptonID_prepWeights.py tree_sig1.root tree_sig2.root tree_bkg1.root tree_bkg2.root 'LepGood_mcMatchId!=0' 'LepGood_mcMatchId==0' LepGood_pt '50,0,200' my_pt_weights.root 0.93 0.98

import ROOT
import sys
from array import array

files = []
def prepTree(fname,cut='1'):
    f_ = ROOT.TFile(fname,"read")
    files.append(f_)
    t_ = f_.tree
    return t_


cut_hardcoded = "LepGood_pt<30 && LepGood_pt>3.5 && (abs(LepGood_pdgId)==11 || LepGood_pt>5) && LepGood_RelIsoFix04*LepGood_pt<10 && LepGood_sip3d<8 && (abs(LepGood_pdgId)!=11 || (abs(LepGood_etaSc)<0.8 && LepGood_mvaIdSpring15 > -0.70) || (abs(LepGood_etaSc)>=0.8 && abs(LepGood_etaSc)<1.479 && LepGood_mvaIdSpring15 > -0.83) || (abs(LepGood_etaSc)>=1.479 && LepGood_mvaIdSpring15 > -0.92)) && (LepGood_mcMatchId==0 || LepGood_mcMatchTau!=1)";
cuts_hardcoded = '((%s) && (%s))'%(cut_hardcoded,'LepGood_mcMatchId!=0')
cutb_hardcoded = '((%s) && (%s))'%(cut_hardcoded,'LepGood_mcMatchId==0')


var,bins = sys.argv[7:9]
tsig = prepTree(sys.argv[1])
tsig2 = prepTree(sys.argv[2]) if sys.argv[2]!='0' else None
tbkg = prepTree(sys.argv[3])
tbkg2 = prepTree(sys.argv[4]) if sys.argv[4]!='0' else None
cuts = "(xsec/1.e5)*(%s)"%(sys.argv[5].replace('hardcoded',cuts_hardcoded),)
cutb = "(xsec/1.e5)*(%s)"%(sys.argv[6].replace('hardcoded',cutb_hardcoded),)
outfname = sys.argv[9]

print cuts
print cutb

tsig.Draw("%s>>htemp(%s)"%(var,bins),cuts)
hsig = ROOT.gDirectory.Get('htemp').Clone('hsig')
if tsig2:
    print 'Using a second sig histo, weighted by %s'%sys.argv[10]
    tsig2.Draw("%s>>htemp(%s)"%(var,bins),"(%s)*(%s)"%(cuts,sys.argv[10]))
    hsig2 = ROOT.gDirectory.Get('htemp').Clone('hsig2')
    hsig.Add(hsig2)

tbkg.Draw("%s>>htemp(%s)"%(var,bins),cutb)
hbkg = ROOT.gDirectory.Get('htemp').Clone('hbkg')
if tbkg2:
    print 'Using a second bkg histo, weighted by %s'%sys.argv[11]
    tbkg2.Draw("%s>>htemp(%s)"%(var,bins),cutb,sys.argv[11])
    hbkg2 = ROOT.gDirectory.Get('htemp').Clone('hbkg2')
    hbkg.Add(hbkg2)

print 'normalization (with under/overflow): signal %f, background %f'%(hsig.Integral(0,hsig.GetNbinsX()+1),hbkg.Integral(0,hbkg.GetNbinsX()+1))

hsig.Scale(1./hsig.Integral(0,hsig.GetNbinsX()+1))
hbkg.Scale(1./hbkg.Integral(0,hbkg.GetNbinsX()+1))
hw = hbkg.Clone('h_weights')
hw.Divide(hsig)

max_w = 10.
for i in xrange(hw.GetNbinsX()):
    if hw.GetBinContent(i+1)>max_w: hw.SetBinContent(i+1,max_w)

newf = ROOT.TFile(outfname,"recreate")
newf.cd()
newt = ROOT.TTree('wtree','wtree')
n = array('i', [0])
w = array('f', 100*[0.])
newt.Branch('nLepGood', n, 'nLepGood/I')
newt.Branch('addW',w,'addW[nLepGood]/F')

for ev in tsig:
    n[0] = ev.nLepGood
    _v = getattr(ev,var)
    for i in xrange(100):
        w[i] = hw.GetBinContent(hw.FindBin(_v[i])) if i<n[0] else 0.
    newt.Fill()
print 'Filled %d entries'%newt.GetEntries()
hw.Write()
newf.Write()
newf.Close()


if tsig2:
    newf = ROOT.TFile("%s_2"%outfname,"recreate")
    newf.cd()
    newt = ROOT.TTree('wtree','wtree')
    n = array('i', [0])
    w = array('f', 100*[0.])
    newt.Branch('nLepGood', n, 'nLepGood/I')
    newt.Branch('addW',w,'addW[nLepGood]/F')

    for ev in tsig2:
        n[0] = ev.nLepGood
        _v = getattr(ev,var)
        for i in xrange(100):
            w[i] = hw.GetBinContent(hw.FindBin(_v[i])) if i<n[0] else 0.
        newt.Fill()
    print 'Filled %d entries'%newt.GetEntries()
    hw.Write()
    newf.Write()
    newf.Close()
