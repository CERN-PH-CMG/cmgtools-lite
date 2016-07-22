def _ttH_idEmu_cuts_E2(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hadronicOverEm>=(0.10-0.03*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dEtaScTrkIn)>=(0.01-0.002*(abs(lep.etaSc)>1.479))): return False
    if (abs(lep.dPhiScTrkIn)>=(0.04+0.03*(abs(lep.etaSc)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.05): return False
    if (lep.eInvMinusPInv>=(0.01-0.005*(abs(lep.etaSc)>1.479))): return False
    if (lep.sigmaIEtaIEta>=(0.011+0.019*(abs(lep.etaSc)>1.479))): return False
    return True
def _ttH_idEmu_cuts_E2_obj(lep):
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

def _soft_MuonId_2016ICHEP(lep):
    if (abs(lep.pdgId())!=13): return False
    if not lep.muonID("TMOneStationTight"): return False #TMOneStationTightMuonId
    if not lep.track().hitPattern().trackerLayersWithMeasurement() > 5: return False
    if not lep.track().hitPattern().pixelLayersWithMeasurement() > 0: return False
    if not (abs(lep.dxy())<0.3 and abs(lep.dz())<20): return False
    return True

def _medium_MuonId_2016ICHEP(lep):
    if (abs(lep.pdgId())!=13): return False
    if not (lep.physObj.isGlobalMuon() or lep.physObj.isTrackerMuon()): return False
    if not (lep.innerTrack().validFraction()>0.49): return False
    if lep.segmentCompatibility()>0.451: return True
    else:
        if not lep.globalTrack().isNonnull(): return False
        if not lep.isGlobalMuon: return False
        if not lep.globalTrack().normalizedChi2()<3: return False
        if not lep.combinedQuality().chi2LocalPosition<12: return False
        if not lep.combinedQuality().trkKink<20: return False 
        if not lep.segmentCompatibility()>0.303: return False

    return True
