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

class HiggsDiffGenTTH(Module):
    def __init__(self, label = 'Hreco_', debug=False):
        self.debug = debug
        self.label = label
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        # Particle counters
        self.out.branch('%snHiggses'%self.label         , 'I')
        self.out.branch('%snTfromhardprocess'%self.label, 'I')
        self.out.branch('%snWFromH'%self.label          , 'I')
        self.out.branch('%snWFromT'%self.label          , 'I')
        self.out.branch('%snQFromW'%self.label          , 'I')
        self.out.branch('%snGenLep'%self.label          , 'I')
        self.out.branch('%snLFromW'%self.label          , 'I')
        self.out.branch('%snNuFromWFromH'%self.label    , 'I')
        self.out.branch('%snNuFromWFromT'%self.label    , 'I')
        self.out.branch('%snQFromWFromH'%self.label     , 'I')
        self.out.branch('%snQFromWFromT'%self.label     , 'I')
        self.out.branch('%snLFromWFromH'%self.label     , 'I')
        self.out.branch('%snLFromWFromT'%self.label     , 'I')

        # Although we expect a maximum of 2 objects per array, we allow for 4 of them to be stored, for safety and later checks
        for suffix in ["_Pt", "_Eta", "_Phi", "_M"]:
            
            self.out.branch('%sHiggses%s'%(self.label,suffix)          , 'F', 4, '%snHiggses'%self.label         ) 
            self.out.branch('%sTfromhardprocess%s'%(self.label,suffix) , 'F', 4, '%snTfromhardprocess'%self.label) 
            self.out.branch('%sWFromH%s'%(self.label,suffix)           , 'F', 4, '%snWFromH'%self.label          ) 
            self.out.branch('%sWFromT%s'%(self.label,suffix)           , 'F', 4, '%snWFromT'%self.label          ) 
            self.out.branch('%sQFromW%s'%(self.label,suffix)           , 'F', 4, '%snQFromW'%self.label          ) 
            self.out.branch('%sGenLep%s'%(self.label,suffix)           , 'F', 4, '%snGenLep'%self.label          ) 
            self.out.branch('%sLFromW%s'%(self.label,suffix)           , 'F', 4, '%snLFromW'%self.label          ) 
            self.out.branch('%sNuFromWFromH%s'%(self.label,suffix)     , 'F', 4, '%snNuFromWFromH'%self.label    ) 
            self.out.branch('%sNuFromWFromT%s'%(self.label,suffix)     , 'F', 4, '%snNuFromWFromT'%self.label    ) 
            self.out.branch('%sQFromWFromH%s'%(self.label,suffix)      , 'F', 4, '%snQFromWFromH'%self.label     ) 
            self.out.branch('%sQFromWFromT%s'%(self.label,suffix)      , 'F', 4, '%snQFromWFromT'%self.label     ) 
            self.out.branch('%sLFromWFromH%s'%(self.label,suffix)      , 'F', 4, '%snLFromWFromH'%self.label     ) 
            self.out.branch('%sLFromWFromT%s'%(self.label,suffix)      , 'F', 4, '%snLFromWFromT'%self.label     ) 
        # Some precomputed quantities of interest

        self.out.branch('%spTHgen'%self.label            , 'F')
        self.out.branch('%spTtgen'%self.label            , 'F', 4, '%snTfromhardprocess'%self.label)
        self.out.branch('%sinv_mass_q1_q2'%self.label    , 'F')
        self.out.branch('%sdelR_partonsFromH'%self.label , 'F')
        self.out.branch('%squark1pT'%self.label          , 'F')
        self.out.branch('%squark2pT'%self.label          , 'F')
        self.out.branch('%sdelR_H_q1l'%self.label        , 'F')
        self.out.branch('%sdelR_H_q2l'%self.label        , 'F')
        self.out.branch('%spTTrueGen'%self.label         , 'F')
        self.out.branch('%spTTrueGenPlusNu'%self.label   , 'F')
        
    def analyze(self, event):
        # Input collections and maps
        genpar = Collection(event,"GenPart","nGenPart") 
        
        Higgses          = []
        Tfromhardprocess = []
        WFromH           = []
        WFromT           = []
        QFromW           = []
        GenLep           = []
        LFromW           = []
        NuFromWFromH     = []
        NuFromWFromT     = []
        QFromWFromH      = []
        QFromWFromT      = []
        LFromWFromH      = []
        LFromWFromT      = []

        for part in genpar:
            # higgs
            if part.pdgId == 25 and part.statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess']):
                Higgses.append(part)

            # tops
            if abs(part.pdgId) == 6 and part.statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess']):
                Tfromhardprocess.append(part)

            # W from higgs
            if (abs(part.pdgId) == 24 and part.statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])
                and part.genPartIdxMother >= 0 and  genpar[part.genPartIdxMother].pdgId == 25 ):
                WFromH.append(part)
                if self.debug: print "it is a hard W coming from a Higgs"
                
            # W from tops 
            if (abs(part.pdgId) == 24 and part.statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])
                and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 6):
                WFromT.append(part)
                if self.debug: print "it is a hard W coming from a top"

            # W decays to quarks
            if (abs(part.pdgId) in [1,2,3,4,5,6] and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24): 
                QFromW.append(part)
                if self.debug: print "it is a quark coming from a W"

            # gen leptons
            if (abs(part.pdgId) in [11,13] and part.status == 1 and part.statusFlags &(1 << diffUtils.statusFlagsMap['isLastCopy']) 
                and not part.statusFlags &(1 << diffUtils.statusFlagsMap['isDirectHadronDecayProduct'])):
                if part.statusFlags &(1 << diffUtils.statusFlagsMap['isPrompt']) or part.statusFlags &(1 << diffUtils.statusFlagsMap['isDirectPromptTauDecayProduct']):
                    GenLep.append(part)
                    if self.debug: print "it is a prompt lepton"

            # gen leptons from W
            if (abs(part.pdgId) in [11,13] and part.status == 1 and part.statusFlags &(1 << diffUtils.statusFlagsMap['isLastCopy']) and not part.statusFlags &(1 << diffUtils.statusFlagsMap['isDirectHadronDecayProduct'])):
                if part.statusFlags &(1 << diffUtils.statusFlagsMap['isPrompt']) or part.statusFlags &(1 << diffUtils.statusFlagsMap['isDirectPromptTauDecayProduct']):
                    if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                        LFromW.append(part)
                        if self.debug: print "it is a prompt lepton"
                        
            # neutrino from W from H
            if abs(part.pdgId) in [12, 14]:
                if self.debug: print "it is a neutrino"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this neutrino is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 25:
                        NuFromWFromH.append(part)
                        if self.debug: print "the mother of this W is a Higgs"
                        
            # neutrino from W from top
            if abs(part.pdgId) in [12, 14]:
                if self.debug: print "it is a neutrino"
                if part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24: 
                    if self.debug: print "the mother of this neutrino is W+ or W-"
                    if abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6:
                        NuFromWFromT.append(part)
                        if self.debug: print "the mother of this W is a top"
        
            # quarks from W from H
            if (abs(part.pdgId) in [1,2,3,4,5,6] and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24
                     and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                if self.debug: print "it is a quark coming from a hard W"
                if (genpar[genpar[part.genPartIdxMother].genPartIdxMother].genPartIdxMother >= 0 
                    and genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId == 25
                    and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                    QFromWFromH.append(part)
                    if self.debug: print "the mother of this hard W is a hard Higgs"

            # quarks from W from T 
            if (abs(part.pdgId) in [1,2,3,4,5,6] and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24 
                     and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                if self.debug: print "it is a quark coming from a hard W"
                if (genpar[genpar[part.genPartIdxMother].genPartIdxMother].genPartIdxMother >= 0 and abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6
                        and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                    QFromWFromT.append(part)
                    if self.debug: print "the mother of this hard W is a hard top"

            # leptons (excl. taus) from W from H 
            if (abs(part.pdgId) in [11,13] and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24 
                     and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                if self.debug: print "it is a lepton coming from a hard W"
                if (genpar[genpar[part.genPartIdxMother].genPartIdxMother].genPartIdxMother >= 0 
                    and genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId == 25 
                    and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                    LFromWFromH.append(part)
                    if self.debug: print "the mother of this hard W is a hard Higgs"
                    
            # leptons (excl. taus) from W from top
            if (abs(part.pdgId) in [11,13] and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24
                     and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                if self.debug: print "it is a lepton coming from a hard W"
                if (genpar[genpar[part.genPartIdxMother].genPartIdxMother].genPartIdxMother >= 0 
                    and abs(genpar[genpar[part.genPartIdxMother].genPartIdxMother].pdgId) == 6 
                    and genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                    LFromWFromT.append(part)
                    if self.debug: print "the mother of this W is a hard top"
        

            if self.debug:
                # taus
                if (abs(part.pdgId) in [15] and part.genPartIdxMother >= 0 and abs(genpar[part.genPartIdxMother].pdgId) == 24):
                    if(genpar[part.genPartIdxMother].statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])):
                        tauFromW.append(part)
                        if self.debug: print "it is a tau coming from a hard W"
                    
                    # leptons from top as recommended by gen particle producer
                if (abs(part.pdgId) in [11,13] 
                    and part.statusFlags &(1 << diffUtils.statusFlagsMap['isPrompt'])
                    and part.statusFlags &(1 << diffUtils.statusFlagsMap['isHardProcess'])
                    and part.statusFlags &(1 << diffUtils.statusFlagsMap['isFirstCopy'])
                    and not part.statusFlags &(1 << diffUtils.statusFlagsMap['isDirectHadronDecayProduct'])):
                    if self.debug: print "it should be a  lepton coming from top"
                    # LFromWFromT.append(part) # why to the same collection? No.
        # End loop on genparticles

        if self.debug:
            print (" >> in this event: "  
                   + " \n higgses              = " + str(len(Higgses)) 
                   + " \n W from Higgs         = " + str(len(WFromH))
                   + " \n hard tops            = " + str(len(Tfromhardprocess))
                   + " \n W from tops          = " + str(len(WFromT))
                   + " \n leptons              = " + str(len(GenLep)) 
                   + " \n QFromWFromH          = " + str(len(QFromWFromH))
                   + " \n QFromWFromT          = " + str(len(QFromWFromT)) 
                   + " \n LFromWFromH          = " + str(len(LFromWFromH)) 
                   + " \n LFromWFromT          = " + str(len(LFromWFromT)) 
                   + " \n NuFromWFromH         = " + str(len(NuFromWFromH)) 
                   + " \n NuFromWFromT         = " + str(len(NuFromWFromT))
                   + " \n quarks from W's      = " + str(len(QFromW))
                   + " \n leptons from W's     = " + str(len(LFromW))
                   #   + " \n taus from W's        = " + str(len(tauFromW))
                   + " \n <<")


        # Fill branches for particles

        self.out.fillBranch('%snHiggses'%self.label         , len(Higgses))
        self.out.fillBranch('%snTfromhardprocess'%self.label, len(Tfromhardprocess))
        self.out.fillBranch('%snWFromH'%self.label          , len(WFromH))
        self.out.fillBranch('%snWFromT'%self.label          , len(WFromT))
        self.out.fillBranch('%snQFromW'%self.label          , len(QFromW))
        self.out.fillBranch('%snGenLep'%self.label          , len(GenLep))
        self.out.fillBranch('%snLFromW'%self.label          , len(LFromW))
        self.out.fillBranch('%snNuFromWFromH'%self.label    , len(NuFromWFromH))
        self.out.fillBranch('%snNuFromWFromT'%self.label    , len(NuFromWFromT))
        self.out.fillBranch('%snQFromWFromH'%self.label     , len(QFromWFromH))
        self.out.fillBranch('%snQFromWFromT'%self.label     , len(QFromWFromT))
        self.out.fillBranch('%snLFromWFromH'%self.label     , len(LFromWFromH))
        self.out.fillBranch('%snLFromWFromT'%self.label     , len(LFromWFromT)) 

        self.out.fillBranch('%sHiggses_Pt'%self.label          , [ part.p4().Pt() for part in Higgses         ]) 
        self.out.fillBranch('%sTfromhardprocess_Pt'%self.label , [ part.p4().Pt() for part in Tfromhardprocess]) 
        self.out.fillBranch('%sWFromH_Pt'%self.label           , [ part.p4().Pt() for part in WFromH          ]) 
        self.out.fillBranch('%sWFromT_Pt'%self.label           , [ part.p4().Pt() for part in WFromT          ]) 
        self.out.fillBranch('%sQFromW_Pt'%self.label           , [ part.p4().Pt() for part in QFromW          ]) 
        self.out.fillBranch('%sGenLep_Pt'%self.label           , [ part.p4().Pt() for part in GenLep          ]) 
        self.out.fillBranch('%sLFromW_Pt'%self.label           , [ part.p4().Pt() for part in LFromW          ]) 
        self.out.fillBranch('%sNuFromWFromH_Pt'%self.label     , [ part.p4().Pt() for part in NuFromWFromH    ]) 
        self.out.fillBranch('%sNuFromWFromT_Pt'%self.label     , [ part.p4().Pt() for part in NuFromWFromT    ]) 
        self.out.fillBranch('%sQFromWFromH_Pt'%self.label      , [ part.p4().Pt() for part in QFromWFromH     ]) 
        self.out.fillBranch('%sQFromWFromT_Pt'%self.label      , [ part.p4().Pt() for part in QFromWFromT     ]) 
        self.out.fillBranch('%sLFromWFromH_Pt'%self.label      , [ part.p4().Pt() for part in LFromWFromH     ]) 
        self.out.fillBranch('%sLFromWFromT_Pt'%self.label      , [ part.p4().Pt() for part in LFromWFromT     ]) 

        self.out.fillBranch('%sHiggses_Eta'%self.label          , [ part.p4().Eta() for part in Higgses         ]) 
        self.out.fillBranch('%sTfromhardprocess_Eta'%self.label , [ part.p4().Eta() for part in Tfromhardprocess]) 
        self.out.fillBranch('%sWFromH_Eta'%self.label           , [ part.p4().Eta() for part in WFromH          ]) 
        self.out.fillBranch('%sWFromT_Eta'%self.label           , [ part.p4().Eta() for part in WFromT          ]) 
        self.out.fillBranch('%sQFromW_Eta'%self.label           , [ part.p4().Eta() for part in QFromW          ]) 
        self.out.fillBranch('%sGenLep_Eta'%self.label           , [ part.p4().Eta() for part in GenLep          ]) 
        self.out.fillBranch('%sLFromW_Eta'%self.label           , [ part.p4().Eta() for part in LFromW          ]) 
        self.out.fillBranch('%sNuFromWFromH_Eta'%self.label     , [ part.p4().Eta() for part in NuFromWFromH    ]) 
        self.out.fillBranch('%sNuFromWFromT_Eta'%self.label     , [ part.p4().Eta() for part in NuFromWFromT    ]) 
        self.out.fillBranch('%sQFromWFromH_Eta'%self.label      , [ part.p4().Eta() for part in QFromWFromH     ]) 
        self.out.fillBranch('%sQFromWFromT_Eta'%self.label      , [ part.p4().Eta() for part in QFromWFromT     ]) 
        self.out.fillBranch('%sLFromWFromH_Eta'%self.label      , [ part.p4().Eta() for part in LFromWFromH     ]) 
        self.out.fillBranch('%sLFromWFromT_Eta'%self.label      , [ part.p4().Eta() for part in LFromWFromT     ]) 

        self.out.fillBranch('%sHiggses_Phi'%self.label          , [ part.p4().Phi() for part in Higgses         ]) 
        self.out.fillBranch('%sTfromhardprocess_Phi'%self.label , [ part.p4().Phi() for part in Tfromhardprocess]) 
        self.out.fillBranch('%sWFromH_Phi'%self.label           , [ part.p4().Phi() for part in WFromH          ]) 
        self.out.fillBranch('%sWFromT_Phi'%self.label           , [ part.p4().Phi() for part in WFromT          ]) 
        self.out.fillBranch('%sQFromW_Phi'%self.label           , [ part.p4().Phi() for part in QFromW          ]) 
        self.out.fillBranch('%sGenLep_Phi'%self.label           , [ part.p4().Phi() for part in GenLep          ]) 
        self.out.fillBranch('%sLFromW_Phi'%self.label           , [ part.p4().Phi() for part in LFromW          ]) 
        self.out.fillBranch('%sNuFromWFromH_Phi'%self.label     , [ part.p4().Phi() for part in NuFromWFromH    ]) 
        self.out.fillBranch('%sNuFromWFromT_Phi'%self.label     , [ part.p4().Phi() for part in NuFromWFromT    ]) 
        self.out.fillBranch('%sQFromWFromH_Phi'%self.label      , [ part.p4().Phi() for part in QFromWFromH     ]) 
        self.out.fillBranch('%sQFromWFromT_Phi'%self.label      , [ part.p4().Phi() for part in QFromWFromT     ]) 
        self.out.fillBranch('%sLFromWFromH_Phi'%self.label      , [ part.p4().Phi() for part in LFromWFromH     ]) 
        self.out.fillBranch('%sLFromWFromT_Phi'%self.label      , [ part.p4().Phi() for part in LFromWFromT     ]) 

        self.out.fillBranch('%sHiggses_M'%self.label          , [ part.p4().M() for part in Higgses         ]) 
        self.out.fillBranch('%sTfromhardprocess_M'%self.label , [ part.p4().M() for part in Tfromhardprocess]) 
        self.out.fillBranch('%sWFromH_M'%self.label           , [ part.p4().M() for part in WFromH          ]) 
        self.out.fillBranch('%sWFromT_M'%self.label           , [ part.p4().M() for part in WFromT          ]) 
        self.out.fillBranch('%sQFromW_M'%self.label           , [ part.p4().M() for part in QFromW          ]) 
        self.out.fillBranch('%sGenLep_M'%self.label           , [ part.p4().M() for part in GenLep          ]) 
        self.out.fillBranch('%sLFromW_M'%self.label           , [ part.p4().M() for part in LFromW          ]) 
        self.out.fillBranch('%sNuFromWFromH_M'%self.label     , [ part.p4().M() for part in NuFromWFromH    ]) 
        self.out.fillBranch('%sNuFromWFromT_M'%self.label     , [ part.p4().M() for part in NuFromWFromT    ]) 
        self.out.fillBranch('%sQFromWFromH_M'%self.label      , [ part.p4().M() for part in QFromWFromH     ]) 
        self.out.fillBranch('%sQFromWFromT_M'%self.label      , [ part.p4().M() for part in QFromWFromT     ]) 
        self.out.fillBranch('%sLFromWFromH_M'%self.label      , [ part.p4().M() for part in LFromWFromH     ]) 
        self.out.fillBranch('%sLFromWFromT_M'%self.label      , [ part.p4().M() for part in LFromWFromT     ]) 

        # Fill branches for some precomputed variables
        self.out.fillBranch('%spTHgen'%self.label, Higgses[0].p4().Pt() if len(Higgses)==1 else -99)
        self.out.fillBranch('%spTtgen'%self.label, [part.p4().Pt() for part in Tfromhardprocess] ) 
        self.out.fillBranch('%sinv_mass_q1_q2'%self.label, (QFromWFromH[0].p4()+QFromWFromH[1].p4()).M() if len(QFromWFromH)==2 else -99)
        self.out.fillBranch('%sdelR_partonsFromH'%self.label, QFromWFromH[0].p4().DeltaR(QFromWFromH[1].p4()) if len(QFromWFromH)==2 else -99)

        self.out.fillBranch('%squark1pT'%self.label, QFromWFromH[0].p4().Pt() if len(QFromWFromH)==2 else -99)
        self.out.fillBranch('%squark2pT'%self.label, QFromWFromH[1].p4().Pt() if len(QFromWFromH)==2 else -99)

        if len(LFromWFromH)==1:
            self.out.fillBranch('%sdelR_H_q1l'%self.label, LFromWFromH[0].p4().DeltaR(QFromWFromH[0].p4()) if len(QFromWFromH)==2 else -99)
            self.out.fillBranch('%sdelR_H_q2l'%self.label, LFromWFromH[0].p4().DeltaR(QFromWFromH[1].p4()) if len(QFromWFromH)==2 else -99)
        
        else:
            # Different error code to highlight different cause
            self.out.fillBranch('%sdelR_H_q1l'%self.label, -88)
            self.out.fillBranch('%sdelR_H_q2l'%self.label, -88)

        # Build pt of Higgs decay particles
        if len(LFromWFromH)==1 and len(QFromWFromH)==2:
            trueVisibleHiggs = LFromWFromH[0].p4() + QFromWFromH[0].p4() + QFromWFromH[1].p4()
            self.out.fillBranch('%spTTrueGen'%self.label, trueVisibleHiggs.Pt())
            if len(NuFromWFromH)==1:
                trueFullHiggs=trueVisibleHiggs+NuFromWFromH[0].p4()
                self.out.fillBranch('%spTTrueGenPlusNu'%self.label, trueFullHiggs.Pt())
            else:
                # Different error code to highligh different cause
                self.out.fillBranch('%spTTrueGenPlusNu'%self.label, -88)
        else:
            self.out.fillBranch('%spTTrueGen'%self.label, -99)
            self.out.fillBranch('%spTTrueGenPlusNu'%self.label, -99)
            


        # Necessary.
        return True



higgsDiffGenTTH = lambda : HiggsDiffGenTTH()
