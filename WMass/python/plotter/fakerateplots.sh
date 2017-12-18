#! /bin/bash

# lumi = 35.5/fb if using run2016 B to H, otherwise it is 19.3
# check in mca file which MC is being used for Z, amc@NLO, madgraph or powheg
# selection and mca of fake rate to see how plots look like

echo ""

# first, choose which of the three analysis you want to run (plots for computation region, application one, closure test
# select also if you want to use data GH
doCompRegion="n" # y or n (or any key but y for no)
doApplRegion="n"
doApplControlRegion="n"
doSignalRegion="n"
doFakeRateCheckData="y"  # in principle it is the same region as doApplControlRegion, but the former has the direct selection, while the latter has the inverted one
doClosureTest="n"
useDataGH="y"
useEBorEE="EE" # ALL (EB and EE), EB (EB only), EE (EE only) (actually any key different from EB or EE means both)
runBatch="n" # to be implemented
queueForBatch="cmscaf1nd"
useSkimmedTrees="y" # skimmed samples are on both pccmsrm28 and eos 
usePtCorrForScaleFactors="n" # y: use corrected pt for scsle factor weight; n: use LepGood_pt (which is what would ave been used if the scale factors where in a friend tree)
etaBinBoundaries=("0.0" "1.479" "2.1" "2.5")

treepath="" # set below depending on where we are
mcafile="mca-80X_V3.txt" # if using skimmed trees on pccmsrm28, few top samples are missing, be careful (new mca is automatically set below)
mcafileFRcheck="mca-80X_V3_FRcheck.txt"  # automatically used instead of mcafile when doing part under doFakeRateCheckData
# not needed anymore, missing samples were produced
# if [[ "${useSkimmedTrees}" == "y" ]]; then
#     mcafile="mca-80X_V3_skimTrees.txt"
# fi
cutfile="qcd1l_SRtrees.txt"
plotfile="test_plots.txt"
#excludeprocesses="data,Z_LO,W_LO,Z,Top,DiBosons"
excludeprocesses="Z_LO,W_LO" # decide whether to use NLO (amc@NLO) or LO (MadGraph) MC, non both! In case you can add other samples (Top, Dibosons) to speed up things
#selectplots="etal1"  # if empty it uses all plots in cfg file
selectplots="trkmt,ptl1,etal1,pfmt,pfmet"  # if empty it uses all plots in cfg file
maxentries="2000000000" # max int number is > 2*10^9
#maxentries="10"
outdirComp="full2016dataBH_puAndTrgSf_ptResScale_8dec"
#outdirComp="test"
outdirAppl="full2016dataBH_puAndTrgSf_ptResScale_8dec"
outdirFRcheck="full2016dataBH_puAndTrgSf_ptResScale_11dec"
#outdirFRcheck="testBatch"
outdirSignal="full2016dataBH_puAndTrgSf_ptResScale_8dec"

# end of settings to be changed by user
#----------------------------------------

host=`echo "$HOSTNAME"`
if [[ "${runBatch}" == "y" ]]; then
    if [[ ${host} != *"lxplus"* ]]; then
	echo "Error! You must be on lxplus to run on batch queues. Do ssh -XY lxplus and work from a release."
	return 0
    fi
fi
mypath="$PWD"

evalScram="eval \`scramv1 runtime -sh\`"
batchFolder="${mypath}/jobsLog"
baseBatchScript="${batchFolder}/baseBatchScript.sh"
batchFileName="${batchFolder}/src/PLOTREGION_ETABIN.sh"  # PLOTREGION and ETABIN will be changed to proper names depending on region
###############################################
# now we build base script to submit batch jobs
# it will be used later to create script to submit batch jobs
###############################################
cat > ${baseBatchScript} <<EOF
#! /bin/bash

cd ${mypath}
${evalScram}

EOF
###############################################


