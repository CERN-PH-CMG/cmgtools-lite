##########################################################
##       CONFIGURATION FOR SOFT MULTILEPTON TREES       ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re


#-------- LOAD ALL ANALYZERS -----------

from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

#-------- SET OPTIONS AND REDEFINE CONFIGURATIONS -----------

run80X = getHeppyOption("run80X",False)
runData = getHeppyOption("runData",False)
runDataQCD = getHeppyOption("runDataQCD",False)
runQCDBM = getHeppyOption("runQCDBM",False)
runFRMC = getHeppyOption("runFRMC",False)
scaleProdToLumi = float(getHeppyOption("scaleProdToLumi",-1)) # produce rough equivalent of X /pb for MC datasets
removeJetReCalibration = getHeppyOption("removeJetReCalibration",False)
removeJecUncertainty = getHeppyOption("removeJecUncertainty",False)
doMETpreprocessor = getHeppyOption("doMETpreprocessor",False)
skipT1METCorr = getHeppyOption("skipT1METCorr",False)
forcedSplitFactor = getHeppyOption("splitFactor",-1)
forcedFineSplitFactor = getHeppyOption("fineSplitFactor",-1)
isTest = getHeppyOption("test",None) != None and not re.match("^\d+$",getHeppyOption("test"))
selectedEvents=getHeppyOption("selectEvents","")
keepGenPart=getHeppyOption("keepGenPart",False)
runSMS = getHeppyOption("runSMS",False)

sample = "main"
#if runDataQCD or runFRMC: sample="qcd1l"
#sample = "z3l"

# Skimming
ttHLepSkim.minLeptons = 2
ttHLepSkim.maxLeptons = 999
ttHJetMETSkim.metCut    = 50
susyCoreSequence.append(ttHJetMETSkim)
# susyCoreSequence.insert(susyCoreSequence.index(ttHLepSkim)+1,globalSkim)
#     susyCoreSequence.remove(ttHLepSkim)
#     globalSkim.selections=["2lep5","1lep5_1tau18", "2tau18","1lep5[maxObj1]"]
# #   [ lambda ev: 2<=sum([(lep.miniRelIso<0.4) for lep in ev.selectedLeptons]) ] 
# #   ["2lep5[os:!DS_TTW_RA5_sync]_1lep50"]#, "1lep5_1tau18", "2tau18","2lep5_1met50"]


# Run miniIso
lepAna.doMiniIsolation = True if run80X else "precomputed"
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
lepAna.doIsolationScan = False
lepAna.mu_isoCorr = "deltaBeta"

# Lepton Preselection
lepAna.inclusive_muon_pt  = 3
lepAna.loose_muon_pt  = 3
lepAna.inclusive_electron_pt  = 5
lepAna.loose_electron_pt  = 5
lepAna.loose_electron_id = "MVA_ID_nonIso_Fall17_SUSYVLooseFO" 
#isolation = "absIso04"
#isolation = None
#isolation = "miniIso"
isolation = "Iperbolic"


# Lepton-Jet Cleaning
jetAna.lepSelCut = lambda lep : False # no cleaning of jets with leptons
jetAnaScaleDown.lepSelCut = lambda lep : False # no cleaning of jets with leptons
jetAnaScaleUp.lepSelCut = lambda lep : False # no cleaning of jets with leptons
#in 2017 was:
#jetAna.cleanSelectedLeptons = False
#in 2016 was:
##jetAna.minLepPt = 20 
##jetAnaScaleUp.minLepPt = 20 
##jetAnaScaleDown.minLepPt = 20 
## otherwise with only absIso cut at 10 GeV and no relIso we risk cleaning away good jets

jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this
if not removeJecUncertainty:
    jetAna.addJECShifts = True
    jetAna.jetPtOrUpOrDnSelection = True 
    jetAnaScaleDown.copyJetsByValue = True # do not remove this
    metAnaScaleDown.copyMETsByValue = True # do not remove this
    jetAnaScaleUp.copyJetsByValue = True # do not remove this
    metAnaScaleUp.copyMETsByValue = True # do not remove this
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleDown)
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleUp)
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleDown)
    susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleUp)


if isolation == "miniIso": 
    lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4 and muon.sip3D() < 8
    lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4 and elec.sip3D() < 8
elif isolation == None:
    lepAna.loose_muon_isoCut     = lambda muon : True
    lepAna.loose_electron_isoCut = lambda elec : True
elif isolation == "absIso04": 
    lepAna.loose_muon_isoCut     = lambda muon : muon.relIso04*muon.pt() < 10 and muon.sip3D() < 8
    lepAna.loose_electron_isoCut = lambda elec : elec.relIso04*elec.pt() < 10 and elec.sip3D() < 8
elif isolation == "Iperbolic":
    lepAna.loose_muon_isoCut     = lambda muon : muon.relIso03*muon.pt() < (20+300/muon.pt()) and  abs(muon.ip3D()) < 0.0175 and muon.sip3D() < 2.5
    lepAna.loose_electron_isoCut = lambda elec : elec.relIso03*elec.pt() < (20+300/elec.pt()) and  abs(elec.ip3D()) < 0.0175 and elec.sip3D() < 2.5
