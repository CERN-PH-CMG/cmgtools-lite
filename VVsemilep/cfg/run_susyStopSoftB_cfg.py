##########################################################
##       CONFIGURATION FOR SUSY STOP SOFT B TREES       ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg
import re

#-------- LOAD ALL ANALYZERS -----------
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from CMGTools.RootTools.samples.configTools import *
from CMGTools.RootTools.samples.autoAAAconfig import *
from CMGTools.Production.promptRecoRunRangeFilter import filterComponent as filterPromptRecoComponent


#-------- DEFINE CONFIGURATION -----------

# Pre-skim
from CMGTools.TTHAnalysis.analyzers.ttHFastMETSkimmer import ttHFastMETSkimmer
ttHFastMETSkim = cfg.Analyzer(
   ttHFastMETSkimmer, name='ttHFastMETSkimmer',
   met      = "slimmedMETs", # jet collection to use
   metCut    =  200,  # MET cut
   )
susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, ttHFastMETSkim)

# Leptons
lepAna.doMiniIsolation = True
lepAna.inclusive_muon_dxy = 999
lepAna.inclusive_muon_dz  = 999
lepAna.loose_muon_dxy = 0.2
lepAna.loose_muon_dz  = 0.5
lepAna.loose_muon_isoCut = lambda muon : muon.miniRelIso < 0.2
lepAna.inclusive_electron_dxy = 999
lepAna.inclusive_electron_dz  = 999
lepAna.inclusive_electron_lostHits  = 9999
lepAna.loose_electron_dxy = 0.5
lepAna.loose_electron_dz  = 1.0
lepAna.loose_electron_pt = 5
lepAna.loose_electron_id = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto"
lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.1
lepAna.loose_electron_lostHits  = 9999
#lepAna.vertexChoice = "vertices" # FIXME

# Photons (may need updates) 
photonAna.do_mc_match = False

# Taus (will need updates)
tauAna.inclusive_dzMax  = 999 # FIXME
tauAna.loose_decayModeID = "decayModeFindingNewDMs"
tauAna.loose_ptMin = 20
tauAna.loose_etaMax = 999 # FIXME
tauAna.loose_dzMax  = 999 # FIXME
tauAna.loose_vetoLeptons = False
tauAna.loose_decayModeID = "decayModeFindingNewDMs" 
tauAna.loose_tauID = "byVLooseIsolationMVArun2v1DBnewDMwLT"
#tauAna.vertexChoice = "vertices" #FIXME

# Jets
jetAna.jetPt = 20
jetAna.calculateType1METCorrection = True
jetAna.jetLepDR = 0.4
jetAna.minLepPt = 0
jetAna.cleanSelectedLeptons = False
#jetAna.recalibrateJets = False
#jetAna.relaxJetId = True

# MET
metAna.recalibrate = "type1"
#metAna.recalibrate = False

# MET Filters 
from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheAna = cfg.Analyzer( hbheAnalyzer, name="hbheAnalyzer", IgnoreTS4TS5ifJetInLowBVRegion=False)

# IVF
ttHSVAna.associatedJetsByRef = False
ttHSVAna.preselection = lambda sv : abs(sv.dxy.value()) < 3 and sv.cosTheta > 0.98
#ttHSVAna.vertexChoice = "vertices" #FIXME
ttHSVAna.jets = 'cleanJets'

# Event (common)
ttHCoreEventAna.jetPt = 20

# Event (susyStopSoftB)
from CMGTools.TTHAnalysis.analyzers.susyStopSoftBEventAnalyzer import susyStopSoftBEventAnalyzer
stopSoftBAna = cfg.Analyzer(
   susyStopSoftBEventAnalyzer, name='stopSoftBAna',
)

# Event selection
from CMGTools.TTHAnalysis.analyzers.ttHJetMETSkimmer import ttHJetMETSkimmer
ttHJetMETSkim = cfg.Analyzer(
   ttHJetMETSkimmer, name='ttHJetMETSkimmer',
   jets      = "cleanJets", # jet collection to use
   jetPtCuts = [],  # e.g. [60,40,30,20] to require at least four jets with pt > 60,40,30,20
   jetVetoPt =  0,  # if non-zero, veto additional jets with pt > veto beyond the ones in jetPtCuts
   metCut    =  200,  # MET cut
   htCut     = ('htJetXj', 0), # cut on HT defined with only jets and pt cut 40, at zero; i.e. no cut
                                # see ttHCoreEventAnalyzer for alternative definitions
   mhtCut    = ('mhtJetX', 0), # cut on MHT defined with all leptons, and jets with pt > 40.
   nBJet     = ('CSVv2IVFM', 0, "jet.pt() > 30"),     # require at least 0 jets passing CSV medium and pt > 30
   )
susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, ttHJetMETSkim)

## Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusyStopSoftB import * 
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerStopSoftB',
     vectorTree = True, saveTLorentzVectors = False,  defaultFloatType = 'F', PDFWeights = [],
     globalVariables = susyStopSoftB_globalVariables,
     globalObjects = susyStopSoftB_globalObjects,
     collections = susyStopSoftB_collections,
)


## For non-signal
susyScanAna.useLumiInfo = False
if True:
    susyCoreSequence.remove(lheWeightAna)
    del treeProducer.collections["LHE_weights"]

#-------- SAMPLES AND TRIGGERS -----------
from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import *
triggerFlagsAna.triggerBits = {
    'MET90MHT90'   : triggers_met90_mht90,
    'MET100MHT100' : triggers_met100_mht100,
    'MET120MHT120' : triggers_met120_mht120,
    'MET90MHT90NoMu'   : triggers_metNoMu90_mhtNoMu90,
    'MET120MHT120NoMu' : triggers_metNoMu120_mhtNoMu120,
    'MET90MHT90Jet80'   : triggers_Jet80MET90,
    'MET120MHT120Jet80' : triggers_Jet80MET120,
    'DoubleEG' : triggers_ee,
    'MuEG'     : triggers_mue,
    'DoubleMu' : triggers_mumu,
    'SingleMu' : triggers_1mu_iso,
    'SingleEl' : triggers_1e,
}
triggerFlagsAna.unrollbits = True

from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *
from CMGTools.RootTools.samples.samples_13TeV_80X_susySignalsPriv import *
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *

#what = "SR" 
what = "CRWc" 
what = "CR2L" 
#what = "CRLL"

## ==== MC: 2L CR ====
if what == "SR":
    QCDHT.remove(QCD_HT100to200); 
    mcSamples = ZJetsToNuNuHT + WJetsToLNuHT + QCDHT + DYJetsM50HT + DYJetsM5to50HT + [TTJets,TT_pow_ext3,TT_pow_ext4,]
    autoAAA(mcSamples)
    mcSamples, mcSamplesMap = mergeExtensions(mcSamples) 
    cropToLumi(mcSamples,100) 
    time=1.5; options = { 'minSplit':5, 'maxFiles':10, 'penaltyByOrigin':[('root://cms-xrd-global',2)] }
    #QCDHT = [ s for (k,s) in mcSamplesMap.iteritems() if "QCD" in k ]
    configureSplittingFromTime(QCDHT+DYJetsM50HT+DYJetsM5to50HT,  4, time, **options)
    configureSplittingFromTime([TTJets,TT_pow_ext3,TT_pow_ext4,], 5, time, **options)
    configureSplittingFromTime(WJetsToLNuHT,  8,  time, **options)
    configureSplittingFromTime(ZJetsToNuNuHT, 12, time, **options)
    dataSamples = [ d for d in dataSamples_PromptReco_v2 if "MET" in d.name ] 
    for d in dataSamples: d.triggers = triggers_met90_mht90 + triggers_met100_mht100 + triggers_met120_mht120 + triggers_metNoMu90_mhtNoMu90  + triggers_metNoMu120_mhtNoMu120 + triggers_Jet80MET90 + triggers_Jet80MET120
    sigSamples = T2cc #T2ttDeg + T2cc
    for s in sigSamples: s.splitFactor = 5 
