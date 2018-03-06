#### A python framework for event, collection and object based analysis
#### whose source fits a two python files (but is faster than the old treeReAnalyzer)

from math import *
from array import array
## safe batch mode
import sys
args = sys.argv[:]
sys.argv = ['-b']
import ROOT
sys.argv = args
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

import time

import CMGTools.TTHAnalysis.tools.treeReaderArrayTools as TRAT 

#### ========= EDM/FRAMEWORK =======================
class Event:
    def __init__(self,tree,entry):
        self._tree = tree
        self._entry = entry
        self._sync()
    def _sync(self):
        self._tree.gotoEntry(self._entry)
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        return TRAT.readBranch(self._tree, name)
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def eval(self,expr):
        if not hasattr(self._tree, '_exprs'):
            self._tree._exprs = {}
            # remove useless warning about EvalInstance()
            import warnings
            warnings.filterwarnings(action='ignore', category=RuntimeWarning, 
                                    message='creating converter for unknown type "const char\*\*"$')
            warnings.filterwarnings(action='ignore', category=RuntimeWarning, 
                                    message='creating converter for unknown type "const char\*\[\]"$')
        if expr not in self._tree._exprs:
            formula = ROOT.TTreeFormula(expr,expr,self._tree)
            if formula.IsInteger():
                formula.go = formula.EvalInstance64
            else:
                formula.go = formula.EvalInstance
            self._tree._exprs[expr] = formula
            # force sync, to be safe
            self._tree.GetEntry(self._entry)
            self._tree.entry = self._entry
            #self._tree._exprs[expr].SetQuickLoad(False)
        else:
            self._sync()
            formula = self._tree._exprs[expr]
        if "[" in expr: # unclear why this is needed, but otherwise for some arrays x[i] == 0 for all i > 0
            formula.GetNdata()
        return formula.go()
            

class Object:
    def __init__(self,event,prefix,index=None):
        self._event = event
        self._prefix = prefix+"_"
        self._index = index
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        if name[:2] == "__" and name[-2:] == "__":
            raise AttributeError
        if name == "pdgLabel": return self.pdgLabel_()
        val = getattr(self._event,self._prefix+name)
        if self._index != None:
            val = val[self._index]
        self.__dict__[name] = val ## cache
        return val
    def __getitem__(self,attr):
        return self.__getattr__(attr)
    def pdgLabel_(self):
        if self.pdgId == +13: return "#mu-";
        if self.pdgId == -13: return "#mu+";
        if self.pdgId == +11: return "e-";
        if self.pdgId == -11: return "e+";
    def p4(self):
        ret = ROOT.TLorentzVector()
        ret.SetPtEtaPhiM(self.pt,self.eta,self.phi,self.mass)
        return ret
    def subObj(self,prefix):
        return Object(self._event,self._prefix+prefix)
    def __repr__(self):
        return ("<%s[%s]>" % (self._prefix[:-1],self._index)) if self._index != None else ("<%s>" % self._prefix[:-1])
    def __str__(self):
        return self.__repr__()

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection
from CMGTools.TTHAnalysis.treeReAnalyzer import Module

class EventLoop:
    def __init__(self,modules):
        self._modules = modules
        self._doneEvents = 0
    def loop(self,trees,maxEvents=-1,cut=None,eventRange=None):
        modules = self._modules
        for m in modules: m.beginJob()
        if type(trees) != list: trees = [ trees ]
        t0 = time.clock(); tlast = t0
        for tree in trees:
            TRAT.initTree(tree)
            for m in modules: m.init(tree)
            for i in xrange(tree.GetEntries()) if eventRange == None else eventRange:
                if maxEvents > 0 and i >= maxEvents-1: break
                e = Event(tree,i)
                if cut != None:
                    evno = e.evt # force some eval of a plain branch (apparently this is needed)
                    cutres = e.eval(cut)
                    if not cutres: continue
                ret = True
                for m in modules: 
                    ret = m.analyze(e)
                    if ret == False: break
                self._doneEvents += 1
                if i > 0 and i % 10000 == 0:
                    t1 = time.clock()
                    print "Processed %8d/%8d entries of this tree (elapsed time %7.1fs, curr speed %8.3f kHz, avg speed %8.3f kHz)" % (i,tree.GetEntries(),t1-t0,(10.000)/(max(t1-tlast,1e-9)),i/1000./(max(t1-t0,1e-9)))
                    tlast = t1
        for m in modules: m.endJob()
    def beginComponent(self,component):
        for m in self._modules: m.beginComponent(component)
    def endComponent(self,component):
        for m in self._modules: m.endComponent(component)

from CMGTools.TTHAnalysis.treeReAnalyzer import PyTree, BookDir, Booker
from CMGTools.TTHAnalysis.treeReAnalyzer import deltaPhi, deltaR, closest 

#### ========= TEST =======================
if __name__ == '__main__':
    class DummyModule(Module):
        def beginJob(self):
            self.maxEta = self.book("TH1F","maxEta","maxEta",20,0.,5.0)
            print "Booked histogram 'maxEta'"
        def analyze(self,event):
            genB = Collection(event,"LepGood")  
            print "Number of leptons: %d" % len(genB)
            jetB = Collection(event,"Jet")  
            print "Number of jets: %d" % len(jetB)
            #if not event.eval("nJet == 5"): return False
            for i in xrange(len(genB)):
                print "eta of leptons #%d: %+5.3f" % (i+1, genB[i].eta)
            print ""
            maxEta = max([abs(gb.eta) for gb in genB])
            self.maxEta.Fill(maxEta)
    from sys import argv
    f = ROOT.TFile(argv[1])
    t = f.Get("tree")
    t.vectorTree = True
    booker = Booker("test.root")
    el = EventLoop([DummyModule("dummy",booker)])
    el.loop(t,1000)
    booker.done()
    print "Wrote to test.root"

