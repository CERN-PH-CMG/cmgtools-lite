#####COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


## SqGltttt
## ------------------------------------------------------
#SqGltttt_mGo1300_mSq1300_mChi100 = kreator.makeMCComponentFromEOS('SqGltttt_mGo1300_mSq1300_mChi100', '/13TeV_SqGltttt_Gl_1300_Sq_1300_LSP_100/', '/store/cmst3/group/susy/alobanov/MC/PHYS14/PU20_25ns/%s', '.*root')
SqGltttt = [ ]


## T1ttbb
## ------------------------------------------------------
#T1ttbb_mGo1500_mChi100 = kreator.makeMCComponentFromEOS('T1ttbb_mGo1500_mChi100', '/T1ttbb_2J_mGo1500_mChi100_3bodydec_asymmDecOnly/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0141903)
T1ttbb = [ ]


## T1ttbbWW
## ------------------------------------------------------
#T1ttbbWW_mGo1000_mCh725_mChi715 = kreator.makeMCComponentFromEOS('T1ttbbWW_mGo1000_mCh725_mChi715', '/T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388)
#T1ttbbWW_mGo1000_mCh725_mChi720 = kreator.makeMCComponentFromEOS('T1ttbbWW_mGo1000_mCh725_mChi720', '/T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388)
#T1ttbbWW_mGo1300_mCh300_mChi290 = kreator.makeMCComponentFromEOS('T1ttbbWW_mGo1300_mCh300_mChi290', '/T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0460525)
#T1ttbbWW_mGo1300_mCh300_mChi295 = kreator.makeMCComponentFromEOS('T1ttbbWW_mGo1300_mCh300_mChi295', '/T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0460525)
T1ttbbWW = [ ]


 
## T1tttt
## ------------------------------------------------------
T1tttt_mGo1500_mChi100 = kreator.makeMCComponent("T1tttt_mGo1500_mChi100", "/SMS-T1tttt_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/MINIAODSIM", "CMS", ".*root")
T1tttt_mGo1200_mChi800 = kreator.makeMCComponent("T1tttt_mGo1200_mChi800", "/SMS-T1tttt_mGluino-1200_mLSP-800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root")
T1tttt = [ T1tttt_mGo1500_mChi100, T1tttt_mGo1200_mChi800 ] 


## T2tt
## ------------------------------------------------------
#T2tt_arxiv150701601 = kreator.makeMCComponentFromEOS('T2tt_arxiv150701601', '/T2tt_arxiv1507.01601/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.000296128)

T2tt = []


## T2ttDeg
## ------------------------------------------------------
#T2ttDeg_mStop350_mChi330_4bodydec = kreator.makeMCComponentFromEOS('T2ttDeg_mStop350_mChi330_4bodydec', '/T2ttDeg_mStop350_mChi330_4bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.003787)
T2ttDeg_mStop350_mChi330_4bodydec_lepOnly = kreator.makeMCComponentFromEOS('T2ttDeg_mStop350_mChi330_4bodydec_lepOnly', '/T2ttDeg_miniAODSIM_76X_lepOnly_dM20gev/','/store/user/castello/susy/%s',".*root", 3.787*(0.332)*(0.332))
T2ttDeg_mStop350_mChi315_4bodydec_lepOnly = kreator.makeMCComponentFromEOS('T2ttDeg_mStop350_mChi315_4bodydec_lepOnly', '/T2ttDeg_mStop350_mChi315_4bodydec_lepOnly_for76X/','/store/cmst3/group/susy/gpetrucc/13TeV/RunIIFall15MiniAODv2/%s',".*root", 3.787*(0.332)*(0.332))
T2ttDeg_mStop350_mChi300_4bodydec_lepOnly = kreator.makeMCComponentFromEOS('T2ttDeg_mStop350_mChi300_4bodydec_lepOnly', '/T2ttDeg_mStop350_mChi300_4bodydec_lepOnly_for76X/','/store/cmst3/group/susy/gpetrucc/13TeV/RunIIFall15MiniAODv2/%s',".*root", 3.787*(0.332)*(0.332))
T2ttDeg = [ T2ttDeg_mStop350_mChi330_4bodydec_lepOnly, T2ttDeg_mStop350_mChi315_4bodydec_lepOnly, T2ttDeg_mStop350_mChi300_4bodydec_lepOnly ]