elif what in ("CR2L", "CRLL"):
    ttHFastMETSkim.metCut = 20
    ttHJetMETSkim.metCut  = 30 
    ttHLepSkim.minLeptons = 2
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(ttHFastLepSkimmer, name="ttHFastLepSkimmer",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 5 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 5,
        minLeptons = 2,
        ptCuts = [25,20],
        requireOppositeFlavourPair = (what == "CR2L")
    )
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, fastSkim)
    from CMGTools.TTHAnalysis.analyzers.ttHFastJetSkimmer import ttHFastJetSkimmer
    fastBSkim = cfg.Analyzer(ttHFastJetSkimmer, name="ttHFastJetSkimmer",
        jets = 'slimmedJets',
        jetCut = lambda j : j.pt() > 20 and j.bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags') > 0.8484, # looser pt because of non-final JECs
        minJets = 1,
    )
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+2, fastBSkim)
    stopSoftBAna.bJet = "require"
    if what == "CR2L":
        stopSoftBAna.eMu = "require"
    else:
        stopSoftBAna.eMu   = "veto"
        stopSoftBAna.llNoZ = "require"
    mcSamples = [ TTLep_pow,
                  TTJets_DiLepton, TTJets_DiLepton_ext,
                  T_tWch_noFullyHad, T_tWch_noFullyHad_ext, TBar_tWch_noFullyHad_ext, TBar_tWch_noFullyHad,
                  DYJetsToLL_M50_LO_ext,
                  DYJetsToLL_M10to50, DYJetsToLL_M10to50_ext,
                  WWTo2L2Nu, WZTo3LNu,
                  W2JetsToLNu_LO, W3JetsToLNu_LO, W4JetsToLNu_LO,
                  T_tch_powheg, TBar_tch_powheg,
                  TTJets_SingleLeptonFromT, TTJets_SingleLeptonFromT_ext, TTJets_SingleLeptonFromTbar, TTJets_SingleLeptonFromTbar_ext ]
    autoAAA(mcSamples)
    mcSamples, mcSamplesMap = mergeExtensions(mcSamples)
    cropToLumi(mcSamples,200)
    DSAndTrig = [ ("MuonEG",triggers_mue), ] if what == "CR2L" else [ ("DoubleMu",triggers_mumu), ("DoubleEG",triggers_ee) ]
    dataSamples = [ ]; vetoTrig = []
    for name, trig in DSAndTrig:
        for d in dataSamples_23Sep2016PlusPrompt:
            if name in d.name: 
                d.triggers = trig[:]; d.vetoTriggers = vetoTrig[:]
                dataSamples.append(d)
        vetoTrig += trig
    if what == "CR2L":
        configureSplittingFromTime(mcSamples, 12, 2.0)
        configureSplittingFromTime([mcSamplesMap[X] for X in "W2JetsToLNu_LO W3JetsToLNu_LO DYJetsToLL_M50_LO DYJetsToLL_M10to50".split()], 5, 2, maxFiles=15)
        configureSplittingFromTime(dataSamples, 5, 2, maxFiles=15)
    elif what == "CRLL":
        configureSplittingFromTime(mcSamples, 15, 2.0, maxFiles=15)
        configureSplittingFromTime(dataSamples, 15, 2.0, maxFiles=15)
    #configureSplittingFromTime([d for d in dataSamples if "Single" in d.name], 8, 2)
