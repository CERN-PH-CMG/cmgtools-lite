from CMGTools.TTHAnalysis.treeReAnalyzer import *

def _MEMInit():
    if "libMEM.so" not in ROOT.gSystem.GetLibraries(): 
        ROOT.gSystem.Load("libMEM.so")
        print "Loaded MEM library"
        ROOT.gInterpreter.ProcessLine("#include \"IPHCNtuple/MEM/interface/MEMFriendTreeCERN.h\"")
        print "Loaded MEM interface"

class ttHLepMEMFriend:
    def __init__(self, config, recllabel='Recl'):
        self._procs = [ "TTLL", "TTHfl", "TTHsl", "TTW", "TTWJJ", "TTbarfl", "TTbarsl", "TTH" ]
        self._posts = [ "", "_nHypAll", "_nNull", "_time", "_err", "_chi2" ]
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"}
        self.inputlabel = '_'+recllabel
        _MEMInit()
        self.mem = ROOT.MEMFriendTreeCERN();
        self.mem.init(config)
        print "Initialized MEM"
    def listBranches(self):
        return ["MEM_"+p+x for p in self._procs for x in self._posts ]
    def __call__(self,event):
        nFO = getattr(event,"nLepFO"+self.inputlabel)
        if nFO < 3: return dict([("MEM_"+p+x,0) for p in self._procs for x in self._posts ])

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        chosen = getattr(event,"iF"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        leps.sort(key = lambda lep: -lep.pt)
        for lep in leps[:3]:
            print "lepton pdgId %d pt %.7f eta %.7f phi %.7f mass %.7f" % (lep.pdgId, lep.pt, lep.eta, lep.phi, lep.mass)

        _var = 0
        jetsc = [j for j in Collection(event,"Jet"+self.systsJEC[_var],"nJet"+self.systsJEC[_var])]
        jetsd = [j for j in Collection(event,"DiscJet"+self.systsJEC[_var],"nDiscJet"+self.systsJEC[_var])]
        _ijets_list = getattr(event,"iJSel"+self.inputlabel+self.systsJEC[_var])
        _ijets = [ij for ij in _ijets_list]
        jets = [ (jetsc[ij] if ij>=0 else jetsd[-ij-1]) for ij in _ijets]
        jets.sort(key = lambda j : j.btagCSV, reverse=True)

        for i,jet in enumerate(jets):
            print "Jet pt %.7f eta %.7f phi %.7f mass %.7f btag %.3f" % (jet.pt, jet.eta, jet.phi, jet.mass, jet.btagCSV)

        if len(jets) < 2: return dict([("MEM_"+p+x,0) for p in self._procs for x in self._posts ])

        self.mem.clear();

        for lep in leps[:3]:
            self.mem.addLepton(lep.p4(), lep.pdgId)

        bjets = jets[:2]
        for j in bjets: 
            #print 'chosen b-jet:',j.pt
            self.mem.addBJet(j.p4(), j.btagCSV)

        if len(jets) >= 4:
            print "CATEGORY: ","3l_2b_2j"
            ok = self.mem.setCategory("3l_2b_2j")
            if not ok: raise RuntimeError, "Hypothesis not found"
            ljets = jets[2:]
            pairs = [(ljets[i1],ljets[i2],(ljets[i1].p4()+ljets[i2].p4()).M()) for i1 in xrange(len(ljets)-1) for i2 in xrange(i1+1,len(ljets)) ]
            def fillTwoPairs(pairs):
                print 'choosing among %d pairs'%len(pairs)
                if len(pairs)==0: return
                pairs.sort(key = lambda (j1,j2,m) : abs(m-80.419))
                self.mem.addJet("jetClosestMw", pairs[0][0].p4(), pairs[0][0].btagCSV)
                self.mem.addJet("jetClosestMw", pairs[0][1].p4(), pairs[0][1].btagCSV)
                #print 'chosen close mw pair:',pairs[0][0].pt,pairs[0][1].pt
                pairs.sort(key = lambda (j1,j2,m) : m)
                self.mem.addJet("jetLowestMjj", pairs[0][0].p4(), pairs[0][0].btagCSV)
                self.mem.addJet("jetLowestMjj", pairs[0][1].p4(), pairs[0][1].btagCSV)
                #print 'chosen low mjj pair:',pairs[0][0].pt,pairs[0][1].pt
                return ([pairs[0][0],pairs[0][1]])

            chosen_mw = fillTwoPairs(pairs)
            # -- second pair is not needed for 3l final state, will not include it to be safe --
            #print 'chosen for mw are', [x.pt for x in chosen_mw]," removing from list"
            #pairs = [x for x in pairs if (x[0] not in chosen_mw and x[1] not in chosen_mw)]
            #fillTwoPairs(pairs)
        elif len(jets) == 3:
            print "CATEGORY: ","3l_2b_1j"
            ok = self.mem.setCategory("3l_2b_1j")
            if not ok: raise RuntimeError, "Hypothesis not found"
            #print 'chosen highest pt jet:',jets[2].pt
            self.mem.addJet("jetHighestPt", jets[2].p4(), jets[2].btagCSV)
            #return dict([("MEM_"+p,0) for p in self._procs ]) # FIXME
        elif len(jets) <= 2:
            print "CATEGORY: ","3l_2b_0j"
            ok = self.mem.setCategory("3l_2b_0j")
            if not ok: raise RuntimeError, "Hypothesis not found"
        else:
            raise RuntimeError, "Error, unsupported hypothesis"
        met = getattr(event,"met"+self.systsJEC[_var]+"_pt")
        metphi = getattr(event,"met"+self.systsJEC[_var]+"_phi")
        mht = event.met_sumEt
        met4 = ROOT.TLorentzVector()
        met4.SetPtEtaPhiM(met,0,metphi,0)
        print 'met pt %.7f phi %.7f:' % (met, metphi)
        print 'mht %.7f ' % (mht,)
        self.mem.setMET(met4, 1,0,0,1, mht)
        
        ret0 = self.mem.compute()
        for pair in ret0:
            print pair.first, pair.second
        print "This was for event ",event.run,event.lumi,event.evt
        return dict([("MEM_"+p.first,p.second) for p in ret0 ])
        
if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t", argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = ttHLepMEMFriend(argv[3])
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 5)

MODULES = [ 
    ( 'MEM_3l', lambda : ttHLepMEMFriend("/afs/cern.ch/work/g/gpetrucc/ttH/marco/CMSSW_8_0_11/src/IPHCNtuple/MEM/test/JobsReco/config.cfg") ),
]
