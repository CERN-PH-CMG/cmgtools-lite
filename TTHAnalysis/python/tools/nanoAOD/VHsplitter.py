from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 


class VHsplitter( Module ): 
    def __init__(self, genCollection="GenPart"):
        self.genCollection = genCollection

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('VHisZH','I')


    def analyze(self, event):
        genBosons = [ g for  g in Collection(event, self.genCollection) if (g.statusFlags == 4481) and (abs(g.pdgId) == 23 or abs(g.pdgId) == 24)  ]
        if len(genBosons) != 1: 
            self.out.fillBranch("VHisZH",-1)
        elif abs(genBosons[0].pdgId) == 23: 
            self.out.fillBranch("VHisZH",1)
        else:
            self.out.fillBranch("VHisZH",0)

        return True
