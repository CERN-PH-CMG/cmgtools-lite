#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess

from optparse import OptionParser
parser = OptionParser(usage="%prog testname ")
parser.add_option("--mu", dest="useMuon", default=False, action='store_true', help="Do fake rate for muons");
parser.add_option("--qcdmc", dest="addQCDMC", default=False, action='store_true', help="Add QCD MC in plots (but do not subtract from data)");
parser.add_option("--full2016data", dest="useFullData2016", default=False, action='store_true', help="Use all 2016 data (B to H, 35.5/fb). By default, only B to F are used (19.3/fb. Luminosity is automatically set depending on this choice");
parser.add_option("--etaRange", dest="etaRange", default="0.0,1.479,2.5", type='string', help="Pass 2 or more numbers separated by comma. They are the boundaries of the eta ranges to use.");
parser.add_option("--charge", dest="charge", default="", type='string', help="Select charge: p for positive, n for negative");
parser.add_option("--test", dest="test", default="", type='string', help="pass the name of a folder (mandatory) to store test FR plots. It is created in plots/fake-rate/test/");
parser.add_option("--fqcd-ranges", dest="fqcd_ranges", default="0,40,50,120", type='string', help="Pass a list of 4 comma separated numbers that represents the ranges for the two mT regions to compute the fake rate");
parser.add_option("--mt", dest="fitvar", default="trkmtfix", type='string', help="Select mT definition: pfmt, trkmt, pfmtfix, trkmtfix");
parser.add_option("--pt", dest="ptvar", default="pt_granular", type='string', help="Select pT definition: pt_granular (default) or pt_coarse");
parser.add_option("--useSkim", dest="useSkim", default=False, action='store_true', help="Use skimmed sample for fake rates");
parser.add_option("--skipStack", dest="skipStack", default=False, action='store_true', help="Skip stack plots");
parser.add_option("--addOpts", dest="addOpts", default="", type='string', help="Options to pass some other options from outside to build the command");
(options, args) = parser.parse_args()

useMuon = options.useMuon
addQCDMC = options.addQCDMC  # trying to add QCD MC to graphs to be compared
charge = str(options.charge)
testDir = str(options.test)
fqcd_ranges = str(options.fqcd_ranges)
fitvar = str(options.fitvar)
ptvar = str(options.ptvar)
useFullData2016 = options.useFullData2016
useSkim = options.useSkim
skipStack = options.skipStack
addOpts = options.addOpts
etaRange = options.etaRange.split(",");

if fqcd_ranges.count(",") != 3:
    print "warning: options --fqcd-ranges requires 4 numbers separated by commas (3 commas expected), but %s was passed" % fqcd_ranges
    quit()

if len(etaRange)<2:
    print "warning: must specify at least 1 eta bin (2 numbers for the boundary). Use option --etaRange '<arg1,arg2,...argN>'"
    quit()

if fitvar not in ["pfmt", "trkmt", "pfmtfix", "trkmtfix"]:
    print "warning: unknown mt definition %s, use pfmt, trkmt, pfmtfix, trkmtfix" % fitvar
    quit()

if not useMuon and ptvar not in ["pt_coarse", "pt_granular"]:
    print "warning: unknown pt definition %s, use pt_coarse, pt_granular" % ptvar
    quit()

if useMuon:
    addQCDMC = True

plotterPath = str(os.environ.get('CMSSW_BASE'))
plotterPath = plotterPath + "/src/CMGTools/WMass/python/plotter/"

chargeSelection = ""
if charge != "":
    if charge == "p":
        chargeSelection = "-A onelep positive 'LepGood1_pdgId < 0'"
    elif charge == "n":
        chargeSelection = "-A onelep negative 'LepGood1_pdgId > 0'"
    else:
        print "%s is not a valid input for charge setting: use p or n" % charge
        quit()

T="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3/" 
if useSkim:
    #T="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_FRELSKIM_V5/"
    T="/eos/cms/store/cmst3/group/wmass/mciprian/TREES_1LEP_80X_V3_FRELSKIM_V6/"
objName='tree' # name of TTree object in Root file, passed to option --obj in tree2yield.py
# if 'pccmsrm29' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/u2/emanuele')
# elif 'lxplus' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/afs/cern.ch/work/e/emanuele/TREES/')
# elif 'cmsrm-an' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/t3/users/dimarcoe/')
print "used trees from: ",T

luminosity = 19.3
#datasetOption = " --pg 'data := data_B,data_C,data_D,data_E,data_F' --xp 'data_G,data_H' "
ptcorr = "ptElFull(LepGood1_calPt,LepGood1_eta)"
ptForScaleFactors =  "LepGood_pt"  # or ptcorr
MCweightOption = ' -W "puw2016_nTrueInt_BF(nTrueInt)*trgSF_We(LepGood1_pdgId,%s,LepGood1_eta,2)" ' % str(ptForScaleFactors)
if useFullData2016:
    #datasetOption = " --pg 'data := data_B,data_C,data_D,data_E,data_F,data_G,data_H' "
    luminosity = 35.9
    MCweightOption = ' -W "puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,%s,LepGood1_eta,2)" ' % str(ptForScaleFactors)