else:
    # nothing to do, will use normal relIso03
    pass

# Switch off slow photon MC matching
photonAna.do_mc_match = False

# Loose Tau configuration
tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 2.3
tauAna.loose_decayModeID = "decayModeFindingNewDMs"
tauAna.loose_tauID = "decayModeFindingNewDMs"
tauAna.loose_vetoLeptons = False # no cleaning with leptons in production 
#jetAna.cleanJetsFromTaus = True
#jetAnaScaleUp.cleanJetsFromTaus = True
#jetAnaScaleDown.cleanJetsFromTaus = True


#-------- ADDITIONAL ANALYZERS -----------

## Adding LHE Analyzer for saving lheHT
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

# ## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
# susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
#                         ttHFatJetAna)
# susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
#                         ttHSVAna)
# susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna), 
#                         ttHHeavyFlavourHadronAna)

# ## Insert declustering analyzer
# from CMGTools.TTHAnalysis.analyzers.ttHDeclusterJetsAnalyzer import ttHDeclusterJetsAnalyzer
# ttHDecluster = cfg.Analyzer(
#     ttHDeclusterJetsAnalyzer, name='ttHDecluster',
#     lepCut     = lambda lep,ptrel : lep.pt() > 10,
#     maxSubjets = 6, # for exclusive reclustering
#     ptMinSubjets = 5, # for inclusive reclustering
#     drMin      = 0.2, # minimal deltaR(l,subjet) required for a successful subjet match
#     ptRatioMax = 1.5, # maximum pt(l)/pt(subjet) required for a successful match
#     ptRatioDiff = 0.1,  # cut on abs( pt(l)/pt(subjet) - 1 ) sufficient to call a match successful
#     drMatch     = 0.02, # deltaR(l,subjet) sufficient to call a match successful
#     ptRelMin    = 5,    # maximum ptRelV1(l,subjet) sufficient to call a match successful
#     prune       = True, # also do pruning of the jets 
#     pruneZCut       = 0.1, # pruning parameters (usual value in CMS: 0.1)
#     pruneRCutFactor = 0.5, # pruning parameters (usual value in CMS: 0.5)
#     verbose     = 0,   # print out the first N leptons
#     jetCut = lambda jet : jet.pt() > 20,
#     mcPartonPtCut = 20,
#     mcLeptonPtCut =  5,
#     mcTauPtCut    = 15,
#     )
# susyCoreSequence.insert(susyCoreSequence.index(ttHFatJetAna)+1, ttHDecluster)

for M in isoTrackAna, badMuonAna, badMuonAnaMoriond2017, badCloneMuonAnaMoriond2017, badChargedHadronAna:
    susyCoreSequence.remove(M)

from CMGTools.TTHAnalysis.analyzers.treeProducerSusyMultilepton import * 

_variablesToRemove = ['Flag_badMuonMoriond2017','Flag_badCloneMuonMoriond2017','badCloneMuonMoriond2017_maxPt','badNotCloneMuonMoriond2017_maxPt',
                      'nSoftBLoose25','nSoftBMedium25','nSoftBTight25','Flag_badChargedHadronFilter','Flag_badMuonFilter']
susyMultilepton_globalVariables = filter(lambda x: x.name not in _variablesToRemove, susyMultilepton_globalVariables)
del susyMultilepton_collections['ivf']

# Soft lepton MVA
ttHCoreEventAna.doLeptonMVASoft = False
#leptonTypeSusyExtraLight.addVariables([
#        NTupleVariable("mvaSoftT2tt",    lambda lepton : lepton.mvaValueSoftT2tt, help="Lepton MVA (Soft T2tt version)"),
#        NTupleVariable("mvaSoftEWK",    lambda lepton : lepton.mvaValueSoftEWK, help="Lepton MVA (Soft EWK version)"),
#        ])

if not removeJecUncertainty:
    susyMultilepton_globalObjects.update({
            "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
            "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
            })
#    susyMultilepton_collections.update({
#            "cleanJets_jecUp"       : NTupleCollection("Jet_jecUp",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC plus 1sigma)"),
#            "cleanJets_jecDown"     : NTupleCollection("Jet_jecDown",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC minus 1sigma)"),
#            "discardedJets_jecUp"   : NTupleCollection("DiscJet_jecUp", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC +1sigma)"),
#            "discardedJets_jecDown" : NTupleCollection("DiscJet_jecDown", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC -1sigma)"),
#            })

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

#Needed only if cleaning in production
#del treeProducer.collections["discardedLeptons"]

## histo counter
if not runSMS:
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer),
                            susyCounter)
    susyScanAna.doLHE=False # until a proper fix is put in the analyzer
