##########################################################
##       CONFIGURATION FOR EXO MONOJET TREES            ##
## skim condition:   MET > 200 GeV                      ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

# Load all analyzers
from CMGTools.MonoXAnalysis.analyzers.dmCore_modules_cff import * 
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.autoAAAconfig import *


#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------

is50ns = getHeppyOption("is50ns",False)
runData = getHeppyOption("runData",False)#True)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
saveSuperClusterVariables = getHeppyOption("saveSuperClusterVariables",True)
saveFatJetIDVariables = getHeppyOption("saveFatJetIDVariables",True)
saveHEEPVariables     = getHeppyOption("saveHEEPVariables",True)
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
doT1METCorr = getHeppyOption("doT1METCorr",True)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("isTest",True)#False)
doLepCorr = getHeppyOption("doLepCorr",False)
doPhotonCorr = getHeppyOption("doPhotonCorr",False)

# Define skims
signalSkim = False
diLepSkim = False
singleLepSkim = False
singleFatJetSkim = False
singlePhotonSkim = False
dibosonSkim = True #False
vGammaSkim =False# True

# --- MONOJET SKIMMING ---
if signalSkim == True:
    monoJetSkim.metCut = 200
    monoJetSkim.jetPtCuts = []

# --- Z->ll control sample SKIMMING ---
if diLepSkim == True:
    monoJetCtrlLepSkim.minLeptons = 2
if singleLepSkim == True:
    monoJetCtrlLepSkim.minLeptons = 1
    # this skim is only used for the SingleElectron CR, so Tight cuts on PT and ID
    monoJetCtrlLepSkim.idCut = '(lepton.muonID("POG_ID_Tight") and lepton.relIso04 < 0.15) if abs(lepton.pdgId())==13 else \
(lepton.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight_full5x5") and (lepton.relIso03<0.0354 if abs(lepton.superCluster().eta())<1.479 else lepton.relIso03<0.0646))'
    #monoJetCtrlLepSkim.idCut = '(lepton.muonID("POG_ID_Loose")) if abs(lepton.pdgId())==13 else (lepton.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"))'
    #monoJetCtrlLepSkim.idCut='(lepton.muonID("POG_SPRING15_25ns_v1_Veto")) if abs(lepton.pdgId())==13 else (lepton.electronID("POG_SPRING15_25ns_v1_Veto"))'
    monoJetCtrlLepSkim.ptCuts = [40]
if singlePhotonSkim == True:
    gammaJetCtrlSkim.minPhotons = 1
    gammaJetCtrlSkim.minJets = 1

# --- V-Tagging SKIMMING ---
if singleFatJetSkim == True:
    print "Vetoing on less than 1 jet"
    monoJetCtrlFatJetSkim.minFatJets = 1

if dibosonSkim == True:
    monoJetCtrlFatJetSkim.minFatJets = 1
    monoJetCtrlLepSkim.minLeptons = 1
    monoJetCtrlLepSkim.idCut = '(lepton.muonID("POG_ID_Loose")) if abs(lepton.pdgId())==13 else (lepton.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"))'
    monoJetCtrlLepSkim.ptCuts = [40]
    monoXFatJetAna.jetPt = 120
    lepAna.inclusive_muon_pt = 30
    lepAna.loose_muon_pt     = 30
    lepAna.inclusive_electron_pt = 30
    lepAna.loose_electron_pt     = 30

#if vGammaSkim == True:
   ######################## #monoXFatJetAna.jetPt = 120
   ######################## #monoJetCtrlFatJetSkim.minFatJets = 1
   ######################## #gammaJetCtrlSkim.minPhotons = 1
   ######################## #gammaJetCtrlSkim.minJets = 1
   ######################## #photonAna.ptMin = 50
    
# --- Photon OR Electron SKIMMING ---
#if photonOrEleSkim == True:
    

# run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
## will become miniIso perhaps?
#lepAna.loose_muon_isoCut     = lambda muon : muon.relIso03 < 10.5
#lepAna.loose_electron_isoCut = lambda electron : electron.relIso03 < 10.5
    

# switch off slow photon MC matching
photonAna.do_mc_match = False


##------------------------------------------
##  TOPOLOGICAL VARIABLES: RAZOR
##------------------------------------------
from PhysicsTools.Heppy.analyzers.eventtopology.RazorAnalyzer import RazorAnalyzer
monoXRazorAna = cfg.Analyzer(
    RazorAnalyzer, name = 'RazorAnalyzer',
    doOnlyDefault = False
    )

