from __future__ import division
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
import ROOT, itertools
from math import *
import sys
import CMGTools.TTHAnalysis.tools.higgsDiffUtils as diffUtils 
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs as HiggsRecoTTHbtagwps

class HiggsDiffRecoTTH(Module):
    def __init__(self, label="Hreco_",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), use_Wmass_constraint=True, btagDeepCSVveto = 'L', doSystJEC=True, useTopTagger=True, debug=False):
        self.debug = debug
        self.useTopTagger = useTopTagger
        self.label = label
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.cuts_mW_had = cuts_mW_had
        self.cuts_mH_vis = cuts_mH_vis
        self.use_Wmass_constraint = use_Wmass_constraint
        self.doSystJEC=doSystJEC
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown"} if self.doSystJEC else {0:""}
        self.btagDeepCSVveto = btagDeepCSVveto

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        # Independent on JES
        self.out.branch('%sGenHiggsDecayMode'%(self.label)          , 'I')

        # Somehow dependent on JES
        for jesLabel in self.systsJEC.values(): 

            # Some quantities
            self.out.branch('%sminDRlj%s'%(self.label,jesLabel)                    , 'F')
            self.out.branch('%svisHmass%s'%(self.label,jesLabel)                   , 'F')
            self.out.branch('%sWmass%s'%(self.label,jesLabel)                      , 'F')
            self.out.branch('%slepIdx%s'%(self.label,jesLabel)                     , 'F')
            self.out.branch('%sj1Idx%s'%(self.label,jesLabel)                      , 'F')
            self.out.branch('%sj2Idx%s'%(self.label,jesLabel)                      , 'F')
            self.out.branch('%spTHvis%s'%(self.label,jesLabel)                     , 'F')
            self.out.branch('%sDRj1j2%s'%(self.label,jesLabel)                , 'F')
            self.out.branch('%sDRj1l%s'%(self.label,jesLabel)            , 'F')
            self.out.branch('%sDRj2l%s'%(self.label,jesLabel)            , 'F')
            self.out.branch('%sBDThttTT_eventReco_mvaValue%s'%(self.label,jesLabel), 'F')

            # Counters
            self.out.branch('%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel) , 'I')
            self.out.branch('%snLeptonsFromHiggs%s'%(self.label,jesLabel)   , 'I')    
            self.out.branch('%snJetsFromHiggs%s'%(self.label,jesLabel)   , 'I')    
            # Useful quadrimomenta
            # We need to save three entire collections, because the triplet selection might select different objects when JEC changes
            for suffix in ["_pt", "_eta", "_phi", "_mass"]:
                # The fat jet closest to the lepton
                self.out.branch('%sfatJetsNearLeptonFromHiggs%s%s'%(self.label,jesLabel,suffix)        , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
                # The reconstructed visible Higgs (lepton and jets)
                self.out.branch('%sleptonsFromHiggs%s%s'%(self.label,jesLabel,suffix), 'F', 2, '%snLeptonsFromHiggs%s'%(self.label,jesLabel)) 
                self.out.branch('%sjetsFromHiggs%s%s'%(self.label,jesLabel,suffix), 'F', 2, '%snJetsFromHiggs%s'%(self.label,jesLabel))
                    
            # Other quantities for the fat jet closest to the lepton
            self.out.branch('%sfatJetsNearLeptonFromHiggs_deltaR%s'%(self.label,jesLabel)    , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            self.out.branch('%sfatJetsNearLeptonFromHiggs_lepIsFromH%s'%(self.label,jesLabel), 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            self.out.branch('%sfatJetsNearLeptonFromHiggs_msoftdrop%s'%(self.label,jesLabel) , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            self.out.branch('%sfatJetsNearLeptonFromHiggs_tau1%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            self.out.branch('%sfatJetsNearLeptonFromHiggs_tau2%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            self.out.branch('%sfatJetsNearLeptonFromHiggs_tau3%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            self.out.branch('%sfatJetsNearLeptonFromHiggs_tau4%s'%(self.label,jesLabel)      , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))


    def analyze(self, event):
        # Some useful input parameters
        year=getattr(event,"year")
        btagvetoval= HiggsRecoTTHbtagwps["DeepFlav_%d_%s"%(year,self.btagDeepCSVveto)][1]

        # Input collections and maps
        closestFatJetToLeptonVars = []
        
        allLeps     = Collection(event,"LepGood","nLepGood")
        nFO      = getattr(event,"nLepFO_Recl")
        selLeps    = getattr(event,"iLepFO_Recl")
        leps   = [allLeps[selLeps[i]] for i in xrange(nFO)]
        jets     = [x for x in Collection(event,"JetSel_Recl","nJetSel_Recl")]
        fatjets  = [x for x in Collection(event,"FatJet","nFatJet")]

        # Store decay mode info from module
        self.out.fillBranch('%sGenHiggsDecayMode'%self.label, event.GenHiggsDecayMode)

        
        for jesLabel in self.systsJEC.values():
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%jesLabel)
            ljj_candidates=[];
            testing_list=[] 
            fatjetsNoB   = [b for b in fatjets if b.btagDeepB<btagvetoval] # I think we want already to exclude bjets, possibly remove the requirement.
            jetsTopNoB=None
            jetsNoTopNoB=None

            # Delicate: here the logic is built such that if one does not use the top tagger then 
            # some variables are left empty to suppress code into "if variable:" blocks
            # Bottom line is that when self.useTopTagger is False we iterate on all the non-b-jets
            if self.useTopTagger:
                j1top = getattr(event,"BDThttTT_eventReco_iJetSel1%s"%jesLabel)
                j2top = getattr(event,"BDThttTT_eventReco_iJetSel2%s"%jesLabel)
                j3top = getattr(event,"BDThttTT_eventReco_iJetSel3%s"%jesLabel)
                jetsTopNoB   = [b for a,b in enumerate(jets) if a in [j1top,j2top,j3top] and b.btagDeepB<btagvetoval] #it is a jet coming from top and not a b-jet
                if score>self.cut_BDT_rTT_score:
                    jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<btagvetoval]
                else:
                    jetsNoTopNoB = []
            else:
                jetsNoTopNoB = [j for j in jets if j.btagDeepB<btagvetoval]


            # Loop on the leptons and jets to check all lepton-jet-jet combinations and rank them
            for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(leps)]:
                lep.SetPtEtaPhiM(getattr(leps[_lep],'conePt'),lep.Eta(), lep.Phi(), lep.M())

                ##### Find the closest fat jet to each lepton
                iClosestFatJetToLep = -99
                minDeltaRfatJetLep = 1000.
                for _j, j in [(ix,x.p4()) for ix,x in enumerate(fatjetsNoB)]: # Find the fat jet closest to the lepton
                    if j.DeltaR(lep) < minDeltaRfatJetLep:
                        iClosestFatJetToLep=_j
                        minDeltaRfatJetLep = j.DeltaR(lep)
                if iClosestFatJetToLep >-1: # Otherwise there are no fat jets
                    fj = fatjetsNoB[iClosestFatJetToLep]
                    closestFat_deltaR = fj.p4().DeltaR(lep)
                    closestFat_lepIsFromH = -99 # -99 if no lepton from H; 0 if this reco lepton is not the correct lepton; 1 if this reco lepton is the correct lepton
                    if len(LFromWFromH) == 1:
                        closestFat_lepIsFromH = 1 if (lep.DeltaR(LFromWFromH[0].p4()) < 0.1) else 0
                    # Must probably add some ID (FatJet_jetId)
                    closestFatJetToLeptonVars.append([closestFat_deltaR, closestFat_lepIsFromH, fj.pt, fj.eta, fj.phi, fj.mass, fj.msoftdrop, fj.tau1, fj.tau2, fj.tau3, fj.tau4])
                ##### End of finding the closest fat jet to each lepton

                # Now looking to all the jet pairs to build the lepton-jet-jet combination
                for _j1,_j2,j1,j2 in [(jets.index(x1),jets.index(x2),x1.p4(),x2.p4()) for x1,x2 in itertools.combinations(jetsNoTopNoB,2)]:
                    # JES-corrected transverse momentum
                    j1.SetPtEtaPhiM(getattr(jets[_j1],'pt%s'%jesLabel),j1.Eta(), j1.Phi(), j1.M())
                    j2.SetPtEtaPhiM(getattr(jets[_j2],'pt%s'%jesLabel),j2.Eta(), j2.Phi(), j2.M())

                    # Build candidate W; if the mass is out of window, exclude this candidate pair
                    # Optionally, later constrain the mass to the W PDG mass (although we use this only to build the candidate, and we store it without constraint)
                    W = j1+j2
                    mW = W.M()
                    if mW<self.cuts_mW_had[0] or mW>self.cuts_mW_had[1]: continue

                    Wconstr = W
                    if self.use_Wmass_constraint:
                        Wconstr = ROOT.TLorentzVector()
                        Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)

                    # Build candidate H; if the mass is out of window, exclude this candidatePair
                    Hvisconstr = lep+Wconstr
                    mHvisconstr = Hvisconstr.M()
                    pTHvisconstr = Hvisconstr.Pt()
                    if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue

                    # Store all non-rejected candidates
                    mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                    delR_j1j2 = j1.DeltaR(j2)
                    ljj_candidates.append((mindR,abs(mHvisconstr-125.0),abs(mW-80.4),delR_j1j2,mHvisconstr,mW, _lep,_j1,_j2,pTHvisconstr))
                    
            # Identify best candidate and fetch quantities to compute and store
            best_ljj_candidate_idx = min(ljj_candidates) if len(ljj_candidates) else None
            best_ljj_candidate = ljj_candidates[ljj_candidates.index(best_ljj_candidate_idx)] if len(ljj_candidates) else None
            minDRlj, _, _, DRj1j2, mHvis, mW, lepidx, j1idx, j2idx, pTHvis = best_ljj_candidate if best_ljj_candidate else [-99,-99,-99,-99,-99,-99,-99,-99,-99,-99] 
            
            l      = None
            j1     = None
            j2     = None
            ls     = []
            js     = []
            DRj1l  = -99
            DRj2l  = -99
            if best_ljj_candidate:
                j1 = jets[j1idx].p4() 
                j2 = jets[j2idx].p4()
                js = [j1, j2]
                l = leps[lepidx].p4()
                ls = [l]
                DRj1l = l.DeltaR(j1)
                DRj2l = l.DeltaR(j2)
            else: pass  

            # Some quantities
            self.out.fillBranch('%sminDRlj%s'%(self.label,jesLabel)                    , minDRlj)
            self.out.fillBranch('%svisHmass%s'%(self.label,jesLabel)                   , mHvis  )
            self.out.fillBranch('%sWmass%s'%(self.label,jesLabel)                      , mW     )
            self.out.fillBranch('%slepIdx%s'%(self.label,jesLabel)                     , lepidx )
            self.out.fillBranch('%sj1Idx%s'%(self.label,jesLabel)                      , j1idx  )
            self.out.fillBranch('%sj2Idx%s'%(self.label,jesLabel)                      , j2idx  )
            self.out.fillBranch('%spTHvis%s'%(self.label,jesLabel)                     , pTHvis )
            self.out.fillBranch('%sDRj1j2%s'%(self.label,jesLabel)                     , DRj1j2 )
            self.out.fillBranch('%sDRj1l%s'%(self.label,jesLabel)                      , DRj1l  )
            self.out.fillBranch('%sDRj2l%s'%(self.label,jesLabel)                      , DRj2l  )
            self.out.fillBranch('%sBDThttTT_eventReco_mvaValue%s'%(self.label,jesLabel), score  )

            # Counters
            self.out.fillBranch('%snLeptonsFromHiggs%s'%(self.label,jesLabel), len(ls))
            self.out.fillBranch('%snJetsFromHiggs%s'%(self.label,jesLabel)   , len(js))    

            # Useful quadrimomenta
            # The reconstructed visible Higgs (somehow one lepton will be duplicate. Consider storing the index)

            self.out.fillBranch('%sleptonsFromHiggs%s_pt'%(self.label,jesLabel)  , [part.Pt()  for part in ls])
            self.out.fillBranch('%sleptonsFromHiggs%s_eta'%(self.label,jesLabel) , [part.Eta() for part in ls])
            self.out.fillBranch('%sleptonsFromHiggs%s_phi'%(self.label,jesLabel) , [part.Phi() for part in ls])
            self.out.fillBranch('%sleptonsFromHiggs%s_mass'%(self.label,jesLabel), [part.M()   for part in ls])
            
            self.out.fillBranch('%sjetsFromHiggs%s_pt'%(self.label,jesLabel)  , [part.Pt() for part in js])
            self.out.fillBranch('%sjetsFromHiggs%s_eta'%(self.label,jesLabel) , [part.Eta()for part in js])
            self.out.fillBranch('%sjetsFromHiggs%s_phi'%(self.label,jesLabel) , [part.Phi()for part in js])
            self.out.fillBranch('%sjetsFromHiggs%s_mass'%(self.label,jesLabel), [part.M()  for part in js])
                    
            # The fat jet closest to the lepton
            # (add later, not needed in this moment)
            #self.out.branch('%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel) , 'I')
            #self.out.branch('%sfatJetsNearLeptonFromHiggs%s%s'%(self.label,suffix,jesLabel)        , 'F', 2, '%snFatJetsNearLeptonFromHiggs%s'%(self.label,jesLabel))
            # Other quantities for the fat jet closest to the lepton from the Higgs
            # (add later, not needed in this moment)
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_deltaR%s'%(self.label,jesLabel)    , 'F', 2, '%snLeptons%s'%(self.label,jesLabel))
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_lepIsFromH%s'%(self.label,jesLabel), 'F', 2, '%snLeptons%s'%(self.label,jesLabel))
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_msoftdrop%s'%(self.label,jesLabel) , 'F', 2, '%snLeptons%s'%(self.label,jesLabel))
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_tau1%s'%(self.label,jesLabel)      , 'F', 2, '%snLeptons%s'%(self.label,jesLabel))
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_tau2%s'%(self.label,jesLabel)      , 'F', 2, '%snLeptons%s'%(self.label,jesLabel))
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_tau3%s'%(self.label,jesLabel)      , 'F', 2, '%snLeptons%s'%(self.label,jesLabel))
            #self.out.branch('%sfatJetsNearLeptonFromHiggs_tau4%s'%(self.label,jesLabel)      , 'F', 2, '%snLeptons%s'%(self.label,jesLabel))


        return True

higgsDiffRecoTTH = lambda : HiggsDiffRecoTTH(label='Hreco_',
                                             cut_BDT_rTT_score = 0.0,
                                             cuts_mW_had = (60.,100.),
                                             cuts_mH_vis = (80.,140.),
                                             use_Wmass_constraint = True,
                                             btagDeepCSVveto = 'M', # or 'M'
                                             useTopTagger=False)
higgsDiffRecoTTH_noWmassConstraint = lambda : HiggsDiffRecoTTH(label='Hreco_',
                                                               cut_BDT_rTT_score = 0.0,
                                                               cuts_mW_had = (60.,100.),
                                                               cuts_mH_vis = (80.,140.),
                                                               use_Wmass_constraint = False,
                                                               btagDeepCSVveto = 'M', # or 'M'
                                                               useTopTagger=False)


higgsDiffRecoTTHLegacyTopTagger = lambda : HiggsDiffRecoTTH(label="Hreco_notoptagger_",
                                                            cut_BDT_rTT_score = 0.0,
                                                            cuts_mW_had = (60.,100.),
                                                            cuts_mH_vis = (80.,140.),
                                                            btagDeepCSVveto = 'M', # or 'M'
                                                            useTopTagger=True)
