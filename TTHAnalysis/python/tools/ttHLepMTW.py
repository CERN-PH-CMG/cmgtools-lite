from CMGTools.TTHAnalysis.treeReAnalyzer import *

from math import sqrt, cos

class ttHLepMTW:
    def __init__(self, recllabel='Recl'):
        self.inputlabel = '_'+recllabel
    def listBranches(self):
        return ["bestMTW3l"]
    def __call__(self,event):
        ret = { "bestMTW3l":-99 }

        nFO = getattr(event,"nLepFO"+self.inputlabel)
        if nFO < 3: return ret

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        l1,l2,l3 = leps[:3]
        bestDM = 9e9
        for i1,i2,i3 in (l1,l2,l3),(l2,l3,l1),(l3,l1,l2):
            if i1.pdgId != -i2.pdgId: continue
            m12 = (i1.p4()+i2.p4()).M()
            if abs(m12 - 91.188) < bestDM:
                bestDM = abs(m12 - 91.188)
                ret["bestMTW3l"] = 2*sqrt( i3.pt * event.met_pt * (1 - cos(i3.phi - event.met_phi) ) )

        return ret
        
if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t", argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = ttHLepMTW()
        def analyze(self,ev):
            self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)

MODULES = [ 
    ( 'bestMTW3l', lambda : ttHLepMTW() ),
]