J=4

BASECONFIG = plotterPath + "w-helicity-13TeV/wmass_e"
MCA = BASECONFIG+'/mca-80X_V5_FRskim.txt'
CUTFILE =BASECONFIG+'/qcd1l_SRtrees.txt'
XVAR=ptvar
FITVAR=fitvar
NUM = "fakeRateNumerator_el"

if useMuon:
    BASECONFIG=plotterPath + "w-helicity-13TeV/wmass_mu"
    MCA=BASECONFIG+'/mca-qcd1l_mu.txt'
    CUTFILE=BASECONFIG+'/qcd1l_mu.txt'
    XVAR="pt_finer"
    FITVAR="fitvar"

OPTIONS = MCA + " " + CUTFILE + " -f -P " + T + " --obj " + objName + " --s2v -j " + str(J) + " -l " + str(luminosity) + " " + str(addOpts)
 
# no friends for the moment
OPTIONS += ' -F Friends '+T+'/friends/tree_Friend_{cname}.root '
# OPTIONS += ' -F Friends '+T+'/friends/tree_FRFriend_{cname}.root '
# OPTIONS += ' --FMC Friends '+T+'/friends/tree_TrgFriend_{cname}.root '  # only for MC, they have trigger scale factors
OPTIONS += ' --fqcd-ranges %s' % fqcd_ranges.replace(","," ")
#OPTIONS += datasetOption

# event weight (NB: not needed for data, and efficiency sf not good for MC since here we have fake electrons)
# use PU reweighting for BF or BH
OPTIONS += MCweightOption

PBASE = plotterPath + "plots/fake-rate/el/"
if useMuon:
    PBASE = plotterPath + "plots/fake-rate/mu/"
if testDir != "":
    PBASE = PBASE.replace('plots/fake-rate/','plots/fake-rate/test/'+str(testDir)+'/')

if charge == "p":
    PBASE = PBASE + "pos/"
elif charge == "n":
    PBASE = PBASE + "neg/"
else:
    PBASE = PBASE + "comb/"

# EWKSPLIT="-p 'W_fake,W,Z,Top,DiBosons,data'"
EWKSPLIT="-p 'W_fake,W,Z,data'"
EWKEXCLUDE="--xp 'W_LO,Z_LO'"
if addQCDMC:
    EWKSPLIT="-p 'QCD,W,Z,data'"

MCEFF = "python " + plotterPath + "w-helicity-13TeV/dataFakeRate.py " + OPTIONS + " " + EWKSPLIT + " " + EWKEXCLUDE +" --groupBy cut " + plotterPath + "w-helicity-13TeV/make_fake_rates_sels.txt " + plotterPath + "w-helicity-13TeV/make_fake_rates_xvars.txt  "
if addQCDMC:
    MCEFF += "--sp QCD "
else:
    MCEFF += "--sp W_fake "

MCEFF += " --sP " + NUM + " --sP " + XVAR + "  --sP " + FITVAR + " " + FITVAR + "  --ytitle 'Fake rate' "
MCEFF += " --fixRatioRange --maxRatioRange 0.7 1.29 "      # ratio for other plots
LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
RANGES=" --showRatio  --ratioRange 0.50 1.99 --yrange 0 1.0  --xcut 25 100 "

MCEFF += (LEGEND+RANGES)

if addQCDMC:
    MCGO=MCEFF + " --algo=fQCD --compare QCD_prefit,data_fqcd,data_prefit "
else:
    MCGO=MCEFF + " --algo=fQCD --compare W_fake_prefit,data_fqcd,data_prefit "

for i in range(0,len(etaRange)-1):
    thisRange = etaRange[i].replace(".","p") + "_" + etaRange[i+1].replace(".","p")
    print MCEFF + " -o " + PBASE + "/fr_sub_eta_" + thisRange + ".root --bare -A onelep eta 'abs(LepGood1_eta)>" + str(etaRange[i]) + " && abs(LepGood1_eta)<" + str(etaRange[i+1]) + "' " + str(chargeSelection) + "\n"
    print "\n\n"
    print MCGO + " -i " + PBASE + "/fr_sub_eta_" + thisRange + ".root -o " + PBASE + "/fr_sub_eta_" + thisRange + "_fQCD.root --subSyst 0.2\n" 

STACK = "python " + plotterPath + "w-helicity-13TeV/stack_fake_rates_data.py "+ RANGES + LEGEND + " --comb-mode=midpoint " # :_fit

if addQCDMC:
    procToCompare="QCD_prefit,data_fqcd"
else:
    procToCompare="W_fake_prefit,data_fqcd"

for i in range(0,len(etaRange)-1):
    PATT=NUM[i]+"_vs_"+XVAR+"_"+FITVAR+"_%s"
    thisRange = etaRange[i].replace(".","p") + "_" + etaRange[i+1].replace(".","p")
    if not skipStack:
        print STACK + "-o " + PBASE + "fr_sub_eta_" + str(thisRange) + "_comp.root " + PBASE + "/fr_sub_eta_" + str(thisRange) + "_fQCD.root:" + PATT + ":" + procToCompare
