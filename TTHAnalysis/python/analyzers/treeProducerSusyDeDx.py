#!/bin/env python
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer import *  
from PhysicsTools.Heppy.analyzers.core.autovars import *  
from PhysicsTools.Heppy.analyzers.objects.autophobj import  *
from math import *

##------------------------------------------  
## LEPTON
##------------------------------------------  

leptonTypeSusy = NTupleObjectType("leptonSusy", baseObjectTypes = [ leptonType ], variables = [
    NTupleVariable("mvaIdFall17noIso",   lambda lepton : lepton.mvaRun2("Fall17noIso") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Fall17 training, without isolation; 1 for muons"),
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -100, help="Electron supercluster pseudorapidity"),
    # More: MC
    NTupleVariable("mcMatchPdgId",  lambda x : x.mcLep.pdgId() if getattr(x,'mcLep',None)!=None else -99, int, mcOnly=True, help="Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z): pdgId of the matched gen-level lepton, zero if non-prompt or fake"),
    NTupleVariable("mcPromptGamma", lambda x : x.mcPho.isPromptFinalState() if getattr(x,"mcPho",None) else 0, int, mcOnly=True, help="Photon isPromptFinalState"),
])
leptonTypeSusy.removeVariable("relIsoAn04")
leptonTypeSusy.removeVariable("eleCutIdSpring15_25ns_v1")
leptonTypeSusy.removeVariable("ICHEPsoftMuonId")
leptonTypeSusy.removeVariable("ICHEPmediumMuonId")

##------------------------------------------  
## TAU
##------------------------------------------  

tauTypeSusy = NTupleObjectType("tauSusy",  baseObjectTypes = [ tauType ], variables = [
     NTupleVariable("idMVAdR03", lambda x : x.idMVAdR03, int, help="1,2,3,4,5,6 if the tau passes the very loose to very very tight WP of the IsolationMVArun2v1DBdR03oldDMwLT discriminator"),
])
tauTypeSusy.removeVariable("idMVANewDM")
tauTypeSusy.removeVariable("idCI3hit")


jetTypeSusy = NTupleObjectType("jetSusy",  baseObjectTypes = [ jetTypeExtra ], variables = [
#   NTupleVariable("charge", lambda x : x.jetCharge(), float, help="Jet charge"), 
#    NTupleVariable("btagDeepCSVCvsB", lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probc')/(x.btag('pfDeepCSVJetTags:probc')+x.btag('pfDeepCSVJetTags:probb')+x.btag('pfDeepCSVJetTags:probbb'))), help="DeepCSV discriminator, CvsB = c/(c+b+bb)"),
#    NTupleVariable("btagDeepCSVCvsL", lambda x : (lambda y : -99 if isnan(y) else y)(x.btag('pfDeepCSVJetTags:probc')/(x.btag('pfDeepCSVJetTags:probc')+x.btag('pfDeepCSVJetTags:probudsg'))), help="DeepCSV discriminator, CvsL = c/(c+udsg)"),
#    NTupleVariable("ctagCsvL", lambda x : x.btag('pfCombinedCvsLJetTags'), float, help="CsvL discriminator"),
#    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
#    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
])
jetTypeSusy.removeVariable("btagCMVA")
jetTypeSusy.removeVariable("nLeptons")

jetTypeSusyFwd = NTupleObjectType("jetFwd",  baseObjectTypes = [ jetType ], variables = [
#    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
#    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
])
jetTypeSusy.removeVariable("btagCMVA")
jetTypeSusyFwd.removeVariable("nLeptons")

##------------------------------------------  
## MET
##------------------------------------------  
  
metTypeSusy = NTupleObjectType("metSusy", baseObjectTypes = [ metType ], variables = [
])

