##########################################################
##       CONFIGURATION FOR SUSY MULTILEPTON TREES       ##
## skim condition: >= 2 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re


#-------- LOAD ALL ANALYZERS -----------

from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------

is50ns = getHeppyOption("is50ns",False)
runData = getHeppyOption("runData",False)
runDataQCD = getHeppyOption("runDataQCD",False)
runSMS = getHeppyOption("runSMS",False)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
SOS = getHeppyOption("SOS",False) ## switch True to overwrite settings for SOS skim (N.B. default settings are those from multilepton preselection)
saveSuperClusterVariables = getHeppyOption("saveSuperClusterVariables",False)
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
removeJecUncertainty = getHeppyOption("removeJecUncertainty",False)
doMETpreprocessor = getHeppyOption("doMETpreprocessor",False)
skipT1METCorr = getHeppyOption("skipT1METCorr",False)
#doAK4PFCHSchargedJets = getHeppyOption("doAK4PFCHSchargedJets",False)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))

# Lepton Skimming
ttHLepSkim.minLeptons = 2
ttHLepSkim.maxLeptons = 999
#ttHLepSkim.idCut  = ""
#ttHLepSkim.ptCuts = [10, 10]

#runData = False

# Run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
lepAna.doIsolationScan = False

# Lepton Preselection
lepAna.loose_electron_id = "POG_MVA_ID_Spring15_NonTrig_VLooseIdEmu"
isolation = "miniIso"

jetAna.mcGT   = 'Spring16_25nsV3_MC'
jetAna.dataGT = 'Spring16_25nsV3_DATA'
jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this
if not removeJecUncertainty:
    jetAna.addJECShifts = True
    jetAnaScaleDown.copyJetsByValue = True # do not remove this
    metAnaScaleDown.copyMETsByValue = True # do not remove this
    jetAnaScaleUp.copyJetsByValue = True # do not remove this
    metAnaScaleUp.copyMETsByValue = True # do not remove this
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleDown)
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleUp)
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleDown)
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleUp)


# Switch on slow QGL
jetAna.doQG = False
jetAnaScaleUp.doQG = False
jetAnaScaleDown.doQG = False

# Switch off slow photon MC matching
photonAna.do_mc_match = False

# Loose Tau configuration
tauAna.loose_decayModeID = "decayModeFinding"
tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 2.3
# Current ra7 config (but not ttH)
#tauAna.loose_vetoLeptonsPOG = True
#tauAna.loose_tauAntiMuonID = "againstMuonTight"
#tauAna.loose_tauAntiElectronID = "againstElectronLoose"
if True: #if cleaning jet-loose tau cleaning
    jetAna.cleanJetsFromTaus = True
    jetAnaScaleUp.cleanJetsFromTaus = True
    jetAnaScaleDown.cleanJetsFromTaus = True


#-------- ADDITIONAL ANALYZERS -----------

## Event Analyzer for susy multi-lepton (at the moment, it's the TTH one)
from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
    ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
    minJets25 = 0,
    )

## JetTau analyzer, to be called (for the moment) once bjetsMedium are produced
from CMGTools.TTHAnalysis.analyzers.ttHJetTauAnalyzer import ttHJetTauAnalyzer
ttHJetTauAna = cfg.Analyzer(
    ttHJetTauAnalyzer, name="ttHJetTauAnalyzer",
    )

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHSVAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                        ttHHeavyFlavourHadronAna)

## Insert declustering analyzer
from CMGTools.TTHAnalysis.analyzers.ttHDeclusterJetsAnalyzer import ttHDeclusterJetsAnalyzer
ttHDecluster = cfg.Analyzer(
    ttHDeclusterJetsAnalyzer, name='ttHDecluster',
    lepCut     = lambda lep,ptrel : lep.pt() > 10,
    maxSubjets = 6, # for exclusive reclustering
    ptMinSubjets = 5, # for inclusive reclustering
    drMin      = 0.2, # minimal deltaR(l,subjet) required for a successful subjet match
    ptRatioMax = 1.5, # maximum pt(l)/pt(subjet) required for a successful match
    ptRatioDiff = 0.1,  # cut on abs( pt(l)/pt(subjet) - 1 ) sufficient to call a match successful
    drMatch     = 0.02, # deltaR(l,subjet) sufficient to call a match successful
    ptRelMin    = 5,    # maximum ptRelV1(l,subjet) sufficient to call a match successful
    prune       = True, # also do pruning of the jets 
    pruneZCut       = 0.1, # pruning parameters (usual value in CMS: 0.1)
    pruneRCutFactor = 0.5, # pruning parameters (usual value in CMS: 0.5)
    verbose     = 0,   # print out the first N leptons
    jetCut = lambda jet : jet.pt() > 20,
    mcPartonPtCut = 20,
    mcLeptonPtCut =  5,
    mcTauPtCut    = 15,
    )
