from __future__ import division
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
import ROOT, itertools
from math import *

#bTagCut = 0.3093 if year==2016 else 0.3033 if year==2017 else 0.2770
class HiggsRecoTTH(Module):
    #def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.4941, doSystJEC=True): #TODO update the values here
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.3093, doSystJEC=True, useTopTagger=True, debug=False):
        self.debug = debug
        self.useTopTagger = useTopTagger
        self.label = label
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown"} if doSystJEC else {0:""}
        for var in self.systsJEC: self.branches.extend(["Hreco_%s%s"%(x,self.systsJEC[var]) for x in ["minDRlj","visHmass","Wmass","lepIdx","j1Idx","j2Idx","pTHvis",
                                                                                                      "nmatchedpartons","nbothmatchedpartons","nmismatchedtoptaggedjets",
                                                                                                      "pTHgen","delR_H_partons","delR_H_j1j2","BDThttTT_eventReco_mvaValue",
                                                                                                      "delR_H_q1l", "delR_H_q2l", "delR_H_j1l", "delR_H_j2l",
                                                                                                      "nQFromWFromH","nLFromWFromH","nQFromWFromT","nLFromWFromT","pTVisPlusNu",
                                                                                                      "matchedleptons","pTTrueGen", "pTTrueGenAll",
                                                                                                      "deltaM_trueGen_H","pTtgen","pTTrueGenplusNu",
                                                                                                      ]]) # added new branches here

        for mylep in [0, 1]:
            for var in self.systsJEC: self.branches.extend(["Hreco_%s%s"%(x,self.systsJEC[var]) for x in ["l%s_fj_deltaR"%mylep, "l%s_fj_lepIsFromH"%mylep,"l%s_fj_pt"%mylep,"l%s_fj_eta"%mylep,
                                                                                                          "l%s_fj_phi"%mylep,"l%s_fj_mass"%mylep,"l%s_fj_msoftdrop"%mylep,"l%s_fj_tau1"%mylep,
                                                                                                          "l%s_fj_tau2"%mylep,"l%s_fj_tau3"%mylep,"l%s_fj_tau4"%mylep]])



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
        ## TODO ##        
        # status flag for gen particles
        # ----------------------------- 
        statusFlagsMap={
        'isHardProcess' : 7,
        'isPrompt'      : 0
        }
        # Return dictionary
        ret      = {} 

        # define variables and gen collections
        # ------------------------------------   
        #HiggsDaughters = genHiggsDaughtersSelection(genpar) # that is how you define a collection from genproducer, i.e. apply the selection on your collection and it return a filtered collection
        #genjet = Collection(event,"GenJet","nGenJet") # avoid loading unused collection
        genpar = Collection(event,"GenPart","nGenPart")
        
        QFromWFromH = []
        LFromWFromH = []
        QFromWFromT = []
        LFromWFromT = []
        NuFromWFromH = []
        nmatchedpartons          = 0
        nbothmatchedpartons      = 0 
        nmismatchedtoptaggedjets = 0
        matchedleptons          = 0
        bothmatchedleptons      = 0 
        pTHgen = 0
        pTtgen = 0
        pTVisPlusNu = 0
        massHgen = 0
        deltaM_trueGen_H = 0
        pTTrueGen = 0
        pTTrueGenplusNu = 0
        delR_H_partons = -99
        delR_H_j1j2    = -99
        delR_H_q1l     = -99
        delR_H_q2l     = -99
        delR_H_j1l     = -99
        delR_H_j2l     = -99
        closestFatJetToLeptonVars = []
        # loop over gen particles #TODO you can simplify the loop a bit but later, keep it explicit for now
        # -----------------------
        for part in genpar:
            if part.pdgId == 25:
                if part.statusFlags &(1 << statusFlagsMap['isHardProcess']):
                   pTHgen = part.p4().Pt()     
            elif part.pdgId == abs(6):
                  if part.statusFlags &(1 << statusFlagsMap['isHardProcess']):
                      pTtgen = part.p4().Pt()
            elif abs(part.pdgId) in range (1,7): # from 1 to 6
                if self.debug: print "it is a quark"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this quark is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                        if self.debug: print "the mother of this W is a Higgs"
                        QFromWFromH.append(part)
                    elif abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6:
                        if self.debug: print "the mother of this W is a Top"
                        QFromWFromT.append(part)
            elif abs(part.pdgId) in [11, 13, 15] and part.statusFlags &(1 << statusFlagsMap['isPrompt']): # TODO: account for isPromptFromTauDecay statusFlag
                if self.debug: print "it is a lepton"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this lepton is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                        if self.debug: print "the mother of this W is a Higgs"
                        LFromWFromH.append(part)
                    elif abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6:
                        if self.debug: print "the mother of this W is a Top"
                        LFromWFromT.append(part)
            elif abs(part.pdgId) in [12, 14, 16] and part.statusFlags &(1 << statusFlagsMap['isPrompt']):
                if self.debug: print "it is a neutrino"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this neutrino is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                        if self.debug: print "the mother of this W is a Higgs"
                        NuFromWFromH.append(part)
        
        # loop over gen jets 
        # ------------------ 
        #for jet in genjet:
            #if not jet.partonFlavour == 5 and not jet.partonFlavour == -5: #TODO that excludes b-jets but it is not necessary
            #if jet.p4().Pt() > 30 and abs(jet.p4().Eta()) < 2.5:  # bit extreme cuts, I think supposed to be 24 and 2.4
               #gengoodJets.append(jet)
               #print "jet flavour = " + str(jet.partonFlavour) + " and mass = " + str(jet.p4().M()) + " GeV and pT = " + str(jet.p4().Pt())
        #MET_pt   = getattr(event,"MET_pt")
        #mhtJet25 = getattr(event,"mhtJet25_Recl")
        nleps    = getattr(event,"nLepGood")
        nFO      = getattr(event,"nLepFO"+self.label)
        ileps    = getattr(event,"iLepFO"+self.label)
        leps     = Collection(event,"LepGood","nLepGood")
        lepsFO   = [leps[ileps[i]] for i in xrange(nFO)]
        jets     = [x for x in Collection(event,"JetSel"+self.label,"nJetSel"+self.label)]
        fatjets  = [x for x in Collection(event,"FatJet","nFatJet")]
       
        for var in self.systsJEC:
            score = getattr(event,"BDThttTT_eventReco_mvaValue%s"%self.systsJEC[var])
            candidates=[]
            testing_list=[] 
            fatjetsNoB   = [b for b in fatjets if b.btagDeepB<self.btagDeepCSVveto] # I think we want already to exclude bjets, possibly remove the requirement.
            jetsTopNoB=None
            jetsNoTopNoB=None

            # Delicate: here the logic is built such that if one does not use the top tagger then 
            # some variables are left empty to suppress code into "if variable:" blocks
            if self.useTopTagger:
                j1top = getattr(event,"BDThttTT_eventReco_iJetSel1%s"%self.systsJEC[var])
                j2top = getattr(event,"BDThttTT_eventReco_iJetSel2%s"%self.systsJEC[var])
                j3top = getattr(event,"BDThttTT_eventReco_iJetSel3%s"%self.systsJEC[var])
                jetsTopNoB   = [b for a,b in enumerate(jets) if a in [j1top,j2top,j3top] and b.btagDeepB<self.btagDeepCSVveto] #it is a jet coming from top and not a b-jet
                if score>self.cut_BDT_rTT_score:
                    jetsNoTopNoB = [j for i,j in enumerate(jets) if i not in [j1top,j2top,j3top] and j.btagDeepB<self.btagDeepCSVveto]
                else:
                    jetsNoTopNoB = []
            else:
                jetsNoTopNoB = [j for j in jets if j.btagDeepB<self.btagDeepCSVveto]
                
            for _lep,lep in [(ix,x.p4()) for ix,x in enumerate(lepsFO)]:
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
                    #TODO#if (len(NuFromWFromH)>1):
                        #TODO#print("HUGE WARNING! WE HAVE NOT ONE BUT ",len(NuFromWFromH), "NEUTRINOS FROM THE W FROM THE HIGGS")
                    for neutrino in NuFromWFromH:
                        VisPlusNu = Hvisconstr+neutrino.p4() # DONE --> FIX THIS (not sum of pts, but pt of the sum of lorentz vectors)
                        pTVisPlusNu = VisPlusNu.Pt()
                    if mHvisconstr<self.cuts_mH_vis[0] or mHvisconstr>self.cuts_mH_vis[1]: continue
                    mindR = min(lep.DeltaR(j1),lep.DeltaR(j2))
                    delR_H_j1j2 = j1.DeltaR(j2)
                    candidates.append((mindR,delR_H_j1j2,mHvisconstr,mW,_lep,_j1,_j2,pTVisPlusNu,pTHvisconstr))
            
            if self.useTopTagger:
                for topjet in jetsTopNoB:
                    for gentopquark in QFromWFromT:
                        if topjet.p4().DeltaR(gentopquark.p4()) > 0.5:
                            #jets tagged as coming from top didn't match with true partons coming from top"
                            nmismatchedtoptaggedjets +=1 #only with respect to the hadronic top where the W is going to qq and this is what I am matching here
            best = min(candidates) if len(candidates) else None
            for q1,q2 in itertools.combinations(QFromWFromH,2):
                delR_H_partons = q1.p4().DeltaR(q2.p4())
            def ExtractIndex(lst):
                return [item[1] for item in lst]
            def ExtractpT(lst):
                return [item[0] for item in lst]
            if best:
                jetmat1 = jets[best[5]] 
                jetmat2 = jets[best[6]]
                testing_list.extend(([jetmat1.p4().Pt(),best[5]],[jetmat2.p4().Pt(),best[6]]))
                lst=sorted(testing_list,reverse=True)
                print(ExtractIndex(lst))
                print(ExtractpT(lst))
                delR_H_j1l = leps[best[4]].p4().DeltaR(jetmat1.p4())
                delR_H_j2l = leps[best[4]].p4().DeltaR(jetmat2.p4())
                for q1,q2 in itertools.combinations(QFromWFromH,2):
                    delR_H_partons = q1.p4().DeltaR(q2.p4())
                    #TODO#if (len(LFromWFromH)>1):
                        #TODO#print("HUGE WARNING! WE HAVE NOT ONE BUT ",len(LFromWFromH), "LEPTONS FROM THE W FROM THE HIGGS")
                    for lepton in LFromWFromH:
                        delR_H_q1l = q1.p4().DeltaR(lepton.p4())  
                        delR_H_q2l = q2.p4().DeltaR(lepton.p4()) 
                        trueGenSum = lepton.p4()+q1.p4()+q2.p4()
                        pTTrueGen  = trueGenSum.Pt()
                        massTrueGen= trueGenSum.M()
                        deltaM_trueGen_H = massTrueGen-massHgen
                        #TODO#if (len(NuFromWFromH)>1):
                            #TODO#print("HUGE WARNING! WE HAVE NOT ONE BUT ",len(NuFromWFromH), "NEUTRINOS FROM THE W FROM THE HIGGS")
                        for nu in NuFromWFromH:
                            TrueGenplusNu = trueGenSum+nu.p4() 
                            pTTrueGenplusNu = TrueGenplusNu.Pt() # DONE --> PT OF SUM OF MOMENTA INSTEAD OF SUM OF PTs
                for quark in QFromWFromH: 
                    if quark.p4().DeltaR(jetmat1.p4()) < 0.3 or quark.p4().DeltaR(jetmat2.p4()) < 0.3:
                        nmatchedpartons +=1
                #if quark.p4().DeltaR(jetmat1.p4()) < 0.3 and quark.p4().DeltaR(jetmat2.p4()) < 0.3: iterate over two quarks in the list #TODO
		        #    nbothmatchedpartons +=1 --> REMOVE
                for l in LFromWFromH:
                    if l.p4().DeltaR(leps[best[4]].p4()) < 0.3 or l.p4().DeltaR(leps[best[4]].p4()) < 0.3:
                        matchedleptons +=1
            else: pass  
            ret["Hreco_minDRlj%s"                     %self.systsJEC[var]] = best[0 ] if best else -99
            ret["Hreco_visHmass%s"                    %self.systsJEC[var]] = best[2 ] if best else -99
            ret["Hreco_Wmass%s"                       %self.systsJEC[var]] = best[3 ] if best else -99
            ret["Hreco_lepIdx%s"                      %self.systsJEC[var]] = best[4 ] if best else -99
            ret["Hreco_j1Idx%s"                       %self.systsJEC[var]] = best[5 ] if best else -99
            ret["Hreco_j2Idx%s"                       %self.systsJEC[var]] = best[6 ] if best else -99
            ret["Hreco_pTHvis%s"                      %self.systsJEC[var]] = best[8 ] if best else -99
            ret["Hreco_delR_H_partons%s"              %self.systsJEC[var]] = delR_H_partons if best else -99 
            ret["Hreco_delR_H_j1j2%s"                 %self.systsJEC[var]] = best[1 ] if best else -99
            ret["Hreco_matchedleptons%s"              %self.systsJEC[var]] = matchedleptons if best else -99 
            ret["Hreco_pTtgen%s"                      %self.systsJEC[var]] = pTtgen 
            ret["Hreco_nmatchedpartons%s"             %self.systsJEC[var]] = nmatchedpartons if best else -99 
            ret["Hreco_nbothmatchedpartons%s"         %self.systsJEC[var]] = -999 #nbothmatchedpartons if best else -99 #TODO
            ret["Hreco_pTHgen%s"                      %self.systsJEC[var]] = pTHgen  
            ret["Hreco_nmismatchedtoptaggedjets%s"    %self.systsJEC[var]] = nmismatchedtoptaggedjets
            ret["Hreco_BDThttTT_eventReco_mvaValue%s" %self.systsJEC[var]] = score
            ret["Hreco_delR_H_q1l%s"                  %self.systsJEC[var]] = delR_H_q1l  if best else -99 
            ret["Hreco_delR_H_q2l%s"                  %self.systsJEC[var]] = delR_H_q2l  if best else -99
            ret["Hreco_delR_H_j1l%s"                  %self.systsJEC[var]] = delR_H_j1l  if best else -99 
            ret["Hreco_delR_H_j2l%s"                  %self.systsJEC[var]] = delR_H_j2l  if best else -99
            ret["Hreco_pTVisPlusNu%s"                 %self.systsJEC[var]] = best[7] if best else -99 
            ret["Hreco_pTTrueGen%s"                   %self.systsJEC[var]] = pTTrueGen   
            ret["Hreco_pTTrueGenplusNu%s"             %self.systsJEC[var]] = pTTrueGenplusNu 
            ret["Hreco_deltaM_trueGen_H%s"            %self.systsJEC[var]] = deltaM_trueGen_H 
            ret['Hreco_nQFromWFromH%s'                %self.systsJEC[var]] = len(QFromWFromH)
            ret['Hreco_nLFromWFromH%s'                %self.systsJEC[var]] = len(LFromWFromH)
            ret['Hreco_nQFromWFromT%s'                %self.systsJEC[var]] = len(QFromWFromT)
            ret['Hreco_nLFromWFromT%s'                %self.systsJEC[var]] = len(LFromWFromT)
            #for mylep in [0, 1]:
                #ret["Hreco_l%s_fj_deltaR%s"      %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][0] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_lepIsFromH%s"  %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][1] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_pt%s"          %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][2] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_eta%s"         %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][3] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_phi%s"         %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][4] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_mass%s"        %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][5] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_msoftdrop%s"   %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][6] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_tau1%s"        %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][7] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_tau2%s"        %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][8] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_tau3%s"        %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][9] if len(closestFatJetToLeptonVars) == 2 else -99
                #ret["Hreco_l%s_fj_tau4%s"        %(mylep,self.systsJEC[var])] = closestFatJetToLeptonVars[mylep][10] if len(closestFatJetToLeptonVars) == 2 else -99
        return ret
