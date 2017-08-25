from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()


SMS_TStauStau_lefthanded = creator.makeMCComponent(
    "SMS_TStauStau_lefthanded", "/SMS-TStauStau_lefthanded_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUSummer16Fast_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1.0)

SMS_TStauStau_righthanded = creator.makeMCComponent(
    "SMS_TStauStau_righthanded", "/SMS-TStauStau_righthanded_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUSummer16Fast_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1.0)

SMS_TStauStau_maximalmixing = creator.makeMCComponent(
    "SMS_TStauStau_maximalmixing", "/SMS-TStauStau_maximalmixing_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUSummer16Fast_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 1.0)

SMS_TChipmStauSnu = creator.makeMCComponent('SMS_TChipmStauSnu', '/SMS-TChipmStauSnu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM', 'CMS', '.*root', 1.0)

TChiStauStau_x0p5 = creator.makeMCComponent('TChiStauStau_x0p5', '/SMS-TChiStauStau_x0p5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM', 'CMS', '.*root', 1.0)

TChiStauStau_x0p5_ext = creator.makeMCComponent('TChiStauStau_x0p5_ext', '/SMS-TChiStauStau_x0p5_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM', 'CMS', '.*root', 1.0)


samples_susy = [TChiStauStau_x0p5, TChiStauStau_x0p5_ext, SMS_TChipmStauSnu, SMS_TStauStau_lefthanded, SMS_TStauStau_righthanded, SMS_TStauStau_maximalmixing]