else:
    susyScanAna.useLumiInfo=True
    susyScanAna.doLHE=True
    susyCounter.bypass_trackMass_check = False
    susyCounter.SMS_varying_masses=['genSusyMGluino','genSusyMNeutralino','genSusyMChargino','genSusyMNeutralino2', 'genSusyMStau', 'genSusyMSnuTau', 'genSusyMStop','genSusyMChargino2', 'genSusyMNeutralino3', 'genSusyMNeutralino4']
    if analysis in ['SOS']:
        susyCounter.SMS_varying_masses += ['genSusyMScan1', 'genSusyMScan2', 'genSusyMScan3', 'genSusyMScan4']
        #susyCounter.SMS_mass_1 = 'genSusyMChargino' ##ForTChiWZ
        #susyCounter.SMS_mass_2 = 'genSusyMNeutralino' ##ForTChiWZ
        susyCounter.SMS_mass_1 = 'genSusyMNeutralino2' ##ForSMS_N2C1/SMS_N2N1
        susyCounter.SMS_mass_2 = 'genSusyMNeutralino' ##ForSMS_N2C1/SMS_N2N1
        #susyCounter.SMS_mass_1 = 'genSusyMScan1' ##For higgsino pMSSM
        #susyCounter.SMS_mass_2 = 'genSusyMScan2' ##For higgsino pMSSM
        #susyCounter.SMS_mass_1 = 'genSusyMStop' ##ForT2tt
        #susyCounter.SMS_mass_2 = 'genSusyMNeutralino' ##ForT2tt
    susyCoreSequence.insert(susyCoreSequence.index(susyScanAna)+1,susyCounter)

# #additional MET quantities
# metAna.doTkMet = True
# treeProducer.globalVariables.append(NTupleVariable("met_trkPt", lambda ev : ev.tkMet.pt() if  hasattr(ev,'tkMet') else  0, help="tkmet p_{T}"))
# treeProducer.globalVariables.append(NTupleVariable("met_trkPhi", lambda ev : ev.tkMet.phi() if  hasattr(ev,'tkMet') else  0, help="tkmet phi"))

if not skipT1METCorr:
    if doMETpreprocessor: 
        print "WARNING: you're running the MET preprocessor and also Type1 MET corrections. This is probably not intended."
    jetAna.calculateType1METCorrection = True
    metAna.recalibrate = "type1"
    jetAnaScaleUp.calculateType1METCorrection = True
    metAnaScaleUp.recalibrate = "type1"
    jetAnaScaleDown.calculateType1METCorrection = True
    metAnaScaleDown.recalibrate = "type1"


#ISR jet collection
if not runData:
    from CMGTools.TTHAnalysis.analyzers.nIsrAnalyzer import NIsrAnalyzer
    nIsrAnalyzer = cfg.Analyzer(
        NIsrAnalyzer, name='nIsrAnalyzer',
    )
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1,nIsrAnalyzer)
    treeProducer.globalVariables.append(NTupleVariable("nISR", lambda ev: ev.nIsr, int, mcOnly=True, help="number of ISR jets according to SUSY recommendations"))


#-------- SAMPLES AND TRIGGERS -----------


from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import * #Commented out those that were included in the SusyMultilep config from DATA2016 trigger file
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleMuSS' : triggers_mumu_ss,
    'DoubleMuNoIso' : triggers_mumu_noniso, #+ triggers_mu27tkmu8,
    'DoubleEl' : triggers_ee, #+ triggers_doubleele33 + triggers_doubleele33_MW,
    'MuEG'     : triggers_mue, #+ triggers_mu30ele30,
    'DoubleMuHT' : triggers_mumu_ht,
    'DoubleElHT' : triggers_ee_ht,
    'MuEGHT' : triggers_mue_ht,
    'TripleEl' : triggers_3e,
    'TripleMu' : triggers_3mu,
    #'TripleMuA' : triggers_3mu_alt,
    'DoubleMuEl' : triggers_2mu1e,
    'DoubleElMu' : triggers_2e1mu,
    'SingleMu' : triggers_1mu_iso,
    #'SingleEl'     : triggers_1e,
    'SingleEl'     : triggers_1e_iso,
    'SOSHighMET' : triggers_SOS_highMET, 
    'SOSDoubleMuLowMET' : triggers_SOS_doublemulowMET, 
    #'SOSTripleMu' : triggers_SOS_tripleMu, 
    #'LepTau' : triggers_leptau,
    #'MET' : triggers_metNoMu90_mhtNoMu90 + triggers_htmet,
    #'HT' : triggers_pfht    
    #'MonoJet80MET90' : triggers_Jet80MET90,
    #'MonoJet80MET120' : triggers_Jet80MET120,
    #'METMu5' : triggers_MET120Mu5,
}
triggerFlagsAna.unrollbits = True
triggerFlagsAna.saveIsUnprescaled = True
triggerFlagsAna.checkL1Prescale = True


if runSMS:
    #if ttHLepSkim in susyCoreSequence: susyCoreSequence.remove(ttHLepSkim)
    #if ttHJetMETSkim in susyCoreSequence: susyCoreSequence.remove(ttHJetMETSkim)
    susyCoreSequence.remove(triggerFlagsAna)
    susyCoreSequence.remove(triggerAna)
    susyCoreSequence.remove(eventFlagsAna)
    

#from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
#from CMGTools.RootTools.samples.samples_13TeV_signals import *
#from CMGTools.RootTools.samples.samples_13TeV_80X_susySignalsPriv import *
#from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall17MiniAOD import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2017 import *
from CMGTools.RootTools.samples.configTools import printSummary, configureSplittingFromTime, cropToLumi, prescaleComponents, insertEventSelector, mergeExtensions
from CMGTools.RootTools.samples.autoAAAconfig import *