##------------------------------------------
##  TOLOLOGIAL VARIABLES: MT2
##------------------------------------------
from CMGTools.TTHAnalysis.analyzers.ttHTopoVarAnalyzer import ttHTopoVarAnalyzer
ttHTopoJetAna = cfg.Analyzer(
    ttHTopoVarAnalyzer, name = 'ttHTopoVarAnalyzer',
    doOnlyDefault = True
    )

from PhysicsTools.Heppy.analyzers.eventtopology.MT2Analyzer import MT2Analyzer
monoXMT2Ana = cfg.Analyzer(
    MT2Analyzer, name = 'MT2Analyzer',
    metCollection     = "slimmedMETs",
    doOnlyDefault = False,
    jetPt = 40.,
    collectionPostFix = "",
    )

##-----------------------------------------------
##  TOLOLOGIAL VARIABLES: MONOJET SPECIFIC ONES
##-----------------------------------------------
from CMGTools.MonoXAnalysis.analyzers.monoJetVarAnalyzer import monoJetVarAnalyzer
monoJetVarAna = cfg.Analyzer(
    monoJetVarAnalyzer, name = 'monoJetVarAnalyzer',
    )

##------------------------------------------
# Event Analyzer for monojet 
##------------------------------------------
from CMGTools.MonoXAnalysis.analyzers.monoJetEventAnalyzer import monoJetEventAnalyzer
MonoJetEventAna = cfg.Analyzer(
    monoJetEventAnalyzer, name="monoJetEventAnalyzer",
    minJets25 = 0,
    )


from CMGTools.MonoXAnalysis.analyzers.treeProducerDarkMatterDiboson import * 

