from CMGTools.TTHAnalysis.treeReAnalyzer import *

def _MEMInit():
    if "libMEM.so" not in ROOT.gSystem.GetLibraries(): 
        ROOT.gSystem.Load("libMEM.so")
        print "Loaded MEM library"
        ROOT.gInterpreter.ProcessLine("#include \"IPHCNtuple/MEM/interface/MEMFriendTreeCERN.h\"")
        print "Loaded MEM interface"

class ttHLepMEMFriend:
    def __init__(self, config, blooseWP, recllabel='Recl'):
        self._procs = [ "TTLL", "TTHfl", "TTHsl", "TTW", "TTbarfl", "TTbarsl", "TTH" ]#, "TTWJJ", "TTH" ]
        self._posts = [ "", "_kinmaxint"]#, "_nHypAll", "_nNull", "_time", "_err", "_chi2" ]
        self.systsJEC = {0:"", 1:"_jecUp", -1:"_jecDown"} # not really used for the moment
        self.inputlabel = '_'+recllabel
        self.blooseWP = blooseWP
        _MEMInit()
        self.mem = ROOT.MEMFriendTreeCERN();
        self.mem.init(config)
        self._events = []
        print "Initialized MEM"
    def listBranches(self):
        return ["MEM_"+p+x for p in self._procs for x in self._posts ]
    def selectEvents(self, events):
        print "Will select events %s" % events
        self._events = list(events)
    def __call__(self,event):
        null_output = dict([("MEM_"+p+x,0) for p in self._procs for x in self._posts ])
        if self._events and event.evt not in self._events:  
            #print "Skipping event %d " % event.evt
            return null_output

        print "\nrun %6d lumi %4d event %d: leps %d" % (event.run, event.lumi, event.evt, event.nLepGood)
        timer = ROOT.TStopwatch(); timer.Start()

        nFO = getattr(event,"nLepFO"+self.inputlabel)
        if nFO < 3: return null_output

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        leps.sort(key = lambda lep: -lep.pt)
        for lep in leps[:3]:
            print "lepton pdgId %d pt %.7f eta %.7f phi %.7f mass %.7f" % (lep.pdgId, lep.pt, lep.eta, lep.phi, lep.mass)

        _var = 0
        jets = [j for j in Collection(event,"JetSel"+self.inputlabel+self.systsJEC[_var],"nJetSel"+self.inputlabel+self.systsJEC[_var])]
        jets.sort(key = lambda j : j.btagCSV, reverse=True)

        for i,jet in enumerate(jets):
            print "Jet pt %.7f eta %.7f phi %.7f mass %.7f btag %.3f" % (jet.pt, jet.eta, jet.phi, jet.mass, jet.btagCSV)

        if len(jets) < 2: return null_output

        self.mem.clear();

        for lep in leps[:3]:
            print "DEBUG: multilepton->FillParticle(\"lepton\", %d, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (lep.pdgId, lep.p4().X(), lep.p4().Y(), lep.p4().Z(), lep.p4().T())
            self.mem.addLepton(lep.p4(), lep.pdgId)

        bjets = filter(lambda j : j.btagCSV>self.blooseWP, jets)[:2]
        ljets = filter(lambda j : j not in bjets, jets)
        for j in bjets: 
            #print 'chosen b-jet:',j.pt
            self.mem.addBJet(j.p4(), j.btagCSV)
            print "DEBUG: multilepton->FillParticle(\"bjet\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (j.btagCSV, j.p4().X(), j.p4().Y(), j.p4().Z(), j.p4().T())

        if len(bjets) >= 1:
            nb = "2b" if (len(bjets) >= 2) else "1b"
            if len(ljets)>=2:
                print "CATEGORY: ","3l_"+nb+"_2j"
                ok = self.mem.setCategory("3l_"+nb+"_2j")
                if not ok: raise RuntimeError, "Hypothesis not found"
                pairs = [(ljets[i1],ljets[i2],(ljets[i1].p4()+ljets[i2].p4()).M()) for i1 in xrange(len(ljets)-1) for i2 in xrange(i1+1,len(ljets)) ]
                def fillTwoPairs(pairs):
                    print 'choosing among %d pairs'%len(pairs)
                    if len(pairs)==0: return
                    pairs.sort(key = lambda (j1,j2,m) : abs(m-80.419))
                    self.mem.addJet("jetClosestMw", pairs[0][0].p4(), pairs[0][0].btagCSV)
                    self.mem.addJet("jetClosestMw", pairs[0][1].p4(), pairs[0][1].btagCSV)
                    print "DEBUG: multilepton->FillParticle(\"jetClosestMw\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (pairs[0][0].btagCSV, pairs[0][0].p4().X(), pairs[0][0].p4().Y(), pairs[0][0].p4().Z(), pairs[0][0].p4().T())
                    print "DEBUG: multilepton->FillParticle(\"jetClosestMw\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (pairs[0][1].btagCSV, pairs[0][1].p4().X(), pairs[0][1].p4().Y(), pairs[0][1].p4().Z(), pairs[0][1].p4().T())
                    #print 'chosen close mw pair:',pairs[0][0].pt,pairs[0][1].pt
                    pairs.sort(key = lambda (j1,j2,m) : m)
                    self.mem.addJet("jetLowestMjj", pairs[0][0].p4(), pairs[0][0].btagCSV)
                    self.mem.addJet("jetLowestMjj", pairs[0][1].p4(), pairs[0][1].btagCSV)
                    print "DEBUG: multilepton->FillParticle(\"jetLowestMjj\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (pairs[0][0].btagCSV, pairs[0][0].p4().X(), pairs[0][0].p4().Y(), pairs[0][0].p4().Z(), pairs[0][0].p4().T())
                    print "DEBUG: multilepton->FillParticle(\"jetLowestMjj\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (pairs[0][1].btagCSV, pairs[0][1].p4().X(), pairs[0][1].p4().Y(), pairs[0][1].p4().Z(), pairs[0][1].p4().T())
                    #print 'chosen low mjj pair:',pairs[0][0].pt,pairs[0][1].pt
                    return ([pairs[0][0],pairs[0][1]])

                chosen_mw = fillTwoPairs(pairs)
                # -- second pair is not needed for 3l final state, will not include it to be safe --
                #print 'chosen for mw are', [x.pt for x in chosen_mw]," removing from list"
                #pairs = [x for x in pairs if (x[0] not in chosen_mw and x[1] not in chosen_mw)]
                #fillTwoPairs(pairs)
                ljByPt = ljets[:]; ljByPt.sort(key = lambda j : -j.pt)
                self.mem.addJet("jetHighestPt", ljByPt[0].p4(), ljByPt[0].btagCSV)
                self.mem.addJet("jetHighestPt", ljByPt[1].p4(), ljByPt[1].btagCSV)
                print "DEBUG: multilepton->FillParticle(\"jetHighestPt\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (ljByPt[0].btagCSV, ljByPt[0].p4().X(), ljByPt[0].p4().Y(), ljByPt[0].p4().Z(), ljByPt[0].p4().T())
                print "DEBUG: multilepton->FillParticle(\"jetHighestPt\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (ljByPt[1].btagCSV, ljByPt[1].p4().X(), ljByPt[1].p4().Y(), ljByPt[1].p4().Z(), ljByPt[1].p4().T())
            elif len(ljets)==1:
                print "CATEGORY: ","3l_"+nb+"_1j"
                ok = self.mem.setCategory("3l_"+nb+"_1j")
                if not ok: raise RuntimeError, "Hypothesis not found"
                #print 'chosen highest pt jet:',jets[2].pt
                self.mem.addJet("jetHighestPt", ljets[0].p4(), ljets[0].btagCSV)
                print "DEBUG: multilepton->FillParticle(\"jetHighestPt\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (ljets[0].btagCSV, ljets[0].p4().X(), ljets[0].p4().Y(), ljets[0].p4().Z(), ljets[0].p4().T())
                #return dict([("MEM_"+p,0) for p in self._procs ]) # FIXME
            elif len(ljets)==0:
                if (nb == "1b"): return null_output # MEM not implemented for 3l_1b_0j
                print "CATEGORY: ","3l_"+nb+"_0j"
                ok = self.mem.setCategory("3l_"+nb+"_0j")
                if not ok: raise RuntimeError, "Hypothesis not found"
            else:
                raise RuntimeError, "Error, unsupported hypothesis"
        else:
            return null_output
        met = getattr(event,"met"+self.systsJEC[_var]+"_pt")
        metphi = getattr(event,"met"+self.systsJEC[_var]+"_phi")
        mht = event.met_sumEt
        met4 = ROOT.TLorentzVector()
        met4.SetPtEtaPhiM(met,0,metphi,0)
        print 'met pt %.7f phi %.7f:' % (met, metphi)
        print 'mht %.7f ' % (mht,)
        self.mem.setMET(met4, 1,0,0,1, mht)
        print "DEBUG: multilepton->mET = TLorentzVector(%.10g,%.10g,%.10g,%.10g);" %  (met4.X(), met4.Y(), met4.Z(), met4.T())
        print "DEBUG: multilepton->mET_cov00 = 1;" 
        print "DEBUG: multilepton->mET_cov01 = 1;" 
        print "DEBUG: multilepton->mET_cov10 = 1;" 
        print "DEBUG: multilepton->mET_cov11 = 1;" 
        print "DEBUG: multilepton->mHT = %.10g;" % mht
        
        ret0 = self.mem.compute()
        for pair in ret0:
            print pair.first, pair.second
        timer.Stop()
        print "This was for event ",event.run,event.lumi,event.evt
        print "T(CPU) = %.1f s, T(Real) = %.1f s " % (timer.CpuTime(),timer.RealTime())
        myout = {}
        for k in self.listBranches(): myout[k]=0
        myout.update( dict([("MEM_"+p.first,p.second) for p in ret0 ]) )
        return myout
        
if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    tree.AddFriend("sf/t", argv[2])
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = ttHLepMEMFriend(argv[3], blooseWP = 0.5426)
            if len(argv) > 4: self.sf.selectEvents( map(int,argv[4:]) )
        def analyze(self,ev):
            self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)

MODULES = [ 
    ( 'MEM_3l', lambda : ttHLepMEMFriend("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_8_0_25/src/CMGTools/TTHAnalysis/python/tools/ttHLepMEMFriend_memcfg.cfg",
                                         blooseWP = 0.5426) ),
]
