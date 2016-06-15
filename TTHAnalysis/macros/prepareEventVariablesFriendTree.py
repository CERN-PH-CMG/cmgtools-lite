#!/usr/bin/env python
from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import LeptonJetReCleaner
from glob import glob
import os.path, re, types, itertools

MODULES = []

utility_files_dir = os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/"
isFastSim = False

#btagSF = utility_files_dir+"/btag/CSVv2_25ns.csv"
#btagEFF = utility_files_dir+"/btag/btageff__ttbar_powheg_pythia8_25ns.root"
#btagSF_FastSim = utility_files_dir+"/btag/CSV_13TEV_Combined_20_11_2015_FullSim_FastSim.csv"

#from CMGTools.TTHAnalysis.tools.btagRWTs_ND import BTagWeightCalculator,BTagReweightFriend,BTagLeptonReweightFriend
## btag reweighting in 76X
#BTagReweight76X = lambda : BTagWeightCalculator(utility_files_dir_tth+"/csv_rwt_fit_hf_76x_2016_02_08.root",
#                                                utility_files_dir_tth+"/csv_rwt_fit_lf_76x_2016_02_08.root")
#systsBTAG = ["nominal", "_JESUp", "_JESDown", "_LFUp", "_LFDown", "_HFUp", "_HFDown", \
#                 "_HFStats1Up", "_HFStats1Down", "_HFStats2Up", "_HFStats2Down", \
#                 "_LFStats1Up", "_LFStats1Down", "_LFStats2Up", "_LFStats2Down", \
#                 "_cErr1Up", "_cErr1Down", "_cErr2Up", "_cErr2Down" ]
#for syst in systsBTAG: # should be converted to lambda functions
#    MODULES.append( ('btagRWJet%s'%syst, BTagReweightFriend(BTagReweight76X, outlabel='btagCSVWeight%s'%syst.replace('nominal',''), rwtSyst=syst.replace('_','')) ))
#    MODULES.append( ('btagRWJetUp%s'%syst, BTagReweightFriend(BTagReweight76X, jets=["Jet_jecUp","DiscJet_jecUp"], outlabel='btagCSVWeight%s'%syst.replace('nominal',''), rwtSyst=syst.replace('_','')) ))
#    MODULES.append( ('btagRWJetDown%s'%syst, BTagReweightFriend(BTagReweight76X, jets=["Jet_jecDown","DiscJet_jecDown"], outlabel='btagCSVWeight%s'%syst.replace('nominal',''), rwtSyst=syst.replace('_','')) ))
#    MODULES.append( ('btagRWLep%s'%syst, BTagLeptonReweightFriend(BTagReweight76X, outlabel='jetBTagCSVWeight%s'%syst.replace('nominal',''), rwtSyst=syst.replace('_','')) ))
#
#from CMGTools.TTHAnalysis.tools.eventBTagRWT import EventBTagRWT
#MODULES.append( ('eventBTagRWT', lambda: EventBTagRWT() ))

#--- Recleaner instances

from CMGTools.TTHAnalysis.tools.leptonChoiceRA5 import _susy2lss_lepId_CBloose,_susy2lss_lepId_loosestFO,_susy2lss_lepId_IPcuts,_susy2lss_lepConePt1015,_susy2lss_lepId_tighterFO,_susy2lss_multiIso,_susy2lss_lepId_CB,_susy2lss_idIsoEmu_cuts
from CMGTools.TTHAnalysis.tools.leptonChoiceRA7 import _susy3l_lepId_CBloose, _susy3l_lepId_loosestFO,_susy3l_lepId_loosestFO,_susy3l_multiIso,_susy3l_lepId_CB
from CMGTools.TTHAnalysis.tools.leptonChoiceEWK import _susy3l_lepId_IPcutsMVA,_susy3l_lepId_CBlooseMVA
from CMGTools.TTHAnalysis.tools.functionsTTH import _ttH_idEmu_cuts_E2
from CMGTools.TTHAnalysis.tools.functionsEWKino import _ewkino_idEmu_cuts_E2, _ewkino_2lss_lepId_CBloose,_ewkino_2lss_lepId_loosestFO, _ewkino_2lss_lepId_tighterFO, _ewkino_2lss_lepId_IPcuts, _ewkino_2lss_lepConePt1015, _ewkino_2lss_leptonMVA_T, _ewkino_2lss_leptonMVA_VT
from CMGTools.TTHAnalysis.tools.conept import conept_RA5, conept_RA7, conept_TTH, conept_SSDL

