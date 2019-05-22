from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

class ttHLeptonCombMasses( Module ):
    def __init__(self, leptonsAndSels, maxLeps=None, postfix=""):
        self.leptonsAndSels = leptonsAndSels[:]
        self.maxLeps = maxLeps
        self.postfix = postfix
        self.branches = [ 'm2l','m3l','m4l', 'mZ1', 'mZ1SFSS', 'mZ2', 'mZZ', 'minMllSFOS','minMllAFOS','minMllAFAS' ]

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for B in self.branches:
            self.wrappedOutputTree.branch(B+self.postfix,'F')

    def analyze(self, event):
        leps = []
        for tag, sel in self.leptonsAndSels:
            leps += filter(sel, Collection(event, tag))
        leps.sort(key = lambda l : -l.pt)
        if self.maxLeps:
            leps = leps[:self.maxLeps]
        nlep = len(leps)

        self.wrappedOutputTree.fillBranch('m2l'+self.postfix, (leps[0].p4() + leps[1].p4()).M() if nlep >= 2 else 0)
        self.wrappedOutputTree.fillBranch('m3l'+self.postfix, (leps[0].p4() + leps[1].p4() + leps[2].p4()).M() if nlep >= 3 else 0)
        self.wrappedOutputTree.fillBranch('m4l'+self.postfix, (leps[0].p4() + leps[1].p4() + leps[2].p4() + leps[3].p4()).M() if nlep >= 4 else 0)

        bestZ1 = [ 0., -1,-1 ]
        bestZ1sfss = [ 0., -1,-1 ]
        bestZ2 = [ 0., -1,-1, 0. ]
        bestZZ = 0
        minMllSFOS = -1
        minMllAFOS = -1
        minMllAFAS = -1
        for i,l1 in enumerate(leps):
            for j in range(i+1,nlep):
                l2 = leps[j]    
                zmass = (l1.p4() + l2.p4()).M()
                if minMllAFAS < 0 or minMllAFAS > zmass: minMllAFAS = zmass
                if l1.pdgId == -l2.pdgId:
                    if minMllSFOS < 0 or minMllSFOS > zmass: minMllSFOS = zmass
                    if minMllAFOS < 0 or minMllAFOS > zmass: minMllAFOS = zmass
                    if bestZ1[0] == 0 or abs(zmass - 91.188) < abs(bestZ1[0] - 91.188):
                        bestZ1 = [ zmass, i, j ]
                elif l1.pdgId == l2.pdgId:
                    if bestZ1sfss[0] == 0 or abs(zmass - 91.188) < abs(bestZ1sfss[0] - 91.188):
                        bestZ1sfss = [ zmass, i, j ]
                elif l1.pdgId * l2.pdgId < 0:
                    if minMllAFOS < 0 or minMllAFOS > zmass: minMllAFOS = zmass
        self.wrappedOutputTree.fillBranch('mZ1'+self.postfix, bestZ1[0])
        self.wrappedOutputTree.fillBranch('mZ1SFSS'+self.postfix, bestZ1sfss[0])
        self.wrappedOutputTree.fillBranch('minMllSFOS'+self.postfix, minMllSFOS)
        self.wrappedOutputTree.fillBranch('minMllAFOS'+self.postfix, minMllAFOS)
        self.wrappedOutputTree.fillBranch('minMllAFAS'+self.postfix, minMllAFAS)

        if bestZ1[0] != 0 and nlep > 3:
            for i,l1 in enumerate(leps):
                if i == bestZ1[1] or i == bestZ1[2]: continue
                for j in range(i+1,nlep):
                    if j == bestZ1[1] or j == bestZ1[2]: continue
                    l2 = leps[j]    
                    if l1.pdgId == -l2.pdgId:
                        if l1.pt + l2.pt > bestZ2[0]:
                            bestZ2 = [ l1.pt + l2.pt, i, j, (l1.p4() + l2.p4()).M() ]
            if bestZ2[0] != 0:
                bestZZ = (leps[bestZ1[1]].p4() + leps[bestZ1[2]].p4() + leps[bestZ2[1]].p4() + leps[bestZ1[2]].p4()).M()
        self.wrappedOutputTree.fillBranch('mZ2'+self.postfix, bestZ2[-1])
        self.wrappedOutputTree.fillBranch('mZZ'+self.postfix, bestZZ)
    
        return True

