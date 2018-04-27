##########################################################
##        CONFIGURATION FOR SUSY SingleLep TREES        ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re


#-------- LOAD ALL ANALYZERS -----------

from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
# Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerStop4Body import *

#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------

runData = getHeppyOption("runData",False)
runSMS = getHeppyOption("runSMS",False)
runFullSimSignal = getHeppyOption("runFullSimSignal",False)
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
removeJecUncertainty = getHeppyOption("removeJecUncertainty",False)
skipT1METCorr = getHeppyOption("skipT1METCorr",False)
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))
allGenParts = getHeppyOption("allGenParts", False)
run2017 = getHeppyOption("run2017", True)


#Assume by default to run on TTbar, only run on other background samples if specifically asked for
runWJets = getHeppyOption("runWJets", False)
runZInv = getHeppyOption("runZInv", False)
runOtherMC1 = getHeppyOption("runOtherMC1", False)
runOtherMC2 = getHeppyOption("runOtherMC2", False)


# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999

#-----------------------------------------------------------------------
# Lepton Preselection
#electron
#lepAna.loose_electron_id = "MVA_ID_NonTrig_Spring16_VLooseIdEmu"
lepAna.loose_electron_id      = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVeto_Veto"
lepAna.loose_electron_eta     = 2.5
lepAna.inclusive_electron_pt  = 3
lepAna.loose_electron_pt      = 3
lepAna.inclusive_electron_id  = ""
#muon
lepAna.inclusive_muon_id  = ""
lepAna.inclusive_muon_pt  = 3
lepAna.loose_muon_pt      = 3
lepAna.loose_muon_eta     = 2.4

lepAna.loose_electron_dxy     = 0.1
lepAna.loose_electron_dz      = 0.5
lepAna.loose_muon_dxy         = 0.1
lepAna.loose_muon_dz          = 0.5

lepAna.loose_electron_relIso     = 0.0
lepAna.loose_muon_relIso         = 0.0
lepAna.inclusive_electron_relIso = 0.0
lepAna.inclusive_muon_relIso     = 0.0

lepAna.loose_electron_lostHits     = 3.0
lepAna.inclusive_electron_lostHits = 3.0

lepAna.match_inclusiveLeptons = True

lepAna.packedCandidates = 'packedPFCandidates'

isolation = "hybIso"
lepAna.doIsolationScan = False

if isolation == "miniIso":
    lepAna.doMiniIsolation = True
    lepAna.miniIsolationPUCorr = 'rhoArea'
    lepAna.miniIsolationVetoLeptons = None
    lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
    lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
    lepAna.ele_isoCorr = "rhoArea"
    lepAna.mu_isoCorr = "rhoArea"
    lepAna.loose_electron_relIso = 0.5
    lepAna.loose_muon_relIso = 0.5
elif isolation == "hybIso":
    lepAna.doMiniIsolation = False
    lepAna.ele_isoCorr = "rhoArea"
    lepAna.mu_isoCorr = "rhoArea"
    absIsoCut   = 20
    ptSwitch    = 25
    relIsoCut   = 1.*absIsoCut/ptSwitch
    lepAna.loose_muon_isoCut     = lambda mu: (mu.absIso03 < absIsoCut) or (mu.relIso03 < relIsoCut)
    lepAna.loose_electron_isoCut = lambda el: (el.absIso03 < absIsoCut) or (el.relIso03 < relIsoCut)

#-----------------------------------------------------------------------
# Jet & MET Preselection
if not removeJecUncertainty:
    jetAna.addJECShifts = True
    jetAna.addJERShifts= True #TODO: check if the lines below should be repeated for the JER Shifts?
    #TODO: uncomment following lines to add jet uncertainties?
    #susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleDown)
    #susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleUp)
    #susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleDown)
    #susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleUp)

myMCGlobalTag = "Summer16_23Sep2016V3_MC"
#myDataGlobalTag = "Spring16_25nsV8BCD_DATA Spring16_25nsV8E_DATA Spring16_25nsV8F_DATA Spring16_25nsV8_DATA"
#myDataRuns      = [276811, 277420, 278802]
myDataGlobalTag = [(1, 'Summer16_23Sep2016BCDV3_DATA'), (276831, 'Summer16_23Sep2016EFV3_DATA'), (278802, 'Summer16_23Sep2016GV3_DATA'), (280919, 'Summer16_23Sep2016HV3_DATA')]

