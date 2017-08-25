from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import WJetsToLNu,  WWTo2L2Nu, QCD_Mu5, QCDPtEMEnriched, QCDPtbcToE, TBar_tch_powheg, DYNJets, WNJets, T_tch_powheg, DYJetsToLL_M10to50_LO, DYJetsToLL_M50_LO_ext2, VVTo2L2Nu_ext, WJetsToLNu_LO_ext, WZJToLLLNu #DYJetsToLL_M50_LO WJetsToLNu_LO

from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import DYJetsToLL_M50_LO_ext as DYJetsToLL_M50_LO
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import TBar_tWch_ext as TBar_tWch
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import T_tWch_ext as T_tWch
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import WJetsToLNu_LO
# WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15,  DYJetsToTauTau_M150_LO, 
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import TT_pow
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016B_23Sep2016, SingleElectron_Run2016B_23Sep2016, MuonEG_Run2016B_23Sep2016, Tau_Run2016B_23Sep2016
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016C_23Sep2016, SingleElectron_Run2016C_23Sep2016, MuonEG_Run2016C_23Sep2016, Tau_Run2016C_23Sep2016
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016D_23Sep2016, SingleElectron_Run2016D_23Sep2016, MuonEG_Run2016D_23Sep2016, Tau_Run2016D_23Sep2016
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016E_23Sep2016, SingleElectron_Run2016E_23Sep2016, MuonEG_Run2016E_23Sep2016, Tau_Run2016E_23Sep2016
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016F_23Sep2016, SingleElectron_Run2016F_23Sep2016, MuonEG_Run2016F_23Sep2016, Tau_Run2016F_23Sep2016
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016G_23Sep2016, SingleElectron_Run2016G_23Sep2016, MuonEG_Run2016G_23Sep2016, Tau_Run2016G_23Sep2016
from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import ZZTo4L, WZTo1L3Nu, WWTo1L1Nu2Q, WZTo1L1Nu2Q, ZZTo2L2Q, WZTo2L2Q, VVTo2L2Nu, WZTo3LNu_amcatnlo
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import Tau_Run2016B_03Feb2017_v2, Tau_Run2016C_03Feb2017, Tau_Run2016D_03Feb2017, Tau_Run2016E_03Feb2017, Tau_Run2016F_03Feb2017, Tau_Run2016G_03Feb2017, Tau_Run2016H_03Feb2017_v2, Tau_Run2016H_03Feb2017_v3

# from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import DYJetsToLL_M10to50_ext1
# DY1JetsToLL_M50_LO, DY2JetsToLL_M50_LO, DY3JetsToLL_M50_LO, DY4JetsToLL_M50_LO,

from CMGTools.H2TauTau.proto.samples.summer16.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.summer16.higgs_susy import mc_higgs_susy_gg, mc_higgs_susy_bb

from CMGTools.H2TauTau.proto.samples.summer16.higgs_susy import HiggsSUSYBB1000 as bbh1000

# Full 2016
json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
lumi = 35900.

# Set cross sections to HTT values

VVTo2L2Nu.xSection = 11.95
WWTo1L1Nu2Q.xSection = 49.997
ZZTo2L2Q.xSection = 3.22
ZZTo4L.xSection = 1.212
WZTo3LNu_amcatnlo.xSection = 5.26
WZTo2L2Q.xSection = 5.595
WZTo1L3Nu.xSection = 3.05
WZTo1L1Nu2Q.xSection = 10.71

w_xsec = 61526.7
dy_xsec = 5765.4

DYJetsToLL_M50_LO.xSection = dy_xsec
DYJetsToLL_M50_LO_ext2.xSection = dy_xsec
# DYJetsToLL_M50.xSection = dy_xsec


# From https://twiki.cern.ch/twiki/pub/CMS/HiggsToTauTauWorking2015/DYNjetWeights.xls r3
# dy_weight_dict = {
#     (0, 0): 0.669144882/dy_xsec,
#     (0, 150): 0.001329134/dy_xsec,
#     (1, 0): 0.018336763/dy_xsec,
#     (1, 150): 0.001241603/dy_xsec,
#     (2, 0): 0.019627356/dy_xsec,
#     (2, 150): 0.001247156/dy_xsec,
#     (3, 0): 0.021024291/dy_xsec,
#     (3, 150): 0.001252443/dy_xsec,
#     (4, 0): 0.015530181/dy_xsec,
#     (4, 150): 0.001226594/dy_xsec,
# }

n_ev_dy_incl = 49144274.0 + 96658943.0
n_ev_dy_1jet = 62627174.0
n_ev_dy_2jet = 19970551.0
n_ev_dy_3jet = 5856110.0
n_ev_dy_4jet = 4197868.0


k_factor = dy_xsec/4954.0
dy_xsec_incl = 4954.0 * k_factor
dy_xsec_1jet = 1012.5 * k_factor
dy_xsec_2jet = 332.8 * k_factor
dy_xsec_3jet = 101.8 * k_factor
dy_xsec_4jet = 54.8 * k_factor


