#!/usr/bin/env python
import sys, pickle
import ROOT

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] OUTFILE")
parser.add_option("-T","--training", dest="training",  type="string", default="MultiClassICHEP16")
parser.add_option("-P","--treepath", dest="treepath",  type="string", default=None)
parser.add_option("-F","--friend", dest="friends",  type="string", default=[], action="append")
parser.add_option("-c","--cut", dest="addcuts", type="string", default=[], action="append")
(options, args) = parser.parse_args()

if len(args)<1 or not options.treepath: raise RuntimeError
fOutName = args[0]

_allfiles=[]
dsets=[]
def load_dataset(name,trainclass,addw=1,path=options.treepath):
    f_ttw = ROOT.TFile('/'.join([path,name,'treeProducerSusyMultilepton/tree.root']))
    _allfiles.append(f_ttw)
    t_ttw = f_ttw.tree
    for friend in options.friends: t_ttw.AddFriend('sf/t','/'.join([path,friend,'evVarFriend_%s.root'%name]))
    pckfile = '/'.join([path,name,"skimAnalyzerCount/SkimReport.pck"])
    pckobj  = pickle.load(open(pckfile,'r'))
    counters = dict(pckobj)
    if not ('Sum Weights' in counters): raise RuntimeError
    w = 1.0*addw/(counters['Sum Weights'])
    dsets.append((trainclass,name,t_ttw,w))
    print 'Added %s dataset, category %s, with weight %f/%f*xsec*genWeight'%(name,trainclass,addw,counters['Sum Weights'])

load_dataset('TTHnobb_pow','ttH')
load_dataset('TTW_LO','ttV')
load_dataset('TTZ_LO','ttV')
if '_3l' in options.training:
    load_dataset('TTJets_DiLepton','tt',addw=0.1)
    load_dataset('TTJets_DiLepton_ext_skim3l','tt',addw=0.9)
else:
    load_dataset('TTJets_SingleLeptonFromT','tt',addw=0.1)
    load_dataset('TTJets_SingleLeptonFromTbar','tt',addw=0.1)
    load_dataset('TTJets_SingleLeptonFromT_ext','tt',addw=0.9)
    load_dataset('TTJets_SingleLeptonFromTbar_ext','tt',addw=0.9)

fOut = ROOT.TFile(fOutName,"recreate")
fOut.cd()
factory = ROOT.TMVA.Factory(options.training, fOut, "!V:!Color:Transformations=I:AnalysisType=Multiclass")
allcuts = ROOT.TCut('1')
for cut in options.addcuts: allcuts += cut

if 'MultiClassICHEP16' in options.training:

    allcuts += "nLepFO_Recl>=2 && LepGood_conePt[iF_Recl[0]]>20 && (abs(LepGood_pdgId[iF_Recl[0]])!=11 || LepGood_conePt[iF_Recl[0]]>25) && LepGood_conePt[iF_Recl[1]]>10 && (abs(LepGood_pdgId[iF_Recl[1]])!=11 || LepGood_conePt[iF_Recl[1]]>15)"
    allcuts += "abs(mZ1_Recl-91.2) > 10 && (met_pt*0.00397 + mhtJet25_Recl*0.00265 > 0.2) && (nBJetLoose25_Recl >= 2 || nBJetMedium25_Recl >= 1) && minMllAFAS_Recl>12"
    if '_3l' in options.training:
        allcuts += "nLepFO_Recl>=3 && LepGood_conePt[iF_Recl[2]]>10 && nJet25_Recl>=2"
#        allcuts += "LepGood_isTight_Recl[iF_Recl[0]] && LepGood_isTight_Recl[iF_Recl[1]] && LepGood_isTight_Recl[iF_Recl[2]]"
    else:
        allcuts += "nLepTight_Recl<=2 && nJet25_Recl>=4 && (LepGood_charge[iF_Recl[0]]*LepGood_charge[iF_Recl[1]] > 0)"
#        allcuts += "LepGood_isTight_Recl[iF_Recl[0]] && LepGood_isTight_Recl[iF_Recl[1]]"

    factory.AddSpectator("iF0 := iF_Recl[0]","F") # do not remove this!
    factory.AddSpectator("iF1 := iF_Recl[1]","F") # do not remove this!
    factory.AddSpectator("iF2 := iF_Recl[2]","F") # do not remove this!
    factory.AddVariable("higher_Lep_eta := max(abs(LepGood_eta[iF_Recl[0]]),abs(LepGood_eta[iF_Recl[1]]))", 'F')
    factory.AddVariable("MT_met_lep1 := MT_met_lep1", 'F')
    factory.AddVariable("numJets_float := nJet25_Recl", 'F')
    factory.AddVariable("mindr_lep1_jet := mindr_lep1_jet", 'F')
    factory.AddVariable("mindr_lep2_jet := mindr_lep2_jet", 'F')
    factory.AddVariable("LepGood_conePt[iF_Recl[0]] := LepGood_conePt[iF_Recl[0]]", 'F') 
    factory.AddVariable("LepGood_conePt[iF_Recl[1]] := LepGood_conePt[iF_Recl[1]]", 'F')
    factory.AddVariable("avg_dr_jet : = avg_dr_jet", 'F');
    factory.AddVariable("met := min(met_pt, 400)", 'F');

else: raise RuntimeError

for trainclass,name,tree,treew in dsets:
    factory.AddTree(tree,trainclass,treew,allcuts)
    print 'Added tree',name

fOut.cd()
for trainclass in set([x[0] for x in dsets]): factory.SetWeightExpression("genWeight*xsec",trainclass)
factory.PrepareTrainingAndTestTree(allcuts,"!V")
#factory.BookMethod(ROOT.TMVA.Types.kBDT,'BDTG','!H:!V:NTrees=500:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000:MaxDepth=8:NegWeightTreatment=PairNegWeightsGlobal')
factory.BookMethod(ROOT.TMVA.Types.kBDT,'BDTG','!H:!V:NTrees=200:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=200:MaxDepth=8:NegWeightTreatment=PairNegWeightsGlobal')
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

fOut.Close()

