##########################################################
##       CONFIGURATION FOR EXO MONOJET TREES            ##
## skim condition:   MET > 200 GeV                      ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

# Load all analyzers
from CMGTools.MonoXAnalysis.analyzers.dmCore_modules_cff import * 
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------

is50ns = getHeppyOption("is50ns",False)
runData = getHeppyOption("runData",True)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
saveSuperClusterVariables = getHeppyOption("saveSuperClusterVariables",True)
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
doT1METCorr = getHeppyOption("doT1METCorr",True)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))
doLepCorr = getHeppyOption("doLepCorr",True)
doPhotonCorr = getHeppyOption("doPhotonCorr",True)

# Define skims
signalSkim = False
diLepSkim = False
singleLepSkim = False
singlePhotonSkim = False

# --- MONOJET SKIMMING ---
if signalSkim == True:
    monoJetSkim.metCut = 200
    monoJetSkim.jetPtCuts = []

# --- Z->ll control sample SKIMMING ---
if diLepSkim == True:
    monoJetCtrlLepSkim.minLeptons = 2
if singleLepSkim == True:
    monoJetCtrlLepSkim.minLeptons = 1
    monoJetCtrlLepSkim.idCut = '(lepton.muonID("POG_ID_Tight") and lepton.relIso04 < 0.12) if abs(lepton.pdgId())==13 else \
(lepton.electronID("POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Tight_full5x5") and (lepton.relIso03<0.0354 if abs(lepton.superCluster().eta())<1.479 else lepton.relIso03<0.0646))'
    monoJetCtrlLepSkim.ptCuts = [20]
if singlePhotonSkim == True:
    gammaJetCtrlSkim.minPhotons = 1
    gammaJetCtrlSkim.minJets = 1

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
##  TOLOLOGIAL VARIABLES: RAZOR
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


from CMGTools.MonoXAnalysis.analyzers.treeProducerDarkMatterMonoJet import * 

