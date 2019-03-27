from CMGTools.TTHAnalysis.tools.conept import conept_TTH
from CMGTools.TTHAnalysis.tools.functionsTTH import clean_and_FO_selection_TTH

MODULES=[]
from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.TTHAnalysis.tools.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner

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
                                                                                           doFwdJets=True,
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
                                                                                             doFwdJets=True,
                                                                                             isMC = False) ))
