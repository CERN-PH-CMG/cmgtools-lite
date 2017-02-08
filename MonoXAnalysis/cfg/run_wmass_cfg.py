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
runData = getHeppyOption("runData",False)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
saveSuperClusterVariables = getHeppyOption("saveSuperClusterVariables",True)
saveFatJetIDVariables = getHeppyOption("saveFatJetIDVariables",False)
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
doT1METCorr = getHeppyOption("doT1METCorr",True)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("isTest",False)
doLepCorr = getHeppyOption("doLepCorr",True)
doPhotonCorr = getHeppyOption("doPhotonCorr",True)

# Define skims
diLepSkim = False
singleLepSkim = True

# --- Z->ll control sample SKIMMING ---
if diLepSkim == True:
    monoJetCtrlLepSkim.minLeptons = 2
# --- 1 Lep SKIMMING
if singleLepSkim == True:
    monoJetCtrlLepSkim.minLeptons = 1
    # NB. The HLT electron ID also includes isolation
    monoJetCtrlLepSkim.idCut = '(lepton.muonID("POG_ID_Tight") and lepton.relIso04 < 0.5) if abs(lepton.pdgId())==13 else (lepton.electronID("POG_Cuts_ID_SPRING16_25ns_v1_HLT"))'
    monoJetCtrlLepSkim.ptCuts = [15]
    

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


from CMGTools.MonoXAnalysis.analyzers.treeProducerDarkMatterMonoJet import * 

## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerDarkMatterMonoJet',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     defaultFloatType = 'F', # use Float_t for floating point
     PDFWeights = PDFWeights,
     doPDFVars = True,
     globalVariables = dmMonoJet_globalVariables,
     globalObjects = dmMonoJet_globalObjects,
     collections = dmMonoJet_collections,
)

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
   treeProducer,
    ])


from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleMuNoIso' : triggers_mumu_noniso + triggers_mu27tkmu8,
    'DoubleEl' : triggers_ee,
    'SingleMu' : triggers_1mu_iso,
    'SingleEl' : triggers_1e,
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = True
triggerFlagsAna.checkL1Prescale = True

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv1 import *
from CMGTools.MonoXAnalysis.samples.samples_monojet_13TeV_80X import *
from CMGTools.MonoXAnalysis.samples.samples_Hinv_13TeV_80X import *

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

json = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt"
if False:
    is50ns = False
    selectedComponents = PrivateSamplesData
    for comp in selectedComponents:
        comp.splitFactor = 100     
        comp.fineSplitFactor = 1

