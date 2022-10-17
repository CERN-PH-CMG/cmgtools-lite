from CMGTools.TTHAnalysis.treeReAnalyzer import *
import itertools

class HadTopSimple:
    def __init__(self, label="", recllabel='Recl'):
        self.namebranches = [ "bJet_fromHadTop_CSV", "lJet_fromHadTop_CSV2", "HadTop_Mass",
                              "HadTop_Pt", "W_fromHadTop_Mass", "bJet_notFromHadTop_CSV"]
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.inputlabel = '_'+recllabel
        self.branches = []
        for var in self.systsJEC: self.branches.extend([br+self.label+self.systsJEC[var] for br in self.namebranches])
    def listBranches(self):
        return self.branches[:]
    def __call__(self,event):

        allret = {}

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iF"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]): _var = 0
            jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
            _ijets_list = getattr(event,"iJSel"+self.inputlabel+self.systsJEC[_var])
            _ijets = [ij for ij in _ijets_list]
            jets = [ (jetsc[ij] if ij>=0 else jetsd[-ij-1]) for ij in _ijets]

            # prepare output
            ret = dict([(name,0.0) for name in self.namebranches])

            best_top = None
            best_top_p4 = None
            best_top_mass = -999

            for j1,j2,j3 in itertools.combinations(jets,3):
                best_btag = max(j1.btagCSV,j2.btagCSV,j3.btagCSV)
                if best_btag < 0.46: continue
                top_p4 = j1.p4() + j2.p4() + j3.p4()
                top_mass = top_p4.M()
                if abs(top_mass-172) < abs(best_top_mass-172):
                    best_top_mass = top_mass
                    best_top_p4 = top_p4
                    best_top = sorted([j1,j2,j3], key = lambda x : x.btagCSV, reverse=True)
                    
            if best_top:
                j1,j2,j3 = best_top
                ret["bJet_fromHadTop_CSV"] = j1.btagCSV
                ret["lJet_fromHadTop_CSV2"] = j3.btagCSV
                ret["HadTop_Mass"] = best_top_mass
                ret["HadTop_Pt"] = best_top_p4.Pt()
                ret["W_fromHadTop_Mass"] = (j2.p4()+j3.p4()).M()
                other_btags = [j.btagCSV for j in itertools.ifilterfalse(lambda x : x in best_top, jets)]
                if len(other_btags)>0: ret["bJet_notFromHadTop_CSV"] = max(other_btags)


            for br in self.namebranches:
                allret[br+self.label+self.systsJEC[var]] = ret[br]
	 	
	return allret


if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t",argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = HadTopSimple('','Recl')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
