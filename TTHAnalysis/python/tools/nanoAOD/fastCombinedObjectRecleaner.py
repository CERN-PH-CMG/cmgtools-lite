from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 


from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput
import ROOT, os
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

class fastCombinedObjectRecleaner(Module):
    def __init__(self,label,inlabel,cleanTausWithLooseLeptons,cleanJetsWithFOTaus,doVetoZ,doVetoLMf,doVetoLMt,jetPts,jetPtsFwd,btagL_thr,btagM_thr,jetCollection='Jet',jetBTag='btagDeepFlavB',tauCollection='Tau',isMC=None, 
                 variations=[]):

        self.label = "" if (label in ["",None]) else ("_"+label)
        self.inlabel = inlabel
        self.tauc = tauCollection
        self.jc = jetCollection

        self.cleanTausWithLooseLeptons = cleanTausWithLooseLeptons
        self.cleanJetsWithFOTaus = cleanJetsWithFOTaus
        self.jetPts = jetPts
        self.jetPtsFwd = jetPtsFwd
        self.jetBTag = jetBTag
        self.btagL_thr = btagL_thr
        self.btagM_thr = btagM_thr
        self.doVetoZ = doVetoZ
        self.doVetoLMf = doVetoLMf
        self.doVetoLMt = doVetoLMt
        if isMC is not None: 
            self.isMC = isMC
        self.variations = variations

    def initComponent(self, component):
        self.isMC = component.isMC

    def beginJob(self,histFile=None,histDirName=None):
        self.vars = ["eta","phi","mass"]
        self.vars_leptons = ["pdgId",'jetIdx','pt']
        self.vars_taus = ["pt"]
        self.vars_taus_int = ['jetIdx']
        self.vars_taus_uchar = ['idMVAoldDMdR032017v2','idDeepTau2017v2p1VSjet']
        self.vars_jets = [("pt","pt_nom") if self.isMC and len(self.variations) else 'pt',"btagDeepB","qgl",'btagDeepFlavB'] + [ 'pt_%s%s'%(x,y) for x in self.variations for y in ["Up","Down"]] #"btagCSVV2",,"btagDeepC"]#"btagCSV","btagDeepCSV",,"btagDeepCSVCvsL","btagDeepCSVCvsB","ptd","axis1"] # FIXME recover
        self.vars_jets_int = (["hadronFlavour"] if self.isMC else [])
        self.vars_jets_nooutput = []
        self.systsJEC = {0:""}
        if self.isMC:
            for sys in range(len(self.variations)):
                self.systsJEC[sys+1]    = '_' + self.variations[sys] + 'Up'
                self.systsJEC[-(sys+1)] = '_' + self.variations[sys] + 'Down'


        self.outmasses=['mZ1','minMllAFAS','minMllAFOS','minMllAFSS','minMllSFOS','mZ2','m4l']
        self._outjetvars = [x%self.jc for x in ['ht%s%%dj','mht%s%%d','nB%sLoose%%d','nB%sMedium%%d','n%s%%d']]
        self.outjetvars=[]
        for jetPt in self.jetPts: self.outjetvars.extend([(x%jetPt+y,'I' if ('nB%s'%self.jc in x or 'n%s'%self.jc in x) else 'F') for x in self._outjetvars for y in self.systsJEC.values()])
        self.outjetvars.extend([('nFwdJet'+self.systsJEC[y],'I') for y in self.systsJEC ])
        self.outjetvars.extend([(x+self.systsJEC[y],'F') for y in self.systsJEC for x in ['FwdJet1_pt','FwdJet1_eta'] ])

        self.branches = [var+self.label for var in self.outmasses]
        self.branches.extend([(var+self.label,_type) for var,_type in self.outjetvars])
        self.branches += [("LepGood_conePt","F",100,"nLepGood")]

        self._helper_lepsF = CollectionSkimmer("LepFO"+self.label, "LepGood", floats=[], maxSize=10, saveSelectedIndices=True,padSelectedIndicesWith=0)
        self._helper_lepsT = CollectionSkimmer("LepTight"+self.label, "LepGood", floats=[], maxSize=10, saveTagForAll=True)
        self._helper_taus = CollectionSkimmer("TauSel"+self.label, self.tauc, floats=self.vars+self.vars_taus, ints=self.vars_taus_int, uchars=self.vars_taus_uchar, maxSize=10)
        self._helper_jets = CollectionSkimmer("%sSel"%self.jc+self.label, self.jc, floats=self.vars+self.vars_jets, ints=self.vars_jets_int, maxSize=20)
        self._helpers = [self._helper_lepsF,self._helper_lepsT,self._helper_taus,self._helper_jets]

        if "/fastCombinedObjectRecleanerHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner worker module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerHelper.cxx+O" % os.environ['CMSSW_BASE'])
        self._worker = ROOT.fastCombinedObjectRecleanerHelper(self._helper_taus.cppImpl(),self._helper_jets.cppImpl(),self.cleanJetsWithFOTaus,self.btagL_thr,self.btagM_thr, True)
        for x in self.jetPts: self._worker.addJetPt(x)
        self._worker.setFwdPt(self.jetPtsFwd[0], self.jetPtsFwd[1])

        if "/fastCombinedObjectRecleanerMassVetoCalculator_cxx.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ recleaner mass and veto calculator module"
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/fastCombinedObjectRecleanerMassVetoCalculator.cxx+O" % os.environ['CMSSW_BASE'])
        self._workerMV = ROOT.fastCombinedObjectRecleanerMassVetoCalculator(self._helper_lepsF.cppImpl(),self._helper_lepsT.cppImpl(),self.doVetoZ,self.doVetoLMf,self.doVetoLMt)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        for x in self._helpers:
            x.initInputTree(inputTree)
        self.initReaders(inputTree)
        self.initWorkers()
        declareOutput(self, wrappedOutputTree, self.branches)
        for x in self._helpers: 
            x.initOutputTree(wrappedOutputTree.tree(), True);

    def initReaders(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for coll in ["LepGood",self.tauc,self.jc]:
            setattr(self,'n'+coll,tree.valueReader('n'+coll))
            _vars = self.vars[:]
            if coll=='LepGood': _vars.extend(self.vars_leptons)
            if coll==self.tauc: _vars.extend(self.vars_taus+self.vars_taus_int+self.vars_taus_uchar)
            if coll==self.jc: _vars.extend(self.vars_jets+self.vars_jets_int+self.vars_jets_nooutput)
            for B in _vars:
                if type(B) == tuple:
                    setattr(self,"%s_%s"%(coll,B[0]), tree.arrayReader("%s_%s"%(coll,B[1])))
                else:
                    setattr(self,"%s_%s"%(coll,B), tree.arrayReader("%s_%s"%(coll,B)))
        return True

    def initWorkers(self):
        self._worker.setLeptons(self.nLepGood, self.LepGood_pt, self.LepGood_eta, self.LepGood_phi, self.LepGood_jetIdx)
        self._worker.setTaus(getattr(self,'n%s'%self.tauc),getattr(self,'%s_pt'%self.tauc),getattr(self,'%s_eta'%self.tauc),getattr(self,'%s_phi'%self.tauc), getattr(self,'%s_jetIdx'%self.tauc))
        jecs= ROOT.vector("TTreeReaderArray<float>*")()
        if self.isMC and len(self.variations):
            for var in self.variations:
                jecs.push_back( getattr(self, '%s_pt_%sUp'%(self.jc, var)))
                jecs.push_back( getattr(self, '%s_pt_%sDown'%(self.jc, var)))

        self._worker.setJets(getattr(self,'n%s'%self.jc),getattr(self,'%s_pt'%self.jc),getattr(self,'%s_eta'%self.jc),getattr(self,'%s_phi'%self.jc), # Jet pt has already been replaced by Jet_pt_nom in mc above
                             getattr(self,'%s_%s'%(self.jc,self.jetBTag)),
                             jecs
                         )
        
        self._workerMV.setLeptons(self.nLepGood, self.LepGood_pt, self.LepGood_eta, self.LepGood_phi, self.LepGood_mass, self.LepGood_pdgId)

    def analyze(self, event):
        # Init
        wpL = _btagWPs["DeepFlav_%d_%s"%(event.year,"L")][1]
        wpM = _btagWPs["DeepFlav_%d_%s"%(event.year,"M")][1]
        if self._ttreereaderversion != event._tree._ttreereaderversion:
            for x in self._helpers: x.initInputTree(event._tree)
            self.initReaders(event._tree)
            self.initWorkers()

        for x in self._helpers: x.clear()

        tags = getattr(event,'_CombinedTagsForCleaning%s'%self.inlabel)
        self.wrappedOutputTree.fillBranch('LepGood_conePt', [tags.leps_conept[i] for i in xrange(self.nLepGood.Get()[0])])


        self._worker.clear()
        self._worker.loadTags(tags,self.cleanTausWithLooseLeptons, wpL, wpM)
        self._worker.run()

        for delta,varname in self.systsJEC.iteritems():
            for x in self._worker.GetJetSums(delta):
                for var in self._outjetvars: 
                    self.wrappedOutputTree.fillBranch(var%x.thr+varname+self.label, getattr(x,var.replace('%d','').replace(self.jc,'Jet')))
                self.wrappedOutputTree.fillBranch('nFwdJet'+varname+self.label,getattr(x,'nFwdJet'))
                self.wrappedOutputTree.fillBranch('FwdJet1_pt'+varname+self.label,getattr(x,'fwd1_pt'))
                self.wrappedOutputTree.fillBranch('FwdJet1_eta'+varname+self.label,getattr(x,'fwd1_eta'))

        self._workerMV.clear()
        self._workerMV.loadTags(tags)
        self._workerMV.run()

        masses = self._workerMV.GetPairMasses()
        for var in self.outmasses: 
            self.wrappedOutputTree.fillBranch(var+self.label, getattr(masses,var))

        return True
