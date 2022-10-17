import PhysicsTools.HeppyCore.framework.config as cfg
from CMGTools.RootTools.RootTools import *

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *


jsonAna.useLumiBlocks = True

#------------------------------------------
## Redefine analyzer parameters
##------------------------------------------

# Muons
#------------------------------
lepAna.loose_muon_dxy = 0.2
lepAna.loose_muon_dz  = 0.5
lepAna.loose_muon_relIso  = 99.
lepAna.loose_muon_pt  = 10.
lepAna.loose_muon_isoCut = lambda muon :muon.miniRelIso < 0.2

lepAna.loose_electron_pt  = 10.
lepAna.loose_electron_eta    = 2.4
lepAna.loose_electron_relIso = 99.
lepAna.loose_electron_isoCut = lambda electron : electron.miniRelIso < 0.1
lepAna.loose_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"
#lepAna.loose_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Medium_full5x5"
lepAna.loose_electron_lostHits = 999. # no cut
lepAna.loose_electron_dxy    = 999.
lepAna.loose_electron_dz     = 999.

lepAna.inclusive_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto_full5x5"
#lepAna.inclusive_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Medium_full5x5"
lepAna.inclusive_electron_lostHits = 999. # no cut since embedded in ID
lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

lepAna.mu_isoCorr = "deltaBeta"
lepAna.ele_isoCorr = "deltaBeta"
lepAna.ele_tightId = "Cuts_SPRING15_25ns_v1_ConvVetoDxyDz"
lepAna.notCleaningElectrons = True
lepAna.doMiniIsolation = True
lepAna.packedCandidates = 'packedPFCandidates'
lepAna.miniIsolationPUCorr = 'rhoArea'
lepAna.ele_effectiveAreas = 'Spring15_25ns_v1'             #new default 
lepAna.mu_effectiveAreas = 'Spring15_25ns_v1'              #new default
lepAna.rhoMuon= 'fixedGridRhoFastjetCentralNeutral',      #new default
lepAna.rhoElectron = 'fixedGridRhoFastjetCentralNeutral', #new default


lepAna.doIsoAnnulus = True

# Photons
#------------------------------
photonAna.ptMin                        = 25,
photonAna.epaMax                       = 2.5,

# Taus 

jetAna.relaxJetId = False
jetAna.doPuId = False
jetAna.doQG = False
jetAna.jetEta = 4.7
jetAna.jetEtaCentral = 2.4
jetAna.jetPt = 25.
#jetAna.dataGT   = 'Summer15_25nsV6_DATA', # jec corrections
#jetAna.mcGT   = 'Summer15_25nsV6_MC', # jec corrections
#jetAna.recalibrateJets = False # True for MC and false for data
jetAna.recalibrateJets = True # True for MC and false for data
jetAna.jetLepDR = 0.4
jetAna.smearJets = False

jetAna.copyJetsByValue = True # do not remove this
metAna.copyMETsByValue = True # do not remove this
jetAna.addJECShifts = True
susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleDown)
susyCoreSequence.insert(susyCoreSequence.index(jetAna)+1, jetAnaScaleUp)
susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleDown)
susyCoreSequence.insert(susyCoreSequence.index(metAna)+1, metAnaScaleUp)


#--------------------------------


# Isolated Track
isoTrackAna.setOff=False

# recalibrate MET
metAna.recalibrate = False

# store all taus by default
genAna.allGenTaus = True

#------------------------------


# Energy sums
#------------------------------
# NOTE: Currently energy sums are calculated with 40 GeV jets (ttHCoreEventAnalyzer.py)
#       However, the input collection is cleanjets which have a 50 GeV cut so this is a labeling problem


