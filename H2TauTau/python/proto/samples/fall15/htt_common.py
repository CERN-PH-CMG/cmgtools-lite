from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import TT_pow_ext, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15, WWTo2L2Nu, ZZp8, WZp8, WJetsToLNu_LO, QCD_Mu5, DYJetsToLL_M50_LO, TBar_tWch, T_tWch, QCDPtEMEnriched, QCDPtbcToE, TT_pow, TToLeptons_tch_amcatnlo, TBarToLeptons_tch_powheg, TToLeptons_tch_powheg
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_Promptv4, SingleElectron_Run2015D_05Oct, SingleElectron_Run2015D_Promptv4, MuonEG_Run2015D_05Oct, MuonEG_Run2015D_Promptv4, Tau_Run2015D_05Oct, Tau_Run2015D_Promptv4
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import VVTo2L2Nu, WWTo1L1Nu2Q, ZZTo2L2Q, ZZTo4L, WZTo3L, WZTo2L2Q, WZTo1L3Nu, WZTo1L1Nu2Q

from CMGTools.H2TauTau.proto.samples.fall15.higgs import HiggsGGH125, HiggsVBF125#, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import mc_higgs_susy_gg, mc_higgs_susy_bb

from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import HiggsSUSYGG160 as ggh160

# Set cross sections to HTT values

VVTo2L2Nu.xSection = 11.95
WWTo1L1Nu2Q.xSection = 49.997
ZZTo2L2Q.xSection = 3.22 
ZZTo4L.xSection = 1.212
WZTo3L.xSection = 5.26
WZTo2L2Q.xSection = 5.595
WZTo1L3Nu.xSection = 3.05
WZTo1L1Nu2Q.xSection = 10.71

DYJetsToLL_M50_LO.xSection = 6025.2
DYJetsToLL_M50.xSection = 6025.2

# Backgrounds
diboson_lo = [ZZp8, WZp8]
diboson_nlo = [VVTo2L2Nu, WWTo1L1Nu2Q, ZZTo2L2Q, ZZTo4L, WZTo3L, WZTo2L2Q, WZTo1L3Nu, WZTo1L1Nu2Q]

essential = [TT_pow_ext, WJetsToLNu_LO, DYJetsToLL_M50_LO, TBar_tWch, T_tWch]

# Build default background list
backgrounds = essential
backgrounds += diboson_nlo
backgrounds += []

backgrounds_mu = backgrounds[:]
backgrounds_mu += [QCD_Mu15]

backgrounds_ele = backgrounds[:]
backgrounds_ele += QCDPtEMEnriched 
backgrounds_ele += QCDPtbcToE

# Data
data_single_muon = [SingleMuon_Run2015D_05Oct, SingleMuon_Run2015D_Promptv4]
data_single_electron = [SingleElectron_Run2015D_05Oct, SingleElectron_Run2015D_Promptv4]
data_muon_electron = [MuonEG_Run2015D_05Oct, MuonEG_Run2015D_Promptv4]
data_tau = [Tau_Run2015D_05Oct, Tau_Run2015D_Promptv4]

# Signals
sm_signals = [HiggsGGH125, HiggsVBF125, HiggsTTH125]
mssm_signals = mc_higgs_susy_bb + mc_higgs_susy_gg

sync_list = [ggh160]

