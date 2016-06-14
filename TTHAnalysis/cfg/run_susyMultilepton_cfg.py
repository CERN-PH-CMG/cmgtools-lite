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
analysis = getHeppyOption("analysis","ttH")
runData = getHeppyOption("runData",False)
runDataQCD = getHeppyOption("runDataQCD",False)
runFRMC = getHeppyOption("runFRMC",False)
runSMS = getHeppyOption("runSMS",False)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
saveSuperClusterVariables = getHeppyOption("saveSuperClusterVariables",False)
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
removeJecUncertainty = getHeppyOption("removeJecUncertainty",False)
doMETpreprocessor = getHeppyOption("doMETpreprocessor",False)
skipT1METCorr = getHeppyOption("skipT1METCorr",False)
#doAK4PFCHSchargedJets = getHeppyOption("doAK4PFCHSchargedJets",False)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))
selectedEvents=getHeppyOption("selectEvents","")

if analysis not in ['ttH','susy','SOS']: raise RuntimeError, 'Analysis type unknown'
print 'Using analysis type: %s'%analysis

# Lepton Skimming
ttHLepSkim.minLeptons = 2
ttHLepSkim.maxLeptons = 999
#ttHLepSkim.idCut  = ""
#ttHLepSkim.ptCuts = []

# Run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
lepAna.doIsolationScan = False

# Lepton Preselection
lepAna.loose_electron_id = "POG_MVA_ID_Spring15_NonTrig_VLooseIdEmu"
isolation = "miniIso"

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



if analysis in ['SOS']:
## -- SOS preselection settings ---

    lepAna.doDirectionalIsolation = [0.3,0.4]
    lepAna.doFixedConeIsoWithMiniIsoVeto = True

    # Lepton Skimming
    ttHLepSkim.minLeptons = 2
    ttHLepSkim.maxLeptons = 999
    ttHLepSkim.ptCuts = [5,3]
    
#    # Jet-Met Skimming
#    ttHJetMETSkim.jetPtCuts = [0,]
    ttHJetMETSkim.metCut    = 50
    susyCoreSequence.append(ttHJetMETSkim)

    # Lepton Preselection
    lepAna.inclusive_muon_pt  = 3
    lepAna.loose_muon_pt  = 3
    lepAna.inclusive_electron_pt  = 5
    lepAna.loose_electron_pt  = 5
#    isolation = None
#    lepAna.loose_electron_id = ""

    # Lepton-Jet Cleaning
    jetAna.minLepPt = 20 
    jetAnaScaleUp.minLepPt = 20 
    jetAnaScaleDown.minLepPt = 20 
    # otherwise with only absIso cut at 10 GeV and no relIso we risk cleaning away good jets

if isolation == "miniIso": 
    if (analysis=="ttH") or (analysis =="SOS"):
        lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4 and muon.sip3D() < 8
        lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4 and elec.sip3D() < 8
    elif analysis=="susy":
        lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
        lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
    else: raise RuntimeError,'analysis field is not correctly configured'
elif isolation == None:
    lepAna.loose_muon_isoCut     = lambda muon : True
    lepAna.loose_electron_isoCut = lambda elec : True
elif isolation == "absIso03":
    lepAna.loose_muon_absIso = 10.0
    lepAna.loose_electron_relIso = 99.0
    lepAna.loose_muon_relIso = 99.0
    lepAna.loose_electron_absIso = 10.0
else:
    # nothing to do, will use normal relIso03
    pass

# Switch on slow QGL
jetAna.doQG = True
jetAnaScaleUp.doQG = True
jetAnaScaleDown.doQG = True

# Switch off slow photon MC matching
photonAna.do_mc_match = False

# Loose Tau configuration
tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 2.3
tauAna.loose_decayModeID = "decayModeFinding"
tauAna.loose_tauID = "byLooseIsolationMVArun2v1DBdR03oldDMwLT"
if analysis in ["ttH"]: #if cleaning jet-loose tau cleaning
    jetAna.cleanJetsFromTaus = True
    jetAnaScaleUp.cleanJetsFromTaus = True
    jetAnaScaleDown.cleanJetsFromTaus = True


#-------- ADDITIONAL ANALYZERS -----------

if analysis in ['SOS']:
    #Adding LHE Analyzer for saving lheHT
    from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer 
    LHEAna = LHEAnalyzer.defaultConfig
    susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
                            LHEAna)

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

