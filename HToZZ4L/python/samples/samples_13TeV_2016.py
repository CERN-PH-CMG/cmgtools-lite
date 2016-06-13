import os

################## 
## Triggers for HLT_MC_SPRING15 and Run II
## Based on HLT_MC_SPRING15 and /frozen/2015/25ns14e33/v2.1/HLT/V1 and /frozen/2015/50ns_5e33/v2.1/HLT/V5
## Names with _50ns are unprescaled at 50ns but prescaled at 25ns
## Names with _run1 are for comparing Spring15 MC to 8 TeV data: they're the closest thing I could find to run1 triggers, they're prescaled or even excluded in data but should appear in MC.

triggers_mumu = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*" ]
triggers_mumu_all = [ "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*",
                      "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*" ]

triggers_ee = [ "HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*" ]

triggers_mue = [ "HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v*",
                 "HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*" ]

triggers_3e = [ "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v*" ]
triggers_3mu = [ "HLT_TripleMu_12_10_5_v*" ]
triggers_2mu1e = [ "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v*" ]
triggers_2e1mu = [ "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v*" ]

triggers_trilep = triggers_3e + triggers_3mu + triggers_2mu1e + triggers_2e1mu

triggers_1e      = [ 'HLT_Ele23_WPLoose_Gsf_v*'  ]
triggers_1e_old  = [ "HLT_Ele32_eta2p1_WP75_Gsf_v*", "HLT_Ele32_eta2p1_WPLoose_Gsf_v*" , 'HLT_Ele27_WP85_Gsf_v*', 'HLT_Ele27_WPLoose_Gsf_v*']

triggers_1mu     = [ 'HLT_IsoMu22_eta2p1_v*', 'HLT_IsoTkMu22_eta2p1_v*', 'HLT_IsoMu22_v*', 'HLT_IsoTkMu22_v*', 'HLT_IsoMu20_v*', 'HLT_IsoTkMu20_v*' ]

triggers_signal_real = triggers_mumu + triggers_ee + triggers_mue + triggers_trilep + triggers_1e
triggers_any = list(set(triggers_signal_real+triggers_1e_old))

triggers_jpsi2mu = [
    "HLT_Dimuon0er16_Jpsi_NoOS_NoVertexing_v*",
    "HLT_Dimuon0er16_Jpsi_NoVertexing_v*",
    "HLT_Dimuon10_Jpsi_Barrel_v*",
    "HLT_Dimuon16_Jpsi_v*",
    "HLT_Dimuon20_Jpsi_v*",
    "HLT_Dimuon6_Jpsi_NoVertexing_v*",
    "HLT_DoubleMu4_3_Jpsi_Displaced_v*",
    "HLT_DoubleMu4_JpsiTrk_Displaced_v*",
    "HLT_Mu7p5_L2Mu2_Jpsi_v*",
    "HLT_Mu7p5_Track2_Jpsi_v*",
    "HLT_Mu7p5_Track3p5_Jpsi_v*",
    "HLT_Mu7p5_Track7_Jpsi_v*",
]
triggers_upsilon2mu = [
    "HLT_Dimuon0_Upsilon_Muon_v*",
    "HLT_Dimuon13_Upsilon_v*",
    "HLT_Dimuon8_Upsilon_Barrel_v*",
    "HLT_Mu7p5_L2Mu2_Upsilon_v*",
    "HLT_Mu7p5_Track2_Upsilon_v*",
    "HLT_Mu7p5_Track3p5_Upsilon_v*",
    "HLT_Mu7p5_Track7_Upsilon_v*",
]

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# GGH cross section from LHC Higgs XS WG: https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV?rev=15
#GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "", "CMS", ".*root", 0.01212) #43.92*2.76E-04)
#QQHZZ4L = kreator.makeMCComponent("QQHZZ4L", "", "CMS", ".*root", 0.001034)# 3.748*2.76E-04)
## split in assing W+/(W+ + W-) = 0.6385 as at 8 TeV, to be updated
#WpHZZ4L = kreator.makeMCComponent("WpHZZ4L", "", "CMS", ".*root", 0.0002339) # 1.38*0.6385*2.76E-04)
#WmHZZ4L = kreator.makeMCComponent("WmHZZ4L", "", "CMS", ".*root", 0.0001471) # 1.38*(1-0.6385)*2.76E-04)
#ZHZZ4LF = kreator.makeMCComponent("ZHZZ4LF", "", "CMS", ".*root", 0.000652) #0.8696*(3.70E-03+2.34E-02+2.76E-04)*0.15038)
#TTHZZ4LF = kreator.makeMCComponent("TTHZZ4LF", "", "CMS", ".*root", 0.000337 ) 