## T5qqqqWW
## ------------------------------------------------------
#T5qqqqWW_mGo1200_mCh1000_mChi800_dilep = kreator.makeMCComponentFromEOS('T5qqqqWW_mGo1200_mCh1000_mChi800_dilep', '/T5qqqqWW_mGo1200_mCh1000_mChi800_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0856418*(3*0.108)*(3*0.108)) 
#T5qqqqWW_mGo1500_mCh800_mChi100 = kreator.makeMCComponentFromEOS('T5qqqqWW_mGo1500_mCh800_mChi100', '/SMS_T5qqqqWW_Gl1500_Chi800_LSP100/', '/store/cmst3/group/susy/alobanov/MC/PHYS14/PU20_25ns/%s', '.*root', 0.0141903)
#T5qqqqWW_mGo1200_mCh1000_mChi800 = kreator.makeMCComponentFromEOS('T5qqqqWW_mGo1200_mCh1000_mChi800', '/SMS_T5qqqqWW_Gl1200_Chi1000_LSP800/', '/store/cmst3/group/susy/alobanov/MC/PHYS14/PU20_25ns/%s', '.*root', 0.0856418)
#T5qqqqWW_mGo1000_mCh800_mChi700 = kreator.makeMCComponentFromEOS('T5qqqqWW_mGo1000_mCh800_mChi700', '/T5qqqqWW_mGo1000_mCh800_mChi700/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388) 
#T5qqqqWW_mGo1000_mCh800_mChi700_dilep= kreator.makeMCComponentFromEOS('T5qqqqWW_mGo1000_mCh800_mChi700_dilep', '/T5qqqqWW_mGo1000_mCh800_mChi700_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(3*0.108)*(3*0.108)) 
#T5qqqqWW_mGo1200_mCh1000_mChi800_cmg = kreator.makeMCComponentFromEOS('T5qqqqWW_mGo1200_mCh1000_mChi800_cmg', '/T5qqqqWW_mGo1200_mCh1000_mChi800/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0856418) 
T5qqqqWW = [  ]


## T5qqqqWZ
## ------------------------------------------------------
#T5qqqqWZ_mGo1200_mCh1000_mChi800_dilep = kreator.makeMCComponentFromEOS('T5qqqqWZ_mGo1200_mCh1000_mChi800_lep', '/T5qqqqWZ_mGo1200_mCh1000_mChi800_lep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0141903*(3*0.108)*(3*0.03366)) 
#T5qqqqWZ_mGo1500_mCh800_mChi100_dilep = kreator.makeMCComponentFromEOS('T5qqqqWZ_mGo1500_mCh800_mChi100_lep', '/T5qqqqWZ_mGo1500_mCh800_mChi100_lep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0856418*(3*0.108)*(3*0.03366)) 
T5qqqqWZ = [  ]


## T5qqqqZZ
## ------------------------------------------------------
#T5qqqqZZ_mGo1200_mCh1000_mChi800_dilep = kreator.makeMCComponentFromEOS('T5qqqqZZ_mGo1200_mCh1000_mChi800_lep', '/T5qqqqZZ_mGo1200_mCh1000_mChi800_lep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0141903*(3*0.03366)*(3*0.03366)) 
#T5qqqqZZ_mGo1500_mCh800_mChi100_dilep = kreator.makeMCComponentFromEOS('T5qqqqZZ_mGo1500_mCh800_mChi100_lep', '/T5qqqqZZ_mGo1500_mCh800_mChi100_lep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0856418*(3*0.03366)*(3*0.03366)) 
T5qqqqZZ = [ ]


## T5qqqqVV
## ------------------------------------------------------
T5qqqqVV = T5qqqqWW + T5qqqqWZ + T5qqqqZZ


