import PhysicsTools.HeppyCore.framework.config as cfg

##from CMGTools.RootTools.samples.autoAAAconfig import *

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import * #<--miniAOD v2 2016 MC for ICHEP
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *  #<--miniAOD v1 2016 DATA

from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import triggers_1mu_iso_50ns, triggers_mumu, triggers_ee, triggers_photon30, triggers_photon50, triggers_photon75, triggers_photon90, triggers_photon120, triggers_photon165_HE10, triggers_jet, triggers_dijet, triggers_HT350, triggers_HT475, triggers_HT600, triggers_HT800, triggers_HT900, triggers_Jet80MET90

###add some special trigger
triggers_1mu_iso_Zeynep = [ 'HLT_IsoTkMu22_v*','HLT_IsoMu22_v*','HLT_IsoMu24_v*','HLT_IsoMu27_v*']
triggers_1ele_iso_Zeynep = [ 'HLT_Ele27_eta2p1_WPLoose_Gsf_v*','HLT_Ele27_WPTight_Gsf_v*','HLT_Ele35_WPLoose_Gsf_v*']

#https://hypernews.cern.ch/HyperNews/CMS/get/susy-interpretations/247.html
triggers_mumu_noniso_Dominick = ['HLT_Mu30_TkMu11_v3','HLT_Mu50_v4', 'HLT_TkMu50_v3']
triggers_ee_noniso_Dominick = ['HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_MW_v6','HLT_Ele105_CaloIdVT_GsfTrkIdT_v6']

##goldenJson = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276384_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
goldenJson = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'


#-------- INITIAL FLAG
isDiJet=False
isMonoJet=False
isZSkim=False
is1L=False
is1PH=False
isEle = False # default is diMuon
is25ns = True

#-------- HOW TO RUN

# diJet = 15(Data) 25(MC)
# diMu/diEle  = 13(Data) 23(MC)
# gamma  = 16(Data) 17,18,19(MC)

#-------- HOW TO RUN

test = 23

if test==0:
    selectedComponents = [DoubleMu_742, DoubleMu_740p9]
#    selectedComponents = [ DoubleMuParked_1Apr_RelVal_dm2012D_v2_newPFHCalib , DoubleMuParked_1Apr_RelVal_dm2012D_v2_oldPFHCalib , DoubleMuparked_1Apr_RelVal_dm2012D_v2 ]
    for comp in selectedComponents:
        comp.splitFactor = 251
        comp.files = comp.files[:]
        comp.triggers = triggers_8TeV_mumu

elif test==1:
    selectedComponents = [ RelValZMM_7_4_1,RelValZMM_7_4_0_pre9 ]
#    selectedComponents = [RelVal_741_Philfixes]
#    selectedComponents = relValkate
    for comp in selectedComponents:
#        comp.splitFactor = 1
        comp.splitFactor = 100
        comp.files = comp.files[:]

elif test==2:
#    isZSkim=True
    is25ns=True
    selectedComponents = [ DYJetsToLL_M50 ]
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.files = ['root://eoscms///store/mc/RunIISpring16MiniAODv2/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/40000/C06A61EE-EF25-E611-870A-02163E011A12.root']

#elif test==2:
#    selectedComponents = [ TTJets_50ns ]
#    isZSkim=True
#    for comp in selectedComponents:
#        comp.triggers = triggers_mumu
#        comp.splitFactor = 1
#        comp.files = ['/afs/cern.ch/user/d/dalfonso/public/TTbarMadP850ns/0066F143-F8FD-E411-9A0B-D4AE526A0D2E.root']
##        comp.files = comp.files[:1]



   # ----------------------- Summer15 options -------------------------------------------------------------------- #
elif test==2:
    selectedComponents = [ DYJetsToLL_M50 ]
    isZSkim=True
    for comp in selectedComponents:
        comp.triggers = triggers_mumu
        comp.splitFactor = 1
        comp.files = comp.files[:1]

