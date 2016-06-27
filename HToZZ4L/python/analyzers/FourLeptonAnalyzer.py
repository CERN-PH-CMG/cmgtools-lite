from math import *
from collections import defaultdict
from CMGTools.HToZZ4L.analyzers.FourLeptonAnalyzerBase import *

        
class FourLeptonAnalyzer( FourLeptonAnalyzerBase ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(FourLeptonAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.tag = cfg_ana.tag
        self.sortAlgo =  getattr(cfg_ana, 'sortAlgo', 'legacy')
        self.debug =  getattr(cfg_ana, 'debug', False)

    def declareHandles(self):
        super(FourLeptonAnalyzer, self).declareHandles()

    def beginLoop(self, setup):
        super(FourLeptonAnalyzer,self).beginLoop(setup)
        self.counters.addCounter('FourLepton')
        count = self.counters.counter('FourLepton')
        count.register('all events')


    def process(self, event):
        self.readCollections( event.input )

        subevent = EventBox()
        setattr(event,'fourLeptonAnalyzer'+self.tag,subevent)

        #startup counter
        self.counters.counter('FourLepton').inc('all events')

        #create a cut flow
        cutFlow = CutFlowMaker(self.counters.counter("FourLepton"),subevent,event.selectedLeptons)

        passed = cutFlow.applyCut(lambda x:True,'At least four loose leptons',4,'looseLeptons')

        #Ask for four goodleptons
        passed = cutFlow.applyCut(self.leptonID,'At least four good non isolated Leptons',4,'goodLeptons')


        #Create Four Lepton Candidates
        subevent.fourLeptonPreCands = self.findOSSFQuads(cutFlow.obj1)
        cutFlow.setSource1(subevent.fourLeptonPreCands)

        #Apply isolation on all legs
        passed=cutFlow.applyCut(self.fourLeptonIsolation,'At least four OSSF Isolated leptons   ',1,'fourLeptonsIsolated')

        #Apply minimum Z mass
        passed=cutFlow.applyCut(self.fourLeptonMassZ1Z2,'Z masses between 12 and 120 GeV',1,'fourLeptonsZMass')

        #Apply ghost suppression
        passed=cutFlow.applyCut(self.ghostSuppression,'Ghost suppression ',1,'fourLeptonsGhostSuppressed')

        #Pt Thresholds
        passed=cutFlow.applyCut(self.fourLeptonPtThresholds,'Pt 20 and 10 GeV',1,'fourLeptonsPtThresholds')

        #QCD suppression
        passed=cutFlow.applyCut(self.qcdSuppression,'QCD suppression',1,'fourLeptonsPtThresholds')

        #Z1 mass
        passed=cutFlow.applyCut(self.fourLeptonMassZ1,'Z1 Mass cut',1,'fourLeptonsMass')

        #smart cut
        passed=cutFlow.applyCut(self.stupidCut,'Smart cut',1,'fourLeptonsFinal')

        #attach jets
        for quad in subevent.fourLeptonsFinal:
            self.attachJets(quad,event.cleanJets)
        
        #compute MELA
        for quad in subevent.fourLeptonsFinal:
            self.fillMEs(quad,quad.cleanJets)

        #Save the best
        if len(subevent.fourLeptonsFinal)>0:
            if self.sortAlgo == "legacy":
                subevent.fourLeptonsFinal.sort(key = lambda x: x.leg2.leg1.pt()+x.leg2.leg2.pt(), reverse = True)
                subevent.fourLeptonsFinal.sort(key = lambda x: abs(x.leg1.M()-91.1876))
            elif self.sortAlgo == "bestKD":
                debug = self.debug

                # 0) assign to each 4l set a short unique identifier instead of the full tuple of 4 ids
                uid_short = {}
                for ic, cand in enumerate(subevent.fourLeptonsFinal):
                    if cand.uid() not in uid_short: uid_short[cand.uid()] = ic

                # 1) first make groups of candidates that share the same 4l events, by id
                candidates = defaultdict(list)
                for ic,cand in enumerate(subevent.fourLeptonsFinal):
                    candidates[cand.uid()].append(cand)

                # 2) sort each set of candidates by MZ1 a la legacy
                for candlist in candidates.values():
                    candlist.sort(key = lambda x: abs(x.leg1.M()-91.1876))

                # 2b) check that al items in the list have the same KD. 
                #     however, they don't, so the check is commented out for now
                #
                # for candlist in candidates.values():
                #    kds = [ c.KD for c in candlist ]
                #    if max(kds)-min(kds) > 1e-5: 
                #        print "Event %d:%d:%d with mismatching KDs for the same set of 4 leptons " % (event.run, event.lumi, event.input.eventAuxiliary().id().event())
                #        debug = True

                # 3) sort the sets using tke KD value of the first candidate in each set
                sortedCandidates = []
                uids_sorted = sorted(candidates.keys(), key = lambda u : candidates[u][0].KD, reverse=True)
                for uid in uids_sorted:
                    candlist = candidates[uid]
                    for cand in candlist:
                        if debug: print "Cand %d %6.2f %6.2f %6.2f %8.6f  %2d  %d"  % (len(sortedCandidates)+1, cand.mass(), cand.leg1.mass(), cand.leg2.mass(), cand.KD, uid_short[cand.uid()], len(cand.daughterPhotons()))
                        sortedCandidates.append(cand)
                if debug: print "" 
                subevent.fourLeptonsFinal = sortedCandidates
            setattr(event,'bestFourLeptons'+self.tag,subevent.fourLeptonsFinal[:getattr(self.cfg_ana,'maxCand',1)])
        else:    
            setattr(event,'bestFourLeptons'+self.tag,[])

        #FSR test
        passedFSR=cutFlow.applyCut(lambda x: x.hasFSR(),'FSR tagged',1,'fourLeptonsFSR')
        if passedFSR:
            for c in subevent.fourLeptonsFSR:
                #print 'Mass' ,c.fsrUncorrected().M(),c.M()
                pass

        return True        