MODULES.append( ('leptonJetReCleanerSusyRA5', lambda : LeptonJetReCleaner("Mini", 
                   lambda lep : lep.miniRelIso < 0.4 and _susy2lss_lepId_CBloose(lep), #and (ht>300 or _susy2lss_idIsoEmu_cuts(lep)), 
                   lambda lep : lep.pt>10 and _susy2lss_lepId_loosestFO(lep) and _susy2lss_lepId_IPcuts(lep), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and _susy2lss_lepConePt1015(lep) and _susy2lss_lepId_IPcuts(lep) and (_susy2lss_lepId_loosestFO(lep) if ht>300 else _susy2lss_lepId_tighterFO(lep)), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and _susy2lss_lepConePt1015(lep) and _susy2lss_multiIso(lep) and _susy2lss_lepId_CB(lep) and (ht>300 or _susy2lss_idIsoEmu_cuts(lep)), # cuts applied on top of loose
                   cleanJet = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanJetsWithTaus = False,
                   doVetoZ = True,
                   doVetoLMf = True,
                   doVetoLMt = True,
                   jetPt = 40,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_RA5(lep),
                   storeJetVariables = True                                                       
                 ) ))

# updated cut-based RA7
#MODULES.append( ('leptonJetReCleanerSusyRA7', lambda : LeptonJetReCleaner("Mini", 
#                   lambda lep : lep.miniRelIso < 0.4 and _susy3l_lepId_CBloose(lep), #and (ht>300 or _susy2lss_idIsoEmu_cuts(lep)), 
#                   lambda lep : lep.pt>10 and _susy3l_lepId_loosestFO(lep) and _susy2lss_lepId_IPcuts(lep), # cuts applied on top of loose
#                   lambda lep,ht : lep.pt>10 and _susy2lss_lepId_IPcuts(lep) and _susy3l_lepId_loosestFO(lep), # cuts applied on top of loose
#                   lambda lep,ht : lep.pt>10 and _susy3l_multiIso(lep) and _susy3l_lepId_CB(lep), # cuts applied on top of loose
#                   cleanJet = lambda lep,jet,dr : dr<0.4,
#                   selectJet = lambda jet: abs(jet.eta)<2.4,
#                   cleanTau = lambda lep,tau,dr: dr<0.4,
#                   looseTau = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idMVAOldDMRun2 >= 1 and tau.idDecayMode, # used in cleaning
#                   tightTau = lambda tau: tau.idMVAOldDMRun2 == 3, # on top of loose
#                   cleanJetsWithTaus = True,
#                   doVetoZ = False,
#                   doVetoLMf = False,
#                   doVetoLMt = True,
#                   jetPt = 30,
#                   bJetPt = 25,
#                   coneptdef = lambda lep: conept_RA7(lep),
#                 ) ))

# MVA (sync 76X)
#MODULES.append( ('leptonJetReCleanerSusyEWK', lambda : LeptonJetReCleaner("Mini", 
#                   lambda lep : lep.miniRelIso < 0.4 and _susy3l_lepId_CBlooseMVA(lep) and _susy3l_lepId_IPcutsMVA(lep), 
#                   lambda lep : True, # cuts applied on top of loose
#                   lambda lep,ht : lep.pt>10 and _susy3l_lepId_loosestFO(lep), # cuts applied on top of loose
#                   #lambda lep,ht : (abs(lep.pdgId) == 13 and lep.mvaSUSY>-0.60 and lep.mediumMuonId>0) or (abs(lep.pdgId)==11 and lep.mvaSUSY>0.25), # loose WP 
#                   lambda lep,ht : (abs(lep.pdgId) == 13 and lep.mvaSUSY>-0.20 and lep.mediumMuonId>0) or (abs(lep.pdgId)==11 and lep.mvaSUSY>0.5), # medium WP
#                   cleanJet = lambda lep,jet,dr : dr<0.4,
#                   selectJet = lambda jet: abs(jet.eta)<2.4,
#                   cleanTau = lambda lep,tau,dr: dr<0.4,
#                   looseTau = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idMVAOldDMRun2dR03 >= 1 and tau.idDecayMode, # used in cleaning 
#                   tightTau = lambda tau: True, # cuts applied on top of loose
#                   cleanJetsWithTaus = True,
#                   doVetoZ = False,
#                   doVetoLMf = False,
#                   doVetoLMt = True,
#                   jetPt = 30,
#                   bJetPt = 25,
#                   coneptdef = lambda lep: conept_RA7(lep)
#                 ) ))

# MVA (upper limits and combination)
MODULES.append( ('leptonJetReCleanerSusyEWK', lambda : LeptonJetReCleaner("Mini", 
                   lambda lep : lep.miniRelIso < 0.4 and _susy3l_lepId_CBlooseMVA(lep) and _susy3l_lepId_IPcutsMVA(lep), 
                   lambda lep : True, # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and _susy3l_lepId_loosestFO(lep), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and (abs(lep.pdgId) == 13 and lep.mvaSUSY>-0.20 and lep.mediumMuonId>0) or (abs(lep.pdgId)==11 and lep.mvaSUSY>0.5), # medium WP
                   cleanJet = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanTau = lambda lep,tau,dr: dr<0.4,
                   looseTau = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idMVAOldDMRun2 >= 1 and tau.idDecayMode, # used in cleaning
                   tightTau = lambda tau: tau.idMVAOldDMRun2 == 3, # on top of loose
                   cleanJetsWithTaus = True,
                   doVetoZ = False,
                   doVetoLMf = False,
                   doVetoLMt = True,
                   jetPt = 30,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_RA7(lep),
                 ) ))

