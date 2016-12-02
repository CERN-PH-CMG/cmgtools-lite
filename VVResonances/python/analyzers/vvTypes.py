from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
import ROOT
dummyLV=ROOT.math.XYZTLorentzVector(0.0,0.0,0.0001,0.0001)


LNuType = NTupleObjectType("LNuType", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("mt",   lambda x : x.mt(), float),
    NTupleVariable("deltaPhi",   lambda x : x.deltaPhi(), float),
])



LLType = NTupleObjectType("LLType", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("mt",   lambda x : x.mt(), float),
    NTupleVariable("deltaPhi",   lambda x : x.deltaPhi(), float),
    NTupleVariable("deltaR",   lambda x : x.deltaR(), float),
])


FatJetType = NTupleObjectType("FatJetType", baseObjectTypes=[jetType], variables = [
    NTupleVariable("tau1",   lambda x : x.substructure.ntau[0], float),
    NTupleVariable("tau2",   lambda x : x.substructure.ntau[1], float),
    NTupleVariable("tau3",   lambda x : x.substructure.ntau[2], float),
    NTupleVariable("tau4",   lambda x : x.substructure.ntau[3], float),
    NTupleVariable("tau21_DDT",   lambda x : x.substructure.tau21_DDT, float),
    NTupleVariable("s1BTag",   lambda x : x.subJetTags[0], float),
    NTupleVariable("s2BTag",   lambda x : x.subJetTags[1], float),
    # BTV-15-002: AK8 jets (w/ JEC applied, jetID applied, |eta| < 2.4, efficiency are computed by using pT > 300 GeV and pruned m_jet > 50 GeV)
    NTupleVariable("btagBOOSTED",   lambda x : x.btag("pfBoostedDoubleSecondaryVertexAK8BJetTags"), float),
    NTupleVariable("btagBOOSTED_recalc", lambda x : x.Hbbtag if hasattr(x,'Hbbtag') else -1.0, float),
    NTupleVariable("s1CTagL",   lambda x : x.subJetCTagL[0], float),
    NTupleVariable("s2CTagL",   lambda x : x.subJetCTagL[1], float),
    NTupleVariable("s1CTagB",   lambda x : x.subJetCTagB[0], float),
    NTupleVariable("s2CTagB",   lambda x : x.subJetCTagB[1], float),
    NTupleVariable("s1_partonFlavour",   lambda x : x.subJet_partonFlavour[0], int,"",-99,True),
    NTupleVariable("s1_hadronFlavour",   lambda x : x.subJet_hadronFlavour[0], int,"",-99,True),
    NTupleVariable("s2_partonFlavour",   lambda x : x.subJet_partonFlavour[1], int,"",-99,True),
    NTupleVariable("s2_hadronFlavour",   lambda x : x.subJet_hadronFlavour[1], int,"",-99,True),
    NTupleVariable("mergedVTruth",   lambda x : x.mergedTrue, int,"",-1,True),
    NTupleVariable("nearestBDRTruth",   lambda x : x.nearestBDR, float,"",-99.0,True),

    ######GEN SUBSTRUCTURE INFO
    NTupleVariable("gen_tau1",   lambda x : x.substructureGEN.ntau[0] if hasattr(x,'substructureGEN') else -99, float,"",-99,True),
    NTupleVariable("gen_tau2",   lambda x : x.substructureGEN.ntau[1] if hasattr(x,'substructureGEN') else -99, float,"",-99,True),
    NTupleVariable("gen_tau3",   lambda x : x.substructureGEN.ntau[2] if hasattr(x,'substructureGEN') else -99, float,"",-99,True),
    NTupleVariable("gen_tau4",   lambda x : x.substructureGEN.ntau[3] if hasattr(x,'substructureGEN') else -99, float,"",-99,True),



])


VVType = NTupleObjectType("VVType", baseObjectTypes=[], variables = [
  NTupleSubObject("LV",  lambda x : x.p4(),fourVectorType),
  NTupleVariable("deltaPhi",   lambda x : x.deltaPhi(), float),
  NTupleVariable("deltaR",   lambda x : x.deltaR(), float),
  NTupleVariable("mt",   lambda x : x.mt(), float),
  NTupleVariable("vbfDEta", lambda x : x.vbfDEta, float),
  NTupleVariable("vbfMass",   lambda x : x.vbfMass, float),
  NTupleSubObject("vbf_j1", lambda x : x.satteliteJets[0] if len(x.satteliteJets)>0 else None, jetType, nillable=True),
  NTupleSubObject("vbf_j2", lambda x : x.satteliteJets[1] if len(x.satteliteJets)>1 else None, jetType, nillable=True),
  NTupleVariable("nJets",   lambda x : len(x.satteliteJets), int),
  NTupleVariable("nCentralJets",   lambda x : len(x.satteliteCentralJets), int),
  NTupleVariable("nLooseBTags",   lambda x : x.nLooseBTags, int),
  NTupleVariable("nMediumBTags",   lambda x : x.nMediumBTags, int),
  NTupleVariable("nTightBTags",   lambda x : x.nTightBTags, int),
  NTupleVariable("nOtherLeptons",   lambda x : x.nOtherLeptons, int),
  NTupleVariable("highestOtherBTag",   lambda x : x.highestEventBTag, float),

])