dy_weight_dict = {
    0:dy_xsec_incl/n_ev_dy_incl,
    1:dy_xsec_1jet/(n_ev_dy_incl*dy_xsec_1jet/dy_xsec_incl + n_ev_dy_1jet),
    2:dy_xsec_2jet/(n_ev_dy_incl*dy_xsec_2jet/dy_xsec_incl  + n_ev_dy_2jet),
    3:dy_xsec_3jet/(n_ev_dy_incl*dy_xsec_3jet/dy_xsec_incl  + n_ev_dy_3jet),
    4:dy_xsec_4jet/(n_ev_dy_incl*dy_xsec_4jet/dy_xsec_incl  + n_ev_dy_4jet),
}

def getDYWeight(n_jets): # , m_gen): # mass > 150 GeV sample buggy...
    # if m_gen > 150.:
    #     return dy_weight_dict[(n_jets, 150)]
    return dy_weight_dict[n_jets]

for sample in [DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_ext2] + DYNJets: # + [DYJetsToTauTau_M150_LO]:
    # sample.fractions = [0.7, 0.204374, 0.0671836, 0.0205415, 0.0110539]

    sample.weight_func = getDYWeight
    sample.xSection = dy_xsec

# From https://twiki.cern.ch/twiki/pub/CMS/HiggsToTauTauWorking2015/DYNjetWeights.xls r3
w_weight_dict = {
    0:1.304600668/w_xsec,
    1:0.216233816/w_xsec,
    2:0.115900663/w_xsec,
    3:0.058200264/w_xsec,
    4:0.06275589/w_xsec
}

def getWWeight(n_jets):
    return w_weight_dict[n_jets]

for sample in [WJetsToLNu_LO] + WNJets: # 

    sample.weight_func = getWWeight
    # sample.xSection = w_xsec

WJetsHT = [] # WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf

# Backgrounds
diboson_nlo = [ZZTo4L, WZTo1L3Nu, WWTo1L1Nu2Q, ZZTo2L2Q,  WZTo2L2Q, WZTo1L1Nu2Q, VVTo2L2Nu, WZTo3LNu_amcatnlo]

essential = [TT_pow, DYJetsToLL_M50_LO, DYJetsToLL_M50_LO_ext2, DYJetsToLL_M10to50_LO, TBar_tWch, T_tWch, TBar_tch_powheg, T_tch_powheg, WJetsToLNu_LO]  # WJetsToLNu, 

# Build default background list
backgrounds = essential
backgrounds += DYNJets
# backgrounds += [DYJetsToTauTau_M150_LO, DYJetsToLL_M10to50_ext1]
backgrounds += WNJets
backgrounds += diboson_nlo
backgrounds += [VVTo2L2Nu_ext, WJetsToLNu_LO_ext, WZJToLLLNu]

backgrounds_mu = backgrounds[:]
# backgrounds_mu += [QCD_Mu15]

backgrounds_ele = backgrounds[:]
backgrounds_ele += QCDPtEMEnriched
backgrounds_ele += QCDPtbcToE

# Data
data_single_muon = [SingleMuon_Run2016B_23Sep2016, SingleMuon_Run2016C_23Sep2016, SingleMuon_Run2016D_23Sep2016, SingleMuon_Run2016E_23Sep2016, SingleMuon_Run2016F_23Sep2016, SingleMuon_Run2016G_23Sep2016]
data_single_electron = [SingleElectron_Run2016B_23Sep2016, SingleElectron_Run2016C_23Sep2016, SingleElectron_Run2016D_23Sep2016, SingleElectron_Run2016E_23Sep2016, SingleElectron_Run2016F_23Sep2016, SingleElectron_Run2016G_23Sep2016]
data_muon_electron = [MuonEG_Run2016B_23Sep2016, MuonEG_Run2016C_23Sep2016, MuonEG_Run2016D_23Sep2016, MuonEG_Run2016E_23Sep2016, MuonEG_Run2016F_23Sep2016, MuonEG_Run2016G_23Sep2016]
data_tau = [Tau_Run2016B_03Feb2017_v2, Tau_Run2016C_03Feb2017, Tau_Run2016D_03Feb2017, Tau_Run2016E_03Feb2017, Tau_Run2016F_03Feb2017, Tau_Run2016G_03Feb2017, Tau_Run2016H_03Feb2017_v2, Tau_Run2016H_03Feb2017_v3]

for sample in data_single_muon + data_single_electron + data_muon_electron + data_tau:
    sample.json = json
    sample.lumi = lumi

# Signals
sm_signals = [HiggsGGH125, HiggsVBF125, HiggsTTH125]
mssm_signals = mc_higgs_susy_bb + mc_higgs_susy_gg

sync_list = [bbh1000, HiggsVBF125]
