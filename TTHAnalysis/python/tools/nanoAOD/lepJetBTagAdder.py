from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

class lepJetBTagAdder( Module ):
    def __init__(self,jetBTagLabel,lepBTagLabel, dummyValue=-99):
        self._jetBTagLabel = jetBTagLabel
        self._lepBTagLabel = lepBTagLabel
        self._dummyValue = dummyValue
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LepGood_" + self._lepBTagLabel, "F", lenVar="nLepGood")
    def analyze(self, event):
        leps = Collection(event, 'LepGood')
        jets = Collection(event, 'Jet')
        nJets = len(jets)
        values = []
        for lep in leps:
            if lep.jetIdx >= 0 and lep.jetIdx < nJets:
                values.append(getattr(jets[lep.jetIdx], self._jetBTagLabel))
            else:
                values.append(self._dummyValue)
        self.out.fillBranch("LepGood_" + self._lepBTagLabel, values)
        return True

lepJetBTagCSV = lambda : lepJetBTagAdder("btagCSVV2", "jetBTagCSV")
lepJetBTagDeepCSV = lambda : lepJetBTagAdder("btagDeepB", "jetBTagDeepCSV")