# for applying fatjet ID
if saveFatJetIDVariables:
    fatJetType.addVariables([
            NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
            NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
            NTupleVariable("chEmEF", lambda x : x.chargedEmEnergyFraction(), float, mcOnly = False,help="chargedEmEnergyFraction (relative to uncorrected jet energy)"),
            NTupleVariable("neEmEF", lambda x : x.neutralEmEnergyFraction(), float, mcOnly = False,help="neutralEmEnergyFraction (relative to uncorrected jet energy)"),
            NTupleVariable("chMult", lambda x : x.chargedMultiplicity(), float, mcOnly = False,help="charged multiplicity (relative to uncorrected jet energy)"),
            NTupleVariable("neMult", lambda x : x.neutralMultiplicity(), float, mcOnly = False,help="neutral multiplicity (relative to uncorrected jet energy)"),
            NTupleVariable("puppiPt", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:pt"), float, mcOnly=False, help="puppi pt for the AK08"),
            NTupleVariable("puppiEta", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:eta"), float, mcOnly=False, help="puppi eta for the AK08"),
            NTupleVariable("puppiPhi", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:phi"), float, mcOnly=False, help="puppi phi for the AK08"),
            NTupleVariable("puppiMass", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:mass"), float, mcOnly=False, help="puppi mass for the AK08"),
            NTupleVariable("puppiTau1", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau1"), float, mcOnly=False, help="puppi tau1 for the AK08"),
            NTupleVariable("puppiTau2", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau2"), float, mcOnly=False, help="puppi tau2 for the AK08"),
            NTupleVariable("puppiTau3", lambda x : x.userFloat("ak8PFJetsPuppiValueMap:NjettinessAK8PuppiTau3"), float, mcOnly=False, help="puppi tau3 for the AK08"),

])

if saveHEEPVariables:
    leptonTypeMonoJet.addVariables([
            NTupleVariable("e2x5Max",    lambda x : x.e2x5Max() if abs(x.pdgId())==11 else -999., help="e2x5Max for electrons"),
            NTupleVariable("e1x5",    lambda x : x.e1x5() if abs(x.pdgId())==11 else -999., help="e1x5 for electrons"),
            NTupleVariable("isolTrkPt",    lambda x : x.dr03TkSumPt() if abs(x.pdgId())==11 else -999., help="isolTrkPt for electrons"),
            NTupleVariable("isolEmHadDepth1",    lambda x : x.dr03EcalRecHitSumEt() + x.dr03HcalDepth1TowerSumEt() if abs(x.pdgId())==11 else -999., help="isolEmHadDepth1 for lectrons"),
            NTupleVariable("eleClusterDEta", lambda x : x.deltaEtaSeedClusterTrackAtVtx() if abs(x.pdgId())==11 else -999., help="Electron Supercluster DEta"),
            NTupleVariable("isEcalDriven", lambda x : x.ecalDrivenSeed() if abs(x.pdgId()) == 11 else -999, int, help="is Ecal Driven to cut on ID"), #added
            NTupleVariable("muonDB", lambda x : x.dB() if abs(x.pdgId()) == 13 else -999, help="muon DB"),
            NTupleVariable("pixelHits", lambda x : x.innerTrack().hitPattern().numberOfValidPixelHits() if abs(x.pdgId()) == 13 and x.innerTrack().isNonnull() else -999, help="Number of pi            xel hits (-1 for electrons)"),
            NTupleVariable("muTrackIso", lambda x: x.trackIso() if abs(x.pdgId()) == 13 else -999, help="muon track isolation"),
            NTupleVariable("muon_dz", lambda x : x.muonBestTrack().dz() if abs(x.pdgId()) == 13 else -999, help="dz for muons"),
            NTupleVariable("nChamberHits", lambda x: x.globalTrack().hitPattern().numberOfValidMuonHits() if abs(x.pdgId()) == 13 and x.globalTrack().isNonnull() else -999, help="Number of muon chamber hits (-1 for electrons)"),
            NTupleVariable("muonPtRatio", lambda x : x.muonBestTrack().ptError()/x.muonBestTrack().pt() if abs(x.pdgId()) == 13 else -999, help="Ratio between ptError and pt"),
])

## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerDarkMatterDiboson',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     doPDFVars = True,
     globalVariables = dmDiboson_globalVariables,
     globalObjects = dmDiboson_globalObjects,
     collections = dmDiboson_collections,
)

##Puppi producers
# Ak04 Puppi Jets Analyzer (generic)
from CMGTools.MonoXAnalysis.analyzers.monoXPuppiJetAnalyzer import monoXPuppiJetAnalyzer
monoXPuppiJetAna = cfg.Analyzer(
    monoXPuppiJetAnalyzer, name = 'monoXPuppiJetAnalyzer',
    jetCol = 'slimmedJetsPuppi',
    jetPt = 100.,
    jetEta = 2.4,
    jetLepDR = 0.4,
    # v--- not implemented for AK8
    #jetLepDR = 0.4,
    #minLepPt = 10,
    relaxJetId = False,
    # v--- not implemented for AK8
    #doPuId = False, # Not commissioned in 7.0.X
    recalibrateJets = True,
    applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
    recalibrationType = "AK4PFPuppi",
    mcGT     = "Spring16_25nsV3_MC",
    dataGT   = "Spring16_25nsV3_DATA", # update with the new one when available in 8.0.X
    jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
    shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
    addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
    rho = ('fixedGridRhoFastjetAll','',''),
    )

## Puppi subJets Analyzer (generic)
from CMGTools.MonoXAnalysis.analyzers.monoXSubJetsPuppiAnalyzer import monoXSubJetsPuppiAnalyzer
monoXSubJetPuppiAna = cfg.Analyzer(
        monoXSubJetsPuppiAnalyzer, name = 'monoXSubJetsPuppiAnalyzer',
        jetCol = 'slimmedJetsAK8PFPuppiSoftDropPacked',
        jetPt = 100.,
        jetEta = 2.4,
        jetLepDR = 0.4,
        # v--- not implemented for AK8
        #jetLepDR = 0.4,
        #minLepPt = 10,
        relaxJetId = False,
        # v--- not implemented for AK8
        #doPuId = False, # Not commissioned in 7.0.X
        recalibrateJets = True,
        applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
        recalibrationType = "AK8PFchs", #unused->no recalibration extracted YET!
        mcGT     = "Spring16_25nsV3_MC",
        dataGT   = "Spring16_25nsV3_DATA", # update with the new one when available in 8.0.X
        jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
        shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
        addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
        rho = ('fixedGridRhoFastjetAll','',''),
        )

## Puppi-SoftDrop subJets Analyzer (generic)
from CMGTools.MonoXAnalysis.analyzers.monoXSubJetsSoftDropAnalyzer import monoXSubJetsSoftDropAnalyzer
monoXSubJetSoftDropAna = cfg.Analyzer(
        monoXSubJetsSoftDropAnalyzer, name = 'monoXSubJetsSoftDropAnalyzer',
        jetCol = 'slimmedJetsAK8PFCHSSoftDropPacked',
        jetPt = 100.,
        jetEta = 2.4,
        jetLepDR = 0.4,
        # v--- not implemented for AK8
        #jetLepDR = 0.4,
        #minLepPt = 10,
        relaxJetId = False,
        # v--- not implemented for AK8
        #doPuId = False, # Not commissioned in 7.0.X
        recalibrateJets = True,
        applyL2L3Residual = True, # Switch to 'Data' when they will become available for Data
        recalibrationType = "AK8PFchs", #unused->no recalibration extracted YET!
        mcGT     = "Spring16_25nsV3_MC",
        dataGT   = "Spring16_25nsV3_DATA", # update with the new one when available in 8.0.X
        jecPath = "%s/src/CMGTools/RootTools/data/jec/" % os.environ['CMSSW_BASE'],
        shiftJEC = 0, # set to +1 or -1 to get +/-1 sigma shifts
        addJECShifts = False, # if true, add  "corr", "corrJECUp", and "corrJECDown" for each jet (requires uncertainties to be available!)
        rho = ('fixedGridRhoFastjetAll','',''),
        )

### adding MET Puppi Analyzer
metPuppiAna = cfg.Analyzer(
        METAnalyzer, name="metAnalyzerPuppi",
        metCollection     = "slimmedMETsPuppi",
        noPUMetCollection = "slimmedMETsPuppi",
        copyMETsByValue = False,
        doTkMet = False,
        includeTkMetCHS = False,
        includeTkMetPVLoose = False,
        includeTkMetPVTight = False,
        doMetNoPU = False,
        doMetNoMu = False,
        doMetNoEle = False,
        doMetNoPhoton = False,
        recalibrate = False,#"type1", changed as it doesn't work... "type1", # or "type1", or True
        applyJetSmearing = False, # does nothing unless the jet smearing is turned on in the jet analyzer
        old74XMiniAODs = False, # set to True to get the correct Raw MET when running on old 74X MiniAODs
        jetAnalyzerPostFix = "Puppi",# changed as it doesn't work...,
        candidates='packedPFCandidates',
        candidatesTypes='std::vector<pat::PackedCandidate>',
        dzMax = 0.1,
        collectionPostFix = "Puppi",
        )

#### metPuppiAnaScaleUp = metPuppiAna.clone(name="metAnalyzerPuppiScaleUp",
####         copyMETsByValue = True,
####         recalibrate = "type1",
####         jetAnalyzerPostFix = "Puppi_jecUp",
####         collectionPostFix = "Puppi_jecUp",
####         )
#### 
#### metPuppiAnaScaleDown = metPuppiAna.clone(name="metAnalyzerPuppiScaleDown",
####         copyMETsByValue = True,
####         recalibrate = "type1",
####         jetAnalyzerPostFix = "Puppi_jecDown",
####         collectionPostFix = "Puppi_jecDown",
####         )

## histo counter
# dmCoreSequence.insert(dmCoreSequence.index(skimAnalyzer),
#                       dmCounter)

# HBHE new filter
from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheAna = cfg.Analyzer(
    hbheAnalyzer, name="hbheAnalyzer", IgnoreTS4TS5ifJetInLowBVRegion=False
    )
dmCoreSequence.insert(dmCoreSequence.index(ttHCoreEventAna),hbheAna)
treeProducer.globalVariables.append(NTupleVariable("hbheFilterNew50ns", lambda ev: ev.hbheFilterNew50ns, int, help="new HBHE filter for 50 ns"))
treeProducer.globalVariables.append(NTupleVariable("hbheFilterNew25ns", lambda ev: ev.hbheFilterNew25ns, int, help="new HBHE filter for 25 ns"))
treeProducer.globalVariables.append(NTupleVariable("hbheFilterIso", lambda ev: ev.hbheFilterIso, int, help="HBHE iso-based noise filter"))

#additional MET quantities
metAna.doTkMet = True
treeProducer.globalVariables.append(NTupleVariable("met_trkPt", lambda ev : ev.tkMet.pt() if  hasattr(ev,'tkMet') else  0, help="tkmet p_{T}"))
treeProducer.globalVariables.append(NTupleVariable("met_trkPhi", lambda ev : ev.tkMet.phi() if  hasattr(ev,'tkMet') else  0, help="tkmet phi"))
if doT1METCorr:
    jetAna.calculateType1METCorrection = True
    metAna.recalibrate = "type1"
    metAna.old74XMiniAODs = False

# lepton scale / resolution corrections
if doLepCorr: 
    doECalElectronCorrections(era="25ns")
    doKalmanMuonCorrections()
if doPhotonCorr:
    doECalPhotonCorrections()

#-------- SEQUENCE
sequence = cfg.Sequence(dmCoreSequence+[
#   monoXRazorAna,
#   monoXMT2Ana,
   monoXPuppiJetAna,
   monoXSubJetPuppiAna,
   monoXSubJetSoftDropAna,
   metPuppiAna,
###    metPuppiAnaScaleUp
###    metPuppiAnaScaleDown,
   monoJetVarAna,
   MonoJetEventAna,
   treeProducer,
    ])

from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
from CMGTools.RootTools.samples.triggers_8TeV import triggers_1mu_8TeV, triggers_mumu_8TeV, triggers_mue_8TeV, triggers_ee_8TeV;
triggers_AllMonojet = triggers_metNoMu90_mhtNoMu90 + triggers_metNoMu120_mhtNoMu120 + triggers_AllMET170 + triggers_AllMET300
triggers_SinglePhoton = triggers_photon155 + triggers_photon165_HE10 + triggers_photon175 + triggers_jet  # last ones added to recover L1 issue of tight H/E cut
trigger_JetHT = triggers_HT800 #remember to do the NOT of (Photon165 || Photon175)
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleEl' : triggers_ee,
    'SingleMu' : triggers_1mu_iso,
    'SingleEl' : triggers_1e,
    'MonoJetMetNoMuMHT90' : triggers_metNoMu90_mhtNoMu90,
    'MonoJetMetNoMuMHT120' : triggers_metNoMu120_mhtNoMu120,
    'Met170'   : triggers_AllMET170,
    'Met300'   : triggers_AllMET300,
    'SinglePho' : triggers_SinglePhoton,
    'Jet_HT'   : trigger_JetHT
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = False
triggerFlagsAna.checkL1Prescale = False

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv1 import *
from CMGTools.MonoXAnalysis.samples.samples_monojet_13TeV_80X import *
#from CMGTools.MonoXAnalysis.samples.samples_monojet_13TeV_76X import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *

selectedComponents = [];

if scaleProdToLumi>0: # select only a subset of a sample, corresponding to a given luminosity (assuming ~30k events per MiniAOD file, which is ok for central production)
    target_lumi = scaleProdToLumi # in inverse picobarns
    for c in selectedComponents:
        if not c.isMC: continue
        nfiles = int(min(ceil(target_lumi * c.xSection / 30e3), len(c.files)))
        #if nfiles < 50: nfiles = min(4*nfiles, len(c.files))
        print "For component %s, will want %d/%d files; AAA %s" % (c.name, nfiles, len(c.files), "eoscms" not in c.files[0])
        c.files = c.files[:nfiles]
        c.splitFactor = len(c.files)
        c.fineSplitFactor = 1

#json = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON.txt"
json = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-278290_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt"
if False:
    is50ns = False
    selectedComponents = PrivateSamplesData
    for comp in selectedComponents:
        comp.splitFactor = 100     
        comp.fineSplitFactor = 1

if runData and not isTest: # For running on data
    ##run_ranges = [ (272021,275125) ]; useAAA=False; is50ns=False
    run_ranges = [ (272021, 278808) ]; useAAA=False; is50ns=False
    #print "Removing the SoftDrop and Puppi subjet collections (not yet in data)"
    #dmCoreSequence.remove(monoXSubJetPuppiAna)
    #dmCoreSequence.remove(monoXSubJetSoftDropAna)

    compSelection = ""
    DatasetsAndTriggers = []
    selectedComponents = []; vetos = []
    ProcessingsAndRunRanges = []; Shorts = []

    
    ProcessingsAndRunRanges.append( ("Run2016B-PromptReco-v1", [272021,272759] ) ); Shorts.append("PromptReco_v1")
    ProcessingsAndRunRanges.append( ("Run2016B-01Jul2016-v2",  [272760,273017] ) ); Shorts.append("01Jul2016-v2")
    ProcessingsAndRunRanges.append( ("Run2016B-PromptReco-v2", [273150,275376] ) ); Shorts.append("PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016C-PromptReco-v2", [275420,276283] ) ); Shorts.append("PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016D-PromptReco-v2", [276315,276811] ) ); Shorts.append("PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016E-PromptReco-v2", [276827,277420] ) ); Shorts.append("PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016F-PromptReco-v1", [277776,278808] ) ); Shorts.append("PromptReco_v1")
    ##ProcessingsAndRunRanges.append( ("Run2016G-PromptReco-v1", [278815,278820] ) ); Shorts.append("PromptReco_v1")

    if diLepSkim == True:
        DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso + triggers_mumu_ss + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt + triggers_AllMonojet) )
        DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_ee_ht + triggers_3e) )
    if singleLepSkim == True or dibosonSkim == True:
        DatasetsAndTriggers.append( ("SingleElectron", triggers_ee + triggers_ee_ht + triggers_3e + triggers_1e + triggers_1e_50ns) )
        DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_mumu_iso + triggers_mumu_ss + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt) )
        #DatasetsAndTriggers.append( ("SinglePhoton",   triggers_SinglePhoton) )
    if vGammaSkim == True:
        DatasetsAndTriggers.append( ("SinglePhoton", triggers_SinglePhoton) )
        DatasetsAndTriggers.append( ("JetHT", trigger_JetHT + triggers_photon165_HE10 + triggers_photon175))
    if singlePhotonSkim == True:
        DatasetsAndTriggers.append( ("SinglePhoton", triggers_SinglePhoton) )
    if signalSkim == True:
        DatasetsAndTriggers.append( ("MET", triggers_AllMonojet ) )
   # else:
   #     DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_ee_ht + triggers_3e) )

    for pd,triggers in DatasetsAndTriggers:
        iproc=0 
        for processing,run_dslimits in ProcessingsAndRunRanges:
            # if ("DoubleEG" in pd): processing.replace("v1","v2",1) 
            for run_range in run_ranges:
                run_min = max(run_range[0],run_dslimits[0])
                run_max = min(run_range[1],run_dslimits[1])
                this_run_range = (run_min,run_max)
                label = "runs_%d_%d" % this_run_range if this_run_range[0] != this_run_range[1] else "run_%d" % (this_run_range[0],)
                compname = pd+"_"+Shorts[iproc]+"_"+label
                if ((compSelection and not re.search(compSelection, compname))):
                    print "Will skip %s" % (compname)

                    continue
                print "Building component ",compname," with run range ",label, "\n"
                comp = kreator.makeDataComponent(compname, 
                                                 "/"+pd+"/"+processing+"/MINIAOD", 
                                                 "CMS", ".*root", 
                                                 json=json, 
                                                 run_range=this_run_range, 
                                                 #triggers=triggers[:], vetoTriggers = vetos[:],
                                                 useAAA=useAAA)
                print "Will process %s (%d files)" % (comp.name, len(comp.files))
                print "\ttrigger sel %s, veto %s" % (triggers, vetos)
                comp.splitFactor = len(comp.files)/10#4
                comp.fineSplitFactor = 1
                selectedComponents.append( comp )
            iproc += 1
        if singleLepSkim and "SinglePhoton" in pd: 
            vetos += triggers
    if json is None:
        dmCoreSequence.remove(jsonAna)

