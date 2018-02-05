

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
runQCDBM = getHeppyOption("runQCDBM",False)
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

sample = "main"
#if runDataQCD or runFRMC: sample="qcd1l"
#sample = "z3l"

if analysis not in ['ttH','susy','SOS']: raise RuntimeError, 'Analysis type unknown'
print 'Using analysis type: %s'%analysis

# Lepton Skimming
ttHLepSkim.minLeptons = 2
ttHLepSkim.maxLeptons = 999

#isotrackAnalyzer mode
isoTrackAna.useLegacy2016=False

if analysis=='susy':
    susyCoreSequence.insert(susyCoreSequence.index(ttHLepSkim)+1,globalSkim)
    susyCoreSequence.remove(ttHLepSkim)
    globalSkim.selections=["2lep5","1lep5_1tau18", "2tau18","1lep5[maxObj1]"]
#   [ lambda ev: 2<=sum([(lep.miniRelIso<0.4) for lep in ev.selectedLeptons]) ] 
#   ["2lep5[os:!DS_TTW_RA5_sync]_1lep50"]#, "1lep5_1tau18", "2tau18","2lep5_1met50"]

# Run miniIso
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.miniIsolationVetoLeptons = None # use 'inclusive' to veto inclusive leptons and their footprint in all isolation cones
lepAna.doIsolationScan = False

# Lepton Preselection
lepAna.loose_electron_id = "MVA_ID_NonTrig_Spring16_VLooseIdEmu"
isolation = "miniIso"

jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this

if analysis=='susy':
    jetAna.cleanJetsFromLeptons=False
    jetAna.cleanSelectedLeptons=True
    jetAna.storeLowPtJets=True
    jetAna.jetEtaCentral = jetAna.jetEta
    jetAna.mcGT="Spring16_25nsV8_MC"    
    jetAna.dataGT   = "Spring16_25nsV8BCD_DATA Spring16_25nsV8E_DATA Spring16_25nsV8F_DATA Spring16_25nsV8_DATA"
    jetAna.runsDataJEC   = [276811, 277420, 278802]
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
    if analysis=='susy':
        jetAnaScaleDown.cleanJetsFromLeptons=False
        jetAnaScaleDown.cleanSelectedLeptons=True
        jetAnaScaleDown.storeLowPtJets=True
        jetAnaScaleDown.jetEtaCentral = jetAnaScaleDown.jetEta
        jetAnaScaleUp.cleanJetsFromLeptons=False
        jetAnaScaleUp.cleanSelectedLeptons=True
        jetAnaScaleUp.storeLowPtJets=True
        jetAnaScaleUp.jetEtaCentral = jetAnaScaleUp.jetEta
        jetAnaScaleDown.mcGT="Spring16_25nsV8_MC"    
        jetAnaScaleDown.dataGT   = "Spring16_25nsV8BCD_DATA Spring16_25nsV8E_DATA Spring16_25nsV8F_DATA Spring16_25nsV8_DATA"
        jetAnaScaleDown.runsDataJEC   = [276811, 277420, 278802]
        jetAnaScaleUp.mcGT="Spring16_25nsV8_MC"    
        jetAnaScaleUp.dataGT   = "Spring16_25nsV8BCD_DATA Spring16_25nsV8E_DATA Spring16_25nsV8F_DATA Spring16_25nsV8_DATA"
        jetAnaScaleUp.runsDataJEC   = [276811, 277420, 278802]


if analysis in ['SOS']:
## -- SOS preselection settings ---

    lepAna.doDirectionalIsolation = [0.3,0.4]
    lepAna.doFixedConeIsoWithMiniIsoVeto = True

    # Lepton Skimming
    ttHLepSkim.minLeptons = 2
    ttHLepSkim.maxLeptons = 999
    