# for electron scale and resolution checks
if saveSuperClusterVariables:
    leptonTypeExtra.addVariables([
            NTupleVariable("e5x5", lambda x: x.e5x5() if (abs(x.pdgId())==11 and hasattr(x,"e5x5")) else -999, help="Electron e5x5"),
            NTupleVariable("r9", lambda x: x.r9() if (abs(x.pdgId())==11 and hasattr(x,"r9")) else -999, help="Electron r9"),
            NTupleVariable("sigmaIetaIeta", lambda x: x.sigmaIetaIeta() if (abs(x.pdgId())==11 and hasattr(x,"sigmaIetaIeta")) else -999, help="Electron sigmaIetaIeta"),
            NTupleVariable("sigmaIphiIphi", lambda x: x.sigmaIphiIphi() if (abs(x.pdgId())==11 and hasattr(x,"sigmaIphiIphi")) else -999, help="Electron sigmaIphiIphi"),
            NTupleVariable("hcalOverEcal", lambda x: x.hcalOverEcal() if (abs(x.pdgId())==11 and hasattr(x,"hcalOverEcal")) else -999, help="Electron hcalOverEcal"),
            NTupleVariable("full5x5_e5x5", lambda x: x.full5x5_e5x5() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_e5x5")) else -999, help="Electron full5x5_e5x5"),
            NTupleVariable("full5x5_r9", lambda x: x.full5x5_r9() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_r9")) else -999, help="Electron full5x5_r9"),
            NTupleVariable("full5x5_sigmaIetaIeta", lambda x: x.full5x5_sigmaIetaIeta() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_sigmaIetaIeta")) else -999, help="Electron full5x5_sigmaIetaIeta"),
            NTupleVariable("full5x5_sigmaIphiIphi", lambda x: x.full5x5_sigmaIphiIphi() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_sigmaIphiIphi")) else -999, help="Electron full5x5_sigmaIphiIphi"),
            NTupleVariable("full5x5_hcalOverEcal", lambda x: x.full5x5_hcalOverEcal() if (abs(x.pdgId())==11 and hasattr(x,"full5x5_hcalOverEcal")) else -999, help="Electron full5x5_hcalOverEcal"),
            NTupleVariable("correctedEcalEnergy", lambda x: x.correctedEcalEnergy() if (abs(x.pdgId())==11 and hasattr(x,"correctedEcalEnergy")) else -999, help="Electron correctedEcalEnergy"),
            NTupleVariable("eSuperClusterOverP", lambda x: x.eSuperClusterOverP() if (abs(x.pdgId())==11 and hasattr(x,"eSuperClusterOverP")) else -999, help="Electron eSuperClusterOverP"),
            NTupleVariable("ecalEnergy", lambda x: x.ecalEnergy() if (abs(x.pdgId())==11 and hasattr(x,"ecalEnergy")) else -999, help="Electron ecalEnergy"),
            NTupleVariable("superCluster_rawEnergy", lambda x: x.superCluster().rawEnergy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.rawEnergy"),
            NTupleVariable("superCluster_preshowerEnergy", lambda x: x.superCluster().preshowerEnergy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.preshowerEnergy"),
            NTupleVariable("superCluster_correctedEnergy", lambda x: x.superCluster().correctedEnergy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.correctedEnergy"),
            NTupleVariable("superCluster_energy", lambda x: x.superCluster().energy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.energy"),
            NTupleVariable("superCluster_clustersSize", lambda x: x.superCluster().clustersSize() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.clustersSize"),
            NTupleVariable("superCluster_seed.energy", lambda x: x.superCluster().seed().energy() if (abs(x.pdgId())==11 and hasattr(x,"superCluster")) else -999, help="Electron superCluster.seed.energy"),
])


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
#   monoXRazorAna,
#   monoXMT2Ana,
   monoJetVarAna,
   MonoJetEventAna,
   treeProducer,
    ])


from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import *
from CMGTools.RootTools.samples.triggers_8TeV import triggers_1mu_8TeV, triggers_mumu_8TeV, triggers_mue_8TeV, triggers_ee_8TeV;
triggers_AllMonojet = triggers_metNoMu90_mhtNoMu90 + triggers_metNoMu120_mhtNoMu120 + triggers_AllMET170 + triggers_AllMET300
triggers_SinglePhoton = triggers_photon155 + triggers_photon165_HE10 + triggers_photon175
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
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = False
triggerFlagsAna.checkL1Prescale = False

from CMGTools.MonoXAnalysis.samples.samples_monojet_13TeV_76X import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *

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

json = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON.txt"
if runData and not isTest: # For running on data
    run_ranges = [ (254227,260627) ]; useAAA=False; is50ns=False

    compSelection = ""
    DatasetsAndTriggers = []
    selectedComponents = []; vetos = []
    ProcessingsAndRunRanges = []; Shorts = []

    # ProcessingsAndRunRanges.append( ("Run2015C_25ns-05Oct2015-v1", [254227,255031] ) ); Shorts.append("Run2015C_05Oct")
    # ProcessingsAndRunRanges.append( ("Run2015D-05Oct2015-v1", [256630,258158] ) ); Shorts.append("Run2015D_05Oct")
    # ProcessingsAndRunRanges.append( ("Run2015D-PromptReco-v4", [258159,999999] ) ); Shorts.append("Run2015D_v4")

    ProcessingsAndRunRanges.append( ("Run2015C_25ns-16Dec2015-v1", [254227,254914] ) ); Shorts.append("Run2015C_16Dec")
    ProcessingsAndRunRanges.append( ("Run2015D-16Dec2015-v1", [256630,260627] ) ); Shorts.append("Run2015D_16Dec")
    
    if diLepSkim == True:
        DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso + triggers_mumu_ss + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt + triggers_AllMonojet) )
        DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_ee_ht + triggers_3e) )
    if singleLepSkim == True:
        DatasetsAndTriggers.append( ("SingleElectron", triggers_ee + triggers_ee_ht + triggers_3e + triggers_1e + triggers_1e_50ns) )
        DatasetsAndTriggers.append( ("SinglePhoton",   triggers_SinglePhoton) )
    if singlePhotonSkim == True:
        DatasetsAndTriggers.append( ("SinglePhoton", triggers_SinglePhoton) )
    if signalSkim == True:
        DatasetsAndTriggers.append( ("MET", triggers_AllMonojet ) )
        

    for pd,triggers in DatasetsAndTriggers:
        iproc=0 
        for processing,run_dslimits in ProcessingsAndRunRanges:
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
                                                 triggers=triggers[:], vetoTriggers = vetos[:],
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
    mcSamples = mcSamples_monojet_Asymptotic25ns
    if signalSkim:
        # full signal scan (many datasets!)
        # mcSamples += mcSamples_monojet_Asymptotic25ns_signals
        monojet_signals_cherrypick = [ DMS_Mphi_2000_Mchi_1_gSM_1p0_gDM_1p0, DMPS_Mphi_2000_Mchi_1_gSM_1p0_gDM_1p0, DMAV_Mphi_2000_Mchi_1_gSM_0p25_gDM_1p0]
        mcSamples += monojet_signals_cherrypick
    selectedComponents = mcSamples 

### 50 ns 74X MC samples
#selectedComponents = mcSamples_monojet_Asymptotic50ns ; is50ns = True
    for comp in selectedComponents:
        comp.splitFactor = len(comp.files)/4
        comp.fineSplitFactor = 1



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
elif test == 'synch-76X': # sync
    #eventSelector.toSelect = [ (1,165,84628), ]
    #sequence = cfg.Sequence([eventSelector] + dmCoreSequence + [ ttHFatJetAna, monoJetVarAna, MonoJetEventAna, treeProducer, ])
    monoJetSkim.metCut = 0  
    what = getHeppyOption("sample")
    if what == "TTbarDM":
        comp = kreator.makeMCComponent("TTbarDM","/TTbarDMJets_pseudoscalar_Mchi-1_Mphi-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 1.0, useAAA=True)
        selectedComponents = [ comp ]
    elif what == "DYJets":
        comp = DYJetsToLL_M50
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_HCALDebug_76X_mcRun2_asymptotic_v12-v1/00000/006C9F73-3FB9-E511-9AFE-001E67E95C52.root' ]
        selectedComponents = [ comp ]
    elif what == "TTJets":
        comp = TJets_LO
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIIFall15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/00547C97-2FCC-E511-8D75-002590DB91D2.root' ]
        selectedComponents = [ comp ]
    elif what == "WJets":
        comp = WJetsToLNu_HT100to200
        comp.files = [ 'root://eoscms//eos/cms/store/mc/RunIIFall15MiniAODv2/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/50000/0CF84FB8-2CBC-E511-B255-001EC9AF22C6.root' ]
        selectedComponents = [ comp ]
    else:
        selectedComponents = mcSamples_monojet_Asymptotic25ns
    jetAna.smearJets       = False
    for comp in selectedComponents:
        comp.splitFactor = 1
        comp.fineSplitFactor = 1 if getHeppyOption("single") else 4
elif test == '76X-Data':
    what = getHeppyOption("sample")
    if what == "DoubleEG":
        comp = DoubleEG_Run2015D_16Dec
        comp.files = [ 'root://eoscms//eos/cms/store/data/Run2015D/DoubleEG/MINIAOD/16Dec2015-v1/20000/40B59022-57A5-E511-B086-0CC47A4C8F26.root' ]
        selectedComponents = [ comp ]
    elif what == "DoubleMuon":
        comp = DoubleMuon_Run2015D_16Dec
        comp.files = [ 'root://eoscms//eos/cms/store/data/Run2015D/DoubleMuon/MINIAOD/16Dec2015-v1/60000/B4354564-90B3-E511-8FC7-0025905B8598.root' ]
        selectedComponents = [ comp ]
    else:
        selectedComponents = dataSamples_Run2015D_16Dec
    for comp in selectedComponents:
        comp.json = json
        comp.splitFactor = 1
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


