from PhysicsTools.HeppyCore.utils.deltar import deltaR

def passBadMuonFilter(muons, packedCandidates):
    maxDR = 0.001
    minMuonTrackRelErr = 0.5
    suspiciousAlgo = 14
    minMuPt = 100
    flagged = False

    for muon in muons:
        # check the muon inner and globaTrack
        foundBadTrack = False
        if muon.innerTrack().isNonnull():
            it = muon.innerTrack()
            if it.pt() < minMuPt:
                continue
            if it.quality(it.highPurity):
                continue
            if it.ptError()/it.pt() < minMuonTrackRelErr:
                continue
            if it.originalAlgo() == suspiciousAlgo and it.algo() == suspiciousAlgo:
                foundBadTrack = True
        if foundBadTrack:
            #   print 'there is suspicious muon  '
            for c in packedCandidates:
                if c.pt() < minMuPt:
                    continue
                if abs(c.pdgId()) == 13:
                    if deltaR(muon.eta(), muon.phi(), c.eta(), c.phi()) < maxDR:
                        flagged = True
                        break
        if flagged:
            break

    return not flagged


def passBadChargedHadronFilter(muons, packedCandidates):
    maxDR = 0.001
    minMuonTrackRelErr = 0.5
    minPtDiffRel = -0.5
    minMuPt = 100
    flagged = False

    for muon in muons:
        if muon.pt() < minMuPt:
            continue
        if muon.innerTrack().isNonnull():
            it = muon.innerTrack()
            if it.quality(it.highPurity):
                continue
            # All events had a drastically high pt error on the inner muon track (fac. ~10). Require at least 0.5
            if it.ptError()/it.pt() < minMuonTrackRelErr:
                continue
            for c in packedCandidates:
                if abs(c.pdgId()) == 211:
                    # Require very loose similarity in pt (one-sided).
                    dPtRel = (c.pt() - it.pt())/(0.5*(c.pt() + it.pt()))
                    # Flag the event bad if dR is tiny
                    if deltaR(it.eta(), it.phi(), c.eta(), c.phi()) < maxDR and dPtRel > minPtDiffRel:
                        flagged = True
                        break
                        if flagged:
                            break
    return not flagged
