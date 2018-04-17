import FWCore.ParameterSet.Config as cms
import os

##
# This file corresponds to 
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription#Instructions_for_7_4_X 
##

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--outputFile", dest="outputFile", default="MetType1_dump.py", type="string", action="store", help="output file")
parser.add_option("--GT", dest="GT", default='MCRUN2_74_V9A', type="string", action="store", help="Global Tag")
parser.add_option("--jecDBFile", dest="jecDBFile", default="", type="string", action="store", help="jec DB File")
###parser.add_option("--uncFile", dest="uncFile", default="", type="string", action="store", help="jec Uncer File")
parser.add_option("--jecEra", dest="jecEra", default='', type="string", action="store", help="jecEra")
parser.add_option("--jerDBFile", dest="jerDBFile", default="", type="string", action="store", help="jer DB File")
parser.add_option("--jerEra", dest="jerEra", default='', type="string", action="store", help="jerEra")
parser.add_option("--maxEvents", dest="maxEvents", default=-1, type="int", action="store", help="maxEvents")
parser.add_option("--removeResiduals", dest="removeResiduals", action="store_true", default=False, help="remove residual JEC?")
parser.add_option("--isData", dest="isData", action="store_true", default=False, help="is data?")
parser.add_option("--redoPuppi", dest="redoPuppi", action="store_true", default=True, help="re-run puppi")
parser.add_option("--addReclusterTrackJetsAK4", dest="reclusterTrackJets", action="store_true", default=False, help="recluster AK4 track jets")
(options, args) = parser.parse_args()

print "cmsswPreprocessor options: isData: %s, GT:%s, removeResiduals: %s jecEra: %s"%(options.isData, options.GT,  options.removeResiduals, options.jecEra)

#print options.outputFile, options.GT

# Define the CMSSW process
process = cms.Process("RERUN")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

#configurable options =======================================================================
useHFCandidates=True #create an additionnal NoHF slimmed MET collection if the option is set to false
usePrivateSQlite=True #use external JECs (sqlite file)
applyResiduals=True #application of residual corrections. Have to be set to True once the 13 TeV residual corrections are available. False to be kept meanwhile. Can be kept to False later for private tests or for analysis checks and developments (not the official recommendation!).
#===================================================================

# Message Logger settings
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet( 
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False) 
)

# How many events to process
process.maxEvents = cms.untracked.PSet( 
   input = cms.untracked.int32(options.maxEvents)
)

### =====================================================================================================

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag.globaltag = options.GT

usePrivateSQlite = options.jecDBFile!=''
if usePrivateSQlite:
    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                               connect = cms.string('sqlite_file:'+os.path.expandvars(options.jecDBFile)),
                               toGet =  cms.VPSet(
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+options.jecEra+"_AK4PF"),
                label= cms.untracked.string("AK4PF")
                ),
            cms.PSet(
                record = cms.string("JetCorrectionsRecord"),
                tag = cms.string("JetCorrectorParametersCollection_"+options.jecEra+"_AK4PFchs"),
                label= cms.untracked.string("AK4PFchs")
                ),
           cms.PSet(record  = cms.string("JetCorrectionsRecord"),
                tag     = cms.string("JetCorrectorParametersCollection_"+options.jecEra+"_AK4PFPuppi"),
                label   = cms.untracked.string("AK4PFPuppi")
                ),
            )
                               )
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource",'jec')

### =====================================================================================================
#process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
from CondCore.DBCommon.CondDBSetup_cfi import *

##___________________________External JER file________________________________||
##https://github.com/cms-jet/JRDatabase/tree/master/SQLiteFiles