if run2017:
    myMCGlobalTag = "Fall17_17Nov2017_V6_MC"
    myDataGlobalTag =  [(1,"Fall17_17Nov2017B_V6_DATA"),(299337,"Fall17_17Nov2017C_V6_DATA"),(302030,"Fall17_17Nov2017D_V6_DATA"),(303435,"Fall17_17Nov2017E_V6_DATA"),(304911,"Fall17_17Nov2017F_V6_DATA")]

jetAna.jetPt = 20.
if not removeJecUncertainty:
    jetAnaScaleUp.jetPt   = 20
    jetAnaScaleDown.jetPt = 20

jetAna.jetEta = 4.7
if not removeJecUncertainty:
    jetAnaScaleUp.jetEta   = 4.7
    jetAnaScaleDown.jetEta = 4.7

# Jet-lepton cleaning
jetAna.minLepPt = -1
if not removeJecUncertainty:
    jetAnaScaleUp.minLepPt   = -1
    jetAnaScaleDown.minLepPt = -1

jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this
if not removeJecUncertainty:
    jetAnaScaleDown.copyJetsByValue = True # do not remove this
    metAnaScaleDown.copyMETsByValue = True # do not remove this
    jetAnaScaleUp.copyJetsByValue   = True # do not remove this
    metAnaScaleUp.copyMETsByValue   = True # do not remove this

jetAna.cleanSelectedLeptons = True
jetAna.jetEtaCentral        = 2.4
if not removeJecUncertainty:
    jetAnaScaleDown.cleanSelectedLeptons = True
    jetAnaScaleDown.jetEtaCentral        = 2.4
    jetAnaScaleUp.cleanSelectedLeptons   = True
    jetAnaScaleUp.jetEtaCentral          = 2.4

jetAna.applyL2L3Residual = "Data"
if not removeJecUncertainty:
    jetAnaScaleDown.applyL2L3Residual = "Data"
    jetAnaScaleUp.applyL2L3Residual   = "Data"


# Switch on slow QGL
jetAna.doQG = True
if not removeJecUncertainty:
    jetAnaScaleUp.doQG   = True
    jetAnaScaleDown.doQG = True

#additional MET quantities
#metAna.doTkMet = True
#treeProducer.globalVariables.append(NTupleVariable("met_trkPt", lambda ev : ev.tkMet.pt() if  hasattr(ev,'tkMet') else  0, help="tkmet p_{T}"))
#treeProducer.globalVariables.append(NTupleVariable("met_trkPhi", lambda ev : ev.tkMet.phi() if  hasattr(ev,'tkMet') else  0, help="tkmet phi"))


jetAna.smearJets = True
if not removeJecUncertainty:
    jetAnaScaleUp.smearJets   = True
    jetAnaScaleDown.smearJets = True

if not skipT1METCorr:
    jetAna.calculateType1METCorrection = True
    #metAna.recalibrate                 = 'type1'
    metAna.recalibrate                 = True
    if not removeJecUncertainty:
        jetAnaScaleUp.calculateType1METCorrection   = True
        metAnaScaleUp.recalibrate                   = True
        jetAnaScaleDown.calculateType1METCorrection = True
        metAnaScaleDown.recalibrate                 = True

if removeJetReCalibration:
    jetAna.recalibrateJets = False
    if not removeJecUncertainty:
        jetAnaScaleUp.recalibrateJets   = False
        jetAnaScaleDown.recalibrateJets = False

if runSMS:
    myMCGlobalTag = "Spring16_FastSimV1_MC"
    jetAna.applyL2L3Residual = False
    jetAna.relaxJetId = True # relax jetId for FastSIM
    if not removeJecUncertainty:
        jetAnaScaleUp.applyL2L3Residual   = False
        jetAnaScaleDown.applyL2L3Residual = False
        jetAnaScaleUp.relaxJetId   = True
        jetAnaScaleDown.relaxJetId = True

jetAna.calculateSeparateCorrections = True

jetAna.lepSelCut = lambda lep: ( abs(lep.pdgId()) == 11 and lep.pt() > 5 ) or ( abs(lep.pdgId()) == 13 and lep.pt() > 3 )

def jetLepRatio( jet, lepton):
    lep_jet_ratio = lepton.pt()/jet.pt()
    if lep_jet_ratio < 0.5 :
        return (jet, lepton)   ## Don't Clean Jet
    else:
        return lepton             ## Clean Jet
jetAna.jetLepArbitration = jetLepRatio
if not removeJecUncertainty:
    jetAnaScaleUp.jetLepArbitration   = jetLepRatio
    jetAnaScaleDown.jetLepArbitration = jetLepRatio