#    # Jet-Met Skimming
#    ttHJetMETSkim.jetPtCuts = [0,]
    ttHJetMETSkim.metCut    = 50
    susyCoreSequence.append(ttHJetMETSkim)

    # Lepton Preselection
    lepAna.inclusive_muon_pt  = 3
    lepAna.loose_muon_pt  = 3
    lepAna.inclusive_electron_pt  = 5
    lepAna.loose_electron_pt  = 5
    #isolation = "absIso04"
    #isolation = None
    isolation = "Iperbolic"
    lepAna.loose_electron_id = "POG_MVA_ID_Spring15_NonTrig_VLooseIdEmu"

    # Lepton-Jet Cleaning
    jetAna.cleanSelectedLeptons = False
    #jetAna.minLepPt = 20 
    #jetAnaScaleUp.minLepPt = 20 
    #jetAnaScaleDown.minLepPt = 20 
    # otherwise with only absIso cut at 10 GeV and no relIso we risk cleaning away good jets

if isolation == "miniIso": 
    if (analysis=="ttH"):
        lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4 and muon.sip3D() < 8
        lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4 and elec.sip3D() < 8
    elif analysis=="susy":
        lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
        lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
    else: raise RuntimeError,'analysis field is not correctly configured'
elif isolation == None:
    lepAna.loose_muon_isoCut     = lambda muon : True
    lepAna.loose_electron_isoCut = lambda elec : True
elif isolation == "absIso04":
    lepAna.loose_muon_isoCut     = lambda muon : muon.RelIsoMIV04*muon.pt() < 10 and muon.sip3D() < 8
    lepAna.loose_electron_isoCut = lambda elec : elec.RelIsoMIV04*elec.pt() < 10 and elec.sip3D() < 8
elif isolation == "Iperbolic":
    lepAna.loose_muon_isoCut     = lambda muon : muon.relIso03*muon.pt() < (20+300/muon.pt()) and  abs(muon.ip3D()) < 0.0175 and muon.sip3D() < 2.5
    lepAna.loose_electron_isoCut = lambda elec : elec.relIso03*elec.pt() < (20+300/elec.pt()) and  abs(elec.ip3D()) < 0.0175 and elec.sip3D() < 2.5
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
tauAna.loose_decayModeID = "decayModeFindingNewDMs"
tauAna.loose_tauID = "decayModeFindingNewDMs"
#if analysis in ["ttH"]: #if cleaning jet-loose tau cleaning
#    jetAna.cleanJetsFromTaus = True
#    jetAnaScaleUp.cleanJetsFromTaus = True
#    jetAnaScaleDown.cleanJetsFromTaus = True


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
    ttHLepSkim.allowLepTauComb = True
    susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                            susyLeptonMatchAna)
    susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                            susyTauMatchAna)
    leptonTypeSusyExtraLight.addVariables([
            NTupleVariable("mcUCSXMatchId", lambda x : x.mcUCSXMatchId if hasattr(x,'mcUCSXMatchId') else -1, mcOnly=True, help="MC truth matching a la UCSX"),
            ])
    tauTypeSusy.addVariables([
            NTupleVariable("mcUCSXMatchId", lambda x : x.mcUCSXMatchId if hasattr(x,'mcUCSXMatchId') else -1, mcOnly=True, help="MC truth matching a la UCSX"),
            ])
    photonAna.do_mc_match = True
    susyMultilepton_collections.update({ # for conversion studies
            "selectedPhotons"    : NTupleCollection("PhoGood", photonTypeSusy, 10, help="Selected photons"),
            }) 
    del susyMultilepton_collections["discardedJets"]
    susyMultilepton_collections.update({"discardedJets"   : NTupleCollection("DiscJet", jetTypeSusySuperLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC)")
                                        })
    #keepJetVars=["pt","eta","phi","mass",
    #             #"etaetaMoment","phiphiMoment",
    #             "mcFlavour","partonFlavour",
    #             "btagCSV"]
    #for var in jetTypeSusyExtraLight.allVars(not runData):
    #    if var.name not in keepJetVars: 
    #        jetTypeSusyExtraLight.removeVariable(var)
    #jetTypeSusyExtraLight.addVariables([
    #        NTupleVariable("etaetaMoment", lambda x : x.etaetaMoment() if hasattr(x,'etaetaMoment') else -1, mcOnly=True, help="eta eta moment"),
    #        NTupleVariable("phiphiMoment", lambda x : x.phiphiMoment() if hasattr(x,'phiphiMoment') else -1, mcOnly=True, help="phi phi moment"),
    #        ])
