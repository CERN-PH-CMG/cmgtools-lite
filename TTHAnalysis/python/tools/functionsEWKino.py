def _ewkino_idEmu_cuts_E2(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True
def _ewkino_idEmu_cuts_E2_obj(lep):
    if (abs(lep.pdgId())!=11): return True
    etasc = lep.superCluster().eta()
    if (lep.hadronicOverEm()>=(0.10-0.03*(abs(etasc)>1.479))): return False
    if (abs(lep.deltaEtaSuperClusterTrackAtVtx())>=(0.01-0.002*(abs(etasc)>1.479))): return False
    if (abs(lep.deltaPhiSuperClusterTrackAtVtx())>=(0.04+0.03*(abs(etasc)>1.479))): return False
    eInvMinusPInv = (1.0/lep.ecalEnergy() - lep.eSuperClusterOverP()/lep.ecalEnergy()) if lep.ecalEnergy()>0. else 9e9
    if (eInvMinusPInv<=-0.05): return False
    if (eInvMinusPInv>=(0.01-0.005*(abs(etasc)>1.479))): return False
    if (lep.full5x5_sigmaIetaIeta()>=(0.011+0.019*(abs(etasc)>1.479))): return False
    return True

def _ewkino_2lss_lepId_CBloose(lep):
    if abs(lep.pdgId) == 13:
        if lep.pt <= 5: return False
        return True #lep.mediumMuonId > 0
    elif abs(lep.pdgId) == 11:
        if lep.pt <= 7: return False
        if not (lep.convVeto and lep.lostHits == 0): 
            return False
        if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
            return False
        if not _ewkino_idEmu_cuts_E2(lep): return False
        return True
    return False

def _ewkino_2lss_lepId_loosestFO(lep):
    if not _ewkino_2lss_lepId_CBloose(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.tightCharge > 0 and lep.mediumMuonID2016 > 0
    elif abs(lep.pdgId) == 11:
        return (lep.convVeto and lep.tightCharge > 1 and lep.lostHits == 0)
    return False

def _ewkino_2lss_lepId_FO(lep):
    if not _ewkino_2lss_lepId_loosestFO(lep): return False
    if (abs(lep.pdgId) == 13):  
        return  (lep.jetPtRatiov2 > 0.3 and lep.jetBTagCSV < 0.3 and lep.mediumMuonID2016 > 0)
    elif (abs(lep.pdgId) == 11): 
        return lep.jetPtRatiov2 > 0.3 and lep.jetBTagCSV < 0.3 and ((abs(lep.eta)<1.479 and lep.mvaIdSpring15>0.0) or (abs(lep.eta)>1.479 and lep.mvaIdSpring15>0.3))

def _ewkino_2lss_lepId_IPcuts(lep):
    if not lep.sip3d<8: return False
    if not (abs(lep.dxy)<0.05): return False
    if not (abs(lep.dz)<0.1): return False
    return True

def _ewkino_2lss_lepConePt1015(lep):
    if lep.conept <= (10 if abs(lep.pdgId)==13 else 15): return False
    return True

def _ewkino_leptonMVA_VT(lep):
    if abs(lep.pdgId) == 13: return (lep.mvaSUSY > 0.45)
    if abs(lep.pdgId) == 11: return (lep.mvaSUSY > 0.75)
    return False

def _ewkino_leptonMVA_T(lep):
    if abs(lep.pdgId) == 13: return (lep.mvaSUSY > 0.15)
    if abs(lep.pdgId) == 11: return (lep.mvaSUSY > 0.65)
    return False

def _ewkino_leptonMVA_M(lep):
    if abs(lep.pdgId) == 13: return (lep.mvaSUSY > -0.20)
    if abs(lep.pdgId) == 11: return (lep.mvaSUSY >  0.50)
    return False

def _ewkino_2lss_lepId_num(lep):
    if not _ewkino_2lss_lepId_loosestFO(lep): return False
    if not _ewkino_leptonMVA_VT(lep): return False
    if abs(lep.pdgId)==11:
        if not _ewkino_idEmu_cuts_E2(lep): return False
    if abs(lep.pdgId) == 13: return lep.mediumMuonID2016 > 0
    return True

def _ewkino_3l_lepId_loosestFO(lep):
    if not _ewkino_2lss_lepId_CBloose(lep): return False
    if abs(lep.pdgId) == 13:
        return True
    elif abs(lep.pdgId) == 11:
        return (lep.convVeto and lep.lostHits == 0)
    return False

def _ewkino_3l_lepId_FO(lep):
    if not _ewkino_3l_lepId_loosestFO(lep): return False
    if (abs(lep.pdgId) == 13):  
        return  (lep.jetPtRatiov2 > 0.3 and lep.jetBTagCSV < 0.3 and lep.mediumMuonID2016 > 0)
    elif (abs(lep.pdgId) == 11): 
        return lep.jetPtRatiov2 > 0.3 and lep.jetBTagCSV < 0.3 and ((abs(lep.eta)<1.479 and lep.mvaIdSpring15>0.0) or (abs(lep.eta)>1.479 and lep.mvaIdSpring15>0.3))

def _ewkino_3l_lepId_num(lep):
    if not _ewkino_3l_lepId_FO(lep): return False
    if not _ewkino_leptonMVA_M(lep): return False
    if abs(lep.pdgId)==11:
        if not _ewkino_idEmu_cuts_E2(lep): return False
    if abs(lep.pdgId) == 13: return lep.mediumMuonID2016 > 0
    return True