MODULES.append( ('leptonJetReCleanerSusySSDL', lambda : LeptonJetReCleaner("Recl", 
                   looseLeptonSel = lambda lep : lep.miniRelIso < 0.4 and _ewkino_2lss_lepId_IPcuts(lep),
                   cleaningLeptonSel = lambda lep : lep.conept>10 and _ewkino_2lss_lepId_CBloose(lep), # cuts applied on top of loose (pt 5, 7, conveto, lotHist<=1 && emulation)
                   FOLeptonSel = lambda lep,ht : lep.conept>10 and _ewkino_2lss_lepId_loosestFO(lep), # cuts on top of loose (previous + tight charge and lostHits==0)
                   tightLeptonSel = lambda lep,ht : lep.conept>10 and _ewkino_2lss_lepConePt1015(lep) and _ewkino_2lss_leptonMVA_VT(lep) and _ewkino_2lss_lepId_tighterFO(lep), # on top of loose 
                   cleanJet = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanTau = lambda lep,tau,dr: dr<0.4,
                   looseTau = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idMVAOldDMRun2dR03 >= 1 and tau.idDecayMode, # used in cleaning 
                   tightTau = lambda tau: True, # cuts applied on top of loose                                                                           
                   cleanJetsWithTaus = False,
                   doVetoZ = True,
                   doVetoLMf = True,
                   doVetoLMt = True,
                   jetPt = 40,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_SSDL(lep)
                 ) ))


MODULES.append( ('leptonJetReCleanerTTH', lambda : LeptonJetReCleaner("Recl", # b1E2 definition of FO
                   looseLeptonSel = lambda lep : lep.miniRelIso < 0.4 and lep.sip3d < 8,
                   cleaningLeptonSel = lambda lep : lep.conept>10 and lep.jetBTagCSV<0.89 and (abs(lep.pdgId)!=11 or lep.conept<30 or _ttH_idEmu_cuts_E2(lep)) and ((lep.jetPtRatiov2>0.3 and lep.jetBTagCSV<0.605) or lep.mvaTTH>0.75), # cuts applied on top of loose
                   FOLeptonSel = lambda lep,ht : lep.conept>10 and lep.jetBTagCSV<0.89 and (abs(lep.pdgId)!=11 or lep.conept<30 or _ttH_idEmu_cuts_E2(lep)) and ((lep.jetPtRatiov2>0.3 and lep.jetBTagCSV<0.605) or lep.mvaTTH>0.75), # cuts applied on top of loose
                   tightLeptonSel = lambda lep,ht : lep.conept>10 and lep.jetBTagCSV<0.89 and (abs(lep.pdgId)!=11 or lep.conept<30 or _ttH_idEmu_cuts_E2(lep)) and ((lep.jetPtRatiov2>0.3 and lep.jetBTagCSV<0.605) or lep.mvaTTH>0.75) and (abs(lep.pdgId)!=13 or lep.mediumMuonId>0) and lep.mvaTTH > 0.75, # cuts applied on top of loose
                   cleanJet = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanJetsWithTaus = True,
                   doVetoZ = True,
                   doVetoLMf = True,
                   doVetoLMt = True,
                   jetPt = 40,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_TTH(lep) ) ))


#--- Lepton choice instances

from CMGTools.TTHAnalysis.tools.leptonChoiceRA5 import LeptonChoiceRA5
from CMGTools.TTHAnalysis.tools.leptonChoiceRA7 import LeptonChoiceRA7
from CMGTools.TTHAnalysis.tools.leptonChoiceEWK import LeptonChoiceEWK

# for RA5
#FRname=utility_files_dir+"/FakeRatesUCSXMethod_301115_withEWKsyst_v6.root"
FRname="hardcodedUCSx"
FS_lepSF=[utility_files_dir+"/leptonSF/sf_mu_mediumID_multi.root",utility_files_dir+"/leptonSF/sf_el_tight_IDEmu_ISOEMu_ra5.root"]