elif analysis=='SOS':
    # Soft lepton MVA
    ttHCoreEventAna.doLeptonMVASoft = True
    leptonTypeSusyExtraLight.addVariables([
            NTupleVariable("mvaSoftT2tt",    lambda lepton : lepton.mvaValueSoftT2tt, help="Lepton MVA (Soft T2tt version)"),
            NTupleVariable("mvaSoftEWK",    lambda lepton : lepton.mvaValueSoftEWK, help="Lepton MVA (Soft EWK version)"),
            ])

# Spring16 electron MVA - follow instructions on pull request for correct area setup
leptonTypeSusy.addVariables([
        NTupleVariable("mvaIdSpring16HZZ",   lambda lepton : lepton.mvaRun2("Spring16HZZ") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, HZZ; 1 for muons"),
        NTupleVariable("mvaIdSpring16GP",   lambda lepton : lepton.mvaRun2("Spring16GP") if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID, Spring16, GeneralPurpose; 1 for muons"),
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
            "discardedJets_jecUp"   : NTupleCollection("DiscJet_jecUp", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC +1sigma)"),
            "discardedJets_jecDown" : NTupleCollection("DiscJet_jecDown", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning (JEC -1sigma)"),
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

if analysis in ['SOS']:
    del treeProducer.collections["discardedLeptons"]

## histo counter
if not runSMS:
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer),
                            susyCounter)
    susyScanAna.doLHE=False # until a proper fix is put in the analyzer
else:
    susyScanAna.useLumiInfo=True
    susyScanAna.doLHE=True
    susyCounter.bypass_trackMass_check = False
    susyCounter.SMS_varying_masses=['genSusyMGluino','genSusyMNeutralino','genSusyMChargino','genSusyMNeutralino2', 'genSusyMStau', 'genSusyMSnuTau', 'genSusyMStop']
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
    treeProducer.globalVariables.append(NTupleVariable("Flag_badChargedHadronFilter", lambda ev: ev.badChargedHadron, help="bad charged hadron filter decision"))
    treeProducer.globalVariables.append(NTupleVariable("Flag_badMuonFilter", lambda ev: ev.badMuon, help="bad muon filter decision"))


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


#ISR jet collection
if analysis=='SOS':
    from CMGTools.TTHAnalysis.analyzers.nIsrAnalyzer import NIsrAnalyzer
    nIsrAnalyzer = cfg.Analyzer(
        NIsrAnalyzer, name='nIsrAnalyzer',
    )
    susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1,nIsrAnalyzer)
    treeProducer.globalVariables.append(NTupleVariable("nISR", lambda ev: ev.nIsr, int, mcOnly=True, help="number of ISR jets according to SUSY recommendations"))


#-------- SAMPLES AND TRIGGERS -----------


from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *
triggerFlagsAna.triggerBits = {
    'DoubleMu' : triggers_mumu_iso,
    'DoubleMuSS' : triggers_mumu_ss,
    'DoubleMuNoIso' : triggers_mumu_noniso + triggers_mu27tkmu8,
    'DoubleEl' : triggers_ee + triggers_doubleele33 + triggers_doubleele33_MW,
    'MuEG'     : triggers_mue + triggers_mu30ele30,
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
    'SOSHighMET' : triggers_SOS_highMET,
    'SOSDoubleMuLowMET' : triggers_SOS_doublemulowMET,
    'SOSTripleMu' : triggers_SOS_tripleMu,
    'LepTau' : triggers_leptau,
    'MET' : triggers_metNoMu90_mhtNoMu90 + triggers_htmet,
    'HT' : triggers_pfht
    
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
    #ttHLepSkim.requireSameSignPair = False

#from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv1 import *
#from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_signals import *
from CMGTools.RootTools.samples.samples_13TeV_80X_susySignalsPriv import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *
from CMGTools.RootTools.samples.configTools import printSummary, configureSplittingFromTime, cropToLumi, prescaleComponents, insertEventSelector

selectedComponents = [TTLep_pow]

if analysis=='susy':
    samples = []#DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M10to50_LO, DYJetsToLL_M50_LO, GGHZZ4L, TBarToLeptons_tch_powheg, TBar_tWch, TGJets, TTGJets, TTJets, TTJets_DiLepton, TTJets_SingleLeptonFromT, 
               #TTJets_SingleLeptonFromTbar, TTTT, TT_pow_ext4, TToLeptons_sch_amcatnlo, TToLeptons_tch_amcatnlo, TToLeptons_tch_powheg, T_tWch, VHToNonbb, WGToLNuG, WJetsToLNu, WJetsToLNu_LO, 
               #WWDouble, WWTo2L2Nu, WWW, WWZ, WZTo3LNu, WZTo3LNu_amcatnlo, WZZ, WpWpJJ, ZGTo2LG, ZZTo4L, ZZZ, tZq_ll]
   
    samples_LHE = []#[TTHnobb_pow, TTLLJets_m1to10, TTWToLNu, TTW_LO, TTZToLLNuNu, TTZ_LO,]
    
    #samples_2l = [TTW_LO,TTZ_LO,WZTo3LNu_amcatnlo,DYJetsToLL_M10to50,DYJetsToLL_M50,WWTo2L2Nu,ZZTo2L2Q,WZTo3LNu,TTWToLNu,TTZToLLNuNu,TTJets_DiLepton,TTHnobb_mWCutfix_ext1,TTHnobb_pow]
    #samples_1l = [WJetsToLNu,TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromTbar,TBarToLeptons_tch_powheg,TToLeptons_sch_amcatnlo,TBar_tWch,T_tWch]
    
    if not getHeppyOption("keepLHEweights",False):
        selectedComponents = samples #samples_2l +samples_1l
    else:
        selectedComponents = samples_LHE

    if runSMS:
        selectedComponents=[TChiSlepSnu,T1tttt_2016,T5qqqqVV_2016]
        #ttHLepSkim.minLeptons = 0
        #ttHLepSkim.requireSameSignPair = False
        lheWeightAna.useLumiInfo=True
        susyScanAna.useLumiInfo=True
        for c in selectedComponents:
            c.splitFactor = len(c.files)

elif analysis=='SOS':

    selectedComponents = selectedComponents
    #samples_scans = [SMS_TChiWZ, SMS_T2ttDiLep_mStop_10to80] 
    #samples_privateSig = Higgsino 
    #samples_mainBkg = [TTJets_DiLepton, TBar_tWch_ext, T_tWch_ext] + DYJetsM5to50HT + DYJetsM50HT
    #samples_mainBkgVV = [VVTo2L2Nu, VVTo2L2Nu_ext]
    #samples_fakesBkg = [TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromT, WJetsToLNuHT] 
    #samples_rareBkg = [WZTo3LNu, WWToLNuQQ, WZTo1L3Nu, WZTo1L1Nu2Q, ZZTo2L2Q, ZZTo4L, WWW, WZZ, WWZ, ZZZ, T_tch_powheg, TBar_tch_powheg, TToLeptons_sch_amcatnlo, TTHnobb_pow, WWDouble, WpWpJJ, TTWToLNu_ext, TTZToLLNuNu_ext, TTZToLLNuNu_m1to10, TTGJets, WGToLNuG_amcatnlo_ext, ZGTo2LG_ext, TGJets] #WZTo2L2Q,WGToLNuG, #still missing
    #selectedComponents = samples_mainBkg + samples_mainBkgVV
    #configureSplittingFromTime(samples_mainBkg,150,3)

    

elif analysis=="ttH":
    selectedComponents = selectedComponents
#    samples_2l = [ TTWToLNu, TTZToLLNuNu, TTLLJets_m1to10, TTTT_ext, tZq_ll ] + TTHnobb_mWCutfix
#    samples_2l = [WJetsToLNu_LO, WJetsToLNu, DYJetsToLL_M10to50_LO, DYJetsToLL_M10to50, DYJetsToLL_M50, DYJetsToLL_M50_LO, TTJets, TT_pow, TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromT, TTJets_DiLepton, TBar_tWch, T_tWch, TToLeptons_tch_amcatnlo, TToLeptons_sch_amcatnlo, TTGJets, WGToLNuG, ZGTo2LG, TGJets, WWDouble, WpWpJJ, TTTT, VHToNonbb, GGHZZ4L,tZq_ll, WZTo3LNu, ZZTo4L, WWTo2L2Nu, WWW, WWZ, WZZ, ZZZ, TTHnobb_pow, TTW_LO, TTZ_LO, TTWToLNu, TTZToLLNuNu, TTLLJets_m1to10] + TTHnobb_mWCutfix
#    samples_1l = [QCD_Mu15] + QCD_Mu5 + [WJetsToLNu_LO,DYJetsToLL_M10to50_LO,DYJetsToLL_M50_LO,TT_pow] + QCDPtEMEnriched + QCDPtbcToE
#    selectedComponents = samples_2l
#    for comp in selectedComponents: comp.splitFactor = 200
#    printSummary(selectedComponents)
#    cropToLumi([TTTT_ext,tZq_ll],200)
#    cropToLumi(TTHnobb_mWCutfix,2000)
#    configureSplittingFromTime(samples_1l,50,3)
#    configureSplittingFromTime(samples_2l,100,3)

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


    #json = os.environ['CMSSW_BASE']+'/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt' # 36.15/fb
    json = os.environ['CMSSW_BASE']+ '/src/CMGTools/TTHAnalysis/data/json/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt' # 36.46 /fb

    #processing = "Run2016B-23Sep2016-v1"; short = "Run2016B_23Sep2016_v1"; run_ranges = [(272760,273017)]; useAAA=True; # -v2 starts from 272760 to 273017
    #dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016B-23Sep2016-v3"; short = "Run2016B_23Sep2016_v3"; run_ranges = [(273150,275376)]; useAAA=True; # -v3 starts from 273150 to 275376
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016C-23Sep2016-v1"; short = "Run2016C_23Sep2016_v1"; run_ranges = [(271036,284044)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016D-23Sep2016-v1"; short = "Run2016D_23Sep2016_v1"; run_ranges = [(271036,284044)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016E-23Sep2016-v1"; short = "Run2016E_23Sep2016_v1"; run_ranges = [(271036,284044)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016F-23Sep2016-v1"; short = "Run2016F_23Sep2016_v1"; run_ranges = [(271036,284044)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016G-23Sep2016-v1"; short = "Run2016G_23Sep2016_v1"; run_ranges = [(271036,284044)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    #run H ==============================================================================================================
    processing = "Run2016H-PromptReco-v1"; short = "Run2016H-PromptReco-v1"; run_ranges = [(281085,281201)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016H-PromptReco-v2"; short = "Run2016H-PromptReco-v2"; run_ranges = [(281207,284035)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))
    processing = "Run2016H-PromptReco-v3"; short = "Run2016H-PromptReco-v3"; run_ranges = [(284036,284044)]; useAAA=True;
    dataChunks.append((json,processing,short,run_ranges,useAAA))


    compSelection = ""; compVeto = ""
    DatasetsAndTriggers = []
    selectedComponents = [];
    exclusiveDatasets = True; # this will veto triggers from previous PDs in each PD, so that there are no duplicate events
 
    if analysis in ['SOS']:
        DatasetsAndTriggers.append( ("MET", triggers_SOS_highMET + triggers_SOS_doublemulowMET) )
        DatasetsAndTriggers.append( ("DoubleMuon", triggers_SOS_tripleMu) )
        #DatasetsAndTriggers.append( ("MET", triggers_Jet80MET90 + triggers_Jet80MET120 + triggers_MET120Mu5 ) )
        #DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_noniso) )
        #DatasetsAndTriggers.append( ("SingleElectron", triggers_1e ) )
        if sample == "z3l":
            DatasetsAndTriggers = []; exclusiveDatasets = False
            DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso) )
            DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee) )
        elif sample == "qcd1l":
            DatasetsAndTriggers = []; exclusiveDatasets = False
            DatasetsAndTriggers.append( ("DoubleMuon", ["HLT_Mu8_v*", "HLT_Mu3_PFJet40_v*"]) )
            DatasetsAndTriggers.append( ("DoubleEG",   ["HLT_Ele%d_CaloIdM_TrackIdM_PFJet30_v*" % pt for pt in (8,12)]) )
            DatasetsAndTriggers.append( ("JetHT",   triggers_FR_jet) )
    else:
        DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu_iso + triggers_mumu_ss + triggers_mu30tkmu11 + triggers_mumu_ht + triggers_3mu + triggers_3mu_alt + triggers_mu27tkmu8) )
        DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_doubleele33 + triggers_doubleele33_MW + triggers_ee_ht + triggers_3e) )
        DatasetsAndTriggers.append( ("MuonEG",     triggers_mue + triggers_mue_ht + triggers_2mu1e + triggers_2e1mu + triggers_mu30ele30) )
        if analysis=='susy':
            DatasetsAndTriggers.append( ("SingleMuon", triggers_leptau + triggers_1mu_iso + triggers_1mu_noniso) )
            DatasetsAndTriggers.append( ("SingleElectron", triggers_leptau + triggers_1e) )
            DatasetsAndTriggers.append( ("Tau", triggers_leptau + triggers_1mu_iso + triggers_1e) )
            #for edgeZ OS
            DatasetsAndTriggers.append( ("JetHT", triggers_pfht ) ) #triggerFlagsAna.triggerBits['htall']
            DatasetsAndTriggers.append( ("MET", triggers_htmet ) ) # triggerFlagsAna.triggerBits['htmet']
        else:
            DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu_iso + triggers_1mu_noniso) )
            DatasetsAndTriggers.append( ("SingleElectron", triggers_1e) )

        if runDataQCD: # for fake rate measurements in data
            FRTrigs_mu = triggers_FR_1mu_noiso
            FRTrigs_el = triggers_FR_1e_noiso
            DatasetsAndTriggers = [
                ("DoubleMuon", FRTrigs_mu ),
                ("DoubleEG",   FRTrigs_el ),
                #("JetHT",   triggers_FR_jet )
            ]
            exclusiveDatasets = False
        if runDataQCD and runQCDBM: # for fake rate measurements in data
            FRTrigs_mu = triggers_FR_1mu_iso + triggers_FR_1mu_noiso
            FRTrigs_el = triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
            DatasetsAndTriggers = [
                ("SingleMuon", triggers_FR_muNoIso ),
                #("DoubleMuon",  triggers_FR_1mu_noiso ),
            ]
            exclusiveDatasets = True

        if runDataQCD or True: # for fake rate measurements in data
            if analysis!='susy':
                ttHLepSkim.minLeptons=1
            else:
                globalSkim.selection = ["1lep5"]
            if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
            FRTrigs = triggers_FR_1mu_iso + triggers_FR_1mu_noiso + triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
            for t in FRTrigs:
                tShort = t.replace("HLT_","FR_").replace("_v*","")
                triggerFlagsAna.triggerBits[tShort] = [ t ]
                FRTrigs_mu = triggers_FR_1mu_iso + triggers_FR_1mu_noiso
                FRTrigs_el = triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g
                DatasetsAndTriggers = [ (pd,trig) for pd,trig in DatasetsAndTriggers ] # if pd in ['DoubleMuon','DoubleEG'] ]
                for pd,trig in DatasetsAndTriggers:
                    print pd
                    if pd in ['DoubleMuon','SingleMuon']:
                        trig.extend(FRTrigs_mu)
                    elif pd in ['DoubleEG','SingleElectron']:
                        trig.extend(FRTrigs_el)
                    else:
                        print 'the strategy for trigger selection on MuonEG for FR studies should yet be implemented'
                        #assert(False)

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
                                                 run_range=(run_range if "PromptReco" not in myprocessing else None), 
                                                 triggers=triggers[:], vetoTriggers = vetos[:],
                                                 useAAA=useAAA)
                if "PromptReco" in myprocessing:
                    from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
                    filterComponent(comp, verbose=1)
                print "Will process %s (%d files)" % (comp.name, len(comp.files))
                comp.splitFactor = len(comp.files)/8
                comp.fineSplitFactor = 1
                selectedComponents.append( comp )
            if exclusiveDatasets: vetos += triggers
    if json is None:
        susyCoreSequence.remove(jsonAna)