# SET UP GLOBAL TAGS
jetAna.mcGT        = myMCGlobalTag
jetAna.dataGT      = myDataGlobalTag
#jetAna.runsDataJEC = myDataRuns
if not removeJecUncertainty:
    jetAnaScaleDown.mcGT        = myMCGlobalTag
    jetAnaScaleDown.dataGT      = myDataGlobalTag
    jetAnaScaleUp.mcGT          = myMCGlobalTag
    jetAnaScaleUp.dataGT        = myDataGlobalTag
    #jetAnaScaleDown.runsDataJEC = myDataRuns
    #jetAnaScaleUp.runsDataJEC   = myDataRuns

#-----------------------------------------------------------------------

# Switch off slow photon MC matching
#photonAna.do_mc_match = False
photonAna.do_mc_match = True

# Loose Tau configuration
tauAna.loose_ptMin = 18
tauAna.loose_etaMax = 2.3
tauAna.loose_decayModeID = "decayModeFindingNewDMs"
tauAna.loose_tauID = "byLooseCombinedIsolationDeltaBetaCorr3Hits"
jetAna.cleanJetsFromTaus = True
if not removeJecUncertainty:
    jetAnaScaleUp.cleanJetsFromTaus = True
    jetAnaScaleDown.cleanJetsFromTaus = True

isoTrackAna.setOff = False

if not run2017:
    isoTrackAna.useLegacy2016 = True

genAna.allGenTaus = True

if allGenParts:
    susySingleLepton_collections.update(
        {
            #"jets"               : NTupleCollection("JetDirty",    genJetType,                   25, help="Cental jets after full selection but before cleaning, sorted by pt"),
            "genJets"            : NTupleCollection("GenJetDirty", genJetType,                   30, help="Gen Jets before cleaning, sorted by pt"),
            "genParticles"       : NTupleCollection("genPartAll",  genParticleWithMotherIndex,  300, help="all pruned genparticles"),
            "packedGenParticles" : NTupleCollection("PkdGenPart",  genParticleWithMotherIndex, 5000, help="all packed genparticles"),
            "packedPFCandidates" : NTupleCollection("PkdPFCands",  genParticleWithMotherIndex, 5000, help="all packed PF Candidates"),
            "gentopquarks"       : NTupleCollection("GenTop",      genParticleType,               2, help="Generated top quarks from hard scattering (needed separately for top pt reweighting)"),
        }
    )

## Event Analyzer for susy single-lepton (at the moment, it's the TTH one)
from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

addSoftTracks = False
if addSoftTracks:
    from PhysicsTools.Heppy.analyzers.objects.TrackAnalyzer import TrackAnalyzer
    trackAna = cfg.Analyzer(
        TrackAnalyzer, name='trackAnalyzer',
        setOff=False,
        trackOpt="reco",
        do_mc_match=True,
        )
    genTrackAna = cfg.Analyzer(
        TrackAnalyzer, name='GenTrackAnalyzer',
        setOff=False,
        trackOpt="gen",
        )
    # Insert TrackAna in the sequence:
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1,
                            genTrackAna)
    susyCoreSequence.insert(susyCoreSequence.index(genTrackAna)+1,
                            trackAna)

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
#susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
#                        ttHFatJetAna)
#susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
#                        ttHSVAna)
#susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
#                        ttHHeavyFlavourHadronAna)


## Insert declustering analyzer
#from CMGTools.TTHAnalysis.analyzers.ttHDeclusterJetsAnalyzer import ttHDeclusterJetsAnalyzer
#ttHDecluster = cfg.Analyzer(
#    ttHDeclusterJetsAnalyzer, name='ttHDecluster',
#    lepCut     = lambda lep,ptrel : lep.pt() > 10,
#    maxSubjets = 6, # for exclusive reclustering
#    ptMinSubjets = 5, # for inclusive reclustering
#    drMin      = 0.2, # minimal deltaR(l,subjet) required for a successful subjet match
#    ptRatioMax = 1.5, # maximum pt(l)/pt(subjet) required for a successful match
#    ptRatioDiff = 0.1,  # cut on abs( pt(l)/pt(subjet) - 1 ) sufficient to call a match successful
#    drMatch     = 0.02, # deltaR(l,subjet) sufficient to call a match successful
#    ptRelMin    = 5,    # maximum ptRelV1(l,subjet) sufficient to call a match successful
#    prune       = True, # also do pruning of the jets
#    pruneZCut       = 0.1, # pruning parameters (usual value in CMS: 0.1)
#    pruneRCutFactor = 0.5, # pruning parameters (usual value in CMS: 0.5)
#    verbose     = 0,   # print out the first N leptons
#    jetCut = lambda jet : jet.pt() > 20,
#    mcPartonPtCut = 20,
#    mcLeptonPtCut =  5,
#    mcTauPtCut    = 15,
#    )
#susyCoreSequence.insert(susyCoreSequence.index(ttHFatJetAna)+1, ttHDecluster)


