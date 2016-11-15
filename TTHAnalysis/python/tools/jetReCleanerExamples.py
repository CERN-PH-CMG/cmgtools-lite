from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class JetReCleaner_base:
    def __init__(self,label=""):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.vars = ("pt","eta","phi","mass","btagCSV")
        self.branches =  [ ("nJetGood"+self.label, "I") ]
        self.branches += [ ("JetGood"+self.label+"_"+V, "F", 20, "nJetGood"+self.label) for V in self.vars ]
    def init(self,tree):
        pass
    def listBranches(self):
        return self.branches

class JetReCleaner(JetReCleaner_base):
    """Pure python version, using collections and objects (0.7 kHz with treeReAnalyzer, 3.1 kHz with treeReAnalyzer2)"""
    def __init__(self,label=""):
        JetReCleaner_base.__init__(self,label)
    def __call__(self,event):
        leps = [l for l in Collection(event,"LepGood")]
        jets = [j for j in Collection(event,"Jet")]
        cleanJets = [ j for j in jets if min(deltaR(j,l) for l in leps) > 0.4 ]
        ret = { 'nJetGood'+self.label : len(cleanJets) }
        for V in self.vars:
            ret[ 'JetGood'+self.label+"_"+V ] = [getattr(j,V) for j in cleanJets]
        return ret

class JetReCleaner_TreeReaders(JetReCleaner_base):
    """Python version using TreeReaderArray for input (runs at ~10 kHz)"""
    def __init__(self,label=""):
        JetReCleaner_base.__init__(self,label)
    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for B in "nLepGood", "nJet": setattr(self, B, tree.valueReader(B))
        for B in "eta", "phi" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for v in self.vars:
            setattr(self,"Jet_"+v, tree.arrayReader("Jet_"+v))
    def makeCleanJets(self,event):
        leps = [ (self.LepGood_eta[i],self.LepGood_phi[i]) for i in xrange(self.nLepGood.Get()[0]) ]
        jets = [ (i, self.Jet_eta[i], self.Jet_phi[i]) for i in xrange(self.nJet.Get()[0]) ]
        cleanJets = []
        for ij,je,jp in jets:
            good = True
            for le,lp in leps:
                if abs(je-le)<0.4 and deltaR(je,jp,le,lp)<0.4:
                    good = False; break
            if good: cleanJets.append(ij)
        return cleanJets
    def __call__(self,event):
        ## Init
        if event._tree._ttreereaderversion > self._ttreereaderversion: 
            self.init(event._tree)
        ## Algo
        cleanJets = self.makeCleanJets(event)
        ## Output (python)
        ret = { 'nJetGood'+self.label : len(cleanJets) }
        for V in self.vars:
            branch = getattr(self, "Jet_"+V)
            ret[ 'JetGood'+self.label+"_"+V ] = [branch[j] for j in cleanJets]
        return ret

class JetReCleaner_CollectionSkimmer(JetReCleaner_TreeReaders):
    """Python version, using TreeReaderArray for input and CollectionSkimmer for output (runs at ~17 kHz)"""
    def __init__(self,label=""):
        JetReCleaner_TreeReaders.__init__(self,label)
        self._helper = CollectionSkimmer("JetGood"+self.label, "Jet", floats=self.vars, maxSize=20)
        self.branches = [] # output is done in C++
    def init(self,tree):
        self._helper.initInputTree(tree)
        self.initReaders(tree)
    def initReaders(self,tree):
        for B in "nLepGood", "nJet": setattr(self, B, tree.valueReader(B))
        for B in "eta", "phi" : setattr(self,"LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for B in "eta", "phi" : setattr(self,"Jet_"+B, tree.arrayReader("Jet_"+B))
    def setOutputTree(self,pytree):
        self._helper.initOutputTree(pytree);
    def __call__(self,event):
        ## Init
        if self._helper.initEvent(event):
            self.initReaders(event._tree)
        ## Algo
        cleanJets = self.makeCleanJets(event)
        ## Output
        self._helper.push_back_all(cleanJets)
        return {}


class JetReCleaner_CppHelper(JetReCleaner_CollectionSkimmer):
    """Version using a C++ worker, and CollectionSkimmer for output, called directly from C++ (runs at ~43 kHz)"""
    def __init__(self,label=""):
        JetReCleaner_CollectionSkimmer.__init__(self,label)
        if "/jetReCleanerExampleHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/jetReCleanerExampleHelper.cxx+" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.JetReCleanerExampleHelper(self._helper.cppImpl())
    def init(self,tree):
        JetReCleaner_CollectionSkimmer.init(self,tree)
        self.initWorker()
    def initWorker(self):
        self._worker.setLeptons(self.nLepGood, self.LepGood_eta, self.LepGood_phi)
        self._worker.setJets(self.nJet, self.Jet_eta, self.Jet_phi)
    def __call__(self,event):
        ## Init
        if self._helper.initEvent(event):
            self.initReaders(event._tree)
            self.initWorker()
        ## Algo + Output
        self._worker.run()
        return {}

class JetReCleaner_CppHelper2(JetReCleaner_CppHelper):
    """Version using a C++ worker, and CollectionSkimmer for output, connected via python (runs at ~35 kHz)"""
    def __init__(self,label=""):
        JetReCleaner_CollectionSkimmer.__init__(self,label)
        if "/jetReCleanerExampleHelper2_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/jetReCleanerExampleHelper2.cxx+" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.JetReCleanerExampleHelper2()
    def __call__(self,event):
        ## Init
        if self._helper.initEvent(event):
            self.initReaders(event._tree)
            self.initWorker()
        ## Algo
        cleanJets = self._worker.run()
        ## Output
        self._helper.push_back(cleanJets) #push_back, since it's a std::vector and not a python list
        return {}


MODULES = [
    ('py', lambda : JetReCleaner()),
    ('tr', lambda : JetReCleaner_TreeReaders()),
    ('cs', lambda : JetReCleaner_CollectionSkimmer()),
    ('cpp1', lambda : JetReCleaner_CppHelper()),
    ('cpp2', lambda : JetReCleaner_CppHelper2()),
    # A second instance, to check no concurrency issues
    ('2py', lambda : JetReCleaner("Another")),
    ('2tr', lambda : JetReCleaner_TreeReaders("Another")),
    ('2cs', lambda : JetReCleaner_CollectionSkimmer("Another")),
    ('2cpp1', lambda : JetReCleaner_CppHelper("Another")),
    ('2cpp2', lambda : JetReCleaner_CppHelper2("Another")),
]