# Jet-MET based Skim (generic, but requirements depend on the final state)
from CMGTools.TTHAnalysis.analyzers.ttHJetMETSkimmer import ttHJetMETSkimmer
ttHJetMETSkim = cfg.Analyzer(
   ttHJetMETSkimmer, name='ttHJetMETSkimmer',
   jets      = "cleanJets", # jet collection to use
   jetPtCuts =  [100],  # e.g. [60,40,30,20] to require at least four jets with pt > 60,40,30,20
   jetVetoPt =  0,  # if non-zero, veto additional jets with pt > veto beyond the ones in jetPtCuts
   metCut    = 200,  # MET cut
   htCut     = ('htJet40j', 0), # cut on HT defined with only jets and pt cut 40, at zero; i.e. no cut
   mhtCut    = ('mhtJet40', 0), # cut on MHT defined with all leptons, and jets with pt > 40.
   nBJet     = ('CSVv2IVFM', 0, "jet.pt() > 25"),     # require at least 0 jets passing CSV medium and pt > 30
   )

ttHJetMETSkim.htCut       = ('htJet50j', 0)
ttHJetMETSkim.mhtCut      = ('htJet40j', 0)
ttHJetMETSkim.nBJet       = ('CSVv2IVFM', 0, "jet.pt() > 25")     # require at least 0 jets passing CSVM and pt > 50

##------------------------------------------
##  ISOLATED TRACK
##------------------------------------------

isoTrackAna.setOff=False
isoTrackAna.doRelIsolation = True

##------------------------------------------
##------------------------------------------


from CMGTools.TTHAnalysis.analyzers.ttHDiJetControl import ttHDiJetControl

ttHDiJetControlAna = cfg.Analyzer(
            ttHDiJetControl, name = 'ttHDiJetControl',
            jetPt = 30.,
            )
from CMGTools.TTHAnalysis.analyzers.hbheAnalyzer import hbheAnalyzer
hbheFilterAna = cfg.Analyzer(
    hbheAnalyzer, name = 'hbheAnalyzer',IgnoreTS4TS5ifJetInLowBVRegion=False
)

susyCoreSequence.insert(susyCoreSequence.index(ttHCoreEventAna),
                        ttHSVAna)



#------------------------------------------
##  PRODUCER
##------------------------------------------
from CMGTools.TTHAnalysis.analyzers.treeProducerSusyDiJet import * 
## Tree Producer
treeProducer = cfg.Analyzer(
     AutoFillTreeProducer, name='treeProducerSusyDiJet',
     vectorTree = True,
     saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
     PDFWeights = PDFWeights,
     globalVariables = susyDiJet_globalVariables,
     globalObjects = susyDiJet_globalObjects,
     collections = susyDiJet_collections,
)

susyDiJet_globalObjects.update({
        "met_jecUp" : NTupleObject("met_jecUp", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC plus 1sigma)"),
        "met_jecDown" : NTupleObject("met_jecDown", metType, help="PF E_{T}^{miss}, after type 1 corrections (JEC minus 1sigma)"),
        })
susyDiJet_collections.update({
            "cleanJets_jecUp"       : NTupleCollection("Jet_jecUp",     jetTypeSusyExtra, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC plus 1sigma)"),
            "cleanJets_jecDown"     : NTupleCollection("Jet_jecDown",     jetTypeSusyExtra, 15, help="Cental jets after full selection and cleaning, sorted by pt (JEC minus 1sigma)"),
            })
#-------- SEQUENCE


sequence = cfg.Sequence(susyCoreSequence + [
                        ttHDiJetControlAna,
                        ttHJetMETSkim, 
                        treeProducer,
                        ])


from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import triggers_dijet55met110, triggers_1mu_iso, triggers_1e, triggers_mumu, triggers_ee, triggers_MET170_NotCleaned, triggers_MET170_HBHECleaned, triggers_MET170_BeamHaloCleaned, triggers_1mu_noniso, triggers_1e_noniso, triggers_mumu_noniso, triggers_ee_noniso, triggers_mumu_ht, triggers_ee_ht, triggers_metNoMu90_mhtNoMu90