ptcorr="ptElFull(LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood1_r9,run,isData,evt)"
ptForScaleFactors="LepGood1_pt"
if [[ "${usePtCorrForScaleFactors}" == "y" ]]; then
    echo "Will use corrected pt instead of LepGood1_pt to compute the trigger/efficiency scale factors"
    ptForScaleFactors="${ptcorr}"
fi


if [[ ${host} == *"pccmsrm28"* ]]; then
    treepath="/u2/emanuele/wmass/" # from pccmsrm28 
elif [[ ${host} == *"lxplus"* ]]; then
    treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco"
fi

if [[ "${runBatch}" == "y" ]]; then
    if [[ ${host} != *"lxplus"* ]]; then
	echo "Warning: to run on batch you must use the trees on eos and be on lxplus."
	return 0
    fi
fi


luminosity=""
dataOption=""
MCweightOption=""
if [[ "${useDataGH}" == "y" ]]; then
    #dataOption=" --pg 'data := data_B,data_C,data_D,data_E,data_F,data_G,data_H' "
    luminosity="35.9"
    MCweigthOption=" -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,${ptForScaleFactors},LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,${ptForScaleFactors},LepGood1_eta)' "
else 
    #dataOption=" --pg 'data := data_B,data_C,data_D,data_E,data_F' --xp data_G,data_H "
    luminosity="19.3"
    MCweigthOption=" -W 'puw2016_nTrueInt_BF(nTrueInt)*trgSF_We(LepGood1_pdgId,${ptForScaleFactors},LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,${ptForScaleFactors},LepGood1_eta)' "
fi

##############################
## WARNING ##
# to use a python command with options froma bash script, do
# command="python [args] [options]"
# echo "${command}" | bash
# otherwise the parsing of the option parameters is not done correctly

commonCommand="python ${mypath}/mcPlots.py -f -j 4 -l ${luminosity} --s2v --tree treeProducerWMass --obj tree --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0.5 1.5 --fixRatioRange ${mypath}/w-helicity-13TeV/wmass_e/${mcafile} ${mypath}/w-helicity-13TeV/wmass_e/${cutfile} ${mypath}/w-helicity-13TeV/wmass_e/${plotfile} --max-entries ${maxentries} ${dataOption} ${MCweigthOption} "

if [[ "X${excludeprocesses}" != "X" ]]; then
    commonCommand="${commonCommand} --xp ${excludeprocesses}"
fi

if [[ "X${selectplots}" != "X" ]]; then
    commonCommand="${commonCommand} --sP ${selectplots}"
fi


####################
# some selections
###################
inEB=" -A eleKin EB 'abs(LepGood1_etaSc) < 1.479' "
inEE=" -A eleKin EE 'abs(LepGood1_etaSc) > 1.479' "

innerEE=" -A eleKin eta1p479to2p1 'abs(LepGood1_etaSc)>1.479 && abs(LepGood1_etaSc)<2.1' "
outerEE=" -A eleKin eta2p1to2p5 'abs(LepGood1_etaSc)>2.1 && abs(LepGood1_etaSc)<2.5' "

not_pass_tightWP="-A eleKin not-fullTightID 'LepGood1_tightId < 3 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.0588 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.0571 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.0695 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.0821 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP_iso0p2="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP_iso0p15="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.15 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.15 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_looseWP="-A eleKin not-fullLooseID 'LepGood1_tightId < 1 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.0994 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.107 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_looseWP_iso0p2="-A eleKin not-fullLooseID 'LepGood1_tightId < 1 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

# use bult-in functions in functions.cc, which automatically select EB or EE, manage cuts and so on
FRnumSel=" -A eleKin FRnumSel 'pass_FakerateNumerator2016((abs(LepGood1_etaSc)<1.479),LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "

notFRnumSel="-A eleKin failFRnumSel 'pass_FakerateApplicationRegion2016(abs(LepGood1_etaSc)<1.479,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "

