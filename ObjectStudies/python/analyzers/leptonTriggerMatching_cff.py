import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.Heppy.analyzers.core.TriggerMatchAnalyzer import TriggerMatchAnalyzer
from PhysicsTools.Heppy.analyzers.core.AutoFillTreeProducer  import * 

_MuPathTemplate = cfg.Analyzer(TriggerMatchAnalyzer, 
    processName = 'PAT',
    fallbackProcessName = 'RECO',
    unpackPathNames = True,
    collToMatch = 'selectedLeptons',
    collMatchSelectors = [ lambda l,t : abs(l.pdgId()) == 13 ],
    collMatchDRCut = 0.2,
    univoqueMatching = True,
    verbose = False,
)
_MuFilterTemplate = _MuPathTemplate.clone(unpackPathNames = False)
_ElPathTemplate   = _MuPathTemplate.clone(collMatchSelectors = [ lambda l,t : abs(l.pdgId()) == 11 ])
_ElFilterTemplate = _ElPathTemplate.clone(unpackPathNames = False)

allTriggerMatchers = {}
def defineMatcher(template, label, selector):
    if label in allTriggerMatchers: raise RuntimeError, "Duplicate definition of "+label
    module = template.clone(
        name = "trigMatcher"+label, label = label,
        trgObjSelectors = [ selector ]
    )
    allTriggerMatchers[label] = module

# Singles Muons (unprescaled)
defineMatcher(_MuPathTemplate, "IsoMu20orIsoTkMu20",  lambda t : t.path("HLT_IsoMu20_v*",1,0) or t.path("HLT_IsoTkMu20_v*",1,0))
defineMatcher(_MuPathTemplate, "IsoMu22orIsoTkMu22",  lambda t : t.path("HLT_IsoMu22_v*",1,0) or t.path("HLT_IsoTkMu22_v*",1,0))
defineMatcher(_MuPathTemplate, "Mu50orTkMu50",  lambda t : t.path("HLT_Mu50_v*",1,0) or t.path("HLT_TkMu50_v*",1,0))

## Singles Muons (prescaled)
defineMatcher(_MuPathTemplate, "Mu17TrkIso",  lambda t : t.path("HLT_Mu17_TrkIsoVVL_*",1,0))
defineMatcher(_MuPathTemplate, "Mu8TrkIso",  lambda t : t.path("HLT_Mu8_TrkIsoVVL_*",1,0))
defineMatcher(_MuPathTemplate, "Mu17",  lambda t : t.path("HLT_Mu17_v*",1,0))
defineMatcher(_MuPathTemplate, "Mu8",  lambda t : t.path("HLT_Mu8_v*",1,0))

# Double Muons
defineMatcher(_MuFilterTemplate, "Mu17Mu8TrkIso_Mu17Leg",
                    lambda t : t.filter("hltL3fL1sDoubleMu114L1f0L2f10OneMuL3Filtered17") and t.filter("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4") )
defineMatcher(_MuFilterTemplate, "Mu17Mu8TrkIso_Mu8Leg",
                     lambda t : t.filter("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4") )
defineMatcher(_MuFilterTemplate, "Mu17Mu8TrkIso_DZ",
                     lambda t : t.filter("hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2") )
defineMatcher(_MuFilterTemplate, "Mu17TkMu8TrkIso_Mu17Leg",
                    lambda t : t.filter("DoubleMu114L1f0L2f10L3Filtered17") and t.filter("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4") )
defineMatcher(_MuFilterTemplate, "Mu17TkMu8TrkIso_TkMu8Leg",
                     lambda t : t.filter("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4") )
defineMatcher(_MuFilterTemplate, "Mu17TkMu8TrkIso_DZ",
                     lambda t : t.filter("hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2") )

# TripleMuons
defineMatcher(_MuFilterTemplate, "TriMu12105_Mu12Leg", lambda t : t.filter("hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered12105"))
defineMatcher(_MuFilterTemplate, "TriMu12105_Mu10Leg", lambda t : t.filter("hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered10105"))
defineMatcher(_MuFilterTemplate, "TriMu12105_Mu5Leg",  lambda t : t.filter("hltL1TripleMu553L2TriMuFiltered3L3TriMuFiltered5"))
defineMatcher(_MuFilterTemplate, "TriMu533_Mu5Leg",  lambda t : t.filter("hltL1TripleMu0L2TriMuFiltered0L3TriMuFiltered3"))
defineMatcher(_MuFilterTemplate, "TriMu533_Mu3Leg",  lambda t : t.filter("hltL1TripleMu0L2TriMuFiltered0L3TriMuFiltered533"))

