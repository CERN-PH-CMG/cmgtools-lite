#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess

from optparse import OptionParser
parser = OptionParser(usage="%prog testname ")
parser.add_option("--mu", dest="useMuon", default=False, action='store_true', help="Do fake rate for muons");
parser.add_option("--qcdmc", dest="addQCDMC", default=False, action='store_true', help="Add QCD MC in plots (but do not subtract from data)");
parser.add_option("--singleEtaBin", dest="singleEtaBin", default=-1.0, type='float', help="Use a single eta bin (pass the upper eta boundary)");
parser.add_option("--charge", dest="charge", default="", type='string', help="Select charge: p for positive, n for negative");
parser.add_option("--wp", dest="workingPoint", default="tight", type='string', help="Select ID working point: tight (default), medium, loose");
parser.add_option("--useSRtrees", dest="useSRtrees", default=False, action='store_true', help="Use trees of signal region instead of fake-rate trees (and apply HLT_SingleEl)");
parser.add_option("--test", dest="test", default="", type='string', help="pass the name of a folder (mandatory) to store test FR plots. It is created in plots/fake-rate/test/");
parser.add_option("--fqcd-ranges", dest="fqcd_ranges", default="0,40,50,120", type='string', help="Pass a list of 4 comma separated numbers that represents the ranges for the two mT regions to compute the fake rate");
parser.add_option("--mt", dest="fitvar", default="trkmtfix", type='string', help="Select mT definition: pfmt, trkmt, pfmtfix, trkmtfix");
(options, args) = parser.parse_args()

useMuon = options.useMuon
addQCDMC = options.addQCDMC  # trying to add QCD MC to graphs to be compared
charge = str(options.charge)
useSRtrees = options.useSRtrees
testDir = str(options.test)
workingPoint = options.workingPoint
fqcd_ranges = str(options.fqcd_ranges)
fitvar = str(options.fitvar)


if fqcd_ranges.count(",") != 3:
    print "warning: options --fqcd-ranges requires 4 numbers separated by commas (3 commas expected), but %s was passed" % fqcd_ranges
    quit()

if workingPoint not in ["loose","medium","tight"]:
    print "warning: unknown working point %s, use loose, medium or tight" % workingPoint
    quit()
numForWP={'loose': 'FullSel_looseID', 'medium': 'FullSel_mediumID', 'tight': 'FullSel_tightID'}

if fitvar not in ["pfmt", "trkmt", "pfmtfix", "trkmtfix"]:
    print "warning: unknown mt definition %s, use pfmt, trkmt, pfmtfix, trkmtfix" % fitvar
    quit()

if useMuon:
    addQCDMC = True

chargeSelection = ""
if charge != "":
    if charge == "p":
        chargeSelection = "-A onelep positive 'LepGood1_pdgId < 0'"
    elif charge == "n":
        chargeSelection = "-A onelep negative 'LepGood1_pdgId > 0'"
    else:
        print "%s is not a valid input for charge setting: use p or n" % charge
        quit()

T="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_FR/"  # WARNING, for the moment it is stored on eos, not in pccmsrm29 or in lxplus
if useSRtrees:
    T="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3/" 
objName='tree' # name of TTree object in Root file, passed to option --obj in tree2yield.py
# if 'pccmsrm29' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/u2/emanuele')
# elif 'lxplus' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/afs/cern.ch/work/e/emanuele/TREES/')
# elif 'cmsrm-an' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/t3/users/dimarcoe/')
print "used trees from: ",T

luminosity = 19.3
J=4

BASECONFIG="wmass/wmass_e"
MCA=BASECONFIG+'/mca-qcd1l.txt'
CUTFILE=BASECONFIG+'/qcd1l.txt'
XVAR="pt_coarse"
FITVAR=fitvar
NUM=numForWP[str(workingPoint)]
BARREL="00_15"; ENDCAP="15_25"; ETA="1.479";
if useMuon:
    BASECONFIG="wmass/wmass_mu"
    MCA=BASECONFIG+'/mca-qcd1l_mu.txt'
    CUTFILE=BASECONFIG+'/qcd1l_mu.txt'
    XVAR="pt_finer"
    FITVAR="fitvar"
    NUM="MuonTightIso"
    BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";

if useSRtrees:
    MCA = MCA.replace('mca-qcd1l','mca-qcd1l_SRtrees')
    CUTFILE = CUTFILE.replace('qcd1l','qcd1l_SRtrees')

OPTIONS = MCA+" "+CUTFILE+" -f -P "+T+" --obj "+objName+" --s2v -j "+str(J)+" -l "+str(luminosity)
# no friends for the moment
OPTIONS += ' -F Friends '+T+'/friends/tree_Friend_{cname}.root '
OPTIONS += ' -F Friends '+T+'/friends/tree_FRFriend_{cname}.root '
OPTIONS += ' --fqcd-ranges %s' % fqcd_ranges.replace(","," ")

