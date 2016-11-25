from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT

class CombinedObjectTagsForCleaning:
    def __init__(self,label):
        self.label = label
    def __str__(self):
        return str(self.__dict__)

class CombinedObjectTaggerForCleaning:

    def __init__(self,label,looseLeptonSel,cleaningLeptonSel,FOLeptonSel,tightLeptonSel,cleaningTauSel,FOTauSel,tightTauSel,selectJet,coneptdef,debug=False):
        self.label = "" if (label in ["",None]) else ("_"+label)

        self.looseLeptonSel = looseLeptonSel
        self.cleanLeptonSel = lambda x : self.looseLeptonSel(x) and cleaningLeptonSel(x) # applied on top of looseLeptonSel
        self.fkbleLeptonSel = lambda x : self.looseLeptonSel(x) and FOLeptonSel(x) # applied on top of looseLeptonSel
        self.tightLeptonSel = lambda x : self.looseLeptonSel(x) and tightLeptonSel(x) # applied on top of looseLeptonSel

        self.cleanTauSel = cleaningTauSel
        self.fkbleTauSel = lambda x : self.cleanTauSel(x) and FOTauSel(x) # applied on top of cleaningTauSel
        self.tightTauSel = lambda x : self.cleanTauSel(x) and tightTauSel(x) # applied on top of cleaningTauSel

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

        tags.lepsL= [self.looseLeptonSel(lep) for lep in leps]
        tags.lepsC= [self.cleanLeptonSel(lep) for lep in leps]
        tags.lepsF= [self.fkbleLeptonSel(lep) for lep in leps]
        tags.lepsT= [self.tightLeptonSel(lep) for lep in leps]
        tags.tausC= [self.cleanTauSel(tau) for tau in taus]
        tags.tausF= [self.fkbleTauSel(tau) for tau in taus]
        tags.tausT= [self.tightTauSel(tau) for tau in taus]
        tags.jetsS= [self.selectJet(jet) for jet in jets]

        setattr(event,'_CombinedTagsForCleaning%s'%self.label,tags)
        if self.debug: print tags
        return []

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
                                                       cleaningTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and tau.idMVAOldDMRun2dR03 >= 1,
                                                       FOTauSel = lambda tau: True, # cuts applied on top of cleaning
                                                       tightTauSel = lambda tau: tau.idMVAOldDMRun2dR03 >= 2, # cuts applied on top of cleaning
                                                       selectJet = lambda jet: abs(jet.eta)<2.4,
                                                       coneptdef = lambda lep: lep.pt,
                                                       debug = True)
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            self.sf1(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
