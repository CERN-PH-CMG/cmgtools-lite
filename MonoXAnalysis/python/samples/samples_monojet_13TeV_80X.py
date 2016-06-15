import PhysicsTools.HeppyCore.framework.config as cfg
import os

#####COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

### common MC samples
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring16MiniAODv1 import *
### DM MC samples
#from CMGTools.RootTools.samples.samples_monojet_13TeV_74X_signals import *

### --- mc ---

# --- 25 ns background samples ---
#DYJetsToNuNu_MJ = [ DYJetsToNuNu_M50 ] + ZJetsToNuNuHT
#VJets_MJ        = [ WJetsToLNu ] + WJetsToLNuHT + DYJetsM50HT + [ DYJetsToLL_M50, DYJetsToLL_M10to50 ]
#Top_MJ          = [ TTJets, TToLeptons_tch_amcatnlo, TToLeptons_tch_amcatnlo_ext, TBar_tWch, T_tWch ]
#DiBosons_MJ     = [ WW, WZ, ZZ ]

# temporary lists
VJets_MJ = VJets
Top_MJ = TTs

#mcSamples_monojet_Asymptotic25ns = DYJetsToNuNu_MJ + VJets_MJ + Top_MJ + DiBosons_MJ + QCDHT + GJetsHT
#mcSamples_monojet_Asymptotic25ns_signals = DM_Scalars + DM_Pseudoscalars + DM_Vectors + DM_Axials

mcSamples_monojet_Asymptotic25ns = VJets_MJ + Top_MJ

### ----------------------------- summary ----------------------------------------     
mcSamples_monojet = mcSamples_monojet_Asymptotic25ns


### --------- private DATA re-recoes for ECAL validation ---------
dcsjson = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/DCSOnly/json_DCSONLY.txt'
DoubleEG_ZElectron_ReReco_files = [ f.strip() for f in open("%s/src/CMGTools/MonoXAnalysis/python/samples/ZElectron_ReReco_PS2016.txt" % os.environ['CMSSW_BASE'], "r") ]
DoubleEG_ZElectron_ReReco = kreator.makePrivateDataComponent('DoubleEG_ZElectron_ReReco','/store/group/dpg_ecal/comm_ecal/localreco/data2016_zskim_multifits/miniaod/run2016B_rereco/',DoubleEG_ZElectron_ReReco_files, dcsjson )

DoubleEG_ZElectron_std_files = [ f.strip() for f in open("%s/src/CMGTools/MonoXAnalysis/python/samples/ZElectron_ReReco_std.txt" % os.environ['CMSSW_BASE'], "r") ]
DoubleEG_ZElectron_std = kreator.makePrivateDataComponent('DoubleEG_ZElectron_std','/store/group/dpg_ecal/comm_ecal/localreco/data2016_zskim_multifits/miniaod/run2016B_std/',DoubleEG_ZElectron_std_files, dcsjson )

PrivateSamplesData = [DoubleEG_ZElectron_std, DoubleEG_ZElectron_ReReco]

from CMGTools.TTHAnalysis.setup.Efficiencies import *
dataDir = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data"

#Define splitting
for comp in mcSamples:
    comp.isMC = True
    comp.isData = False
    comp.splitFactor = 250 #  if comp.name in [ "WJets", "DY3JetsM50", "DY4JetsM50","W1Jets","W2Jets","W3Jets","W4Jets","TTJetsHad" ] else 100
    comp.puFileMC=dataDir+"/puProfile_Summer12_53X.root"
    comp.puFileData=dataDir+"/puProfile_Data12.root"
    comp.efficiency = eff2012
# for comp in dataSamples:
#     comp.splitFactor = 1000
#     comp.isMC = False
#     comp.isData = True


if __name__ == "__main__":
   import sys
   if "test" in sys.argv:
       from CMGTools.RootTools.samples.ComponentCreator import testSamples
       testSamples(mcSamples)
