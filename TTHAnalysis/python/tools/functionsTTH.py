def _ttH_idEmu_cuts_E2(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True
def _ttH_idEmu_cuts_E2_obj(lep):
    if (abs(lep.pdgId())!=11): return True
    etasc = lep.superCluster().eta()
    if (lep.hadronicOverEm()>=(0.10-0.03*(abs(etasc)>1.479))): return False
    if (abs(lep.deltaEtaSuperClusterTrackAtVtx())>=(0.01-0.002*(abs(etasc)>1.479))): return False
    if (abs(lep.deltaPhiSuperClusterTrackAtVtx())>=(0.04+0.03*(abs(etasc)>1.479))): return False
    eInvMinusPInv = (1.0/lep.ecalEnergy() - lep.eSuperClusterOverP()/lep.ecalEnergy()) if lep.ecalEnergy()>0. else 9e9
    if (eInvMinusPInv<=-0.05): return False
    if (eInvMinusPInv>=(0.01-0.005*(abs(etasc)>1.479))): return False
    if (lep.full5x5_sigmaIetaIeta()>=(0.011+0.019*(abs(etasc)>1.479))): return False
    return True

def _soft_MuonId_2016ICHEP(lep):
    if (abs(lep.pdgId())!=13): return False
    if not lep.muonID("TMOneStationTight"): return False #TMOneStationTightMuonId
    if not lep.track().hitPattern().trackerLayersWithMeasurement() > 5: return False
    if not lep.track().hitPattern().pixelLayersWithMeasurement() > 0: return False
    if not (abs(lep.dxy())<0.3 and abs(lep.dz())<20): return False
    return True

def _medium_MuonId_2016ICHEP(lep):
    if (abs(lep.pdgId())!=13): return False
    if not (lep.physObj.isGlobalMuon() or lep.physObj.isTrackerMuon()): return False
    if not (lep.innerTrack().validFraction()>0.49): return False
    if lep.segmentCompatibility()>0.451: return True
    else:
        if not lep.globalTrack().isNonnull(): return False
        if not lep.isGlobalMuon: return False
        if not lep.globalTrack().normalizedChi2()<3: return False
        if not lep.combinedQuality().chi2LocalPosition<12: return False
        if not lep.combinedQuality().trkKink<20: return False 
        if not lep.segmentCompatibility()>0.303: return False

    return True


from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import LeptonJetReCleaner
from CMGTools.TTHAnalysis.tools.conept import conept_TTH

MODULES=[]

from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import *
from CMGTools.TTHAnalysis.tools.fastCombinedObjectRecleaner import *

def clean_and_FO_selection_TTH(lep):
    return lep.conept>10 and lep.jetBTagDeepCSV<0.4941 and (abs(lep.pdgId)!=11 or _ttH_idEmu_cuts_E2(lep)) \
        and (lep.mvaTTH>0.90 or (lep.jetPtRatiov2>0.5 and lep.jetBTagDeepCSV<0.1522 and (abs(lep.pdgId)!=13 or lep.segmentCompatibility>0.3) and (abs(lep.pdgId)!=11 or lep.mvaIdSpring16HZZ > (0.0 if abs(lep.eta)<1.479 else 0.7)) ) )

MODULES.append( ('leptonJetFastReCleanerTTH_step1', lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                                                                       looseLeptonSel = lambda lep : lep.miniRelIso < 0.4 and lep.sip3d < 8,
                                                                                       cleaningLeptonSel = clean_and_FO_selection_TTH,
                                                                                       FOLeptonSel = clean_and_FO_selection_TTH,
                                                                                       tightLeptonSel = lambda lep : clean_and_FO_selection_TTH(lep) and (abs(lep.pdgId)!=13 or lep.mediumMuonId>0) and lep.mvaTTH > 0.90,
                                                                                       FOTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idMVAdR03 >=2  and tau.idDecayMode,
                                                                                       tightTauSel = lambda tau: tau.idMVAdR03 >= 3,
                                                                                       selectJet = lambda jet: abs(jet.eta)<2.4,
                                                                                       coneptdef = lambda lep: conept_TTH(lep) ) ))
MODULES.append( ('leptonJetFastReCleanerTTH_step2_mc',lambda : fastCombinedObjectRecleaner(label="Recl",
                                                                                           inlabel="_InternalRecl",
                                                                                           cleanTausWithLooseLeptons=True,
                                                                                           cleanJetsWithFOTaus=True,
                                                                                           doVetoZ=False,
                                                                                           doVetoLMf=False,
                                                                                           doVetoLMt=False,
                                                                                           jetPts=[25,40],
                                                                                           btagL_thr=0.1522,
                                                                                           btagM_thr=0.4941,
                                                                                           isMC = True) ))
