#! /bin/bash

# this script is a wrapper for the commands used to compute and pack the fake rate
# it should be run from lxplus, the check is made below

######################
# options to set
######################
#--------------------------
# choose the dataset to use (2016 B to F or 2016 B to H)
useFull2016dataset="y"
#--------------------------
istest="y"
testdir="SRtrees_new/hltID_looseWP_iso0p2_noSF_trkmtfix_0_50_50_120"  # used only if istest is 'y', be as much informative as possible
# by default, if this is a test we do not pack to avoid overwriting something when we just do tests
# you can override this feature setting this flag to 'y'
# even if you don't pack, the command you would use is printed in stdout
packFRfromTest="n" 
#-------------------------
WPoption="loose" # loose, medium, tight (loose uses iso < 0.2, check wmass/make_fake_rates_sels.txt)
mtRanges="0,50,50,120"
mtDefinition="trkmtfix"
######################
######################

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

cmdComputeFR="python wmass/make_fake_rates_data.py --qcdmc --wp ${WPoption} --mt ${mtDefinition} ${testoption} --fqcd-ranges ${mtRanges}"
if [[ "${useFull2016dataset}" == "y" ]]; then
    cmdComputeFR="${cmdComputeFR} --full2016data "
fi

echo "${cmdComputeFR} | grep python > commands4fakeRate.sh" | bash
cat commands4fakeRate.sh | bash  # here we really run the commands saved in commands4fakeRate.sh

# now we pack the FR histograms
cmdPackFR="python wmass/pack_fake_rates_data.py ${CMSSW_BASE}/src/CMGTools/MonoXAnalysis/data/fakerate/FR_data_el.root --lep-flavour el --input-path plots/fake-rate/${packdir}/comb/"
if [[ "${packFRfromTest}" == "y" ]] || [[ "${istest}" != "y" ]]; then
    echo "${cmdPackFR}" | bash
else
    echo "Not packing FR because istest='y'. You can force the packing setting packFRfromTest='y'."
    echo "Anyway, the command to pack is reported below"
    echo "${cmdPackFR}"
fi