## Single lepton + ST skim
#from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
#ttHSTSkimmer = cfg.Analyzer(
#    ttHSTSkimmer, name='ttHSTSkimmer',
#    minST = 200,
#    )

#add LHE Analyzer
from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer
LHEAna = LHEAnalyzer.defaultConfig
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                            LHEAna)

#from CMGTools.TTHAnalysis.analyzers.ttHReclusterJetsAnalyzer import ttHReclusterJetsAnalyzer
#ttHReclusterJets = cfg.Analyzer(
#    ttHReclusterJetsAnalyzer, name="ttHReclusterJetsAnalyzer",
#    pTSubJet = 30,
#    etaSubJet = 5.0,
#            )

#ttHLepSkim.allowLepTauComb = True
#susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
#                        susyLeptonMatchAna)
#susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
#                        susyTauMatchAna)
#leptonTypeSusyExtraLight.addVariables([
#    NTupleVariable("mcUCSXMatchId", lambda x : x.mcUCSXMatchId if hasattr(x,'mcUCSXMatchId') else -1, mcOnly=True, help="MC truth matching a la UCSX"),
#    ])
#tauTypeSusy.addVariables([
#    NTupleVariable("mcUCSXMatchId", lambda x : x.mcUCSXMatchId if hasattr(x,'mcUCSXMatchId') else -1, mcOnly=True, help="MC truth matching a la UCSX"),
#    ])

if lepAna.doIsolationScan:
    leptonTypeSusyExtraLight.addVariables([
        NTupleVariable("scanAbsIsoCharged005", lambda x : getattr(x, 'ScanAbsIsoCharged005', -999), help="PF abs charged isolation dR=0.05, no pile-up correction"),
        NTupleVariable("scanAbsIsoCharged01",  lambda x : getattr(x, 'ScanAbsIsoCharged01', -999),  help="PF abs charged isolation dR=0.1, no pile-up correction"),
        NTupleVariable("scanAbsIsoCharged02",  lambda x : getattr(x, 'ScanAbsIsoCharged02', -999),  help="PF abs charged isolation dR=0.2, no pile-up correction"),
        NTupleVariable("scanAbsIsoCharged03",  lambda x : getattr(x, 'ScanAbsIsoCharged03', -999),  help="PF abs charged isolation dR=0.3, no pile-up correction"),
        NTupleVariable("scanAbsIsoCharged04",  lambda x : getattr(x, 'ScanAbsIsoCharged04', -999),  help="PF abs charged isolation dR=0.4, no pile-up correction"),
        NTupleVariable("scanAbsIsoNeutral005", lambda x : getattr(x, 'ScanAbsIsoNeutral005', -999), help="PF abs neutral+photon isolation dR=0.05, no pile-up correction"),
        NTupleVariable("scanAbsIsoNeutral01",  lambda x : getattr(x, 'ScanAbsIsoNeutral01', -999),  help="PF abs neutral+photon isolation dR=0.1, no pile-up correction"),
        NTupleVariable("scanAbsIsoNeutral02",  lambda x : getattr(x, 'ScanAbsIsoNeutral02', -999),  help="PF abs neutral+photon isolation dR=0.2, no pile-up correction"),
        NTupleVariable("scanAbsIsoNeutral03",  lambda x : getattr(x, 'ScanAbsIsoNeutral03', -999),  help="PF abs neutral+photon isolation dR=0.3, no pile-up correction"),
        NTupleVariable("scanAbsIsoNeutral04",  lambda x : getattr(x, 'ScanAbsIsoNeutral04', -999),  help="PF abs neutral+photon isolation dR=0.4, no pile-up correction"),
        NTupleVariable("miniIsoR",             lambda x : getattr(x, 'miniIsoR', -999),             help="miniIso cone size"),
        NTupleVariable("effArea",              lambda x : getattr(x, 'EffectiveArea03', -999),      help="effective area used for PU subtraction"),
        NTupleVariable("rhoForEA",             lambda x : getattr(x, 'rho', -999),                  help="rho used for EA PU subtraction")
        ])