MODULES.append( ('leptonJetFastReCleanerTTH_step2_data',lambda : fastCombinedObjectRecleaner(label="Recl",
                                                                                             inlabel="_InternalRecl",
                                                                                             cleanTausWithLooseLeptons=True,
                                                                                             cleanJetsWithFOTaus=True,
                                                                                             doVetoZ=False,
                                                                                             doVetoLMf=False,
                                                                                             doVetoLMt=False,
                                                                                             jetPts=[25,40],
                                                                                             btagL_thr=0.1522,
                                                                                             btagM_thr=0.4941,
                                                                                             isMC = False) ))

from CMGTools.TTHAnalysis.tools.eventVars_2lss import EventVars2LSS
MODULES.append( ('eventVars', lambda : EventVars2LSS('','Recl')) )

from CMGTools.TTHAnalysis.tools.kinMVA_2D_2lss_3l import KinMVA_2D_2lss_3l
MODULES.append( ('kinMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", skip_BDTv8 = False, skip_MEM = True, skip_Hj=False)) )
MODULES.append( ('nov8MVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", skip_BDTv8 = True, skip_MEM = True, skip_Hj=True)) )
MODULES.append( ('kinMEMMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", skip_BDTv8 = False, skip_MEM = False, skip_Hj=False)) )

from CMGTools.TTHAnalysis.tools.BDTv8_eventReco_cpp import BDTv8_eventReco
MODULES.append( ('BDTv8_Hj', lambda : BDTv8_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                      os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                      os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hj_csv_BDTG.weights.xml',
                                                      os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                      selection = [
                lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                ]
                                                      )) )

from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger
# Activated below, but not present in 2017B:
# HLT_Ele32_WPTight_Gsf_v
# HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v
# HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v
# Moreover, some 3mu triggers are only in last part of the dataset (e.g. 5_3_3)
MODULES.append( ('Trigger_2lss', lambda : EvtTagger("Trigger_2l",[
                lambda ev : \
                    ev.HLT_BIT_HLT_IsoMu27_v or \
                    ev.HLT_BIT_HLT_Ele32_WPTight_Gsf_v or \
                    ev.HLT_BIT_HLT_Ele35_WPTight_Gsf_v or \
                    ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v or \
                    ev.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v or \
                    ev.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v or \
                    ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v or \
                    ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v or \
                    ev.HLT_BIT_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v \
                    ] )))
MODULES.append( ('Trigger_3l', lambda : EvtTagger("Trigger_3l",[
                lambda ev : \
                    ev.HLT_TripleMu or \
                    ev.HLT_TripleEl or \
                    ev.HLT_DoubleMuEl or \
                    ev.HLT_DoubleElMu or \
                    ev.Trigger_2l \
                    ] )))

from CMGTools.TTHAnalysis.tools.objTagger import ObjTagger
MODULES.append( ('TauTightFlag', lambda : ObjTagger("isTauTight","TauSel_Recl",
                                                    [lambda tau : tau.idMVAdR03>=3] )))

from CMGTools.TTHAnalysis.tools.bTagEventWeightsCSVFullShape import BTagEventWeightFriend
MODULES.append( ('eventBTagWeight', lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/btag/DeepCSV_94XSF_V1_B_F.csv",
                                                                   discrname="btagDeepCSV")))

from CMGTools.TTHAnalysis.tools.BDT_resolvedTopTagger_cpp import BDT_resolvedTopTagger
MODULES.append( ('BDT_rTT', lambda : BDT_resolvedTopTagger(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xGBoost_v0.weights.xml")) )

from CMGTools.TTHAnalysis.tools.higgsRecoTTH import HiggsRecoTTH
MODULES.append( ('higgsRecoTTH', lambda : HiggsRecoTTH(label="_Recl",
                                                       cut_BDT_rTT_score = 0.0,
                                                       cuts_mW_had = (60.,100.),
                                                       cuts_mH_vis = (80.,140.),
                                                       btagDeepCSVveto = 0.1522) ))

from CMGTools.TTHAnalysis.tools.ttHMCEventReco import TTHMCEventReco
MODULES.append( ('genLevelChain', lambda : TTHMCEventReco()) )

from CMGTools.TTHAnalysis.tools.matchRecoToPartonsTTH import MatchRecoToPartonsTTH
MODULES.append( ('matchPartons', lambda : MatchRecoToPartonsTTH(label="_Recl")) )

from CMGTools.TTHAnalysis.tools.vertexWeightFriend import VertexWeightFriend
# run on a big number of events, ideally one job per file using -N big_number, and not on skimmed trees when auto-reweighthing the pileup to avoid loss of statistical power!
MODULES.append( ('vtxWeight', lambda : VertexWeightFriend(myfile=None, targetfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/pileup/puWeights_2017_41p4fb_rereco_69p2mb.root",
                                                          myhist=None,targethist="pileup",name="vtxWeight2017",
                                                          verbose=False,vtx_coll_to_reweight="nTrueInt",autoPU=True)) )
