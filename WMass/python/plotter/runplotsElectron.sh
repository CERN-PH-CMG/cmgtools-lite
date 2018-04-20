#! /bin/bash

# lumi = 35.9/fb if using run2016 B to H, otherwise it is 19.3
# check in mca file which MC is being used for Z, amc@NLO, madgraph or powheg
# selection and mca of fake rate to see how plots look like

# This script prints the commands to produce plots or send jobs to manage the production 

echo ""
plotterPath="${CMSSW_BASE}/src/CMGTools/WMass/python/plotter"

#####################################################
# some selections (other customizable options start below)
# cuts are added after eleKin selection step (check in the cut file, could use also a dummy step like alwaystrue)
#####################################################

#ptcorr="ptElFull(LepGood1_pt,LepGood1_eta,LepGood1_phi,LepGood1_r9,run,isData,evt)"
#ptcorr="LepGood1_calPt"
ptcorr="ptElFull(LepGood1_calPt,LepGood1_eta)"

inEB=" -A eleKin EB 'abs(LepGood1_eta) < 1.479' "
inEE=" -A eleKin EE 'abs(LepGood1_eta) > 1.479' "

not_pass_tightWP="-A eleKin not-fullTightID 'LepGood1_tightId < 3 || if3(abs(LepGood1_eta)<1.479,LepGood1_relIso04EA > 0.0588 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.0571 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_eta)<1.479,LepGood1_relIso04EA > 0.0695 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.0821 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP_iso0p2="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_eta)<1.479,LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP_iso0p15="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_eta)<1.479,LepGood1_relIso04EA > 0.15 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.15 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_looseWP="-A eleKin not-fullLooseID 'LepGood1_tightId < 1 || if3(abs(LepGood1_eta)<1.479,LepGood1_relIso04EA > 0.0994 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.107 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_looseWP_iso0p2="-A eleKin not-fullLooseID 'LepGood1_tightId < 1 || if3(abs(LepGood1_eta)<1.479,LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

# use bult-in functions in functions.cc, which automatically select EB or EE, manage cuts and so on
#FRnumSel=" -A eleKin FRnumSel 'pass_FakerateNumerator2016((abs(LepGood1_eta)<1.479),LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "
#notFRnumSel="-A eleKin failFRnumSel 'pass_FakerateApplicationRegion2016(abs(LepGood1_eta)<1.479,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "

# use variables in friend trees, which were filled with the conditions to pass the ID+iso (the one we decided to use at the moment)
FRnumSel=" -A eleKin FRnumSel 'LepGood1_customId == 1' "  #looseID + iso<0.2 in EB, medium ID in EE
#FRnumSel=" -A eleKin FRnumSel 'pass_FakerateNumerator_loose2016(fabs(LepGood1_eta)<1.479,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "
#FRnumSel=" -A eleKin FRnumSel 'pass_FakerateNumerator_medium2016(fabs(LepGood1_eta)<1.479,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "

notFRnumSel="-A eleKin failFRnumSel 'LepGood1_customId == 0' " #looseID + iso<0.2 in EB, medium ID in EE
#notFRnumSel="-A eleKin failFRnumSel ' !pass_FakerateNumerator_loose2016(fabs(LepGood1_eta)<1.479,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "
#notFRnumSel="-A eleKin failFRnumSel ' !pass_FakerateNumerator2016(fabs(LepGood1_eta)<1.479,LepGood1_tightId,LepGood1_dxy,LepGood1_dz,LepGood1_lostHits,LepGood1_convVeto,LepGood1_relIso04EA)' "

#Wsel="-A eleKin WregionSel '(${ptcorr})>30 && met_pt>20 && pt_2(${ptcorr}, LepGood1_phi, met_trkPt, met_trkPhi ) < 40 && mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) < 110'"
#Wsel="-A eleKin WregionSel '(${ptcorr})>30 && met_pt>20'"
Wsel="-A eleKin WregionSel 'ptElFull(LepGood1_calPt,LepGood1_eta) > 30 && ptElFull(LepGood1_calPt,LepGood1_eta) < 45'"
HLT27sel="-R HLT_SingleEL HLT_Ele27 'HLT_BIT_HLT_Ele27_WPTight_Gsf_v == 1'"

mtCutApplControlRegion="-A eleKin pfmt 'mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) < 60'"
#mtCutApplControlRegion="-A eleKin pfmt 'mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) > 40 && mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) < 60'"
mtCutApplSignalRegion="-A eleKin pfmt 'mt_2(met_pt,met_phi,${ptcorr},LepGood1_phi) > 30'"

##############################################################
##############################################################

# Here we have some options to be customized

##################################
##################################
# Some general options
##################################
useDataGH="y"
useHLTpt27="y" # being tested, already there for |eta|>2.1 to fix turn on effects
runBatch="y"
queueForBatch="cmscaf1nw"
nameTag="_trkmtTest_fitNorm" 
useSkimmedTrees="y" # skimmed samples are on both pccmsrm28 and eos 
usePtCorrForScaleFactors="n" # y: use corrected pt for scale factor weight; n: use LepGood_pt (which is what would have been used if the scale factors where in a friend tree)
# eta bin boundaries to divide regions in eta
etaBinBoundaries=("0.0" "1.479" "2.1" "2.5")
#etaBinBoundaries=("0.0" "2.5")
today=`date +"%d_%m_%Y"`
batchDirName="plots_${today}${nameTag}"  # name of directory to create inside jobsLog
##################################
##################################
# MCA files
##################################
mcafile="mca-80X_V3.txt"
mcafileFRcheck="mca-80X_V3_FRcheck.txt"  # automatically used instead of mcafile when doing part under doFakeRateCheckData
#mcafileFRskim="mca-80X_V3_FRskim.txt" # temporary patch: if using skimmed trees on lxplus the W sample has a different name
cutfile="qcd1l_SRtrees.txt" # we start from it and add or remove cuts
plotfile="test_plots.txt"
#
##################################
##################################
# Some MCA options
##################################
#excludeprocesses="data,Z_LO,W_LO,Z,Top,DiBosons"
excludeprocesses="Z_LO,W_LO" # decide whether to use NLO (amc@NLO) or LO (MadGraph) MC, non both! In case you can add other samples (Top, Dibosons) to speed up things
#selectplots=""  # if empty it uses all plots in cfg file
#selectplots="nJetClean,ptl1,etal1,pfmet,tkmet,ele1ID,awayJet_pt,wpt_tk,ele1dxy"  # if empty it uses all plots in cfg file
#selectplots="ptl1,etal1,pfmet,trkmt_trkmetEleCorr,pfmt,wpt_tk,nJetClean,ele1Iso04,ele1ID"  # if empty it uses all plots in cfg file
#selectplots="ptl1,etal1,pfmet,pfmt,trkmt_trkmetEleCorr,tkmet"
selectplots="trkmt_trkmetEleCorr_dxy_dy,trkmt_trkmetEleCorr,trkmt"
#selectplots="ptl1,etal1"
#maxentries="150000" # max int number is > 2*10^9
maxentries=""  # all events if ""
#
##################################
##################################
# to scale all mC to data use option --scaleBkgToData <arg> many tmes for every process 
# you also need not to have any process defined as signal
#scaleAllMCtoData="" # if "", nothing is added to mcPlots.py command
scaleAllMCtoData="--fitData" 
#scaleAllMCtoData=" --scaleBkgToData QCD --scaleBkgToData W --scaleBkgToData Z --scaleBkgToData Top --scaleBkgToData DiBosons " # does not seem to work as expected

#############################
# Now we declare some dictionary in bash
# Note that the key should not have spaces between square brakets and quotes, otherwise the spaces are interpreted as part of the key
# this is important if you loop on the keys like the following (whihc is the recommended way):
# for region in "${!regionKey[@]}"; do something with dictionary; done
# In this case the quotes around ${!regionKey[@]} should remove the spaces, i.e. the keys would not match anymore if you declared things as regionKey[  "key"]
#
# Also, it seems that without =() at the end of declaration we add some empty keys
###############################
declare -A regionKey=()
declare -A runRegion=()
declare -A regionName=()
declare -A skimTreeDir=()
declare -A outputDir=()
declare -A regionCuts=()
declare -A qcdFromFR=()   
#############################
# Note:
# ---------------------------
# regionName must be unique because it distinguishes the output folder, which is currently built using regionName and outputDir
# FIXME: change the logic of the output folder naming convention
#############################
#############################
# COMPUTATION REGION
#----------------------------
regionKey["FRcompRegion"]="FRcompRegion"
runRegion["FRcompRegion"]="n"
regionName["FRcompRegion"]="FR_computation_region"
skimTreeDir["FRcompRegion"]="TREES_1LEP_80X_V3_FRELSKIM_V5"
outputDir["FRcompRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}_highEtaEElowHLTpt"
regionCuts["FRcompRegion"]=" -A eleKin pfmet20 'met_pt < 20' "
qcdFromFR["FRcompRegion"]="n"
#
#############################
#############################
# COMPUTATION REGION (numerator)
#----------------------------
regionKey["FRcompNumRegion"]="FRcompNumRegion"
runRegion["FRcompNumRegion"]="n"
regionName["FRcompNumRegion"]="FR_computationNumerator_region"
skimTreeDir["FRcompNumRegion"]="TREES_1LEP_80X_V3_FRELSKIM_V5"
outputDir["FRcompNumRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}"
regionCuts["FRcompNumRegion"]=" -A eleKin pfmet20 'met_pt < 20' ${FRnumSel}"
qcdFromFR["FRcompNumRegion"]="n"
#
#############################
#############################
# FR validation REGION
#----------------------------
regionKey["FRcheckRegion"]="FRcheckRegion"
runRegion["FRcheckRegion"]="n"
regionName["FRcheckRegion"]="FR_check_region"
skimTreeDir["FRcheckRegion"]="TREES_1LEP_80X_V3_WENUSKIM_V5"
outputDir["FRcheckRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}"
regionCuts["FRcheckRegion"]=" -X nJet30 ${FRnumSel} ${mtCutApplControlRegion} -A eleKin pfmet20 'met_pt > 20' "
qcdFromFR["FRcheckRegion"]="y"
#
#############################
#############################
# APPLICATION REGION
#----------------------------
regionKey["FRapplRegion"]="FRapplRegion"
runRegion["FRapplRegion"]="n"
regionName["FRapplRegion"]="FR_application_region"
skimTreeDir["FRapplRegion"]="TREES_1LEP_80X_V3_WENUSKIM_V5"
outputDir["FRapplRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}"
regionCuts["FRapplRegion"]=" -X nJet30 ${Wsel} ${notFRnumSel} "
qcdFromFR["FRapplRegion"]="n"
#
#############################
#############################
# WMASS SIGNAL REGION
#----------------------------
regionKey["WmassSignalRegion"]="WmassSignalRegion"
runRegion["WmassSignalRegion"]="n"
regionName["WmassSignalRegion"]="wmass_signal_region"
skimTreeDir["WmassSignalRegion"]="TREES_1LEP_80X_V3_WENUSKIM_V5"
outputDir["WmassSignalRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}"
regionCuts["WmassSignalRegion"]=" -X nJet30 ${Wsel} ${FRnumSel} ${mtCutApplSignalRegion}"
qcdFromFR["WmassSignalRegion"]="y"
#
#############################
#############################
# WHELICITY SIGNAL REGION (avoid possibly all kinematic selections)
#----------------------------
regionKey["WhelicitySignalRegion"]="WhelicitySignalRegion"
runRegion["WhelicitySignalRegion"]="y"
regionName["WhelicitySignalRegion"]="whelicity_signal_region"
skimTreeDir["WhelicitySignalRegion"]="TREES_1LEP_80X_V3_WENUSKIM_V5"
outputDir["WhelicitySignalRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}_restrictPt_HLT27"
regionCuts["WhelicitySignalRegion"]=" -X nJet30 ${FRnumSel} ${Wsel}" # ${mtCutApplSignalRegion}"
qcdFromFR["WhelicitySignalRegion"]="y"
#
#############################
#############################
# SIGNAL REGION before FR numerator (avoid possibly all kinematic selections, so to see what we get with the trigger)
#----------------------------
regionKey["SignalRegionDenominator"]="SignalRegionDenominator"
runRegion["SignalRegionDenominator"]="n"
regionName["SignalRegionDenominator"]="signal_region_denominator"
skimTreeDir["SignalRegionDenominator"]="TREES_1LEP_80X_V3_WENUSKIM_V5"
outputDir["SignalRegionDenominator"]="full2016dataBH_puAndTrgSf_ptResScale_${today}"
regionCuts["SignalRegionDenominator"]=" -X nJet30"
qcdFromFR["SignalRegionDenominator"]="n"
#
#############################
#############################
# FR closure in computation REGION
#----------------------------
regionKey["FRclosureCompRegion"]="FRclosureCompRegion"
runRegion["FRclosureCompRegion"]="n"
regionName["FRclosureCompRegion"]="FR_computationClosure_region"
skimTreeDir["FRclosureCompRegion"]="TREES_1LEP_80X_V3_WENUSKIM_V5"
outputDir["FRclosureCompRegion"]="full2016dataBH_puAndTrgSf_ptResScale_${today}"
regionCuts["FRclosureCompRegion"]=" -A eleKin pfmet20 'met_pt < 20' ${FRnumSel}"
qcdFromFR["FRclosureCompRegion"]="y"
#
#############################



######################################################
######################################################
######################################################
# end of settings to be changed by user
#----------------------------------------
######################################################
######################################################
######################################################


host=`echo "$HOSTNAME"`
if [[ "${runBatch}" == "y" ]]; then
    if [[ ${host} != *"lxplus"* ]]; then
	echo "Error! You must be on lxplus to run on batch queues. Do ssh -XY lxplus and work from a release."
	return 0
    fi
fi

mypath="$PWD"

evalScram="eval \`scramv1 runtime -sh\`"
batchFolder="${mypath}/jobsLog/${batchDirName}"
mkdir -p ${batchFolder}/src
mkdir -p ${batchFolder}/log
baseBatchScript="${batchFolder}/baseBatchScript.sh"
batchFileName="${batchFolder}/src/PLOTREGION_ETABIN.sh"  # PLOTREGION and ETABIN will be changed to proper names later in the script depending on region
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

ptForScaleFactors="LepGood1_pt"
if [[ "${usePtCorrForScaleFactors}" == "y" ]]; then
    echo "Will use corrected pt instead of LepGood1_pt to compute the trigger/efficiency scale factors"
    ptForScaleFactors="${ptcorr}"
fi

treepath="" # set below depending on where we are
if [[ ${host} == *"pccmsrm28"* ]]; then
    treepath="/u2/emanuele/wmass/" # from pccmsrm28 
elif [[ ${host} == *"lxplus"* ]]; then
    treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco"
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


commonCommand="python ${plotterPath}/mcPlots.py -f -l ${luminosity} --s2v --tree treeProducerWMass --obj tree --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 ${plotterPath}/w-helicity-13TeV/wmass_e/${mcafile} ${plotterPath}/w-helicity-13TeV/wmass_e/${cutfile} ${plotterPath}/w-helicity-13TeV/wmass_e/${plotfile} ${dataOption} ${MCweigthOption} "

if [[ "X${scaleAllMCtoData}" != "X" ]]; then
    commonCommand="${commonCommand} ${scaleAllMCtoData} "
fi

if [[ "X${maxentries}" != "X" ]]; then
    commonCommand="${commonCommand} --max-entries ${maxentries} "
fi

if [[ "${runBatch}" != "y" ]]; then
    commonCommand="${commonCommand} -j 4 "
fi


if [[ "X${excludeprocesses}" != "X" ]]; then
    commonCommand="${commonCommand} --xp ${excludeprocesses}"
    # add ratio plot only if not excluding data
    if [[ "${excludeprocesses}" != *"data"* ]]; then
	commonCommand="${commonCommand} --showRatio --maxRatioRange 0.5 1.5 --fixRatioRange "
    fi
fi

if [[ "X${selectplots}" != "X" ]]; then
    commonCommand="${commonCommand} --sP ${selectplots}"
fi

if [[ "${useHLTpt27}" == "y" ]]; then
    commonCommand="${commonCommand} ${HLT27sel}"
fi

nEtaBoundaries="${#etaBinBoundaries[@]}"
let "nEtaBins_minus1=${nEtaBoundaries}-2"


# with ! we expand the keys, not the values of the dictionary
for region in "${!regionKey[@]}"; 
do

    if [[ "${runRegion[${region}]}" == "y" ]]; then

        # echo "key: ${region}"
	thisRegionKey="${regionKey[${region}]}"
        # runThisRegion="${runRegion[${region}]}"
	thisRegionName="${regionName[${region}]}"
        # cutThisRegion="${regionCuts[${region}]}"
        # skimtreeThisRegion="${skimTreeDir[$region]}"
        outputdirThisRegion="${outputDir[$region]}${nameTag}"
        # echo "runThisRegion: ${runThisRegion}"
        # echo "thisRegionName: ${thisRegionName}"
        # echo "cutThisRegion: ${cutThisRegion}"
        # echo "skimtreeThisRegion: ${skimtreeThisRegion}"
        # echo "outputdirThisRegion: ${outputdirThisRegion}"

	echo "#----------------------------------"
	echo "# Doing ${thisRegionKey}"
	echo "#----------------------------------"

	if [[ "${useSkimmedTrees}" == "y" ]]; then
	    treedir="${skimTreeDir[${region}]}" 
	else 
	    treedir="TREES_1LEP_80X_V3"
	fi

	#treeAndFriend=" -P ${treepath}/${treedir}/ -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root "
	treeAndFriend=" -P ${treepath}/${treedir}/ -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root "

	regionCommand="${commonCommand} ${treeAndFriend} ${regionCuts[${region}]}"

	if [[ "${qcdFromFR[${region}]}" == "y" ]]; then
        # we change the mca file in commonCommand with the new one specific for this study
	    regionCommand="${regionCommand/${mcafile}/${mcafileFRcheck}}"    
	# elif [[ "${skimTreeDir[${region}]}" == "TREES_1LEP_80X_V3_FRELSKIM_V5" ]]; then
        # # we change the mca file in commonCommand with the new one specific for this study
	#     regionCommand="${regionCommand/${mcafile}/${mcafileFRskim}}"    
	fi

        #commonFRcheck="${commonCommandFRcheck} ${treeAndFriend} -X nJet30 ${Wsel} ${FRnumSel} ${mtCutApplControlRegion} ${dataOptionFakes}"
	thisBatchFileName="${batchFileName/PLOTREGION/${thisRegionKey}}"

	for i in `seq 0 ${nEtaBins_minus1}`;
	do

	    echo ""
	    etalow="${etaBinBoundaries[$i]/./p}"
	    etahigh="${etaBinBoundaries[($i+1)]/./p}"
	    etabin="eta_${etalow}_${etahigh}"
	    srcBatchFileName="${thisBatchFileName/ETABIN/${etabin}}"
	    logPatternToChange="${batchFolder}/src/"
	    logPatternToPut="${batchFolder}/log/"
	    logBatchFileName="${srcBatchFileName/${logPatternToChange}/${logPatternToPut}}" # change folder from /src/ to /log/
	    logBatchFileName="${logBatchFileName/.sh/.log}"
            #echo "${etabin}"
	    #echo "${thisBatchFileName}"
	    cp ${baseBatchScript} ${srcBatchFileName}

	    etaRangeCut=" -A eleKin ${etabin} 'abs(LepGood1_eta) > ${etaBinBoundaries[$i]} && abs(LepGood1_eta) < ${etaBinBoundaries[($i+1)]}' "
	    regionCommand_eta="${regionCommand} --pdir ${plotterPath}/plots/distribution/${treedir}/${thisRegionName}/${outputdirThisRegion}/${etabin}/ ${etaRangeCut}" 
	    echo "${regionCommand_eta}" >> ${srcBatchFileName}
	    echo "" >> ${srcBatchFileName}
	    ######
	    # echo "corefiles=\`ls core.* 2&>1\`" >> ${srcBatchFileName}
	    # echo "for file in \${corefiles}" >> ${srcBatchFileName}
	    # echo "do" >> ${srcBatchFileName}
	    # echo "    rm ${mypath}/core.*" >> ${srcBatchFileName}
	    # echo "done" >> ${srcBatchFileName}
	    echo "rm ${mypath}/core.*" >> ${srcBatchFileName}

	    if [[ "${runBatch}" == "y" ]]; then
		commandBatch="bsub -q ${queueForBatch} -oo ${logBatchFileName}  \"source ${srcBatchFileName}\" "
		echo "${commandBatch}"
	    #echo "${commandBatch}" | bash
	    else
		echo "${regionCommand_eta}"
	    fi
	done

	echo ""
	echo ""
	echo ""

    fi

done

echo ""
echo ""