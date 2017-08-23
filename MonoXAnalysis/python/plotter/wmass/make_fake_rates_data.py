#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess

from optparse import OptionParser
parser = OptionParser(usage="%prog testname ")
parser.add_option("--mu", dest="useMuon", default=False, action='store_true', help="Do fake rate for muons");
parser.add_option("--qcdmc", dest="addQCDMC", default=False, action='store_true', help="Add QCD MC in plots (but do not subtract from data)");
parser.add_option("--singleEtaBin", dest="singleEtaBin", default=-1.0, type='float', help="Use a single eta bin (pass the upper eta boundary)");
(options, args) = parser.parse_args()

useMuon = options.useMuon
addQCDMC = options.addQCDMC  # trying to add QCD MC to graphs to be compared

T='/data1/emanuele/wmass/TREES_1LEP_53X_V3_FRELSKIM_V3'  # WARNING, for the moment it is stored in pccmsrm29, but not in lxplus
objName='tree' # name of TTree object in Root file, passed to option --obj in tree2yield.py
if useMuon:
    T='/data1/emanuele/wmass/TREES_1LEP_53X_V2'
    objName='treeProducerWMassEle'
if 'pccmsrm29' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/u2/emanuele')
elif 'lxplus' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/afs/cern.ch/work/e/emanuele/TREES/')
elif 'cmsrm-an' in os.environ['HOSTNAME']: T = T.replace('/data1/emanuele/wmass','/t3/users/dimarcoe/')
print "used trees from: ",T
J=4
BASECONFIG="wmass/wmass_e"
MCA=BASECONFIG+'/mca-qcd1l.txt'
CUTFILE=BASECONFIG+'/qcd1l.txt'
XVAR="pt_coarse"
FITVAR="mt"
NUM="FullSel"
BARREL="00_15"; ENDCAP="15_25"; ETA="1.479";

if useMuon:
    BASECONFIG="wmass/wmass_mu"
    MCA=BASECONFIG+'/mca-qcd1l_mu.txt'
    CUTFILE=BASECONFIG+'/qcd1l_mu.txt'
    XVAR="pt_finer"
    FITVAR="mt"
    NUM="MuonTightIso"
    BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";
    
if options.singleEtaBin > 0.0:
    ALL="00_" + "{0:.1f}".format(options.singleEtaBin).replace(".","p")
    ETA=options.singleEtaBin

OPTIONS = MCA+" "+CUTFILE+" -f -P "+T+" --obj "+objName+" --s2v -j "+str(J)+" -l 19.7 "
OPTIONS += ' -F mjvars/t "'+T+'/friends/evVarFriend_{cname}.root" '

PBASE = "plots/fake-rate/el/"
if useMuon:
    PBASE = "plots/fake-rate/mu/"
EWKSPLIT="-p 'W_fake,W,Z,Top,DiBosons,data'"
if addQCDMC:
    EWKSPLIT="-p 'W_fake,W,Z,data,Top,DiBosons,QCD'"

MCEFF="  python wmass/dataFakeRate.py "+ OPTIONS + " " + EWKSPLIT + " --groupBy cut wmass/make_fake_rates_sels.txt wmass/make_fake_rates_xvars.txt  "
MCEFF += "--sp W_fake "
if addQCDMC:
    MCEFF += "--sp QCD "
MCEFF += "--sP "+NUM+" --sP "+XVAR+"  --sP "+FITVAR+" "+FITVAR+"  --ytitle 'Fake rate' "
MCEFF += " --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots
LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
RANGES=" --showRatio  --ratioRange 0.00 3.99 "
if useMuon:
    RANGES+=" --yrange 0 1.0  --xcut 25 100 "
else:
    RANGES+=" --yrange 0 0.40  --xcut 25 100 "

MCEFF += (LEGEND+RANGES)

if addQCDMC:
    MCGO=MCEFF + " --algo=fQCD --compare W_fake_prefit,data_fqcd,data_prefit,QCD_prefit "
else:
    MCGO=MCEFF + " --algo=fQCD --compare W_fake_prefit,data_fqcd,data_prefit "

if options.singleEtaBin > 0.0:
    print MCEFF+" -o "+PBASE+"/fr_sub_eta_"+ALL+".root --bare -A onelep eta 'abs(LepGood_eta)<"+ETA+"'\n"
    print "\n\n"
    print MCGO + "-i " + PBASE + "/fr_sub_eta_"+ALL+".root -o "+PBASE+"/fr_sub_eta_"+ALL+"_fQCD.root --subSyst 0.2\n" 
else:
    print MCEFF+" -o "+PBASE+"/fr_sub_eta_"+BARREL+".root --bare -A onelep eta 'abs(LepGood_eta)<"+ETA+"'\n"
    print MCEFF+" -o "+PBASE+"/fr_sub_eta_"+ENDCAP+".root --bare -A onelep eta 'abs(LepGood_eta)>"+ETA+"'\n"
    print "\n\n"
    print MCGO + "-i " + PBASE + "/fr_sub_eta_"+BARREL+".root -o "+PBASE+"/fr_sub_eta_"+BARREL+"_fQCD.root --subSyst 0.2\n" 
    print MCGO + "-i " + PBASE + "/fr_sub_eta_"+ENDCAP+".root -o "+PBASE+"/fr_sub_eta_"+ENDCAP+"_fQCD.root --subSyst 0.2\n" 


STACK="python wmass/stack_fake_rates_data.py "+RANGES+LEGEND+" --comb-mode=midpoint " # :_fit
PATT=NUM+"_vs_"+XVAR+"_"+FITVAR+"_%s"

if addQCDMC:
    procToCompare="W_fake_prefit,data_fqcd,QCD_prefit"
else:
    procToCompare="W_fake_prefit,data_fqcd"

if options.singleEtaBin > 0.0:
    print STACK + "-o "+PBASE+"fr_sub_eta_"+ALL+"_comp.root "+PBASE+"/fr_sub_eta_"+ALL+"_fQCD.root:"+PATT+":"+procToCompare
else:
    for E in [BARREL,ENDCAP]:
        print STACK + "-o "+PBASE+"fr_sub_eta_"+E+"_comp.root "+PBASE+"/fr_sub_eta_"+E+"_fQCD.root:"+PATT+":"+procToCompare
