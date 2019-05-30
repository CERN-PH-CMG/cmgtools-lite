from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 

class ttHLepQCDFakeRateAnalyzer( Module ):
    def __init__(self, jetSel = lambda jet : True, 
                       pairSel = lambda p : True, 
                       requirePair = True, 
                       maxLeptons = -1, 
                       isMC = None, 
                       saveJetIndex = True,
                       jetFloats = ["pt", "eta", "phi", "btagCSVV2", "btagDeepB", "btagDeepC", "btagDeepFlavB", "btagDeepFlavC"],
                       jetInts = ["jetId", "hadronFlavour"]):
        self.jetSel = jetSel
        self.pairSel = pairSel
        self.maxLeptons = maxLeptons
        self.requirePair = requirePair
        self.jetFloats = jetFloats
        self.jetInts = jetInts
        self.isMC = isMC
        self.saveIndex = saveJetIndex

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        vnames = []
        for v in self.jetFloats[:]:
            if not inputTree.GetBranch("Jet_"+v): 
                print "Skip missing Jet_"+v
                continue
            self.out.branch("LepGood_awayJet_"+v, "F", lenVar="nLepGood")
            vnames.append(v)
        for v in self.jetInts[:]:
            if not inputTree.GetBranch("Jet_"+v): 
                print "Skip missing Jet_"+v
                continue
            self.out.branch("LepGood_awayJet_"+v, "I", lenVar="nLepGood")
            vnames.append(v)
        if self.saveIndex:
            self.out.branch("LepGood_awayJet_index", "I", lenVar="nLepGood")
        self.vnames = vnames


    def analyze(self, event):
        leps = Collection(event, 'LepGood')
        if self.maxLeptons > 0 and len(leps) > self.maxLeptons:
            return False
        
        jets = []
        for ij,j in enumerate(Collection(event, 'Jet')):
            if self.jetSel(j): jets.append((ij,j))
        jets.sort(key = lambda ijj : ijj[1].pt, reverse=True)

        ret = dict((v, [0 for l in leps]) for v in self.vnames)
        indices = [ -1 for l in leps ]

        npairs = 0
        for i,lep in enumerate(leps):
            for ij, jet in jets:
                if self.pairSel((lep,jet)):
                    for v in self.vnames:
                        ret[v][i] = getattr(jet, v)
                    indices[i] = ij
                    npairs += 1
                    break

        if self.requirePair:
            if npairs == 0: 
                return False

        for v in self.vnames:
            self.out.fillBranch("LepGood_awayJet_"+v, ret[v])
        
        if self.saveIndex:
            self.out.fillBranch("LepGood_awayJet_index", indices)
        return True
