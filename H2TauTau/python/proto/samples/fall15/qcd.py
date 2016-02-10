import PhysicsTools.HeppyCore.framework.config as cfg

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

QCDMu20ToInf = creator.makeMCComponent('QCDMu20ToInf', '/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM', 'CMS', '.*root', 720648000 )

qcd_total = [
    QCDMu20ToInf
]

qcd_mu = [
    QCDMu20ToInf
]