## T5qqqqWWDeg
## ------------------------------------------------------
#T5qqqqWWDeg_mGo1000_mCh315_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1000_mCh315_mChi300_dilep', '/T5qqqqWWDeg_mGo1000_mCh315_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.333)*(0.333)) 
#T5qqqqWWDeg_mGo1000_mCh325_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1000_mCh325_mChi300_dilep', '/T5qqqqWWDeg_mGo1000_mCh325_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.324)*(0.324)) 
#T5qqqqWWDeg_mGo1400_mCh315_mChi300 = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1400_mCh315_mChi300', '/SMS_T5qqqqWW_mGl1400_mChi315_mLSP300/', '/store/cmst3/group/susy/alobanov/MC/PHYS14/PU20_25ns/%s', '.*root', 0.0252977)
#T5qqqqWWDeg_mGo1000_mCh310_mChi300 = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1000_mCh310_mChi300', '/T5qqqqWWDeg_mGo1000_mCh310_mChi300/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388) 
#T5qqqqWWDeg_mGo1000_mCh310_mChi300_dilep= kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1000_mCh310_mChi300_dilep', '/T5qqqqWWDeg_mGo1000_mCh310_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.333)*(0.333)) 
#T5qqqqWWDeg_mGo1000_mCh315_mChi300 = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1000_mCh315_mChi300', '/T5qqqqWWDeg_mGo1000_mCh315_mChi300/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388) 
#T5qqqqWWDeg_mGo1000_mCh325_mChi300 = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo1000_mCh325_mChi300', '/T5qqqqWWDeg_mGo1000_mCh325_mChi300/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388) 
#T5qqqqWWDeg_mGo800_mCh305_mChi300 = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo800_mCh305_mChi300', '/T5qqqqWWDeg_mGo800_mCh305_mChi300/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 1.4891) 
#T5qqqqWWDeg_mGo800_mCh305_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqWWDeg_mGo800_mCh305_mChi300_dilep', '/T5qqqqWWDeg_mGo800_mCh305_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 1.4891*(0.342)*(0.342)) 
T5qqqqWWDeg = [  ]


## T5qqqqWZDeg
## ------------------------------------------------------
#T5qqqqWZDeg_mGo1000_mCh315_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqWZDeg_mGo1000_mCh315_mChi300_dilep', '/T5qqqqWZDeg_mGo1000_mCh315_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.333)*(0.112)) 
#T5qqqqWZDeg_mGo1000_mCh325_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqWZDeg_mGo1000_mCh325_mChi300_dilep', '/T5qqqqWZDeg_mGo1000_mCh325_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.324)*(0.108)) 
T5qqqqWZDeg = [  ]