MODULES.append( ('leptonChoiceRA5_Sync', lambda : LeptonChoiceRA5("Loop","Mini",whichApplication="Fakes",lepChoiceMethod="TTSync",FRFileName=FRname,isFastSim=isFastSim,lepSFFileNameFastSim=FS_lepSF))) 
MODULES.append( ('leptonChoiceRA5_Fakes', lambda : LeptonChoiceRA5("Loop","Mini",whichApplication="Fakes",lepChoiceMethod="TT_loopTF_2FF",FRFileName=FRname,isFastSim=isFastSim,lepSFFileNameFastSim=FS_lepSF))) 
#MODULES.append( ('leptonChoiceRA5_FO', lambda : LeptonChoiceRA5("SortFO","Mini",whichApplication="Fakes",lepChoiceMethod="sort_FO",FRFileName=FRname,isFastSim=isFastSim,lepSFFileNameFastSim=FS_lepSF))) 
MODULES.append( ('leptonChoiceRA5_Flips', lambda : LeptonChoiceRA5("Flips","Mini",whichApplication="Flips",FRFileName="hardcodedUCSx",isFastSim=isFastSim,lepSFFileNameFastSim=FS_lepSF)))


# for RA7
# syntax: <filepath>::<histogram>[::<upvar>::<downvar>]
# objects are always lists, first entry is muons, second is electrons
# entries themselves can be lists if there are more than 1 histogram per flavor
RA7_FRname     = [[utility_files_dir+"/fakerate/ra7_FR_Jan16.root::FRMuPtCorr_UCSX_non::FRMuPtCorr_UCSX_HI_non::FRMuPtCorr_UCSX_LO_non"],
                  [utility_files_dir+"/fakerate/ra7_FR_Jan16.root::FRElPtCorr_UCSX_non::FRElPtCorr_UCSX_HI_non::FRElPtCorr_UCSX_LO_non"]]
