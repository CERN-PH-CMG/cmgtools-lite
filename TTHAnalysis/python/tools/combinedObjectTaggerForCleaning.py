import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class CombinedObjectTaggerForCleaning(Module):

    def __init__(self,label,
                 looseLeptonSel = lambda l : True,
                 cleaningLeptonSel = lambda l : True,
                 FOLeptonSel = lambda l : True,
                 tightLeptonSel = lambda l : True,
                 FOTauSel = lambda t : True,
                 tightTauSel = lambda t : True,
                 selectJet = lambda j : True,
                 coneptdef = lambda l : l.pt,
                 debug=False):

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

    # interface for old code
    def listBranches(self):
        return []

    def __call__(self,event):
        from CMGTools.TTHAnalysis.treeReAnalyzer import Collection
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        taus = [t for t in Collection(event,"TauGood","nTauGood")]
        jets = [j for j in Collection(event,"Jet","nJet")]
        self.run(event, leps,taus,jets)
        return {}

    # interface for new code
    def analyze(self, event):
        from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
        leps = [l for l in Collection(event,"LepGood")]
        taus = [t for t in Collection(event,"Tau")]
        jets = [j for j in Collection(event,"Jet")]
        self.run(event, leps,taus,jets)
        return True

    def run(self, event, leps,taus,jets):

        tags = ROOT.CombinedObjectTags(len(leps),len(taus),len(jets))

        if not self.coneptdef: raise RuntimeError, 'Choose the definition to be used for cone pt'
        for lep in leps: lep.conept = self.coneptdef(lep)

        for i,lep in enumerate(leps):
            if self.looseLeptonSel(lep): tags.setLepFlags(i,True,self.cleanLeptonSel(lep),self.fkbleLeptonSel(lep),self.tightLeptonSel(lep),lep.conept)
        for i,tau in enumerate(taus):
            if self.fkbleTauSel(tau): tags.setTauFlags(i,True,self.tightTauSel(tau))
        for i,jet in enumerate(jets):
            if self.selectJet(jet): tags.setJetFlags(i,True)

        setattr(event,'_CombinedTagsForCleaning%s'%self.label,tags)
        return {}

MODULES=[]

if __name__ == '__main__':
    from CMGTools.TTHAnalysis.treeReAnalyzer import EventLoop
    from CMGTools.TTHAnalysis.treeReAnalyzer import Module as CMGModule
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(CMGModule):
        def __init__(self, name):
            CMGModule.__init__(self,name,None)
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
