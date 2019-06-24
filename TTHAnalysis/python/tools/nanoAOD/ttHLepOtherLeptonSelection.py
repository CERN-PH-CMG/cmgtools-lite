from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class otherLeptonSelection( Module ):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LepGood_otherLeptonSelection", "I", lenVar="nLepGood")
    def analyze(self, event):
        leps = [l for l in Collection(event, 'LepGood') ]
        ret = [ 0 for l in leps ]
        if len(leps) == 2:
            for i,l1 in enumerate(leps):
                l2 = leps[1-i]
                if abs(l2.genPartFlav) not in (1,15): continue
                if l2.mvaTTH < 0.9: continue
                if deltaR(l1.eta, l1.phi, l2.eta, l2.phi) < 0.8: continue
                ret[i] = 1
        self.out.fillBranch("LepGood_otherLeptonSelection", ret)
        return True

oLS = lambda : otherLeptonSelection()
