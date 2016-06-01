#!/usr/bin/env python

# this script will calculate weights the distribution of variableToReweight in signal leptons to the one in background leptons, saving the output as a friend tree
# usage: python trainLeptonID_prepWeights.py tree_sig.root tree_bkg.root sigCut bkgCut variableToReweight bins outfile.root
# like:  python trainLeptonID_prepWeights.py tree_sig.root tree_bkg.root 'LepGood_mcMatchId!=0' 'LepGood_mcMatchId==0' LepGood_pt '50,0,200' my_pt_weights.root

import ROOT
import sys
from array import array

files = []
def prepTree(fname,cut='1'):
    f_ = ROOT.TFile(fname,"read")
    files.append(f_)
    t_ = f_.tree
    return t_

var,bins = sys.argv[5:7]
tsig = prepTree(sys.argv[1])
tbkg = prepTree(sys.argv[2])

tsig.Draw("%s>>htemp(%s)"%(var,bins),sys.argv[3])
hsig = ROOT.gDirectory.Get('htemp').Clone('hsig')

tbkg.Draw("%s>>htemp(%s)"%(var,bins),sys.argv[4])
hbkg = ROOT.gDirectory.Get('htemp').Clone('hbkg')

print 'normalization (with under/overflow): signal %f, background %f'%(hsig.Integral(0,hsig.GetNbinsX()+1),hbkg.Integral(0,hbkg.GetNbinsX()+1))

hsig.Scale(1./hsig.Integral(0,hsig.GetNbinsX()+1))
hbkg.Scale(1./hbkg.Integral(0,hbkg.GetNbinsX()+1))
hw = hbkg.Clone('h_weights')
hw.Divide(hsig)

max_w = 10.
for i in xrange(hw.GetNbinsX()):
    if hw.GetBinContent(i+1)>max_w: hw.SetBinContent(i+1,max_w)

newf = ROOT.TFile(sys.argv[7],"recreate")
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
