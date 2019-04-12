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

def _ttH_idEmu_cuts_E3(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.00*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.04): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True
def _ttH_idEmu_cuts_E3_obj(lep):
    if (abs(lep.pdgId())!=11): return True
    etasc = lep.superCluster().eta()
    if (lep.hadronicOverEm()>=(0.10-0.00*(abs(etasc)>1.479))): return False
    eInvMinusPInv = (1.0/lep.ecalEnergy() - lep.eSuperClusterOverP()/lep.ecalEnergy()) if lep.ecalEnergy()>0. else 9e9
    if (eInvMinusPInv<=-0.04): return False
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


import bisect
tauID_oldDMdR0p3wLT2017v2_WP_arrays = [None]*7
tauID_oldDMdR0p3wLT2017v2_WP_arrays[6]=[ #Efficiency: 0.4, idx = 6, VVT
( 21.499, 0.975201 ),
( 23.99, 0.976925 ),
( 26.4932, 0.978126 ),
( 28.9839, 0.979079 ),
( 31.4852, 0.980054 ),
( 33.97, 0.980684 ),
( 36.4678, 0.981174 ),
( 38.9167, 0.981206 ),
( 42.7948, 0.981461 ),
( 47.7929, 0.981953 ),
( 52.8021, 0.982025 ),
( 57.8094, 0.981996 ),
( 64.9841, 0.981836 ),
( 75.0272, 0.981335 ),
( 85.0626, 0.981096 ),
( 95.0522, 0.981808 ),
( 110.744, 0.982142 ),
( 136.024, 0.982425 ),
( 161.245, 0.982149 ),
( 186.384, 0.982817 ),
( 220.564, 0.98124 ),
( 271.301, 0.98211 ),
( 338.565, 0.98132 ),
( 439.535, 0.97752 ),
( 537.345, 0.97394 ),
( 644.707, 0.98568 ),
( 748.5, 0.96764 ),
( 860.167, 0.94798 ),
( 1036.5, 0.94676 ),
]
tauID_oldDMdR0p3wLT2017v2_WP_arrays[5]=[ #Efficiency: 0.5, idx = 5, VT
( 21.499, 0.96405 ),
( 23.99, 0.966388 ),
( 26.4932, 0.967992 ),
( 28.9839, 0.969311 ),
( 31.4852, 0.970579 ),
( 33.97, 0.971421 ),
( 36.4678, 0.972104 ),
( 38.9167, 0.972131 ),
( 42.7948, 0.9725 ),
( 47.7929, 0.9732 ),
( 52.8021, 0.973181 ),
( 57.8094, 0.973095 ),
( 64.9841, 0.972736 ),
( 75.0272, 0.971856 ),
( 85.0626, 0.97127 ),
( 95.0522, 0.97241 ),
( 110.744, 0.972898 ),
( 136.024, 0.973729 ),
( 161.245, 0.973609 ),
( 186.384, 0.9735 ),
( 220.564, 0.972611 ),
( 271.301, 0.972925 ),
( 338.565, 0.971817 ),
( 439.535, 0.970575 ),
( 537.345, 0.9689 ),
( 644.707, 0.9587 ),
( 748.5, 0.9676 ),
( 860.167, 0.94795 ),
( 1036.5, 0.94675 ),
]
tauID_oldDMdR0p3wLT2017v2_WP_arrays[4]=[ #Efficiency: 0.6, idx = 4, T
( 21.499, 0.946846 ),
( 23.99, 0.949968 ),
( 26.4932, 0.952147 ),
( 28.9839, 0.954008 ),
( 31.4852, 0.955488 ),
( 33.97, 0.956636 ),
( 36.4678, 0.957598 ),
( 38.9167, 0.957705 ),
( 42.7948, 0.958113 ),
( 47.7929, 0.959017 ),
( 52.8021, 0.958952 ),
( 57.8094, 0.958817 ),
( 64.9841, 0.958186 ),
( 75.0272, 0.95702 ),
( 85.0626, 0.95589 ),
( 95.0522, 0.957823 ),
( 110.744, 0.958922 ),
( 136.024, 0.960023 ),
( 161.245, 0.960685 ),
( 186.384, 0.96048 ),
( 220.564, 0.959643 ),
( 271.301, 0.95834 ),
( 338.565, 0.957595 ),
( 439.535, 0.95428 ),
( 537.345, 0.95166 ),
( 644.707, 0.94132 ),
( 748.5, 0.73726 ),
( 860.167, 0.94792 ),
( 1036.5, 0.94674 ),
]
tauID_oldDMdR0p3wLT2017v2_WP_arrays[3]=[ #Efficiency: 0.7, idx = 3, M
( 21.499, 0.915749 ),
( 23.99, 0.920235 ),
( 26.4932, 0.923359 ),
( 28.9839, 0.926021 ),
( 31.4852, 0.928059 ),
( 33.97, 0.929552 ),
( 36.4678, 0.930896 ),
( 38.9167, 0.931294 ),
( 42.7948, 0.931757 ),
( 47.7929, 0.932821 ),
( 52.8021, 0.932758 ),
( 57.8094, 0.932772 ),
( 64.9841, 0.931815 ),
( 75.0272, 0.930305 ),
( 85.0626, 0.92877 ),
( 95.0522, 0.932007 ),
( 110.744, 0.933343 ),
( 136.024, 0.935642 ),
( 161.245, 0.937768 ),
( 186.384, 0.937144 ),
( 220.564, 0.938407 ),
( 271.301, 0.933715 ),
( 338.565, 0.93301 ),
( 439.535, 0.93021 ),
( 537.345, 0.91652 ),
( 644.707, 0.92184 ),
( 748.5, 0.73722 ),
( 860.167, 0.85279 ),
( 1036.5, 0.94673 ),
]
tauID_oldDMdR0p3wLT2017v2_WP_arrays[2]=[ #Efficiency: 0.8, idx = 2, L
( 21.499, 0.847098 ),
( 23.99, 0.854083 ),
( 26.4932, 0.859018 ),
( 28.9839, 0.863439 ),
( 31.4852, 0.866511 ),
( 33.97, 0.86949 ),
( 36.4678, 0.872027 ),
( 38.9167, 0.872313 ),
( 42.7948, 0.872895 ),
( 47.7929, 0.875152 ),
( 52.8021, 0.874756 ),
( 57.8094, 0.874508 ),
( 64.9841, 0.873462 ),
( 75.0272, 0.872467 ),
( 85.0626, 0.870138 ),
( 95.0522, 0.875467 ),
( 110.744, 0.878422 ),
( 136.024, 0.882307 ),
( 161.245, 0.886487 ),
( 186.384, 0.89019 ),
( 220.564, 0.88874 ),
( 271.301, 0.87986 ),
( 338.565, 0.88464 ),
( 439.535, 0.88904 ),
( 537.345, 0.86388 ),
( 644.707, 0.87306 ),
( 748.5, 0.43968 ),
( 860.167, 0.85276 ),
( 1036.5, 0.94672 ),
]
tauID_oldDMdR0p3wLT2017v2_WP_arrays[1]=[ #Efficiency: 0.9, idx = 1, VL
( 21.499, 0.650359 ),
( 23.99, 0.663417 ),
( 26.4932, 0.671989 ),
( 28.9839, 0.678143 ),
( 31.4852, 0.683681 ),
( 33.97, 0.690357 ),
( 36.4678, 0.696038 ),
( 38.9167, 0.696698 ),
( 42.7948, 0.698674 ),
( 47.7929, 0.703422 ),
( 52.8021, 0.703852 ),
( 57.8094, 0.704777 ),
( 64.9841, 0.703983 ),
( 75.0272, 0.705216 ),
( 85.0626, 0.700663 ),
( 95.0522, 0.712623 ),
( 110.744, 0.717677 ),
( 136.024, 0.725085 ),
( 161.245, 0.73068 ),
( 186.384, 0.74214 ),
( 220.564, 0.74444 ),
( 271.301, 0.72251 ),
( 338.565, 0.74697 ),
( 439.535, 0.74597 ),
( 537.345, 0.61034 ),
( 644.707, 0.61898 ),
( 748.5, 0.43964 ),
( 860.167, 0.85273 ),
( 1036.5, 0.94671 ),
]
tauID_oldDMdR0p3wLT2017v2_WP_arrays[0]=[ #Efficiency: 0.95, idx = 0, VVL
( 21.499, 0.416049 ),
( 23.99, 0.424832 ),
( 26.4932, 0.434589 ),
( 28.9839, 0.439006 ),
( 31.4852, 0.445049 ),
( 33.97, 0.454461 ),
( 36.4678, 0.461244 ),
( 38.9167, 0.466298 ),
( 42.7948, 0.468553 ),
( 47.7929, 0.474322 ),
( 52.8021, 0.477965 ),
( 57.8094, 0.479831 ),
( 64.9841, 0.477952 ),
( 75.0272, 0.487271 ),
( 85.0626, 0.479775 ),
( 95.0522, 0.495259 ),
( 110.744, 0.502725 ),
( 136.024, 0.512396 ),
( 161.245, 0.51634 ),
( 186.384, 0.54127 ),
( 220.564, 0.55302 ),
( 271.301, 0.514655 ),
( 338.565, 0.586185 ),
( 439.535, 0.558635 ),
( 537.345, 0.50942 ),
( 644.707, 0.56734 ),
( 748.5, 0.43962 ),
( 860.167, 0.852715 ),
( 1036.5, 0.946705 ),
]
import ROOT
RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_mvaOutput_normalization = ROOT.TFormula("RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_mvaOutput_normalization",
                                                                                    "1./(1.+4944671.000000*((1./(0.5*TMath::Max(1.e-6,x+1.)))-1.)/13174771.000000)")
