from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import *
import ROOT
import math
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


def tau21DDT(x):
    mass = x.userFloat('ak8PFJetsPuppiSoftDropMass')
    tau1 = x.userFloat('NjettinessAK8Puppi:tau1')
    tau2 = x.userFloat('NjettinessAK8Puppi:tau2')
    pt = x.pt()
    if mass>0:
        return tau2/tau1+(0.082*math.log(mass*mass/pt))
    else: 
        return -999;


FatJetType = NTupleObjectType("FatJetType", baseObjectTypes=[jetType], variables = [
    NTupleVariable("tau1",   lambda x : x.userFloat('NjettinessAK8Puppi:tau1'), float),
    NTupleVariable("tau2",   lambda x : x.userFloat('NjettinessAK8Puppi:tau2'), float),
    NTupleVariable("tau3",   lambda x : x.userFloat('NjettinessAK8Puppi:tau3'), float),
    NTupleVariable("tau4",   lambda x : x.userFloat('NjettinessAK8Puppi:tau4'), float),
    NTupleVariable("N2b1",   lambda x : x.userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN2'), float),
    NTupleVariable("N2b2",   lambda x : x.userFloat('ak8PFJetsPuppiSoftDropValueMap:nb2AK8PuppiSoftDropN2'), float),
    NTupleVariable("N3b1",   lambda x : x.userFloat('ak8PFJetsPuppiSoftDropValueMap:nb1AK8PuppiSoftDropN3'), float),
    NTupleVariable("N3b2",   lambda x : x.userFloat('ak8PFJetsPuppiSoftDropValueMap:nb2AK8PuppiSoftDropN3'), float),
    NTupleVariable("tau21_DDT", lambda x : tau21DDT(x), float),
    NTupleVariable("s1BTag",   lambda x : x.subJetTags[0], float),
    NTupleVariable("s2BTag",   lambda x : x.subJetTags[1], float),
    # BTV-15-002: AK8 jets (w/ JEC applied, jetID applied, |eta| < 2.4, efficiency are computed by using pT > 300 GeV and pruned m_jet > 50 GeV)
    NTupleVariable("btagBOOSTED",   lambda x : x.btag("pfBoostedDoubleSecondaryVertexAK8BJetTags"), float),
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
    NTupleVariable("s1_subJetBTagWeight0", lambda x : x.subJet_btagWeights0[0], float,"",-99,True),
    NTupleVariable("s2_subjetBTagWeight0", lambda x : x.subJet_btagWeights0[1], float,"",-99,True),
    NTupleVariable("s1_subJetBTagWeight1", lambda x : x.subJet_btagWeights1[0], float,"",-99,True),
    NTupleVariable("s2_subjetBTagWeight1", lambda x : x.subJet_btagWeights1[1], float,"",-99,True),

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
    NTupleVariable("l2_softDrop_mass", lambda x: x.leg2.softDropMassCor, float),
    NTupleVariable("l2_softDrop_mass_low", lambda x: x.leg2.softDrop_low, float),
    NTupleVariable("l2_softDrop_mass_high", lambda x: x.leg2.softDrop_high, float),
    NTupleVariable("l2_softDrop_massBare", lambda x: x.leg2.softDropMassBare, float),
    NTupleVariable("btagWeight",  lambda x : x.btagWeight,float),
    NTupleVariable("gen_partialMass",   lambda x : x.genPartialMass, float,"",-99,True),
    ## GEN LEVEL STUFF
    NTupleSubObject("l2_gen",  lambda x : x.leg2.genJetP4 if hasattr(x.leg2,'genJetP4') else dummyLV,fourVectorType,True),
    NTupleVariable("l2_gen_softDrop_mass",  lambda x : x.leg2.genSoftDrop.mass(), float, mcOnly=True),
])



LNuJJType = NTupleObjectType("LNuJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("altLV",  lambda x : x.leg1.alternateLV+x.leg2.p4(),fourVectorType),
    NTupleSubObject("rawLV",  lambda x : x.leg1.rawP4()+x.leg2.p4(),fourVectorType),
    NTupleSubObject("l1",  lambda x : x.leg1,LNuType),
    NTupleSubObject("altl1",  lambda x : x.leg1.alternateLV,fourVectorType),
    NTupleSubObject("l1_l",  lambda x : x.leg1.leg1,leptonTypeExtra),
    NTupleVariable("l1_l_chargedHadronIsoRel", lambda x: x.leg1.leg1.chargedHadronIso()/x.leg1.leg1.pt(), float),
    NTupleSubObject("l1_met",  lambda x : x.leg1.leg2,metType),
    #Scale factors , For HLT use the OR between the two triggers:
    NTupleVariable("sf",  lambda x : x.leg1.leg1.sfWV*(x.leg1.leg1.eff_HLT_DATA+x.eff_HLTMET_DATA-x.leg1.leg1.eff_HLT_DATA*x.eff_HLTMET_DATA)/(x.leg1.leg1.eff_HLT_MC+x.eff_HLTMET_MC-x.leg1.leg1.eff_HLT_MC*x.eff_HLTMET_MC),float),
    NTupleVariable("sfWV",  lambda x : x.leg1.leg1.sfWV, float),
#    NTupleVariable("sfHLT",  lambda x : x.leg1.leg1.sfHLT, float),
#    NTupleVariable("sfHLTMET",  lambda x : x.sfHLTMET, float)
])


LLJJType = NTupleObjectType("LLJJType", baseObjectTypes=[VJType], variables = [
    NTupleSubObject("l1",  lambda x : x.leg1,LLType),
    NTupleSubObject("l1_l1",  lambda x : x.leg1.leg1,leptonTypeExtra),
    NTupleSubObject("l1_l2",  lambda x : x.leg1.leg2,leptonTypeExtra),
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