susyCoreSequence.insert(susyCoreSequence.index(ttHFatJetAna)+1, ttHDecluster)


from CMGTools.TTHAnalysis.analyzers.treeProducerSusyMultilepton import * 

if not removeJecUncertainty:
    susyMultilepton_globalObjects.update({
            "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
            "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
            })
    susyMultilepton_collections.update({
            "cleanJets_jecUp"       : NTupleCollection("Jet_jecUp",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC plus 1sigma)"),
            "cleanJets_jecDown"     : NTupleCollection("Jet_jecDown",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC minus 1sigma)"),
            "discardedJets_jecUp"   : NTupleCollection("DiscJet_jecUp", jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC +1sigma)"),
            "discardedJets_jecDown" : NTupleCollection("DiscJet_jecDown", jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC -1sigma)"),
            })

## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusyMultilepton',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     globalVariables = susyMultilepton_globalVariables,
     globalObjects = susyMultilepton_globalObjects,
     collections = susyMultilepton_collections,
)


## histo counter
if not runSMS:
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer),
                            susyCounter)
else:
    susyCounter.bypass_trackMass_check = False
    susyCoreSequence.insert(susyCoreSequence.index(susyScanAna)+1,susyCounter)

# HBHE new filter
from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheAna = cfg.Analyzer(
    hbheAnalyzer, name="hbheAnalyzer", IgnoreTS4TS5ifJetInLowBVRegion=False
    )
if not runSMS:
    susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),hbheAna)
    treeProducer.globalVariables.append(NTupleVariable("hbheFilterNew50ns", lambda ev: ev.hbheFilterNew50ns, int, help="new HBHE filter for 50 ns"))
    treeProducer.globalVariables.append(NTupleVariable("hbheFilterNew25ns", lambda ev: ev.hbheFilterNew25ns, int, help="new HBHE filter for 25 ns"))
    treeProducer.globalVariables.append(NTupleVariable("hbheFilterIso", lambda ev: ev.hbheFilterIso, int, help="HBHE iso-based noise filter"))

#additional MET quantities
metAna.doTkMet = True
treeProducer.globalVariables.append(NTupleVariable("met_trkPt", lambda ev : ev.tkMet.pt() if  hasattr(ev,'tkMet') else  0, help="tkmet p_{T}"))
treeProducer.globalVariables.append(NTupleVariable("met_trkPhi", lambda ev : ev.tkMet.phi() if  hasattr(ev,'tkMet') else  0, help="tkmet phi"))

if not skipT1METCorr:
    if doMETpreprocessor: 
        print "WARNING: you're running the MET preprocessor and also Type1 MET corrections. This is probably not intended."
    jetAna.calculateType1METCorrection = True
    metAna.recalibrate = "type1"
    jetAnaScaleUp.calculateType1METCorrection = True
    metAnaScaleUp.recalibrate = "type1"
    jetAnaScaleDown.calculateType1METCorrection = True
    metAnaScaleDown.recalibrate = "type1"


#-------- SAMPLES AND TRIGGERS -----------