selectedComponents = [TTLep_pow]

#From samples_13TeV_signals
#samples_scans = [SMS_TChiWZ, SMS_T2ttDiLep_mStop_10to80] 
#samples_higgsinos = [SMS_N2C1_Higgsino,SMS_N2N1_Higgsino] 
#samples_privateSig = Higgsino 
#samples_pMSSM = [pMSSM_Higgsino]
#From samples_13TeV_RunIISummer16MiniAODv2
#samples_mainBkg = [TTJets_DiLepton, TTJets_DiLepton_ext, TBar_tWch_ext, T_tWch_ext] + DYJetsM5to50HT + DYJetsM50HT 
#samples_mainBkgVV = [VVTo2L2Nu, VVTo2L2Nu_ext]
#samples_fakesBkg = [TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromT] + WJetsToLNuHT 
#samples_rareBkg = [WZTo3LNu, WWToLNuQQ, WZTo1L3Nu, WZTo1L1Nu2Q, ZZTo2L2Q, ZZTo4L, WWW, WZZ, WWZ, ZZZ, T_tch_powheg, TBar_tch_powheg, TToLeptons_sch_amcatnlo, WWDouble, WpWpJJ, TTWToLNu_ext, TTZToLLNuNu_ext, TTZToLLNuNu_m1to10, TTGJets, WGToLNuG_amcatnlo_ext, ZGTo2LG_ext, TGJets] #WZTo2L2Q,WGToLNuG, #still missing

#From samples_13TeV_RunIIFall17MiniAOD (some samples still missing)
samples_mainBkg =  [T_tWch_noFullyHad, TBar_tWch_noFullyHad] + DYJetsToLLM4to50HT + DYJetsToLLM50HT + [TTJets_DiLepton] #TTJets_DiLepton not yet finished
samples_mainBkgVV = [WWTo2L2Nu,ZZTo2L2Nu] #[VVTo2L2Nu, VVTo2L2Nu_ext]
samples_fakesBkg = [TTJets_SingleLeptonFromT, TTJets_SingleLeptonFromTbar] + WJetsToLNuHT 
samples_rareBkg = [WZTo3LNu_fxfx, WWToLNuQQ, WZTo1L1Nu2Q, ZZTo4L, WWW_4F, WZZ, WWZ_4F, ZZZ, T_tch, TBar_tch, T_sch_lep, WWTo2L2Nu_DPS_hpp, TTWToLNu_fxfx, TTZToLLNuNu_amc, TTZToLLNuNu_m1to10, TTGJets, TGJets_lep] #WZTo3LNu, WZTo1L3Nu, , ZZTo2L2Q, WpWpJJ,  WGToLNuG_amcatnlo_ext, ZGTo2LG_ext, WZTo2L2Q,WGToLNuG, #still missing

samples_mainBkg = [DYJetsToLL_M5to50_LO]#DYJetsToLL_M50_LO,DYJetsToLL_M50_LO_ext,DYJetsToLL_M10to50_LO]

cropToLumi([WWW_4F, WZZ, WWZ_4F, ZZZ, WWToLNuQQ, WZTo1L1Nu2Q, TTWToLNu_fxfx, TTZToLLNuNu_amc, TTZToLLNuNu_m1to10],200)
configureSplittingFromTime(samples_fakesBkg,50,3)
configureSplittingFromTime(samples_mainBkg,50,3)
configureSplittingFromTime(samples_rareBkg,100,3)

