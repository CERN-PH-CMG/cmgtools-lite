##########################################################
##       CONFIGURATION FOR SUSY SingleLep TREES       ##
## skim condition: >= 1 loose leptons, no pt cuts or id ##
##########################################################
import PhysicsTools.HeppyCore.framework.config as cfg


#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *


# Lepton Preselection
# ele
lepAna.loose_electron_id = "POG_MVA_ID_Run2_NonTrig_VLoose"
lepAna.loose_electron_pt  = 5
# mu
lepAna.loose_muon_pt  = 5

# lep collection
lepAna.packedCandidates = 'packedPFCandidates'

# selec Iso
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

# --- LEPTON SKIMMING ---
ttHLepSkim.minLeptons = 1
ttHLepSkim.maxLeptons = 999
#LepSkim.idCut  = ""
#LepSkim.ptCuts = []

# JETS
jetAna.minLepPt = 10 # --- JET-LEPTON CLEANING ---
jetAna.jetPt = 25
jetAna.jetEta = 2.4

#jetAna.mcGT = "Summer15_V5_p6_MC" # use default
jetAna.doQG = True
jetAna.smearJets = False #should be false in susycore, already
jetAna.recalibrateJets = True #should be true in susycore, already

## MET
metAna.recalibrate = False #should be false in susycore, already

## Iso Track
isoTrackAna.setOff=False

# store all taus by default
genAna.allGenTaus = True

from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
	ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
	minJets25 = 0,
	)

## Insert the FatJet, SV, HeavyFlavour analyzers in the sequence
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
			ttHFatJetAna)
susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
			ttHSVAna)
#susyCoreSequence.insert(susyCoreSequence.index(metAna),
#			metNoHFAna)
## Single lepton + ST skim
from CMGTools.TTHAnalysis.analyzers.ttHSTSkimmer import ttHSTSkimmer
ttHSTSkimmer = cfg.Analyzer(
	ttHSTSkimmer, name='ttHSTSkimmer',
	minST = 200,
	)

#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import * # central trigger list
from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *

triggerFlagsAna.triggerBits = {
	# put trigger here
	## hadronic
	'HT350' : triggers_HT350,
	'HT600' : triggers_HT600,
	'HT800' : triggers_HT800,
	'MET170' : triggers_MET170,
	'HT350MET120' : triggers_HT350MET120,
	'HT350MET100' : triggers_HT350MET100,
	'HTMET' : triggers_HT350MET100 + triggers_HT350MET120,
	## muon
	'SingleMu' : triggers_1mu,
	'IsoMu27' : triggers_1mu,
	'Mu45eta2p1' : trigger_1mu_noiso_r,
	'Mu50' : trigger_1mu_noiso_w,
	'MuHT600' : triggers_mu_ht600,
	'MuHT400MET70' : triggers_mu_ht400_met70,
	'MuHT350MET70' : triggers_mu_ht350_met70,
	'MuHTMET' : triggers_mu_ht350_met70 + triggers_mu_ht400_met70,
	'MuMET120' : triggers_mu_met120,
	'MuHT400B': triggers_mu_ht400_btag,
	## electrons
	'IsoEle32' : triggers_1el,
	'Ele105' : trigger_1el_noiso,
	'EleHT600' : triggers_el_ht600,
	'EleHT400MET70' : triggers_el_ht400_met70,
	'EleHT350MET70' : triggers_el_ht350_met70,
	'EleHTMET' : triggers_el_ht350_met70 + triggers_el_ht400_met70,
	'EleHT200' :triggers_el_ht200,
	'EleHT400B': triggers_el_ht400_btag
	}

## TEMPORARY
# HBHE filter analyzer
from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheFilterAna = cfg.Analyzer(
    hbheAnalyzer, name = 'hbheAnalyzer',
)


removeResiduals = True
isData=False
# -------------------- Running pre-processor
import subprocess
jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_50nsV2_MC.db'
jecEra    = 'Summer15_50nsV2_MC'
preprocessorFile = "$CMSSW_BASE/tmp/MetType1_jec_%s.py"%(jecEra)
extraArgs=[]
if isData:
	extraArgs.append('--isData')
	GT= '74X_dataRun2_Prompt_v1'
else:
	GT= 'MCRUN2_74_V9A'
if removeResiduals:extraArgs.append('--removeResiduals')
args = ['python',
	os.path.expandvars('$CMSSW_BASE/python/CMGTools/ObjectStudies/corMETMiniAOD_cfgCreator.py'),\
		'--GT='+GT,
	'--outputFile='+preprocessorFile,
	'--jecDBFile='+jecDBFile,
	'--jecEra='+jecEra
	] + extraArgs
#print "Making pre-processorfile:"
#print " ".join(args)
subprocess.call(args)
from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
preprocessor = CmsswPreprocessor(preprocessorFile)

# Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusySingleLepton import *
## Tree Producer
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



#-------- SAMPLES AND TRIGGERS -----------

# -- new 74X samples
#from CMGTools.RootTools.samples.samples_13TeV_74X import *
# -- samples at DESY
from CMGTools.SUSYAnalysis.samples.samples_13TeV_74X_desy import *

#selectedComponents = [
#	T1tttt_mGo1500_mChi100,
#	T1tttt_mGo1200_mChi800
	#TTJets,
	#TTJets_50ns
	#TTJets_LO,
	#TTJets_LO_50ns,
	#TTJets_LO_25ns
#        ]
selectedComponents = [
    QCD_HT300to500,
    QCD_HT500to700,
    QCD_HT700to1000,
    QCD_HT1000to1500,
    QCD_HT1500to2000,
    QCD_HT2000toInf
]

#-------- SEQUENCE

sequence = cfg.Sequence(susyCoreSequence+[
		ttHEventAna,
		#ttHSTSkimmer,
		#ttHReclusterJets,
		hbheFilterAna,
		treeProducer,
		])


#-------- HOW TO RUN
#test = 'MC'
test = 'data'
#test = 1

if test==1:
	# test a single component, using a single thread.
	isData = False
	comp = TTJets
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
		comp.fineSplitFactor = 5
		comp.splitFactor = len(comp.files)

elif test=='MC':
	from CMGTools.SUSYAnalysis.samples.samples_13TeV_74X_desy import *
	selectedComponents = mcSamples_Asymptotic50ns

	for comp in selectedComponents:
                comp.splitFactor = len(comp.files)

elif test=="data":
	#from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import *
	from CMGTools.SUSYAnalysis.samples.samples_13TeV_DATA2015_desy import *
	isData = True
	#selectedComponents = [ SingleElectron_Run2015B, SingleMuon_Run2015B ]
	#selectedComponents = [ SingleElectron_Run2015B ]
	#selectedComponents = [ SingleElectron_Run2015B_17Jul ]
	selectedComponents = [ SingleMuon_Run2015B_17Jul ]
	#selectedComponents = [ JetHT_Run2015B_17Jul ]
	#selectedComponents = [ HTMHT_Run2015B ]

	for comp in selectedComponents:
		#comp.splitFactor = len(comp.files)
		#comp.fineSplitFactor = 10
		comp.files = comp.files[:1]


from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
		     sequence = sequence,
		     services = [],
		     preprocessor=preprocessor,
		     events_class = Events)
