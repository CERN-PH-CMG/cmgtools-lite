from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class fastCombinedObjectRecleaner:

    def __init__(self,label,inlabel,doVetoZ,doVetoLMf,doVetoLMt):

        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inlabel = inlabel

        self.vars = ["pt","eta","phi","mass"]
        self.vars_leptons = ["pdgId"]
        self.vars_jets = ["btagCSV"]

        self.outvars=['mZ1','minMllAFAS','minMllAFOS','minMllAFSS','minMllSFOS']
        self.branches = [var+self.label for var in self.outvars]

        self._helper_lepsF = CollectionSkimmer("LepFO"+self.label, "LepGood", floats=[], maxSize=20, saveSelectedIndices=True)
        self._helper_lepsT = CollectionSkimmer("LepTight"+self.label, "LepGood", floats=[], maxSize=20, saveTagForAll=True)
        self._helper_taus = CollectionSkimmer("TauSel"+self.label, "TauGood", floats=self.vars, maxSize=20)
        self._helper_jets = CollectionSkimmer("JetSel"+self.label, "Jet", floats=self.vars+self.vars_jets, maxSize=20)
        self._helpers = [self._helper_lepsF,self._helper_lepsT,self._helper_taus,self._helper_jets]

        if "/fastCombinedObjectRecleanerHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner worker module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerHelper.cxx+O" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.fastCombinedObjectRecleanerHelper(self._helper_taus.cppImpl(),self._helper_jets.cppImpl())

        if "/fastCombinedObjectRecleanerMassVetoCalculator_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner mass and veto calculator module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerMassVetoCalculator.cxx+O" % os.environ['CMSSW_BASE'])
        self._workerMV = ROOT.fastCombinedObjectRecleanerMassVetoCalculator(doVetoZ,doVetoLMf,doVetoLMt)

    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for x in self._helpers:
            x.initInputTree(tree)
        self.initReaders(tree)
        self.initWorkers()

    def setOutputTree(self,pytree):
        for x in self._helpers: x.initOutputTree(pytree);

    def initReaders(self,tree):
        for coll in ["LepGood","TauGood","Jet"]:
            setattr(self,'n'+coll,tree.valueReader('n'+coll))
            _vars = self.vars[:]
            if coll=='LepGood': _vars.extend(self.vars_leptons)
            if coll=='Jet': _vars.extend(self.vars_jets)
            for B in _vars:
                setattr(self,"%s_%s"%(coll,B), tree.arrayReader("%s_%s"%(coll,B)))

    def initWorkers(self):
        self._worker.setLeptons(self.nLepGood, self.LepGood_eta, self.LepGood_phi)
        self._worker.setTaus(self.nTauGood, self.TauGood_eta, self.TauGood_phi)
        self._worker.setJets(self.nJet, self.Jet_eta, self.Jet_phi)
        self._workerMV.setLeptons(self.nLepGood, self.LepGood_pt, self.LepGood_eta, self.LepGood_phi,self.LepGood_mass, self.LepGood_pdgId)

    def listBranches(self):
        return self.branches

    def __call__(self,event):
        ## Init
        if any([x.initEvent(event) for x in self._helpers]):
            self.initReaders(event._tree)
            self.initWorkers()

        tags = getattr(event,'_CombinedTagsForCleaning%s'%self.inlabel)

        self._worker.clear()
        for i in tags.lepsC: self._worker.selectLepton(i)
        for i in tags.tausC: self._worker.selectTau(i)
        for i in tags.jetsS: self._worker.selectJet(i)
        self._worker.run()

        self._workerMV.clear()
        for i in tags.lepsL: self._workerMV.setLeptonFlagLoose(i);
        for i in tags.lepsF: self._workerMV.setLeptonFlagFO(i);
        for i in tags.lepsT: self._workerMV.setLeptonFlagTight(i);
        self._workerMV.run()
        vetoedFO = self._workerMV.getVetoedFO()
        vetoedTight = self._workerMV.getVetoedTight()
        for i in xrange(vetoedFO.size()): self._helper_lepsF.push_back(vetoedFO.at(i))
        for i in xrange(vetoedTight.size()): self._helper_lepsT.push_back(vetoedTight.at(i))

        ret = {}
        masses = self._workerMV.GetPairMasses()
        for var in self.outvars: ret[var+self.label]=getattr(masses,var)
        return ret

MODULES=[('clean2',lambda : fastCombinedObjectRecleaner(label="",inlabel="_Test",doVetoZ=True,doVetoLMf=True,doVetoLMt=True))]
