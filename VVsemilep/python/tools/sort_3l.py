from CMGTools.TTHAnalysis.treeReAnalyzer import *

class Sort3L:
    def __init__(self, label="", recllabel='Recl'):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
 	self.branches = [ "iJetByCSV_0"+self.systsJEC[x]+self.label for x in self.systsJEC ]
        self.inputlabel = '_'+recllabel
    def listBranches(self):
        return self.branches[:]	
    def __call__(self,event):
        ret = {}
        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]): _var = 0
            jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
            ijs = [ij for ij in getattr(event,"iJ"+self.systsJEC[_var]+self.inputlabel)]
            btags = [ (jetsc[ij].btagCSV if ij>=0 else jetsd[-ij-1].btagCSV) for ij in ijs ]
            ret["iJetByCSV_0"+self.systsJEC[var]+self.label] = ijs[btags.index(max(btags))] if len(ijs)>0 else -99
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2])
    print tree.GetEntries()
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = Sort3L("testSort3L","Recl")
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