def tauID_oldDMdR0p3wLT2017v2_WP(pt,score,WP):
    xMin = tauID_oldDMdR0p3wLT2017v2_WP_arrays[WP][0][0]
    xMax = tauID_oldDMdR0p3wLT2017v2_WP_arrays[WP][-1][0]
    cutVar = pt
    cutVar = max(cutVar,xMin+1e-3)
    cutVar = min(cutVar,xMax-1e-3)
    idx = bisect.bisect(tauID_oldDMdR0p3wLT2017v2_WP_arrays[WP],(cutVar,0))-1
    x1,c1 = tauID_oldDMdR0p3wLT2017v2_WP_arrays[WP][idx]
    x2,c2 = tauID_oldDMdR0p3wLT2017v2_WP_arrays[WP][idx+1]
    x = (cutVar-x1)/(x2-x1)
    if max(0,min(1,x))!=x: raise RuntimeError
    return RecoTauTag_tauIdMVAIsoDBoldDMdR0p3wLT2017v2_mvaOutput_normalization.Eval(score)>(c1*x+c2*(1-x))

from CMGTools.TTHAnalysis.tools.leptonJetReCleaner import LeptonJetReCleaner
from CMGTools.TTHAnalysis.tools.conept import conept_TTH

MODULES=[]

from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import *
from CMGTools.TTHAnalysis.tools.fastCombinedObjectRecleaner import *
from CMGTools.TTHAnalysis.tools.objFloatCalc import ObjFloatCalc
MODULES.append( ('jetPtRatiov3', lambda : ObjFloatCalc(None,"LepGood",
                                                    dict(jetPtRatiov3 = lambda lep: lep.jetPtRatiov2 if lep.jetBTagCSV > -98 else 1.0/(1.0 + lep.relIso04)))) )