selectedComponents = WJetsToLNuHT#samples_mainBkg#samples_fakesBkg#samples_rareBkg + samples_mainBkg + samples_mainBkgVV
#selectedComponents = WJetsToLNuHT

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

    json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt' # full 2017 dataset, EOY rereco, 41.4/fb

    for era in 'BCDEF': dataChunks.append((json,filter(lambda dset: 'Run2017'+era in dset.name,dataSamples_31Mar2018),'2017'+era,[],False))

    DatasetsAndTriggers = []
    selectedComponents = [];
    exclusiveDatasets = True; # this will veto triggers from previous PDs in each PD, so that there are no duplicate events
 
    DatasetsAndTriggers.append( ("MET", triggers_SOS_highMET) )
    DatasetsAndTriggers.append( ("DoubleMuon", triggers_SOS_doublemulowMET + triggers_mumu_iso + triggers_3mu) )
    #DatasetsAndTriggers.append( ("MET", triggers_Jet80MET90 + triggers_Jet80MET120 + triggers_MET120Mu5 ) )
    #DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_noniso) )
    #DatasetsAndTriggers.append( ("SingleElectron", triggers_1e ) )
    # Cristina: questo qua sotto serve solo per fake-rate maps, ma non penso che quando si facciano trigger maps per sos si usi questo cfg
    # if sample == "z3l":
    #     DatasetsAndTriggers = []; exclusiveDatasets = False
    #     DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso) )
    #     DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee) )
    # elif sample == "qcd1l":
    #     DatasetsAndTriggers = []; exclusiveDatasets = False
    #     DatasetsAndTriggers.append( ("DoubleMuon", ["HLT_Mu8_v*", "HLT_Mu3_PFJet40_v*"]) )
    #     DatasetsAndTriggers.append( ("DoubleEG",   ["HLT_Ele%d_CaloIdM_TrackIdM_PFJet30_v*" % pt for pt in (8,12)]) )
    #     DatasetsAndTriggers.append( ("JetHT",   triggers_FR_jet) )


    ###### Cristina: La parte qua sotto e' copiata da ttH_cfg, e sotto commentata c'e' la versione in susyMultilep. non sono sicura di capire tutte le differenze
    for json,dsets,short,run_ranges,useAAA in dataChunks:
        if len(run_ranges)==0: run_ranges=[None]
        vetos = []
        for pd,triggers in DatasetsAndTriggers:
            for run_range in run_ranges:
                label = ""
                if run_range!=None:
                    label = "_runs_%d_%d" % run_range if run_range[0] != run_range[1] else "run_%d" % (run_range[0],)
                _ds = filter(lambda dset : re.match('%s_.*'%pd,dset.name),dsets)
                for idx,_comp in enumerate(_ds):
                    compname = pd+"_"+short+label
                    if (len(_ds)>1): compname += '_ds%d'%(idx+1)
                    comp = kreator.makeDataComponent(compname, 
                                                     _comp.dataset,
                                                     "CMS", ".*root", 
                                                     json=json, 
                                                     run_range=(run_range if "PromptReco" not in _comp.dataset else None), 
                                                     triggers=triggers[:], vetoTriggers = vetos[:],
                                                     useAAA=useAAA)
                    if "PromptReco" in comp.dataset:
                        from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
                        filterComponent(comp, verbose=0)
                    #print "Will process %s (%d files)" % (comp.name, len(comp.files))
                    comp.splitFactor = len(comp.files)/8# if 'Single' not in comp.name else len(comp.files)/16 # numbers yet to be tuned for 2017
                    comp.fineSplitFactor = 1
                    selectedComponents.append( comp )
            if exclusiveDatasets: vetos += triggers
    if json is None:
        susyCoreSequence.remove(jsonAna)
    if runDataQCD: # for fake rate measurements in data
         configureSplittingFromTime(selectedComponents, 3.5, 2, maxFiles=15)
    else:
        for comp in selectedComponents:
            comp.splitFactor = int(ceil(len(comp.files)/3))
#        configureSplittingFromTime(filter(lambda x: 'MET' in x.name,selectedComponents),50,5)
#        configureSplittingFromTime(filter(lambda x: 'DoubleMuon' in x.name,selectedComponents),50,5)

    ###### 
    # for json,processing,short,run_ranges,useAAA in dataChunks:
    #     if len(run_ranges)==0: run_ranges=[None]
    #     vetos = []
    #     for pd,triggers in DatasetsAndTriggers:
    #         for run_range in run_ranges:
    #             label = ""
    #             if run_range!=None:
    #                 label = "_runs_%d_%d" % run_range if run_range[0] != run_range[1] else "run_%d" % (run_range[0],)
    #             compname = pd+"_"+short+label
    #             if ((compSelection and not re.search(compSelection, compname)) or
    #                 (compVeto      and     re.search(compVeto,      compname))):
    #                     print "Will skip %s" % (compname)
    #                     continue
    #             myprocessing = processing
    #             comp = kreator.makeDataComponent(compname, 
    #                                              "/"+pd+"/"+myprocessing+"/MINIAOD", 
    #                                              "CMS", ".*root", 
    #                                              json=json, 
    #                                              run_range=(run_range if "PromptReco" not in myprocessing else None), 
    #                                              triggers=triggers[:], vetoTriggers = vetos[:],
    #                                              useAAA=useAAA)
    #             if "PromptReco" in myprocessing:
    #                 from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
    #                 filterComponent(comp, verbose=1)
    #             print "Will process %s (%d files)" % (comp.name, len(comp.files))
    #             comp.splitFactor = len(comp.files)/8
    #             comp.fineSplitFactor = 1
    #             selectedComponents.append( comp )
    #         if exclusiveDatasets: vetos += triggers
    # if json is None:
    #     susyCoreSequence.remove(jsonAna)

#printSummary(selectedComponents)


###### Cristina: inoltre in SUSYMultilep c'era anche questa parte, che non c'e' piu' in ttH_cfg. a cosa serve?
# if True and runData:
#     from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
#     for c in selectedComponents:
#         printnewsummary = False
#         c.splitFactor = len(c.files)/3
#         if "PromptReco" in c.name:
#             printnewsummary = True
#             filterComponent(c, 1)
#             c.splitFactor = len(c.files)/3
#     if printnewsummary: printSummary(selectedComponents)





#### The following is an old set up for SOS FR Maps

