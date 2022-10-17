import os.path

MODULES = []

from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import LeptonJetReCleaner

utility_files_dir = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/")
isFastSim = False

# btag event weights in 80X
from CMGTools.TTHAnalysis.tools.bTagEventWeights import BTagEventWeightFriend
btagsf_payload = os.path.join(utility_files_dir, "btag", "CSVv2_ichep.csv")
btagsf_payload_fastsim = os.path.join(utility_files_dir, "btag", "CSV_13TEV_TTJets_11_7_2016.csv")
bTagEventWeight = lambda : BTagEventWeightFriend(csvfile=btagsf_payload, algo='csv', recllabel='Recl')
btag_efficiency_file = os.path.join(utility_files_dir, "btag", "bTagEffs.root")
bTagEventWeightFastSIM = lambda : BTagEventWeightFriend(csvfile=btagsf_payload, csvfastsim=btagsf_payload_fastsim, eff_rootfile=btag_efficiency_file, algo='csv', recllabel='Recl')
MODULES.append( ('eventBTagWeight', bTagEventWeight ))
MODULES.append( ('bTagEventWeightFastSIM', bTagEventWeightFastSIM ))


#--- Recleaner instances
from CMGTools.TTHAnalysis.tools.leptonChoiceRA5 import _susy2lss_lepId_CBloose,_susy2lss_lepId_loosestFO,_susy2lss_lepId_IPcuts,_susy2lss_lepConePt1015,_susy2lss_lepId_tighterFO,_susy2lss_multiIso,_susy2lss_lepId_CB,_susy2lss_idIsoEmu_cuts
from CMGTools.TTHAnalysis.tools.leptonChoiceRA7 import _susy3l_lepId_CBloose, _susy3l_lepId_loosestFO,_susy3l_lepId_loosestFO,_susy3l_multiIso,_susy3l_lepId_CB
from CMGTools.TTHAnalysis.tools.leptonBuilderEWK import _susyEWK_lepId_CBloose, _susyEWK_lepId_IPcuts, _susyEWK_lepId_MVAFO, _susyEWK_lepId_MVAmedium, _susyEWK_tauId_CBloose, _susyEWK_tauId_CBtight
from CMGTools.TTHAnalysis.tools.functionsEWKino import _ewkino_idEmu_cuts_E2, _ewkino_2lss_lepId_CBloose, _ewkino_2lss_lepId_FO, _ewkino_2lss_lepId_num,_ewkino_3l_lepId_FO, _ewkino_3l_lepId_num, _ewkino_2lss_lepId_IPcuts, _ewkino_leptonMVA_VT, _ewkino_leptonMVA_M
from CMGTools.TTHAnalysis.tools.conept import conept_RA5, conept_RA7, conept_EWK, conept_SSDL, conept_SSDL_for3l

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
MODULES.append( ('leptonJetReCleanerSusyRA7', lambda : LeptonJetReCleaner("Mini", 
                   lambda lep : lep.miniRelIso < 0.4 and _susy3l_lepId_CBloose(lep), #and (ht>300 or _susy2lss_idIsoEmu_cuts(lep)), 
                   lambda lep : lep.pt>10 and _susy3l_lepId_loosestFO(lep) and _susy2lss_lepId_IPcuts(lep), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and _susy2lss_lepId_IPcuts(lep) and _susy3l_lepId_loosestFO(lep), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and _susy3l_multiIso(lep) and _susy3l_lepId_CB(lep), # cuts applied on top of loose
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


# MVA (upper limits and combination)
MODULES.append( ('leptonJetReCleanerSusyEWK3L', lambda : LeptonJetReCleaner("Mini", 
                   lambda lep : lep.miniRelIso < 0.4 and _susyEWK_lepId_CBloose(lep) and _susyEWK_lepId_IPcuts(lep), 
                   lambda lep : lep.pt>10 and lep.conept>10 and (_susyEWK_lepId_MVAmedium(lep) or _susyEWK_lepId_MVAFO(lep)),
                   lambda lep,ht : lep.pt>10 and lep.conept>10 and (_susyEWK_lepId_MVAmedium(lep) or _susyEWK_lepId_MVAFO(lep)), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and lep.conept>10 and _susyEWK_lepId_MVAmedium(lep), # medium WP
                   cleanJet = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanTau = lambda lep,tau,dr: dr<0.4,
                   looseTau = lambda tau: _susyEWK_tauId_CBloose(tau), # used in cleaning
                   tightTau = lambda tau: _susyEWK_tauId_CBtight(tau), # on top of loose
                   cleanJetsWithTaus = True,
                   cleanTausWithLoose = True,
                   doVetoZ = False,
                   doVetoLMf = False,
                   doVetoLMt = True,
                   jetPt = 30,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_EWK(lep, 2),
                 ) ))

# All jets, needed for tau fakes study
MODULES.append( ('leptonJetReCleanerNoCleanTausSusyEWK3L', lambda : LeptonJetReCleaner("Mini", 
                   lambda lep : lep.miniRelIso < 0.4 and _susyEWK_lepId_CBloose(lep) and _susyEWK_lepId_IPcuts(lep), 
                   lambda lep : lep.pt>10 and lep.conept>10 and (_susyEWK_lepId_MVAmedium(lep) or _susyEWK_lepId_MVAFO(lep)),
                   lambda lep,ht : lep.pt>10 and lep.conept>10 and (_susyEWK_lepId_MVAmedium(lep) or _susyEWK_lepId_MVAFO(lep)), # cuts applied on top of loose
                   lambda lep,ht : lep.pt>10 and lep.conept>10 and _susyEWK_lepId_MVAmedium(lep), # medium WP
                   cleanJet  = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanTau  = lambda lep,tau,dr: dr<0.4,
                   looseTau  = lambda tau: _susyEWK_tauId_CBloose(tau), # used in cleaning
                   tightTau  = lambda tau: _susyEWK_tauId_CBtight(tau), # on top of loose
                   cleanJetsWithTaus = False,
                   cleanTausWithLoose = True,
                   doVetoZ = False,
                   doVetoLMf = False,
                   doVetoLMt = True,
                   jetPt = 20,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_EWK(lep, 2),
                 ) ))

MODULES.append( ('leptonJetReCleanerSusyEWK2L', lambda : LeptonJetReCleaner("Recl", 
                   looseLeptonSel = lambda lep : lep.miniRelIso < 0.4 and _ewkino_2lss_lepId_IPcuts(lep) and _ewkino_2lss_lepId_CBloose(lep),
                   cleaningLeptonSel = lambda lep : lep.pt>10 and lep.conept>10 and (_ewkino_2lss_lepId_num(lep) or _ewkino_2lss_lepId_FO(lep)), # cuts on top of loose
                   FOLeptonSel = lambda lep,ht : lep.pt>10 and lep.conept>10 and (_ewkino_2lss_lepId_num(lep) or _ewkino_2lss_lepId_FO(lep)), # cuts on top of loose
                   tightLeptonSel = lambda lep,ht : lep.pt>10 and lep.conept>10 and _ewkino_2lss_lepId_num(lep), # on top of loose 
                   cleanJet = lambda lep,jet,dr : dr<0.4,
                   selectJet = lambda jet: abs(jet.eta)<2.4,
                   cleanTau = lambda lep,tau,dr: dr<0.4,
                   looseTau = lambda tau: _susyEWK_tauId_CBloose(tau), # used in cleaning
                   tightTau = lambda tau: _susyEWK_tauId_CBtight(tau), # on top of loose
                   cleanJetsWithTaus = True,
                   doVetoZ = True,
                   doVetoLMf = True,
                   doVetoLMt = True,
                   jetPt = 40,
                   bJetPt = 25,
                   coneptdef = lambda lep: conept_SSDL(lep)
                 ) ))

MODULES.append( ('MediumMuonID2016', lambda : ObjTagger(label='ICHEPmediumMuonId', coll='LepGood',
                                                      sel = [lambda x : abs(x.pdgId)==13,
                                                             lambda x : x.isGlobalMuon or x.isTrackerMuon,
                                                             lambda x : x.innerTrackValidHitFraction>0.49,
                                                             lambda x : x.segmentCompatibility>0.451 or (x.isGlobalMuon and x.globalTrackChi2<3 and x.chi2LocalPosition<12 and x.trkKink<20 and x.segmentCompatibility>0.303)
                                                             ])) )



#--- Lepton builder instances
from CMGTools.TTHAnalysis.tools.leptonBuilderEWK import LeptonBuilderEWK

MODULES.append( ('leptonBuilderEWK', lambda : LeptonBuilderEWK("Mini")))
MODULES.append( ('leptonBuilderWZCR_EWK', lambda : LeptonBuilderEWK("Recl")))

#--- Tau builder instances
from CMGTools.TTHAnalysis.tools.TauFakesBuilder import TauFakesBuilder

MODULES.append( ('tauFakesBuilderEWKMini', lambda : TauFakesBuilder("Mini")))
MODULES.append( ('tauFakesBuilderEWKRecl', lambda : TauFakesBuilder("Recl")))

#--- Lepton choice instances

from CMGTools.TTHAnalysis.tools.leptonChoiceRA5 import LeptonChoiceRA5
from CMGTools.TTHAnalysis.tools.leptonChoiceRA7 import LeptonChoiceRA7

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
MODULES.append( ('leptonChoiceEWK', lambda : LeptonChoiceEWK("Loop","Mini",whichApplication="Super",isFastSim=isFastSim,filePathFakeRate=RA7_FRname,filePathLeptonSFfull=RA7_full_lepSF,filePathLeptonSFfast=RA7_fast_lepSF,filePathPileUp=RA7_puweights)))


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
MODULES.append( ('kinMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", skip_BDTv8 = True, skip_MEM = True)) )
from CMGTools.TTHAnalysis.tools.kinMVA_MultiClass import KinMVA_MultiClass
MODULES.append( ('kinMVA_MultiClass', lambda : KinMVA_MultiClass(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/macros/leptons/weights/MultiClassICHEP16_%s_BDTG.weights.xml")) )
from CMGTools.TTHAnalysis.tools.HadTopSimple import HadTopSimple
MODULES.append( ('HadTopSimple', lambda : HadTopSimple()) )
from CMGTools.TTHAnalysis.tools.BDT2_HadTop import BDT2_HadTop
MODULES.append( ('BDT2_HadTop', lambda : BDT2_HadTop(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_BDTG.weights_BDT2.xml")) )
from CMGTools.TTHAnalysis.tools.BDTv8_eventReco_cpp import BDTv8_eventReco
MODULES.append( ('BDTv8_eventReco', lambda : BDTv8_eventReco(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_BDTG_bdt_v8_80x.weights.xml",
                                                             selection = [
#                lambda leps,jets,event : event.nJet25_Recl >= 2 and event.nLepFO_Recl >= 2 and (event.nLepFO_Recl >= 3 or leps[0].charge*leps[1].charge > 0),
#                lambda leps,jets,event : event.nBJetLoose25_Recl >= 2 or event.nBJetMedium25_Recl >= 1,
#                lambda leps,jets,event : leps[0].conePt > 20 and leps[1].conePt > 10,
                                                             ])) )

# retuned soft muon ID for 2016 conditions
from CMGTools.TTHAnalysis.tools.objTagger import ObjTagger
MODULES.append( ('SoftMuonID2016', lambda : ObjTagger(label='SoftMuonID2016', coll='LepGood',
                                                      sel = [lambda x : abs(x.pdgId)==13,
                                                             lambda x : x.TMOneStationTightMuonId,
                                                             lambda x : x.trackerLayers > 5,
                                                             lambda x : x.pixelLayers > 0,
                                                             lambda x : abs(x.dxy)<0.3 and abs(x.dz)<20.,
                                                             ])) )

#--- Lepton MVA in friend tree

from CMGTools.TTHAnalysis.tools.LepMVAFriend import LepMVAFriend

MODULES.append( ('LepMVAFriendTTH', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/tth/%s_BDTG.weights.xml",
                                                          os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/tth/%s_BDTG.weights.xml",),
                                                         training="forMoriond16", label="TTHMoriond16")) )
MODULES.append( ('LepMVAFriendSUSY', lambda: LepMVAFriend((os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/susy/%s_BDTG.weights.xml",
                                                           os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/leptonMVA/susy/%s_BDTG.weights.xml",),
                                                          training="forMoriond16", label="SUSY")) )
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


