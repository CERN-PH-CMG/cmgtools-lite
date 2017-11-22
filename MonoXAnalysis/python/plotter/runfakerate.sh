#! /bin/bash

# this script is a wrapper for the commands used to compute and pack the fake rate
# it should be run from lxplus, the check is made below

######################
# options to set
######################
#--------------------------
# choose the dataset to use (2016 B to F or 2016 B to H)
useDetector="EE" #  EB or EE to do only barrel or endcap, any other value makes the code run both EB and EE
useFull2016dataset="y"
useSkimmedTrees="n"
onlypack="n" # just pack an already existing fake-rate 
# if onlypack='n', the packing might still be done at the end of FR computation, see options below
# else, if onlypack='y', it overrides the packFRfromTest option below
#--------------------------
istest="y"
testdir="SRtrees_new/hltID_mediumWP_36fb_PUTrgSF_trkmtfix_0_50_50_120_EE"  # used only if istest is 'y', be as much informative as possible
# by default, if this is a test we do not pack to avoid overwriting something when we just do tests
# you can override this feature setting this flag to 'y'
# even if you don't pack, the command you would use is printed in stdout
packFRfromTest="n" 
#-------------------------
WPoption="medium" # loose, medium, tight (loose uses iso < 0.2, check wmass/make_fake_rates_sels.txt)
mtRanges="0,50,50,120"
mtDefinition="trkmtfix"  # trkmtfix, trkmt, pfmtfix, pfmt
######################
######################
# additional options to be passed to wmass/make_fake_rates_data.py
# can pass a new cut as you would do with mcPlots.py 
addOption=""
#addOption=" -A eleKin awayJetPt 'LepGood_awayJet_pt > 45' "


# check we are on lxplus  
host=`echo "$HOSTNAME"`
if [[ ${host} != *"lxplus"* ]]; then
  echo "Error! You must be on lxplus. Do ssh -XY lxplus and work from a release."
  return 0
fi

srtreeoption=""
frGraphDir="el"

packdir="${frGraphDir}"
if [[ "${istest}" == "y" ]]; then
    testoption=" --test ${testdir}/ "
    packdir="test/${testdir}/${frGraphDir}"
fi

cmdComputeFR="python wmass/make_fake_rates_data.py --qcdmc --wp ${WPoption} --mt ${mtDefinition} ${testoption} --fqcd-ranges ${mtRanges} --addOpts \"${addOption}\" "
if [[ "${useFull2016dataset}" == "y" ]]; then
    cmdComputeFR="${cmdComputeFR} --full2016data "
fi

if [[ "${useSkimmedTrees}" == "y" ]]; then
    cmdComputeFR="${cmdComputeFR} --useSkim "
fi

if [[ "${useDetector}" == "EB" ]]; then
    cmdComputeFR="${cmdComputeFR} --EB-only "
elif [[ "${useDetector}" == "EE" ]]; then
    cmdComputeFR="${cmdComputeFR} --EE-only "
fi

if [[ "${onlypack}" == "y" ]]; then
    echo "onlypack=='y': will not run fake-rate script, but just pack."
    echo "Packing from plots/fake-rate/${packdir}/comb/"
else
    echo "Running: ${cmdComputeFR}"
    echo "${cmdComputeFR} | grep python > commands4fakeRate.sh" | bash
    echo "The commands used for fake-rate are stored in commands4fakeRate.sh"
    cat commands4fakeRate.sh | bash  # here we really run the commands saved in commands4fakeRate.sh
fi

# now we pack the FR histograms
cmdPackFR="python wmass/pack_fake_rates_data.py ${CMSSW_BASE}/src/CMGTools/MonoXAnalysis/data/fakerate/FR_data_el.root --lep-flavour el --input-path plots/fake-rate/${packdir}/comb/"
if [[ "${packFRfromTest}" == "y" ]] || [[ "${istest}" != "y" ]] || [[ "${onlypack}" == "y" ]]; then
    echo "${cmdPackFR}" | bash
else
    echo "Not packing FR because istest='y'. You can force the packing setting packFRfromTest='y'."
    echo "Anyway, the command to pack is reported below"
    echo "${cmdPackFR}"
fi

