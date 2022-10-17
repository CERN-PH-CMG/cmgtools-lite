from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class JetReCleaner:
    def __init__(self,label=""):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.floats = ("pt","eta","phi","btagCSV")
        self.ints = ("hadronFlavour",)
        if "/jetReCleanerExampleHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/jetReCleanerExampleHelper.cxx+" % os.environ['CMSSW_BASE'])
    def init(self,tree):
        for v in self.floats+self.ints:
            if not tree.GetBranch("Jet_"+v): print "Missing branch Jet_"+v
        self.floats = [v for v in self.floats if tree.GetBranch("Jet_"+v)]
        self.ints   = [v for v in self.ints   if tree.GetBranch("Jet_"+v)]
        self._helper = CollectionSkimmer("JetGood"+self.label, "Jet", floats=self.floats, ints=self.ints, saveSelectedIndices=True, maxSize=20)
        self._worker = ROOT.JetReCleanerExampleHelper(self._helper.cppImpl())
        self._helper.initInputTree(tree)
        self.initReaders(tree)
        self._helper.initOutputTree(self._out);
    def listBranches(self):
        return []
    def initReaders(self,tree):
        for B in "nLepGood", "nJet": setattr(self, B, tree.valueReader(B))
        for B in "eta", "phi" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for B in "eta", "phi" : setattr(self,"Jet_"+B, tree.arrayReader("Jet_"+B))
        self._worker.setLeptons(self.nLepGood, self.LepGood_eta, self.LepGood_phi)
        self._worker.setJets(self.nJet, self.Jet_eta, self.Jet_phi)
    def setOutputTree(self,pytree):
        self._out = pytree
    def __call__(self,event):
        ## Init
        if self._helper.initEvent(event):
            self.initReaders(event._tree)
        ## Algo
        self._worker.run()
        return {}

class LepOtherCleaner:
    def __init__(self,label=""):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.floats = ("pt","eta","phi","miniRelIso","sip3d")
        self.ints = ("mcMatchAny","mcMatchId","ICHEPmediumMuonId",)
    def init(self,tree):
        for v in self.floats+self.ints:
            if not tree.GetBranch("LepOther_"+v): print "Missing branch LepOther_"+v
        self.floats = [v for v in self.floats if tree.GetBranch("LepOther_"+v)]
        self.ints   = [v for v in self.ints   if tree.GetBranch("LepOther_"+v)]
        self._helper = CollectionSkimmer("LepOtherGood"+self.label, "LepOther", floats=self.floats, ints=self.ints, saveSelectedIndices=True, maxSize=20)
        self._helper.initInputTree(tree)
        self.initReaders(tree)
        self._helper.initOutputTree(self._out);
    def listBranches(self):
        return []
    def initReaders(self,tree):
        for B in "nLepGood", "nLepOther", "nJet": setattr(self, B, tree.valueReader(B))
        for B in "eta", "phi" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for B in "pt", "eta", "phi", "btagCSV" : setattr(self,"Jet_"+B, tree.arrayReader("Jet_"+B))
        for B in "eta", "phi","pdgId", "dz": setattr(self,"LepOther_"+B, tree.arrayReader("LepOther_"+B))
    def setOutputTree(self,pytree):
        self._out = pytree
    def __call__(self,event):
        ## Init
        if self._helper.initEvent(event):
            self.initReaders(event._tree)
        ## Algo
        vetos = [ (self.LepGood_eta[i],self.LepGood_phi[i]) for i in xrange(self.nLepGood.Get()[0]) ]
        for i in xrange(self.nJet.Get()[0]):
            jeta,jphi = (self.Jet_eta[i],self.Jet_phi[i])
            if min(deltaR(jeta,jphi,leta,lphi) for (leta,lphi) in vetos) > 0.4:
                vetos.append((jeta,jphi)) 
                break ## clean respect to the leading jet only
        #vetos += [ (self.Jet_eta[i],self.Jet_phi[i]) for i in ijets if self.Jet_pt[i] > 40 or self.Jet_btagCSV[i] > 0.46 ]
        for i in xrange(self.nLepOther.Get()[0]):
            if abs(self.LepOther_pdgId[i]) != 13: continue
            if abs(self.LepOther_dz[i]) >= 0.2: continue
            eta, phi = self.LepOther_eta[i], self.LepOther_phi[i]
            bad = False
            for (le,lp) in vetos:
                if abs(le-eta) < 0.4 and deltaR(le,lp,eta,phi) < 0.4:
                    bad = True; 
                    break
            if not bad: self._helper.push_back(i)
        return {}

MODULES = [
    ('jets', lambda : JetReCleaner()),
    ('leps', lambda : LepOtherCleaner()),
]