#TODO: uncomment this so the uncertainties are in the output
#if not removeJecUncertainty:
#    susyStop4Body_globalObjects.update({
#            "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
#            "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
#            })
#    susyStop4Body_collections.update({
#            "cleanJets_jecUp"       : NTupleCollection("Jet_jecUp",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC plus 1sigma)"),
#            "cleanJets_jecDown"     : NTupleCollection("Jet_jecDown",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC minus 1sigma)"),
#            "discardedJets_jecUp"   : NTupleCollection("DiscJet_jecUp", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC +1sigma)"),
#            "discardedJets_jecDown" : NTupleCollection("DiscJet_jecDown", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC -1sigma)"),
#            })

#susyCounter.doLHE = False

## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name = 'treeProducerStop4Body',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susyStop4Body_globalVariables,
     globalObjects = susyStop4Body_globalObjects,
     collections = susyStop4Body_collections,
)

if not runSMS:
    susyScanAna.doLHE = False # until a proper fix is put in the analyzer
    susyScanAna.useLumiInfo = False
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer), susyCounter)
else:
    lheWeightAna.useLumiInfo = True
    susyScanAna.useLumiInfo  = True
    susyScanAna.doLHE        = True
    susyCounter.bypass_trackMass_check = False
    susyCounter.SMS_varying_masses     = [ 'genSusyMNeutralino','genSusyMChargino' , 'genSusyMStop']
    susyCoreSequence.insert(susyCoreSequence.index(susyScanAna)+1, susyCounter)

jsonAna.useLumiBlocks = True


# HBHE new filter
#from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
#hbheAna = cfg.Analyzer(
#    hbheAnalyzer, name="hbheAnalyzer", IgnoreTS4TS5ifJetInLowBVRegion=False
#    )
#if not runSMS:
#    susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),hbheAna)
#    treeProducer.globalVariables.append(NTupleVariable("hbheFilterNew50ns", lambda ev: ev.hbheFilterNew50ns, int, help="new HBHE filter for 50 ns"))
#    treeProducer.globalVariables.append(NTupleVariable("hbheFilterNew25ns", lambda ev: ev.hbheFilterNew25ns, int, help="new HBHE filter for 25 ns"))
#    #treeProducer.globalVariables.append(NTupleVariable("hbheFilterIso", lambda ev: ev.hbheFilterIso, int, help="HBHE iso-based noise filter"))
#    #treeProducer.globalVariables.append(NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"))
#    #treeProducer.globalVariables.append(NTupleVariable("Flag_badMuonFilter", lambda ev: ev.badMuon, help="bad muon filter decision"))

#-------- SAMPLES AND TRIGGERS -----------

#from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *
from CMGTools.RootTools.samples.triggers_13TeV_Spring16_degStop import *
triggerFlagsAna.triggerBits = {}
for trigger in  triggers:
  trigger_name = "trigger_{trig}".format(trig=trigger.replace("_v*","") )
  HLT_name = "{trig}".format(trig=trigger.replace("_v*","").replace("HLT_","") )
  triggerFlagsAna.triggerBits[HLT_name] = eval( trigger_name )

