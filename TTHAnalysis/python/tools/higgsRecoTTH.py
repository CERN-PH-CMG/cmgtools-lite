from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection


import ROOT, itertools

class HiggsRecoTTH(Module):
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.4941, doSystJEC=True):
        self.label = label
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalUp", -1:"_jesTotalDown"} if doSystJEC else {0:""}
        for var in self.systsJEC: self.branches.extend(["Hreco_%s%s"%(x,self.systsJEC[var]) for x in ["minDRlj","visHmass","Wmass","lepIdx","j1Idx","j2Idx","pTHvis"]])
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.cuts_mW_had = cuts_mW_had
        self.cuts_mH_vis = cuts_mH_vis
        self.btagDeepCSVveto = btagDeepCSVveto
    
    # old interface
    def listBranches(self):
        return self.branches
    def __call__(self,event):
        return self.run(event,CMGCollection)

    # new interface
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self,wrappedOutputTree, self.branches)
    def analyze(self, event):
        writeOutput(self, self.run(event, NanoAODCollection))
        return True

    # code
    def run(self,event,Collection):
    # status flag for gen particles
        statusFlagsMap={
        'isHardProcess' : 7,
        'isPrompt'      : 0
        }
    # define variables and gen collections
        genjet = Collection(event,"GenJet","nGenJet")
        genpar = Collection(event,"GenPart","nGenPart")
        nHiggs = 0
        nHiggs_good = 0 # "good" Higgs is a one that is hard process, see statusFlags
        ngenjets = 0
        gencandid = []
    # loop over gen particles
        for part in genpar:
            if not part.statusFlags &(1<< statusFlagsMap['isPrompt']): continue # cutting out all particles from non-prompt decays, i.e. choosing prompt: decays not coming from hadron, muon or a tau
            if not part.genPartIdxMother == 25: continue # cutting out all particles coming from a non-Higgs chain 
            if part.pdgId == 25:
               nHiggs +=1
               if part.statusFlags &(1<< statusFlagsMap['isHardProcess']):
                  #print "making sure that the Higgs is a hard process" 
                  nHiggs_good +=1
    # some statements that can be used later
    # --------------------------------------
            #if part.genPartIdxMother == 24 or part.genPartIdxMother == -24: # if the gen particle's mother is W+ or W- then it is interesting
            #if part.pdgId not in range(1, 8): continue  # if the gen particle is not a quark then it is not interesting, we want to reconstruct jets
            #if not jet.partonFlavour == 5 and not jet.partonFlavour == -5: #that excludes b-jets but it is not necessary
    # loop over gen jets  
            for jet in genjet:
                if jet.p4().Pt() < 30 or abs(jet.p4().Eta()) > 2.5: continue # bit extreme cuts, I think supposed to be 24 and 2.4
                eta_jet_gen = jet.p4().Eta()
                phi_jet_gen = jet.p4().Phi()
                gencandid.append((eta_jet_gen,phi_jet_gen)) 
                ngenjets +=1
                print "jet flavour = " + str(jet.partonFlavour) + " and mass = " + str(jet.p4().M()) + " GeV and pT = " + str(jet.p4().Pt())
        print gencandid 
        print "number of jets in event = " + str(ngenjets)       
        
        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO"+self.label)
        ileps = getattr(event,"iLepFO"+self.label)
        leps = Collection(event,"LepGood","nLepGood")
        lepsFO = [leps[ileps[i]] for i in xrange(nFO)]
        jets = [x for x in Collection(event,"JetSel"+self.label,"nJetSel"+self.label)]
        ret = {}        

        for var in self.systsJEC:
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%self.systsJEC[var])
            candidates=[]
            
            if score>self.cut_BDT_rTT_score:

                j1top = getattr(event,"BDThttTT_eventReco_iJetSel1%s"%self.systsJEC[var])
                j2top = getattr(event,"BDThttTT_eventReco_iJetSel2%s"%self.systsJEC[var])
                j3top = getattr(event,"BDThttTT_eventReco_iJetSel3%s"%self.systsJEC[var])
                jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<self.btagDeepCSVveto]
                for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                    #if not len(lepsFO)==2: continue
                    #if not lepsFO[0].charge==lepsFO[1].charge: continue 
                    for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                        j1.SetPtEtaPhiM(getattr(jets[jets.index(x1)],'pt%s'%self.systsJEC[var]),j1.Eta(), j1.Phi(), j1.M())
                        j2.SetPtEtaPhiM(getattr(jets[jets.index(x2)],'pt%s'%self.systsJEC[var]),j2.Eta(), j2.Phi(), j2.M())
                        W = j1+j2
                        mW = W.M()
                        if mW<self.cuts_mW_had[0] or mW>self.cuts_mW_had[1]: continue
                        Wconstr = ROOT.TLorentzVector()
                        Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)
                        Hvisconstr = lep+Wconstr
                        mHvisconstr = Hvisconstr.M()
                        pTHvisconstr = Hvisconstr.Pt()
                        if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue
                        mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                        candidates.append((mindR,mHvisconstr,mW,_lep,_j1,_j2,pTHvisconstr))
                        
            best = min(candidates) if len(candidates) else None


            ret["Hreco_minDRlj%s" %self.systsJEC[var]] = best[0] if best else -99
            ret["Hreco_visHmass%s"%self.systsJEC[var]] = best[1] if best else -99
            ret["Hreco_Wmass%s"   %self.systsJEC[var]] = best[2] if best else -99
            ret["Hreco_lepIdx%s"  %self.systsJEC[var]] = best[3] if best else -99
            ret["Hreco_j1Idx%s"   %self.systsJEC[var]] = best[4] if best else -99
            ret["Hreco_j2Idx%s"   %self.systsJEC[var]] = best[5] if best else -99
            ret["Hreco_pTHvis%s"  %self.systsJEC[var]] = best[6] if best else -99
        return ret
