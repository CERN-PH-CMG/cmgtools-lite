from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.TTHAnalysis.tools.mvaTool import *

def mL4(ev): 
    all_leps = [l for l in Collection(ev,"LepGood")]
    nFO = getattr(ev,"nLepFO_Recl")
    chosen = getattr(ev,"iLepFO_Recl")
    leps = [all_leps[chosen[i]] for i in xrange(nFO)]
    if len(leps) < 4: return 0
    leps = leps[:4]
    min_mass = 999999
    for i1,l1 in enumerate(leps): 
        for i2,l2 in enumerate(leps): 
            if i1<=i2: continue
            mass = (l1.p4()+l2.p4()).M()
            if mass < min_mass: 
                min_mass = mass
    return min_mass
            
    

class FinalMVA_4L(Module):
    def __init__(self):
        self._MVAs = {}
        self._vars = [
            MVAVar("lep1_conePt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[0])]) if ev.nLepFO_Recl >= 1 else 0),
            MVAVar("lep2_conePt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[1])]) if ev.nLepFO_Recl >= 2 else 0),
            MVAVar("lep3_conePt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[2])]) if ev.nLepFO_Recl >= 3 else 0),
            MVAVar("lep4_conePt", func = lambda ev : (ev.LepGood_conePt[int(ev.iLepFO_Recl[3])]) if ev.nLepFO_Recl >= 4 else 0),
            MVAVar("massL4"     , func = lambda ev : mL4(ev)),
            MVAVar("met_LD"     , func = lambda ev : (ev.MET_pt if ev.year != 2017 else ev.METFixEE2017_pt) *0.6 + ev.mhtJet25_Recl*0.4),
            MVAVar("has_SFOS"   , func = lambda ev : ev.hasOSSF4l),
            
        ]
        P = os.environ["CMSSW_BASE"] + '/src/CMGTools/TTHAnalysis/data/kinMVA/tth/4l_0tau_3.xml' 
        self._MVAs["FinalMVA_4L_BDTG"] = MVATool("BDTG", P, self._vars) 
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        for out in self._MVAs.keys():
            self.wrappedOutputTree.branch(out,'F')

    def analyze(self, event):
        myvars = [event.iLepFO_Recl[0],event.iLepFO_Recl[1],event.iLepFO_Recl[2]]
        writeOutput(self, dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()]))
        return True

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("ttHLepTreeProducerBase")
    #tree.AddFriend("sf/t", argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = FinalMVA_3L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

