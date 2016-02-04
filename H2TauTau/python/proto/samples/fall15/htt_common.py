from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import TT_pow_ext, DYJetsToLL_M50, WJetsToLNu, WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, WWTo2L2Nu, ZZ, WZ,  QCD_Mu5, DYJetsToLL_M50_LO, TBar_tWch, T_tWch, QCDPtEMEnriched, QCDPtbcToE, TToLeptons_tch_amcatnlo, TBarToLeptons_tch_powheg, TToLeptons_tch_powheg, DYNJets #QCD_Mu15, WJetsToLNu_LO
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import SingleMuon_Run2015D_16Dec, SingleElectron_Run2015D_16Dec, MuonEG_Run2015D_16Dec, Tau_Run2015D_16Dec
from CMGTools.RootTools.samples.samples_13TeV_RunIIFall15MiniAODv2 import ZZTo4L, WZTo1L3Nu, WZTo3L, WWTo1L1Nu2Q#, WZTo1L1Nu2Q, VVTo2L2Nu, , ZZTo2L2Q, , WZTo2L2Q

from CMGTools.H2TauTau.proto.samples.fall15.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import mc_higgs_susy_gg, mc_higgs_susy_bb

from CMGTools.H2TauTau.proto.samples.fall15.higgs_susy import HiggsSUSYGG160 as ggh160

# Set cross sections to HTT values

# VVTo2L2Nu.xSection = 11.95
# WWTo1L1Nu2Q.xSection = 49.997
# ZZTo2L2Q.xSection = 3.22 
ZZTo4L.xSection = 1.212
# WZTo3L.xSection = 5.26
# WZTo2L2Q.xSection = 5.595
WZTo1L3Nu.xSection = 3.05
# WZTo1L1Nu2Q.xSection = 10.71

DYJetsToLL_M50_LO.xSection = 6025.2
DYJetsToLL_M50.xSection = 6025.2

# Backgrounds
diboson_lo = [ZZ, WZ]
diboson_nlo = [ZZTo4L, WZTo1L3Nu, WZTo3L, WWTo1L1Nu2Q] #, VVTo2L2Nu, ZZTo2L2Q,  WZTo2L2Q, WZTo1L1Nu2Q]

essential = [TT_pow_ext, WJetsToLNu, DYJetsToLL_M50_LO, TBar_tWch, T_tWch] #WJetsToLNu_LO

# Build default background list
backgrounds = essential
backgrounds += DYNJets
backgrounds += diboson_nlo
backgrounds += []

backgrounds_mu = backgrounds[:]
# backgrounds_mu += [QCD_Mu15]

backgrounds_ele = backgrounds[:]
backgrounds_ele += QCDPtEMEnriched 
backgrounds_ele += QCDPtbcToE

# Data
data_single_muon = [SingleMuon_Run2015D_16Dec]
data_single_electron = [SingleElectron_Run2015D_16Dec]
data_muon_electron = [MuonEG_Run2015D_16Dec]
data_tau = [Tau_Run2015D_16Dec]

# Signals
sm_signals = [HiggsGGH125, HiggsVBF125, HiggsTTH125]
mssm_signals = mc_higgs_susy_bb + mc_higgs_susy_gg

sync_list = [ggh160]