elif what == "CRWc":
    ttHFastMETSkim.metCut = 30
    ttHJetMETSkim.metCut  = 30 
    ttHLepSkim.minLeptons = 1
    from CMGTools.TTHAnalysis.analyzers.ttHFastLepSkimmer import ttHFastLepSkimmer
    fastSkim = cfg.Analyzer(
        ttHFastLepSkimmer, name="ttHFastLepSkimmer",
        muons = 'slimmedMuons', muCut = lambda mu : mu.pt() > 20 and mu.isLooseMuon(),
        electrons = 'slimmedElectrons', eleCut = lambda ele : ele.pt() > 20,
        minLeptons = 1,
    )
    susyCoreSequence.insert(susyCoreSequence.index(skimAnalyzer)+1, fastSkim)
    #mcSamples = [ TTJets, TBar_tWch, T_tWch, TBarToLeptons_tch_powheg, TToLeptons_tch_powheg,
    #              WJetsToLNu, DYJetsToLL_M10to50, DYJetsToLL_M50, WWTo2L2Nu, WZTo3LNu ]
    #mcSamples = [ TTJets_LO, TTLep_powUEP8M2, TTSemi_powUEP8M2 ] #, DYJetsToLL_M10to50, DYJetsToLL_M10to50_LO, DY1JetsToLL_M10to50, DY2JetsToLL_M10to50 ]
    mcSamples = [ WJetsToLNu_reHLT  ]#, TTJets, DYJetsToLL_M10to50, DYJetsToLL_M50, QCD_Mu15 ]
    #jetAna.mcGT = "Spring16_FastSimV1_MC"
    #jetAna.applyL2L3Residual = False
    autoAAA(mcSamples)
    cropToLumi(mcSamples,2.5) 
    #mcSamples = WNJets
    configureSplittingFromTime(mcSamples, 12, 1)
    #configureSplittingFromTime(WNJets, 5, 1)
    dataSamples = [ ]; vetoTrig = []
    for name, trig in ("SingleMu", triggers_1mu_iso),("SingleEl", triggers_1e),: # ("DoubleMu",triggers_mumu), ("DoubleEG",triggers_ee):#, ("MuonEG",triggers_mue),("SingleEl", triggers_1e):
        for d in [SingleMuon_Run2016G_23Sep2016]:#[ SingleMuon_Run2016H_PromptReco_v2, SingleElectron_Run2016G_23Sep2016, SingleElectron_Run2016H_PromptReco_v2 ]: #MuonEG_more: #29Jul2016: #dataSamples_Run2016C_v2 + dataSamples_Run2016D_v2 :
            if name in d.name: 
                d.triggers = trig[:]; d.vetoTriggers = vetoTrig[:]
                dataSamples.append(d)
        vetoTrig += trig
    configureSplittingFromTime(dataSamples, 10, 1.5, maxFiles=15)
    #configureSplittingFromTime([d for d in dataSamples if "Single" in d.name], 8, 2)


for d in dataSamples:
    d.json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    if "PromptReco" in d.dataset: filterPromptRecoComponent(d,verbose=0)

selectedComponents = dataSamples + mcSamples # [mcSamplesMap["ZJetsToNuNu_HT800t1200"]]#sigSamples # dataSamples # mcSamples #


#-------- SEQUENCE -----------
sequence = cfg.Sequence(susyCoreSequence+[
        ttHFatJetAna,
        ttHSVAna, 
        stopSoftBAna,
        #ttHHeavyFlavourHadronAna,
        hbheAna,
        treeProducer,
    ])

#-------- HOW TO RUN -----------
test = getHeppyOption('test')
if test == "1":
    print "The test wil use %s " % selectedComponents[0].name
    selectedComponents = doTest1(selectedComponents[0], sequence=sequence, cache=False )
    print "The test wil use file %s " % selectedComponents[0].files[0]
elif test == "1Z":
    print ZJetsToNuNu_HT200to400_ext.files[2]
    selectedComponents = doTest1(ZJetsToNuNu_HT200to400_ext, sequence=sequence, cache=True )
elif test == "sync":
    T2ttDeg_mStop425_mChi405_4bodydec.files = T2ttDeg_mStop425_mChi405_4bodydec.files[:5]
    selectedComponents = [ T2ttDeg_mStop425_mChi405_4bodydec ]
    if getHeppyOption('events'): 
        selectedComponents[0].splitFactor = 1
        insertEventSelector(sequence)
elif test in ('2','3','5s'):
    selectedComponents = [ TTLep_pow, mcSamplesMap["DYJetsToLL_M50_LO"] ]  + [ d for d in dataSamples if "Run2016G" in d.name ]
    #selectedComponents = [ mcSamplesMap[X] for X in "TTJets_SingleLeptonFromT W3JetsToLNu_LO".split() ]
    #from CMGTools.Production.promptRecoRunRangeFilter import filterWithCollection
    #for comp in selectedComponents:
    #    if comp.isData and "PromptReco" in comp.name: comp.files = filterWithCollection(comp.files, [274315,275658,275832,276363,276454])
    doTestN(test,selectedComponents)
elif test in ('2M',):
    selectedComponents = doTestN('2',mcSamples)
elif test in ('2D',):
    redefineRunRange(dataSamples,[274315,274315])
    selectedComponents = doTestN('2',dataSamples)

printSummary(selectedComponents)

config = autoConfig(selectedComponents, sequence) #, xrd_aggressive=-1)

