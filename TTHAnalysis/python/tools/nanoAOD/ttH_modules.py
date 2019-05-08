conf = dict(
        muPt = 5, 
        elePt = 7, 
        miniRelIso = 0.4, 
        sip3d = 8, 
        dxy =  0.05, 
        dz = 0.1, 
        eleId = "mvaFall17V1noIso_WPL"
)

ttH_skim_cut = ("nMuon + nElectron >= 2 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf)


muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt" ] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and getattr(l, conf["eleId"])

from CMGTools.TTHAnalysis.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
lepSkim = ttHPrescalingLepSkimmer(5, 
                muonSel = muonSelection, electronSel = electronSelection,
                minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                minLeptons = 2, requireSameSignPair = True,
                jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4, 
                minJets = 4, minMET = 70)
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))

from CMGTools.TTHAnalysis.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.TTHAnalysis.tools.nanoAOD.yearTagger import yearTag
from CMGTools.TTHAnalysis.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV

ttH_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV]

# def clean_and_FO_selection_TTH(lep):
#     return lep.pt > 10 and lep.mvaTTH > 0.90
# 
# from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning 
# combinedTagger = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
#                                                        looseLeptonSel = lambda lep : True,
#                                                        cleaningLeptonSel = clean_and_FO_selection_TTH,
#                                                        FOLeptonSel = clean_and_FO_selection_TTH,
#                                                        tightLeptonSel = lambda lep : clean_and_FO_selection_TTH(lep) and lep.mvaTTH > 0.90,
#                                                        FOTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2,
#                                                        tightTauSel = lambda tau: tauID_oldDMdR0p3wLT2017v2_WP(tau.pt,tau.mvaId2017,2),
#                                                        selectJet = lambda jet: abs(jet.eta)<2.4,
#                                                        coneptdef = lambda lep: lep.pt) ))
# 