from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
triggerFlagsAna.triggerBits = {
    'mu17mu8' : triggers_mu17mu8,
    'mu17mu8_dz' : triggers_mu17mu8_dz,
    'mu17tkmu8_dz' : triggers_mu17tkmu8_dz,
    'mu17el12' : triggers_mu17el12,
    'el17el12_dz' : triggers_el17el12_dz,
    'el23el12_dz' : triggers_el23el12_dz,
    'mu8el17' : triggers_mu8el17,
    'mu8el23' : triggers_mu8el23,


    'mu30tkmu11_noniso' : triggers_mu30tkmu11,
    'mu30el30_noniso'   : triggers_mu30ele30,
    'doubleele33_noniso': triggers_doubleele33,
    ## combine HT triggers into one OR
    'htall': triggers_pfht200 + 
             triggers_pfht250 + 
             triggers_pfht300 + 
             triggers_pfht350 + 
             triggers_pfht400 + 
             triggers_pfht475 + 
             triggers_pfht600 + 
             triggers_pfht650 + 
             triggers_pfht800,
    'atall': triggers_at51 +
             triggers_at52 +
             triggers_at53 +
             triggers_at54 +
             triggers_at55 +
             triggers_at57 +
             triggers_at63,
    'htmet': triggers_htmet
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = True
triggerFlagsAna.checkL1Prescale = True

if runSMS:
    susyCoreSequence.remove(triggerFlagsAna)
    susyCoreSequence.remove(triggerAna)
    susyCoreSequence.remove(eventFlagsAna)
    ttHLepSkim.requireSameSignPair = True

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_signals import *

from CMGTools.RootTools.samples.configTools import printSummary, configureSplittingFromTime, cropToLumi

#print 'After cropping to lumi and adjusting the splitting:'
#printSummary(selectedComponents)
# Use the dropLHEweights option if you don't need the per-event LHE weights! It saves a lot of space.


#selectedComponents = SMS_miniAODv2_T1tttt
#susyCounter.SMS_varying_masses = ['genSusyMGluino','genSusyMNeutralino']

selectedComponents = [TTJets_DiLepton, TTJets_DiLepton_ext, TTLep_pow_ext,
                      TBar_tWch, T_tWch,
                      DYJetsToLL_M10to50, DYJetsToLL_M50,
                      #DY1JetsToLL_M50_LO, DY2JetsToLL_M50_LO, DY3JetsToLL_M50_LO, DY4JetsToLL_M50_LO  ]
                      DYJetsToLL_M50_HT100to200_ext, DYJetsToLL_M50_HT200to400_ext, DYJetsToLL_M50_HT400to600_ext, DYJetsToLL_M50_HT600toInf, DYJetsToLL_M50_HT600toInf_ext,
                      ZZ, WZTo2L2Q, WZTo3LNu, WWTo2L2Nu, TTZToLLNuNu, TTWToLNu ]
for comp in selectedComponents:
    comp.splitFactor = 100
    comp.fineSplitFactor = 1
                      

if runData and not isTest: # For running on data

    is50ns = False
    dataChunks = []

    json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274443_13TeV_PromptReco_Collisions16_JSON.txt' ## june 16, 2.6 fb-1

    processing = "Run2016B-PromptReco-v1"; short = "Run2016B-PromptReco-v1"; run_ranges = []; useAAA=False;
    dataChunks.append((json,processing,short,run_ranges,useAAA))

    processing = "Run2016B-PromptReco-v2"; short = "Run2016B-PromptReco-v2"; run_ranges = []; useAAA=False;
    dataChunks.append((json,processing,short,run_ranges,useAAA))

    compSelection = ""; compVeto = ""
    DatasetsAndTriggers = []
    selectedComponents = [];
 
    DatasetsAndTriggers.append( ("DoubleMuon", []) )
    DatasetsAndTriggers.append( ("DoubleEG",   []) )
    DatasetsAndTriggers.append( ("MuonEG",     []) )
    DatasetsAndTriggers.append( ("JetHT",      []) )
    DatasetsAndTriggers.append( ("HTMHT",      []) )
    
    for json,processing,short,run_ranges,useAAA in dataChunks:
        if len(run_ranges)==0: run_ranges=[None]
        vetos = []
        for pd,triggers in DatasetsAndTriggers:
            for run_range in run_ranges:
                label = ""
                if run_range!=None:
                    label = "_runs_%d_%d" % run_range if run_range[0] != run_range[1] else "run_%d" % (run_range[0],)
                compname = pd+"_"+short+label
                if ((compSelection and not re.search(compSelection, compname)) or
                    (compVeto      and     re.search(compVeto,      compname))):
                        print "Will skip %s" % (compname)
                        continue
                myprocessing = processing
                comp = kreator.makeDataComponent(compname, 
                                                 "/"+pd+"/"+myprocessing+"/MINIAOD", 
                                                 "CMS", ".*root", 
                                                 json=json, 
                                                 run_range=run_range, 
                                                 triggers=triggers[:], vetoTriggers = vetos[:],
                                                 useAAA=useAAA)
                print "Will process %s (%d files)" % (comp.name, len(comp.files))
    #            print "\ttrigger sel %s, veto %s" % (triggers, vetos)
                comp.splitFactor = len(comp.files)/8
                comp.fineSplitFactor = 1
                selectedComponents.append( comp )
            vetos += triggers
    if json is None:
        susyCoreSequence.remove(jsonAna)

if runSMS:
    jetAna.applyL2L3Residual = False
    jetAnaScaleUp.applyL2L3Residual = False
    jetAnaScaleDown.applyL2L3Residual = False

if removeJetReCalibration:
    jetAna.recalibrateJets = False
    jetAnaScaleUp.recalibrateJets = False
    jetAnaScaleDown.recalibrateJets = False

if forcedSplitFactor>0 or forcedFineSplitFactor>0:
    if forcedFineSplitFactor>0 and forcedSplitFactor!=1: raise RuntimeError, 'splitFactor must be 1 if setting fineSplitFactor'
    for c in selectedComponents:
        if forcedSplitFactor>0: c.splitFactor = forcedSplitFactor
        if forcedFineSplitFactor>0: c.fineSplitFactor = forcedFineSplitFactor


#-------- SEQUENCE -----------

sequence = cfg.Sequence(susyCoreSequence+[
        ttHJetTauAna,
        ttHEventAna,
        treeProducer,
    ])
preprocessor = None

#-------- HOW TO RUN -----------

test = getHeppyOption('test')
if test == '1':
    comp = selectedComponents[0]
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
elif test == 'synch':
    selectedComponents =  [TTJets_DiLepton]
    for comp in selectedComponents:
        comp.files = ['/afs/cern.ch/work/m/mdunser/public/synchFiles/files2016/doubleMuonFile.root']
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
elif test == '2':
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        comp.fineSplitFactor = 1
elif test == '3':
    for comp in selectedComponents:
        comp.files = comp.files[:1]
        comp.splitFactor = 1
        comp.fineSplitFactor = 4
elif test == '5':
    for comp in selectedComponents:
        comp.files = comp.files[:5]
        comp.splitFactor = 1
        comp.fineSplitFactor = 5
elif test == '80X-data':
    DoubleMuon = kreator.makeDataComponent("DoubleMuon_Run2016B", 
                            "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", 
                            run_range = (271036,274443), triggers = [] )
    selectedComponents = [ DoubleMuon ]
    for comp in selectedComponents:
        comp.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274443_13TeV_PromptReco_Collisions16_JSON.txt'
        comp.splitFactor = 1
        comp.files = ['/afs/cern.ch/work/m/mdunser/public/synchFiles/files2016/doubleMuonFile.root']

elif test != None:
    raise RuntimeError, "Unknown test %r" % test

## FAST mode: pre-skim using reco leptons, don't do accounting of LHE weights (slow)"
## Useful for large background samples with low skim efficiency
if getHeppyOption("fast"):
    susyCounter.doLHE = False
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer2lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 5 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 7,
        minLeptons = 2, 
    )
    if jsonAna in sequence:
        sequence.insert(sequence.index(jsonAna)+1, fastSkim)
    else:
        sequence.insert(sequence.index(skimAnalyzer)+1, fastSkim)