triggerFlagsAna.triggerBits = {
'PFMET170_HBHE' : triggers_MET170_HBHECleaned,
'PFMET170_BeamHalo' : triggers_MET170_BeamHaloCleaned,
'PFMET170' : triggers_MET170_NotCleaned,
'SingleMu' : triggers_1mu_iso,
'SingleEl' : triggers_1e_noniso,
'SingleMu_noniso' : triggers_1mu_noniso,
'SingleEl_noniso' : triggers_1e_noniso,
'DoubleMu' : triggers_mumu,
'DoubleEl' : triggers_ee,
'DoubleMu_ht' : triggers_mumu_ht,
'DoubleEl_ht' : triggers_ee_ht,
'DoubleMu_noniso' : triggers_mumu_noniso,
'DoubleE_noniso' : triggers_ee_noniso,
'DiCentralPFJet55_PFMET110' : triggers_dijet55met110,
'MET_MHT': triggers_metNoMu90_mhtNoMu90,
}


#-------- SAMPLES AND TRIGGERS -----------
#------------------------------------------
##  PRODUCER
##---------------

#-------- SAMPLES AND TRIGGERS -----------

#-------- HOW TO RUN
#isData =True
isData =False
runPreprocessor = False
#sample = 'data'
sample = 'MC'
test = 1

if sample == "MC":

        from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import *
	
	selectedComponents = DYJetsM50HT

	if test==1:
		# test a single component, using a single thread.
		comp = TTJets_SingleLeptonFromTbar_ext
#		comp.files = comp.files[:1]
		selectedComponents = [comp]
		#comp.splitFactor = len(comp.files)
                comp.splitFactor = 1
	elif test==2:
		# test all components (1 thread per component).
		for comp in selectedComponents:
			comp.splitFactor = 1
			comp.fineSplitFactor = 2
			comp.files = comp.files[:1]
	elif test==3:
		# run all components (1 thread per component).
		for comp in selectedComponents:
			comp.fineSplitFactor = 1
			comp.splitFactor = len(comp.files)

elif sample == "data":

        jsonFilter =True
    
        from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import *

	selectedComponents = [MET_Run2016B_PromptReco_v2]

	if test==1: 

		comp = MET_Run2016B_PromptReco_v2
		comp.fineSplitFactor = 1  
	#	comp.files = comp.files[:2]
		selectedComponents = [comp]
		comp.splitFactor = 1
		#comp.splitFactor = len(comp.files)
                comp.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt'  
	elif test==2:
		for comp in selectedComponents:
			comp.splitFactor = 1
			comp.fineSplitFactor = 2
			comp.files = comp.files[1:20]
	elif test==3:
     
		# run on everything
		for comp in selectedComponents:
			comp.fineSplitFactor = 1  
			comp.splitFactor = len(comp.files)
			#comp.splitFactor = 1
                        comp.json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274443_13TeV_PromptReco_Collisions16_JSON.txt'  



if runPreprocessor:
    removeResiduals = False
    # -------------------- Running pre-processor
    import subprocess

    if isData:
        uncFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV5_DATA_UncertaintySources_AK4PFchs.txt'
        jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV5_DATA.db'
        jecEra    = 'Summer15_25nsV5_DATA'
    else:
        uncFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV5_MC_UncertaintySources_AK4PFchs.txt'
        jecDBFile = '$CMSSW_BASE/src/CMGTools/RootTools/data/jec/Summer15_25nsV5_MC.db'
        jecEra    = 'Summer15_25nsV5_MC'
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
            '--uncFile='+uncFile,
            '--jecEra='+jecEra
            ] + extraArgs
    subprocess.call(args)
    from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
    preprocessor = CmsswPreprocessor(preprocessorFile)

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events

config = cfg.Config( components = selectedComponents,
                     sequence = sequence,
                     services = [],
                     #preprocessor=preprocessor, # comment if pre-processor non needed
                     events_class = Events)