if is50ns:
    jetAna.mcGT     = "Summer15_50nsV5_MC"
    jetAna.dataGT   = "Summer15_50nsV5_DATA"
    pfChargedCHSjetAna.mcGT     = "Summer15_50nsV5_MC"
    pfChargedCHSjetAna.dataGT   = "Summer15_50nsV5_DATA"
else: 
    jetAna.mcGT   = "Spring16_25nsV6_MC"
    jetAna.dataGT = "Spring16_25nsV6_DATA"
    monoXFatJetAna.mcGT = "Spring16_25nsV6_MC"
    monoXFatJetAna.dataGT = "Spring16_25nsV6_DATA"
    monoXPuppiJetAna.mcGT = "Spring16_25nsV6_MC"
    monoXPuppiJetAna.dataGT = "Spring16_25nsV6_DATA"
    monoXSubJetPuppiAna.mcGT = "Spring16_25nsV6_MC"
    monoXSubJetPuppiAna.dataGT = "Spring16_25nsV6_DATA"
    monoXSubJetSoftDropAna.mcGT = "Spring16_25nsV6_MC"
    monoXSubJetSoftDropAna.dataGT = "Spring16_25nsV6_DATA"

if removeJetReCalibration:
    ## NOTE: jets will still be recalibrated, since calculateSeparateCorrections is True,
    ##       however the code will check that the output 4-vector is unchanged.
    jetAna.recalibrateJets = False