# event weight (NB: not needed for data, and sf not good for MC since here we have fake electrons)
# puwBF should be used, but for the moment I don't
#OPTIONS += ' -W "puwBF" '

if options.singleEtaBin > 0.0:
    ALL="00_" + "{0:.1f}".format(options.singleEtaBin).replace(".","p")
    ETA=options.singleEtaBin

PBASE = "plots/fake-rate/el/"
if useSRtrees:
    PBASE = "plots/fake-rate/el_SRtrees/"
if useMuon:
    PBASE = "plots/fake-rate/mu/"
    if useSRtrees:
        PBASE = "plots/fake-rate/mu_SRtrees/"
if testDir != "":
    PBASE = PBASE.replace('plots/fake-rate/','plots/fake-rate/test/'+str(testDir)+'/')

if charge == "p":
    PBASE = PBASE + "pos/"
elif charge == "n":
    PBASE = PBASE + "neg/"
else:
    PBASE = PBASE + "comb/"

# EWKSPLIT="-p 'W_fake,W,Z,Top,DiBosons,data'"
# check if Diboson and Top samples are present for the FR trees at 13 TeV
EWKSPLIT="-p 'W_fake,W,Z,data'"
if addQCDMC:
    EWKSPLIT="-p 'QCD,W,Z,data'"
#if useSRtrees:
#    EWKSPLIT = EWKSPLIT.replace('W,Z,data','W,Z,Top,DiBosons,data')

MCEFF="  python wmass/dataFakeRate.py "+ OPTIONS + " " + EWKSPLIT + " --groupBy cut wmass/make_fake_rates_sels.txt wmass/make_fake_rates_xvars.txt  "
if addQCDMC:
    MCEFF += "--sp QCD "
else:
    MCEFF += "--sp W_fake "

MCEFF += "--sP "+NUM+" --sP "+XVAR+"  --sP "+FITVAR+" "+FITVAR+"  --ytitle 'Fake rate' "
MCEFF += " --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots
LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
RANGES=" --showRatio  --ratioRange 0.50 1.99 "
RANGES+=" --yrange 0 1.0  --xcut 25 100 "

MCEFF += (LEGEND+RANGES)

if addQCDMC:
    MCGO=MCEFF + " --algo=fQCD --compare QCD_prefit,data_fqcd,data_prefit "
else:
    MCGO=MCEFF + " --algo=fQCD --compare W_fake_prefit,data_fqcd,data_prefit "

if options.singleEtaBin > 0.0:
    print MCEFF+" -o "+PBASE+"/fr_sub_eta_"+ALL+".root --bare -A onelep eta 'abs(LepGood1_eta)<"+ETA+"' " + str(chargeSelection) +"\n"
    print "\n\n"
    print MCGO + "-i " + PBASE + "/fr_sub_eta_"+ALL+".root -o "+PBASE+"/fr_sub_eta_"+ALL+"_fQCD.root --subSyst 0.2\n" 
else:
    print MCEFF+" -o "+PBASE+"/fr_sub_eta_"+BARREL+".root --bare -A onelep eta 'abs(LepGood1_eta)<"+ETA+"' " + str(chargeSelection) +"\n"
    print MCEFF+" -o "+PBASE+"/fr_sub_eta_"+ENDCAP+".root --bare -A onelep eta 'abs(LepGood1_eta)>"+ETA+"' " + str(chargeSelection) +"\n"
    print "\n\n"
    print MCGO + "-i " + PBASE + "/fr_sub_eta_"+BARREL+".root -o "+PBASE+"/fr_sub_eta_"+BARREL+"_fQCD.root --subSyst 0.2\n" 
    print MCGO + "-i " + PBASE + "/fr_sub_eta_"+ENDCAP+".root -o "+PBASE+"/fr_sub_eta_"+ENDCAP+"_fQCD.root --subSyst 0.2\n" 


STACK="python wmass/stack_fake_rates_data.py "+RANGES+LEGEND+" --comb-mode=midpoint " # :_fit
PATT=NUM+"_vs_"+XVAR+"_"+FITVAR+"_%s"

if addQCDMC:
    procToCompare="QCD_prefit,data_fqcd"
else:
    procToCompare="W_fake_prefit,data_fqcd"

if options.singleEtaBin > 0.0:
    print STACK + "-o "+PBASE+"fr_sub_eta_"+ALL+"_comp.root "+PBASE+"/fr_sub_eta_"+ALL+"_fQCD.root:"+PATT+":"+procToCompare
else:
    for E in [BARREL,ENDCAP]:
        print STACK + "-o "+PBASE+"fr_sub_eta_"+E+"_comp.root "+PBASE+"/fr_sub_eta_"+E+"_fQCD.root:"+PATT+":"+procToCompare