Wsel="-A eleKin WregionSel '(${ptcorr})>30 && met_pt>20 && pt_2(${ptcorr}, LepGood1_phi, met_trkPt, met_trkPhi ) < 40 && mt_2(met_trkPt,met_trkPhi,${ptcorr},LepGood1_phi) < 110'"

mtCutApplControlRegion="-A eleKin pfmt 'mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) < 60'"
#mtCutApplControlRegion="-A eleKin pfmt 'mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) > 40 && mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) < 60'"
mtCutApplSignalRegion="-A eleKin pfmt 'mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) > 60'"

########################

# computation region
if [[ "${doCompRegion}" == "y" ]]; then
    if [[ "${useSkimmedTrees}" == "y" ]]; then
	treedir="TREES_1LEP_80X_V3_FRELSKIM_V3"  # skimmed tree from pccmsrm28    
    else
	treedir="TREES_1LEP_80X_V3"
    fi
    
    treeAndFriendCompRegion=" -P ${treepath}/${treedir}/ -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root "
    commonCompReg="${commonCommand} ${treeAndFriendCompRegion}"

    if [[ "${useEBorEE}" != "EE" ]]; then

	commonCompRegEB="${commonCompReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/denSel/EB/ ${inEB} "
	echo "${commonCompRegEB}"
	echo "${commonCompRegEB}" | bash
	commonCompRegEB="${commonCompReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/numSel/EB/ ${inEB} "
	echo "${commonCompRegEB} ${FRnumSel} " 
	echo "${commonCompRegEB} ${FRnumSel} " | bash

    fi

    if [[ "${useEBorEE}" != "EB" ]]; then
	commonCompRegEE="${commonCompReg} ${inEE} "

        # den
	commonCompRegEEin="${commonCompRegEE} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/denSel/EE_eta1p479to2p1/ ${innerEE}"
	echo "${commonCompRegEEin}"
	echo "${commonCompRegEEin}" | bash
	# commonCompRegEEout="${commonCompRegEE} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/denSel/EE_eta2p1to2p5/ ${outerEE}"
	# echo "${commonCompRegEEout}"
	# echo "${commonCompRegEEout}" | bash

	# num
	commonCompRegEEin="${commonCompRegEE} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/numSel/EE_eta1p479to2p1/ ${innerEE}"
	echo "${commonCompRegEEin} ${FRnumSel} " 
	echo "${commonCompRegEEin} ${FRnumSel} " | bash
	# commonCompRegEEout="${commonCompRegEE} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/numSel/EE_eta2p1to2p5/ ${outerEE}"
	# echo "${commonCompRegEEout} ${FRnumSel} " 
	# echo "${commonCompRegEEout} ${FRnumSel} " | bash
    fi
fi

# application region