if forcedSplitFactor>0 or forcedFineSplitFactor>0:
    if forcedFineSplitFactor>0 and forcedSplitFactor!=1: raise RuntimeError, 'splitFactor must be 1 if setting fineSplitFactor'
    for c in selectedComponents:
        if forcedSplitFactor>0: c.splitFactor = forcedSplitFactor
        if forcedFineSplitFactor>0: c.fineSplitFactor = forcedFineSplitFactor

if runData==False and not isTest: # MC all
    ### 25 ns 74X MC samples
    is50ns = False
    mcSamples = mcSamples_diboson#zgamma#monojet_Asymptotic25ns
    #if signalSkim:
        # full signal scan (many datasets!)
        # mcSamples += mcSamples_monojet_Asymptotic25ns_signals
        # monojet_signals_cherrypick = [ DMS_Mphi_2000_Mchi_1_gSM_1p0_gDM_1p0, DMPS_Mphi_2000_Mchi_1_gSM_1p0_gDM_1p0, DMAV_Mphi_2000_Mchi_1_gSM_0p25_gDM_1p0]
        # mcSamples += monojet_signals_cherrypick
    selectedComponents = mcSamples 
    for comp in selectedComponents:
        comp.splitFactor = len(comp.files)/10#4
        comp.fineSplitFactor = 1