## T5qqqqZZDeg
## ------------------------------------------------------
T5qqqqZZDeg_mGo1000_mCh315_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqZZDeg_mGo1000_mCh315_mChi300_dilep', '/T5qqqqZZDeg_mGo1000_mCh315_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.112)*(0.112)) 
T5qqqqZZDeg_mGo1000_mCh325_mChi300_dilep = kreator.makeMCComponentFromEOS('T5qqqqZZDeg_mGo1000_mCh325_mChi300_dilep', '/T5qqqqZZDeg_mGo1000_mCh325_mChi300_dilep/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388*(0.108)*(0.108)) 
T5qqqqZZDeg = [ T5qqqqZZDeg_mGo1000_mCh315_mChi300_dilep, T5qqqqZZDeg_mGo1000_mCh325_mChi300_dilep ]


## T5qqqqVVDeg
## ------------------------------------------------------
T5qqqqVVDeg = T5qqqqWWDeg + T5qqqqWZDeg + T5qqqqZZDeg


## T5ttttDeg
## ------------------------------------------------------
#T5ttttDeg_mGo1000_mStop300_mCh285_mChi280 = kreator.makeMCComponentFromEOS('T5ttttDeg_mGo1000_mStop300_mCh285_mChi280', '/T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_23bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388)
#T5ttttDeg_mGo1000_mStop300_mChi280 = kreator.makeMCComponentFromEOS('T5ttttDeg_mGo1000_mStop300_mChi280', '/T5ttttDeg_mGo1000_mStop300_mChi280_4bodydec/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388)
#T5ttttDeg_mGo1300_mStop300_mChi280 = kreator.makeMCComponentFromEOS('T5ttttDeg_mGo1300_mStop300_mChi280', '/T5ttttDeg_mGo1300_mStop300_mChi280_4bodydec_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0460525)
#T5ttttDeg_mGo1300_mStop300_mCh285_mChi280 = kreator.makeMCComponentFromEOS('T5ttttDeg_mGo1300_mStop300_mCh285_mChi280', '/T5ttttDeg_mGo1300_mStop300_mCh285_mChi280_23bodydec_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0460525)
#T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_dil = kreator.makeMCComponentFromEOS('T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_dil', '/T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_23bodydec_dilepfilterPt8p5_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.325388)
#T5ttttDeg_mGo1300_mStop300_mCh285_mChi280_dil = kreator.makeMCComponentFromEOS('T5ttttDeg_mGo1300_mStop300_mCh285_mChi280_dil', '/T5ttttDeg_mGo1300_mStop300_mCh285_mChi280_23bodydec_dilepfilterPt8p5_v2/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.0460525)
T5ttttDeg = [  ]


## T6ttWW
## ------------------------------------------------------
#T6ttWW_mSbot600_mCh425_mChi50 = kreator.makeMCComponentFromEOS('T6ttWW_mSbot600_mCh425_mChi50', '/T6ttWW_600_425_50/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.174599)
#T6ttWW_mSbot650_mCh150_mChi50 = kreator.makeMCComponentFromEOS('T6ttWW_mSbot650_mCh150_mChi50', '/T6ttWW_650_150_50/', '/store/cmst3/group/susy/gpetrucc/13TeV/RunIISpring15DR74/%s',".*root", 0.107045)
T6ttWW = [  ]


## T6qqWW
## ------------------------------------------------------
## note: cross section for q~ q~ from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVsquarkantisquark (i.e. gluinos and stops decoupled)
##T6qqWW_mSq950_mCh325_mChi300 = kreator.makeMCComponentFromEOS('T6qqWW_mSq950_mCh325_mChi300', '/SMS_T6qqWW_mSq950_mChi325_mLSP300/', '/store/cmst3/group/susy/alobanov/MC/PHYS14/PU20_25ns/%s', '.*root', 0.0898112)
T6qqWW = [ ]


## TChiNeuSlepSneu (flavor-democratic)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: chi2->sleplep (0.5)
TChiNeuSlepSneu_mCh750_mChi100    = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh750_mChi100'   , '/TChiNeuSlepSneu_mCh750_mChi100/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.00669356*0.5)
TChiNeuSlepSneu_mCh450_mChi300    = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh450_mChi300'   , '/TChiNeuSlepSneu_mCh450_mChi300/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0734361 *0.5)
TChiNeuSlepSneu_mCh300_mChi270    = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh300_mChi270'   , '/TChiNeuSlepSneu_mCh300_mChi270/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.386936  *0.5)
TChiNeuSlepSneu = [TChiNeuSlepSneu_mCh750_mChi100, TChiNeuSlepSneu_mCh450_mChi300, TChiNeuSlepSneu_mCh300_mChi270]


## TChiNeuSlepSneu_TE (tau-enriched)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: chi1->stauneu or tausneu (0.33), chi2->stautau (0.5*0.33)
TChiNeuSlepSneu_mCh750_mChi100_TE = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh750_mChi100_TE', '/TChiNeuSlepSneu_mCh750_mChi100_TE/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.00669356*0.5*0.33)
TChiNeuSlepSneu_mCh450_mChi300_TE = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh450_mChi300_TE', '/TChiNeuSlepSneu_mCh450_mChi300_TE/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0734361 *0.5*0.33)
TChiNeuSlepSneu_mCh300_mChi270_TE = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh300_mChi270_TE', '/TChiNeuSlepSneu_mCh300_mChi270_TE/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.386936  *0.5*0.33)
TChiNeuSlepSneu_TE = [TChiNeuSlepSneu_mCh750_mChi100_TE, TChiNeuSlepSneu_mCh450_mChi300_TE, TChiNeuSlepSneu_mCh300_mChi270_TE]


