from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class fastCombinedObjectRecleaner:

    def __init__(self,label,inlabel,cleanTausWithLooseLeptons,cleanJetsWithFOTaus,doVetoZ,doVetoLMf,doVetoLMt,jetPts,btagL_thr,btagM_thr):

        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inlabel = inlabel

        self.vars = ["pt","eta","phi","mass"]
        self.vars_leptons = ["pdgId"]
        self.vars_jets = ["btagCSV"]

        self.cleanTausWithLooseLeptons = cleanTausWithLooseLeptons
        self.cleanJetsWithFOTaus = cleanJetsWithFOTaus
        self.jetPts = jetPts

        self.outmasses=['mZ1','minMllAFAS','minMllAFOS','minMllAFSS','minMllSFOS']
        self._outjetvars = ['htJet%dj','mhtJet%d','nBJetLoose%d','nBJetMedium%d']
        self.outjetvars=[]
        for jetPt in self.jetPts: self.outjetvars.extend([(x%jetPt,'I' if 'nBJet' in x else 'F') for x in self._outjetvars])
        self.branches = [var+self.label for var in self.outmasses]
        self.branches.extend([(var+self.label,_type) for var,_type in self.outjetvars])
        self.branches += [("LepGood_conePt","F",20,"nLepGood")]

        self._helper_lepsF = CollectionSkimmer("LepFO"+self.label, "LepGood", floats=[], maxSize=20, saveSelectedIndices=True,padSelectedIndicesWith=0)
        self._helper_lepsT = CollectionSkimmer("LepTight"+self.label, "LepGood", floats=[], maxSize=20, saveTagForAll=True)
        self._helper_taus = CollectionSkimmer("TauSel"+self.label, "TauGood", floats=self.vars, maxSize=20)
        self._helper_jets = CollectionSkimmer("JetSel"+self.label, "Jet", floats=self.vars+self.vars_jets, maxSize=20)
        self._helpers = [self._helper_lepsF,self._helper_lepsT,self._helper_taus,self._helper_jets]

        if "/fastCombinedObjectRecleanerHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner worker module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerHelper.cxx+O" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.fastCombinedObjectRecleanerHelper(self._helper_taus.cppImpl(),self._helper_jets.cppImpl(),self.cleanJetsWithFOTaus,btagL_thr,btagM_thr)
        for x in self.jetPts: self._worker.addJetPt(x)

        if "/fastCombinedObjectRecleanerMassVetoCalculator_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner mass and veto calculator module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerMassVetoCalculator.cxx+O" % os.environ['CMSSW_BASE'])
        self._workerMV = ROOT.fastCombinedObjectRecleanerMassVetoCalculator(self._helper_lepsF.cppImpl(),self._helper_lepsT.cppImpl(),doVetoZ,doVetoLMf,doVetoLMt)

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
        self._worker.setLeptons(self.nLepGood, self.LepGood_pt, self.LepGood_eta, self.LepGood_phi)
        self._worker.setTaus(self.nTauGood, self.TauGood_pt, self.TauGood_eta, self.TauGood_phi)
        self._worker.setJets(self.nJet, self.Jet_pt, self.Jet_eta, self.Jet_phi, self.Jet_btagCSV)
        self._workerMV.setLeptons(self.nLepGood, self.LepGood_pt, self.LepGood_eta, self.LepGood_phi, self.LepGood_mass, self.LepGood_pdgId)

    def listBranches(self):
        return self.branches

    def __call__(self,event):
        ## Init
        if any([x.initEvent(event) for x in self._helpers]):
            self.initReaders(event._tree)
            self.initWorkers()

        tags = getattr(event,'_CombinedTagsForCleaning%s'%self.inlabel)
        ret = {}
        ret['LepGood_conePt'] = [tags.leps_conept[i] for i in xrange(self.nLepGood.Get()[0])]

        self._worker.clear()
        self._worker.loadTags(tags,self.cleanTausWithLooseLeptons)
        self._worker.run()

        for x in self._worker.GetJetSums():
            for var in self._outjetvars: ret[var%x.thr+self.label]=getattr(x,var.replace('%d',''))

        self._workerMV.clear()
        self._workerMV.loadTags(tags)
        self._workerMV.run()

        masses = self._workerMV.GetPairMasses()
        for var in self.outmasses: ret[var+self.label] = getattr(masses,var)
        return ret

MODULES=[]
