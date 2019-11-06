from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection


import ROOT, itertools

class HiggsRegressionTTH(Module):
    def __init__(self,label="_Recl", cut_BDT_rTT_score = 0.0, btagDeepCSVveto = 0.4941, doSystJEC=False):
        self.label = label
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.btagDeepCSVveto = btagDeepCSVveto
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalUp", -1:"_jesTotalDown"} if doSystJEC else {0:""}
        thevars = [
            'Lep0_pt', 'Lep0_eta', 'Lep0_phi','Lep1_pt', 'Lep1_eta', 'Lep1_phi','Lep2_pt', 'Lep2_eta', 'Lep2_phi',
            'Jet0_pt','Jet0_eta','Jet0_phi','Jet0_btagdiscr',#'Jet1_mass',
            'Jet1_pt','Jet1_eta','Jet1_phi','Jet1_btagdiscr',#'Jet1_mass',
            'Jet2_pt','Jet2_eta','Jet2_phi','Jet2_btagdiscr',#'Jet2_mass',
            'Jet3_pt','Jet3_eta','Jet3_phi','Jet3_btagdiscr',#'Jet2_mass',
            'Jet4_pt','Jet4_eta','Jet4_phi','Jet4_btagdiscr',#'Jet2_mass',
            'Jet5_pt','Jet5_eta','Jet5_phi','Jet5_btagdiscr',#'Jet2_mass',
            'Jet6_pt','Jet6_eta','Jet6_phi','Jet6_btagdiscr',#'Jet2_mass',
            'HadTop_pt','HadTop_eta','HadTop_phi',
            'TopScore',
            'met','met_phi',
            'HTXS_Higgs_pt','HTXS_Higgs_y',
            'evt_tag'
        ]
        for var in self.systsJEC: self.branches.extend(["%s%s"%(x,self.systsJEC[var]) for x in thevars])
        
        


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
        
        nleps = getattr(event,"nLepGood")
        nFO = getattr(event,"nLepFO"+self.label)
        ileps = getattr(event,"iLepFO"+self.label)
        leps = Collection(event,"LepGood","nLepGood")
        lepsFO = [leps[ileps[i]] for i in xrange(nFO)]
        jets = [x for x in Collection(event,"JetSel"+self.label,"nJetSel"+self.label)]
        (met, met_phi)  = event.MET_pt, event.MET_phi
        ret = {}        

        for var in self.systsJEC:
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%self.systsJEC[var])
            
            candidates=[]
            top1 = None
            top2 = None
            top3 = None
            HadTop = None

            if score>self.cut_BDT_rTT_score:

                j1top = int(getattr(event,"BDThttTT_eventReco_iJetSel1%s"%self.systsJEC[var]))
                j2top = int(getattr(event,"BDThttTT_eventReco_iJetSel2%s"%self.systsJEC[var]))
                j3top = int(getattr(event,"BDThttTT_eventReco_iJetSel3%s"%self.systsJEC[var]))
                # make had top and fill
                #top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(getattr(jets[jets.index(j1top)],'pt%s'%self.systsJEC[var]),jets[jets.index(j1top)].Eta(), jets[jets.index(j1top)].Phi(), jets[jets.index(j1top)].M())
                #top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(getattr(jets[jets.index(j2top)],'pt%s'%self.systsJEC[var]),jets[jets.index(j2top)].Eta(), jets[jets.index(j2top)].Phi(), jets[jets.index(j2top)].M())
                #top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(getattr(jets[jets.index(j3top)],'pt%s'%self.systsJEC[var]),jets[jets.index(j3top)].Eta(), jets[jets.index(j3top)].Phi(), jets[jets.index(j3top)].M())
                
                top1 = ROOT.TLorentzVector(); top1.SetPtEtaPhiM(jets[j1top].p4().Pt(),jets[j1top].p4().Eta(), jets[j1top].p4().Phi(), jets[j1top].p4().M())
                top2 = ROOT.TLorentzVector(); top2.SetPtEtaPhiM(jets[j2top].p4().Pt(),jets[j2top].p4().Eta(), jets[j2top].p4().Phi(), jets[j2top].p4().M())
                top3 = ROOT.TLorentzVector(); top3.SetPtEtaPhiM(jets[j3top].p4().Pt(),jets[j3top].p4().Eta(), jets[j3top].p4().Phi(), jets[j3top].p4().M())
                HadTop = top1+top2+top3
                
                jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<self.btagDeepCSVveto]

                # Later fill only j1 j2 j3, but for now let's use all jets
                #for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                #    for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                #        j1.SetPtEtaPhiM(getattr(jets[jets.index(x1)],'pt%s'%self.systsJEC[var]),j1.Eta(), j1.Phi(), j1.M())
                #        j2.SetPtEtaPhiM(getattr(jets[jets.index(x2)],'pt%s'%self.systsJEC[var]),j2.Eta(), j2.Phi(), j2.M())
                #        W = j1+j2
                #        mW = W.M()
                #        if mW<self.cuts_mW_had[0] or mW>self.cuts_mW_had[1]: continue
                #        Wconstr = ROOT.TLorentzVector()
                #        Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)
                #        Hvisconstr = lep+Wconstr
                #        mHvisconstr = Hvisconstr.M()
                #        if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue
                #        mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                #        candidates.append((mindR,mHvisconstr,mW,_lep,_j1,_j2))
                        
            ret["HadTop_pt%s" %self.systsJEC[var]]  = HadTop.Pt()  if HadTop else -99
            ret["HadTop_eta%s" %self.systsJEC[var]] = HadTop.Eta() if HadTop else -99
            ret["HadTop_phi%s" %self.systsJEC[var]] = HadTop.Phi() if HadTop else -99
            ret["TopScore%s" %self.systsJEC[var]]   = score # else -99? Or not?

            
            evt_tag = 1
            for l,lp4 in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
                if len(lepsFO)<3:
                    ret['Lep%s_pt%s'  %(l, self.systsJEC[var])] = lp4.Pt()
                    ret['Lep%s_eta%s' %(l, self.systsJEC[var])] = lp4.Eta()
                    ret['Lep%s_phi%s' %(l, self.systsJEC[var])] = lp4.Phi()
                    evt_tag *= lepsFO[l].pdgId
                
            
            ret["evt_tag%s"     %self.systsJEC[var]] = evt_tag

            for j, jp4 in [(ix,x.p4()) for ix,x in enumerate(jets)]:
                #jp4.SetPtEtaPhiM(getattr(jets[jets.index(j)],'pt%s'%self.systsJEC[var]),jp4.Eta(), jp4.Phi(), jp4.M())
                if len(jets) <7: # fix this
                    jp4.SetPtEtaPhiM(jp4.Pt(),jp4.Eta(), jp4.Phi(), jp4.M())
                    ret['Jet%s_pt%s'  %(j, self.systsJEC[var])] = jp4.Pt()
                    ret['Jet%s_eta%s' %(j, self.systsJEC[var])] = jp4.Eta()
                    ret['Jet%s_phi%s' %(j, self.systsJEC[var])] = jp4.Phi()
                    ret['Jet%s_btagdiscr%s' %(j, self.systsJEC[var])] = jets[j].btagDeepB


            ret["met%s"     %self.systsJEC[var]] = met
            ret["met_phi%s" %self.systsJEC[var]] = met_phi
            ret["HTXS_Higgs_pt%s"%self.systsJEC[var]] = getattr(event,"HTXS_Higgs_pt")
            ret["HTXS_Higgs_y%s"%self.systsJEC[var]] = getattr(event,"HTXS_Higgs_y")
        return ret