def clean_and_FO_selection_TTH(lep):
    return lep.conept>10 and lep.jetBTagDeepCSV<0.4941 and (abs(lep.pdgId)!=11 or _ttH_idEmu_cuts_E3(lep)) \
        and (lep.mvaTTH>0.90 or \
                 (abs(lep.pdgId)==13 and lep.jetBTagDeepCSV<0.07 and lep.segmentCompatibility>0.3 and lep.jetPtRatiov3>0.60) or \
                 (abs(lep.pdgId)==11 and lep.jetBTagDeepCSV<0.07 and lep.mvaIdFall17noIso>0.5 and lep.jetPtRatiov3>0.60) \
                 )

MODULES.append( ('leptonJetFastReCleanerTTH_step1', lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                                                                       looseLeptonSel = lambda lep : lep.miniRelIso < 0.4 and lep.sip3d < 8,
                                                                                       cleaningLeptonSel = clean_and_FO_selection_TTH,
                                                                                       FOLeptonSel = clean_and_FO_selection_TTH,
                                                                                       tightLeptonSel = lambda lep : clean_and_FO_selection_TTH(lep) and (abs(lep.pdgId)!=13 or lep.mediumMuonId>0) and lep.mvaTTH > 0.90,
                                                                                       FOTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.mvaId2017,1) and tau.idDecayMode,
                                                                                       tightTauSel = lambda tau: tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.mvaId2017,2),
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
MODULES.append( ('kinMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", useTT_2lss='v8,rTT,httTT', useMEM_3l = False)) )
MODULES.append( ('noTTMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", useTT_2lss='', useMEM_3l = False)) )
MODULES.append( ('kinMEMMVA_2D_2lss_3l', lambda : KinMVA_2D_2lss_3l(os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/kinMVA/tth/%s_BDTG.weights.xml", useTT_2lss='v8,rTT,httTT', useMEM_3l = True)) )

from CMGTools.TTHAnalysis.tools.BDTv8_eventReco_cpp import BDTv8_eventReco
MODULES.append( ('oldcode_BDTv8_Hj', lambda : BDTv8_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                      os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                      os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hj_csv_BDTG.weights.xml',
                                                      os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                      selection = [
                lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                ]
                                                      )) )

from CMGTools.TTHAnalysis.tools.BDT_eventReco_cpp import BDT_eventReco
MODULES.append( ('BDTv8_Hj', lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                    os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                    os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hj_2017_configA_dcsv_BDTG.weights.xml',
                                                    os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                    os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                                    os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HadTopTagger_resolved_XGB_CSV_sort_withKinFit.xml.gz',
                                                    os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                                    algostring = 'k_BDTv8_Hj',
                                                    csv_looseWP = 0.5426,
                                                    csv_mediumWP = 0.8484,
                                                    selection = [
                lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                ]
                                                            )) )
MODULES.append( ('BDTrTT_Hj', lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hj_2017_configA_dcsv_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HadTopTagger_resolved_XGB_CSV_sort_withKinFit.xml.gz',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                                     algostring = 'k_rTT_Hj',
                                                     csv_looseWP = 0.5426,
                                                     csv_mediumWP = 0.8484,
                                                      selection = [
                lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                ]
                                                     )) )
MODULES.append( ('BDThttTT_Hj', lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hj_2017_configA_dcsv_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HadTopTagger_resolved_XGB_CSV_sort_withKinFit.xml.gz',
                                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                                     algostring = 'k_httTT_Hj',
                                                     csv_looseWP = 0.5426,
                                                     csv_mediumWP = 0.8484,
                                                      selection = [
                lambda leps,jets,event : len(leps)>=2 and len(jets)>=3,
                lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                ]
                                                     )) )

from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger

MODULES.append( ('Trigger_1e', lambda : EvtTagger("Trigger_1e",[
                lambda ev : ev.HLT_BIT_HLT_Ele32_WPTight_Gsf_v or ev.HLT_BIT_HLT_Ele35_WPTight_Gsf_v
                    ])))
MODULES.append( ('Trigger_1m', lambda : EvtTagger("Trigger_1m",[
                lambda ev : ev.HLT_BIT_HLT_IsoMu24_v or ev.HLT_BIT_HLT_IsoMu27_v
                    ])))
MODULES.append( ('Trigger_2e', lambda : EvtTagger("Trigger_2e",[
                lambda ev : ev.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v or ev.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v
                    ])))
MODULES.append( ('Trigger_2m', lambda : EvtTagger("Trigger_2m",[
                lambda ev : ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v or ev.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v
                    ])))
MODULES.append( ('Trigger_em', lambda : EvtTagger("Trigger_em",[
                lambda ev : ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v or \
                    ev.HLT_BIT_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v or \
                    ev.HLT_BIT_HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v
                    ])))
MODULES.append( ('Trigger_3e', lambda : EvtTagger("Trigger_3e",[
                lambda ev : ev.HLT_BIT_HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v
                    ])))
MODULES.append( ('Trigger_3m', lambda : EvtTagger("Trigger_3m",[
                lambda ev : ev.HLT_BIT_HLT_TripleMu_12_10_5_v
                    ])))
MODULES.append( ('Trigger_mee', lambda : EvtTagger("Trigger_mee",[
                lambda ev : ev.HLT_BIT_HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v
                    ])))
MODULES.append( ('Trigger_mme', lambda : EvtTagger("Trigger_mme",[
                lambda ev : ev.HLT_BIT_HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v
                    ])))
MODULES.append( ('Trigger_2lss', lambda : EvtTagger("Trigger_2lss",[
                lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em ])))
MODULES.append( ('Trigger_3l', lambda : EvtTagger("Trigger_3l",[
                lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme ])))


from CMGTools.TTHAnalysis.tools.objTagger import ObjTagger
MODULES.append( ('TauTightFlag', lambda : ObjTagger("isTauTight","TauSel_Recl",
                                                    [lambda tau : tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.mvaId2017,2)] )))

from CMGTools.TTHAnalysis.tools.bTagEventWeightsCSVFullShape import BTagEventWeightFriend
MODULES.append( ('eventBTagWeight', lambda : BTagEventWeightFriend(csvfile=os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/data/btag/DeepCSV_94XSF_V2_B_F.csv",
                                                                   discrname="btagDeepCSV")))

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

from CMGTools.TTHAnalysis.tools.bestHmmFriend import BestHmm
MODULES.append( ('bestHmm', lambda : BestHmm(label="_Recl")) )
