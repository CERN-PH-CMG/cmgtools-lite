import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from CMGTools.MonoXAnalysis.postprocessing.framework.datamodel import Collection 
from CMGTools.MonoXAnalysis.postprocessing.framework.eventloop import Module
from PhysicsTools.HeppyCore.utils.deltar import deltaR

class lepIsoEAProducer(Module):
    def __init__(self,EAfile,rho='rho'):
        self.rho = rho
        self.EAinputfile = EAfile
        if "/EffectiveAreas_cc.so" not in ROOT.gSystem.GetLibraries():
            ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/MonoXAnalysis/python/postprocessing/helpers/EffectiveAreas.cc+" % os.environ['CMSSW_BASE'])
    def beginJob(self):
        self._worker = ROOT.EffectiveAreas(self.EAinputfile)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("LepGood_relIso04EA", "F", lenVar="nLepGood")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leps = Collection(event, "LepGood")
        iso = []
        for l in leps:
            if abs(l.pdgId)!=11: # implemented only for electrons
                iso.append(-1000) 
            else:
                eA = self._worker.getEffectiveArea(abs(l.eta))
                rho = getattr(event,self.rho)
                # approximation, since we don't have the three components of the isolation
                # should be chad + max(0.0, nhad + pho - rho*eA)
                iso.append((l.relIso04*l.pt - rho*eA)/l.pt) 
                # print "eta=%f,pt=%f,eA=%f,rho=%f,reliso=%f,relisocorr=%f" % (l.eta,l.pt,eA,rho,l.relIso04,(l.relIso04*l.pt - rho*eA)/l.pt)
        self.out.fillBranch("LepGood_relIso04EA", iso)
        return True

class lepAwayJetProducer(Module):
    def __init__(self, lepSel = lambda lep: True, jetSel = lambda jet : True, pairSel = lambda lep, jet : True):
        self.lepSel = lepSel
        self.jetSel = jetSel
        self.pairSel = pairSel
        self.jetSort = lambda jet: jet.pt 
        self.vars = ("pt","eta","phi")
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for V in self.vars:
            self.out.branch("LepGood_awayJet_"+V, "F", lenVar="nLepGood")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        leps = filter(self.lepSel, Collection(event, "LepGood"))
        jets = filter(self.jetSel, Collection(event, "Jet"))
        jets.sort(key = self.jetSort, reverse=True)
        ret = {}
        for V in self.vars: ret[V] = []
        for lep in leps: lep.awayJet = None
        for lep in leps:
            for jet in jets:
                if self.pairSel(lep,jet):
                    lep.awayJet = jet
                    break
            for V in self.vars: 
                ret[V].append(getattr(lep.awayJet,V) if lep.awayJet else 0)
        for V in self.vars:
            self.out.fillBranch("LepGood_awayJet_"+V,ret[V])
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

eleRelIsoEA = lambda : lepIsoEAProducer("%s/src/RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt" % os.environ['CMSSW_BASE'])
lepQCDAwayJet = lambda : lepAwayJetProducer(jetSel = lambda jet : jet.pt > 30 and abs(jet.eta) < 2.4,
                                            pairSel =lambda lep, jet: deltaR(lep.eta,lep.phi, jet.eta, jet.phi) > 0.7)