if analysis=="susy":
    susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                            susyLeptonMatchAna)
    leptonTypeSusyExtraLight.addVariables([
            NTupleVariable("mcUCSXMatchId", lambda x : x.mcUCSXMatchId if hasattr(x,'mcUCSXMatchId') else -1, mcOnly=True, help="MC truth matching a la UCSX"),
            ])


if lepAna.doIsolationScan:
    leptonTypeSusyExtraLight.addVariables([
            NTupleVariable("scanAbsIsoCharged005", lambda x : x.ScanAbsIsoCharged005 if hasattr(x,'ScanAbsIsoCharged005') else -999, help="PF abs charged isolation dR=0.05, no pile-up correction"),
            NTupleVariable("scanAbsIsoCharged01", lambda x : x.ScanAbsIsoCharged01 if hasattr(x,'ScanAbsIsoCharged01') else -999, help="PF abs charged isolation dR=0.1, no pile-up correction"),
            NTupleVariable("scanAbsIsoCharged02", lambda x : x.ScanAbsIsoCharged02 if hasattr(x,'ScanAbsIsoCharged02') else -999, help="PF abs charged isolation dR=0.2, no pile-up correction"),
            NTupleVariable("scanAbsIsoCharged03", lambda x : x.ScanAbsIsoCharged03 if hasattr(x,'ScanAbsIsoCharged03') else -999, help="PF abs charged isolation dR=0.3, no pile-up correction"),
            NTupleVariable("scanAbsIsoCharged04", lambda x : x.ScanAbsIsoCharged04 if hasattr(x,'ScanAbsIsoCharged04') else -999, help="PF abs charged isolation dR=0.4, no pile-up correction"),
            NTupleVariable("scanAbsIsoNeutral005", lambda x : x.ScanAbsIsoNeutral005 if hasattr(x,'ScanAbsIsoNeutral005') else -999, help="PF abs neutral+photon isolation dR=0.05, no pile-up correction"),
            NTupleVariable("scanAbsIsoNeutral01", lambda x : x.ScanAbsIsoNeutral01 if hasattr(x,'ScanAbsIsoNeutral01') else -999, help="PF abs neutral+photon isolation dR=0.1, no pile-up correction"),
            NTupleVariable("scanAbsIsoNeutral02", lambda x : x.ScanAbsIsoNeutral02 if hasattr(x,'ScanAbsIsoNeutral02') else -999, help="PF abs neutral+photon isolation dR=0.2, no pile-up correction"),
            NTupleVariable("scanAbsIsoNeutral03", lambda x : x.ScanAbsIsoNeutral03 if hasattr(x,'ScanAbsIsoNeutral03') else -999, help="PF abs neutral+photon isolation dR=0.3, no pile-up correction"),
            NTupleVariable("scanAbsIsoNeutral04", lambda x : x.ScanAbsIsoNeutral04 if hasattr(x,'ScanAbsIsoNeutral04') else -999, help="PF abs neutral+photon isolation dR=0.4, no pile-up correction"),
            NTupleVariable("miniIsoR", lambda x: getattr(x,'miniIsoR',-999), help="miniIso cone size"),
            NTupleVariable("effArea", lambda x: getattr(x,'EffectiveArea03',-999), help="effective area used for PU subtraction"),
            NTupleVariable("rhoForEA", lambda x: getattr(x,'rho',-999), help="rho used for EA PU subtraction")
            ])