####if runData==False and isTest: # Synch MC sample
####    is50ns = False
####    comp = kreator.makeMCComponent("TTbarDM","/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.0)
####    selectedComponents = [ comp ]
####    for comp in selectedComponents:
####        comp.splitFactor = len(comp.files)
####        comp.fineSplitFactor = 1
####

from CMGTools.HToZZ4L.tools.configTools import printSummary

if not getHeppyOption("test"):
    printSummary(selectedComponents)
    autoAAA(selectedComponents)


#-------- HOW TO RUN ----------- 
test = getHeppyOption('test')
if test == 'DYJets':
    monoJetSkim.metCut = 0
    monoJetCtrlLepSkim.minLeptons = 2
    comp = DYJetsToLL_M50_HT100to200
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
elif test == 'EOS':
    comp = DYJetsToLL_M50
    comp.files = comp.files[:1]
    if getHeppyOption('Wigner'):
        print "Will read from WIGNER"
        comp.files = [ 'root://eoscms//eos/cms/store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/0432E62A-7A6C-E411-87BB-002590DB92A8.root' ]
    else:
        print "Will read from CERN Meyrin"
        comp.files = [ 'root://eoscms//eos/cms/store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/10000/F675C068-5E6C-E411-B915-0025907DC9AC.root' ]
    os.system("/afs/cern.ch/project/eos/installation/0.3.15/bin/eos.select fileinfo "+comp.files[0].replace("root://eoscms//","/"))
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
elif test == 'SingleMu':
    comp = SingleMu
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    selectedComponents = [ comp ]
elif test == '5':
    for comp in selectedComponents:
        comp.files = comp.files[:5]
        comp.splitFactor = 1
        comp.fineSplitFactor = 5
