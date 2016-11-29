from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class fastCombinedObjectRecleaner:

    def __init__(self,label="",inlabel=""):

        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inlabel = inlabel

        self.branches = [] # output is done in C++
        self.vars = ["pt","eta","phi","mass"]

        self._helper_lepsF = CollectionSkimmer("LepFO"+self.label, "LepGood", floats=[], maxSize=20, saveSelectedIndices=True)
        self._helper_lepsT = CollectionSkimmer("LepTight"+self.label, "LepGood", floats=[], maxSize=20, saveTagForAll=True)
        self._helper_taus = CollectionSkimmer("TauSel"+self.label, "TauGood", floats=self.vars, maxSize=20)
        self._helper_jets = CollectionSkimmer("JetSel"+self.label, "Jet", floats=self.vars+['btagCSV'], maxSize=20)
        self._helpers = [self._helper_lepsF,self._helper_lepsT,self._helper_taus,self._helper_jets]

        if "/fastCombinedObjectRecleanerHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner worker module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerHelper.cxx+O" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.fastCombinedObjectRecleanerHelper(self._helper_taus.cppImpl(),self._helper_jets.cppImpl())

    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for x in self._helpers:
            x.initInputTree(tree)
        self.initReaders(tree)
        self.initWorker()

    def setOutputTree(self,pytree):
        for x in self._helpers: x.initOutputTree(pytree);

    def initReaders(self,tree):
        for coll in ["LepGood","TauGood","Jet"]:
            setattr(self,'n'+coll,tree.valueReader('n'+coll))
            for B in self.vars:
                setattr(self,"%s_%s"%(coll,B), tree.arrayReader("%s_%s"%(coll,B)))

    def initWorker(self):
        self._worker.setLeptons(self.nLepGood, self.LepGood_eta, self.LepGood_phi)
        self._worker.setTaus(self.nTauGood, self.TauGood_eta, self.TauGood_phi)
        self._worker.setJets(self.nJet, self.Jet_eta, self.Jet_phi)

    def listBranches(self):
        return self.branches

    def __call__(self,event):
        ## Init
        if any([x.initEvent(event) for x in self._helpers]):
            self.initReaders(event._tree)
            self.initWorker()

        tags = getattr(event,'_CombinedTagsForCleaning%s'%self.inlabel)

        for _cpt,_idx in sorted([(tags.conept[i],i) for i,x in filter(lambda y: y[1], enumerate(tags.lepsF))], reverse=True):
            self._helper_lepsF.push_back(_idx)

        for i,x in enumerate(tags.lepsT):
            if x: self._helper_lepsT.push_back(i)

        self._worker.clear()
        for i,x in enumerate(tags.lepsC): self._worker.selectLepton(i,x)
        for i,x in enumerate(tags.tausC): self._worker.selectTau(i,x)
        for i,x in enumerate(tags.jetsS): self._worker.selectJet(i,x)
        self._worker.run()

        return {}