# if runFRMC: 
#     QCD_Mu5 = [ QCD_Pt20to30_Mu5, QCD_Pt30to50_Mu5, QCD_Pt50to80_Mu5, QCD_Pt80to120_Mu5, QCD_Pt120to170_Mu5 ]
# #    QCDPtEMEnriched = [ QCD_Pt20to30_EMEnriched, QCD_Pt30to50_EMEnriched, QCD_Pt50to80_EMEnriched, QCD_Pt80to120_EMEnriched, QCD_Pt120to170_EMEnriched ]
# #    QCDPtbcToE = [ QCD_Pt_20to30_bcToE, QCD_Pt_30to80_bcToE, QCD_Pt_80to170_bcToE ]
# #    QCDHT = [ QCD_HT100to200, QCD_HT200to300, QCD_HT300to500, QCD_HT500to700 ]
# #    selectedComponents = [QCD_Mu15] + QCD_Mu5 + QCDPtEMEnriched + QCDPtbcToE + [WJetsToLNu_LO,DYJetsToLL_M10to50,DYJetsToLL_M50]
# #    selectedComponents = [ QCD_Pt_170to250_bcToE, QCD_Pt120to170_EMEnriched, QCD_Pt170to300_EMEnriched ]
# #    selectedComponents = [QCD_Mu15]

# #    selectedComponents = [TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromTbar]

#     selectedComponents = [QCD_Mu15] + QCD_Mu5 + [WJetsToLNu,DYJetsToLL_M10to50,DYJetsToLL_M50] 

#     time = 5.0
#     configureSplittingFromTime([WJetsToLNu],20,time)
# #    configureSplittingFromTime([WJetsToLNu_LO],20,time)
#     configureSplittingFromTime([DYJetsToLL_M10to50],10,time)
#     configureSplittingFromTime([DYJetsToLL_M50],30,time)
#     configureSplittingFromTime([QCD_Mu15]+QCD_Mu5,70,time)
# #    configureSplittingFromTime(QCDPtbcToE,50,time)
# #    configureSplittingFromTime(QCDPtEMEnriched,25,time)
# #    configureSplittingFromTime([ QCD_HT100to200, QCD_HT200to300 ],10,time)
# #    configureSplittingFromTime([ QCD_HT300to500, QCD_HT500to700 ],15,time)
# #    configureSplittingFromTime([ QCD_Pt120to170_EMEnriched,QCD_Pt170to300_EMEnriched ], 15, time)
# #    configureSplittingFromTime([ QCD_Pt_170to250_bcToE ], 30, time)
#     if runQCDBM:
#         configureSplittingFromTime([QCD_Mu15]+QCD_Mu5,15,time)
#     for c in selectedComponents:
#         c.triggers = []
#         c.vetoTriggers = [] 
#     #printSummary(selectedComponents)