elif test == 'synch-80X': # sync
    #eventSelector.toSelect = [ (1,165,84628), ]
    #sequence = cfg.Sequence([eventSelector] + dmCoreSequence + [ ttHFatJetAna, monoJetVarAna, MonoJetEventAna, treeProducer, ])
    monoJetSkim.metCut = 0  
    what = getHeppyOption("sample")
    if what == "TTbarDM":
        comp = kreator.makeMCComponent("TTbarDM","/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.0)
        selectedComponents = [ comp ]
    elif what == "DYJets":
        comp = DYJetsToLL_M50
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIISpring16MiniAODv1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/60000/E0553CDE-0300-E611-B2C4-0CC47A4C8F1C.root' ]
        selectedComponents = [ comp ]
    elif what == "TTJets":
        comp = TTJets
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIISpring16MiniAODv1/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_v3-v2/70000/C81219FD-150C-E611-BF27-002590A88736.root' ]
        selectedComponents = [ comp ]
    elif what == "WJets":
        comp = WJetsToLNu_HT100to200
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIISpring16MiniAODv1/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/60000/00DD003D-4201-E611-A6F7-0CC47A745282.root' ]
        selectedComponents = [ comp ]
    else:
        selectedComponents = mcSamples_diboson#zgamma#monojet_Asymptotic25ns
    jetAna.smearJets       = False
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1 if getHeppyOption("single") else 2
elif test == '80X-Data':
    what = getHeppyOption("sample")
    if what == "DoubleEG":
        comp = kreator.makeDataComponent('DoubleEG_Run2016B', '/DoubleEG/Run2016B-PromptReco-v2/MINIAOD', "CMS", ".*root", json, (272021,273523) )
        comp.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleEG/MINIAOD/PromptReco-v2/000/273/448/00000/28E31C7B-1C1C-E611-988C-02163E011BAC.root' ]
        selectedComponents = [ comp ]
    elif what == "DoubleMuon":
        comp = kreator.makeDataComponent('DoubleMuon_Run2016B', '/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD', "CMS", ".*root", json, (272021,273523) )
        comp.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleMuon/MINIAOD/PromptReco-v2/000/273/448/00000/7ED72389-581C-E611-BF09-02163E011BF0.root' ]
        selectedComponents = [ comp ]
    else:
        selectedComponents = dataSamples_Run2015D_16Dec
    for comp in selectedComponents:
        comp.json = json
        comp.splitFactor = 7
        comp.fineSplitFactor = 1 if getHeppyOption("single") else 8
        if not getHeppyOption("all"):
            comp.files = comp.files[:1]
    dmCoreSequence.remove(jsonAna)
elif test == 'simone':
    ##dmCoreSequence.remove(monoXSubJetPuppiAna)
    ##dmCoreSequence.remove(monoXSubJetSoftDropAna)
    from PhysicsTools.Heppy.utils.miniAodFiles import miniAodFiles
    sample = cfg.MCComponent(
           files = [
           #"root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleElectron/RAW/v2/000/273/150/00000/A8A803BC-CC17-E611-BA8C-02163E014550.root",
          # "root://eoscms//eos/cms/store/data/Run2016B/DoubleMuon/MINIAOD/PromptReco-v2/000/273/448/00000/7ED72389-581C-E611-BF09-02163E011BF0.root"
           #"root://cms-xrd-global.cern.ch//store/data/Run2016B/SingleElectron/MINIAOD/PromptReco-v2/000/273/158/00000/06277EC1-181A-E611-870F-02163E0145E5.root"
           #"root://xrootd.unl.edu//store/mc/RunIISpring16DR80/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext3-v1/60000/08078977-2F1F-E611-AF79-001E675053A5.root"
           #"root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v1/00000/00A10CC4-4227-E611-BBF1-C4346BBCD528.root"
           #"root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv1/TT_TuneCUETP8M1_13TeV-powheg-pythia8-evtgen/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/00000/4603CC0B-D012-E611-972B-90B11C06E1A0.root"
           #"root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/00000/04FB4BAA-3A33-E611-BC64-008CFA197A90.root",
           #"root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/00000/9C6425C8-081C-E611-9F71-001E67E71A56.root",
           #"file:A8A803BC-CC17-E611-BA8C-02163E014550.root",
           "root://cms-xrd-global.cern.ch//store/mc/RunIISpring16MiniAODv2/GluGluSpin0ToZGamma_ZToQQ_W_0-p-014_M_1000_TuneCUEP8M1_13TeV_pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/10000/3E743410-C82B-E611-8948-0025907FD40C.root",
           #"root://cms-xrd-global.cern.ch//store/data/Run2016B/SinglePhoton/MINIAOD/PromptReco-v2/000/273/158/00000/00DD3222-261A-E611-9FD2-02163E011E34.root",
                 ],
           name="ZHLL125", isEmbed=False,
           puFileMC="puMC.root",
           puFileData="puData.root",
           splitFactor = 5
    )
    
    sample.isMC=True#False
    selectedComponents = [sample]
elif test== 'simoneComponent':
    comp = kreator.makeMCComponent("ZGamma_Signal_1000TeV","/GluGluSpin0ToZGamma_ZToQQ_W_0-p-014_M_1000_TuneCUEP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 1.)
    selectedComponents = [ comp ]

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerDarkMatterDiboson/tree.root',
    option='recreate'
    )    
outputService.append(output_service)

# the following is declared in case this cfg is used in input to the heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
from CMGTools.TTHAnalysis.tools.EOSEventsWithDownload import EOSEventsWithDownload
event_class = EOSEventsWithDownload
EOSEventsWithDownload.aggressive = 2 # always fetch if running on Wigner
if getHeppyOption("nofetch")  or getHeppyOption("isCrab"):
    event_class = Events
config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = outputService,  
                     events_class = event_class)