VJType = NTupleObjectType("VJType", baseObjectTypes=[VVType], variables = [
    NTupleSubObject("l2",  lambda x : x.leg2,FatJetType),
    NTupleSubObject("l2_softDrop",  lambda x : x.leg2.substructure.softDropJet,fourVectorType),
    NTupleSubObject("l2_pruned",  lambda x : x.leg2.substructure.prunedJet,fourVectorType),
    NTupleVariable("l2_softDrop_massCorr",  lambda x : x.leg2.substructure.softDropJetMassCor,float),
    NTupleVariable("l2_softDrop_massBare",  lambda x : x.leg2.substructure.softDropJetMassBare,float),
    NTupleVariable("l2_softDrop_nSubJets",  lambda x : len(x.leg2.substructure.softDropSubjets),int),
    NTupleSubObject("l2_softDrop_s1",  lambda x : x.leg2.substructure.softDropSubjets[0] if len(x.leg2.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l2_softDrop_s2",  lambda x : x.leg2.substructure.softDropSubjets[1] if len(x.leg2.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l2_pruned_s1",  lambda x : x.leg2.substructure.prunedSubjets[0] if len(x.leg2.substructure.prunedSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l2_pruned_s2",  lambda x : x.leg2.substructure.prunedSubjets[1] if len(x.leg2.substructure.prunedSubjets)>1 else dummyLV,fourVectorType),
    NTupleVariable("btagWeight",  lambda x : x.btagWeight,float),

    ## GEN LEVEL STUFF
    NTupleSubObject("l2_gen",  lambda x : x.leg2.substructureGEN.jet if hasattr(x.leg2,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l2_gen_softDrop",  lambda x : x.leg2.substructureGEN.softDropJet if hasattr(x.leg2,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l2_gen_pruned",  lambda x : x.leg2.substructureGEN.prunedJet if hasattr(x.leg2,'substructureGEN') else dummyLV,fourVectorType,True),
])



LNuJJType = NTupleObjectType("LNuJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("altLV",  lambda x : x.leg1.alternateLV+x.leg2.p4(),fourVectorType),
    NTupleSubObject("rawLV",  lambda x : x.leg1.rawP4()+x.leg2.p4(),fourVectorType),
    NTupleSubObject("l1",  lambda x : x.leg1,LNuType),
    NTupleSubObject("altl1",  lambda x : x.leg1.alternateLV,fourVectorType),
    NTupleSubObject("l1_l",  lambda x : x.leg1.leg1,leptonTypeExtra),
    NTupleSubObject("l1_met",  lambda x : x.leg1.leg2,metType),
    #Scale factors , For HLT use the OR between the two triggers:
    NTupleVariable("gen_partialMass",   lambda x : x.genPartialMass if hasattr(x.leg2,'substructureGEN') else -99, float,"",-99,True),
    NTupleVariable("sf",  lambda x : x.leg1.leg1.sfWV*(x.leg1.leg1.sfHLT+x.sfHLTMET-x.leg1.leg1.sfHLT*x.sfHLTMET),float),
    NTupleVariable("sfWV",  lambda x : x.leg1.leg1.sfWV, float),
    NTupleVariable("sfHLT",  lambda x : x.leg1.leg1.sfHLT, float),
    NTupleVariable("sfHLTMET",  lambda x : x.sfHLTMET, float)
])


LLJJType = NTupleObjectType("LLJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("l1",  lambda x : x.leg1,LLType),
    NTupleSubObject("l1_l1",  lambda x : x.leg1.leg1,leptonTypeExtra),
    NTupleSubObject("l1_l2",  lambda x : x.leg1.leg2,leptonTypeExtra),
])



JJType = NTupleObjectType("JJType", baseObjectTypes=[VJType], variables = [


    NTupleSubObject("l1",  lambda x : x.leg1,FatJetType),
    NTupleSubObject("l1_softDrop",  lambda x : x.leg1.substructure.softDropJet,fourVectorType),
    NTupleSubObject("l1_pruned",  lambda x : x.leg1.substructure.prunedJet,fourVectorType),
    NTupleVariable("l1_softDrop_massCorr",  lambda x : x.leg1.substructure.softDropJetMassCor,float),
    NTupleVariable("l1_softDrop_massBare",  lambda x : x.leg1.substructure.softDropJetMassBare,float),
    NTupleVariable("l1_softDrop_nSubJets",  lambda x : len(x.leg1.substructure.softDropSubjets),int),
    NTupleSubObject("l1_softDrop_s1",  lambda x : x.leg1.substructure.softDropSubjets[0] if len(x.leg1.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_softDrop_s2",  lambda x : x.leg1.substructure.softDropSubjets[1] if len(x.leg1.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_pruned_s1",  lambda x : x.leg1.substructure.prunedSubjets[0] if len(x.leg1.substructure.prunedSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_pruned_s2",  lambda x : x.leg1.substructure.prunedSubjets[1] if len(x.leg1.substructure.prunedSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_gen",  lambda x : x.leg1.substructureGEN.jet if hasattr(x.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_gen_softDrop",  lambda x : x.leg1.substructureGEN.softDropJet if hasattr(x.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_gen_pruned",  lambda x : x.leg1.substructureGEN.prunedJet if hasattr(x.leg1,'substructureGEN') else dummyLV,fourVectorType,True),

])



NuNuJJType = NTupleObjectType("NuNuJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("l1",  lambda x : x.leg1,metType)
])


TruthType = NTupleObjectType("TruthType", baseObjectTypes=[], variables = [
    NTupleSubObject("genBoson", lambda x: x.genBoson if hasattr(x, 'genBoson') else dummyLV, fourVectorType, True),
    NTupleVariable("genTop_weight", lambda x: x.genTop_weight if hasattr(x, 'genTop_weight') else 1., float, "" , 1., True),
    NTupleVariable("genTop_1_pt", lambda x: x.genTop_1_pt if hasattr(x, 'genTop_1_pt') else -99, float, "" , -99, True),
    NTupleVariable("genTop_2_pt", lambda x: x.genTop_2_pt if hasattr(x, 'genTop_2_pt') else -99, float, "" , -99, True),
])


#Types for TTbar
WbJJType = NTupleObjectType("WbJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("l1",  lambda x : x.leg1,fourVectorType),
    NTupleSubObject("l1_Wjet",  lambda x : x.leg1.leg1,FatJetType),
    NTupleSubObject("l1_Wjet_softDrop",  lambda x : x.leg1.leg1.substructure.softDropJet,fourVectorType),
    NTupleSubObject("l1_Wjet_softDrop_s1",  lambda x : x.leg1.leg1.substructure.softDropSubjets[0] if len(x.leg1.leg1.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_Wjet_softDrop_s2",  lambda x : x.leg1.leg1.substructure.softDropSubjets[1] if len(x.leg1.leg1.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_Wjet_gen",  lambda x : x.leg1.leg1.substructureGEN.jet if hasattr(x.leg1.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_Wjet_gen_softDrop",  lambda x : x.leg1.leg1.substructureGEN.softDropJet if hasattr(x.leg1.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_bjet",  lambda x : x.leg1.leg2,jetType),
])

WbWbType = NTupleObjectType("WbWbType", baseObjectTypes=[VVType], variables = [
    NTupleSubObject("l1",  lambda x : x.leg1,fourVectorType),
    NTupleSubObject("l1_Wjet",  lambda x : x.leg1.leg1,FatJetType),
    NTupleSubObject("l1_Wjet_softDrop",  lambda x : x.leg1.leg1.substructure.softDropJet,fourVectorType),
    NTupleSubObject("l1_Wjet_softDrop_s1",  lambda x : x.leg1.leg1.substructure.softDropSubjets[0] if len(x.leg1.leg1.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_Wjet_softDrop_s2",  lambda x : x.leg1.leg1.substructure.softDropSubjets[1] if len(x.leg1.leg1.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_Wjet_gen",  lambda x : x.leg1.leg1.substructureGEN.jet if hasattr(x.leg1.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_Wjet_gen_softDrop",  lambda x : x.leg1.leg1.substructureGEN.softDropJet if hasattr(x.leg1.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_bjet",  lambda x : x.leg1.leg2,jetType),

    NTupleSubObject("l2",  lambda x : x.leg2,fourVectorType),
    NTupleSubObject("l2_Wjet",  lambda x : x.leg2.leg1,FatJetType),
    NTupleSubObject("l2_Wjet_softDrop",  lambda x : x.leg2.leg1.substructure.softDropJet,fourVectorType),
    NTupleSubObject("l2_Wjet_softDrop_s1",  lambda x : x.leg2.leg1.substructure.softDropSubjets[0] if len(x.leg2.leg1.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l2_Wjet_softDrop_s2",  lambda x : x.leg2.leg1.substructure.softDropSubjets[1] if len(x.leg2.leg1.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l2_Wjet_gen",  lambda x : x.leg2.leg1.substructureGEN.jet if hasattr(x.leg2.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l2_Wjet_gen_softDrop",  lambda x : x.leg2.leg1.substructureGEN.softDropJet if hasattr(x.leg2.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l2_bjet",  lambda x : x.leg2.leg2,jetType),

])
