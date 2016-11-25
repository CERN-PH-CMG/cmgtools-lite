import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

###############################
####### Parameters ############
###############################
#options = VarParsing ('python')
#
#options.register('reportEvery', 1000,
#    VarParsing.multiplicity.singleton,
#    VarParsing.varType.int,
#    "Report every N events (default is N=10)"
#)
#options.register('wantSummary', False,
#    VarParsing.multiplicity.singleton,
#    VarParsing.varType.bool,
#    "Print out trigger and timing summary"
#)
#
### 'maxEvents' is already registered by the Framework, changing default value
#options.setDefault('maxEvents', 100)
#
#options.parseArguments()

process = cms.Process("RERUN")

process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff")
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000#options.reportEvery

### Events to process
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIISpring16MiniAODv2/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v4/00000/107D4288-EE2B-E611-8CDA-02163E0114CC.root'
    )
)

### Output file
#process.TFileService = cms.Service("TFileService",
#   fileName = cms.string(options.outputFilename)
#)

## Options and Output Report
process.options   = cms.untracked.PSet(
#    wantSummary = cms.untracked.bool(options.wantSummary),
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True)
)

#################################################
## Update PAT jets
#################################################

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
updateJetCollection(
   process,
   #jetSource = cms.InputTag('selectedUpdatedPatJetsNewJEC'),
   jetSource = cms.InputTag('slimmedJets'),                                                                                                                                                
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
   btagDiscriminators = [
    'deepFlavourJetTags:probudsg'        ,
    'deepFlavourJetTags:probb'           ,
    'deepFlavourJetTags:probc'           ,
    'deepFlavourJetTags:probbb'          ,
    'deepFlavourJetTags:probcc'          ,
    ]
)







process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",                     
    compressionAlgorithm = cms.untracked.string('LZMA'),    
    compressionLevel = cms.untracked.int32(4),              
    dataset = cms.untracked.PSet(   
        dataTier = cms.untracked.string(''),                
        filterName = cms.untracked.string('')               
    ),      
    dropMetaData = cms.untracked.string('ALL'),             
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),                   
    fastCloning = cms.untracked.bool(False),                
    fileName = cms.untracked.string('BTagging.root'),  
    outputCommands = cms.untracked.vstring(#'keep *',
                                           #'drop *_deepNNTagInfos*_*_*',
                                           'drop *',
                                           'keep *_selectedUpdatedPatJets*_*_*',
                                           ),
    overrideInputFileSplitLevels = cms.untracked.bool(True) 
)           
            
process.endpath = cms.EndPath(process.MINIAODSIMoutput)                                                                                                                                                     