# for electron scale and resolution checks
if saveSuperClusterVariables:
    leptonTypeSusyExtraLight.addVariables([
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
from CMGTools.RootTools.samples.triggers_8TeV import triggers_1mu_8TeV, triggers_mumu_8TeV, triggers_mue_8TeV, triggers_ee_8TeV;
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleMuSS' : triggers_mumu_ss,
    'DoubleMuNoIso' : triggers_mumu_noniso,
    'DoubleEl' : triggers_ee,
    'MuEG'     : triggers_mue,
    'DoubleMuHT' : triggers_mumu_ht,
    'DoubleElHT' : triggers_ee_ht,
    'MuEGHT' : triggers_mue_ht,
    'TripleEl' : triggers_3e,
    'TripleMu' : triggers_3mu,
    'TripleMuA' : triggers_3mu_alt,
    'DoubleMuEl' : triggers_2mu1e,
    'DoubleElMu' : triggers_2e1mu,
    'SingleMu' : triggers_1mu_iso,
    'SingleEl'     : triggers_1e,
    'MonoJet80MET90' : triggers_Jet80MET90,
    'MonoJet80MET120' : triggers_Jet80MET120,
    'METMu5' : triggers_MET120Mu5,
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = True
triggerFlagsAna.checkL1Prescale = True

if runSMS:
    susyCoreSequence.remove(triggerFlagsAna)
    susyCoreSequence.remove(triggerAna)
    susyCoreSequence.remove(eventFlagsAna)
    ttHLepSkim.requireSameSignPair = True

from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv1 import *
from CMGTools.RootTools.samples.samples_13TeV_signals import *
from CMGTools.RootTools.samples.samples_13TeV_76X_susySignalsPriv import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
from CMGTools.HToZZ4L.tools.configTools import printSummary, configureSplittingFromTime, cropToLumi

selectedComponents = [TTLep_pow_ext]
#selectedComponents = SMS_miniAODv2_T1tttt
#susyCounter.SMS_varying_masses = ['genSusyMGluino','genSusyMNeutralino']

if analysis=='susy':
    samples_2l = [DYJetsToLL_M10to50,DYJetsToLL_M50,WWTo2L2Nu,ZZTo2L2Q,WZTo3LNu,TTWToLNu,TTZToLLNuNu,TTJets_DiLepton,TTHnobb_mWCutfix_ext1]
    samples_1l = [WJetsToLNu,TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromTbar,TBarToLeptons_tch_powheg,TToLeptons_sch_amcatnlo,TBar_tWch,T_tWch]
    selectedComponents = samples_1l+samples_2l
    cropToLumi(selectedComponents,2)
    configureSplittingFromTime(samples_1l,50,3)
    configureSplittingFromTime(samples_2l,100,3)
    printSummary(selectedComponents)


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


if runData and not isTest: # For running on data

    is50ns = False
    dataChunks = []

    json = os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/json/Cert_271036-273450_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'
    processing = "Run2016B-PromptReco-v1"; short = "Run2016B_PromptReco_v1"; run_ranges = [(273013,273149)]; useAAA=False;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016B-PromptReco-v2"; short = "Run2016B_PromptReco_v2"; run_ranges = [(273150,273450)]; useAAA=False;
    dataChunks.append((json,processing,short,run_ranges,useAAA))

    json = os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/json/json_DCSONLY.txt'
    processing = "Run2016B-PromptReco-v2"; short = "Run2016B_PromptReco_v2"; run_ranges = [(273492,273504),(273554,273555),(273725,273730)]; useAAA=False;
    dataChunks.append((json,processing,short,run_ranges,useAAA))

    compSelection = ""; compVeto = ""
    DatasetsAndTriggers = []
    selectedComponents = [];
 
    if analysis in ['SOS']:
        DatasetsAndTriggers.append( ("MET", triggers_Jet80MET90 + triggers_Jet80MET120 + triggers_MET120Mu5 ) )
        #DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_iso_50ns + triggers_1mu_noniso) )
    else:
        DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso + triggers_mumu_ss + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt) )
        DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_ee_ht + triggers_3e) )
        DatasetsAndTriggers.append( ("MuonEG",     triggers_mue + triggers_mue_ht + triggers_2mu1e + triggers_2e1mu) )
        DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_iso_50ns + triggers_1mu_noniso) )
        DatasetsAndTriggers.append( ("SingleElectron", triggers_1e + triggers_1e_50ns) )

        if runDataQCD: # for fake rate measurements in data
            ttHLepSkim.minLeptons = 1
            if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
            FRTrigs = triggers_FR_1mu_iso + triggers_FR_1mu_noiso + triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
            for t in FRTrigs:
                tShort = t.replace("HLT_","FR_").replace("_v*","")
                triggerFlagsAna.triggerBits[tShort] = [ t ]
                FRTrigs_mu = triggers_FR_1mu_iso + triggers_FR_1mu_noiso
                FRTrigs_el = triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
                DatasetsAndTriggers = [ (pd,trig) for pd,trig in DatasetsAndTriggers if pd in ['DoubleMuon','DoubleEG'] ]
                for pd,trig in DatasetsAndTriggers:
                    if pd in ['DoubleMuon','SingleMuon']:
                        trig.extend(FRTrigs_mu)
                    elif pd in ['DoubleEG','SingleElectron']:
                        trig.extend(FRTrigs_el)
                    else:
                        print 'the strategy for trigger selection on MuonEG for FR studies should yet be implemented'
                        assert(False)

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

