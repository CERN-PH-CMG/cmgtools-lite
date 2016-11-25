from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

# SMS_TChiStauStau = creator.makeMCComponent(
#     "SMS_TChiStauStau", "/SMS-TChiStauStau_x0p5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 1.0)

SMS_TStauStau = creator.makeMCComponent(
    "SMS_TStauStau", "/SMS-TStauStau_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 1.0)

SMS_TChipmStauSnu = creator.makeMCComponent('SMS_TChipmStauSnu', '/SMS-TChipmStauSnu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 'CMS', '.*root', 1.0)

samples_susy = [SMS_TStauStau, SMS_TChipmStauSnu]#SMS_TChiStauStau
