#! /bin/bash

# this script is a wrapper for the commands used to compute and pack the fake rate
# it should be run from lxplus to use ntuples on eos (the skimmed ntuples are on pccmsrm28), the check is made below

######################
# options to set
######################
#--------------------------
# choose the dataset to use (2016 B to F or 2016 B to H)
useFull2016dataset="y"
useSkimmedTrees="y" # skimmed samples are on pccmsrm28
onlypack="n" # just pack an already existing fake-rate 
# if onlypack='n', the packing might still be done at the end of FR computation, see options below
# else, if onlypack='y', it overrides the packFRfromTest option below
#--------------------------
etaRange="0.0,1.0,1.479,2.1,2.5"
wp_etaRange="loose,loose,medium,medium" # loose, medium, tight (loose uses iso < 0.2, check wmass/make_fake_rates_sels.txt)
mtRanges="0,30,30,120"
mtDefinition="trkmtfix"  # trkmtfix, trkmt, pfmtfix, pfmt
ptDefinition="pt_coarse"  # pt_coarse, pt_granular (first is mainly for QCD)
#-------------------------
istest="y"
# following option testdit is used only if istest is 'y'
testdir="SRtrees_new/fakeRate_36fb_PUTrgSF_${mtDefinition}_${ptDefinition}_pfmetLess20"
# by default, if this is a test we do not pack to avoid overwriting something when we just do tests
# you can override this feature setting this flag to 'y'
# even if you don't pack, the command you would use is printed in stdout
packFRfromTest="n" 
# anyway, the packing uses the FR made with the 2-mt-regions method, which is not good. Unles I modify the script, it is not needed (also because we have to smooth the FR)
######################
######################
# additional options to be passed to wmass/make_fake_rates_data.py
# can pass a new cut as you would do with mcPlots.py 
#addOption=" -A eleKin pfmet 'met_pt<20' -A eleKin pfmtLess40 'mt_2(met_pt,met_phi,ptCorrAndResidualScale(LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood1_r9,run,isData,evt) ,LepGood_phi)<40' "
addOption=" -A eleKin pfmet 'met_pt<20' "
#addOption=" -A eleKin awayJetPt 'LepGood_awayJet_pt > 45' "


# check we are on lxplus  
host=`echo "$HOSTNAME"`
if [[ "${useSkimmedTrees}" == "y" ]]; then
    if [[ ${host} != *"pccmsrm28"* ]]; then
	echo "Error! You must be on pccmsrm28 to use skimmed ntuples. Do ssh -XY pccmsrm28 and work from a release."
	return 0
    fi
elif [[ ${host} != *"lxplus"* ]]; then
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

cmdComputeFR="python wmass/make_fake_rates_data.py --qcdmc --mt ${mtDefinition} ${testoption} --fqcd-ranges ${mtRanges} --pt ${ptDefinition} "
if [[ "${useFull2016dataset}" == "y" ]]; then
    cmdComputeFR="${cmdComputeFR} --full2016data "
fi

if [[ "${useSkimmedTrees}" == "y" ]]; then
    cmdComputeFR="${cmdComputeFR} --useSkim "
fi

if [[ "X${etaRange}" != "X" ]]; then
    cmdComputeFR="${cmdComputeFR} --etaRange \"${etaRange}\" "
fi

if [[ "X${wp_etaRange}" != "X" ]]; then
    cmdComputeFR="${cmdComputeFR} --wp \"${wp_etaRange}\" "
fi

if [[ "X${addOption}" != "X" ]]; then
    cmdComputeFR="${cmdComputeFR} --addOpts \"${addOption}\" "
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

