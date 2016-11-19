
def _susy2lss_lepId_CBloose(lep):
        if abs(lep.pdgId) == 13:
            if lep.pt <= 5: return False
            return True #lep.mediumMuonId > 0
        elif abs(lep.pdgId) == 11:
            if lep.pt <= 7: return False
            if not (lep.convVeto and lep.lostHits <= 1): 
                return False
            if not lep.mvaIdSpring15 > -0.70+(-0.83+0.70)*(abs(lep.etaSc)>0.8)+(-0.92+0.83)*(abs(lep.etaSc)>1.479):
                return False
            if not _susy2lss_idEmu_cuts(lep): return False
            return True
        return False

def _susy2lss_lepConePt1015(lep):
    if lep.conept <= (10 if abs(lep.pdgId)==13 else 15): return False
    return True

def _susy2lss_lepId_loosestFO(lep):
    if not _susy2lss_lepId_CBloose(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonId > 0 and lep.tightCharge > 0
    elif abs(lep.pdgId) == 11:
        return (lep.convVeto and lep.tightCharge > 1 and lep.lostHits == 0)
    return False

def _susy2lss_lepId_tighterFO(lep):
    if not _susy2lss_lepId_loosestFO(lep): return False
    if abs(lep.pdgId)==11:
        if not lep.mvaIdSpring15 > -0.155+(-0.56+0.155)*(abs(lep.etaSc)>0.8)+(-0.76+0.56)*(abs(lep.etaSc)>1.479):
            return False
        if not _susy2lss_idIsoEmu_cuts(lep): return False
    return True

def _susy2lss_lepId_inSituLoosestFO(lep):
    if not _susy2lss_lepId_loosestFO(lep): return False
    if abs(lep.pdgId)==11:
        if not lep.mvaIdSpring15 > -0.363+(-0.579+0.363)*(abs(lep.etaSc)>0.8)+(-0.623+0.579)*(abs(lep.etaSc)>1.479):
            return False
    return True

def _susy2lss_lepId_inSituTighterFO(lep):
    if not _susy2lss_lepId_loosestFO(lep): return False
    if abs(lep.pdgId)==11:
        if not lep.mvaIdSpring15 > 0.051+(-0.261-0.051)*(abs(lep.etaSc)>0.8)+(-0.403+0.261)*(abs(lep.etaSc)>1.479):
            return False
        if not _susy2lss_idIsoEmu_cuts(lep): return False
    return True

def _susy2lss_lepId_IPcuts(lep):
    if not lep.sip3d<4: return False
    if not (abs(lep.dxy)<0.05): return False
    if not (abs(lep.dz)<0.1): return False
    return True

def _susy2lss_lepId_CB(lep):
    if not _susy2lss_lepId_CBloose(lep): return False
    if not _susy2lss_lepId_IPcuts(lep): return False
    if abs(lep.pdgId) == 13:
        return lep.mediumMuonId > 0 and lep.tightCharge > 0
    elif abs(lep.pdgId) == 11:
        if not (lep.convVeto and lep.tightCharge > 1 and lep.lostHits == 0): 
            return False
        return lep.mvaIdSpring15 > 0.87+(0.60-0.87)*(abs(lep.etaSc)>0.8)+(0.17-0.60)*(abs(lep.etaSc)>1.479)
    return False

def _susy2lss_idEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.sigmaIEtaIEta>=(0.011 if abs(lep.etaSc)<1.479 else 0.031)): return False
    if (lep.hadronicOverEm>=0.08): return False
    if (abs(lep.dEtaScTrkIn)>=0.01): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04 if abs(lep.etaSc)<1.479 else 0.08)): return False
    if (abs(lep.eInvMinusPInv)>=0.01): return False
    return True
def _susy2lss_idEmu_cuts_obj(lep):
    if (abs(lep.pdgId())!=11): return True
    if (lep.full5x5_sigmaIetaIeta()>=(0.011 if abs(lep.superCluster().eta())<1.479 else 0.031)): return False
    if (lep.hadronicOverEm()>=0.08): return False
    if (abs(lep.deltaEtaSuperClusterTrackAtVtx())>=0.01): return False
    if (abs(lep.deltaPhiSuperClusterTrackAtVtx())>=(0.04 if abs(lep.superCluster().eta())<1.479 else 0.08)): return False
    if (abs((1.0/lep.ecalEnergy() - lep.eSuperClusterOverP()/lep.ecalEnergy()) if lep.ecalEnergy()>0. else 9e9)>=0.01): return False
    return True

def _susy2lss_idIsoEmu_cuts(lep):
    if (abs(lep.pdgId)!=11): return True
    if not _susy2lss_idEmu_cuts(lep): return False
    if (lep.ecalPFClusterIso>=0.45*lep.pt): return False
    if (lep.hcalPFClusterIso>=0.25*lep.pt): return False
    if (lep.dr03TkSumPt>=0.2*lep.pt): return False
    return True
def _susy2lss_idIsoEmu_cuts_obj(lep):
    if (abs(lep.pdgId())!=11): return True
    if not _susy2lss_idEmu_cuts_obj(lep): return False
    if (lep.ecalPFClusterIso()>=0.45*lep.pt()): return False
    if (lep.hcalPFClusterIso()>=0.25*lep.pt()): return False
    if (lep.dr03TkSumPt()>=0.2*lep.pt()): return False
    return True

def _susy2lss_leptonMVA(lep):
    if abs(lep.pdgId) == 13: return (lep.mvaTTHMoriond16 > 0.45)
    if abs(lep.pdgId) == 11: return (lep.mvaTTHMoriond16 > 0.75)
    return False
    
def _susy2lss_multiIso(lep):
        if abs(lep.pdgId) == 13: A,B,C = (0.16,0.76,7.2)
        else:                    A,B,C = (0.12,0.80,7.2)
        return lep.miniRelIso < A and (lep.jetPtRatiov2 > B or lep.jetPtRelv2 > C)

def _susy2lss_multiIso_relaxedForInSituApp(lep):
        if abs(lep.pdgId) == 13: A,B,C = (0.4,0.76,7.2)
        else:                    A,B,C = (0.4,0.80,7.2)
        return lep.miniRelIso < A and (1/lep.jetPtRatiov2 < (1/B + lep.miniRelIso) or lep.jetPtRelv2 > C)