H4L = [ ]

# cross section from McM (powheg) 
ZZTo4L = kreator.makeMCComponent("ZZTo4L","/ZZTo4L_13TeV_powheg_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 1.256)
#ZZTo4L_aMC = kreator.makeMCComponent("ZZTo4L_aMC","/ZZTo4L_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM", "CMS", ".*root", 1.256)

#GGZZTo2e2mu = kreator.makeMCComponent("GGZZTo2e2mu", "", "CMS", ".*root", 0.00319364)
#GGZZTo2e2tau = kreator.makeMCComponent("GGZZTo2e2tau", "", "CMS", ".*root", 0.00319364)
GGZZTo2mu2tau = kreator.makeMCComponent("GGZZTo2mu2tau", "/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 0.00319364)
GGZZTo4e = kreator.makeMCComponent("GGZZTo4e", "/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 0.00158582)
GGZZTo4mu = kreator.makeMCComponent("GGZZTo4mu", "/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 0.00158582)
GGZZTo4tau = kreator.makeMCComponent("GGZZTo4tau", "/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM", "CMS", ".*root", 0.00158582)

GGZZTo4L = [ GGZZTo2mu2tau, GGZZTo4e, GGZZTo4mu, GGZZTo4tau ] # GGZZTo2e2mu, GGZZTo2e2tau, 

### Z+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)
DYJetsToLL_LO_M50 = kreator.makeMCComponent("DYJetsToLL_LO_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 2008.*3)


## Cross section from McM (aMC@NLO)
DYJetsToLL_M10to50 = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 18610)
DYJetsToLL_LO_M10to50 = kreator.makeMCComponent("DYJetsToLL_LO_M10to50", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 18610)
DYJets = [ DYJetsToLL_M50, DYJetsToLL_M10to50, DYJetsToLL_LO_M50, DYJetsToLL_LO_M10to50  ] 

# cross section from McM (powheg)
WZTo3LNu = kreator.makeMCComponent("WZTo3LNu", "/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 4.42965)

# cross section from StandardModelCrossSectionsat13TeV NNLO times BR=(3*0.108)**2
#WWTo2L2Nu = kreator.makeMCComponent("WWTo2L2Nu", "", "CMS", ".*root", 118.7*((3*0.108)**2) )

# TTbar cross section: MCFM with dynamic scale, StandardModelCrossSectionsat13TeV
TTLep = kreator.makeMCComponent("TTLep", "/TTTo2L2Nu_13TeV-powheg/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3_ext1-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2))

#TBar_tWch = kreator.makeMCComponent("TBar_tWch", "", "CMS", ".*root",35.6)   
#T_tWch = kreator.makeMCComponent("T_tWch", "", "CMS", ".*root",35.6)
#SingleTop = [ TBar_tWch, T_tWch ]


### TriBosons
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Triboson
#WWZ = kreator.makeMCComponent("WWZ", "", "CMS", ".*root",  0.1651 )
#WZZ = kreator.makeMCComponent("WZZ", "", "CMS", ".*root",  0.05565 )
#ZZZ = kreator.makeMCComponent("ZZZ", "", "CMS", ".*root",  0.01398 )

#TriBosons = [ WWZ, WZZ, ZZZ ]

### W+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
#WJetsToLNu = kreator.makeMCComponent("WJetsToLNu","", "CMS", ".*root", 20508.9*3)
#WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu","", "CMS", ".*root", 20508.9*3)

mcSamples_4l =  H4L + [ ZZTo4L ] + DYJets + [ WZTo3LNu, TTLep ] #+ SingleTop + [ WJetsToLNu ]
#mcSamples_25ns =  H4L + [ ZZTo4L, ZZTo4L_aMC ] + GGZZTo4L + DYJets + [ WZTo3LNu, WWTo2L2Nu, TTLep ] + SingleTop + [ WJetsToLNu, WJetsToLNu_LO ] + TriBosons

### ===== Onia ======
JpsiToMuMuPt8 = kreator.makeMCComponent("JpsiToMuMuPt8","/JpsiToMuMu_JpsiPt8_TuneCUEP8M1_13TeV-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM", "CMS", ".*root", 1.0)
#UpsToMuMuPt6 = kreator.makeMCComponent("UpsToMuMuPt6", "", "CMS", ".*root", 1.0)

mcSamples_onia = [ JpsiToMuMuPt8, ] # UpsToMuMuPt6 ]

mcSamples = mcSamples_4l + mcSamples_onia

#-----------DATA---------------
dataDir = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/data"
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-274421_13TeV_PromptReco_Collisions16_JSON.txt'
from CMGTools.TTHAnalysis.setup.Efficiencies import eff2012

jsonFilter=False
DoubleMuon_Run2016B_PromptV2 = kreator.makeDataComponent("DoubleMuon_Run2016B_PromptV2", "/DoubleMuon/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)
DoubleEG_Run2016B_PromptV2 = kreator.makeDataComponent("DoubleEG_Run2016B_PromptV2", "/DoubleEG/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)
MuonEG_Run2016B_PromptV2 = kreator.makeDataComponent("MuonEG_Run2016B_PromptV2", "/MuonEG/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)
SingleMuon_Run2016B_PromptV2 = kreator.makeDataComponent("SingleMuon_Run2016B_PromptV2", "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)
SingleElectron_Run2016B_PromptV2 = kreator.makeDataComponent("SingleElectron_Run2016B_PromptV2", "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)
Charmonium_Run2016B_PromptV2 = kreator.makeDataComponent("Charmonium_Run2016B_PromptV2", "/Charmonium/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)
MuOnia_Run2016B_PromptV2 = kreator.makeDataComponent("MuOnia_Run2016B_PromptV2", "/MuOnia/Run2016B-PromptReco-v2/MINIAOD", "CMS", ".*root", jsonFilter=jsonFilter, json=json)

dataSamples = [ 
    DoubleMuon_Run2016B_PromptV2, DoubleEG_Run2016B_PromptV2, MuonEG_Run2016B_PromptV2, SingleMuon_Run2016B_PromptV2, SingleElectron_Run2016B_PromptV2,
]
dataSamples_onia = [ 
    Charmonium_Run2016B_PromptV2, MuOnia_Run2016B_PromptV2, 
]

dataSamples_all = dataSamples + dataSamples_onia

#Define splitting
for comp in mcSamples:
    comp.splitFactor = 250 
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012
    comp.triggers = []
    comp.vetoTriggers = []

for comp in dataSamples_all:
    comp.splitFactor = max(len(comp.files)/5,1)
    if "Single" in comp.name: comp.splitFactor = max(1,comp.splitFactor/2)
    comp.fineSplitFactor = 1

DatasetsAndTriggers = []
DatasetsAndTriggers.append( ("DoubleEG",   triggers_ee + triggers_3e) )
DatasetsAndTriggers.append( ("DoubleMuon", triggers_mumu + triggers_3mu) )
DatasetsAndTriggers.append( ("MuonEG",     triggers_mue + triggers_2mu1e + triggers_2e1mu) )
DatasetsAndTriggers.append( ("SingleElectron", triggers_1e) )
DatasetsAndTriggers.append( ("SingleMuon", triggers_1mu) )
vetos = []
for pd,triggers in DatasetsAndTriggers:
    for comp in dataSamples_all:
        if pd in comp.dataset:
            comp.triggers = triggers[:]
            comp.vetoTriggers = vetos[:]
    vetos += triggers
    
if __name__ == '__main__':
    import sys
    if "refresh" in sys.argv:
        from CMGTools.Production.cacheChecker import CacheChecker
        checker = CacheChecker()
        for d in dataSamples_all:
                checker.checkComp(d, verbose=True)