##------------------------------------------  
## IsoTrackDeDx
##------------------------------------------  
isoTrackTypeDeDx = NTupleObjectType("isoTrackTypeDeDx", baseObjectTypes = [ particleType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("dxy",   lambda x : x.dxy(), help="d_{xy} with respect to PV, in cm (with sign)"),
    NTupleVariable("dz",    lambda x : x.dz() , help="d_{z} with respect to PV, in cm (with sign)"),
    NTupleVariable("edxy",  lambda x : x.dxyError(), help="#sigma(d_{xy}) with respect to PV, in cm"),
    NTupleVariable("edz", lambda x : x.dzError(), help="#sigma(d_{z}) with respect to PV, in cm"),    

    NTupleVariable("trackerLayers", lambda x : x.hitPattern().trackerLayersWithMeasurement(), int, help="Tracker Layers"),
    NTupleVariable("pixelLayers", lambda x : x.hitPattern().pixelLayersWithMeasurement(), int, help="Pixel Layers"),
    NTupleVariable("pixelHits", lambda x : x.hitPattern().numberOfValidPixelHits(), int, help="Pixel hits"),

    NTupleVariable("highPurity", lambda x : x.isHighPurityTrack(), int, help="High purity"),

    NTupleVariable("awayJet_idx", lambda x : x.leadAwayJet.index if x.leadAwayJet else -1, int),
    NTupleVariable("awayJet_pt", lambda x : x.leadAwayJet.pt() if x.leadAwayJet else 0),
    NTupleVariable("awayJet_dr", lambda x : deltaR(x, x.leadAwayJet) if x.leadAwayJet else 0),

    NTupleVariable("awayNJet", lambda x : x.awayJetInfo['num'], int),
    NTupleVariable("awayHTJet", lambda x : x.awayJetInfo['ht']),

    NTupleVariable("awayMu_idx", lambda x : x.leadAwayMu.index if x.leadAwayMu else -1, int),
    NTupleVariable("awayMu_dr", lambda x : deltaR(x, x.leadAwayMu) if x.leadAwayMu else 0),
    NTupleVariable("awayMu_mll", lambda x : (x.leadAwayMu.p4()+x.p4()).M() if x.leadAwayMu else 0),

    NTupleVariable("awayEle_idx", lambda x : x.leadAwayEle.index if x.leadAwayEle else -1, int),
    NTupleVariable("awayEle_dr", lambda x : deltaR(x, x.leadAwayEle) if x.leadAwayEle else 0),
    NTupleVariable("awayEle_mll", lambda x : (ROOT.reco.Candidate.p4(x.leadAwayEle)+x.p4()).M() if x.leadAwayEle else 0),

    NTupleVariable("closestMu_idx", lambda x : x.closestMu.index if x.closestMu else -1, int),
    NTupleVariable("closestEle_idx", lambda x : x.closestEle.index if x.closestEle else -1, int),
    NTupleVariable("closestTau_idx", lambda x : x.closestTau.index if x.closestTau else -1, int),

    NTupleVariable("myDeDx", lambda x : x.myDeDx),

    NTupleVariable("mcMatch", lambda x : x.mcMatch.index if x.mcMatch else -1, int, mcOnly=True),
])

##------------------------------------------  
## genCharginoType
##------------------------------------------  
genCharginoType  = NTupleObjectType("genCharginoType", baseObjectTypes = [ genParticleWithMotherId ], variables = [
    NTupleVariable("beta", lambda x : x.p()/x.energy()),
    NTupleVariable("decayR", lambda x : x.decayPoint.R()),
    NTupleVariable("decayZ", lambda x : x.decayPoint.Z()),
])

## Tree Producer
treeProducer = cfg.Analyzer(
    AutoFillTreeProducer, name='treeProducerSusyDeDx',
    vectorTree = True, saveTLorentzVectors = False,  defaultFloatType = 'F', PDFWeights = [],
    globalVariables = [
        NTupleVariable("rho",  lambda ev: ev.rho, float, help="kt6PFJets rho"),
        NTupleVariable("nVert",  lambda ev: len(ev.goodVertices), int, help="Number of good vertices"),

        NTupleVariable("nJet30", lambda ev: sum([j.pt() > 30 for j in ev.cleanJets]), int, help="Number of jets with pt > 30, |eta|<2.4"),
        NTupleVariable("nJet30a", lambda ev: sum([j.pt() > 30 for j in ev.cleanJetsAll]), int, help="Number of jets with pt > 30, |eta|<4.7"),

        ## ------- lheHT, needed for merging HT binned samples
        NTupleVariable("lheHT", lambda ev : getattr(ev,"lheHT",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
        NTupleVariable("lheHTIncoming", lambda ev : getattr(ev,"lheHTIncoming",-999), mcOnly=True, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),
        ],
    globalObjects = {
        "met"         : NTupleObject("met", metTypeSusy, help="PF E_{T}^{miss}"),
        "met_jecUp"   : NTupleObject("met_jecUp", metTypeSusy, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
        "met_jecDown" : NTupleObject("met_jecDown", metTypeSusy, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
        },
    collections = {
        ##--------------------------------------------------
        "selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
        "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusy, 8, help="Leptons after the preselection"),
        ##------------------------------------------------
        "cleanJets"       : NTupleCollection("Jet",     jetTypeSusy, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
        "cleanJetsFwd"    : NTupleCollection("JetFwd",  jetTypeSusyFwd,  6, help="Forward jets after full selection and cleaning, sorted by pt"),
        ##------------------------------------------------
        "isoTracks"       : NTupleCollection("IsoTrack",  isoTrackTypeDeDx, 4, help="Isolated tracks"),
        ##------------------------------------------------
        "genCharginos"    : NTupleCollection("GenChargino",  genCharginoType, 4, mcOnly=True, help="Gen chargino"),
        },
    )