printSummary(selectedComponents)

if True and runData:
    from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
    for c in selectedComponents:
        printnewsummary = False
        c.splitFactor = len(c.files)/3
        if "PromptReco" in c.name:
            printnewsummary = True
            filterComponent(c, 1)
            c.splitFactor = len(c.files)/3
    if printnewsummary: printSummary(selectedComponents)


if runFRMC: 
    QCD_Mu5 = [ QCD_Pt20to30_Mu5, QCD_Pt30to50_Mu5, QCD_Pt50to80_Mu5, QCD_Pt80to120_Mu5, QCD_Pt120to170_Mu5 ]
#    QCDPtEMEnriched = [ QCD_Pt20to30_EMEnriched, QCD_Pt30to50_EMEnriched, QCD_Pt50to80_EMEnriched, QCD_Pt80to120_EMEnriched, QCD_Pt120to170_EMEnriched ]
#    QCDPtbcToE = [ QCD_Pt_20to30_bcToE, QCD_Pt_30to80_bcToE, QCD_Pt_80to170_bcToE ]
#    QCDHT = [ QCD_HT100to200, QCD_HT200to300, QCD_HT300to500, QCD_HT500to700 ]
#    selectedComponents = [QCD_Mu15] + QCD_Mu5 + QCDPtEMEnriched + QCDPtbcToE + [WJetsToLNu_LO,DYJetsToLL_M10to50,DYJetsToLL_M50]
#    selectedComponents = [ QCD_Pt_170to250_bcToE, QCD_Pt120to170_EMEnriched, QCD_Pt170to300_EMEnriched ]
#    selectedComponents = [QCD_Mu15]