elif test==3:
    isZSkim=True
    selectedComponents = [ DYJetsToLL_M50_50ns,TTJets_50ns ]

    comp=comp=TTJets_LO
    comp.files = ['/afs/cern.ch/work/d/dalfonso/public/001F4F14-786E-E511-804F-0025905A60FE.root']
    selectedComponents = [comp]

    for comp in selectedComponents:
        if isEle:
            comp.triggers = triggers_ee
        else:
            comp.triggers = triggers_mumu
        comp.splitFactor = 1000
        comp.files = comp.files[:]
#        comp.splitFactor = 1
#        comp.files = comp.files[:1]

elif test==4:
    is1L=False
    selectedComponents = [ WJetsToLNu_50ns ]
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]

elif test==5:
    selectedComponents = QCDPt_50ns
    isDiJet=True
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]
        comp.fineSplitFactor = 5

elif test==6:
    selectedComponents = [ GJets_Pt15to6000_50ns ]
    is1PH=True
    for comp in selectedComponents:
        comp.splitFactor = 100
        comp.files = comp.files[:]

elif test==7:
    selectedComponents = [QCD_Pt30to50_50ns, QCD_Pt50to80_50ns, QCD_Pt80to120_50ns, QCD_Pt120to170_50ns]
    is1PH=True
    for comp in selectedComponents:
        comp.splitFactor = 100
        comp.files = comp.files[:]

    # ------------------------------------------------------------------------------------------- #

### this is for the Zskim
elif test==13:
    isZSkim=True
    if isEle:
        selectedComponents = [ DoubleEG_Run2016B_PromptReco_v2, DoubleEG_Run2016C_PromptReco_v2, DoubleEG_Run2016D_PromptReco_v2 ]
    else:
        selectedComponents = [ DoubleMuon_Run2016B_PromptReco_v2, DoubleMuon_Run2016C_PromptReco_v2, DoubleMuon_Run2016D_PromptReco_v2 ]
    for comp in selectedComponents:
#        comp.splitFactor = 1
#        comp.files = comp.files[5:10]
#        comp.fineSplitFactor = 1
        comp.splitFactor = 1000
        comp.files = comp.files[:]
        if isEle:
            comp.triggers = triggers_ee + triggers_1ele_iso_Zeynep + triggers_ee_noniso_Dominick
        else:
            comp.triggers = triggers_mumu + triggers_1mu_iso_Zeynep + triggers_ee_noniso_Dominick
        comp.json = goldenJson
        comp.intLumi= 0.04003
        print comp

### this is for the Wskim
elif test==14:
    is1L=False
    selectedComponents = [ SingleMuon_Run2016B_PromptReco_v2 ]
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]
        comp.json = goldenJson
        comp.intLumi= 0.04003

### this is for the QCDlike
elif test==15:
    isDiJet=True
    selectedComponents = [ JetHT_Run2016B_PromptReco_v2 ]
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]
        comp.json = goldenJson
        comp.intLumi= 0.04003
#        if isEarlyRun:
#            comp.run_range=(251027,251585) # in 17july runInJSON: 251244,251251,251252,251561,251562
#        else:
#            comp.run_range=(251585,251883) # in promptReco runInJSON: 251643,251721,251883

        print comp

### this is for the PhotonSkim
elif test==16:
    is1PH=True
    selectedComponents = [ SinglePhoton_Run2016B_PromptReco_v2, SinglePhoton_Run2016C_PromptReco_v2, SinglePhoton_Run2016D_PromptReco_v2 ]
    for comp in selectedComponents:
        comp.triggers = triggers_photon30 + triggers_photon50 + triggers_photon75 + triggers_photon90 + triggers_photon120 + triggers_photon165_HE10
        comp.splitFactor = 1000
        comp.files = comp.files[:]
        comp.json = goldenJson
        comp.intLumi= 0.04003
    # ------------------------------------------------------------------------------------------- #
    #        --> 25ns MC here

#QCD
elif test==17:
    selectedComponents = QCDHT + WJetsToLNuHT
    is1PH=True
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]
#        comp.splitFactor = 1
#        comp.files = comp.files[:1]

