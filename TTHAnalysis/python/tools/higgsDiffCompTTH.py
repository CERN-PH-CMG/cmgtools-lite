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

class HiggsDiffCompTTH(Module):
    def __init__(self,label="_Recl",cut_BDT_rTT_score = 0.0, cuts_mW_had = (50.,110.), cuts_mH_vis = (90.,130.), use_Wmass_constraint=True, attemptDisentangling=True, btagDeepCSVveto = 'L', doSystJEC=True, useTopTagger=True, debug=False):
        self.debug = debug
        self.useTopTagger = useTopTagger
        self.label = label
        self.branches = []
        self.systsJEC = {0:"", 1:"_jesTotalCorrUp", -1:"_jesTotalCorrDown"} if doSystJEC else {0:""}
        self.cut_BDT_rTT_score = cut_BDT_rTT_score
        self.cuts_mW_had = cuts_mW_had
        self.cuts_mH_vis = cuts_mH_vis
        self.use_Wmass_constraint = use_Wmass_constraint
        self.attemptDisentangling = attemptDisentangling
        self.btagDeepCSVveto = btagDeepCSVveto


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        # Independent on JES
        
        self.out.branch('%srightlepidx'%self.label                                      , 'I')
        self.out.branch('%swronglepidx'%self.label                                      , 'I')

        # Somehow dependent on JES
        for jesLabel in self.systsJEC.values():
            self.out.branch('%spTVisCrossCheck%s'%(self.label,jesLabel)                      , 'F')
            self.out.branch('%spTVisPlusNu%s'%(self.label,jesLabel)                          , 'F')
            self.out.branch('%snmatchedpartons%s'%(self.label,jesLabel)                      , 'I')
            #self.out.branch('%snmismatchedtoptaggedjets%s'%(self.label,jesLabel)             , 'I')
            #self.out.branch('%snmatchedleptons%s'%(self.label,jesLabel)                      , 'I')
            self.out.branch('%sdelR_lep_jm1%s'%(self.label,jesLabel)                         , 'F')
            self.out.branch('%sdelR_lep_jm2%s'%(self.label,jesLabel)                         , 'F')
            self.out.branch('%sdelR_jm1_jm2%s'%(self.label,jesLabel)                         , 'F')
            self.out.branch('%sboth_selected_jets_matched%s'%(self.label,jesLabel)           , 'I')
            self.out.branch('%sinv_mass_jm1jm2%s'%(self.label,jesLabel)                      , 'F')
            self.out.branch('%sinv_mass_H_jets_match_plusNu%s'%(self.label,jesLabel)         , 'F')
            self.out.branch('%sinv_mass_H_jets_match%s'%(self.label,jesLabel)                , 'F')
            self.out.branch('%spTVis_jets_match%s'%(self.label,jesLabel)                     , 'F')
            self.out.branch('%spTVis_jets_match_plusNu%s'%(self.label,jesLabel)              , 'F')
            self.out.branch('%spTVis_jets_match_plusNu_plus_gen_lep%s'%(self.label,jesLabel) , 'F')
            self.out.branch('%spTVis_jets_match_with_gen_lep%s'%(self.label,jesLabel)        , 'F')
            self.out.branch('%sclosestJet_pt_ToQ1FromWFromH%s'%(self.label,jesLabel)         , 'F')
            self.out.branch('%sclosestJet_pt_ToQ2FromWFromH%s'%(self.label,jesLabel)         , 'F')
            self.out.branch('%sclosestJet_ptres_ToQ1FromWFromH%s'%(self.label,jesLabel)      , 'F')
            self.out.branch('%sclosestJet_ptres_ToQ2FromWFromH%s'%(self.label,jesLabel)      , 'F')
            self.out.branch('%sclosestJet_delR_ToQ1FromWFromH%s'%(self.label,jesLabel)       , 'F')
            self.out.branch('%sclosestJet_delR_ToQ2FromWFromH%s'%(self.label,jesLabel)       , 'F')
            self.out.branch('%sclosestJet_flavour_ToQ1FromWFromH%s'%(self.label,jesLabel)    , 'F')
            self.out.branch('%sclosestJet_flavour_ToQ2FromWFromH%s'%(self.label,jesLabel)    , 'F')
            self.out.branch('%sdelR_lep_jm_closest%s'%(self.label,jesLabel)                  , 'F')
            self.out.branch('%sdelR_lep_jm_farthest%s'%(self.label,jesLabel)                 , 'F')
            self.out.branch('%sdelR_jm_closest_jm_farthest%s'%(self.label,jesLabel)          , 'F')
            self.out.branch('%sdelR_lep_closest_wrongjet%s'%(self.label,jesLabel)            , 'F')
            # Other quantities
            self.out.branch('%smHrightlep%s'%(self.label,jesLabel)                           , 'F')
            self.out.branch('%smHwronglep%s'%(self.label,jesLabel)                           , 'F')

    def makeVisibleHiggs(self, l, j1, j2, nu=None):
        if (not j1) or (not j2) or (not l) or (j1.Pt()>9999.) or (j2.Pt()>9999.) or (l.Pt()>9999.):
            return None, None
        W = j1+j2
        mW = W.M()

        Wconstr = W
        if self.use_Wmass_constraint:
            Wconstr = ROOT.TLorentzVector()
            Wconstr.SetPtEtaPhiM(W.Pt(),W.Eta(),W.Phi(),80.4)

        Hvisconstr = l+Wconstr

        # Add neutrino momentum to visible object (to check how badly we reconstruct pt due to combinatorics rather than shared MET between top and Higgs leg
        VisPlusNu=None
        if nu:
            VisPlusNu = Hvisconstr+nu
        
        return Hvisconstr, VisPlusNu
        
    def analyze(self, event):
        # Some useful input parameters
        year=getattr(event,"year")
        if self.btagDeepCSVveto in ['VL','L','M','T','VT']:
            btagvetoval = HiggsRecoTTHbtagwps["DeepFlav_%d_%s"%(year,self.btagDeepCSVveto)][1]
        else:
            btagvetoval = self.btagDeepCSVveto

        # Input collections and maps

        higgs        = [ x.p4() for x in Collection(event,'%sHiggses'%self.label          , '%snHiggses'%self.label         ) ]
        top          = [ x.p4() for x in Collection(event,'%sTfromhardprocess'%self.label , '%snTfromhardprocess'%self.label) ]
        WfromH       = [ x.p4() for x in Collection(event,'%sWFromH'%self.label           , '%snWFromH'%self.label          ) ]
        WfromT       = [ x.p4() for x in Collection(event,'%sWFromT'%self.label           , '%snWFromT'%self.label          ) ]
        QfromW       = [ x.p4() for x in Collection(event,'%sQFromW'%self.label           , '%snQFromW'%self.label          ) ]
        GenLep       = [ x.p4() for x in Collection(event,'%sGenLep'%self.label           , '%snGenLep'%self.label          ) ]
        LFromW       = [ x.p4() for x in Collection(event,'%sLFromW'%self.label           , '%snLFromW'%self.label          ) ]
        NuFromWFromH = [ x.p4() for x in Collection(event,'%sNuFromWFromH'%self.label     , '%snNuFromWFromH'%self.label    ) ]
        NuFromWFromT = [ x.p4() for x in Collection(event,'%sNuFromWFromT'%self.label     , '%snNuFromWFromT'%self.label    ) ]
        QFromWFromH  = [ x.p4() for x in Collection(event,'%sQFromWFromH'%self.label      , '%snQFromWFromH'%self.label     ) ]
        QFromWFromT  = [ x.p4() for x in Collection(event,'%sQFromWFromT'%self.label      , '%snQFromWFromT'%self.label     ) ]
        LFromWFromH  = [ x.p4() for x in Collection(event,'%sLFromWFromH'%self.label      , '%snLFromWFromH'%self.label     ) ]
        LFromWFromT  = [ x.p4() for x in Collection(event,'%sLFromWFromT'%self.label      , '%snLFromWFromT'%self.label     ) ]

        pTHgen          = getattr(event,'%spTHgen'%self.label)
        pTtgen          = getattr(event,'%spTtgen'%self.label) # list of size 2 (hopefully)
        pTTrueGen       = getattr(event,'%spTTrueGen'%self.label)
        pTTrueGenPlusNu = getattr(event,'%spTTrueGenPlusNu'%self.label)
        
        allLeps     = Collection(event,"LepGood","nLepGood")
        nFO      = getattr(event,"nLepFO_Recl")
        selLeps    = getattr(event,"iLepFO_Recl")
        leps   = [allLeps[selLeps[i]] for i in xrange(nFO)]
        thejets     = [x for x in Collection(event,"JetSel_Recl","nJetSel_Recl")]
        thejetsNoB     = [j for j in thejets if j.btagDeepB<btagvetoval]
        thejetsmore = [x for x in Collection(event,"Jet")]
        thejetsphieta = [[j.phi, j.eta] for j in thejets]
        thejetsmoreskimmed = [j for j in thejetsmore if [j.phi,j.eta] in thejetsphieta]

        # Get right & wrong lepton index
        rightlep = -99
        wronglep = -99
        if (len(QFromWFromH)==2 and len(LFromWFromH)==1):
            ilist=[i[0] for i in sorted(enumerate(leps),key=lambda x:x[1].p4().DeltaR(LFromWFromH[0]))]
            rightlep = ilist[0]
            wronglep = ilist[-1] # last element in list, usually ilist[1] since len(leps)==2 usually
        self.out.fillBranch('%srightlepidx'%self.label                          , rightlep    )
        self.out.fillBranch('%swronglepidx'%self.label                          , wronglep    )

        # Get higgs mass by combining gen quarks with right & wrong leptons
        mHrightlep = -99
        mHwronglep = -99
        if len(QFromWFromH)==2 and len(LFromWFromH)==1:
            mHrightlep = (leps[rightlep].p4()+QFromWFromH[0]+QFromWFromH[1]).M()
            mHwronglep = (leps[wronglep].p4()+QFromWFromH[0]+QFromWFromH[1]).M()
        
        for jesLabel in self.systsJEC.values():

            # We need to have saved three entire collections, because the triplet selection might select different objects when JEC changes
            leptonFromHiggs = [ x.p4() for x in Collection(event,'%sleptonsFromHiggs%s'%(self.label,jesLabel),'%snLeptonsFromHiggs%s'%(self.label,jesLabel))]
            jetsFromHiggs   = [ x.p4() for x in Collection(event,'%sjetsFromHiggs%s'%(self.label,jesLabel), '%snJetsFromHiggs%s'%(self.label,jesLabel)) ]
  
            if len(leptonFromHiggs)==1:
                leptonFromHiggs = leptonFromHiggs[0]
            elif len(leptonFromHiggs)>1:
                print('The reco algorithm selected %s>1 leptons, this by construction should not happen!')
                leptonFromHiggs = None
            else:
                leptonFromHiggs = None

            # Apply JEC to jetsNoB
            jetsNoB=[] 
            for x in thejetsNoB:
                j=x.p4()
                j.SetPtEtaPhiM(getattr(x,'pt%s'%jesLabel), j.Eta(), j.Phi(), j.M())
                jetsNoB.append(j)

            # Make the recoHiggs starting from the saved objects
            
            pTVisPlusNu=-99.
            pTVisCrossCheck=-99.
            if len(jetsFromHiggs) ==2 and leptonFromHiggs and not isinstance(leptonFromHiggs,list): # The- algorithm did fire

                visHiggs, visHiggsPlusNu = self.makeVisibleHiggs(leptonFromHiggs, jetsFromHiggs[0], jetsFromHiggs[1], NuFromWFromH[0] if len(NuFromWFromH)==1 else None)

                if visHiggs:
                    pTVisCrossCheck=visHiggs.Pt()
                # Add neutrino momentum to visible object (to check how badly we reconstruct pt due to combinatorics rather than shared MET between top and Higgs leg
                if visHiggsPlusNu:
                    pTVisPlusNu = visHiggsPlusNu.Pt()
                elif len(NuFromWFromH) > 1:
                    pTVisPlusNu=-88

            self.out.fillBranch('%spTVisPlusNu%s'%(self.label,jesLabel)                          , pTVisPlusNu    )
            self.out.fillBranch('%spTVisCrossCheck%s'%(self.label,jesLabel)                      , pTVisCrossCheck)

            # Match the jets and the quarks
            nmatchedpartons=-1 # nmatchedparsons is set to be -1 if the two quarks are not available for matching, and 0,1,2 if the two quarks are.
            q1, q2 = [None, None]
            # Closest
            jm1=None
            jm2=None
            dr_closestTo_q1=9999.
            dr_closestTo_q2=9999.
            flav_closestTo_q1=99999999. # Avoid high-pdgid-hadrons
            flav_closestTo_q2=99999999.
            # Next-to-closest
            jnm1=None
            jnm2=None
            dr_nClosestTo_q1=9999.
            dr_nClosestTo_q2=9999.
            flav_nClosestTo_q1=99999999. # Avoid high-pdgid-hadrons
            flav_nClosestTo_q2=99999999.
            if len(QFromWFromH)==2:
                q1, q2 = QFromWFromH

                # I need these rather than the jetsNoB because I want to allow matching to match the QfromH to b-jets. 
                # I need this and not jets[] because I want to access the flavour.
                for _x,x in enumerate(thejets):
