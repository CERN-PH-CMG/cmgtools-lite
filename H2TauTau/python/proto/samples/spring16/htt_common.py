from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import DYJetsToLL_M50, WJetsToLNu,  WWTo2L2Nu, ZZ, WZ,  QCD_Mu5, DYJetsToLL_M50_LO, TBar_tWch, T_tWch, QCDPtEMEnriched, QCDPtbcToE, TBarToLeptons_tch_powheg, DYNJets, WNJets, TToLeptons_tch_powheg, WJetsToLNu_LO, DYJetsToLL_M10to50_LO
# WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf, QCD_Mu15,  DYJetsToTauTau_M150_LO, 
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import TT_pow_ext3 as TT_pow_ext
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016B_PromptReco_v2, SingleElectron_Run2016B_PromptReco_v2, MuonEG_Run2016B_PromptReco_v2, Tau_Run2016B_PromptReco_v2
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016C_PromptReco_v2, SingleElectron_Run2016C_PromptReco_v2, MuonEG_Run2016C_PromptReco_v2, Tau_Run2016C_PromptReco_v2
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016D_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2, MuonEG_Run2016D_PromptReco_v2, Tau_Run2016D_PromptReco_v2
from CMGTools.RootTools.samples.samples_13TeV_DATA2016 import SingleMuon_Run2016G_PromptReco_v1, SingleElectron_Run2016G_PromptReco_v1, MuonEG_Run2016G_PromptReco_v1, Tau_Run2016G_PromptReco_v1
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import ZZTo4L, WZTo1L3Nu, WWTo1L1Nu2Q, WZTo1L1Nu2Q, ZZTo2L2Q, WZTo2L2Q, VVTo2L2Nu, WZTo3LNu_amcatnlo

# from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv2 import DYJetsToLL_M10to50_ext1
# DY1JetsToLL_M50_LO, DY2JetsToLL_M50_LO, DY3JetsToLL_M50_LO, DY4JetsToLL_M50_LO,

from CMGTools.H2TauTau.proto.samples.spring16.higgs import HiggsGGH125, HiggsVBF125, HiggsTTH125
from CMGTools.H2TauTau.proto.samples.spring16.higgs_susy import mc_higgs_susy_gg, mc_higgs_susy_bb

from CMGTools.H2TauTau.proto.samples.spring16.higgs_susy import HiggsSUSYGG160 as ggh160

# 21 July

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt'
lumi = 12918.1407

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-279116_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'

# lumi_2016G = 1659.026988066 # 2016 G
lumi_2016G = 1080.463515944 # 2016 G HLT_IsoMu22_v3

json_tt = json
lumi_tt = lumi

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
dy_xsec = 6025.2

DYJetsToLL_M50_LO.xSection = dy_xsec
DYJetsToLL_M50.xSection = dy_xsec

DYJetsToLL_M50_LO.nevents = [1000.] # Temporary entry
WJetsToLNu_LO.nevents = [1000.] # Temporary entry

# From https://twiki.cern.ch/twiki/pub/CMS/HiggsToTauTauWorking2015/DYNjetWeights.xls r3
dy_weight_dict = {
    (0, 0): 0.669144882/dy_xsec,
    (0, 150): 0.001329134/dy_xsec,
    (1, 0): 0.018336763/dy_xsec,
    (1, 150): 0.001241603/dy_xsec,
    (2, 0): 0.019627356/dy_xsec,
    (2, 150): 0.001247156/dy_xsec,
    (3, 0): 0.021024291/dy_xsec,
    (3, 150): 0.001252443/dy_xsec,
    (4, 0): 0.015530181/dy_xsec,
    (4, 150): 0.001226594/dy_xsec,
}

def getDYWeight(n_jets, m_gen):
    if m_gen > 150.:
        return dy_weight_dict[(n_jets, 150)]
    return dy_weight_dict[(n_jets, 0)]

for sample in [DYJetsToLL_M50_LO] + DYNJets: # + [DYJetsToTauTau_M150_LO]:
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

def getWWeight(n_jets, m_gen_dummy):
    return w_weight_dict[n_jets]

for sample in [WJetsToLNu_LO] + WNJets: # 

    sample.weight_func = getWWeight
    # sample.xSection = w_xsec

WJetsHT = [] # WJetsToLNu_HT100to200, WJetsToLNu_HT200to400, WJetsToLNu_HT400to600, WJetsToLNu_HT600toInf

# Backgrounds
diboson_lo = [ZZ, WZ]
diboson_nlo = [ZZTo4L, WZTo1L3Nu, WWTo1L1Nu2Q, ZZTo2L2Q,  WZTo2L2Q, WZTo1L1Nu2Q, VVTo2L2Nu, WZTo3LNu_amcatnlo]

essential = [TT_pow_ext, DYJetsToLL_M50_LO, DYJetsToLL_M10to50_LO, TBar_tWch, T_tWch, TBarToLeptons_tch_powheg, TToLeptons_tch_powheg, WJetsToLNu_LO]  # WJetsToLNu, 

# Build default background list
backgrounds = essential
backgrounds += DYNJets
# backgrounds += [DYJetsToTauTau_M150_LO, DYJetsToLL_M10to50_ext1]
backgrounds += WNJets
backgrounds += diboson_nlo
backgrounds += []

backgrounds_mu = backgrounds[:]
# backgrounds_mu += [QCD_Mu15]

backgrounds_ele = backgrounds[:]
backgrounds_ele += QCDPtEMEnriched
backgrounds_ele += QCDPtbcToE

# Data
data_single_muon = [SingleMuon_Run2016B_PromptReco_v2, SingleMuon_Run2016C_PromptReco_v2, SingleMuon_Run2016D_PromptReco_v2, SingleMuon_Run2016G_PromptReco_v1]
data_single_electron = [SingleElectron_Run2016B_PromptReco_v2, SingleElectron_Run2016C_PromptReco_v2, SingleElectron_Run2016D_PromptReco_v2]
data_muon_electron = [MuonEG_Run2016B_PromptReco_v2, MuonEG_Run2016C_PromptReco_v2, MuonEG_Run2016D_PromptReco_v2]
data_tau = [Tau_Run2016B_PromptReco_v2, Tau_Run2016C_PromptReco_v2, Tau_Run2016D_PromptReco_v2] #, ]

for sample in data_single_muon + data_single_electron + data_muon_electron + data_tau:
    sample.json = json
    sample.lumi = lumi if sample != SingleMuon_Run2016G_PromptReco_v1 else lumi_2016G

# Signals
sm_signals = [HiggsGGH125, HiggsVBF125, HiggsTTH125]
mssm_signals = mc_higgs_susy_bb + mc_higgs_susy_gg

sync_list = [ggh160]