# GJets
elif test==18:
    selectedComponents = [GJets_HT40to100,GJets_HT100to200, GJets_HT200to400, GJets_HT400to600, GJets_HT600toInf]
    is1PH=True
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]   

# WG/ZG/TTG
elif test==19:
    selectedComponents = [ZGJets, ZNuNuGJets_40130, ZGTo2LG, WGToLNuG, WGJets, TTGJets, TGJets, TGJets_ext]
    is1PH=True
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]   
                                                                                                                                                                                
elif test==23:
    isZSkim=True
    is25ns=True
    selectedComponents = [ DYJetsToLL_M50, TTJets_DiLepton, TTJets_DiLepton_ext, ZZTo4L, ZZTo2L2Q, ZZTo2L2Nu, WWTo2L2Nu, WZTo2L2Q, WZTo3LNu ] + TriBosons + [ TBar_tWch, T_tWch, TToLeptons_tch_powheg, TBarToLeptons_tch_powheg, TToLeptons_sch_amcatnlo + TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromT]
    for comp in selectedComponents:
# no trigger on MC for now
#        if isEle:
#            comp.triggers = triggers_ee
#        else:
#            comp.triggers = triggers_mumu
#        comp.splitFactor = 1
#        comp.files = comp.files[:1]
        comp.splitFactor = 200
        comp.files = comp.files[:]

elif test==25:
    isDiJet=True
    is25ns=True
    selectedComponents = [ TTJets ] + WJetsToLNuHT + ZJetsToNuNuHT + QCDHT
    for comp in selectedComponents:
        comp.splitFactor = 1000
        comp.files = comp.files[:]

    # ------------------------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------- #

from CMGTools.ObjectStudies.analyzers.metCoreModules_cff import *

cfg.Analyzer.nosubdir = True

##------------------------------------------
##  PRODUCER
##------------------------------------------


from CMGTools.ObjectStudies.analyzers.treeProducerMET import *

treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerMET',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     PDFWeights = PDFWeights,
     globalVariables = met_globalVariables,
     globalObjects = met_globalObjects,
     collections = met_collections,
     defaultFloatType = 'F',
     treename = 'METtree'
)

##------------------------------------------
##  SEQUENCE
##------------------------------------------

metSequence = cfg.Sequence(
    metCoreSequence + [treeProducer]
    )

###---- to switch off the comptrssion
#treeProducer.isCompressed = 0

# -------------------- lepton modules below needed for the Muon Selection

if isZSkim:
    ttHLepSkim.ptCuts = [20,10]
    ttHLepSkim.minLeptons = 2
    if isZSkim and isEle:
        ttHLepSkim.ptCuts = [25,15]
        ttHZskim.lepId=[11] ## default is set To Muons
    metSequence.insert(metSequence.index(lepAna)+1,ttHLepSkim)
    metSequence.insert(metSequence.index(lepAna)+2,ttHZskim)
    metSequence.remove(photonAna)

if is1L:
    ttHLepSkim.minLeptons = 1
    metSequence.insert(metSequence.index(lepAna)+1,ttHLepSkim)

if isDiJet:
    vertexAna.keepFailingEvents = True # keep events with no good vertices
    ttHJetMETSkim.jetPtCuts = [100,100]
    metSequence.insert(metSequence.index(photonAna)+2,ttHJetMETSkim)
    metSequence.remove(photonAna)

if isMonoJet:
    ttHJetMETSkim.jetPtCuts = [200]
    metSequence.insert(metSequence.index(photonAna)+2,ttHJetMETSkim)
    metSequence.remove(photonAna)

from CMGTools.ObjectStudies.analyzers.GammaSkimmer import GammaSkimmer
gammaSkim = cfg.Analyzer(
            GammaSkimmer, name='GammaSkimmer',
            )

if is1PH and test==17:
    photonAna.ptMin = 50
    photonAna.etaMax = 1.4
    metSequence.insert(metSequence.index(photonAna)+1,gammaSkim)