#                    if x.btagDeepB > 0.3093: continue # Optionally kill > Medium B-Jets
                    j=x.p4()
                    j.SetPtEtaPhiM(getattr(x,'pt%s'%jesLabel), j.Eta(), j.Phi(), j.M()) # Correct the pt
#                    jflav = getattr(x,'hadronFlavour')
                    jflav = getattr(thejetsmoreskimmed[_x],'partonFlavour')
                    drq1=q1.DeltaR(j)
                    drq2=q2.DeltaR(j)
                    if drq1 < dr_closestTo_q1:
                        dr_nClosestTo_q1=dr_closestTo_q1
                        flav_nClosestTo_q1=flav_closestTo_q1
                        jnm1=jm1
                        dr_closestTo_q1=drq1
                        flav_closestTo_q1=jflav
                        jm1=j
                    elif drq1 < dr_nClosestTo_q1:
                        dr_nClosestTo_q1=drq1
                        flav_nClosestTo_q1=jflav
                        jnm1=j
                    if drq2 < dr_closestTo_q2:
                        dr_nClosestTo_q2=dr_closestTo_q2
                        flav_nClosestTo_q2=flav_closestTo_q2
                        jnm2=jm2
                        dr_closestTo_q2=drq2
                        flav_closestTo_q2=jflav
                        jm2=j
                    elif drq2 < dr_nClosestTo_q2:
                        dr_nClosestTo_q2=drq2
                        flav_nClosestTo_q2=jflav
                        jnm2=j

                # Disentangle cases where the same jet matches both jets
                # choice: pick the closest next-to-closest as the second jet
                if(jm1==jm2):
                    if self.attemptDisentangling: # By default it's true
                        if dr_nClosestTo_q1 <= dr_nClosestTo_q2:
                            jm1=jnm1
                            dr_closestTo_q1=dr_nClosestTo_q1
                            flav_closestTo_q1=flav_nClosestTo_q1
                        else:
                            jm2=jnm2
                            dr_closestTo_q2=dr_nClosestTo_q2
                            flav_closestTo_q2=flav_nClosestTo_q2
                    else:
                        jm1=None
                        jm2=None
                        dr_closestTo_q1=9999.
                        dr_closestTo_q2=9999.
                        flav_closestTo_q1=99999999. # Avoid high-pdgid-hadrons
                        flav_closestTo_q2=99999999.

            # Before applying matching thresholds, store a few things
            self.out.fillBranch('%sclosestJet_pt_ToQ1FromWFromH%s'%(self.label,jesLabel)         , jm1.Pt()                   if jm1 else -99.)
            self.out.fillBranch('%sclosestJet_ptres_ToQ1FromWFromH%s'%(self.label,jesLabel)      , (jm1.Pt()-q1.Pt())/q1.Pt() if jm1 else -99.)
            self.out.fillBranch('%sclosestJet_delR_ToQ1FromWFromH%s'%(self.label,jesLabel)       , dr_closestTo_q1            if jm1 else -99.)
            self.out.fillBranch('%sclosestJet_flavour_ToQ1FromWFromH%s'%(self.label,jesLabel)    , flav_closestTo_q1          if jm1 else -99.)
            self.out.fillBranch('%sclosestJet_pt_ToQ2FromWFromH%s'%(self.label,jesLabel)         , jm2.Pt()                   if jm2 else -99.)
            self.out.fillBranch('%sclosestJet_ptres_ToQ2FromWFromH%s'%(self.label,jesLabel)      , (jm2.Pt()-q2.Pt())/q2.Pt() if jm2 else -99.)
            self.out.fillBranch('%sclosestJet_delR_ToQ2FromWFromH%s'%(self.label,jesLabel)       , dr_closestTo_q2            if jm2 else -99.)
            self.out.fillBranch('%sclosestJet_flavour_ToQ2FromWFromH%s'%(self.label,jesLabel)    , flav_closestTo_q2          if jm2 else -99.)
            
            # Now apply thresholds: if they don't satisfy matching thresholds, wipe them out
            # Since I am at it, count how many partons have a jet matched to them
            nmatchedpartons=0 # nmatchedparsons is set to be -1 if the two quarks are not available for matching, and 0,1,2 if the two quarks are.
            if jm1:
                if dr_closestTo_q1 > 0.3 or abs(jm1.Pt()-q1.Pt())/q1.Pt() > 0.6:
                    jm1=None
                else:
                    nmatchedpartons+=1
            if jm2:
                if dr_closestTo_q2 > 0.3 or abs(jm2.Pt()-q2.Pt())/q2.Pt() > 0.6:
                    jm2=None
                else:
                    nmatchedpartons+=1
        
            self.out.fillBranch('%snmatchedpartons%s'%(self.label,jesLabel)                      , nmatchedpartons)

            # Compare the matched jets and the reco jets
            # First I want to write down a few quantities
            visHiggs_matched, visHiggsPlusNu_matched = self.makeVisibleHiggs(leptonFromHiggs, jm1, jm2, NuFromWFromH[0] if len(NuFromWFromH)==1 else None)

            both_selected_jets_matched = 1 if (jm1 and jm2 and len(jetsFromHiggs)==2 and \
            ((abs(jm1.Pt()-jetsFromHiggs[0].Pt())<1e-10 and abs(jm2.Pt()-jetsFromHiggs[1].Pt())<1e-10) or \
            (abs(jm2.Pt()-jetsFromHiggs[0].Pt())<1e-10 and abs(jm1.Pt()-jetsFromHiggs[1].Pt())<1e-10))) else 0
            self.out.fillBranch('%sboth_selected_jets_matched%s'%(self.label,jesLabel) , both_selected_jets_matched)
            self.out.fillBranch('%sinv_mass_jm1jm2%s'%(self.label,jesLabel)                      , (jm1+jm2).M()               if (jm1 and jm2)             else -99.)
            self.out.fillBranch('%sinv_mass_H_jets_match%s'%(self.label,jesLabel)                , visHiggs_matched.M()        if visHiggs_matched          else -99.)
            self.out.fillBranch('%sinv_mass_H_jets_match_plusNu%s'%(self.label,jesLabel)         , visHiggsPlusNu_matched.M()  if visHiggsPlusNu_matched    else -99.)
            self.out.fillBranch('%spTVis_jets_match%s'%(self.label,jesLabel)                     , visHiggs_matched.Pt()       if visHiggs_matched          else -99.)
            self.out.fillBranch('%spTVis_jets_match_plusNu%s'%(self.label,jesLabel)              , visHiggsPlusNu_matched.Pt() if visHiggsPlusNu_matched    else -99.)
            self.out.fillBranch('%sdelR_lep_jm1%s'%(self.label,jesLabel)                         , leptonFromHiggs.DeltaR(jm1) if (jm1 and leptonFromHiggs) else -99.)
            self.out.fillBranch('%sdelR_lep_jm2%s'%(self.label,jesLabel)                         , leptonFromHiggs.DeltaR(jm2) if (jm2 and leptonFromHiggs) else -99.)
            self.out.fillBranch('%sdelR_jm1_jm2%s'%(self.label,jesLabel)                         , jm1.DeltaR(jm2)             if jm1 and jm2               else -99.)

            # Now stored matched jets stuf  according to closeness to lepton
            dr_ljm1=leptonFromHiggs.DeltaR(jm1) if (jm1 and leptonFromHiggs) else -99.
            dr_ljm2=leptonFromHiggs.DeltaR(jm2) if (jm2 and leptonFromHiggs) else -99.
            closest_jm = jm1 if dr_ljm1<dr_ljm2 else jm2
            farthes_jm = jm2 if dr_ljm1<dr_ljm2 else jm1
            self.out.fillBranch('%sdelR_lep_jm_closest%s'%(self.label,jesLabel)                  , leptonFromHiggs.DeltaR(closest_jm) if (closest_jm and leptonFromHiggs) else -99.)
            self.out.fillBranch('%sdelR_lep_jm_farthest%s'%(self.label,jesLabel)                 , leptonFromHiggs.DeltaR(farthes_jm) if (farthes_jm and leptonFromHiggs) else -99.)
            self.out.fillBranch('%sdelR_jm_closest_jm_farthest%s'%(self.label,jesLabel)          , closest_jm.DeltaR(farthes_jm)      if (closest_jm and farthes_jm)      else -99.)

            # Find the closest wrong jet, assuming the lepton from Higgs has been selected (the algorithm did fire)
            dr_l_closestWrong=9999.
            j_closestWrong=None
            if leptonFromHiggs:
                # I need these rather than the jetsNoB because I want to allow matching to match the QfromH to b-jets.
                # I need this and not jets[] because I want to access the flavour.
                for x in thejets:
                    j=x.p4()
                    j.SetPtEtaPhiM(getattr(x,'pt%s'%jesLabel), j.Eta(), j.Phi(), j.M()) # Correct the pt. Not really needed, but added just in case pt is accessed in later edits
                    if j==jm1 or j==jm2:
                        continue
                    drlj=leptonFromHiggs.DeltaR(j) 
                    if drlj < dr_l_closestWrong:
                        dr_l_closestWrong=drlj
                        j_closestWrong=j
            
            self.out.fillBranch('%sdelR_lep_closest_wrongjet%s'%(self.label,jesLabel), leptonFromHiggs.DeltaR(j_closestWrong) if j_closestWrong else -99.)

            # Other quantities
            self.out.fillBranch('%smHrightlep%s'%(self.label,jesLabel)  ,  mHrightlep)
            self.out.fillBranch('%smHwronglep%s'%(self.label,jesLabel)  ,  mHwronglep)

        return True


higgsDiffCompTTH = lambda : HiggsDiffCompTTH(label="Hreco_",
                                             cut_BDT_rTT_score = 0.0,
                                             cuts_mW_had = (60.,100.),
                                             cuts_mH_vis = (80.,140.),
                                             use_Wmass_constraint = True,
                                             attemptDisentangling = True,
                                             btagDeepCSVveto = 'M', # or 'M'
                                             doSystJEC=True,
                                             useTopTagger=False)

higgsDiffCompTTH_noWmassConstraint = lambda : HiggsDiffCompTTH(label="Hreco_",
                                             cut_BDT_rTT_score = 0.0,
                                             cuts_mW_had = (60.,100.),
                                             cuts_mH_vis = (80.,140.),
                                             use_Wmass_constraint = False,
                                             attemptDisentangling = True,
                                             btagDeepCSVveto = 'M', # or 'M'
                                             doSystJEC=True,
                                             useTopTagger=False)