usePrivateSQliteJER = options.jerDBFile!=''
if usePrivateSQliteJER:
    process.jer = cms.ESSource("PoolDBESSource",CondDBSetup,
                               connect = cms.string('sqlite_file:'+os.path.expandvars(options.jerDBFile)),
                               toGet =  cms.VPSet(
            #######
            ### read the PFchs JER

            cms.PSet(
                record = cms.string('JetResolutionRcd'),
                #tag    = cms.string('JR_MC_PtResolution_Summer15_25nsV6_AK4PF'),
                tag    = cms.string('JR_'+options.jerEra+'_MC_PtResolution_AK4PFchs'),
                label  = cms.untracked.string('AK4PFchs_pt')
                ),
            cms.PSet(
                record = cms.string("JetResolutionRcd"),
                #tag = cms.string("JR_MC_PhiResolution_Summer15_25nsV6_AK4PF"),
                tag = cms.string('JR_'+options.jerEra+'_MC_PhiResolution_AK4PFchs'),
                label= cms.untracked.string("AK4PFchs_phi")
                ),
            cms.PSet(
                record = cms.string('JetResolutionScaleFactorRcd'),
                #tag    = cms.string('JR_DATAMCSF_Summer15_25nsV6_AK4PFchs'),
                tag    = cms.string('JR_'+options.jerEra+'_MC_SF_AK4PFchs'),
                label  = cms.untracked.string('AK4PFchs')
                ),

            #######
            ### read the Puppi JER

            cms.PSet(
                record = cms.string('JetResolutionRcd'),
                #tag    = cms.string('JR_MC_PtResolution_Summer15_25nsV6_AK4PF'),
                tag    = cms.string('JR_'+options.jerEra+'_MC_PtResolution_AK4PFPuppi'),
                label  = cms.untracked.string('AK4PFPuppi_pt')
                ),
            cms.PSet(
                record = cms.string("JetResolutionRcd"),
                #tag = cms.string("JR_MC_PhiResolution_Summer15_25nsV6_AK4PF"),
                tag = cms.string('JR_'+options.jerEra+'_MC_PhiResolution_AK4PFPuppi'),
                label= cms.untracked.string("AK4PFPuppi_phi")
                ),
            cms.PSet(
                record = cms.string('JetResolutionScaleFactorRcd'),
                #tag    = cms.string('JR_DATAMCSF_Summer15_25nsV6_AK4PFchs'),
                tag    = cms.string('JR_'+options.jerEra+'_MC_SF_AK4PFPuppi'),
                label  = cms.untracked.string('AK4PFPuppi')
                ),


            ) )
    process.es_prefer_jer = cms.ESPrefer("PoolDBESSource",'jer')



### =====================================================================================================

fname = 'root://eoscms.cern.ch//store/data/Run2015B/JetHT/MINIAOD/PromptReco-v1/000/251/252/00000/263D331F-AF27-E511-969B-02163E012627.root' if options.isData else 'root://eoscms//eos/cms/store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/Asympt50ns_MCRUN2_74_V9A-v2/60000/001C7571-0511-E511-9B8E-549F35AE4FAF.root'
# Define the input source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring([ fname ])
)

### ---------------------------------------------------------------------------
### Removing the HF from the MET computation
### ---------------------------------------------------------------------------
process.noHFCands = cms.EDFilter("CandPtrSelector",
                                 src=cms.InputTag("packedPFCandidates"),
                                 cut=cms.string("abs(pdgId)!=1 && abs(pdgId)!=2 && abs(eta)<3.0")
                                 )

### =====================================================================================================

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

#default configuration for miniAOD reprocessing, change the isData flag to run on data
#for a full met computation, remove the pfCandColl input
runMetCorAndUncFromMiniAOD(process,
                           isData=options.isData,
                           )


##https://twiki.cern.ch/twiki/bin/view/CMSPublic/ReMiniAOD03Feb2017Notes#MET_Recipes
if options.isData:
    from PhysicsTools.PatUtils.tools.corMETFromMuonAndEG import corMETFromMuonAndEG
    corMETFromMuonAndEG(process,
                        pfCandCollection="", #not needed
                        electronCollection="slimmedElectronsBeforeGSFix",
                        photonCollection="slimmedPhotonsBeforeGSFix",
                        corElectronCollection="slimmedElectrons",
                        corPhotonCollection="slimmedPhotons",
                        allMETEGCorrected=True,
                        muCorrection=False,
                        eGCorrection=True,
                        runOnMiniAOD=True,
                        postfix="MuEGClean"
                        )
    process.slimmedMETsMuEGClean = process.slimmedMETs.clone()
    process.slimmedMETsMuEGClean.src = cms.InputTag("patPFMetT1MuEGClean")
    process.slimmedMETsMuEGClean.rawVariation =  cms.InputTag("patPFMetRawMuEGClean")
    process.slimmedMETsMuEGClean.t1Uncertainties = cms.InputTag("patPFMetT1%sMuEGClean")
    del process.slimmedMETsMuEGClean.caloMET