#triggerFlagsAna.triggerBits = {
#  'HT2000': ['HLT_HT2000_v*'],
#  'Ele25_eta2p1_WPTight_Gsf': ['HLT_Ele25_eta2p1_WPTight_Gsf_v*'],
#  'PFMET110_PFMHT110_IDTight': ['HLT_PFMET110_PFMHT110_IDTight_v*'],
#  'PFJet450': ['HLT_PFJet450_v*'],
#  'PFMETNoMu100_PFMHTNoMu100_IDTight': ['HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v*'],
#  'Ele25_WPTight_Gsf': ['HLT_Ele25_WPTight_Gsf_v*'],
#  'IsoMu27': ['HLT_IsoMu27_v*'],
#  'Mu3er_PFHT140_PFMET125': ['HLT_Mu3er_PFHT140_PFMET125_v*'],
#  'MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight': ['HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v*'],
#  'Ele32_eta2p1_WPTight_Gsf': ['HLT_Ele32_eta2p1_WPTight_Gsf_v*'],
#  'MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight': ['HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight_v*'],
#  'PFMETNoMu90_PFMHTNoMu90_IDTight': ['HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v*'],
#  'AK8PFJet450': ['HLT_AK8PFJet450_v*'],
#  'Ele22_eta2p1_WPLoose_Gsf': ['HLT_Ele22_eta2p1_WPLoose_Gsf_v*'],
#  'MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight': ['HLT_MonoCentralPFJet80_PFMETNoMu100_PFMHTNoMu100_IDTight_v*'],
#  'PFMET120_PFMHT120_IDTight': ['HLT_PFMET120_PFMHT120_IDTight_v*'],
#  'Mu50': ['HLT_Mu50_v*'],
#  'IsoMu22_eta2p1': ['HLT_IsoMu22_eta2p1_v*'],
#  'MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight': ['HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight_v*'],
#  'Ele24_eta2p1_WPLoose_Gsf': ['HLT_Ele24_eta2p1_WPLoose_Gsf_v*'],
#  'HT2500': ['HLT_HT2500_v*'],
#  'PFMET120_Mu5': ['HLT_PFMET120_Mu5_v*'],
#  'PFHT800': ['HLT_PFHT800_v*'],
#  'PFHT900': ['HLT_PFHT900_v*'],
#  'PFMET90_PFMHT90_IDTight': ['HLT_PFMET90_PFMHT90_IDTight_v*'],
#  'Ele27_WPTight_Gsf': ['HLT_Ele27_WPTight_Gsf_v*'],
#  'PFMET170_NoiseCleaned': ['HLT_PFMET170_NoiseCleaned_v*'],
#  'IsoTkMu22_eta2p1': ['HLT_IsoTkMu22_eta2p1_v*'],
#  'Ele27_eta2p1_WPLoose_Gsf_HT200': ['HLT_Ele27_eta2p1_WPLoose_Gsf_HT200_v*'],
#  'IsoTkMu24': ['HLT_IsoTkMu24_v*'],
#  'IsoMu22': ['HLT_IsoMu22_v*'],
#  'IsoMu24': ['HLT_IsoMu24_v*'],
#  'IsoTkMu22': ['HLT_IsoTkMu22_v*'],
#  'Ele25_eta2p1_WPLoose_Gsf': ['HLT_Ele25_eta2p1_WPLoose_Gsf_v*'],
#  'IsoTkMu27': ['HLT_IsoTkMu27_v*'],
#  'PFMET100_PFMHT100_IDTight': ['HLT_PFMET100_PFMHT100_IDTight_v*'],
#  'Ele27_eta2p1_WPTight_Gsf': ['HLT_Ele27_eta2p1_WPTight_Gsf_v*'],
#  'PFMETNoMu110_PFMHTNoMu110_IDTight': ['HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v*'],
#  'PFMETNoMu120_PFMHTNoMu120_IDTight': ['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*']
#}
triggerFlagsAna.unrollbits = False
triggerFlagsAna.saveIsUnprescaled = False
triggerFlagsAna.checkL1prescale = False

#if runSMS:
#    susyCoreSequence.remove(triggerFlagsAna)
#    susyCoreSequence.remove(triggerAna)
#    susyCoreSequence.remove(eventFlagsAna)

selectedComponents = []

