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

output_fn  = 'training/TL_TMVAOutputTraining_WZ.root'
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

factory.AddVariable('LepGood_pt[0]','p_{T1}', 'F')
factory.AddVariable('LepGood_pt[1]','p_{T2}', 'F')
factory.AddVariable('met_pt', 'F')
factory.AddVariable('mt2davis(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],met_pt,met_phi)','MT2_{ll}', 'F')
factory.AddVariable('mt_2(LepGood_pt[0],LepGood_phi[0],LepGood_pt[1],LepGood_phi[1])','MT l1 l2', 'F')
factory.AddVariable('mt_2(LepGood_pt[0],LepGood_phi[0],met_pt,met_phi)','MT l1 met', 'F')
factory.AddVariable('abs(deltaPhi(LepGood_phi[0],LepGood_phi[1]))','#Delta #phi l1 l2', 'F')
factory.AddVariable('abs(deltaPhi(LepGood_phi[1],met_phi))','#Delta #phi l2 met', 'F')
factory.AddVariable('abs(deltaPhi(phi_2(LepGood_pt[0],LepGood_eta[0],LepGood_phi[0],LepGood_mass[0],LepGood_pt[1],LepGood_eta[1],LepGood_phi[1],LepGood_mass[1]),LepGood_phi[1]))','d#phi(ll,l2)', 'F')
factory.AddVariable('LepGood_eta[0]*LepGood_eta[1]','#eta_{1}*#eta_{2}', 'F')
factory.AddVariable('abs(LepGood_eta[0]+LepGood_eta[1])','abs(#eta_{1}+#eta_{2})','F')

## get background and signal trees/chains

sig_tfile = r.TFile('/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/WW_DPS_herwig/treeProducerWMass/tree.root')

useNLO = False
if useNLO:
    bkg_tfile = r.TChain('tree')
    bkg_tfile.Add('/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/WZTo3LNu_fxfx_part1/treeProducerWMass/tree.root')
    bkg_tfile.Add('/eos/user/m/mdunser/dps-13TeV-combination/TREES_latest/WZTo3LNu_fxfx_part2/treeProducerWMass/tree.root')
    factory.SetBackgroundWeightExpression('genWeight/abs(genWeight)') ## reweight by the genweight for NLO samples

else:
    bkg_tfile = r.TChain('tree')
    bkg_tfile.Add('/eos/cms/store/cmst3/group/tthlep/peruzzi/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2/WZTo3LNu_treeProducerSusyMultilepton_tree.root')
    #bkg_tfile.Add('/eos/cms/store/cmst3/user/mdunser/HeppyProduction/TTH_150117//WZTo3LNu_mll01_ext_part1_treeProducerSusyMultilepton_tree.root')
    #bkg_tfile.Add('/eos/cms/store/cmst3/user/mdunser/HeppyProduction/TTH_150117//WZTo3LNu_mll01_ext_part2_treeProducerSusyMultilepton_tree.root')
    #bkg_tfile.Add('/eos/cms/store/cmst3/user/mdunser/HeppyProduction/TTH_150117//WZTo3LNu_mll01_ext_part3_treeProducerSusyMultilepton_tree.root')


sig_weight = 1.0
bkg_weight = 1.0

sig_tree = sig_tfile.Get('tree')

factory.AddSignalTree    ( sig_tree , sig_weight)
factory.AddBackgroundTree( bkg_tfile, bkg_weight)


# cuts defining the signal and background sample
common_cuts = '(nLepGood==2 && LepGood_pt[0]>25. && LepGood_pt[1]>20. && met_pt > 15. )' # && LepGood_tightId[1]>0 && LepGood_tightId[0]>0 && met_pt>15.)'
tightCharge = '(LepGood_chargeConsistency[0] ==2 || abs(LepGood_pdgId[0]) == 13) && (LepGood_chargeConsistency[1] ==2 || abs(LepGood_pdgId[1]) == 13)'
mmac        = '(abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 169)'
mmss        = '(LepGood_pdgId[0]*LepGood_pdgId[1] == 169)'
afac        = '(abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 169 || abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 121)'
afss        = '(LepGood_pdgId[0]*LepGood_pdgId[1] == 169 || LepGood_pdgId[0]*LepGood_pdgId[1] == 121)'
TT          = 'LepGood_mvaTTH[0] > 0.75 && LepGood_mvaTTH[1] > 0.75'
sig_cutstring = ' && '.join([common_cuts, afac, tightCharge, TT])
bkg_cutstring = ' && '.join([common_cuts, afss, tightCharge, TT])

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
## fisher = factory.BookMethod(r.TMVA.Types.kFisher, "Fisher", 
##                             ':'.join(['H',
##                                       '!V',
##                                       'Fisher:CreateMVAPdfs',
##                                       'PDFInterpolMVAPdf=Spline2',
##                                       'NbinsMVAPdf=50',
##                                       'NsmoothMVAPdf=10']) )
## 
## ## likelihood
## lh = factory.BookMethod(r.TMVA.Types.kLikelihood, 'LikelihoodD', 
##                         ':'.join([ '!H', 
##                                    '!V', 
##                                    '!TRansformOutput', 
##                                    'CreateMVAPdfs',
##                                    'PDFInterpol=Spline2', 
##                                    'NSmoothSig[0]=20', 
##                                    'NSmooth=5', 
##                                    'NAvEvtPerBin=50', 
##                                    'VarTransform=Decorrelate' ]))
 
## do the training
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

#rarity=root.GetRarity('<BDT>')

output_f.Close()

r.TMVA.TMVAGui(output_fn)