if [[ "${doApplRegion}" == "y" ]] || [[ "${doApplControlRegion}" == "y" ]] || [[ "${doSignalRegion}" == "y" ]]; then

    if [[ "${useSkimmedTrees}" == "y" ]]; then
	treedir="TREES_1LEP_80X_V3_WENUSKIM_V3"  # skimmed tree from pccmsrm28
    else 
	treedir="TREES_1LEP_80X_V3"
    fi

    treeAndFriendApplRegion=" -P ${treepath}/${treedir}/ -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root "
    commonApplReg="${commonCommand} ${treeAndFriendApplRegion} -X nJet30 ${Wsel} ${notFRnumSel}"
    commonSigReg="${commonCommand} ${treeAndFriendApplRegion} -X nJet30 ${Wsel} ${FRnumSel}"

    if [[ "${useEBorEE}" != "EE" ]]; then

	if [[ "${doApplRegion}" == "y" ]]; then
	    commonApplRegEB="${commonApplReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/application_region/${outdirAppl}/EB/ ${inEB}" 
	    echo "${commonApplRegEB}"
	    echo "${commonApplRegEB}" | bash
	fi

	if [[ "${doApplControlRegion}" == "y" ]]; then
	    commonApplControlRegEB="${commonApplReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/application_region/${outdirAppl}/EB/ ${inEB} ${mtCutApplControlRegion}" 
	    echo "${commonApplControlRegEB}"
	    echo "${commonApplControlRegEB}" | bash
	fi

	if [[ "${doSignalRegion}" == "y" ]]; then
	    commonSigRegEB="${commonSigReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/signal_region/${outdirSignal}/EB/ ${inEB} ${mtCutApplSignalRegion}"
	    echo "${commonSigRegEB}"
            echo "${commonSigRegEB}" | bash
	fi

    fi

    if [[ "${useEBorEE}" != "EB" ]]; then

	if [[ "${doApplRegion}" == "y" ]]; then
	    commonApplRegEE="${commonApplReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/application_region/${outdirAppl}/EE_eta1p479to2p1/ ${innerEE}" 
	    echo "${commonApplRegEE}"
	    echo "${commonApplRegEE}" | bash
	fi

	if [[ "${doApplControlRegion}" == "y" ]]; then
	    commonApplControlRegEE="${commonApplReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/application_region/${outdirAppl}/EE_eta1p479to2p1/ ${innerEE} ${mtCutApplControlRegion}" 
	    echo "${commonApplControlRegEE}"
	    echo "${commonApplControlRegEE}" | bash
	fi

	if [[ "${doSignalRegion}" == "y" ]]; then
	    commonSigRegEE="${commonSigReg} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/signal_region/${outdirSignal}/EE_eta1p479to2p1/ ${innerEE} ${mtCutApplSignalRegion}"
	    echo "${commonSigRegEE}"
            echo "${commonSigRegEE}" | bash
	fi

    fi
fi

echo ""
echo ""
echo ""

if [[ "${doFakeRateCheckData}" == "y" ]]; then

    if [[ "${useSkimmedTrees}" == "y" ]]; then
	treedir="TREES_1LEP_80X_V3_WENUSKIM_V3"  # skimmed tree from pccmsrm28
    else 
	treedir="TREES_1LEP_80X_V3"
    fi

    # we change the mca file in commonCommand with the new one specific for this study
    commonCommandFRcheck="${commonCommand}"
    commonCommandFRcheck="${commonCommandFRcheck/${mcafile}/${mcafileFRcheck}}"
    #echo "commonCommandFRcheck = ${commonCommandFRcheck}"

    #commonCommandFRcheck="python mcPlots.py -f -j 4 -l ${luminosity} --s2v --tree treeProducerWMass --obj tree --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0.5 1.5 --fixRatioRange w-helicity-13TeV/wmass_e/${mcafileFRcheck} w-helicity-13TeV/wmass_e/${cutfile} w-helicity-13TeV/wmass_e/${plotfile} --max-entries ${maxentries} ${dataOption} ${MCweigthOption} --xp ${excludeprocesses}"

    treeAndFriendFRcheck=" -P ${treepath}/${treedir}/ -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root "
    #commonFRcheck="${commonCommandFRcheck} ${treeAndFriendFRcheck} -X nJet30 ${Wsel} ${FRnumSel} ${mtCutApplControlRegion} ${dataOptionFakes}"
    commonFRcheck="${commonCommandFRcheck} ${treeAndFriendFRcheck} -X nJet30 ${Wsel} ${FRnumSel} ${mtCutApplControlRegion}"

    regionName="frCheckData_region"
    thisBatchFileName="${batchFileName}"
    thisBatchFileName=${thisBatchFileName/PLOTREGION/${regionName}}
    
    if [[ "${useEBorEE}" != "EE" ]]; then

	etabin=""
	thisBatchFileName=${thisBatchFileName/ETABIN/${etabin}}

	batchLogFileName="${batchFileNameBase}_EB.log"
	batchSrcFileName="${batchFileNameBase/log/src}"
	batchSrcFileName="${batchSrcFileName}_EB.sh"

	commonFRcheckEB="${commonFRcheck} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/frCheckData_region/${outdirFRcheck}/EB/ ${inEB}" 
	echo "${commonFRcheckEB}"
        # print to file 
	# echo "echo \"#! /bin/bash \" > ${batchSrcFileName}" | bash
	# echo "echo \"cd ${mypath}/\" >> ${batchSrcFileName}" | bash
	# echo "echo \"eval \\`scramv1 runtime -sh\\`\" >> ${batchSrcFileName}" | bash
	# echo "echo \"${commonFRcheckEB}\" >> ${batchSrcFileName}" | bash

	if [[ "${runBatch}" == "y" ]]; then
	    echo ""
	    commandBatch="bsub -q ${queueForBatch} -oo ${batchLogFileName}  \"source ${batchSrcFileName}\" "
	    echo "${commandBatch}"
	    #echo "${commandBatch}" | bash
	fi

    fi
    if [[ "${useEBorEE}" != "EB" ]]; then
	commonFRcheckEE="${commonFRcheck} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/frCheckData_region/${outdirFRcheck}/EE_eta1p479to2p1/ ${innerEE}" 
	echo "${commonFRcheckEE}"
	echo "${commonFRcheckEE}" | bash
	#
	commonFRcheckEE="${commonFRcheck} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/frCheckData_region/${outdirFRcheck}/EE_eta2p1to2p5/ ${outerEE}" 
	echo "${commonFRcheckEE}"
	echo "${commonFRcheckEE}" | bash
    fi