if not run2017:
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
    #from CMGTools.RootTools.samples.samples_13TeV_signals import *
    #from CMGTools.RootTools.samples.samples_13TeV_80X_susySignalsPriv import *
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
    from CMGTools.RootTools.samples.samples_Stop4Body import *

    selectedComponents = [
        TTJets,
        TT_pow,
    #    TT_pow_backup,
        TTJets_SingleLeptonFromTbar,
        TTJets_SingleLeptonFromTbar_ext,
        TTJets_SingleLeptonFromT,
        TTJets_SingleLeptonFromT_ext,
        TTJets_DiLepton,
        TTJets_DiLepton_ext,
        TTJets_LO_HT600to800_ext,
        TTJets_LO_HT800to1200_ext,
        TTJets_LO_HT1200to2500_ext,
        TTJets_LO_HT2500toInf_ext,
    ]

    if runWJets:
        selectedComponents = [
            WJetsToLNu,
            WJetsToLNu_LO,
            WJetsToLNu_HT70to100,
            WJetsToLNu_HT100to200,
            WJetsToLNu_HT100to200_ext,
            WJetsToLNu_HT100to200_ext2,
            WJetsToLNu_HT200to400,
            WJetsToLNu_HT200to400_ext,
            WJetsToLNu_HT200to400_ext2,
            WJetsToLNu_HT400to600,
            WJetsToLNu_HT400to600_ext,
            WJetsToLNu_HT600to800,
            WJetsToLNu_HT600to800_ext,
            WJetsToLNu_HT800to1200,
            WJetsToLNu_HT800to1200_ext,
            WJetsToLNu_HT1200to2500,
            WJetsToLNu_HT1200to2500_ext,
            WJetsToLNu_HT2500toInf,
            WJetsToLNu_HT2500toInf_ext,
            WJetsToLNu_Pt_100to250,
            WJetsToLNu_Pt_100to250_ext,
            WJetsToLNu_Pt_250to400,
            WJetsToLNu_Pt_250to400_ext,
            WJetsToLNu_Pt_400to600,
            WJetsToLNu_Pt_400to600_ext,
            WJetsToLNu_Pt_600toInf,
            WJetsToLNu_Pt_600toInf_ext,
        ]

    if runZInv:
        selectedComponents = [
            ZJetsToNuNu_HT100to200,
            ZJetsToNuNu_HT100to200_ext,
            ZJetsToNuNu_HT200to400,
            ZJetsToNuNu_HT200to400_ext,
            ZJetsToNuNu_HT400to600,
            ZJetsToNuNu_HT400to600_ext,
            ZJetsToNuNu_HT600to800,
            ZJetsToNuNu_HT800to1200,
            ZJetsToNuNu_HT1200to2500,
            ZJetsToNuNu_HT1200to2500_ext,
            ZJetsToNuNu_HT2500toInf,
        ]

    if runOtherMC1:
        selectedComponents = [
            WW,
            WW_ext,
            WZ,
            WZ_ext,
            ZZ,
            ZZ_ext,
            DYJetsToLL_M5to50_HT100to200,
            DYJetsToLL_M5to50_HT100to200_ext,
            DYJetsToLL_M5to50_HT200to400,
            DYJetsToLL_M5to50_HT200to400_ext,
            DYJetsToLL_M5to50_HT400to600,
            DYJetsToLL_M5to50_HT400to600_ext,
            DYJetsToLL_M5to50_HT600toInf,
            DYJetsToLL_M5to50_HT600toInf_ext,
            DYJetsToLL_M50_HT70to100,
            DYJetsToLL_M50_HT100to200,
            DYJetsToLL_M50_HT100to200_ext,
            DYJetsToLL_M50_HT200to400,
            DYJetsToLL_M50_HT200to400_ext,
            DYJetsToLL_M50_HT400to600,
            DYJetsToLL_M50_HT400to600_ext,
            DYJetsToLL_M50_HT600to800,
            DYJetsToLL_M50_HT800to1200,
            DYJetsToLL_M50_HT1200to2500,
            DYJetsToLL_M50_HT2500toInf,
        ]
    if runOtherMC2:
        selectedComponents = [
            TBar_tWch_ext,
            T_tch_powheg,
            T_tWch_ext,
            TBar_tch_powheg,
            QCD_HT50to100,
            QCD_HT100to200,
            QCD_HT200to300,
            QCD_HT200to300_ext,
            QCD_HT300to500,
            QCD_HT300to500_ext,
            QCD_HT500to700,
            QCD_HT500to700_ext,
            QCD_HT700to1000,
            QCD_HT700to1000_ext,
            QCD_HT1000to1500,
            QCD_HT1000to1500_ext,
            QCD_HT1500to2000,
            QCD_HT1500to2000_ext,
            QCD_HT2000toInf,
            QCD_HT2000toInf_ext,
            TTW_LO,
            TTWToQQ,
            TTWToLNu_ext,
            TTWToLNu_ext2,
            TTGJets,
            TTGJets_ext,
            TTZ_LO,
            TTZToLLNuNu_ext,
            TTZToLLNuNu_m1to10,
            TTZToQQ,
        ]
    if runSMS: # For running on signal
        #from CMGTools.RootTools.samples.samples_13TeV_80X_susySignalsPriv import *
        #selectedComponents = [ SMS_T2tt_genHT_160_genMET_80_mStop_275_mLSP_205 ]
        #selectedComponents = [ SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1 ]
        selectedComponents = signalSamples
        selectedComponents = [ SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1 ]

    if runFullSimSignal:
        selectedComponents = signalFullSim

    if runData: # For running on data
        selectedComponents = [
            JetHT_Run2016B_03Feb2017_v2,
            JetHT_Run2016C_03Feb2017,
            JetHT_Run2016D_03Feb2017,
            JetHT_Run2016E_03Feb2017,
            JetHT_Run2016F_03Feb2017,
            JetHT_Run2016G_03Feb2017,
            JetHT_Run2016H_03Feb2017_v2,
            JetHT_Run2016H_03Feb2017_v3,
            MET_Run2016B_03Feb2017_v2,
            MET_Run2016C_03Feb2017,
            MET_Run2016D_03Feb2017,
            MET_Run2016E_03Feb2017,
            MET_Run2016F_03Feb2017,
            MET_Run2016G_03Feb2017,
            MET_Run2016H_03Feb2017_v2,
            MET_Run2016H_03Feb2017_v3,
            SingleElectron_Run2016B_03Feb2017_v2,
            SingleElectron_Run2016C_03Feb2017,
            SingleElectron_Run2016D_03Feb2017,
            SingleElectron_Run2016E_03Feb2017,
            SingleElectron_Run2016F_03Feb2017,
            SingleElectron_Run2016G_03Feb2017,
            SingleElectron_Run2016H_03Feb2017_v2,
            SingleElectron_Run2016H_03Feb2017_v3,
            SingleMuon_Run2016B_03Feb2017_v2,
            SingleMuon_Run2016C_03Feb2017,
            SingleMuon_Run2016D_03Feb2017,
            SingleMuon_Run2016E_03Feb2017,
            SingleMuon_Run2016F_03Feb2017,
            SingleMuon_Run2016G_03Feb2017,
            SingleMuon_Run2016H_03Feb2017_v2,
            SingleMuon_Run2016H_03Feb2017_v3,
        ]
        for comp in selectedComponents:
            comp.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
        #if test != 0 and jsonAna in susyCoreSequence: susyCoreSequence.remove(jsonAna)