#    selectedComponents = [TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromTbar]

    selectedComponents = [QCD_Mu15] + QCD_Mu5 + [WJetsToLNu,DYJetsToLL_M10to50,DYJetsToLL_M50] 

    time = 5.0
    configureSplittingFromTime([WJetsToLNu],20,time)
#    configureSplittingFromTime([WJetsToLNu_LO],20,time)
    configureSplittingFromTime([DYJetsToLL_M10to50],10,time)
    configureSplittingFromTime([DYJetsToLL_M50],30,time)
    configureSplittingFromTime([QCD_Mu15]+QCD_Mu5,70,time)
#    configureSplittingFromTime(QCDPtbcToE,50,time)
#    configureSplittingFromTime(QCDPtEMEnriched,25,time)
#    configureSplittingFromTime([ QCD_HT100to200, QCD_HT200to300 ],10,time)
#    configureSplittingFromTime([ QCD_HT300to500, QCD_HT500to700 ],15,time)
#    configureSplittingFromTime([ QCD_Pt120to170_EMEnriched,QCD_Pt170to300_EMEnriched ], 15, time)
#    configureSplittingFromTime([ QCD_Pt_170to250_bcToE ], 30, time)
    if runQCDBM:
        configureSplittingFromTime([QCD_Mu15]+QCD_Mu5,15,time)
    for c in selectedComponents:
        c.triggers = []
        c.vetoTriggers = [] 
    #printSummary(selectedComponents)