if runFRMC: 
    selectedComponents = [QCD_Mu15] + QCD_Mu5 + QCDPtEMEnriched + QCDPtbcToE + [WJetsToLNu_LO,DYJetsToLL_M10to50,DYJetsToLL_M50]
    printSummary(selectedComponents)
    ttHLepSkim.minLeptons = 1
    if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
    FRTrigs = triggers_FR_1mu_iso + triggers_FR_1mu_noiso + triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
    for c in selectedComponents:
        c.triggers = []
        c.vetoTriggers = [] 
        c.splitFactor = len(c.files)/4
    for t in FRTrigs:
        tShort = t.replace("HLT_","FR_").replace("_v*","")
        triggerFlagsAna.triggerBits[tShort] = [ t ]
    treeProducer.collections = {
        "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
        "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
    }
    if True: # 
        from CMGTools.TTHAnalysis.analyzers.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
        ttHLepQCDFakeRateAna = cfg.Analyzer(ttHLepQCDFakeRateAnalyzer, name="ttHLepQCDFakeRateAna",
            jetSel = lambda jet : jet.pt() > (25 if abs(jet.eta()) < 2.4 else 30),
            pairSel = lambda lep, jet: deltaR(lep.eta(),lep.phi(), jet.eta(), jet.phi()) > 0.7,
        )
        susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, ttHLepQCDFakeRateAna)
        treeProducer.collections = {
            "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
            "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
        }
        leptonTypeSusyExtraLight.addVariables([
            NTupleVariable("awayJet_pt", lambda x: x.awayJet.pt() if x.awayJet else 0, help="pT of away jet"),
            NTupleVariable("awayJet_eta", lambda x: x.awayJet.eta() if x.awayJet else 0, help="eta of away jet"),
            NTupleVariable("awayJet_phi", lambda x: x.awayJet.phi() if x.awayJet else 0, help="phi of away jet"),
            NTupleVariable("awayJet_btagCSV", lambda x: x.awayJet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.awayJet else 0, help="b-tag disc of away jet"),
            NTupleVariable("awayJet_mcFlavour", lambda x: x.awayJet.partonFlavour() if x.awayJet else 0, int, mcOnly=True, help="pT of away jet"),
        ])
    if True: # drop events that don't have at least one lepton+jet pair (reduces W+jets by ~50%)
        ttHLepQCDFakeRateAna.minPairs = 1
    if True: # fask skim 
        from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
        fastSkim = cfg.Analyzer(
            ttHFastLepSkimmer, name="ttHFastLepSkimmer1lep",
            muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
            electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
            minLeptons = 1,
        )
        susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, fastSkim)
        susyCoreSequence.remove(lheWeightAna)
        susyCounter.doLHE = False


    

if is50ns:
    # no change in MC GT since there's no 76X 50ns MC
    jetAna.dataGT   = "76X_dataRun2_v15_Run2015B_50ns"
    jetAnaScaleUp.dataGT   = "76X_dataRun2_v15_Run2015B_50ns"
    jetAnaScaleDown.dataGT   = "76X_dataRun2_v15_Run2015B_50ns"

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

#trigMatchExample = cfg.Analyzer(
#    TriggerMatchAnalyzer, name="TriggerMatchEle27",
#    processName = 'PAT',
#    label = 'Ele27_WP85_Gsf',
#    unpackPathNames = True,
#    trgObjSelectors = [lambda ob: ob.pt()>20, lambda ob: abs(ob.eta())<2.5, lambda ob: len( [t for t in ob.pathNames(True) if re.match("HLT_Ele27_WP85_Gsf_v",t)] )>0 ],
#    collToMatch = "selectedLeptons",
#    collMatchSelectors = [lambda lep,ob: abs(lep.pt()/ob.pt()-1)<0.5, lambda lep,ob: abs(lep.pdgId())==11],
#    collMatchDRCut = 0.3,
#    univoqueMatching = True,
#    verbose = False
#)
#susyCoreSequence.append(trigMatchExample)
#leptonTypeSusyExtra.addVariables([
#        NTupleVariable("matchedTrgObj_Ele27_WP85_Gsf_pt", lambda x: getattr(x,'matchedTrgObjEle27_WP85_Gsf').pt() if getattr(x,'matchedTrgObjEle27_WP85_Gsf',None) else -999, help="Electron trigger pt")
#])

