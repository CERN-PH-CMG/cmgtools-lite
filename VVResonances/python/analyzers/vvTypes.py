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
    NTupleVariable("massDropMu",   lambda x : x.substructure.massDrop[0], float),
    NTupleVariable("massDropY",   lambda x : x.substructure.massDrop[1], float),
    NTupleVariable("s1BTag",   lambda x : x.subJetTags[0], float),
    NTupleVariable("s2BTag",   lambda x : x.subJetTags[1], float),
    # BTV-15-002: AK8 jets (w/ JEC applied, jetID applied, |eta| < 2.4, efficiency are computed by using pT > 300 GeV and pruned m_jet > 50 GeV)
    NTupleVariable("btagBOOSTED",   lambda x : x.btag("pfBoostedDoubleSecondaryVertexAK8BJetTags"), float),
    NTupleVariable("btagBOOSTED_recalc", lambda x : x.Hbbtag if hasattr(x,'Hbbtag') else -1.0, float),
    NTupleVariable("s1CTagL",   lambda x : x.subJetCTagL[0], float),
    NTupleVariable("s2CTagL",   lambda x : x.subJetCTagL[1], float),
    NTupleVariable("s1CTagB",   lambda x : x.subJetCTagB[0], float),
    NTupleVariable("s2CTagB",   lambda x : x.subJetCTagB[1], float),
    NTupleVariable("s1_partonFlavour",   lambda x : x.subJet_partonFlavour[0], int,"",0,True),
    NTupleVariable("s1_hadronFlavour",   lambda x : x.subJet_hadronFlavour[0], int,"",0,True),
    NTupleVariable("s2_partonFlavour",   lambda x : x.subJet_partonFlavour[1], int,"",0,True),
    NTupleVariable("s2_hadronFlavour",   lambda x : x.subJet_hadronFlavour[1], int,"",0,True),
    NTupleVariable("mergedVTruth",   lambda x : x.mergedTrue, int,"",-1,True),
    NTupleVariable("nearestBDRTruth",   lambda x : x.nearestBDR, float,"",-99.0,True)
])



PyTauType = NTupleObjectType("PyTau", baseObjectTypes=[fourVectorType], variables = [
    NTupleVariable("nPions",   lambda x : x.nPions, int),
    NTupleVariable("nMuons", lambda x : x.nMuons, int),
    NTupleVariable("nPosMuons", lambda x : x.nPosMuons, int),
    NTupleVariable("nNegMuons", lambda x : x.nNegMuons, int),
    NTupleVariable("nElectrons", lambda x : x.nElectrons, int),
    NTupleVariable("nPosElectrons", lambda x : x.nPosElectrons, int),
    NTupleVariable("nNegElectrons", lambda x : x.nNegElectrons, int),

    NTupleVariable("nPhotons", lambda x : x.nPhotons, int),
    NTupleVariable("chargedIso", lambda x : x.chargedIso, float),
    NTupleVariable("photonIso", lambda x : x.photonIso, float),
    NTupleVariable("neutralIso", lambda x : x.neutralIso, float),
    NTupleVariable("decayMode", lambda x : x.decayMode, int),
    NTupleVariable("leadMuPt", lambda x : x.leadMuonPt, float),
    NTupleVariable("leadElePt", lambda x : x.leadElectronPt, float)

])


TauTauType = NTupleObjectType("TauTauType", baseObjectTypes=[], variables = [
  NTupleSubObject("LV",  lambda x : x.p4(),fourVectorType),
  NTupleSubObject("l1",   lambda x : x.leg1, PyTauType),
  NTupleSubObject("l1_t1",   lambda x : x.leg1.leg1, fourVectorType),
  NTupleSubObject("l1_t2",   lambda x : x.leg1.leg2, fourVectorType),
  NTupleSubObject("l2",   lambda x : x.leg2, PyTauType),
  NTupleSubObject("l2_t1",   lambda x : x.leg2.leg1, fourVectorType),
  NTupleSubObject("l2_t2",   lambda x : x.leg2.leg2, fourVectorType),

])

TauJetType = NTupleObjectType("TauJetType", baseObjectTypes=[], variables = [
  NTupleSubObject("LV",  lambda x : x.p4(),fourVectorType),
  NTupleSubObject("LVWithMET",  lambda x : x.LVWithMET,fourVectorType),
  NTupleSubObject("l1",   lambda x : x.leg1, PyTauType),
  NTupleSubObject("l1_t1",   lambda x : x.leg1.leg1, fourVectorType),
  NTupleSubObject("l1_t2",   lambda x : x.leg1.leg2, fourVectorType),
  NTupleSubObject("l2",   lambda x : x.leg2, jetType),
  NTupleSubObject("l2_pruned",   lambda x : x.leg2.substructure.prunedJet,fourVectorType),
  NTupleSubObject("l2_softDrop",  lambda x : x.leg2.substructure.softDropJet,fourVectorType)

])




