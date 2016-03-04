import FWCore.ParameterSet.Config as cms
# from CMGTools.Production.datasetToSource import datasetToSource
from CMGTools.H2TauTau.tools.setupJSON import setupJSON
# from CMGTools.H2TauTau.tools.setupRecoilCorrection import setupRecoilCorrection
# from CMGTools.H2TauTau.tools.setupEmbedding import setupEmbedding
# from CMGTools.H2TauTau.objects.jetreco_cff import addAK4Jets
from CMGTools.H2TauTau.tools.setupOutput import addTauMuOutput, addTauEleOutput, addDiTauOutput, addMuEleOutput, addDiMuOutput
from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET

def createProcess(runOnMC=True, channel='tau-mu', runSVFit=False,
                  p4TransferFunctionFile='CMGTools/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root', # Christians's default. If not touched, it would default to this anyways
                  integrateOverP4=False):
    '''Set up CMSSW process to run MVA MET and SVFit.

    Args:
        runOnMC (bool): run on MC (access to gen-level products) or data
        channel (string): choose from 'tau-mu' 'di-tau' 'tau-ele' 'mu-ele' 
                          'all-separate' 'all'
        runSVFit (bool): enables the svfit mass reconstruction used for the 
                         H->tau tau analysis.
    '''

    sep_line = '-'*70

    process = cms.Process("H2TAUTAU")

    # Adding jet collection
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    process.GlobalTag.globaltag = '76X_mcRun2_asymptotic_RunIIFall15DR76_v1'
    if not runOnMC:
        process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'

    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_38T_cff')

    runMVAMET(process, jetCollectionPF="patJetsReapplyJEC")

    
    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetCorrFactorsUpdated
    process.patJetCorrFactorsReapplyJEC = patJetCorrFactorsUpdated.clone(
        src=cms.InputTag("slimmedJets"),
        levels=['L1FastJet', 
            'L2Relative', 
            'L3Absolute'],
      payload='AK4PFchs'
    ) # Make sure to choose the appropriate levels and payload here!

    if not runOnMC:
        process.patJetCorrFactorsReapplyJEC.levels += ['L3Residual']

    from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import patJetsUpdated
    process.patJetsReapplyJEC = patJetsUpdated.clone(
        jetSource = cms.InputTag("slimmedJets"),
        jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
    )

    process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

    numberOfFilesToProcess = -1
    numberOfFilesToProcess = 1
    debugEventContent = False

    # increase to 1000 before running on the batch, to reduce size of log files
    # on your account
    reportInterval = 100

    print sep_line
    print 'channel', channel
    print 'runSVFit', runSVFit

    # Input & JSON             -------------------------------------------------

    # dataset_user = 'htautau_group'
    # dataset_name = '/VBF_HToTauTau_M-125_13TeV-powheg-pythia6/Spring14dr-PU20bx25_POSTLS170_V5-v1/AODSIM/SS14/'
    # dataset_files = 'miniAOD-prod_PAT_.*root'

    if runOnMC:
        from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import HiggsSUSYGG160 as ggh160
        process.source = cms.Source(
            "PoolSource",
            noEventSort = cms.untracked.bool(True),
            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
            fileNames = cms.untracked.vstring(ggh160.files)
        )
    else:
        # from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_Promptv4
        process.source = cms.Source(
            "PoolSource",
            noEventSort = cms.untracked.bool(True),
            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
            fileNames = cms.untracked.vstring('root://eoscms.cern.ch//eos/cms/store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v4/000/258/159/00000/6CA1C627-246C-E511-8A6A-02163E014147.root')
        )


    if runOnMC:
        process.genEvtWeightsCounter = cms.EDProducer(
            'GenEvtWeightCounter',
            verbose = cms.untracked.bool(False)
        )

    if numberOfFilesToProcess > 0:
        process.source.fileNames = process.source.fileNames[:numberOfFilesToProcess]

    print 'Run on MC?', runOnMC, process.source.fileNames[0]

    if not runOnMC:
        print 'Running on data, setting up JSON file'
        json = setupJSON(process)


    # Message logger setup.
    process.load("FWCore.MessageLogger.MessageLogger_cfi")
    process.MessageLogger.cerr.FwkReport.reportEvery = reportInterval
    process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

    process.options = cms.untracked.PSet(
        allowUnscheduled=cms.untracked.bool(True)
    )


    # process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
    # process.load('JetMETCorrections.Configuration.JetCorrectors_cff')


    # # if '25ns' in process.source.fileNames[0] or 'mcRun2_asymptotic_v2' in process.source.fileNames[0]:
    # print 'Using 25 ns MVA MET training'
    # for mvaMETCfg in [process.mvaMETTauMu, process.mvaMETTauEle, process.mvaMETDiMu, process.mvaMETDiTau, process.mvaMETMuEle]:
    #     mvaMETCfg.inputFileNames = cms.PSet(
    #     U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru_7_4_X_miniAOD_25NS_July2015.root'),
    #     DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrphi_7_4_X_miniAOD_25NS_July2015.root'),
    #     CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_7_4_X_miniAOD_25NS_July2015.root'),
    #     CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_7_4_X_miniAOD_25NS_July2015.root')
    # )

    # load the channel paths -------------------------------------------

    process.MVAMET.requireOS = cms.bool(False)

    if channel == 'tau-mu':
        process.load('CMGTools.H2TauTau.objects.tauMuObjectsMVAMET_cff')
        process.mvaMETTauMu = process.MVAMET.clone()
        process.mvaMETTauMu.srcLeptons = cms.VInputTag("tauPreSelectionTauMu", "muonPreSelectionTauMu")
        process.mvaMETTauMu.MVAMETLabel = cms.string('mvaMETTauMu')
        process.cmgTauMu.metCollection = cms.InputTag('mvaMETTauMu', 'mvaMETTauMu')
        if not runSVFit:
            process.cmgTauMuCorSVFitPreSel.SVFitVersion = 0
        if integrateOverP4:
            process.cmgTauMuCorSVFitPreSel.integrateOverP4 = integrateOverP4
        if p4TransferFunctionFile:
            process.cmgTauMuCorSVFitPreSel.p4TransferFunctionFile = p4TransferFunctionFile

    elif channel == 'tau-ele':
        process.load('CMGTools.H2TauTau.objects.tauEleObjectsMVAMET_cff')
        process.mvaMETTauEle = process.MVAMET.clone()
        process.mvaMETTauEle.srcLeptons = cms.VInputTag("tauPreSelectionTauEle", "electronPreSelectionTauEle")
        process.mvaMETTauEle.MVAMETLabel = cms.string('mvaMETTauEle')
        process.cmgTauEle.metCollection = cms.InputTag('mvaMETTauEle', 'mvaMETTauEle')
        if not runSVFit:
            process.cmgTauEleCorSVFitPreSel.SVFitVersion = 0

    elif channel == 'mu-ele':
        process.load('CMGTools.H2TauTau.objects.muEleObjectsMVAMET_cff')
        process.mvaMETMuEle = process.MVAMET.clone()
        process.mvaMETMuEle.srcLeptons = cms.VInputTag("muonPreSelectionMuEle", "electronPreSelectionMuEle")
        process.mvaMETMuEle.MVAMETLabel = cms.string('mvaMETMuEle')
        process.cmgMuEle.metCollection = cms.InputTag('mvaMETMuEle', 'mvaMETMuEle')
        if not runSVFit:
            process.cmgMuEleCorSVFitPreSel.SVFitVersion = 0
        else:
            process.cmgMuEleCorSVFitPreSel.SVFitVersion = 2

    # elif channel == 'mu-ele':
    #     process.MVAMET.srcLeptons = cms.VInputTag("electronPreSelectionMuEle", "muonPreSelectionMuEle")
    #     # process.muEleSequence.insert(4, process.MVAMET)
    # elif channel == 'di-tau':
    #     process.MVAMET.srcLeptons = cms.VInputTag("tauPreSelectionDiTau", "tauPreSelectionDiTau")
    #     # process.diTauSequence.insert(2, process.MVAMET)
    # elif channel == 'di-mu':
    #     process.MVAMET.srcLeptons = cms.VInputTag("muonPreSelectionDiMu", "muonPreSelectionDiMu")
    #     # process.diMuSequence.insert(2, process.MVAMET)


    # OUTPUT definition ----------------------------------------------------------
    process.outpath = cms.EndPath()


    if runOnMC:
        pass
        # process.genEvtWeightsCounterPath = cms.Path(process.genEvtWeightsCounter)
        # process.schedule.insert(0, process.genEvtWeightsCounterPath)

    # Enable printouts like this:
    # process.cmgTauMuCorSVFitPreSel.verbose = True

    oneFile = (channel == 'all')

    if channel == 'tau-mu' or 'all' in channel:
        addTauMuOutput(process, debugEventContent, addPreSel=False, oneFile=oneFile)
    if channel == 'tau-ele' or 'all' in channel:
        addTauEleOutput(process, debugEventContent, addPreSel=False, oneFile=oneFile)
    if channel == 'mu-ele' or 'all' in channel:
        addMuEleOutput(process, debugEventContent, addPreSel=False, oneFile=oneFile)
    if channel == 'di-mu' or 'all' in channel:
        addDiMuOutput(process, debugEventContent, addPreSel=False, oneFile=oneFile)
    if channel == 'di-tau' or 'all' in channel:
        addDiTauOutput(process, debugEventContent, addPreSel=False, oneFile=oneFile)



    # if not runOnMC:
    #     # process.tauMuSequence.remove(process.cmgTauMuCor)
    #     process.cmgTauMuTauPtSel.src = 'cmgTauMu'
    #     # process.tauEleSequence.remove(process.cmgTauEleCor)
    #     process.cmgTauEleTauPtSel.src = 'cmgTauEle'
    #     # process.diTauSequence.remove(process.cmgDiTauCor)
    #     process.cmgDiTauTauPtSel.src = 'cmgDiTau'