if selectedEvents!="":
    events=[ int(evt) for evt in selectedEvents.split(",") ]
    print "selecting only the following events : ", events
    eventSelector= cfg.Analyzer(
        EventSelector,'EventSelector',
        toSelect = events
        )
    susyCoreSequence.insert(susyCoreSequence.index(lheWeightAna), eventSelector)

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
elif test == "ra5-sync-mc":
    comp = cfg.MCComponent( files = ["root://eoscms.cern.ch//store/mc/RunIISpring16MiniAODv1/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/00000/6E02CA07-BA02-E611-A59E-14187741208F.root"], name="TTW_RA5_sync" )
    comp.triggers = []
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
    sequence.remove(jsonAna)
elif test == '80X-MC':
    what = getHeppyOption("sample","TTLep")
    if what == "TTLep":
        TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
        selectedComponents = [ TTLep_pow ]
        comp = selectedComponents[0]
        comp.triggers = []
        comp.files = [ '/store/mc/RunIISpring16MiniAODv1/TTTo2L2Nu_13TeV-powheg/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/00000/002606A5-C909-E611-85DA-44A8423D7E31.root' ]
        tmpfil = os.path.expandvars("/tmp/$USER/002606A5-C909-E611-85DA-44A8423D7E31.root")
        if not os.path.exists(tmpfil):
            os.system("xrdcp root://eoscms//eos/cms%s %s" % (comp.files[0],tmpfil))
        comp.files = [ tmpfil ]
        if not getHeppyOption("single"): comp.fineSplitFactor = 4
    else: raise RuntimeError, "Unknown MC sample: %s" % what
elif test == '80X-Data':
    DoubleMuon = kreator.makeDataComponent("DoubleMuon_Run2016B_run274315", "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (274315,274315), triggers = triggers_mumu)
    DoubleEG = kreator.makeDataComponent("DoubleEG_Run2016B_run274315", "/DoubleEG/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (274315,274315), triggers = triggers_ee)
    DoubleMuon.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleMuon/MINIAOD/PromptReco-v2/000/274/315/00000/A287989F-E129-E611-B5FB-02163E0142C2.root' ]
    DoubleEG.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleEG/MINIAOD/PromptReco-v2/000/274/315/00000/FEF59D1D-EE29-E611-8793-02163E0143AE.root' ]
    selectedComponents = [ DoubleMuon, DoubleEG ]
    for comp in selectedComponents:
        comp.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt'
        tmpfil = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(comp.files[0]))
        if not os.path.exists(tmpfil): os.system("xrdcp %s %s" % (comp.files[0],tmpfil)) 
        comp.files = [tmpfil]
        comp.splitFactor = 1
        comp.fineSplitFactor = 4
elif test == 'ttH-sync':
    ttHLepSkim.minLeptons=0
    selectedComponents = selectedComponents[:1]
    comp = selectedComponents[0]
    comp.files = ['/store/mc/RunIIFall15MiniAODv2/ttHToNonbb_M125_13TeV_powheg_pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/021B993B-4DBB-E511-BBA6-008CFA1111B4.root']
    tmpfil = os.path.expandvars("/tmp/$USER/021B993B-4DBB-E511-BBA6-008CFA1111B4.root")
    if not os.path.exists(tmpfil):
        os.system("xrdcp root://eoscms//eos/cms%s %s" % (comp.files[0],tmpfil))
    comp.files = [ tmpfil ]
    if not getHeppyOption("single"): comp.fineSplitFactor = 8
elif test != None:
    raise RuntimeError, "Unknown test %r" % test

## FAST mode: pre-skim using reco leptons, don't do accounting of LHE weights (slow)"
## Useful for large background samples with low skim efficiency
if getHeppyOption("fast"):
    susyCounter.doLHE = False
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer2lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
        minLeptons = 2, 
    )
    if jsonAna in sequence:
        sequence.insert(sequence.index(jsonAna)+1, fastSkim)
    else:
        sequence.insert(sequence.index(skimAnalyzer)+1, fastSkim)
if getHeppyOption("dropLHEweights",True):
    treeProducer.collections.pop("LHE_weights")
    if lheWeightAna in sequence: sequence.remove(lheWeightAna)
    susyCounter.doLHE = False

## Auto-AAA
from CMGTools.RootTools.samples.autoAAAconfig import *
if not getHeppyOption("isCrab"):
    autoAAA(selectedComponents)

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

# print summary of components to process
printSummary(selectedComponents)

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