if runData and not isTest: # For running on data
    useAAA=False; is50ns=False

    compSelection = ""
    DatasetsAndTriggers = []
    selectedComponents = []; vetos = []
    ProcessingsAndRunRanges = []; Shorts = []

    # --- 2015 DATA ---
    # ProcessingsAndRunRanges.append( ("Run2015C_25ns-05Oct2015-v1", [254227,255031] ) ); Shorts.append("Run2015C_05Oct")
    # ProcessingsAndRunRanges.append( ("Run2015D-05Oct2015-v1", [256630,258158] ) ); Shorts.append("Run2015D_05Oct")
    # ProcessingsAndRunRanges.append( ("Run2015D-PromptReco-v4", [258159,999999] ) ); Shorts.append("Run2015D_v4")
    # ProcessingsAndRunRanges.append( ("Run2015C_25ns-16Dec2015-v1", [254227,254914] ) ); Shorts.append("Run2015C_16Dec")
    # ProcessingsAndRunRanges.append( ("Run2015D-16Dec2015-v1", [256630,260627] ) ); Shorts.append("Run2015D_16Dec")
    
    # --- 2016 DATA ---
    ProcessingsAndRunRanges.append( ("Run2016B-PromptReco-v1", [272023,273146] ) ); Shorts.append("Run2016B_PromptReco_v1")
    ProcessingsAndRunRanges.append( ("Run2016B-PromptReco-v2", [273150,275376] ) ); Shorts.append("Run2016B_PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016C-PromptReco-v2", [275420,276283] ) ); Shorts.append("Run2016C_PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016D-PromptReco-v2", [276315,276811] ) ); Shorts.append("Run2016D_PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016E-PromptReco-v2", [276830,277420] ) ); Shorts.append("Run2016E_PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016F-PromptReco-v1", [277820,278808] ) ); Shorts.append("Run2016F_PromptReco_v1")
    ProcessingsAndRunRanges.append( ("Run2016G-PromptReco-v1", [278816,280385] ) ); Shorts.append("Run2016G_PromptReco_v1")
    ProcessingsAndRunRanges.append( ("Run2016H-PromptReco-v1", [281010,281202] ) ); Shorts.append("Run2016H_PromptReco_v1")
    ProcessingsAndRunRanges.append( ("Run2016H-PromptReco-v2", [281207,284035] ) ); Shorts.append("Run2016H_PromptReco_v2")
    ProcessingsAndRunRanges.append( ("Run2016H-PromptReco-v3", [284036,284068] ) ); Shorts.append("Run2016H_PromptReco_v3")

    if diLepSkim == True:
        DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso + triggers_mumu_ss + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt) )
        DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_doubleele33 + triggers_doubleele33_MW + triggers_ee_ht + triggers_3e) )
    elif singleLepSkim == True:
        DatasetsAndTriggers.append( ("SingleElectron", triggers_1e) )
        DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_noniso) )

    for pd,triggers in DatasetsAndTriggers:
        iproc=0 
        for processing,run_range in ProcessingsAndRunRanges:
            # if ("DoubleEG" in pd): processing.replace("v1","v2",1) 
            label = "runs_%d_%d" % (run_range[0],run_range[1]) if run_range[0] != run_range[1] else "run_%d" % run_range[0]
            compname = pd+"_"+Shorts[iproc]+"_"+label
            if ((compSelection and not re.search(compSelection, compname))):
                print "Will skip %s" % (compname)

                continue
            print "Building component ",compname," with run range ",label, "\n"
            comp = kreator.makeDataComponent(compname, 
                                             "/"+pd+"/"+processing+"/MINIAOD", 
                                             "CMS", ".*root", 
                                             json=json, 
                                             run_range=run_range, 
                                             #triggers=triggers[:], vetoTriggers = vetos[:],
                                             useAAA=useAAA)
            print "Will process %s (%d files)" % (comp.name, len(comp.files))
            print "\ttrigger sel %s, veto %s" % (triggers, vetos)
            comp.splitFactor = len(comp.files)/4
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
    mcSamples = [DYJetsToLL_M50_reHLT, WJetsToLNu_reHLT]
    selectedComponents = mcSamples 
    for comp in selectedComponents:
        comp.splitFactor = len(comp.files)/4
        comp.fineSplitFactor = 1
        # if 'HToInvisible' in comp.name: triggerFlagsAna.processName = 'HLT2'
        # else: triggerFlagsAna.processName = 'HLT'

if runData==False and isTest: # Synch MC sample
    is50ns = False
    comp = kreator.makeMCComponent("TTbarDM","/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.0)
    selectedComponents = [ comp ]
    for comp in selectedComponents:
        comp.splitFactor = len(comp.files)
        comp.fineSplitFactor = 1


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
    what = getHeppyOption("sample")
    if what == "TTbarDM":
        comp = kreator.makeMCComponent("TTbarDM","/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.0)
        selectedComponents = [ comp ]
    elif what == "VBFHinv":
        comp = kreator.makeMCComponent("VBF_HToInvisible_M125","/VBF_HToInvisible_M125_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM", "CMS", ".*root", 3.782)
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIISpring16MiniAODv2/VBF_HToInvisible_M125_13TeV_powheg_pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/90000/0E1D90B0-583A-E611-8CC4-008CFA56D894.root' ]
        triggerFlagsAna.processName = 'HLT2'
        selectedComponents = [ comp ]
    elif what == "DYJets":
        comp = DYJetsToLL_M50
#        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIISpring16MiniAODv1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/60000/E0553CDE-0300-E611-B2C4-0CC47A4C8F1C.root' ]
        comp.files = [ 'root://eoscms//eos/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/40000/00200284-F15C-E611-AA9B-002590574776.root' ]
        triggerFlagsAna.processName = 'HLT2'
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
        selectedComponents = monojet_Asymptotic25ns
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

## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerDarkMatterMonoJet/tree.root',
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


