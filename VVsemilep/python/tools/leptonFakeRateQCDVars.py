from CMGTools.TTHAnalysis.treeReAnalyzer import *

class LeptonFakeRateQCDVars:
    def __init__(self,leptonSel,jetSel, jetSort = lambda jet:jet.pt, label=None, isMC=True):
        self.label = "" if (label in ["",None]) else ("_"+label)
        self.leptonSel = leptonSel
        self.jetSel = jetSel
        self.jetSort = jetSort
        self.jetvars = "pt eta phi btagCSV mcFlavour".split()
    def listBranches(self):
        label = self.label
        return [ ("nLepGood","I") ] + [ ("LepGood_awayJet%s_%s"%(self.label,var),"F",8,"nLepGood") for var in self.jetvars ]
    def __call__(self,event):
        leps = [l for l in Collection(event,"LepGood","nLepGood")]
        jetsc = [j for j in Collection(event,"Jet","nJet")]
        ret = { "nLepGood" : event.nLepGood }
        for var in self.jetvars:
            ret["LepGood_awayJet%s_%s"%(self.label,var)] = [-99.0] * event.nLepGood
        for il,lep in enumerate(leps):
            if not self.leptonSel(lep): continue
            jets = [ j for j in jetsc if self.jetSel(j,lep,deltaR(j,lep)) ]
            if len(jets) == 0: continue 
            jet = max(jets, key=self.jetSort)
            #print "lepton pt %6.1f eta %+5.2f phi %+5.2f  matched with jet  pt %6.1f eta %+5.2f phi %+5.2f  " % (
            #    lep.pt, lep.eta, lep.phi, jet.pt, jet.eta, jet.phi )
            for var in self.jetvars:
                if var=="mcFlavour" and hasattr(jet,var)==False:
                    ret["LepGood_awayJet%s_%s"%(self.label,var)][il] = 0
                    continue
                ret["LepGood_awayJet%s_%s"%(self.label,var)][il] = getattr(jet,var) 
        return ret

class LeptonFakeRateQCDExtraVars:
    def __init__(self):
        self.branches = [ ("nLepGood","I") ]
        for pt in 25,30,40,60:
            self.branches += [  ("LepGood_awayNJet%s"%(pt),"I",8,"nLepGood") ]
            self.branches += [  ("LepGood_awayHTJet%s"%(pt),"F",8,"nLepGood") ]
        for pt in 25,:
            for B in "Loose", "Medium", "Tight":
                self.branches += [  ("LepGood_awayNBJet%s%s"%(B,pt),"I",8,"nLepGood") ]
    def listBranches(self):
        return self.branches
    def init(self,tree):
        self._ttreereaderversion = tree._ttreereaderversion
        for B in "nLepGood","nJet": setattr(self, B, tree.valueReader(B))
        for B in "eta", "phi",: setattr(self, "LepGood_"+B, tree.arrayReader("LepGood_"+B))
        for B in "pt", "eta", "phi", "btagCSV": setattr(self, "Jet_"+B, tree.arrayReader("Jet_"+B))
    def __call__(self,event):
        ## Init
        if event._tree._ttreereaderversion > self._ttreereaderversion: 
            self.init(event._tree)
        leta, lphi = self.LepGood_eta.At, self.LepGood_phi.At
        jpt, jeta, jphi, jbtag = self.Jet_pt.At, self.Jet_eta.At, self.Jet_phi.At, self.Jet_btagCSV.At
        nLep = self.nLepGood.Get()[0]
        nJet = self.nJet.Get()[0]
        ret = { "nLepGood":nLep }
        for B in self.branches:
            if B[0] not in ret: ret[B[0]] = [0  for il in xrange(nLep)]
        for il in xrange(nLep):
            for ij in xrange(nJet):
                if jpt(ij) <= 25: continue
                if deltaR(leta(il), lphi(il), jeta(ij), jphi(ij)) > 0.7:
                    ret["LepGood_awayNJet25"][il] += 1
                    ret["LepGood_awayHTJet25"][il] += jpt(ij)
                    ret["LepGood_awayNBJetLoose25"][il]  += (jbtag(ij) > 0.5426)
                    ret["LepGood_awayNBJetMedium25"][il] += (jbtag(ij) > 0.8484)
                    ret["LepGood_awayNBJetTight25"][il]  += (jbtag(ij) > 0.9535)
                    if jpt(ij) <= 30: continue
                    ret["LepGood_awayNJet30"][il] += 1
                    ret["LepGood_awayHTJet30"][il] += jpt(ij)
                    if jpt(ij) <= 40: continue
                    ret["LepGood_awayNJet40"][il] += 1
                    ret["LepGood_awayHTJet40"][il] += jpt(ij)
                    if jpt(ij) <= 60: continue
                    ret["LepGood_awayNJet60"][il] += 1
                    ret["LepGood_awayHTJet60"][il] += jpt(ij)
        return ret

MODULES = [
    ('leptonFakeRateQCDVarsTTH', lambda : LeptonFakeRateQCDVars(
                lambda lep : lep.sip3d < 8,
                lambda jet, lep, dr : jet.pt > (20 if abs(jet.eta)<2.4 else 30) and dr > 0.7) ),
    ('leptonFakeRateQCDExtraVarsTTH', lambda : LeptonFakeRateQCDExtraVars())
]

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = LeptonFakeRateQCDVars(
                lambda lep : lep.sip3d < 6 and lep.relIso03 < 0.5,
                lambda jet, lep, dr : jet.pt > (20 if abs(jet.eta)<2.4 else 30) and dr > 0.7)
            self.sf2 = LeptonFakeRateQCDVars(
                lambda lep : lep.sip3d < 6 and lep.relIso03 < 0.5,
                lambda jet, lep, dr : jet.pt > 20 and abs(jet.eta) < 2.4 and dr > 0.7, 
                label="Central")
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
            print self.sf2(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