if runFRMC or runDataQCD:
    susyScanAna.useLumiInfo = False
    if analysis!='susy':
        ttHLepSkim.minLeptons=1
    else:
        globalSkim.selection = ["1lep5"]
    if ttHJetMETSkim in susyCoreSequence: susyCoreSequence.remove(ttHJetMETSkim)
    if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
    if runDataQCD:
        FRTrigs = triggers_FR_1mu_iso + triggers_FR_1mu_noiso + triggers_FR_1e_noiso + triggers_FR_1e_iso + triggers_FR_1e_b2g + triggers_FR_jet + triggers_FR_muNoIso
        for t in FRTrigs:
            tShort = t.replace("HLT_","FR_").replace("_v*","")
            triggerFlagsAna.triggerBits[tShort] = [ t ]
    treeProducer.collections = {
        "selectedLeptons" : NTupleCollection("LepGood",  leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
        "otherLeptons"    : NTupleCollection("LepOther", leptonTypeSusy, 8, help="Leptons after the preselection"),
        "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
        "discardedJets"    : NTupleCollection("DiscJet", jetTypeSusySuperLight if analysis=='susy' else jetTypeSusyExtraLight, 15, help="Jets discarted in the jet-lepton cleaning"),
        "selectedTaus"    : NTupleCollection("TauGood",  tauTypeSusy, 8, help="Taus after the preselection"),
        "otherTaus"       : NTupleCollection("TauOther",  tauTypeSusy, 8, help="Taus after the preselection not selected"),
    }
    if True: # 
        from CMGTools.TTHAnalysis.analyzers.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
        ttHLepQCDFakeRateAna = cfg.Analyzer(ttHLepQCDFakeRateAnalyzer, name="ttHLepQCDFakeRateAna",
            jetSel = lambda jet : jet.pt() > (25 if abs(jet.eta()) < 2.4 else 30),
            pairSel = lambda lep, jet: deltaR(lep.eta(),lep.phi(), jet.eta(), jet.phi()) > 0.7,
        )
        susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, ttHLepQCDFakeRateAna)
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
        susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim)
        susyCoreSequence.remove(lheWeightAna)
        susyCounter.doLHE = False
    if runQCDBM:
        fastSkimBM = cfg.Analyzer(
            ttHFastLepSkimmer, name="ttHFastLepSkimmerBM",
            muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 8,
            electrons = 'slimmedElectrons', eleCut = lambda ele : False,
            minLeptons = 1,
        )
        fastSkim.minLeptons = 2
        ttHLepSkim.maxLeptons = 1
        susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, fastSkimBM)
        from PhysicsTools.Heppy.analyzers.core.TriggerMatchAnalyzer import TriggerMatchAnalyzer
        trigMatcher1Mu2J = cfg.Analyzer(
            TriggerMatchAnalyzer, name="trigMatcher1Mu",
            label='1Mu',
            processName = 'PAT',
            fallbackProcessName = 'RECO',
            unpackPathNames = True,
            trgObjSelectors = [ lambda t : t.path("HLT_Mu8_v*",1,0) or t.path("HLT_Mu17_v*",1,0) or t.path("HLT_Mu22_v*",1,0) or t.path("HLT_Mu27_v*",1,0) or t.path("HLT_Mu45_eta2p1_v*",1,0) or t.path("HLT_L2Mu10_v*",1,0) ],
            collToMatch = 'cleanJetsAll',
            collMatchSelectors = [ lambda l,t : True ],
            collMatchDRCut = 0.4,
            univoqueMatching = True,
            verbose = False,
            )
        susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, trigMatcher1Mu2J)
        ttHLepQCDFakeRateAna.jetSel = lambda jet : jet.pt() > 25 and abs(jet.eta()) < 2.4 and jet.matchedTrgObj1Mu