# SingleElectron
#defineMatcher(_ElPathTemplate, "Ele27Loose",  lambda t : t.path("HLT_Ele27_WPLoose_Gsf_v*",1,0))
defineMatcher(_ElPathTemplate, "Ele27Tight",  lambda t : t.path("HLT_Ele27_WPTight_Gsf_v*",1,0))
defineMatcher(_ElPathTemplate, "Ele27erLoose",  lambda t : t.path("HLT_Ele27_eta2p1_WPLoose_Gsf_v*",1,0))
defineMatcher(_ElPathTemplate, "Ele25Tight",  lambda t : t.path("HLT_Ele25_WPTight_Gsf_v*",1,0))
defineMatcher(_ElPathTemplate, "Ele25erTight",  lambda t : t.path("HLT_Ele25_eta2p1_WPTight_Gsf_v*",1,0))
defineMatcher(_ElPathTemplate, "Ele25erLoose",  lambda t : t.path("HLT_Ele25_eta2p1_WPLoose_Gsf_v*",1,0))

# DoubleElectron
defineMatcher(_ElFilterTemplate, "Ele17Ele12_Ele17Leg", lambda t : t.filter("hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter") )
defineMatcher(_ElFilterTemplate, "Ele17Ele12_Ele8Leg",  lambda t : t.filter("hltEle17Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter") )
defineMatcher(_ElFilterTemplate, "Ele17Ele12_DZ",       lambda t : t.filter("hltEle17Ele12CaloIdLTrackIdLIsoVLDZFilter") )
defineMatcher(_ElFilterTemplate, "Ele23Ele12_Ele23Leg", lambda t : t.filter("hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg1Filter") )
defineMatcher(_ElFilterTemplate, "Ele23Ele12_Ele12Leg", lambda t : t.filter("hltEle23Ele12CaloIdLTrackIdLIsoVLTrackIsoLeg2Filter") )
defineMatcher(_ElFilterTemplate, "Ele23Ele12_DZ",       lambda t : t.filter("hltEle23Ele12CaloIdLTrackIdLIsoVLDZFilter") )

# TripleElectron
defineMatcher(_ElFilterTemplate, "El16128_El16Leg", lambda t : t.filter("hltEle16Ele12Ele8CaloIdLTrackIdLDphiLeg1Filter") )
defineMatcher(_ElFilterTemplate, "El16128_El12Leg", lambda t : t.filter("hltEle16Ele12Ele8CaloIdLTrackIdLDphiLeg2Filter") )
defineMatcher(_ElFilterTemplate, "El16128_El8Leg",  lambda t : t.filter("hltEle16Ele12Ele8CaloIdLTrackIdLDphiLeg3Filter") )

# MuEG: ele
defineMatcher(_ElFilterTemplate, "Mu17Ele12_Ele12", lambda t : t.filter("hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter") )
defineMatcher(_ElFilterTemplate, "Mu23Ele12_Ele12", lambda t : t.filter("hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter") )
defineMatcher(_ElFilterTemplate, "Mu23Ele8_Ele8",   lambda t : t.filter("hltMu23TrkIsoVVLEle8CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter") )
defineMatcher(_ElFilterTemplate, "Mu8Ele17_Ele17",  lambda t : t.filter("hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter") )
defineMatcher(_ElFilterTemplate, "Mu8Ele23_Ele23",  lambda t : t.filter("hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter") )
# MuEG: mu
defineMatcher(_MuFilterTemplate, "Mu17Ele12_Mu17", lambda t : t.filter("hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered17") )
defineMatcher(_MuFilterTemplate, "Mu23Ele12_Mu23", lambda t : t.filter("hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23") )
defineMatcher(_MuFilterTemplate, "Mu23Ele8_Mu23",  lambda t : t.filter("hltMu23TrkIsoVVLEle8CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23") )
defineMatcher(_MuFilterTemplate, "Mu8Ele17_Mu8",   lambda t : t.filter("hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8") )
defineMatcher(_MuFilterTemplate, "Mu8Ele23_Mu8",   lambda t : t.filter("hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8") )

# Define a Sequence and a Mixin Type
LeptonTriggerMatchersSequence = allTriggerMatchers.values()
WithLeptonTriggerMatchType = NTupleObjectType("withLeptonTriggerMatchType", baseObjectTypes = [], variables = [
    NTupleVariable(k, eval("lambda x : getattr(x, 'matchedTrgObj%s', None) != None" % k), int, help = 'TriggerMatching: '+k) for k in allTriggerMatchers.keys()
])