# if runFRMC or runDataQCD:
#     susyScanAna.useLumiInfo = False
#     if analysis!='susy':
#         ttHLepSkim.minLeptons=1
#     else:
#         globalSkim.selection = ["1lep5"]
#     if ttHJetMETSkim in susyCoreSequence: susyCoreSequence.remove(ttHJetMETSkim)
#     if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
#     if runDataQCD:
#         FRTrigs = triggers_FR_1mu_iso + triggers_FR_1mu_noiso + triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g + triggers_FR_jet + triggers_FR_muNoIso
#         for t in FRTrigs:
#             tShort = t.replace("HLT_","FR_").replace("_v*","")
#             triggerFlagsAna.triggerBits[tShort] = [ t ]
#     treeProducer.collections = {
#         "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
#         "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
#         "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
#         "discardedJets"    : NTupleCollection("DiscJet", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning"),
#         "selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
#         "otherTaus"       : NTupleCollection("TauOther",  tauTypeSusy, 8, help="Taus after the preselection not selected"),
#     }
#     if True: # 
#         from CMGTools.TTHAnalysis.analyzers.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
#         ttHLepQCDFakeRateAna = cfg.Analyzer(ttHLepQCDFakeRateAnalyzer, name="ttHLepQCDFakeRateAna",
#             jetSel = lambda jet : jet.pt() > (25 if abs(jet.eta()) < 2.4 else 30),
#             pairSel = lambda lep, jet: deltaR(lep.eta(),lep.phi(), jet.eta(), jet.phi()) > 0.7,
#         )
#         susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, ttHLepQCDFakeRateAna)
#         leptonTypeSusyExtraLight.addVariables([
#             NTupleVariable("awayJet_pt", lambda x: x.awayJet.pt() if x.awayJet else 0, help="pT of away jet"),
#             NTupleVariable("awayJet_eta", lambda x: x.awayJet.eta() if x.awayJet else 0, help="eta of away jet"),
#             NTupleVariable("awayJet_phi", lambda x: x.awayJet.phi() if x.awayJet else 0, help="phi of away jet"),
#             NTupleVariable("awayJet_btagCSV", lambda x: x.awayJet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.awayJet else 0, help="b-tag disc of away jet"),
#             NTupleVariable("awayJet_mcFlavour", lambda x: x.awayJet.partonFlavour() if x.awayJet else 0, int, mcOnly=True, help="pT of away jet"),
#         ])
#     if True: # drop events that don't have at least one lepton+jet pair (reduces W+jets by ~50%)
#         ttHLepQCDFakeRateAna.minPairs = 1
#     if True: # fask skim 
#         from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
#         fastSkim = cfg.Analyzer(
#             ttHFastLepSkimmer, name="ttHFastLepSkimmer1lep",
#             muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
#             electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
#             minLeptons = 1,
#         )
#         susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim)
#         susyCoreSequence.remove(lheWeightAna)
#         susyCounter.doLHE = False
#     if runQCDBM:
#         fastSkimBM = cfg.Analyzer(
#             ttHFastLepSkimmer, name="ttHFastLepSkimmerBM",
#             muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 8,
#             electrons = 'slimmedElectrons', eleCut = lambda ele : False,
#             minLeptons = 1,
#         )
#         fastSkim.minLeptons = 2
#         ttHLepSkim.maxLeptons = 1
#         susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, fastSkimBM)
#         from PhysicsTools.Heppy.analyzers.core.TriggerMatchAnalyzer import TriggerMatchAnalyzer
#         trigMatcher1Mu2J = cfg.Analyzer(
#             TriggerMatchAnalyzer, name="trigMatcher1Mu",
#             label='1Mu',
#             processName = 'PAT',
#             fallbackProcessName = 'RECO',
#             unpackPathNames = True,
#             trgObjSelectors = [ lambda t : t.path("HLT_Mu8_v*",1,0) or t.path("HLT_Mu17_v*",1,0) or t.path("HLT_Mu22_v*",1,0) or t.path("HLT_Mu27_v*",1,0) or t.path("HLT_Mu45_eta2p1_v*",1,0) or t.path("HLT_L2Mu10_v*",1,0) ],
#             collToMatch = 'cleanJetsAll',
#             collMatchSelectors = [ lambda l,t : True ],
#             collMatchDRCut = 0.4,
#             univoqueMatching = True,
#             verbose = False,
#             )
#         susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, trigMatcher1Mu2J)
#         ttHLepQCDFakeRateAna.jetSel = lambda jet : jet.pt() > 25 and abs(jet.eta()) < 2.4 and jet.matchedTrgObj1Mu
# if sample == "z3l":
#     ttHLepSkim.minLeptons = 3
#     if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
#     treeProducer.collections = {
#         "selectedLeptons" : NTupleCollection("LepGood", leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
#         "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
#     }
#     from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
#     fastSkim = cfg.Analyzer(
#         ttHFastLepSkimmer, name="ttHFastLepSkimmer3lep",
#         muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
#         electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
#         minLeptons = 3,
#     )
#     fastSkim2 = cfg.Analyzer(
#         ttHFastLepSkimmer, name="ttHFastLepSkimmer2lep",
#         muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 10 and mu.isLooseMuon(),
#         electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 10,
#         minLeptons = 2,
#     )
#     susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim)
#     susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim2)
#     susyCoreSequence.remove(lheWeightAna)
#     susyCoreSequence.remove(ttHJetMETSkim)
#     susyCounter.doLHE = False
#     if not runData:
#         selectedComponents = [DYJetsToLL_M50_LO]
#         #prescaleComponents([DYJetsToLL_M50_LO], 2)
#         #configureSplittingFromTime([DYJetsToLL_M50_LO],4,1.5)
#         selectedComponents = [WZTo3LNu,ZZTo4L]
#         cropToLumi([WZTo3LNu,ZZTo4L], 50)
#         #configureSplittingFromTime([WZTo3LNu,ZZTo4L],20,1.5)
#     else:
#         if True:
#             from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
#             for c in selectedComponents:  
#                 if "PromptReco" in c.name: filterComponent(c, 1)
#         if analysis == 'SOS':
#             configureSplittingFromTime(selectedComponents,10,2)

if runSMS:
    jetAna.mcGT = "Spring16_FastSimV1_MC" #To be updated to 2017 JEC for FastSIM
    jetAna.applyL2L3Residual = False
    jetAnaScaleUp.applyL2L3Residual = False
    jetAnaScaleDown.applyL2L3Residual = False

if removeJetReCalibration:
    jetAna.recalibrateJets = False
    jetAnaScaleUp.recalibrateJets = False
    jetAnaScaleDown.recalibrateJets = False

if getHeppyOption("noLepSkim",False):
    if globalSkim in sequence:
        globalSkim.selection = []
    if ttHLepSkim in sequence:
        ttHLepSkim.minLeptons=0 

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
    from CMGTools.Production.promptRecoRunRangeFilter import filterWithCollection
    for comp in selectedComponents:
        if comp.isData: comp.files = filterWithCollection(comp.files, [274315,275658,276363,276454])
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
elif test == "ewkinosync":
    comp = cfg.MCComponent( files = ["root://eoscms.cern.ch//store/mc/RunIIFall15MiniAODv2/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/60000/14C51DB0-D6B8-E511-8D9B-8CDCD4A9A484.root"], name="TTW_EWK_sync" )
    comp.triggers = []
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [comp]
    sequence.remove(jsonAna)
elif test == "ra5-sync-mc":
    comp = cfg.MCComponent( files = ["root://eoscms.cern.ch//store/mc/RunIISpring16MiniAODv1/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/00000/6E02CA07-BA02-E611-A59E-14187741208F.root"], name="TTW_RA5_sync" )
    comp.triggers = []
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    selectedComponents = [ comp ]
    sequence.remove(jsonAna)