## TChiNeuSlepSneu_TD (tau-dominated)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: chi2->stautau (0.5*0.33)
TChiNeuSlepSneu_mCh750_mChi100_TD = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh750_mChi100_TD', '/TChiNeuSlepSneu_mCh750_mChi100_TD/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.00669356*0.5*0.33*0.33)
TChiNeuSlepSneu_mCh450_mChi300_TD = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh450_mChi300_TD', '/TChiNeuSlepSneu_mCh450_mChi300_TD/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0734361 *0.5*0.33*0.33)
TChiNeuSlepSneu_mCh300_mChi270_TD = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh300_mChi270_TD', '/TChiNeuSlepSneu_mCh300_mChi270_TD/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.386936  *0.5*0.33*0.33)
TChiNeuSlepSneu_TD = [TChiNeuSlepSneu_mCh750_mChi100_TD, TChiNeuSlepSneu_mCh450_mChi300_TD, TChiNeuSlepSneu_mCh300_mChi270_TD]


## TChiNeuSlepSneu_SS (flavor-democratic, same-sign)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: chi2->sleplep (0.5)
TChiNeuSlepSneu_mCh450_mChi300_SS95 = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh450_mChi300_SS95', '/TChiNeuSlepSneu_mCh450_mChi300_SS95/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0734361*0.5)
TChiNeuSlepSneu_mCh300_mChi270_SS95 = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh300_mChi270_SS95', '/TChiNeuSlepSneu_mCh300_mChi270_SS95/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.386936 *0.5)
TChiNeuSlepSneu_mCh450_mChi300_SS05 = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh450_mChi300_SS05', '/TChiNeuSlepSneu_mCh450_mChi300_SS05/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0734361*0.5)
TChiNeuSlepSneu_mCh300_mChi270_SS05 = kreator.makeMCComponentFromEOS('TChiNeuSlepSneu_mCh300_mChi270_SS05', '/TChiNeuSlepSneu_mCh300_mChi270_SS05/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.386936 *0.5)
TChiNeuSlepSneu_SS = [TChiNeuSlepSneu_mCh450_mChi300_SS95, TChiNeuSlepSneu_mCh300_mChi270_SS95, TChiNeuSlepSneu_mCh450_mChi300_SS05, TChiNeuSlepSneu_mCh300_mChi270_SS05]


## TChiChiSlepSneu (flavor-democratic)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: 1.0
TChiChiSlepSneu_mCh350_mChi200    = kreator.makeMCComponentFromEOS('TChiChiSlepSneu_mCh350_mChi200'   , '/TChiChiSlepSneu_mCh350_mChi200/'   , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.209439  )
TChiChiSlepSneu_mCh600_mChi50     = kreator.makeMCComponentFromEOS('TChiChiSlepSneu_mCh600_mChi50'    , '/TChiChiSlepSneu_mCh600_mChi50/'    , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0201372 )
TChiChiSlepSneu = [ TChiChiSlepSneu_mCh350_mChi200, TChiChiSlepSneu_mCh600_mChi50]


## TChiNeuWH (multi-lepton)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: H->tautau, ZZ, WW (0.0632+0.264+0.022), Z->ll (0.10099), W->lnu (0.3257)
TChiNeuWH_mCh250_mChi20  = kreator.makeMCComponentFromEOS('TChiNeuWH_mCh250_mChi20', '/TChiNeuWH_mCh250_mChi20/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.782487*0.3492*0.10099*0.3257*0.3257)
TChiNeuWH_mCh150_mChi20  = kreator.makeMCComponentFromEOS('TChiNeuWH_mCh150_mChi20', '/TChiNeuWH_mCh150_mChi20/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 5.18086 *0.3492*0.10099*0.3257*0.3257)
TChiNeuWH  = [ TChiNeuWH_mCh250_mChi20, TChiNeuWH_mCh150_mChi20 ]


## TChiNeuWH_SL (single-lepton)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: W->lnu (0.3257)
TChiNeuWH_mCh250_mChi20_SL  = kreator.makeMCComponentFromEOS('TChiNeuWH_mCh250_mChi20_SL', '/TChiNeuWH_mCh250_mChi20_SL/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.782487*0.3257)
TChiNeuWH_mCh150_mChi20_SL  = kreator.makeMCComponentFromEOS('TChiNeuWH_mCh150_mChi20_SL', '/TChiNeuWH_mCh150_mChi20_SL/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 5.18086 *0.3257)
TChiNeuWH_SL  = [ TChiNeuWH_mCh250_mChi20_SL, TChiNeuWH_mCh150_mChi20_SL ]


## TChiNeuWZ (multi-lepton)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: Z->ll (0.10099), W->lnu (0.3257)
TChiNeuWZ_mCh350_mChi20  = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh350_mChi20' , '/TChiNeuWZ_mCh350_mChi20/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.209439*0.10099*0.3257)
TChiNeuWZ_mCh350_mChi100 = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh350_mChi100', '/TChiNeuWZ_mCh350_mChi100/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.209439*0.10099*0.3257)
TChiNeuWZ_mCh200_mChi100 = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh200_mChi100', '/TChiNeuWZ_mCh200_mChi100/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 1.80739 *0.10099*0.3257)
TChiNeuWZ_mCh150_mChi120 = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh150_mChi120', '/TChiNeuWZ_mCh150_mChi120/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 5.18086 *0.10099*0.3257)
TChiNeuWZ  = [ TChiNeuWZ_mCh350_mChi100, TChiNeuWZ_mCh350_mChi20, TChiNeuWZ_mCh200_mChi100, TChiNeuWZ_mCh150_mChi120 ]


## TChiNeuWZ_OS (opposite-sign)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn2x1wino
## BR: compressed from https://www.dropbox.com/s/84iatcyjwegv9nj/susy-degenerate-BRs.pdf?dl=0
TChiNeuWZ_mCh100_mChi95  = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh100_mChi95' , '/TChiWZDeg_miniAODSIM_76X_lepOnly_dM5gev/' , '/store/user/castello/susy/%s', ".*root", 22.67*0.112)
TChiNeuWZ_mCh100_mChi90  = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh100_mChi90' , '/TChiWZDeg_miniAODSIM_76X_lepOnly_dM10gev/', '/store/user/castello/susy/%s', ".*root", 22.67*0.112)
TChiNeuWZ_mCh100_mChi80  = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh100_mChi80' , '/TChiWZDeg_miniAODSIM_76X_lepOnly_dM20gev/', '/store/user/castello/susy/%s', ".*root", 22.67*0.112)
## BR: Z->ll (0.10099)
TChiNeuWZ_mCh350_mChi20_OS  = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh350_mChi20_OS' , '/TChiNeuWZ_mCh350_mChi20_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.209439*0.10099)
TChiNeuWZ_mCh350_mChi100_OS = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh350_mChi100_OS', '/TChiNeuWZ_mCh350_mChi100_OS/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.209439*0.10099)
TChiNeuWZ_mCh200_mChi100_OS = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh200_mChi100_OS', '/TChiNeuWZ_mCh200_mChi100_OS/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 1.80739 *0.10099)
TChiNeuWZ_mCh150_mChi120_OS = kreator.makeMCComponentFromEOS('TChiNeuWZ_mCh150_mChi120_OS', '/TChiNeuWZ_mCh150_mChi120_OS/', '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 5.18086 *0.10099)
TChiNeuWZ_OS = [ TChiNeuWZ_mCh100_mChi95, TChiNeuWZ_mCh100_mChi90, TChiNeuWZ_mCh100_mChi80, TChiNeuWZ_mCh350_mChi100_OS, TChiNeuWZ_mCh350_mChi20_OS, TChiNeuWZ_mCh200_mChi100_OS, TChiNeuWZ_mCh150_mChi120_OS ]


## TSlepSlep
## ------------------------------------------------------
## NO XSEC IS PUT HERE! samples are inclusive in handedness, need
## to put the value separately in your analyzer code!
TSlepSlep_mSlep300_mChi20 = kreator.makeMCComponentFromEOS('TSlepSlep_mSlep300_mChi20' , '/TSlepSlep_mSlep300_mChi20/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 1.)
TSlepSlep_mSlep150_mChi60 = kreator.makeMCComponentFromEOS('TSlepSlep_mSlep150_mChi60' , '/TSlepSlep_mSlep150_mChi60/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 1.)
TSlepSlep = [ TSlepSlep_mSlep300_mChi20, TSlepSlep_mSlep150_mChi60 ]


## TNeuNeuZZ (multi-lepton)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn1n2hino
## BR: ZZ->4l (0.10099*0.10099)
TNeuNeuZZ_mNeu400_mChi1 = kreator.makeMCComponentFromEOS('TNeuNeuZZ_mNeu400_mChi1' , '/TNeuNeuZZ_mNeu400_mChi1/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0887325*0.10099*0.10099)
TNeuNeuZZ_mNeu450_mChi1 = kreator.makeMCComponentFromEOS('TNeuNeuZZ_mNeu450_mChi1' , '/TNeuNeuZZ_mNeu450_mChi1/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0537702*0.10099*0.10099)
TNeuNeuZZ = [ TNeuNeuZZ_mNeu400_mChi1, TNeuNeuZZ_mNeu450_mChi1 ]


## TNeuNeuZZ_OS (opposite-sign)
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn1n2hino
## BR: exactly one Z->ll (0.10099)
TNeuNeuZZ_mNeu400_mChi1_OS = kreator.makeMCComponentFromEOS('TNeuNeuZZ_mNeu400_mChi1_OS' , '/TNeuNeuZZ_mNeu400_mChi1_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0887325*0.10099)
TNeuNeuZZ_mNeu450_mChi1_OS = kreator.makeMCComponentFromEOS('TNeuNeuZZ_mNeu450_mChi1_OS' , '/TNeuNeuZZ_mNeu450_mChi1_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0537702*0.10099)
TNeuNeuZZ_OS = [ TNeuNeuZZ_mNeu400_mChi1_OS, TNeuNeuZZ_mNeu450_mChi1_OS ]


## TNeuNeuHZ_OS
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn1n2hino
## BR: Z->ll (0.10099), H->tautau, ZZ, WW (0.0632+0.264+0.022)
TNeuNeuHZ_mNeu300_mChi1_OS = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu300_mChi1_OS' , '/TNeuNeuHZ_mNeu300_mChi1_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.284855*0.10099*0.3492)
TNeuNeuHZ_mNeu350_mChi1_OS = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu350_mChi1_OS' , '/TNeuNeuHZ_mNeu350_mChi1_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.153841*0.10099*0.3492)
TNeuNeuHZ_mNeu400_mChi1_OS = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu400_mChi1_OS' , '/TNeuNeuHZ_mNeu400_mChi1_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0887325*0.10099*0.3492)
TNeuNeuHZ_mNeu450_mChi1_OS = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu450_mChi1_OS' , '/TNeuNeuHZ_mNeu450_mChi1_OS/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0537702*0.10099*0.3492)
TNeuNeuHZ_OS = [ TNeuNeuHZ_mNeu300_mChi1_OS, TNeuNeuHZ_mNeu350_mChi1_OS, TNeuNeuHZ_mNeu400_mChi1_OS, TNeuNeuHZ_mNeu450_mChi1_OS ]


## TNeuNeuHZ_SL
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn1n2hino
## BR: Z->ll (0.10099), H->bbar (0.577)
TNeuNeuHZ_mNeu300_mChi1_SL = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu300_mChi1_SL' , '/TNeuNeuHZ_mNeu300_mChi1_SL/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.284855*0.10099*0.577 )
TNeuNeuHZ_mNeu350_mChi1_SL = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu350_mChi1_SL' , '/TNeuNeuHZ_mNeu350_mChi1_SL/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.153841*0.10099*0.577 )
TNeuNeuHZ_mNeu400_mChi1_SL = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu400_mChi1_SL' , '/TNeuNeuHZ_mNeu400_mChi1_SL/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0887325*0.10099*0.577 )
TNeuNeuHZ_mNeu450_mChi1_SL = kreator.makeMCComponentFromEOS('TNeuNeuHZ_mNeu450_mChi1_SL' , '/TNeuNeuHZ_mNeu450_mChi1_SL/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0537702*0.10099*0.577 )
TNeuNeuHZ_SL = [ TNeuNeuHZ_mNeu300_mChi1_SL, TNeuNeuHZ_mNeu350_mChi1_SL, TNeuNeuHZ_mNeu400_mChi1_SL, TNeuNeuHZ_mNeu450_mChi1_SL ]


## TNeuNeuHH
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn1n2hino
## BR: H->tautau, ZZ, WW (0.0632+0.264+0.022)**2
TNeuNeuHH_mNeu350_mChi1 = kreator.makeMCComponentFromEOS('TNeuNeuHH_mNeu350_mChi1' , '/TNeuNeuHH_mNeu350_mChi1/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.153841*0.3492*0.3492)
TNeuNeuHH_mNeu400_mChi1 = kreator.makeMCComponentFromEOS('TNeuNeuHH_mNeu400_mChi1' , '/TNeuNeuHH_mNeu400_mChi1/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0887325*0.3492*0.3492)
TNeuNeuHH_mNeu450_mChi1 = kreator.makeMCComponentFromEOS('TNeuNeuHH_mNeu450_mChi1' , '/TNeuNeuHH_mNeu450_mChi1/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0537702*0.3492*0.3492)
TNeuNeuHH = [ TNeuNeuHH_mNeu350_mChi1, TNeuNeuHH_mNeu400_mChi1, TNeuNeuHH_mNeu450_mChi1 ]


## TNeuNeuHH_BB
## ------------------------------------------------------
## xsec: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVn1n2hino
## BR: H->bbbar (0.577)**2
TNeuNeuHH_mNeu350_mChi1_BB = kreator.makeMCComponentFromEOS('TNeuNeuHH_mNeu350_mChi1_BB' , '/TNeuNeuHH_mNeu350_mChi1_BB/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.153841*0.577*0.577)
TNeuNeuHH_mNeu400_mChi1_BB = kreator.makeMCComponentFromEOS('TNeuNeuHH_mNeu400_mChi1_BB' , '/TNeuNeuHH_mNeu400_mChi1_BB/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0887325*0.577*0.577)
TNeuNeuHH_mNeu450_mChi1_BB = kreator.makeMCComponentFromEOS('TNeuNeuHH_mNeu450_mChi1_BB' , '/TNeuNeuHH_mNeu450_mChi1_BB/' , '/store/group/phys_susy/cheidegg/EWKSignals_76X_MiniAODv2/%s', ".*root", 0.0537702*0.577*0.577)
TNeuNeuHH_BB = [ TNeuNeuHH_mNeu350_mChi1_BB, TNeuNeuHH_mNeu400_mChi1_BB, TNeuNeuHH_mNeu450_mChi1_BB ]



## mcSamplesPriv
## ------------------------------------------------------
mcSamplesPriv = SqGltttt + T1ttbb + T1ttbbWW + T1tttt + T2tt + T2ttDeg + T5qqqqVV + T5qqqqVVDeg + T5ttttDeg + T6ttWW + T6qqWW + TChiChiSlepSneu + TChiNeuSlepSneu + TChiNeuSlepSneu_SS + TChiNeuSlepSneu_TD + TChiNeuWH + TChiNeuWH_SL + TChiNeuWZ + TChiNeuWZ_OS + TSlepSlep + TNeuNeuZZ + TNeuNeuZZ_OS + TNeuNeuHZ_OS + TNeuNeuHZ_SL + TNeuNeuHH + TNeuNeuHH_BB



from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in mcSamplesPriv:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012


if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(mcSamplesPriv)
