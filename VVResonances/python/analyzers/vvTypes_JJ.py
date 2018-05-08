from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
import ROOT
dummyLV=ROOT.math.XYZTLorentzVector(0.0,0.0,0.0001,0.0001)

FatJetType = NTupleObjectType("FatJetType", baseObjectTypes=[jetTypeID], variables = [
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
    # NTupleSubObject("l2_softDrop",  lambda x : x.leg2.substructure.softDropJet,fourVectorType),
    NTupleVariable("l2_softDrop_pt", lambda x: x.leg2.substructure.softDropJet.pt(), float),
    NTupleVariable("l2_softDrop_eta", lambda x: x.leg2.substructure.softDropJet.eta(), float),
    NTupleVariable("l2_softDrop_phi", lambda x: x.leg2.substructure.softDropJet.phi(), float),
    NTupleVariable("l2_softDrop_mass", lambda x: x.leg2.substructure.softDropJetMassBare*x.leg2.substructure.softDropJetMassCor, float),
    NTupleSubObject("l2_pruned",  lambda x : x.leg2.substructure.prunedJet,fourVectorType),
    NTupleVariable("l2_softDrop_massCorr",  lambda x : x.leg2.substructure.softDropJetMassCor,float),
    NTupleVariable("l2_softDrop_massBare",  lambda x : x.leg2.substructure.softDropJetMassBare,float),
    NTupleVariable("l2_softDrop_massL2L3",  lambda x : x.leg2.substructure.softDropJetMassL2L3,float),
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

JJType = NTupleObjectType("JJType", baseObjectTypes=[VJType], variables = [


    NTupleSubObject("l1",  lambda x : x.leg1,FatJetType),
    # NTupleSubObject("l1_softDrop",  lambda x : x.leg1.substructure.softDropJet,fourVectorType),
    NTupleVariable("l1_softDrop_pt", lambda x: x.leg1.substructure.softDropJet.pt(), float),
    NTupleVariable("l1_softDrop_eta", lambda x: x.leg1.substructure.softDropJet.eta(), float),
    NTupleVariable("l1_softDrop_phi", lambda x: x.leg1.substructure.softDropJet.phi(), float),
    NTupleVariable("l1_softDrop_mass", lambda x: x.leg1.substructure.softDropJetMassBare*x.leg1.substructure.softDropJetMassCor, float),
    NTupleSubObject("l1_pruned",  lambda x : x.leg1.substructure.prunedJet,fourVectorType),
    NTupleVariable("l1_softDrop_massCorr",  lambda x : x.leg1.substructure.softDropJetMassCor,float),
    NTupleVariable("l1_softDrop_massBare",  lambda x : x.leg1.substructure.softDropJetMassBare,float),
    NTupleVariable("l1_softDrop_massL2L3",  lambda x : x.leg1.substructure.softDropJetMassL2L3,float),
    NTupleVariable("l1_softDrop_nSubJets",  lambda x : len(x.leg1.substructure.softDropSubjets),int),
    NTupleSubObject("l1_softDrop_s1",  lambda x : x.leg1.substructure.softDropSubjets[0] if len(x.leg1.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_softDrop_s2",  lambda x : x.leg1.substructure.softDropSubjets[1] if len(x.leg1.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_pruned_s1",  lambda x : x.leg1.substructure.prunedSubjets[0] if len(x.leg1.substructure.prunedSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_pruned_s2",  lambda x : x.leg1.substructure.prunedSubjets[1] if len(x.leg1.substructure.prunedSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_gen",  lambda x : x.leg1.substructureGEN.jet if hasattr(x.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_gen_softDrop",  lambda x : x.leg1.substructureGEN.softDropJet if hasattr(x.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleSubObject("l1_gen_pruned",  lambda x : x.leg1.substructureGEN.prunedJet if hasattr(x.leg1,'substructureGEN') else dummyLV,fourVectorType,True),
    NTupleVariable("gen_partialMass",   lambda x : x.genPartialMass if (hasattr(x.leg2,'substructureGEN') and hasattr(x.leg1,'substructureGEN')) else -99, float,"",-99,True),

])