fi

# QCD closure test
mca_clos="mca-80X-qcdClosureTest.txt"
sel_clos="wenu_80X.txt"
plot_clos="qcdClosureTest_plots.txt"
plotmode_clos="stack" # norm, nostack, stack (but with just MC we can define a signal and remove it from the stack with --noStackSig)
#subdir_clos="puBH_TrgSfBH"
subdir_clos="testagain_noMetWpt"
maxentries_clos="2000000000"
#maxentries_clos="1000"
otherCut=" -X pfmet -X w_pt "

cmdClosure="python ${mypath}/mcPlots.py -P ${treepath}/${treedir}/ -f -j 4 -l ${luminosity} --s2v --tree treeProducerWMass --obj tree -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root --lspam '     #bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0.0 2.0 --fixRatioRange ${mypath}/w-helicity-13TeV/wmass_e/${mca_clos} ${mypath}/w-helicity-13TeV/wmass_e/${sel_clos} ${mypath}/w-helicity-13TeV/wmass_e/${plot_clos} --plotmode ${plotmode_clos} --max-entries ${maxentries_clos} --sp QCD --ratioDen QCD --ratioNums QCD_mcfakes,background --ratioYLabel 'fake/MC' --noStackSig --showIndivSigs ${MCweigthOption} "

# --sp QCD --noStackSig --showSigShape --ratioNums background

qcdclosTest_cut=" -R id looseWP_iso0p2 'LepGood1_tightId >= 1 && if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA < 0.2 && abs(LepGood1_dz) < 0.1 && abs(LepGood1_dxy) < 0.05, LepGood1_relIso04EA < 0.2 && abs(LepGood1_dz) < 0.2 && abs(LepGood1_dxy) < 0.1) && LepGood1_lostHits <= 1 && LepGood1_convVeto == 1' -R w_tkmt w_tkmt 'mt_2(met_trkPt,met_trkPhi,LepGood1_pt,LepGood1_phi) < 110' ${otherCut} "

if [[ "${doClosureTest}" == "y" ]]; then
    if [[ "${useEBorEE}" != "EE" ]]; then
	echo "${cmdClosure} ${qcdclosTest_cut} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/closureTest/${subdir_clos}/EB ${inEB}" | bash
    fi
    if [[ "${useEBorEE}" != "EB" ]]; then
	echo "${cmdClosure} ${qcdclosTest_cut} --pdir ${mypath}/plots/test/${treedir}/fakeRateSel/closureTest/${subdir_clos}/EE ${inEE}" | bash
    fi
fi