elif test == "tau-sync":
    comp = cfg.MCComponent( files = [ "root://eoscms.cern.ch//store/mc/RunIISpring16MiniAODv2/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/50000/8E84F4BB-B620-E611-BBD8-B083FECFF2BF.root"], name="TTW_Tau" )
    comp.triggers = []
    comp.splitFactor = 1
    comp.fineSplitFactor = 6
    selectedComponents = [ comp ]
    sequence.remove(jsonAna)
    ttHLepSkim.minLeptons = 0
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
elif test == '94X-MC':
    print "=================================dwdwdwdwd======"
    what = getHeppyOption("sample","TTLep")
    if what == "TTLep":
        TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
        selectedComponents = [ TTLep_pow ]
        comp = selectedComponents[0]
        comp.triggers = []
        comp.files = [ '/store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
        tmpfil = os.path.expandvars("/tmp/$USER/3CC234EB-44E0-E711-904F-FA163E0DF774.root")
        if not os.path.exists(tmpfil):
            os.system("xrdcp root://cms-xrd-global.cern.ch/%s %s" % (comp.files[0],tmpfil))
        comp.files = [ tmpfil ]
        if not getHeppyOption("single"): comp.fineSplitFactor = 4
    else: raise RuntimeError, "Unknown MC sample: %s" % what
elif test == '80X-Data':
    what = getHeppyOption("sample","ZLL")
    if what == "ZLL":
        json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Final/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
        DoubleMuon = kreator.makeDataComponent("DoubleMuon_Run2016H_run283885", "/DoubleMuon/Run2016H-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (283885,283885), triggers = triggers_mumu)
        DoubleEG = kreator.makeDataComponent("DoubleEG_Run2016H_run283885", "/DoubleEG/Run2016H-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (283885,283885), triggers = triggers_ee)
        DoubleMuon.files = [ 'root://eoscms//eos/cms/store/data/Run2016H/DoubleMuon/MINIAOD/PromptReco-v2/000/283/885/00000/5A21CC75-D09D-E611-BFDC-FA163E163D77.root' ]
        DoubleEG.files = [ 'root://eoscms//eos/cms/store/data/Run2016H/DoubleEG/MINIAOD/PromptReco-v2/000/283/885/00000/743981FC-949D-E611-836E-FA163EC09DF2.root' ]
        selectedComponents = [ DoubleMuon, DoubleEG ]
    elif what == "MET":
        json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Final/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
        MET = kreator.makeDataComponent("MET_Run2016H_run283885", "/MET/Run2016H-PromptReco-v2/MINIAOD", "CMS", ".*root", run_range = (283885,283885), triggers = triggers_SOS_highMET)
        MET.files = [ 'root://eoscms//eos/cms/store/data/Run2016H/MET/MINIAOD/PromptReco-v2/000/283/885/00000/92E8E127-A59D-E611-83F2-02163E01187D.root' ]
        selectedComponents = [ MET ]
    elif what == "SingleMuon":
        SingleMuon = kreator.makeDataComponent("SingleMuon_Run2016H_run281693","/SingleMuon/Run2016H-PromptReco-v2/MINIAOD","CMS",".*root", run_range=(281680, 281700), triggers = triggers_1mu_iso)
        DoubleMuon.files = [ 'root://eoscms//eos/cms/store/data/Run2016B/DoubleMuon/MINIAOD/PromptReco-v2/000/274/315/00000/A287989F-E129-E611-B5FB-02163E0142C2.root' ]
        selectedComponents = [ SingleMuon ]
    for comp in selectedComponents:
        comp.json = json
        tmpfil = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(comp.files[0]))
        if not os.path.exists(tmpfil): os.system("xrdcp %s %s" % (comp.files[0],tmpfil)) 
        if not os.path.exists(tmpfil): os.system("xrdcp %s %s" % (comp.files[0],tmpfil))
        comp.files = [tmpfil]
        comp.splitFactor = 1
        comp.fineSplitFactor = 4
elif test == '94X-Data':
    what = getHeppyOption("sample","DoubleMuon")
    if what == "DoubleMuon":
        json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        DoubleMuon = kreator.makeDataComponent("DoubleMuon_Run2017C_run299649", "/DoubleMuon/Run2017C-17Nov2017-v1/MINIAOD", "CMS", ".*root", run_range = (299649,299649), triggers = [])
        DoubleMuon.files = [ 'root://eoscms//eos/cms/store/data/Run2017C/DoubleMuon/MINIAOD/17Nov2017-v1/50000/00519DC1-7ED3-E711-96E1-008CFAFBE5E0.root'  ]
        selectedComponents = [ DoubleMuon ]
    for comp in selectedComponents:
        comp.json = json
        tmpfil = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(comp.files[0]))
        if not os.path.exists(tmpfil): os.system("xrdcp %s %s" % (comp.files[0],tmpfil)) 
        comp.files = [tmpfil]
        comp.splitFactor = 1
        if not getHeppyOption("single"): comp.fineSplitFactor = 4
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
if not getHeppyOption("keepLHEweights",False):
    if "LHE_weights" in treeProducer.collections: treeProducer.collections.pop("LHE_weights")
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
