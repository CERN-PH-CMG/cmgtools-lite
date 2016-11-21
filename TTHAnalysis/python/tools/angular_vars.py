from CMGTools.TTHAnalysis.treeReAnalyzer import *

class angular_vars:
    def __init__(self, label="", recllabel='Recl'):
        self.namebranches = [ "L_phi", 
                              "B_loose_phi", "B_medium_phi", "B_tight_phi", 
                              "DR_l_b_loose1", "DR_l_b_medium1", "DR_l_b_tight1", 
                              "DR_l_b_loose2", "DR_l_b_medium2", "DR_l_b_tight2",
                              "pTl_DR_l_b_loose1", "pTl_DR_l_b_medium1", "pTl_DR_l_b_tight1", 
                              "pTl_DR_l_b_loose2", "pTl_DR_l_b_medium2", "pTl_DR_l_b_tight2",  
                              "L_pt" ]
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.inputlabel = '_'+recllabel
        self.branches = []
        for var in self.systsJEC: self.branches.extend([br+self.systsJEC[var]+self.label for br in self.namebranches])
        self.branches.extend([("iF%s_%d"%(self.inputlabel,i)+self.label,"I") for i in xrange(8)])
    def listBranches(self):
        return self.branches[:]	
    def __call__(self,event):

        allret = {}

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        chosen = getattr(event,"iF"+self.inputlabel)
        for i in xrange(8): allret["iF%s_%d"%(self.inputlabel,i)+self.label] = chosen[i] if i<nFO else 0
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        for var in self.systsJEC:
            _var = var
            if not hasattr(event,"nJet"+self.systsJEC[var]): _var = 0
            jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
            jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
            _ijets_list = getattr(event,"iJ"+self.systsJEC[_var]+self.inputlabel)
            _ijets = [ij for ij in _ijets_list]
            jets = [ (jetsc[ij] if ij>=0 else jetsd[-ij-1]) for ij in _ijets]
            bloose  = [j for j in jets if j.btagCSV > 0.46]
            bmedium = [j for j in jets if j.btagCSV > 0.80]
            btight = [j for j in jets if j.btagCSV > 0.935]
            met = getattr(event,"met"+self.systsJEC[_var]+"_pt")
            metphi = getattr(event,"met"+self.systsJEC[_var]+"_phi")
            njet = len(jets); nlep = len(leps); nbloose = len(bloose); nbmedium = len(bmedium); nbtight = len(btight);
            ret = dict([(name,0.0) for name in self.namebranches])

            #L_phi:

            l_phi = 0
            for i in range(len(leps)):
                l_phi += leps[i].conePt * abs(deltaPhi(metphi,leps[i].phi))
            ret["L_phi"] = l_phi


            #B_phi:

            b_loose_phi = 0
            for j in range(len(bloose)):
                b_loose_phi += bloose[j].pt * abs(deltaPhi(metphi,bloose[j].phi))
            ret["B_loose_phi"] = b_loose_phi
            b_medium_phi = 0
            for k in range(len(bmedium)):
                b_medium_phi += bmedium[k].pt * abs(deltaPhi(metphi,bmedium[k].phi))
            ret["B_medium_phi"] = b_medium_phi
            b_tight_phi = 0
            for l in range(len(btight)):
                b_tight_phi += btight[l].pt * abs(deltaPhi(metphi,btight[l].phi))
            ret["B_tight_phi"] = b_tight_phi

            #DR_l_b_1:

            if nlep>=1:
                if nbloose >= 1:
                    ret["DR_l_b_loose1"] = min([deltaR(m,leps[0]) for m in bloose])
                if nbmedium >= 1:
                    ret["DR_l_b_medium1"] = min([deltaR(n,leps[0]) for n in bmedium])
                if nbtight >= 1:
                    ret["DR_l_b_tight1"] = min([deltaR(p,leps[0]) for p in btight])

            #DR_l_b_2:

            if nlep>=2:
                if nbloose >= 1:
                    ret["DR_l_b_loose2"] = min([deltaR(q,leps[1]) for q in bloose])
                if nbmedium >= 1:
                    ret["DR_l_b_medium2"] = min([deltaR(r,leps[1]) for r in bmedium])
                if nbtight >= 1:
                    ret["DR_l_b_tight2"] = min([deltaR(s,leps[1]) for s in btight])

            #pTl_DR_l_b_1:

            if nlep>=1:
                if nbloose >= 1:
                    ret["pTl_DR_l_b_loose1"] = leps[0].conePt * min([deltaR(t,leps[0]) for t in bloose])
                if nbmedium >= 1:
                    ret["pTl_DR_l_b_medium1"] = leps[0].conePt * min([deltaR(u,leps[0]) for u in bmedium])
                if nbtight >= 1:
                    ret["pTl_DR_l_b_tight1"] = leps[0].conePt * min([deltaR(v,leps[0]) for v in btight])

            #pTl_DR_l_b_2:	      

            if nlep>=2:
                if nbloose >= 1:
                    ret["pTl_DR_l_b_loose2"] = leps[1].conePt * min([deltaR(w,leps[1]) for w in bloose])
                if nbmedium >= 1:
                    ret["pTl_DR_l_b_medium2"] = leps[1].conePt * min([deltaR(x,leps[1]) for x in bmedium])
                if nbtight >= 1:
                    ret["pTl_DR_l_b_tight2"] = leps[1].conePt * min([deltaR(y,leps[1]) for y in btight])

            #L_pt:

            l_pt = 0
            for z in range(len(leps)):
                l_pt += leps[z].conePt
            ret["L_pt"] = l_pt

            for br in self.namebranches:
                allret[br+self.systsJEC[var]+self.label] = ret[br]
	 	
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
            self.sf = angular_vars('test_angular_vars','Recl')
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