if not useHFCandidates:
    runMetCorAndUncFromMiniAOD(process,
                               isData=options.isData,
                               pfCandColl=cms.InputTag("noHFCands"),
                               reclusterJets=True, #needed for NoHF
                               recoMetFromPFCs=True, #needed for NoHF
                               postfix="NoHF"
                               )

if options.redoPuppi:
    from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
    makePuppiesFromMiniAOD( process );

# recorrect only
#    runMetCorAndUncFromMiniAOD(process,
#                               isData=options.isData,
#                               metType="Puppi",
#                               postfix="Puppi"
#                               )

    runMetCorAndUncFromMiniAOD(process,
                               isData=options.isData,
                               metType="Puppi",
                               pfCandColl=cms.InputTag("puppiForMET"),
                               recoMetFromPFCs=True,
                               jetFlavor="AK4PFPuppi",
                               postfix="Puppi"
                               )

    ## temporary fix since we do not have good JEC yet
    process.basicJetsForMetPuppi.jetCorrEtaMax = cms.double(2.4)
    process.corrPfMetType1Puppi.jetCorrEtaMax = cms.double(2.4)



### -------------------------------------------------------------------
### the lines below remove the L2L3 residual corrections when processing data
### -------------------------------------------------------------------
if options.removeResiduals:
    process.patPFMetT1T2Corr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT1T2SmearCorr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2Corr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2SmearCorr.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.shiftedPatJetEnDown.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    process.shiftedPatJetEnUp.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")

    process.patPFMetT1T2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT1T2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2CorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.patPFMetT2SmearCorrNoHF.jetCorrLabelRes = cms.InputTag("L3Absolute")
    process.shiftedPatJetEnDownNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
    process.shiftedPatJetEnUpNoHF.jetCorrLabelUpToL3Res = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
### ------------------------------------------------------------------



process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = cms.untracked.vstring( "keep *_slimmedMETs*_*_*",
                                            "keep *_patPFMetT1Txy_*_*",
#                                            "keep patJets_*_*_RERUN", #for debugging only
                                            "keep *_slimmedMETsNoHF_*_*",
                                            "keep *_slimmedMETsPuppi_*_*",
                                            "keep *_patPFMetT1TxyNoHF_*_*",
                                            "keep *_puppiMETEGCor_*_*",
##                                            "keep *_*_*_RERUN",
                                            ),
    fileName = cms.untracked.string('corMETMiniAOD.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

if options.reclusterTrackJets:
    process.MessageLogger.destinations = ['cerr'] # temporarily avoid a lot of printouts
    process.MessageLogger.cerr.threshold = cms.untracked.string('ERROR') # temporarily avoid a lot of printouts
    process.pfChargedCHS = cms.EDFilter("CandPtrSelector", src = cms.InputTag("packedPFCandidates"), cut = cms.string("fromPV && charge!=0"))
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets
    process.ak4PFChargedJetsCHS = ak4PFJets.clone(src = 'pfChargedCHS', doAreaFastjet = True)
    from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
    addJetCollection(
        process,
        postfix = "",
        labelName = 'AK4ChargedPFCHS',
        jetSource = cms.InputTag('ak4PFChargedJetsCHS'),
        pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
        pfCandidates = cms.InputTag('packedPFCandidates'),
        svSource = cms.InputTag('slimmedSecondaryVertices'),
        btagDiscriminators = ['None'],
        jetCorrections = ('AK4PFchs', [], 'None'),
        genJetCollection = cms.InputTag('slimmedGenJets'),
        genParticles = cms.InputTag('prunedGenParticles'),
        algo = 'AK',
        rParam = 0.4
        )
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
    process.MINIAODSIMoutput.outputCommands.append("keep patJets_patJetsAK4ChargedPFCHS__RERUN")
    process.p = cms.Path(process.pfChargedCHS*process.ak4PFChargedJetsCHS*process.patJetsAK4ChargedPFCHS)


process.endpath = cms.EndPath(process.MINIAODSIMoutput)

ofile = os.path.expandvars(options.outputFile)
if os.path.isfile(ofile): os.remove(ofile)
dumpFile  = open(ofile, "w")
dumpFile.write(process.dumpPython())
dumpFile.close()
print "Written preprocessor cfg to %s"%ofile
