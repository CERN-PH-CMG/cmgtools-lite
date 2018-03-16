import ROOT as r

import os

r.gROOT.ProcessLine(".L %s/src/CMGTools/DPS13TeV/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

def deactivateBranches(tree):
    tree.SetBranchStatus('*', 0)
    tree.SetBranchStatus('branchname'     , 1)
    return tree

r.TMVA.Tools.Instance()
 
# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.
includePt = True
useHerwig = True

output_fn  = 'TL_DPS{gen}_BDT{pt}.root'.format(pt='_noPt1' if not includePt else '',gen='Herwigpp' if useHerwig else 'Pythia')
output_f   = r.TFile(output_fn,'RECREATE')
 
factory = r.TMVA.Factory('TMVAClassification', output_f,
                         ':'.join([
                         '!V',
                         '!Silent',
                         'Color',
                         'DrawProgressBar',
                         'Transformations=I;P',
                         'AnalysisType=Classification'])  )



#### our variables
if includePt:
	factory.AddVariable('LepGood_pt[0]','p_{T1}', 'F')
factory.AddVariable('LepGood_pt[1]','p_{T2}', 'F') 
factory.AddVariable('met_pt', 'F') 
factory.AddVariable('mt2davis(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],met_pt,met_phi)','MT2_{ll}', 'F')
factory.AddVariable('mt_2(LepGood_pt[0],LepGood_phi[0],LepGood_pt[1],LepGood_phi[1])','MT l1 l2', 'F') 
factory.AddVariable('mt_2(LepGood_pt[0],LepGood_phi[0],met_pt,met_phi)','MT l1 met', 'F') 
factory.AddVariable('abs(deltaPhi(LepGood_phi[0],LepGood_phi[1]))','#Delta #phi l1 l2', 'F') 
factory.AddVariable('abs(deltaPhi(LepGood_phi[1],met_phi))','#Delta #phi l2 met', 'F') 
factory.AddVariable('abs(deltaPhi(phi_2(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_mass[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],LepGood_mass[1]),LepGood_phi[1]))','#Delta #phi l1l2 l2', 'F')
factory.AddVariable('LepGood_eta[0]*LepGood_eta[1]','#eta_{1}*#eta_{2}', 'F')
factory.AddVariable('abs(LepGood_eta[0]+LepGood_eta[1])','abs(#eta_{1}+#eta_{2})','F')

#factory.AddVariable('mt_2(LepGood_pt[1],LepGood_phi[1],met_pt,met_phi)','MT l2 met', 'F') 
#factory.AddVariable('abs(deltaPhi(LepGood_phi[0],met_phi))','#Delta #phi l1 met', 'F') 
#factory.AddVariable('abs(deltaPhi(deltaPhi(LepGood_phi[0],LepGood_phi[1]),met_phi))','#Delta #phi l1l2 met', 'F')





#factory.AddVariable('abs(dphi_2(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],2))','#Delta #phi ll l2', 'F')

    #factory.AddVariable('max(abs(mt_2(LepGood_pt[0],LepGood_phi[0],met_trkPt,met_trkPhi)-80.),abs(mt_2(LepGood_pt[1],LepGood_phi[1],met_trkPt,met_trkPhi)-80.))','maxThing','F')
    #factory.AddVariable('min(mt_2(LepGood_pt[0],LepGood_phi[0],met_trkPt,met_trkPhi)-91.,mt_2(LepGood_pt[1],LepGood_phi[1],met_trkPt,met_trkPhi)-91.)','minThing','F')
    #factory.AddVariable('mt_2(LepGood_pt[1],LepGood_phi[1],met_pt,met_phi)','MT l2 met', 'F') 
    #factory.AddVariable('abs(deltaPhi(LepGood_phi[0],met_phi))','#Delta #phi 1', 'F') 
    #factory.AddVariable('abs(eta_2(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_mass[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],LepGood_mass[1]))','|#eta ll|','F')   


## get background tree and friends etc p. 16 
treePath = '/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/'
#bkgtreePath = '/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/SingleMuon_Run2016H_part'
#from ROOT import TChain, TSelector, TTree
bkg_tfile = r.TChain('tree')
list1 = ( list( i for i in os.listdir(treePath) if 'SingleMuon_Run2016G' in i) )
n=len(list1)
for d in list1:
    temp = treePath+d+'/treeProducerWMass/tree.root'
    if os.path.isfile(temp):
        bkg_tfile.Add(temp)

#for d in list1:
 #   bkg_tfile.Add(treePath+d+'/treeProducerWMass/tree.root')

#bkg_tfile = r.TFile(treePath+'/SingleMuon_Run2016H_part15/treeProducerWMass/tree.root')
#bkg_ffile = r.TFile('bkgfriendtreefile')
#bkg_tree = bkg_tfile.Get('tree')
#bkg_tree.AddFriend('sf/t', bkg_ffile)

sig_weight = 1.0;
bkg_weight = 1.0;

## get signal tree and friends etc p. 16
#WWDoubleTo2L/
sig_tfile = r.TFile(treePath+'/WW_DPS_herwig/treeProducerWMass/tree.root')
#sig_ffile = r.TFile('bkgfriendtreefile')
sig_tree = sig_tfile.Get('tree')
#sig_tree.AddFriend('sf/t', sig_ffile)

factory.AddSignalTree    ( sig_tree, sig_weight)
factory.AddBackgroundTree( bkg_tfile, bkg_weight)

# cuts defining the signal and background sample
common_cuts = '(LepGood_pt[0] > 25 && LepGood_pt[1] > 20 && nLepGood ==2 && met_pt > 15 && LepGood_tightId[1] > 0 && LepGood_tightId[0] > 0) &&'
afac = '( abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 169 || abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 143 || abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 121)'
afss = '(LepGood_pdgId[0]*LepGood_pdgId[1] == 169) &&'
TLnLL='(LepGood_relIso03[0] > 0.1 ||  LepGood_relIso03[1] > 0.1)'
TL='((LepGood_relIso03[0] > 0.1 && LepGood_relIso03[1] < 0.1) || (LepGood_relIso03[0] < 0.1 && LepGood_relIso03[1] > 0.1))'
LL='(LepGood_relIso03[0] > 0.1 &&  LepGood_relIso03[1] > 0.1)'
sig_cutstring = common_cuts+afac
bkg_cutstring = common_cuts+afss+TL



sigCut = r.TCut(sig_cutstring)
bgCut  = r.TCut(bkg_cutstring)

## just some histograms if you want to. not really necessary
## h_ahisto = r.TH1F('h_ahisto', 'h_ahisto', 50, 0., 1000)
## sig_tree.Draw('(variable)>>h_ahisto', sig_cutstring)
## h_ahisto.Scale(1./h_ahisto.Integral())

 
factory.PrepareTrainingAndTestTree(sigCut,   # signal events p. 21
                                   bgCut,    # background events
                                   ':'.join([
                                   'nTrain_Signal=0',
                                   'nTrain_Background=0',
				   'nTest_Signal=0',
                                   'nTest_Background=0', 
                                   'SplitMode=Random',
                                   'NormMode=NumEvents',
                                   '!V' ]))

## define your methods: BDT, FISHER, LIKELIHOOD. along with the options

# rectangular

## rec = factory.BookMethod(r.TMVA.Types.kCuts, 'Cuts',
## 	  		  ':'.join(['!H', 
##                                    '!V']))

### some sort of bdt
bdt = factory.BookMethod(r.TMVA.Types.kBDT, 'BDT', 
                         ':'.join([ '!H', 
                                    '!V', 
                                    'NTrees=850', 
                                    'MinNodeSize=0.05', 	
				    'MaxDepth=3', 
                                    'BoostType=AdaBoost', 
                                    'AdaBoostBeta=0.5', 
                                    'SeparationType=GiniIndex', 
                                    'nCuts=20', 
                                    'CreateMVAPdfs',
                                    'PruneMethod=NoPruning' ]))

## # Fisher discriminant (same as LD)
fisher = factory.BookMethod(r.TMVA.Types.kFisher, "Fisher", 
                            ':'.join(['H',
                                      '!V',
                                      'Fisher:CreateMVAPdfs',
                                      'PDFInterpolMVAPdf=Spline2',
                                       'NbinsMVAPdf=50',
                                      'NsmoothMVAPdf=10']) )

## ## likelihood
lh = factory.BookMethod(r.TMVA.Types.kLikelihood, 'LikelihoodD', 
                        ':'.join([ '!H', 
                                   '!V', 
                                   '!TRansformOutput', 
                                   'CreateMVAPdfs',
                                   'PDFInterpol=Spline2', 
                                   'NSmoothSig[0]=20', 
                                   'NSmooth=5', 
                                   'NAvEvtPerBin=50', 
                                   'VarTransform=Decorrelate' ]))

## do the training
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

#rarity=root.GetRarity('<BDT>')

output_f.Close()

r.TMVA.TMVAGui(output_fn)