RA7_full_lepSF = [[utility_files_dir+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root::pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_tag_IsoMu20_pass",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_MuonID_NUM_TightIP2D_DENOM_LooseID_VAR_map_pt_eta.root::pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_PF_pass_&_tag_IsoMu20_pass",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_MuonID_NUM_TightIP3D_DENOM_LooseID_VAR_map_pt_eta.root::pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_PF_pass_&_tag_IsoMu20_pass",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fullsim/muons/TnP_MuonID_NUM_MultiIsoMedium_DENOM_MediumID_VAR_map_pt_eta.root::pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_tag_combRelIsoPF04dBeta_bin0_&_tag_pt_bin0_&_Medium_pass_&_tag_IsoMu20_pass"],
                  [utility_files_dir+"/leptonSF/ra7_lepsf_fullsim/electrons/kinematicBinSFele.root::MVATight_and_IDEmu_and_TightIP2D_and_TightIP3D",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fullsim/electrons/kinematicBinSFele.root::MultiIsoTight_vs_AbsEta"]]
RA7_fast_lepSF = [[utility_files_dir+"/leptonSF/ra7_lepsf_fastsim/muons/sf_mu_mediumID.root::histo3D", 
                   utility_files_dir+"/leptonSF/ra7_lepsf_fastsim/muons/sf_mu_tightIP2D.root::histo3D",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fastsim/muons/sf_mu_tightIP3D.root::histo3D",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fastsim/muons/sf_mu_multi.root::histo3D"],
                  [utility_files_dir+"/leptonSF/ra7_lepsf_fastsim/electrons/sf_el_tight2d3dIDEmu.root::histo3D",
                   utility_files_dir+"/leptonSF/ra7_lepsf_fastsim/electrons/sf_el_multi.root::histo3D"]]
RA7_puweights = utility_files_dir+"/pileup/ra7_puWeights.root::pileup"

MODULES.append( ('leptonChoiceRA7', lambda : LeptonChoiceRA7("Loop","Mini",whichApplication="Fakes",isFastSim=isFastSim,filePathFakeRate=RA7_FRname,filePathLeptonSFfull=RA7_full_lepSF,filePathLeptonSFfast=RA7_fast_lepSF,filePathPileUp=RA7_puweights))) 
MODULES.append( ('leptonChoiceEWK', lambda : LeptonChoiceEWK("Loop","Mini",isFastSim=isFastSim,filePathFakeRate=RA7_FRname,filePathLeptonSFfull=RA7_full_lepSF,filePathLeptonSFfast=RA7_fast_lepSF))) 


#--- Friend trees for fake rate calculation

from CMGTools.TTHAnalysis.tools.leptonFakeRateQCDVars import LeptonFakeRateQCDVars

MODULES.append( ('leptonFakeRateQCDVarsTTH', lambda : LeptonFakeRateQCDVars(
                lambda lep : lep.sip3d < 8,
                lambda jet, lep, dr : jet.pt > (20 if abs(jet.eta)<2.4 else 30) and dr > 0.7) ) )
MODULES.append( ('leptonFakeRateQCDVarsSusy', lambda : LeptonFakeRateQCDVars(
                lambda lep : lep.miniRelIso < 0.4 and _susy2lss_lepId_CBloose(lep) and _susy2lss_lepId_loosestFO(lep) and _susy2lss_lepId_IPcuts(lep),
                lambda jet, lep, dr : jet.pt > 40 and abs(jet.eta)<2.4 and dr > 1.0 and jet.id ) ) )


#--- Pileup reweighting

from CMGTools.TTHAnalysis.tools.vertexWeightFriend import VertexWeightFriend

putruefilemc = utility_files_dir+"/pileup/zjets-4-nvtx_plots_true.root"
putruefiledata_central = utility_files_dir+"/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_pileup_69000_50.root"
putruefiledata_up = utility_files_dir+"/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_pileup_69000_50_p5pc.root"
putruefiledata_down = utility_files_dir+"/json/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_pileup_69000_50_m5pc.root"
MODULES.append ( ('puWeightsTrue_central', lambda : VertexWeightFriend(putruefilemc,putruefiledata_central,"nTrueInt_signal","pileup",verbose=True,vtx_coll_to_reweight="nTrueInt",name="vtxWeight") ) )
MODULES.append ( ('puWeightsTrue_up', lambda : VertexWeightFriend(putruefilemc,putruefiledata_up,"nTrueInt_signal","pileup",verbose=True,vtx_coll_to_reweight="nTrueInt",postfix="up",name="vtxWeightUp") ) )
MODULES.append ( ('puWeightsTrue_down', lambda : VertexWeightFriend(putruefilemc,putruefiledata_down,"nTrueInt_signal","pileup",verbose=True,vtx_coll_to_reweight="nTrueInt",postfix="down",name="vtxWeightDown") ) )


#--- TTH event variables

from CMGTools.TTHAnalysis.tools.eventVars_2lss import EventVars2LSS 
MODULES.append( ('ttH2lss', lambda : EventVars2LSS()) )
from CMGTools.TTHAnalysis.tools.kinMVA_2D_2lss_3l import KinMVA_2D_2lss_3l
MODULES.append( ('kinMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml")) )
from CMGTools.TTHAnalysis.tools.BDT2_HadTop import BDT2_HadTop
MODULES.append( ('BDT2_HadTop', lambda : BDT2_HadTop(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_BDTG.weights_BDT2.xml")) )

#--- Lepton MVA in friend tree

from CMGTools.TTHAnalysis.tools.LepMVAFriend import LepMVAFriend

MODULES.append( ('LepMVAFriendTTH', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/tth/%s_BDTG.weights.xml",
                                                          os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/tth/%s_BDTG.weights.xml",),
                                                         training="forMoriond16", label="TTHMoriond16")) )
MODULES.append( ('LepMVAFriendSUSY', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/susy/%s_BDTG.weights.xml",
                                                           os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/susy/%s_BDTG.weights.xml",),
                                                          training="forMoriond16", label="TTZMoriond16")) )
MODULES.append( ('LepMVAFriendJetLessIVF', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVF_%s_BDTG.weights.xml",
                                                                 os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVF_%s_BDTG.weights.xml",),
                                                                training="SoftJetLessIVF", label="JetLessIVF")) )
MODULES.append( ('LepMVAFriendNoPtRewJetLess', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/%s_noPtRew_BDTG.weights.xml",
                                                                     os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/%s_noPtRew_BDTG.weights.xml",),
                                                                    training="SoftJetLessIVF", label="JetLessNoPtRew")) )
MODULES.append( ('LepMVAFriendJetLessCSV', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLess_%s_BDTG.weights.xml",
                                                                 os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLess_%s_BDTG.weights.xml",),
                                                                training="SoftJetLess", label="JetLessCSV")) )
MODULES.append( ('LepMVAFriendJetLessSVSafe', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessSVSafe_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessSVSafe_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessIVFSVSafe", label="JetLessSVSafe")) )
MODULES.append( ('LepMVAFriendJetLessNOBTAG', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAG_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAG_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessNOBTAG", label="JetLessNOBTAG")) )
MODULES.append( ('LepMVAFriendJetLessNO04ISO', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNO04ISO_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNO04ISO_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessNO04ISO", label="JetLessNO04ISO")) )

MODULES.append( ('LepMVAFriendJetLessNOBTAGNOTAU_SIGT2tt', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAGNOTAU_SIGT2tt_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAGNOTAU_SIGT2tt_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessNOBTAG", label="JetLessNOBTAGNOTAU_SIGT2tt")) )
MODULES.append( ('LepMVAFriendJetLessNOBTAGNOTAU_SIGTChiNeu8090', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAGNOTAU_SIGTChiNeu8090_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAGNOTAU_SIGTChiNeu8090_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessNOBTAG", label="JetLessNOBTAGNOTAU_SIGTChiNeu8090")) )

MODULES.append( ('LepMVAFriendJetLessNOBTAGNOTAU_SIGDY', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAGNOTAU_SIGDY_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessNOBTAGNOTAU_SIGDY_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessNOBTAG", label="JetLessNOBTAGNOTAU_SIGDY")) )
MODULES.append( ('LepMVAFriendJetLessIVFNOTAU_SIGT2tt', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVFNOTAU_SIGT2tt_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVFNOTAU_SIGT2tt_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessIVF", label="JetLessIVFNOTAU_SIGT2tt")) )
MODULES.append( ('LepMVAFriendJetLessIVFNOTAU_SIGTChiNeu8090', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVFNOTAU_SIGTChiNeu8090_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVFNOTAU_SIGTChiNeu8090_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessIVF", label="JetLessIVFNOTAU_SIGTChiNeu8090")) )

MODULES.append( ('LepMVAFriendJetLessIVFNOTAU_SIGDY', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVFNOTAU_SIGDY_%s_BDTG.weights.xml",
                                                                    os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/jetless/SoftJetLessIVFNOTAU_SIGDY_%s_BDTG.weights.xml",),
                                                                   training="SoftJetLessIVF", label="JetLessIVFNOTAU_SIGDY")) )



class VariableProducer(Module):
    def __init__(self,name,booker,modules):
        Module.__init__(self,name,booker)
        self._modules = [ (n,m() if type(m) == types.FunctionType else m) for (n,m) in modules ]
    def beginJob(self):
        self.t = PyTree(self.book("TTree","t","t"))
        self.branches = {}
        for name,mod in self._modules:
            print name
            print mod.listBranches()
            for B in mod.listBranches():
                # don't add the same branch twice
                if B in self.branches: 
                    print "Will not add branch %s twice" % (B,)
                    continue
                self.branches[B] = True
                if type(B) == tuple:
                    if len(B) == 2:
                        self.t.branch(B[0],B[1])
                    elif len(B) == 4:
                        self.t.branch(B[0],B[1],n=B[2],lenVar=B[3])
                    elif len(B) == 3:
                        self.t.branch(B[0],B[1],n=B[2],lenVar=None)
                else:
                    self.t.branch(B ,"F")
    def analyze(self,event):
        for name,mod in self._modules:
            keyvals = mod(event)
            for B,V in keyvals.iteritems():
                setattr(self.t, B, V)
                setattr(event,  B, V)
        self.t.fill()


import os, itertools
from optparse import OptionParser
parser = OptionParser(usage="%prog [options] <TREE_DIR> <OUT>")
parser.add_option("-m", "--modules", dest="modules",  type="string", default=[], action="append", help="Run these modules");
parser.add_option("-d", "--dataset", dest="datasets",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times)");
parser.add_option("-D", "--dm", "--dataset-match", dest="datasetMatches",  type="string", default=[], action="append", help="Process only this dataset (or dataset if specified multiple times): REGEXP");
parser.add_option("-c", "--chunk",   dest="chunks",    type="int",    default=[], action="append", help="Process only these chunks (works only if a single dataset is selected with -d)");
parser.add_option("-N", "--events",  dest="chunkSize", type="int",    default=500000, help="Default chunk size when splitting trees");
parser.add_option("-j", "--jobs",    dest="jobs",      type="int",    default=1, help="Use N threads");
parser.add_option("-p", "--pretend", dest="pretend",   action="store_true", default=False, help="Don't run anything");
parser.add_option("-T", "--tree-dir",   dest="treeDir",     type="string", default="sf", help="Directory of the friend tree in the file (default: 'sf')");
parser.add_option("-q", "--queue",   dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
parser.add_option("-t", "--tree",    dest="tree",      default='ttHLepTreeProducerTTH', help="Pattern for tree name");
parser.add_option("-V", "--vector",  dest="vectorTree", action="store_true", default=True, help="Input tree is a vector");
parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename") 
parser.add_option("--FMC", "--add-friend-mc",    dest="friendTreesMC",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to MC only. Can use {name}, {cname} patterns in the treename") 
parser.add_option("--FD", "--add-friend-data",    dest="friendTreesData",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename) to data trees only. Can use {name}, {cname} patterns in the treename") 
parser.add_option("-L", "--list-modules",  dest="listModules", action="store_true", default=False, help="just list the configured modules");
parser.add_option("-n", "--new",  dest="newOnly", action="store_true", default=False, help="Make only missing trees");
parser.add_option("-I", "--import", dest="imports",  type="string", default=[], action="append", help="Modules to import");
parser.add_option("--fastsim",  dest="isFastSim", action="store_true", default=False, help="Run with configuration for FastSim samples");
parser.add_option("--log", "--log-dir", dest="logdir", type="string", default=None, help="Directory of stdout and stderr");
parser.add_option("--env",   dest="env",     type="string", default="lxbatch", help="Give the environment on which you want to use the batch system (lxbatch, psi)");
parser.add_option("--bk",   dest="bookkeeping",  action="store_true", default=False, help="If given the command used to run the friend tree will be stored");
(options, args) = parser.parse_args()

if options.imports:
    MODULES = []
    from importlib import import_module
    for mod in options.imports:
        import_module(mod)
        obj = sys.modules[mod]
        for (name,x) in obj.MODULES:
            print "Loaded %s from %s " % (name, mod)
            MODULES.append((name,x))

if options.listModules:
    print "List of modules"
    for (n,x) in MODULES:
        if type(x) == types.FunctionType: x = x()
        print "   '%s': %s" % (n,x)
    exit()

if "{P}" in args[1]: args[1] = args[1].replace("{P}",args[0])
if len(args) != 2 or not os.path.isdir(args[0]):
    print "Usage: program <TREE_DIR> <OUT>"
    exit()
if not os.path.isdir(args[1]): 
    os.system("mkdir -p "+args[1])
    if not os.path.isdir(args[1]): 
        print "Could not create output directory"
        exit()
if len(options.chunks) != 0 and len(options.datasets) != 1:
    print "must specify a single dataset with -d if using -c to select chunks"
    exit()

jobs = []
for D in glob(args[0]+"/*"):
    treename = options.tree
    fname    = "%s/%s/%s_tree.root" % (D,options.tree,options.tree)
    if (not os.path.exists(fname)) and (os.path.exists("%s/%s/tree.root" % (D,options.tree)) ):
        treename = "tree"
        fname    = "%s/%s/tree.root" % (D,options.tree)

    if (not os.path.exists(fname)) and (os.path.exists("%s/%s/tree.root.url" % (D,options.tree)) ):
        treename = "tree"
        fname    = "%s/%s/tree.root" % (D,options.tree)
        fname    = open(fname+".url","r").readline().strip()

    if os.path.exists(fname) or (os.path.exists("%s/%s/tree.root.url" % (D,options.tree))):
        short = os.path.basename(D)
        if options.datasets != []:
            if short not in options.datasets: continue
        if options.datasetMatches != []:
            found = False
            for dm in  options.datasetMatches:
                if re.match(dm,short): found = True
            if not found: continue
        data =  any(x in short for x in "DoubleMu DoubleEl DoubleEG MuEG MuonEG SingleMu SingleEl".split()) # FIXME
        f = ROOT.TFile.Open(fname)
        t = f.Get(treename)
        if not t:
            print "Corrupted ",fname
            continue
        entries = t.GetEntries()
        f.Close()
        if options.newOnly:
            fout = "%s/evVarFriend_%s.root" % (args[1],short)
            if os.path.exists(fout):
                f = ROOT.TFile.Open(fname);
                t = f.Get(treename)
                if t.GetEntries() != entries:
                    print "Component %s has to be remade, mismatching number of entries (%d vs %d)" % (short, entries, t.GetEntries()) 
                    f.Close()
                else:
                    print "Component %s exists already and has matching number of entries (%d)" % (short, entries) 
                    continue 
        chunk = options.chunkSize
        if entries < chunk:
            print "  ",os.path.basename(D),("  DATA" if data else "  MC")," single chunk"
            jobs.append((short,fname,"%s/evVarFriend_%s.root" % (args[1],short),data,xrange(entries),-1))
        else:
            nchunk = int(ceil(entries/float(chunk)))
            print "  ",os.path.basename(D),("  DATA" if data else "  MC")," %d chunks" % nchunk
            for i in xrange(nchunk):
                if options.chunks != []:
                    if i not in options.chunks: continue
                r = xrange(int(i*chunk),min(int((i+1)*chunk),entries))
                jobs.append((short,fname,"%s/evVarFriend_%s.chunk%d.root" % (args[1],short,i),data,r,i))
print "\n"
print "I have %d task(s) to process" % len(jobs)

if options.queue:
    import os, sys

    runner = "lxbatch_runner.sh"
    super  = "bsub -q {queue}".format(queue = options.queue)
    if options.queue in ["all.q", "short.q", "long.q"] and options.env == "psi":
        super  = "qsub -q {queue} -N friender".format(queue = options.queue)
        runner = "psibatch_runner.sh"

    basecmd = "{dir}/{runner} {dir} {cmssw} python {self} -N {chunkSize} -T {tdir} -t {tree} {data} {output}".format(
                dir = os.getcwd(), runner=runner, cmssw = os.environ['CMSSW_BASE'],
                self=sys.argv[0], chunkSize=options.chunkSize, tdir=options.treeDir,
                tree=options.tree, data=args[0], output=args[1])

    writelog = ""
    logdir   = ""
    if options.logdir: logdir = options.logdir.rstrip("/")

    if options.vectorTree: basecmd += " --vector "
    friendPost =  "".join(["  -F  %s %s " % (fn,ft) for fn,ft in options.friendTrees])
    friendPost += "".join([" --FM %s %s " % (fn,ft) for fn,ft in options.friendTreesMC])
    friendPost += "".join([" --FD %s %s " % (fn,ft) for fn,ft in options.friendTreesData])
    friendPost += "".join(["  -m  '%s'  " % m for m in options.modules])
    for (name,fin,fout,data,range,chunk) in jobs:
        if chunk != -1:
            if options.logdir: writelog = "-o {logdir}/{data}_{chunk}.out -e {logdir}/{data}_{chunk}.err".format(logdir=logdir, data=name, chunk=chunk)
            cmd = "{super} {writelog} {base} -d {data} -c {chunk} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)
        else:
            if options.logdir: writelog = "-o {logdir}/{data}.out -e {logdir}/{data}.err".format(logdir=logdir, data=name)
            cmd = "{super} {writelog} {base} -d {data} {post}".format(super=super, writelog=writelog, base=basecmd, data=name, chunk=chunk, post=friendPost)

        print cmd
        if not options.pretend: 
            os.system(cmd)
        
    exit()

maintimer = ROOT.TStopwatch()
def _runIt(myargs):
    (name,fin,fout,data,range,chunk) = myargs
    timer = ROOT.TStopwatch()
    fetchedfile = None
    if 'LSB_JOBID' in os.environ or 'LSF_JOBID' in os.environ:
        if fin.startswith("root://"):
            try:
                tmpdir = os.environ['TMPDIR'] if 'TMPDIR' in os.environ else "/tmp"
                tmpfile =  "%s/%s" % (tmpdir, os.path.basename(fin))
                print "xrdcp %s %s" % (fin, tmpfile)
                os.system("xrdcp %s %s" % (fin, tmpfile))
                if os.path.exists(tmpfile):
                    fin = tmpfile 
                    fetchedfile = fin
                    print "success :-)"
            except:
                pass
        fb = ROOT.TFile.Open(fin)
    elif "root://" in fin:        
        ROOT.gEnv.SetValue("TFile.AsyncReading", 1);
        fb   = ROOT.TXNetFile(fin+"?readaheadsz=65535&DebugLevel=0")
        os.environ["XRD_DEBUGLEVEL"]="0"
        os.environ["XRD_DebugLevel"]="0"
        os.environ["DEBUGLEVEL"]="0"
        os.environ["DebugLevel"]="0"
    else:
        fb = ROOT.TFile.Open(fin)
        print fb

    print "getting tree.."
    tb = fb.Get(options.tree)

    if not tb: tb = fb.Get("tree") # new trees
    if options.vectorTree:
        tb.vectorTree = True
    else:
        tb.vectorTree = False

    friends = options.friendTrees[:]
    friends += (options.friendTreesData if data else options.friendTreesMC)
    friends_ = [] # to make sure pyroot does not delete them
    for tf_tree,tf_file in friends:
        tf = tb.AddFriend(tf_tree, tf_file.format(name=name, cname=name)),
        friends_.append(tf) # to make sure pyroot does not delete them
    nev = tb.GetEntries()
    if options.pretend:
        print "==== pretending to run %s (%d entries, %s) ====" % (name, nev, fout)
        return (name,(nev,0))
    print "==== %s starting (%d entries) ====" % (name, nev)
    booker = Booker(fout)
    modulesToRun = MODULES
    if options.modules != []:
        toRun = {}
        for m,v in MODULES:
            for pat in options.modules:
                if re.match(pat,m):
                    toRun[m] = True 
        modulesToRun = [ (m,v) for (m,v) in MODULES if m in toRun ]
    el = EventLoop([ VariableProducer(options.treeDir,booker,modulesToRun), ])
    el.loop([tb], eventRange=range)
    booker.done()
    fb.Close()
    time = timer.RealTime()
    print "=== %s done (%d entries, %.0f s, %.0f e/s) ====" % ( name, nev, time,(nev/time) )
    if fetchedfile and os.path.exists(fetchedfile):
        print 'Cleaning up: removing %s'%fetchedfile
        os.system("rm %s"%fetchedfile)
    if options.bookkeeping:
        if not os.path.exists(fout[:fout.rfind("/")] + "/cmd"): os.system("mkdir -p " + fout[:fout.rfind("/")] + "/cmd")
        fcmd = open(fout[:fout.rfind("/")] + "/cmd/" + fout[fout.rfind("/")+1:].rstrip(".root") + "_command.txt", "w")
        fcmd.write("%s\n\n" % " ".join(sys.argv)) 
        fcmd.write("%s\n%s\n" % (args,options)) 
        fcmd.close()
    return (name,(nev,time))

if options.jobs > 0:
    from multiprocessing import Pool
    pool = Pool(options.jobs)
    ret  = dict(pool.map(_runIt, jobs)) if options.jobs > 0 else dict([_runIt(j) for j in jobs])
else:
    ret = dict(map(_runIt, jobs))
fulltime = maintimer.RealTime()
totev   = sum([ev   for (ev,time) in ret.itervalues()])
tottime = sum([time for (ev,time) in ret.itervalues()])
print "Done %d tasks in %.1f min (%d entries, %.1f min)" % (len(jobs),fulltime/60.,totev,tottime/60.)