# --------------------
# -------------------- FINE TUNE CONTENT
# --------------------

if isZSkim or is1PH:
    met_globalObjects.update({
            "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC up variation"),
            "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC down variation"),
            "met_shifted_UnclusteredEnUp" : NTupleObject("met_shifted_UnclusteredEnUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with met unclustered Up"),
            "met_shifted_UnclusteredEnDown" : NTupleObject("met_shifted_UnclusteredEnDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with met unclustered Down"),
            "metPuppi_jecUp" : NTupleObject("metPuppi_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC up variation (Puppi)"),
            "metPuppi_jecDown" : NTupleObject("metPuppi_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with JEC down variation (Puppi)"),
            "metPuppi_shifted_UnclusteredEnUp" : NTupleObject("metPuppi_shifted_UnclusteredEnUp", metType, help="PF E_{T}^{miss}, after type 1 corrections with met unclustered Up"),
            "metPuppi_shifted_UnclusteredEnDown" : NTupleObject("metPuppi_shifted_UnclusteredEnDown", metType, help="PF E_{T}^{miss}, after type 1 corrections with met unclustered Down"),
            })

if is1PH:
    met_collections.update({
            "selectedPhotons"    : NTupleCollection("gamma", photonType, 50, help="photons with pt>20 and loose cut based ID"),
            })

if is1PH and not test==17:
    met_collections.update({
            "generatorSummary" : NTupleCollection("GenPart", genParticleWithLinksType, 100 , help="Hard scattering particles, with ancestry and links"),
            })

#if isDiJet:
#    met_collections.update({
#            "cleanJetsAll"       : NTupleCollection("jet", jetType, 100, help="all jets (w/ x-cleaning, w/ ID applied w/o PUID applied pt>20 |eta|<5.2) , sorted by pt", filter=lambda l : l.pt()>100  )
#            })

# --------------------

if comp.isData:
    eventFlagsAna.processName = 'RECO'

if comp.isData and comp.json is None:
    metSequence.remove(jsonAna)

# --------------------


if isZSkim or is1PH:

    triggerFlagsAna.triggerBits = {
        'DoubleMu' : triggers_mumu, # [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*" ]
        'DoubleEG' : triggers_ee, # [ "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*" ]
        'SingleMu' : triggers_1mu_iso_Zeynep, # [ 'HLT_IsoTkMu22_v*','HLT_IsoMu22_v*','HLT_IsoMu24_v*','HLT_IsoMu27_v*']
        'SingleEle' : triggers_1ele_iso_Zeynep, # [ 'HLT_Ele27_eta2p1_WPLoose_Gsf_v*','HLT_Ele27_WPTight_Gsf_v*','HLT_Ele35_WPLoose_Gsf_v*']
        'HighPTMuNonIso' : triggers_mumu_noniso_Dominick,
        'HighPTEleNonIso' : triggers_ee_noniso_Dominick,
        'Photon30' : triggers_photon30, #["HLT_Photon30_R9Id90_HE10_IsoM_v*"]
        'Photon50' : triggers_photon50, #["HLT_Photon50_R9Id90_HE10_IsoM_v*"]
        'Photon75' : triggers_photon75, #["HLT_Photon75_R9Id90_HE10_IsoM_v*"]
        'Photon90' : triggers_photon90, #["HLT_Photon90_R9Id90_HE10_IsoM_v*"]
        'Photon120': triggers_photon120, #["HLT_Photon120_R9Id90_HE10_IsoM_v*"]
        'Photon165': triggers_photon165_HE10, #["HLT_Photon165_HE10_v*"]
        }