dropLHEWeights = True
if dropLHEWeights:
    treeProducer.collections.pop("LHE_weights")
    if lheWeightAna in sequence: sequence.remove(lheWeightAna)
    susyCounter.doLHE = False

## Auto-AAA
if not getHeppyOption("isCrab"):
    from CMGTools.Production import changeComponentAccessMode
    from CMGTools.Production.localityChecker import LocalityChecker
    tier2Checker = LocalityChecker("T2_CH_CERN", datasets="/*/*/MINIAOD*")
    for comp in selectedComponents:
        if len(comp.files) == 0: raise RuntimeError, "Empty component: "+comp.name
        if not hasattr(comp,'dataset'): continue
        if not re.match("/[^/]+/[^/]+/MINIAOD(SIM)?", comp.dataset): continue
        if "/store/" not in comp.files[0]: continue
        if re.search("/store/(group|user|cmst3)/", comp.files[0]): continue
        if not tier2Checker.available(comp.dataset):
            print "Dataset %s is not available, will use AAA" % comp.dataset
            changeComponentAccessMode.convertComponent(comp, "root://cms-xrd-global.cern.ch/%s")
            if 'X509_USER_PROXY' not in os.environ or "/afs/" not in os.environ['X509_USER_PROXY']:
                raise RuntimeError, "X509_USER_PROXY not defined or not pointing to /afs"

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerSusyMultilepton/tree.root',
    option='recreate'
    )    
outputService.append(output_service)

# the following is declared in case this cfg is used in input to the heppy.py script
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
