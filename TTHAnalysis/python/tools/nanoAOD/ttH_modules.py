conf = dict(
        muPt = 5, 
        elePt = 7, 
        miniRelIso = 0.4, 
        sip3d = 8, 
        dxy =  0.05, 
        dz = 0.1, 
        eleId = "mvaFall17V2noIso_WPL",
)

ttH_skim_cut = ("nMuon + nElectron >= 2 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf)


muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt" ] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and getattr(l, conf["eleId"])

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(5, 
                muonSel = muonSelection, electronSel = electronSelection,
                minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                minLeptons = 2, requireSameSignPair = True,
                jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0, 
                minJets = 4, minMET = 70)
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLeptonCombMasses import ttHLeptonCombMasses
lepMasses = ttHLeptonCombMasses( [ ("Muon",muonSelection), ("Electron",electronSelection) ], maxLeps = 4)

from CMGTools.TTHAnalysis.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.TTHAnalysis.tools.nanoAOD.yearTagger import yearTag
from CMGTools.TTHAnalysis.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepJetBTagDeepFlavC

ttH_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepMasses]

#==== 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
centralJetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0
lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = centralJetSel,
                                  pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                  maxLeptons = 1, requirePair = True)
from CMGTools.TTHAnalysis.tools.nanoAOD.nBJetCounter import nBJetCounter
nBJetDeepCSV25NoRecl = lambda : nBJetCounter("DeepCSV25", "btagDeepB", centralJetSel)
nBJetDeepFlav25NoRecl = lambda : nBJetCounter("DeepFlav25", "btagDeepFlavB", centralJetSel)

ttH_sequence_step1_FR = [m for m in ttH_sequence_step1 if m != lepSkim] + [ lepFR, nBJetDeepCSV25NoRecl, nBJetDeepFlav25NoRecl ]
ttH_skim_cut_FR = ("nMuon + nElectron >= 1 && nJet >= 1 && Sum$(Jet_pt > 25 && abs(Jet_eta)<2.4) >= 1 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 1").format(**conf)


#==== items below are normally run as friends ====

def ttH_idEmu_cuts_E3(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hoe>=(0.10-0.00*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.04): return False
    if (lep.sieie>=(0.011+0.019*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    return True

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > 0.90: return lep.pt
    else: return 0.90 * lep.pt * (1 + lep.jetRelIso)

def smoothBFlav(jetpt,ptmin,ptmax,year,scale_loose=1.0):
    wploose = (0.0614, 0.0521, 0.0494)
    wpmedium = (0.3093, 0.3033, 0.2770)
    x = min(max(0.0, jetpt - ptmin)/(ptmax-ptmin), 1.0)
    return x*wploose[year-2016]*scale_loose + (1-x)*wpmedium[year-2016]

def clean_and_FO_selection_TTH(lep,year):
    bTagCut = 0.3093 if year==2016 else 0.3033 if year==2017 else 0.2770
    return lep.conept>10 and lep.jetBTagDeepFlav<bTagCut and (abs(lep.pdgId)!=11 or ttH_idEmu_cuts_E3(lep)) \
        and (lep.mvaTTH>(0.85 if abs(lep.pdgId)==13 else 0.80) or \
             (abs(lep.pdgId)==13 and lep.jetBTagDeepFlav< smoothBFlav(0.9*lep.pt*(1+lep.jetRelIso), 20, 45, year) and lep.jetRelIso < 0.50) or \
             (abs(lep.pdgId)==11 and lep.mvaFall17V2noIso_WP80 and lep.jetRelIso < 0.70))

tightLeptonSel = lambda lep,year : clean_and_FO_selection_TTH(lep,year) and (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > (0.85 if abs(lep.pdgId)==13 else 0.80)

foTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idDecayMode and (int(tau.idMVAoldDMdR032017v2)>>1 & 1) # VLoose WP
tightTauSel = lambda tau: (int(tau.idMVAoldDMdR032017v2)>>2 & 1) # Loose WP

from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.TTHAnalysis.tools.nanoAOD.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner
recleaner_step1 = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                       looseLeptonSel = lambda lep : lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8 and (abs(lep.pdgId)!=11 or lep.lostHits<=1),
                                       cleaningLeptonSel = clean_and_FO_selection_TTH,
                                       FOLeptonSel = clean_and_FO_selection_TTH,
                                       tightLeptonSel = tightLeptonSel,
                                       FOTauSel = foTauSel,
                                       tightTauSel = tightTauSel,
                                       selectJet = lambda jet: abs(jet.eta)<2.4 and jet.pt > 25 and jet.jetId > 0, # FIXME need to select on pt or ptUp or ptDown
                                       coneptdef = lambda lep: conept_TTH(lep))
recleaner_step2_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                       cleanTausWithLooseLeptons=True,
                                       cleanJetsWithFOTaus=True,
                                       doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                       jetPts=[25,40],
                                       btagL_thr=0.1522,
                                       btagM_thr=0.4941,
                                       isMC = True)
recleaner_step2_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                         cleanTausWithLooseLeptons=True,
                                         cleanJetsWithFOTaus=True,
                                         doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                         jetPts=[25,40],
                                         btagL_thr=0.1522,
                                         btagM_thr=0.4941,
                                         isMC = False)

from CMGTools.TTHAnalysis.tools.eventVars_2lss import EventVars2LSS
eventVars = lambda : EventVars2LSS('','Recl', doSystJEC=False)

from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import jetmetUncertainties2016, jetmetUncertainties2017, jetmetUncertainties2018