else:
    from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import *
    from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import *
    selectedComponents = [
        TTJets,
        TTLep_pow,
        TTHad_pow,
        TTSemi_pow,
    ]
    if runWJets:
        selectedComponents = [
            WJetsToLNu_LO,
            W1JetsToLNu_LO,
            W2JetsToLNu_LO,
            W3JetsToLNu_LO,
            W4JetsToLNu_LO,
        ]
    if runZInv:
        selectedComponents = [
        ]
    if runOtherMC1:
        selectedComponents = [
            WW,
            WZ,
            ZZ,
            DYJetsToLL_M50,
            DYJetsToLL_M50_ext,
            DYJetsToLL_M50_LO,
            DYJetsToLL_M50_LO_ext,
        ] + DYJetsToLLM4to50HT + DYJetsToLLM50HT
    if runOtherMC2:
        selectedComponents = [
            T_sch_lep, #TODO: Look for TBar. Hasn't been created until date.
            T_tch,
            TBar_tch,
            T_tWch_noFullyHad,
            TBar_tWch_noFullyHad,
        ] + QCDHT + TTXs + TTXXs
    if runSMS:
        selectedComponents = []
    if runFullSimSignal:
        selectedComponents = []
    if runData:
        selectedComponents = [
            JetHT_Run2017B_17Nov2017,
            JetHT_Run2017C_17Nov2017,
            JetHT_Run2017D_17Nov2017,
            JetHT_Run2017E_17Nov2017,
            JetHT_Run2017F_17Nov2017,
            MET_Run2017B_17Nov2017,
            MET_Run2017C_17Nov2017,
            MET_Run2017D_17Nov2017,
            MET_Run2017E_17Nov2017,
            MET_Run2017F_17Nov2017,
            SingleElectron_Run2017B_17Nov2017,
            SingleElectron_Run2017C_17Nov2017,
            SingleElectron_Run2017D_17Nov2017,
            SingleElectron_Run2017E_17Nov2017,
            SingleElectron_Run2017BF_17Nov2017,
            SingleMuon_Run2017B_17Nov2017,
            SingleMuon_Run2017C_17Nov2017,
            SingleMuon_Run2017D_17Nov2017,
            SingleMuon_Run2017E_17Nov2017,
            SingleMuon_Run2017F_17Nov2017,
        ]
        for comp in selectedComponents:
            comp.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"

#ISR jet counting
from CMGTools.TTHAnalysis.analyzers.nIsrAnalyzer import NIsrAnalyzer
nISRAna = cfg.Analyzer(NIsrAnalyzer, name="NIsrAnalyzer",)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), nISRAna)

#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
    ttHEventAna,
    treeProducer,
    ])
preprocessor = None


#-------- HOW TO RUN
test = getHeppyOption('test')
if test==1:
    # test a single component, using a single thread.
    comp = selectedComponents[0]
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    #comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        #comp.fineSplitFactor = 1

## Auto-AAA
from CMGTools.RootTools.samples.autoAAAconfig import *
if not getHeppyOption("isCrab"):
    autoAAA(selectedComponents)

outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerStop4Body/tree.root',
    option='recreate'
    )
outputService.append(output_service)

from CMGTools.HToZZ4L.tools.configTools import printSummary
printSummary(selectedComponents)

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload if not preprocessor else Events
EOSEventsWithDownload.aggressive = 2 # always fetch if running on Wigner
if getHeppyOption("nofetch") or getHeppyOption("isCrab"):
    event_class = Events
    if preprocessor: preprocessor.prefetch = False
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = outputService,
                     preprocessor = preprocessor,
                     events_class = event_class)
