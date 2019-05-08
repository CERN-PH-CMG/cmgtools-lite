from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import itertools

class ttHPrescalingLepSkimmer( Module ):
    def __init__(self,
            prescaleFactor,
            muonSel = lambda l : True,
            electronSel = lambda l : True,
            minLeptons = 0,
            minLeptonsNoPrescale = 0,
            requireSameSignPair = False,
            jetSel = lambda j : True,
            minJets = 0,
            minMET = 0,
            useEventNumber = True,
            label = "prescaleFromSkim"):

        self.prescaleFactor = prescaleFactor
        self.useEventNumber = useEventNumber
        self.muonSel = muonSel
        self.electronSel = electronSel
        self.minLeptons = minLeptons
        self.minLeptonsNoPrescale = minLeptonsNoPrescale
        self.requireSameSignPair = requireSameSignPair
        self.jetSel = jetSel
        self.minJets = minJets
        self.minMET = minMET
        self.label = label
        self.events = 0

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch(self.label,'i')

    def analyze(self, event):
        if self.prescaleFactor == 1:
            self.wrappedOutputTree.fillBranch(self.label, self.prescaleFactor)
            return True

        toBePrescaled = True
        if self.minLeptons > 0:
            muons = filter(self.muonSel, Collection(event, 'Muon'))
            electrons = filter(self.electronSel, Collection(event, 'Electron'))
            leps = muons + electrons
            if len(leps) < self.minLeptonsNoPrescale:
                return False
            if len(leps) >= self.minLeptons:
                if self.requireSameSignPair:
                    if any([(l1.charge * l2.charge > 0) for l1,l2 in itertools.combinations(leps,2)]):
                        toBePrescaled = False
                else:
                    toBePrescaled = False
        if self.minJets > 0:
            jets = filter(self.jetSel, Collection(event, 'Jet'))
            if len(jets) >= self.minJets:
                toBePrescaled = False
        if self.minMET > 0:
            if event.MET_pt > self.minMET:
                toBePrescaled = False
        if not toBePrescaled:
            self.wrappedOutputTree.fillBranch(self.label, 1)
            return True
        elif self.prescaleFactor == 0:
            return False
        self.events += 1
        evno = self.events
        if self.useEventNumber: # use run and LS number multiplied by some prime numbers
            evno = event.event*223 + event.luminosityBlock*997
        if (evno % self.prescaleFactor == 1):
            self.wrappedOutputTree.fillBranch(self.label, self.prescaleFactor)
            return True
        else:
            return False

