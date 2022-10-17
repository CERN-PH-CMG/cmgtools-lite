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

def mvaEWKwp(lep, wp):
    # WP = 0,1,2,3,4,5 for VL,L,M,T,VT,ET
    if   wp == 0: WP = -0.9  if abs(lep.pdgId) == 13 else -0.3 ;
    elif wp == 1: WP = -0.6  if abs(lep.pdgId) == 13 else  0.25;
    elif wp == 2: WP = -0.2  if abs(lep.pdgId) == 13 else  0.5 ;
    elif wp == 3: WP =  0.15 if abs(lep.pdgId) == 13 else  0.65;
    elif wp == 4: WP =  0.45 if abs(lep.pdgId) == 13 else  0.75;
    elif wp == 5: WP =  0.65 if abs(lep.pdgId) == 13 else  0.85;
    else        : WP = -0.2  if abs(lep.pdgId) == 13 else  0.5 ;
    return WP

def conept_EWK(lep, wp = 2):
    # WP = 0,1,2,3,4,5 for VL,L,M,T,VT,ET
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13):
        return lep.pt
    WP = mvaEWKwp(lep, wp)
    if lep.pt > 10 and lep.mvaSUSY > WP and (abs(lep.pdgId) == 11 or lep.mediumMuonID2016 > 0): return lep.pt
    B = 0.85
    if   wp == 2: B = 0.75 if abs(lep.pdgId) == 13 else 0.85
    elif wp == 4: B = 0.80 if abs(lep.pdgId) == 13 else 0.90
    return lep.pt * B / lep.jetPtRatiov2

def conept_SSDL(lep):
    ## New proposal from MARCO - 160617
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)==13):
        if (lep.mediumMuonId>0 and lep.mvaSUSY > 0.45): return lep.pt
        else :  return 0.80 * lep.pt / lep.jetPtRatiov2
    if (abs(lep.pdgId)==11):
        if (lep.mvaSUSY > 0.75):  return lep.pt
        else:   return 0.90 * lep.pt / lep.jetPtRatiov2

def conept_SSDL_for3l(lep):

    ## New proposal from MARCO - 160617
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)==13):
        if (lep.mediumMuonId>0 and lep.mvaSUSY > -0.2): return lep.pt
        else :  return 0.75 * lep.pt / lep.jetPtRatiov2
    if (abs(lep.pdgId)==11):
        if (lep.mvaSUSY > 0.5):  return lep.pt
        else:   return 0.80 * lep.pt / lep.jetPtRatiov2

##  OLD DEF
##    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
##    if (abs(lep.pdgId)==13 and lep.mediumMuonId>0 and lep.mvaSUSY > 0.15): return lep.pt
##    if (abs(lep.pdgId)==11 and lep.mvaSUSY > 0.65): return lep.pt
##    else:  return 0.85 * lep.pt / lep.jetPtRatiov2

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)!=13 or lep.mediumMuonId>0) and lep.mvaTTH > 0.90: return lep.pt
    else: return 0.90 * lep.pt / lep.jetPtRatiov3