if sample == "z3l":
    ttHLepSkim.minLeptons = 3
    if getHeppyOption("fast"): raise RuntimeError, 'Already added ttHFastLepSkimmer with 2-lep configuration, this is wrong.'
    treeProducer.collections = {
        "selectedLeptons" : NTupleCollection("LepGood", leptonTypeSusyExtraLight, 8, help="Leptons after the preselection"),
        "cleanJets"       : NTupleCollection("Jet",     jetTypeSusyExtraLight, 15, help="Cental jets after full selection and cleaning, sorted by pt"),
    }
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer3lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 3 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
        minLeptons = 3,
    )
    fastSkim2 = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer2lep",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 10 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 10,
        minLeptons = 2,
    )
    susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim)
    susyCoreSequence.insert(susyCoreSequence.index(jsonAna)+1, fastSkim2)
    susyCoreSequence.remove(lheWeightAna)
    susyCoreSequence.remove(ttHJetMETSkim)
    susyCounter.doLHE = False
    if not runData:
        selectedComponents = [DYJetsToLL_M50_LO]
        #prescaleComponents([DYJetsToLL_M50_LO], 2)
        #configureSplittingFromTime([DYJetsToLL_M50_LO],4,1.5)
        selectedComponents = [WZTo3LNu,ZZTo4L]
        cropToLumi([WZTo3LNu,ZZTo4L], 50)
        #configureSplittingFromTime([WZTo3LNu,ZZTo4L],20,1.5)
    else:
        if True:
            from CMGTools.Production.promptRecoRunRangeFilter import filterComponent
            for c in selectedComponents:  
                if "PromptReco" in c.name: filterComponent(c, 1)
        if analysis == 'SOS':
            configureSplittingFromTime(selectedComponents,10,2)

if is50ns:
    # no change in MC GT since there's no 76X 50ns MC
    jetAna.dataGT   = "76X_dataRun2_v15_Run2015B_50ns"
    jetAnaScaleUp.dataGT   = "76X_dataRun2_v15_Run2015B_50ns"
    jetAnaScaleDown.dataGT   = "76X_dataRun2_v15_Run2015B_50ns"

if runSMS:
    jetAna.mcGT = "Spring16_FastSimV1_MC"
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
