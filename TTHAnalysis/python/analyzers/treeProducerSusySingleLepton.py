from CMGTools.TTHAnalysis.analyzers.treeProducerSusyCore import *
from CMGTools.TTHAnalysis.analyzers.ntupleTypes import *

susySingleLepton_globalVariables = susyCore_globalVariables + [

            NTupleVariable("LHEweight_original", lambda ev: ev.LHE_originalWeight if  hasattr(ev,'LHE_originalWeight') else 0, mcOnly=True, help="original LHE weight"),

            ##-------- custom jets ------------------------------------------
            NTupleVariable("htJet25", lambda ev : ev.htJet25, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
            NTupleVariable("mhtJet25", lambda ev : ev.mhtJet25, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 25 GeV)"),
            NTupleVariable("htJet40j", lambda ev : ev.htJet40j, help="H_{T} computed from only jets (with |eta|<2.4, pt > 40 GeV)"),
            NTupleVariable("htJet40", lambda ev : ev.htJet40, help="H_{T} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
            NTupleVariable("mhtJet40", lambda ev : ev.mhtJet40, help="H_{T}^{miss} computed from leptons and jets (with |eta|<2.4, pt > 40 GeV)"),
            #NTupleVariable("nSoftBJetLoose25",  lambda ev: sum([(sv.mva>0.3 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with loose sv mva"),
            #NTupleVariable("nSoftBJetMedium25", lambda ev: sum([(sv.mva>0.7 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with medium sv mva"),
            #NTupleVariable("nSoftBJetTight25",  lambda ev: sum([(sv.mva>0.9 and (sv.jet == None or sv.jet.pt() < 25)) for sv in ev.ivf]) + len(ev.bjetsMedium), int, help="Exclusive sum of jets with pt > 25 passing CSV medium and SV from ivf with tight sv mva"),
            ##------------------------------------------------

            NTupleVariable("metNoHF_rawPt", lambda ev : ev.metNoHF.uncorPt() if  hasattr(ev,'metNoHF') else  0, help="raw noHF met p_{T}"),
            NTupleVariable("metNoHF_rawPhi", lambda ev : ev.metNoHF.uncorPhi() if  hasattr(ev,'metNoHF') else  0, help="raw noHF met phi"),
            NTupleVariable("metNoHF_rawSumEt", lambda ev : ev.metNoHF.uncorSumEt() if  hasattr(ev,'metNoHF') else  0, help="raw noHF met sumEt"),
                
            ##--------------------------------------------------
            ## MET filter information (temporary)
            ##--------------------------------------------------
            NTupleVariable("Flag_HBHENoiseFilter_fix", lambda ev: ev.hbheFilterNew if hasattr(ev,'hbheFilterNew') else  0, help="HBEHE baseline temporary filter decision"),
            NTupleVariable("Flag_HBHEIsoNoiseFilter_fix", lambda ev: ev.hbheFilterIso if hasattr(ev,'hbheFilterIso') else  0, help="HBEHE isolation temporary filter decision"),
   
            # ----------------------- HT from LHE event (requires LHE analyzer to have run)  --------------------------------------------------------- #
            NTupleVariable("lheHT", lambda ev : ev.lheHT, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer"),
            NTupleVariable("lheHTIncoming", lambda ev : ev.lheHTIncoming, help="H_{T} computed from quarks and gluons in Heppy LHEAnalyzer (only LHE status<0 as mothers)"),
            # ---------------------------------------------------------------------------------------------------------------------------------------- #

]
susySingleLepton_globalObjects = susyCore_globalObjects.copy()
susySingleLepton_globalObjects.update({
            # put more here
})

susySingleLepton_collections = susyCore_collections.copy()
susySingleLepton_collections.update({

            # put more here
            "genParticles"     : NTupleCollection("genPartAll",  genParticleWithMotherId, 200, help="all pruned genparticles"), # need to decide which gen collection ?
            ## ---------------------------------------------
            "selectedLeptons" : NTupleCollection("LepGood", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
            "selectedTaus"    : NTupleCollection("TauGood", tauTypeSusy, 3, help="Taus after the preselection"),
            "selectedIsoTrack"    : NTupleCollection("isoTrack", isoTrackType, 50, help="isoTrack, sorted by pt"),
            ##------------------------------------------------
            "cleanJetsAll"       : NTupleCollection("Jet",     jetTypeSusy, 25, help="Cental jets after full selection and cleaning, sorted by pt"),
            "allJetsUsedForMET"       : NTupleCollection("JetForMET",     jetType, 40, help="All Jets used for MET"),
            "fatJets"         : NTupleCollection("FatJet",  fatJetType,  15, help="AK8 jets, sorted by pt"),
            #"reclusteredFatJets" : NTupleCollection("RCFatJet",     fourVectorType,20, help="FatJets1.2 reclusterd from ak4 cleanJetsAll pT > 30, eta <5 "),
            "discardedJets"    : NTupleCollection("DiscJet", jetTypeSusy, 15, help="Jets discarted in the jet-lepton cleaning"),
            ##------------------------------------------------
            #"ivf"       : NTupleCollection("SV",     svType, 20, help="SVs from IVF"),
            "LHE_weights"    : NTupleCollection("LHEweight",  weightsInfoType, 1000, mcOnly=True, help="LHE weight info"),
})

