from CMGTools.TTHAnalysis.treeReAnalyzer import *

def conept_RA5(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13):
        return lep.pt
    A = 0.12 if (abs(lep.pdgId)==11) else 0.16
    B = 0.80 if (abs(lep.pdgId)==11) else 0.76
    C = 7.2 if (abs(lep.pdgId)==11) else 7.2
    if (lep.jetPtRelv2>C):
        return lep.pt*(1+max(lep.miniRelIso-A,0))
    else:
        return max(lep.pt,lep.pt/lep.jetPtRatiov2*B)

def conept_RA7(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13):
        return lep.pt
    A = 0.16 if (abs(lep.pdgId)==11) else 0.20
    B = 0.76 if (abs(lep.pdgId)==11) else 0.69
    C = 7.2 if (abs(lep.pdgId)==11) else 6.0
    if (lep.jetPtRelv2>C):
        return lep.pt*(1+max(lep.miniRelIso-A,0))
    else:
        return max(lep.pt,lep.pt/lep.jetPtRatiov2*B)

def conept_SSDL(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)!=13 or lep.mediumMuonId>0) and lep.mvaTTH > 0.75: return lep.pt
    else: return 0.85 * lep.pt / lep.jetPtRatiov2

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)!=13 or lep.mediumMuonId>0) and lep.mvaTTH > 0.75: return lep.pt
    else: return 0.85 * lep.pt / lep.jetPtRatiov2

from CMGTools.TTHAnalysis.analyzers.ntupleTypes import jetLepAwareJEC
def conept_TTH_production(lep):
    if (abs(lep.pdgId())!=11 and abs(lep.pdgId())!=13): return lep.pt()
    if (abs(lep.pdgId())!=13 or lep.muonID("POG_ID_Medium")>0) and getattr(lep, 'mvaValueTTH', -1) > 0.75: return lep.pt()
    else: return 0.85*jetLepAwareJEC(lep).Pt() if hasattr(lep,'jet') else -1

