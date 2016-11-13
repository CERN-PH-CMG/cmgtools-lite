##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES       ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *

#JSON
jsonAna.useLumiBlocks = True

####### Leptons  #####
# lep collection
lepAna.packedCandidates = 'packedPFCandidates'

## ELECTRONS
lepAna.loose_electron_eta = 2.4
lepAna.loose_electron_pt  = 10
lepAna.inclusive_electron_pt  = 10

eleID = "CBID"

if eleID == "CBID":
  lepAna.loose_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto"
  lepAna.loose_electron_lostHits = 999. # no cut since embedded in ID
  lepAna.loose_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.loose_electron_dz     = 999. # no cut since embedded in ID

  lepAna.inclusive_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_Veto"
  lepAna.inclusive_electron_lostHits = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

elif eleID == "MVAID":
  lepAna.inclusive_electron_id  = "" # same as in susyCore
  lepAna.loose_electron_id = "POG_MVA_ID_Spring15_NonTrig_VLoose" # Spring15 25ns era

elif eleID == "Incl": # as inclusive as possible
  lepAna.loose_electron_id  = ""
  lepAna.loose_electron_lostHits = 999. # no cut
  lepAna.loose_electron_dxy    = 999.
  lepAna.loose_electron_dz     = 999.

  lepAna.inclusive_electron_id  = ""
  lepAna.inclusive_electron_lostHits = 999.  # no cut
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

## MUONS
lepAna.loose_muon_pt  = 10
lepAna.inclusive_muon_pt  = 10

# Isolation
isolation = "miniIso"

if isolation == "miniIso":
  # do miniIso
  lepAna.doMiniIsolation = True
  lepAna.miniIsolationPUCorr = 'rhoArea'
  lepAna.miniIsolationVetoLeptons = None
  lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
  lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
  # normal relIso03
  lepAna.ele_isoCorr = "rhoArea"
  lepAna.mu_isoCorr = "rhoArea"

  lepAna.loose_electron_relIso = 0.5
  lepAna.loose_muon_relIso = 0.5

########################
###### ANALYZERS #######
########################

#add LHE ana for HT info
from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer
LHEAna = LHEAnalyzer.defaultConfig

from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
  ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
  minJets25 = 0,
  )

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
      ttHFatJetAna)
#susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
#     ttHSVAna)

# Add anyLepSkimmer
from CMGTools.TTHAnalysis.analyzers.anyLepSkimmer import anyLepSkimmer
anyLepSkim = cfg.Analyzer(
    anyLepSkimmer, name='anyLepSkimmer',
    minLeptons = 0,
    maxLeptons = 999,
)
susyCoreSequence.insert(susyCoreSequence.index(lepAna)+1, anyLepSkim)

## Single lepton + ST skim
from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
ttHSTSkimmer = cfg.Analyzer(
  ttHSTSkimmer, name='ttHSTSkimmer',
  minST = 150,
  )

## HT skim
from CMGTools.TTHAnalysis.analyzers.ttHHTSkimmer import ttHHTSkimmer
ttHHTSkimmer = cfg.Analyzer(
  ttHHTSkimmer, name='ttHHTSkimmer',
  minHT = 350,
  )

#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import * # central trigger list
from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *

#-------- TRIGGERS -----------
triggerFlagsAna.triggerBits = {
  ## hadronic
  'HT350' : triggers_HT350,
  'HT600' : triggers_HT600,
  'HT800' : triggers_HT800,
  'HT900' : triggers_HT900,
  'MET170' : triggers_MET170,
  'HT350MET120' : triggers_HT350MET120,
  'HT350MET100' : triggers_HT350MET100,
  'HTMET' : triggers_HT350MET100 + triggers_HT350MET120,
  'PFJet450' : triggers_pfjet450,
  'AK4PFJet450' : triggers_ak4pfjet450,
  'AK8PFJet450' : triggers_ak8pfjet450,
  'CaloJet500' : triggers_calojet500,

  ##MET test
  'MET170_HBHE' : triggers_MET170_HBHECleaned,
  'MET170_BH' : triggers_MET170_BeamHaloCleaned,
  'MET170_HBHE_BH' : triggers_MET170_HBHE_BeamHaloCleaned,
  'MET190_TypeOne_HBHE_BH' : triggers_METTypeOne190_HBHE_BeamHaloCleaned,
  
  'MET100MHT100' : triggers_MET100MHT100,
  ## muon
  'SingleMu' : triggers_1mu,
  'IsoMu27' : triggers_1mu,
  'IsoMu20' : triggers_1mu20,
  'IsoMu24' : triggers_1mu24,
  'Mu45eta2p1' : trigger_1mu_noiso_r,
  'Mu50' : trigger_1mu_noiso_w,
  'MuHT600' : triggers_mu_ht600,
  'MuHT400MET70' : triggers_mu_ht400_met70,
  'MuHT350MET70' : triggers_mu_ht350_met70,
  'MuHT350MET50' : triggers_mu_ht350_met50,
  'MuHT350' : triggers_mu_ht350,
  'MuHT400' : triggers_mu_ht400,
  'Mu50HT400' : triggers_mu50_ht400,
  'MuHTMET' : triggers_mu_ht350_met70 + triggers_mu_ht400_met70,
  'MuMET120' : triggers_mu_met120,
  'MuHT400B': triggers_mu_ht400_btag,
  ## electrons
  'IsoEle32' : triggers_1el,
  'IsoEle23' : triggers_1el23,
  'IsoEle22' : triggers_1el22,
  'IsoEle27T' : triggers_1el27WPTight,
  'Ele105' : trigger_1el_noiso,
  'Ele115' : trigger_1el_noiso_115,
  'EleHT600' : triggers_el_ht600,
  'EleHT400MET70' : triggers_el_ht400_met70,
  'EleHT350MET70' : triggers_el_ht350_met70,
  'EleHT350MET50' : triggers_el_ht350_met50,
  'EleHT350' : triggers_el_ht350,
  'EleHT400' : triggers_el_ht400,
  'Ele50HT400' : triggers_el50_ht400,
  'EleHTMET' : triggers_el_ht350_met70 + triggers_el_ht400_met70,
  'EleHT200' :triggers_el_ht200,
  'EleHT400B': triggers_el_ht400_btag
  }

#########################
# --- LEPTON SKIMMING ---
#########################

## OTHER LEPTON SKIMMER
anyLepSkim.minLeptons = 0
anyLepSkim.maxLeptons = 999

# GOOD LEPTON SKIMMER -- FROM TTH (in Core already)
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999

####### JETS #########
jetAna.jetPt = 20
jetAna.jetEta = 2.4

# --- JET-LEPTON CLEANING ---
#jetAna.cleanSelectedLeptons = True
jetAna.minLepPt = 10

## JEC
jetAna.mcGT = "Spring16_25nsV6_MC"
#jetAna.dataGT = "Summer15_25nsV6_DATA"
jetAna.dataGT = "Spring16_25nsV6_DATA"
# add also JEC up/down shifts corrections
jetAna.addJECShifts = True

jetAna.doQG = True
jetAna.smearJets = False #should be false in susycore, already
jetAna.recalibrateJets = False # false for miniAOD v2!
jetAna.applyL2L3Residual = True

#jetAna.calculateType1METCorrection = True
## MET (can be used for MiniAODv2)
metAna.recalibrate = True

## Iso Track
isoTrackAna.setOff=False

# store all taus by default
genAna.allGenTaus = True

#-------- HOW TO RUN
isData = True # default, but will be overwritten below

#sample = 'MC'
sample = 'data'
#sample = 'Signal'
test = 1

if sample == "MC":

  print 'Going to process MC'

  isData = False
  isSignal = False

  # modify skim
  anyLepSkim.minLeptons = 1
  ttHLepSkim.minLeptons = 0

  # -- new 74X samples
  #from CMGTools.RootTools.samples.samples_13TeV_74X import *
  # -- samples at DESY
  # MiniAODv1
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_74X_desy import *
  # MiniAODv2
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_RunIISpring15MiniAODv2_desy import *
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_RunIISpring15MiniAODv2_desy_Compact import *
  from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *
#  from CMGTools.RootTools.samples.samples_13TeV_MiniAODv2_Signals_desy import *
#  selectedComponents = TTs + SingleTop #TTJets_SingleLepton

  selectedComponents = [TBarToLeptons_tch_powheg]

  if test==1:
    # test a single component, using a single thread.
    comp = QCD_HT300to500
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 2
  elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 1
      comp.files = comp.files[:1]
  elif test==3:
    # run all components (1 thread per component).
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)
  elif test==0:
    # PRODUCTION
    # run on everything

    #selectedComponents =  [TTJets_LO , TTJets_LO_HT600to800, TTJets_LO_HT800to1200, TTJets_LO_HT1200to2500, TTJets_LO_HT2500toInf] + QCDHT + WJetsToLNuHT + SingleTop + DYJetsM50HT + TTV
    #selectedComponents =  #SingleTop + DYJetsM50HT + TTV
    #selectedComponents = [TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromTbar_ext, TTJets_SingleLeptonFromT, TTJets_SingleLeptonFromT_ext, TTJets_DiLepton, TTJets_DiLepton_ext]

    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)

elif sample == "Signal":

  print 'Going to process Signal'

  isData = False
  isSignal = True

  # Set FastSim JEC
  #jetAna.mcGT = "FastSim_MCRUN2_74_V9"
  #jetAna.mcGT = "MCRUN2_74_V9"
#  jetAna.mcGT = "FastSim_Summer15_25nsV6_MC"

  #### REMOVE JET ID FOR FASTSIM
  jetAna.relaxJetId = True

  # modify skim
  anyLepSkim.minLeptons = 0
  ttHLepSkim.minLeptons = 0

  # -- new 74X samples
  #from CMGTools.RootTools.samples.samples_13TeV_74X import *
  # -- samples at DESY
  # MiniAODv1
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_74X_desy import *
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_74X_Signals_desy import *
  # MiniAODv2
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_RunIISpring15MiniAODv2_desy import *
#  from CMGTools.SUSYAnalysis.samples.samples_13TeV_MiniAODv2_Signals_AAA import *
  from CMGTools.RootTools.samples.samples_80x_signal import *
  # Benchmarks
  #selectedComponents = [ T1tttt_mGo_1475to1500_mLSP_1to1250, T1tttt_mGo_1500to1525_mLSP_50to1125, T1tttt_mGo_1200_mLSP_1to825, T1tttt_mGo_1900to1950_mLSP_0to1450 ]
  # Rest
  #selectedComponents = mcSamplesT1tttt
  #selectedComponents = [T1tttt_mGo_1000to1050_mLSP_1to800, T1tttt_mGo_1225to1250_mLSP_1to1025, T1tttt_mGo_1325to1350_mLSP_1to1125, T1tttt_mGo_600to625_mLSP_250to375]
  selectedComponents = [SMS_T1tttt_TuneCUETP8M1]#[T1tttt_mGo_1475to1500_mLSP_1to1250, T1tttt_mGo_1200_mLSP_1to825 ]

  if test==1:
    # test a single component, using a single thread.
    comp  = SMS_T1tttt_TuneCUETP8M1
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 1
  elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 1
      comp.files = comp.files[:1]
  elif test==3:
    # run all components (1 thread per component).
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)
  elif test==0:
    # PRODUCTION
    # run on everything

    #selectedComponents = [ T1tttt_mGo_1200_mLSP_1to825, T1tttt_mGo_1900to1950_mLSP_0to1450 ]

    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)



elif sample == "data":

  print 'Going to process DATA'

  isData = True
  isSignal = False

  # modify skim
  anyLepSkim.minLeptons = 1
  ttHLepSkim.minLeptons = 0

  #For now no JEC
  #print jetAna.shiftJEC , jetAna.recalibrateJets , jetAna.addJECShifts , jetAna.calculateSeparateCorrections , jetAna.calculateType1METCorrection
  #jetAna.addJECShifts = False
  #jetAna.doQG = False
  #jetAna.smearJets = False #should be false in susycore, already
  jetAna.recalibrateJets = True # false for miniAOD v2!
  #jetAna.calculateSeparateCorrections = False
  #jetAna.applyL2L3Residual = False
  #print jetAna.shiftJEC , jetAna.recalibrateJets , jetAna.addJECShifts , jetAna.calculateSeparateCorrections , jetAna.calculateType1METCorrection

  # central samples
  from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
  #from CMGTools.SUSYAnalysis.samples.samples_13TeV_DATA2016 import *

  #  selectedComponents = [SingleElectron_Run2016B_PromptReco_v2, SingleMuon_Run2016B_PromptReco_v2, JetHT_Run2016B_PromptReco_v2_HT800Only]