VVType = NTupleObjectType("VVType", baseObjectTypes=[], variables = [
  NTupleSubObject("LV",  lambda x : x.p4(),fourVectorType),
  NTupleVariable("deltaPhi",   lambda x : x.deltaPhi(), float),
  NTupleVariable("deltaR",   lambda x : x.deltaR(), float),
  NTupleVariable("mt",   lambda x : x.mt(), float),
  NTupleVariable("vbfDEta", lambda x : x.vbfDEta, float),
  NTupleVariable("vbfMass",   lambda x : x.vbfMass, float),
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
    NTupleVariable("l2_softDrop_massUp",  lambda x : x.leg2.substructure.softDropJetUp,float),
    NTupleVariable("l2_softDrop_massDown",  lambda x : x.leg2.substructure.softDropJetDown,float),
    NTupleVariable("l2_softDrop_massSmear",  lambda x : x.leg2.substructure.softDropJetSmear,float),
    NTupleVariable("l2_softDrop_massCorr",  lambda x : x.leg2.substructure.softDropJetMassCor,float),
    NTupleVariable("l2_softDrop_massBare",  lambda x : x.leg2.substructure.softDropJetMassBare,float),
    NTupleVariable("l2_softDrop_nSubJets",  lambda x : len(x.leg2.substructure.softDropSubjets),int),
    NTupleSubObject("l2_softDrop_s1",  lambda x : x.leg2.substructure.softDropSubjets[0] if len(x.leg2.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l2_softDrop_s2",  lambda x : x.leg2.substructure.softDropSubjets[1] if len(x.leg2.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l2_pruned_s1",  lambda x : x.leg2.substructure.prunedSubjets[0] if len(x.leg2.substructure.prunedSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l2_pruned_s2",  lambda x : x.leg2.substructure.prunedSubjets[1] if len(x.leg2.substructure.prunedSubjets)>1 else dummyLV,fourVectorType),
    NTupleVariable("btagWeight",  lambda x : x.btagWeight,float),

])



LNuJJType = NTupleObjectType("LNuJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("altLV",  lambda x : x.leg1.alternateLV+x.leg2.p4(),fourVectorType),
    NTupleSubObject("rawLV",  lambda x : x.leg1.rawP4()+x.leg2.p4(),fourVectorType),
    NTupleSubObject("l1",  lambda x : x.leg1,LNuType),
    NTupleSubObject("altl1",  lambda x : x.leg1.alternateLV,fourVectorType),
    NTupleSubObject("l1_l",  lambda x : x.leg1.leg1,leptonTypeExtra),
    NTupleSubObject("l1_met",  lambda x : x.leg1.leg2,metType),
    #Scale factors , For HLT use the OR between the two triggers:
    NTupleVariable("sf",  lambda x : x.leg1.leg1.sfWV*(x.leg1.leg1.sfHLT+x.sfHLTMET-x.leg1.leg1.sfHLT*x.sfHLTMET),float)



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
    NTupleVariable("l1_softDrop_massUp",  lambda x : x.leg1.substructure.softDropJetUp,float),
    NTupleVariable("l1_softDrop_massDown",  lambda x : x.leg1.substructure.softDropJetDown,float),
    NTupleVariable("l1_softDrop_massSmear",  lambda x : x.leg1.substructure.softDropJetSmear,float),
    NTupleVariable("l1_softDrop_massCorr",  lambda x : x.leg1.substructure.softDropJetMassCor,float),
    NTupleVariable("l1_softDrop_massBare",  lambda x : x.leg1.substructure.softDropJetMassBare,float),
    NTupleVariable("l1_softDrop_nSubJets",  lambda x : len(x.leg1.substructure.softDropSubjets),int),
    NTupleSubObject("l1_softDrop_s1",  lambda x : x.leg1.substructure.softDropSubjets[0] if len(x.leg1.substructure.softDropSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_softDrop_s2",  lambda x : x.leg1.substructure.softDropSubjets[1] if len(x.leg1.substructure.softDropSubjets)>1 else dummyLV,fourVectorType),
    NTupleSubObject("l1_pruned_s1",  lambda x : x.leg1.substructure.prunedSubjets[0] if len(x.leg1.substructure.prunedSubjets)>0 else dummyLV,fourVectorType),
    NTupleSubObject("l1_pruned_s2",  lambda x : x.leg1.substructure.prunedSubjets[1] if len(x.leg1.substructure.prunedSubjets)>1 else dummyLV,fourVectorType),


])



NuNuJJType = NTupleObjectType("NuNuJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("l1",  lambda x : x.leg1,metType)
])
