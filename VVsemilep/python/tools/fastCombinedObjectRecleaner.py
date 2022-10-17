from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class fastCombinedObjectRecleaner:

    def __init__(self,label,inlabel,cleanTausWithLooseLeptons,cleanJetsWithFOTaus,doVetoZ,doVetoLMf,doVetoLMt,jetPts,btagL_thr,btagM_thr,jetCollection='Jet',isMC=True):

        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inlabel = inlabel

        self.vars = ["pt","eta","phi","mass"]
        self.vars_leptons = ["pdgId"]
        self.vars_taus = ["mvaId2017"]
        self.vars_taus_int = ["idMVAdR03"]
        self.vars_jets = ["btagCSV","btagDeepCSV","qgl","btagDeepCSVCvsL","btagDeepCSVCvsB","ptd","axis1","corr","corr_JECUp","corr_JECDown"]
        self.vars_jets_int = ["mult"]+(["hadronFlavour"] if isMC else [])
        self.vars_jets_nooutput = []
        self.jc = jetCollection

        self.cleanTausWithLooseLeptons = cleanTausWithLooseLeptons
        self.cleanJetsWithFOTaus = cleanJetsWithFOTaus
        self.jetPts = jetPts

        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}

        self.outmasses=['mZ1','minMllAFAS','minMllAFOS','minMllAFSS','minMllSFOS','mZ2','m4l']
        self._outjetvars = [x%self.jc for x in ['ht%s%%dj','mht%s%%d','nB%sLoose%%d','nB%sMedium%%d','n%s%%d']]
        self.outjetvars=[]
        for jetPt in self.jetPts: self.outjetvars.extend([(x%jetPt+y,'I' if ('nB%s'%self.jc in x or 'n%s'%self.jc in x) else 'F') for x in self._outjetvars for y in self.systsJEC.values()])
        self.branches = [var+self.label for var in self.outmasses]
        self.branches.extend([(var+self.label,_type) for var,_type in self.outjetvars])
        self.branches += [("LepGood_conePt","F",20,"nLepGood")]

        self._helper_lepsF = CollectionSkimmer("LepFO"+self.label, "LepGood", floats=[], maxSize=20, saveSelectedIndices=True,padSelectedIndicesWith=0)
        self._helper_lepsT = CollectionSkimmer("LepTight"+self.label, "LepGood", floats=[], maxSize=20, saveTagForAll=True)
        self._helper_taus = CollectionSkimmer("TauSel"+self.label, "TauGood", floats=self.vars+self.vars_taus, ints=self.vars_taus_int, maxSize=20)
        self._helper_jets = CollectionSkimmer("%sSel"%self.jc+self.label, self.jc, floats=self.vars+self.vars_jets, ints=self.vars_jets_int, maxSize=20)
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
        for coll in ["LepGood","TauGood",self.jc]:
            setattr(self,'n'+coll,tree.valueReader('n'+coll))
            _vars = self.vars[:]
            if coll=='LepGood': _vars.extend(self.vars_leptons)
            if coll=='TauGood': _vars.extend(self.vars_taus+self.vars_taus_int)
            if coll==self.jc: _vars.extend(self.vars_jets+self.vars_jets_int+self.vars_jets_nooutput)
            for B in _vars:
                setattr(self,"%s_%s"%(coll,B), tree.arrayReader("%s_%s"%(coll,B)))

    def initWorkers(self):
        self._worker.setLeptons(self.nLepGood, self.LepGood_pt, self.LepGood_eta, self.LepGood_phi)
        self._worker.setTaus(self.nTauGood, self.TauGood_pt, self.TauGood_eta, self.TauGood_phi)
        self._worker.setJets(getattr(self,'n%s'%self.jc),getattr(self,'%s_pt'%self.jc),getattr(self,'%s_eta'%self.jc),getattr(self,'%s_phi'%self.jc),
                             getattr(self,'%s_btagDeepCSV'%self.jc),getattr(self,'%s_corr'%self.jc),getattr(self,'%s_corr_JECUp'%self.jc),getattr(self,'%s_corr_JECDown'%self.jc))
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

        for delta,varname in self.systsJEC.iteritems():
            for x in self._worker.GetJetSums(delta):
                for var in self._outjetvars: ret[var%x.thr+varname+self.label]=getattr(x,var.replace('%d','').replace(self.jc,'Jet'))

        self._workerMV.clear()
        self._workerMV.loadTags(tags)
        self._workerMV.run()

        masses = self._workerMV.GetPairMasses()
        for var in self.outmasses: ret[var+self.label] = getattr(masses,var)
        return ret

MODULES=[]