#    if runSVFit:
#        process.cmgTauMuCorSVFitPreSel.SVFitVersion = 2
        # process.cmgTauEleCorSVFitPreSel.SVFitVersion = 2
        # process.cmgDiTauCorSVFitPreSel.SVFitVersion = 2
        # process.cmgMuEleCorSVFitPreSel.SVFitVersion = 2
        # process.cmgDiMuCorSVFitPreSel.SVFitVersion = 2
#    else:
#        process.cmgTauMuCorSVFitPreSel.SVFitVersion = 0
        # process.cmgTauEleCorSVFitPreSel.SVFitVersion = 0
        # process.cmgDiTauCorSVFitPreSel.SVFitVersion = 0
        # process.cmgMuEleCorSVFitPreSel.SVFitVersion = 0
        # process.cmgDiMuCorSVFitPreSel.SVFitVersion = 0

    # if integrateOverP4:
    #     process.cmgTauMuCorSVFitPreSel.integrateOverP4 = integrateOverP4
    #     process.cmgTauEleCorSVFitPreSel.integrateOverP4 = integrateOverP4
    #     process.cmgDiTauCorSVFitPreSel.integrateOverP4 = integrateOverP4
    #     process.cmgMuEleCorSVFitPreSel.integrateOverP4 = integrateOverP4

    # if p4TransferFunctionFile:
    #     process.cmgTauMuCorSVFitPreSel.p4TransferFunctionFile = p4TransferFunctionFile
    #     process.cmgTauEleCorSVFitPreSel.p4TransferFunctionFile = p4TransferFunctionFile
    #     process.cmgDiTauCorSVFitPreSel.p4TransferFunctionFile = p4TransferFunctionFile
    #     process.cmgMuEleCorSVFitPreSel.p4TransferFunctionFile = p4TransferFunctionFile

    print sep_line
    print 'INPUT:'
    print sep_line
    print process.source.fileNames
    print
    if not runOnMC:
        print 'json:', json
    print
    print sep_line
    print 'PROCESSING'
    print sep_line
    print 'runOnMC:', runOnMC
    print

    # from FWCore.ParameterSet.Utilities import convertToUnscheduled
    # convertToUnscheduled(process)

    return process

# if __name__ == '__main__':
#     process = createProcess()

process = createProcess()
