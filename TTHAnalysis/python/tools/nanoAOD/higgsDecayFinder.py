from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 


class higgsDecayFinder( Module ): 
    def __init__(self, genCollection="GenPart"):
        self.genCollection = genCollection

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('GenHiggsDecayMode','I')

    def getHiggsDecay(self, idx, genParts):
        decayproducts = [] 
        for g in genParts:
            if g.genPartIdxMother == idx: 
                if (g.pdgId == 25):
                    return self.getHiggsDecay( genParts.index(g),genParts)
                else: 
                    decayproducts.append( abs(g.pdgId) )
        if len(decayproducts) > 2: print "More than two decay products?", decayproducts
        if not len(decayproducts): print 'No decay products found...'
        return decayproducts

    def analyze(self, event):
        genParts = [ g for g in Collection(event, self.genCollection) ]
        if not any( map(lambda x : x.pdgId == 25, genParts)):
            self.out.fillBranch('GenHiggsDecayMode',0)
            return True
        decay = None
        for g in genParts:
            if g.pdgId != 25: continue
            decay = self.getHiggsDecay(genParts.index(g), genParts)

        if not decay                     : self.out.fillBranch('GenHiggsDecayMode',-1); return True 
        
        if   decay == [22,22]                    : self.out.fillBranch('GenHiggsDecayMode',22); return True
        elif decay == [22,23] or decay ==[23,22] : self.out.fillBranch('GenHiggsDecayMode',2223); return True
        elif decay == [23,23]                    : self.out.fillBranch('GenHiggsDecayMode',23); return True
        elif decay == [23,23]                    : self.out.fillBranch('GenHiggsDecayMode',23); return True
        elif decay == [24,24]                    : self.out.fillBranch('GenHiggsDecayMode',24); return True
        elif decay == [15,15]                    : self.out.fillBranch('GenHiggsDecayMode',15); return True 
        elif decay == [13,13]                    : self.out.fillBranch('GenHiggsDecayMode',13); return True 
        else: 
            self.out.fillBranch('GenHiggsDecayMode',-1); return True 
        

