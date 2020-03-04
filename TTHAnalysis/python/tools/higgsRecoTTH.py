from __future__ import division
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
import ROOT, itertools
from math import *

#bTagCut 
#= 0.3093 if year==2016 
#= 0.3033 if year==2017 
#= 0.2770 if year==2018

class HiggsRecoTTH(Module):
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), btagDeepCSVveto = 0.3093, doSystJEC=True, useTopTagger=True, debug=False):
        self.debug = debug
        self.useTopTagger = useTopTagger
        self.label = label
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown"} if doSystJEC else {0:""}
        for var in self.systsJEC: self.branches.extend(["Hreco_%s%s"%(x,self.systsJEC[var]) for x in ["minDRlj","visHmass","Wmass","lepIdx","j1Idx","j2Idx","pTHvis", "pTVisPlusNu",
                                                                                                      "nmatchedpartons","nbothmatchedpartons","nmismatchedtoptaggedjets","nmatchedleptons",
                                                                                                      "delR_H_partons","delR_H_j1j2","delR_H_q1l", "delR_H_q2l", "delR_H_j1l_reco", "delR_H_j2l_reco",
                                                                                                      "nQFromWFromH","nLFromWFromH","nQFromWFromT","nLFromWFromT", "nNuFromWFromH",
                                                                                                      "deltaM_trueGen_H","BDThttTT_eventReco_mvaValue",
                                                                                                      "pTHgen","pTtgen","pTTrueGen","pTTrueGenPlusNu",
                                                                                                      "pTHgen_no_cond","pTtgen_no_cond","pTTrueGen_no_cond","pTTrueGenPlusNu_no_cond"]]) 

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
        statusFlagsMap={
        'isHardProcess' : 7,
        'isPrompt'      : 0,
        'isLastCopy'    : 13,
        }
        ret      = {} 
        
        genpar = Collection(event,"GenPart","nGenPart") 
        closestFatJetToLeptonVars = []
        QFromWFromH  = []
        LFromWFromH  = []
        QFromWFromT  = []
        LFromWFromT  = []
        NuFromWFromH = []
        nmatchedpartons           = 0
        nbothmatchedpartons       = 0 
        nmismatchedtoptaggedjets  = 0
        nmatchedleptons           = 0
        pTHgen          = 0
        pTtgen          = 0
        pTVisPlusNu     = 0
        pTTrueGen       = 0
        pTTrueGenplusNu = 0
        #massHgen = 0
        #deltaM_trueGen_H = 0
        delR_H_partons      = -99
        delR_H_j1j2         = -99
        delR_H_q1l          = -99
        delR_H_q2l          = -99
        delR_H_j1l_reco     = -99
        delR_H_j2l_reco     = -99
        
        for part in genpar:
            if part.pdgId == 25 and part.statusFlags &(1 << statusFlagsMap['isHardProcess']):
                #TODO: consider the pt of the stxs higgs
                pTHgen = part.p4().Pt()     
            elif part.pdgId == abs(6) and part.statusFlags &(1 << statusFlagsMap['isHardProcess']):
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
            elif abs(part.pdgId) in [11, 13, 15] and part.statusFlags &(1 << statusFlagsMap['isPrompt']) and part.statusFlags &(1 << statusFlagsMap['isLastCopy']) and part.status ==1: 
                # TODO: account for isPromptFromTauDecay statusFlag
                # TODO: account for same-sign leptons 
                # TODO: account for isHardProcess for leptons? (https://github.com/HEP-KBFI/tth-nanoAOD-tools/blob/master/python/postprocessing/modules/genParticleProducer.py)
                if self.debug: print "it is a lepton"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this lepton is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                        if self.debug: print "the mother of this W is a Higgs"
                        LFromWFromH.append(part)
                    elif abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6:
                        if self.debug: print "the mother of this W is a Top"
                        LFromWFromT.append(part)
            elif abs(part.pdgId) in [12, 14, 16]:
                if self.debug: print "it is a neutrino"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this neutrino is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                        if self.debug: print "the mother of this W is a Higgs"
                        NuFromWFromH.append(part)
        
        #for jet in genjet:
            #if not jet.partonFlavour == 5 and not jet.partonFlavour == -5: that excludes b-jets but it is not necessary
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
    
                if len(NuFromWFromH) != 1: continue 
                #TODO: cutting all events in which two W (W+ and W- decayed leptonically and thus resulting in two neutrinos)
                #TODO: should also consider two leptons same-sign cut using decays of tops?
                #TODO: am I cutting on reco stuff? 
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
                    if (len(NuFromWFromH)>1):
                        print("WARNING! we have not one but ",len(NuFromWFromH), "neutrinos from W from H. I am in reconstruction loop.")
                    for neutrino in NuFromWFromH:
                        VisPlusNu = Hvisconstr+neutrino.p4() 
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
                            nmismatchedtoptaggedjets +=1 #only with respect to the hadronic top where W -> qq, this is what being matched here
            best = min(candidates) if len(candidates) else None
            def ExtractIndex(lst):
                return [item[1] for item in lst]
            def ExtractpT(lst):
                return [item[0] for item in lst]
            if best: #TODO: what does that actually do compared to "if best else -99"
                jetreco1 = jets[best[5]] 
                jetreco2 = jets[best[6]]
                testing_list.extend(([jetreco1.p4().Pt(),best[5]],[jetreco2.p4().Pt(),best[6]]))
                lst=sorted(testing_list,reverse=True)
                #print(ExtractIndex(lst))
                #print(ExtractpT(lst))
                delR_H_j1l_reco = leps[best[4]].p4().DeltaR(jetreco1.p4())
                delR_H_j2l_reco = leps[best[4]].p4().DeltaR(jetreco2.p4())
                for q1,q2 in itertools.combinations(QFromWFromH,2):
                    delR_H_partons = q1.p4().DeltaR(q2.p4())
                    if (len(LFromWFromH)>1):
                        print("WARNING: we have not one but ",len(LFromWFromH), "leptons from W from H. I am in the if best")
                    for lepton in LFromWFromH:
                        delR_H_q1l = q1.p4().DeltaR(lepton.p4())  
                        delR_H_q2l = q2.p4().DeltaR(lepton.p4()) 
                        trueGenSum = lepton.p4()+q1.p4()+q2.p4()
                        pTTrueGen  = trueGenSum.Pt()
                        #massTrueGen= trueGenSum.M()
                        #deltaM_trueGen_H = massTrueGen-massHgen
                        if (len(NuFromWFromH)>1):
                            print("WARNING: we have not one but ",len(NuFromWFromH), "neutrinos from W from H. I am in the if best")
                        for nu in NuFromWFromH:
                            TrueGenplusNu = trueGenSum+nu.p4() 
                            pTTrueGenplusNu = TrueGenplusNu.Pt()
                if (len(QFromWFromH)>2):
                    print("WARNING: we have not two but ",len(QFromWFromH), "quarks from W from H. I am in the if best")
                for quark in QFromWFromH: #TODO: iterate over both quarks and fill nbothmatchedpartons
                    if quark.p4().DeltaR(jetreco1.p4()) < 0.3 or quark.p4().DeltaR(jetreco2.p4()) < 0.3:
                        nmatchedpartons +=1
                if (len(LFromWFromH)>1):
                    print("WARNING: we have not one but ",len(LFromWFromH), "leptons from W from H. I am in the if best")
                for l in LFromWFromH:
                    if l.p4().DeltaR(leps[best[4]].p4()) < 0.3 or l.p4().DeltaR(leps[best[4]].p4()) < 0.3:
                        nmatchedleptons +=1
            else: pass  
            ret["Hreco_minDRlj%s"                     %self.systsJEC[var]] = best[0 ] if best else -99
            ret["Hreco_delR_H_j1j2%s"                 %self.systsJEC[var]] = best[1 ] if best else -99
            ret["Hreco_visHmass%s"                    %self.systsJEC[var]] = best[2 ] if best else -99
            ret["Hreco_Wmass%s"                       %self.systsJEC[var]] = best[3 ] if best else -99
            ret["Hreco_lepIdx%s"                      %self.systsJEC[var]] = best[4 ] if best else -99
            ret["Hreco_j1Idx%s"                       %self.systsJEC[var]] = best[5 ] if best else -99
            ret["Hreco_j2Idx%s"                       %self.systsJEC[var]] = best[6 ] if best else -99
            ret["Hreco_pTVisPlusNu%s"                 %self.systsJEC[var]] = best[7 ] if best else -99 
            ret["Hreco_pTHvis%s"                      %self.systsJEC[var]] = best[8 ] if best else -99
            ret["Hreco_delR_H_partons%s"              %self.systsJEC[var]] = delR_H_partons             if best else -99 
            ret["Hreco_nmatchedleptons%s"             %self.systsJEC[var]] = nmatchedleptons            if best else -99 
            ret["Hreco_pTtgen%s"                      %self.systsJEC[var]] = pTtgen                     if best else -99
            ret["Hreco_nmatchedpartons%s"             %self.systsJEC[var]] = nmatchedpartons            if best else -99 
            ret["Hreco_pTHgen%s"                      %self.systsJEC[var]] = pTHgen                     if best else -99 
            ret["Hreco_nmismatchedtoptaggedjets%s"    %self.systsJEC[var]] = nmismatchedtoptaggedjets   if best else -99
            ret["Hreco_delR_H_q1l%s"                  %self.systsJEC[var]] = delR_H_q1l                 if best else -99 
            ret["Hreco_delR_H_q2l%s"                  %self.systsJEC[var]] = delR_H_q2l                 if best else -99
            ret["Hreco_delR_H_j1l_reco%s"             %self.systsJEC[var]] = delR_H_j1l_reco            if best else -99 
            ret["Hreco_delR_H_j2l_reco%s"             %self.systsJEC[var]] = delR_H_j2l_reco            if best else -99
            ret["Hreco_pTTrueGen%s"                   %self.systsJEC[var]] = pTTrueGen                  if best else -99
            ret["Hreco_pTTrueGenPlusNu%s"             %self.systsJEC[var]] = pTTrueGenplusNu            if best else -99
            #ret["Hreco_deltaM_trueGen_H%s"            %self.systsJEC[var]] = deltaM_trueGen_H           if best else -99 #TODO
            ret['Hreco_nQFromWFromH%s'                %self.systsJEC[var]] = len(QFromWFromH)           if best else -99
            ret['Hreco_nLFromWFromH%s'                %self.systsJEC[var]] = len(LFromWFromH)           if best else -99
            ret['Hreco_nQFromWFromT%s'                %self.systsJEC[var]] = len(QFromWFromT)           if best else -99
            ret['Hreco_nLFromWFromT%s'                %self.systsJEC[var]] = len(LFromWFromT)           if best else -99
            ret['Hreco_nNuFromWFromH%s'               %self.systsJEC[var]] = len(NuFromWFromH)          if best else -99
            ret["Hreco_pTTrueGen_no_cond%s"           %self.systsJEC[var]] = pTTrueGen                  
            ret["Hreco_pTTrueGenPlusNu_no_cond%s"     %self.systsJEC[var]] = pTTrueGenplusNu          
            ret["Hreco_pTtgen_no_cond%s"              %self.systsJEC[var]] = pTtgen                   
            ret["Hreco_pTHgen_no_cond%s"              %self.systsJEC[var]] = pTHgen             
            ret["Hreco_BDThttTT_eventReco_mvaValue%s" %self.systsJEC[var]] = score # if best?
            #ret["Hreco_nbothmatchedpartons%s"         %self.systsJEC[var]] = nbothmatchedpartons        if best else -99 #TODO
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
