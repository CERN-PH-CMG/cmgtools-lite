##########  Recipe  ####
#
#   git clone git@github.com:gpetruc/IPHCNtuple.git IPHCNtuple -b 94x-ichep18
#   cd IPHCNtuple/
#   git config core.sparsecheckout true
#   echo '/MEM/' >> .git/info/sparse-checkout
#   git read-tree -mu HEAD
#   cd MEM
#   ( cd Madgraph && bash SetupMadgraph.sh )
#   ( cd src && make libMEM.so && cp libMEM.so $CMSSW_BASE/lib/$SCRAM_ARCH -v )
#
#####


from CMGTools.TTHAnalysis.treeReAnalyzer import *
import os

def _MEMInit():
    if "libMEM.so" not in ROOT.gSystem.GetLibraries(): 
        ROOT.gSystem.Load("libMEM.so")
        print "Loaded MEM library"
        ROOT.gInterpreter.ProcessLine("#include \"IPHCNtuple/MEM/interface/MEMFriendTreeCERN.h\"")
        print "Loaded MEM interface"

class ttHLepMEMFriend:
    def __init__(self, config, blabel, blooseWP, recllabel='Recl', jetPtCut=25.0, doJEC=False):
        self._procs = [ "TTLL", "TTHfl", "TTHsl", "TTW", "TTbarfl", "TTbarsl", ]#, "TTWJJ", "TTH" ]
        self._posts = [ "", "_kinmaxint"]#, "_nHypAll", "_nNull", "_time", "_err", "_chi2" ]
        self._memouts = [ "MEM_"+p+x for p in self._procs for x in self._posts ] + [ "MEM_TTH_"+x for x in ("mean","avg","kinmaxint") ]
        if not doJEC:
            self.JECs = [""]
        elif doJEC == "only":
            self.JECs = ["_jecUp", "_jecDown"] 
        else:
            self.JECs = ["", "_jecUp", "_jecDown"]
        self.inputlabel = '_'+recllabel
        self.blabel = blabel
        self.blooseWP = blooseWP
        self.jetPtCut = jetPtCut
        _MEMInit()
        self.mem = ROOT.MEMFriendTreeCERN();
        self.mem.init(config)
        self._events = []
        print "Initialized MEM"
    def listBranches(self):
        return [x+y for x in self._memouts for y in self.JECs]
    def selectEvents(self, events):
        print "Will select events %s" % events
        self._events = list(events)
    def __call__(self,event):
        myout = dict((x,0) for x in self.listBranches())
        if self._events and event.evt not in self._events:  
            #print "Skipping event %d " % event.evt
            return myout

        print "\nrun %6d lumi %4d event %d: leps %d" % (event.run, event.lumi, event.evt, event.nLepGood)
        timer = ROOT.TStopwatch(); timer.Start()

        nFO = getattr(event,"nLepFO"+self.inputlabel)
        if nFO < 3: return myout

        all_leps = [l for l in Collection(event,"LepGood","nLepGood")]
        chosen = getattr(event,"iLepFO"+self.inputlabel)
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        leps.sort(key = lambda lep: -lep.pt)
        for lep in leps[:3]:
            print "lepton pdgId %d pt %.7f eta %.7f phi %.7f mass %.7f" % (lep.pdgId, lep.pt, lep.eta, lep.phi, lep.mass)

        for jecPostfix in self.JECs:
            print "Considering jets%s" % jecPostfix

            alljets = [j for j in Collection(event,"JetSel"+self.inputlabel,"nJetSel"+self.inputlabel)]
            if jecPostfix:
                jets = []
                for i,jet in enumerate(alljets):
                    print "before: jet pt %.7f eta %.7f phi %.7f mass %.7f btag %.3f  corrUp %.3f corrDn %.3f" % (jet.pt, jet.eta, jet.phi, jet.mass, getattr(jet,self.blabel), jet.corr_JECUp, jet.corr_JECDown)
                    if "jecUp"     in jecPostfix: corr = jet.corr_JECUp/jet.corr
                    elif "jecDown" in jecPostfix: corr = jet.corr_JECDown/jet.corr
                    jet.pt = jet.pt * corr
                    jet.mass = jet.mass * corr
                    print "after : jet pt %.7f eta %.7f phi %.7f mass %.7f btag %.3f  p4.pt %.7f " % (jet.pt, jet.eta, jet.phi, jet.mass, getattr(jet,self.blabel), jet.p4().Pt())
                    if j.pt > self.jetPtCut: jets.append(jet)
            else:
                jets = alljets

            jets.sort(key = lambda j : getattr(j,self.blabel), reverse=True)

            for i,jet in enumerate(jets):
                print "Jet pt %.7f eta %.7f phi %.7f mass %.7f btag %.3f" % (jet.pt, jet.eta, jet.phi, jet.mass, getattr(jet,self.blabel))

            if len(jets) < 2: continue

            self.mem.clear();

            for lep in leps[:3]:
                print "DEBUG: multilepton->FillParticle(\"lepton\", %d, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (lep.pdgId, lep.p4().X(), lep.p4().Y(), lep.p4().Z(), lep.p4().T())
                self.mem.addLepton(lep.p4(), lep.pdgId)

            bjets = filter(lambda j : getattr(j,self.blabel)>self.blooseWP, jets)[:2]
            ljets = filter(lambda j : j not in bjets, jets)
            for j in bjets: 
                #print 'chosen b-jet:',j.pt
                self.mem.addBJet(j.p4(), getattr(j,self.blabel))
                print "DEBUG: multilepton->FillParticle(\"bjet\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(j,self.blabel), j.p4().X(), j.p4().Y(), j.p4().Z(), j.p4().T())

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
                        self.mem.addJet("jetClosestMw", pairs[0][0].p4(), getattr(pairs[0][0],self.blabel))
                        self.mem.addJet("jetClosestMw", pairs[0][1].p4(), getattr(pairs[0][1],self.blabel))
                        print "DEBUG: multilepton->FillParticle(\"jetClosestMw\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(pairs[0][0],self.blabel), pairs[0][0].p4().X(), pairs[0][0].p4().Y(), pairs[0][0].p4().Z(), pairs[0][0].p4().T())
                        print "DEBUG: multilepton->FillParticle(\"jetClosestMw\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(pairs[0][1],self.blabel), pairs[0][1].p4().X(), pairs[0][1].p4().Y(), pairs[0][1].p4().Z(), pairs[0][1].p4().T())
                        #print 'chosen close mw pair:',pairs[0][0].pt,pairs[0][1].pt
                        pairs.sort(key = lambda (j1,j2,m) : m)
                        self.mem.addJet("jetLowestMjj", pairs[0][0].p4(), getattr(pairs[0][0],self.blabel))
                        self.mem.addJet("jetLowestMjj", pairs[0][1].p4(), getattr(pairs[0][1],self.blabel))
                        print "DEBUG: multilepton->FillParticle(\"jetLowestMjj\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(pairs[0][0],self.blabel), pairs[0][0].p4().X(), pairs[0][0].p4().Y(), pairs[0][0].p4().Z(), pairs[0][0].p4().T())
                        print "DEBUG: multilepton->FillParticle(\"jetLowestMjj\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(pairs[0][1],self.blabel), pairs[0][1].p4().X(), pairs[0][1].p4().Y(), pairs[0][1].p4().Z(), pairs[0][1].p4().T())
                        #print 'chosen low mjj pair:',pairs[0][0].pt,pairs[0][1].pt
                        return ([pairs[0][0],pairs[0][1]])

                    chosen_mw = fillTwoPairs(pairs)
                    # -- second pair is not needed for 3l final state, will not include it to be safe --
                    #print 'chosen for mw are', [x.pt for x in chosen_mw]," removing from list"
                    #pairs = [x for x in pairs if (x[0] not in chosen_mw and x[1] not in chosen_mw)]
                    #fillTwoPairs(pairs)
                    ljByPt = ljets[:]; ljByPt.sort(key = lambda j : -j.pt)
                    self.mem.addJet("jetHighestPt", ljByPt[0].p4(), getattr(ljByPt[0],self.blabel))
                    self.mem.addJet("jetHighestPt", ljByPt[1].p4(), getattr(ljByPt[1],self.blabel))
                    print "DEBUG: multilepton->FillParticle(\"jetHighestPt\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(ljByPt[0],self.blabel), ljByPt[0].p4().X(), ljByPt[0].p4().Y(), ljByPt[0].p4().Z(), ljByPt[0].p4().T())
                    print "DEBUG: multilepton->FillParticle(\"jetHighestPt\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(ljByPt[1],self.blabel), ljByPt[1].p4().X(), ljByPt[1].p4().Y(), ljByPt[1].p4().Z(), ljByPt[1].p4().T())
                elif len(ljets)==1:
                    print "CATEGORY: ","3l_"+nb+"_1j"
                    ok = self.mem.setCategory("3l_"+nb+"_1j")
                    if not ok: raise RuntimeError, "Hypothesis not found"
                    #print 'chosen highest pt jet:',jets[2].pt
                    self.mem.addJet("jetHighestPt", ljets[0].p4(), getattr(ljets[0],self.blabel))
                    print "DEBUG: multilepton->FillParticle(\"jetHighestPt\", 0, %.10g, 0,0,0,0, TLorentzVector(%.10g,%.10g,%.10g,%.10g));" %  (getattr(ljets[0],self.blabel), ljets[0].p4().X(), ljets[0].p4().Y(), ljets[0].p4().Z(), ljets[0].p4().T())
                    #return dict([("MEM_"+p,0) for p in self._procs ]) # FIXME
                elif len(ljets)==0:
                    if (nb == "1b"): continue # MEM not implemented for 3l_1b_0j
                    print "CATEGORY: ","3l_"+nb+"_0j"
                    ok = self.mem.setCategory("3l_"+nb+"_0j")
                    if not ok: raise RuntimeError, "Hypothesis not found"
                else:
                    raise RuntimeError, "Error, unsupported hypothesis"
            else:
                continue
            met = getattr(event,"met"+jecPostfix+"_pt")
            metphi = getattr(event,"met"+jecPostfix+"_phi")
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
            myout.update( dict([("MEM_"+p.first+jecPostfix,p.second) for p in ret0 ]) )
            print "Done jets%s after  %.1f s, T(Real) = %.1f s " % (jecPostfix, timer.CpuTime(),timer.RealTime())
            timer.Continue()
        timer.Stop()
        print "This was for event ",event.run,event.lumi,event.evt
        print "T(CPU) = %.1f s, T(Real) = %.1f s " % (timer.CpuTime(),timer.RealTime())
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
            self.sf = ttHLepMEMFriend(argv[3], blabel="btagDeepCSV", blooseWP = 0.1522, doJEC=True)
            if len(argv) > 4: self.sf.selectEvents( map(int,argv[4:]) )
        def analyze(self,ev):
            self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 500)

MODULES = [ 
    ( 'MEM_3l', lambda : ttHLepMEMFriend("%s/src/CMGTools/TTHAnalysis/python/tools/ttHLepMEMFriend_memcfg.cfg" % os.environ['CMSSW_BASE'],
                                         blabel="btagDeepCSV", blooseWP = 0.1522) ),
    ( 'MEM_wJECs_3l', lambda : ttHLepMEMFriend("%s/src/CMGTools/TTHAnalysis/python/tools/ttHLepMEMFriend_memcfg.cfg" % os.environ['CMSSW_BASE'],
                                         blabel="btagDeepCSV", blooseWP = 0.1522, doJEC=True) ),
    ( 'MEM_JECs_3l', lambda : ttHLepMEMFriend("%s/src/CMGTools/TTHAnalysis/python/tools/ttHLepMEMFriend_memcfg.cfg" % os.environ['CMSSW_BASE'],
                                         blabel="btagDeepCSV", blooseWP = 0.1522, doJEC="only") ),
]