if isDiJet:
    triggerFlagsAna.triggerBits = {
        'SingleJet': triggers_jet,
        'DiJet'    : triggers_dijet, #["HLT_DiPFJetAve40_v*", "HLT_DiPFJetAve60_v*"]
        'PFHT350_Prescale' : triggers_HT350, #["HLT_PFHT350_v*"] # prescaled
        'PFHT475_Prescale' : triggers_HT475, #["HLT_PFHT475_v*"] # prescaled
        'PFHT600_Prescale' : triggers_HT600, #["HLT_PFHT600_v*"] # prescaled
        'PFHT900' : triggers_HT900, #["HLT_PFHT900_v*"]
        'PFHT800' : triggers_HT800, #["HLT_PFHT800_v*"]
        'MonoJet' : triggers_Jet80MET90, #["["HLT_MonoCentralPFJet80_PFMETNoMu90_NoiseCleaned_PFMHTNoMu90_IDTight_v*","HLT_MonoCentralPFJet80_PFMETNoMu90_JetIdCleaned_PFMHTNoMu90_IDTight_v*","HLT_MonoCentralPFJet80_PFMETNoMu90_PFMHTNoMu90_IDTight_v*"]
        }

if comp.isData:
## to save prescale uncomment these
    triggerFlagsAna.unrollbits = True
    triggerFlagsAna.saveIsUnprescaled = True
    triggerFlagsAna.checkL1prescale = True


# ------------------------------------------------------------------------------------------- #
##------------------------------------------
##  SERVICES
##------------------------------------------

from PhysicsTools.HeppyCore.framework.services.tfile import TFileService 
output_service = cfg.Service(
      TFileService,
      'outputfile',
      name="outputfile",
      fname='METtree.root',
      option='recreate'
    )


# the following is declared in case this cfg is used in input to the heppy.py script                                                                                           
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

# -------------------- Running Download from EOS

from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload
if getHeppyOption("nofetch"):
    event_class = Events 


# -------------------- Running pre-processor

import subprocess
if comp.isData:
    ## DATA 25ns
    removeResiduals = False
    uncFile = os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/jec/Spring16_25nsV6_DATA_Uncertainty_AK4PFchs.txt'
    jecDBFile = os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/jec/Spring16_25nsV6_DATA.db'
    jecEra    = 'Spring16_25nsV6_DATA'
    jerDBFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/PatUtils/data/JER/Spring16_25nsV6_MC.db'
    jerEra    = 'Spring16_25nsV6'
else:
    ## MC 25ns
    removeResiduals = False
    uncFile = os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/jec/Spring16_25nsV6_MC_Uncertainty_AK4PFchs.txt'
    jecDBFile = os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/jec/Spring16_25nsV6_MC.db'
    jecEra    = 'Spring16_25nsV6_MC'
    jerDBFile = os.environ['CMSSW_BASE']+'/src/PhysicsTools/PatUtils/data/JER/Spring16_25nsV6_MC.db'
    jerEra    = 'Spring16_25nsV6'

preprocessorFile = "$CMSSW_BASE/tmp/MetType1_jec_%s.py"%(jecEra)
extraArgs=[]
if comp.isData:
    extraArgs.append('--isData')
    GT= '80X_dataRun2_Prompt_ICHEP16JEC_v0'
else:
    GT= '80X_mcRun2_asymptotic_2016_miniAODv2_v1'

if removeResiduals:extraArgs.append('--removeResiduals')
args = ['python',
  os.path.expandvars(os.environ['CMSSW_BASE']+'/python/CMGTools/ObjectStudies/corMETMiniAOD_cfgCreator.py'),\
  '--GT='+GT,
  '--outputFile='+preprocessorFile,
  '--jecDBFile='+jecDBFile,
  '--jecEra='+jecEra,
  '--jerDBFile='+jerDBFile,
  '--jerEra='+jerEra
  ] + extraArgs
#print "Making pre-processorfile:"
#print " ".join(args)

subprocess.call(args)
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor(preprocessorFile)

###autoAAA(selectedComponents)

#printComps(config.components, True)               
config = cfg.Config( components = selectedComponents,
                     sequence = metSequence,
                     services = [output_service],
                     preprocessor=preprocessor, # comment if pre-processor non needed
#                     events_class = event_class)
                     events_class = Events)

#printComps(config.components, True)
        
