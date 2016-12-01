from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT

class CombinedObjectTagsForCleaning:
    def __init__(self,label):
        self.label = label
    def __str__(self):
        return str(self.__dict__)

class CombinedObjectTaggerForCleaning:

    def __init__(self,label,looseLeptonSel,cleaningLeptonSel,FOLeptonSel,tightLeptonSel,FOTauSel,tightTauSel,selectJet,coneptdef,debug=False):
        self.label = "" if (label in ["",None]) else ("_"+label)

        self.looseLeptonSel = looseLeptonSel
        self.cleanLeptonSel = cleaningLeptonSel # applied on top of looseLeptonSel
        self.fkbleLeptonSel = FOLeptonSel # applied on top of looseLeptonSel
        self.tightLeptonSel = tightLeptonSel # applied on top of looseLeptonSel

        self.fkbleTauSel = FOTauSel
        self.tightTauSel = tightTauSel # applied on top of FOTauSel

        self.selectJet = selectJet

        self.coneptdef = coneptdef
        self.debug = debug

    def listBranches(self):
        return []

    def __call__(self,event):

        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        taus = [t for t in Collection(event,"TauGood","nTauGood")]
        jets = [j for j in Collection(event,"Jet","nJet")]

        tags = CombinedObjectTagsForCleaning(self.label)

        if not self.coneptdef: raise RuntimeError, 'Choose the definition to be used for cone pt'
        for lep in leps: lep.conept = self.coneptdef(lep)
        tags.conept = [lep.conept for lep in leps]

        tags.lepsL= [j for j,obj in filter(lambda (i,lep) : self.looseLeptonSel(lep), enumerate(leps))]
        tags.lepsC= [j for j,obj in filter(lambda (i,lep) : (i in tags.lepsL) and self.cleanLeptonSel(lep), enumerate(leps))]
        tags.lepsF= [j for j,obj in filter(lambda (i,lep) : (i in tags.lepsL) and self.fkbleLeptonSel(lep), enumerate(leps))]
        tags.lepsT= [j for j,obj in filter(lambda (i,lep) : (i in tags.lepsL) and self.tightLeptonSel(lep), enumerate(leps))]
        tags.tausF= [j for j,obj in filter(lambda (i,tau) : self.fkbleTauSel(tau), enumerate(taus))]
        tags.tausT= [j for j,obj in filter(lambda (i,tau) : (i in tags.tausF) and self.tightTauSel(tau), enumerate(taus))]
        tags.jetsS= [j for j,obj in filter(lambda (i,jet) : self.selectJet(jet), enumerate(jets))]

        lepsF_sorted = [_idx for _cpt,_idx in sorted([(tags.conept[i],i) for i in tags.lepsF], reverse=True)]
        tags.lepsF = lepsF_sorted

        setattr(event,'_CombinedTagsForCleaning%s'%self.label,tags)
        if self.debug: print tags
        return {}

MODULES=[]

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = CombinedObjectTaggerForCleaning("Test",
                                                       looseLeptonSel = lambda lep : lep.miniRelIso < 0.4 and lep.sip3d < 8,
                                                       cleaningLeptonSel = lambda lep : True, # cuts applied on top of loose
                                                       FOLeptonSel = lambda lep : lep.conept>10 and lep.jetBTagCSV<0.80, # cuts applied on top of loose
                                                       tightLeptonSel = lambda lep : lep.conept>10 and lep.jetBTagCSV<0.80 and lep.mvaTTH > 0.75, # cuts applied on top of loose
                                                       FOTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and tau.idMVAOldDMRun2dR03 >= 1,
                                                       tightTauSel = lambda tau: tau.idMVAOldDMRun2dR03 >= 2, # cuts applied on top of FO tau
                                                       selectJet = lambda jet: abs(jet.eta)<2.4,
                                                       coneptdef = lambda lep: lep.pt,
                                                       debug = True)
        def analyze(self,ev):
            self.sf1(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
