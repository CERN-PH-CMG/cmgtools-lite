from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class electronMuonCleaner( Module ):
    def __init__(self, muonSel, deltaR):
        self.muonSel = muonSel
        self.deltaR  = deltaR

    def analyze(self, event):
        muons = Collection(event, "Muon")
        elecs = Collection(event, "Electron")
        areCleanFromMuons = []
        for el in elecs: 
            isCleanFromMuons = True
            for mu in muons:
                if not self.muonSel(mu): continue
                if deltaR(el,mu) < self.deltaR: 
                    isCleanFromMuons = False
            areCleanFromMuons.append(isCleanFromMuons)
        setattr(event, 'Electron_isCleanFromMuons', areCleanFromMuons)
        return True