#  selectedComponents = [JetHT_Run2016B_PromptReco_v2_HT800Only, JetHT_Run2016C_PromptReco_v2_HT800Only]#, JetHT_Run2016D_PromptReco_v2_HT800Only]
#  selectedComponents = [JetHT_Run2016C_PromptReco_v2_HT800Only]#, JetHT_Run2016D_PromptReco_v2_HT800Only]
#  selectedComponents = [JetHT_Run2016F_PromptReco_v1_HT800Only]
#  selectedComponents = [SingleMuon_Run2016F_PromptReco_v1_IsoMu27Only]

  selectedComponents = [JetHT_Run2016H_PromptReco_v2_HT800Only, SingleMuon_Run2016H_PromptReco_v2_IsoMu27Only, SingleElectron_Run2016H_PromptReco_v2_Ele27Only, JetHT_Run2016G_PromptReco_v1_HT800Only, SingleMuon_Run2016G_PromptReco_v1_IsoMu27Only, SingleElectron_Run2016G_PromptReco_v1_Ele27Only]

  if test!=0 and jsonAna in susyCoreSequence: susyCoreSequence.remove(jsonAna)
  if test==1:
    # test one component (2 thread)
    comp = SingleElectron_Run2016B_PromptReco_v2 #JetHT_Run2016B_PromptReco_v2_HT800Only
#SingleElectron_Run2016B_PromptReco_v2
#    comp.files = comp.files[:1]
    comp.files = comp.files[10:12]
    #comp.files = comp.files[10:11]
    selectedComponents = [comp]
    comp.splitFactor = len(comp.files)
  elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 1
#      comp.files = comp.files[:1]
      comp.files = comp.files[10:11]
  elif test==3:
    # run all components (10 files per component).
    for comp in selectedComponents:
      comp.files = comp.files[20:30]
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)
  elif test==0:
    # PRODUCTION
    # run on everything
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)



## PDF weights
PDFWeights = []
#PDFWeights = [ ("CT10",53), ("MSTW2008lo68cl",41), ("NNPDF21_100",101) ]
#PDFWeights = [ ("CT10nlo",53),("MSTW2008nlo68cl",41),("NNPDF30LO",101),("NNPDF30_nlo_nf_5_pdfas",103), ("NNPDF30_lo_as_0130",101)]
#PDFWeights = [ ("NNPDF30_lo_as_0130",101) ]
# see for TTJets  https://github.com/cms-sw/genproductions/blob/c41ab29f3d86c9e53df8b0d76c12cd519adbf013/bin/MadGraph5_aMCatNLO/cards/production/13TeV/tt0123j_5f_ckm_LO_MLM/tt0123j_5f_ckm_LO_MLM_run_card.dat#L52
# and then https://lhapdf.hepforge.org/pdfsets.html

#--------- Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusySingleLepton import *
treeProducer = cfg.Analyzer(
  AutoFillTreeProducer, name='treeProducerSusySingleLepton',
  vectorTree = True,
  saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
  defaultFloatType = 'F', # use Float_t for floating point
  PDFWeights = PDFWeights,
  globalVariables = susySingleLepton_globalVariables,
  globalObjects = susySingleLepton_globalObjects,
  collections = susySingleLepton_collections,
  )


if isSignal:
  ## SUSY Counter
  ## histo counter
  #susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer),
  susyCoreSequence.insert(susyCoreSequence.index(susyScanAna)+1,
        susyCounter)
#  susyCoreSequence.append(susyCounter)


  # change scn mass parameters
  susyCounter.SUSYmodel = 'T1tttt'
  susyCounter.SMS_mass_1 = "genSusyMGluino"
  susyCounter.SMS_mass_2 = "genSusyMNeutralino"
  susyCounter.SMS_varying_masses = ['genSusyMGluino','genSusyMNeutralino']

#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
    LHEAna,
    ttHEventAna,
#    ttHSTSkimmer,
    ttHHTSkimmer,
    treeProducer,
#   susyCounter
    ])

# remove skimming for Data or Signal
#if isData:# or isSignal :
# sequence.remove(ttHHTSkimmer)
# sequence.remove(ttHSTSkimmer)

if isSignal:
 sequence.remove(ttHHTSkimmer)
# sequence.remove(ttHSTSkimmer)
 sequence.remove(eventFlagsAna)
#  sequence.remove(hbheFilterAna)

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerSusySingleLepton/tree.root',
    #fname='susyCounter/counts.root',
    option='recreate'
    )
outputService.append(output_service)

print "running"
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
         sequence = sequence,
         services = outputService,
         events_class = Events)
