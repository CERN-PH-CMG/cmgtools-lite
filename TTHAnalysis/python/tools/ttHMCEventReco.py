from CMGTools.TTHAnalysis.treeReAnalyzer import Collection, deltaR
from CMGTools.TTHAnalysis.tools.collectionSkimmer import CollectionSkimmer
import ROOT, os

class TTHMCEventReco:
    def __init__(self,label=""):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.floats = ["pt","eta","phi","mass"]
        self.ints = ['pdgId']
        if "/jetReCleanerExampleHelper_cxx.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/tools/jetReCleanerExampleHelper.cxx+" % os.environ['CMSSW_BASE'])
        self._helpers = []
    def init(self,tree):
        for v in self.floats+self.ints:
            if not tree.GetBranch("GenPart_"+v): print "Missing branch GenPart_"+v
        self.floats = [v for v in self.floats if tree.GetBranch("GenPart_"+v)]
        self.ints   = [v for v in self.ints   if tree.GetBranch("GenPart_"+v)]

        self.collections = ['Higgs','Top','ATop','bFromTop','WFromTop','bFromATop','WFromATop',
                            'dFromWFromTop','dFromWFromATop','dDirectFromHiggs','dAllFromHiggs',
                            'dFromOnShellVFromHiggs','dFromOffShellVFromHiggs','allFinalParton']

        for x in self.collections:
            cs = CollectionSkimmer(x+self.label, "GenPart", floats=self.floats, ints=self.ints, saveSelectedIndices=True, saveTagForAll=True, maxSize=50)
            setattr(self,'_h_%s'%x,cs)
            self._helpers.append(cs)
        for x in self._helpers:
            x.initInputTree(tree)
            x.initOutputTree(self._out)
        self.initReaders(tree)
    def listBranches(self):
        return []
    def initReaders(self,tree):
        for B in "nGenPart", : setattr(self, B, tree.valueReader(B))
        for B in "pdgId", "motherIndex", "status", "motherId", "mass" : setattr(self,B, tree.arrayReader("GenPart_"+B))
    def setOutputTree(self,pytree):
        self._out = pytree
    def __call__(self,event):
        allinits = [x.initEvent(event) for x in self._helpers]
        if any(allinits):
            self.initReaders(event._tree)

        for x in self.collections:
            setattr(self,'_%s'%x,[])

        for i in xrange(self.nGenPart.Get()[0]):
            if self.pdgId[i]==25 and self.status[i]==62: self._Higgs.append(i)
            elif self.pdgId[i]==6 and self.status[i]==62: self._Top.append(i)
            elif self.pdgId[i]==-6 and self.status[i]==62: self._ATop.append(i)
        for i in xrange(self.nGenPart.Get()[0]):
            if self.pdgId[i]==5 and self.motherIndex[i] in self._Top: self._bFromTop.append(i)
            elif self.pdgId[i]==24 and self.motherIndex[i] in self._Top: self._WFromTop.append(i)
            elif self.pdgId[i]==-5 and self.motherIndex[i] in self._ATop: self._bFromATop.append(i)
            elif self.pdgId[i]==-24 and self.motherIndex[i] in self._ATop: self._WFromATop.append(i)
            elif self.motherIndex[i] in self._Higgs: self._dDirectFromHiggs.append(i)
        for i in xrange(self.nGenPart.Get()[0]):
            if self.motherIndex[i] in self._WFromTop: self._dFromWFromTop.append(i)
            elif self.motherIndex[i] in self._WFromATop: self._dFromWFromATop.append(i)
            elif abs(self.motherId[i]) in (23,24) and self.motherIndex[i] in self._dDirectFromHiggs: self._dAllFromHiggs.append(i)
            elif abs(self.pdgId[i]) not in (23,24) and i in self._dDirectFromHiggs: self._dAllFromHiggs.append(i)
        if len(self._dDirectFromHiggs)>=2 and abs(self.pdgId[self._dDirectFromHiggs[0]]) in (23,24):
            i1 = self._dDirectFromHiggs[0] if self.mass[self._dDirectFromHiggs[0]]>=self.mass[self._dDirectFromHiggs[1]] else self._dDirectFromHiggs[1]
            for i in self._dAllFromHiggs:
                if self.motherIndex[i]==i1: self._dFromOnShellVFromHiggs.append(i)
                else: self._dFromOffShellVFromHiggs.append(i)
        self._allFinalParton = list(set(self._dAllFromHiggs+self._dFromWFromTop+self._dFromWFromATop+self._bFromTop+self._bFromATop))

        for x in self.collections:
            getattr(self,'_h_%s'%x).push_back_all(getattr(self,'_%s'%x))

        return {}
