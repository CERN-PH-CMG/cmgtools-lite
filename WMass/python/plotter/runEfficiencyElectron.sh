#!/bin/bash

# Can run as:
#
# bsub -q cmscaf1nw -oo /afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/runEfficiencyElectron.log  "source /afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/runEfficiencyElectron.sh"                                                                
#
# Or better, pipe the output into another file .sh (set justPrint=y), edit it my hands according to you needs and then run a job on that
#
# Remember to set options below

#############################
#
#      WARNING
#
# At the moment there is no simple way to select LO or NLO W samples from w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt (except commenting out the unnecessary ones)
# Therefore, until this is implemented, remember to submit either LO or NLO after editing w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt
#
# In alternative, since only W is used here, you can directly read w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_LO.txt for LO,
# and w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_lessFiles.txt for NLO (this has a limited number of samples, it is useless to run on all for NLO)
# This second possibility is currently used in this script
#
###############################

justPrint="y"   # if "y", it just prints commands (useful before submitting the job)
doAlsoLO="y"    # decide to run also on LO samples, by default only NLO is done
doAlsoSmear="y"    # decide to run smearing some quantity on which we cut, like pfmt
outDir="plots/gen_eff_tightCharge_chargeMatch"
plotterDir="/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter"
treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
#treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5" 
#mca_W_NLO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_genCutOnly.txt"          # less statistics
mca_W_NLO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_lessFiles_genCutOnly.txt" # all statistics
mca_W_LO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_LO_genCutOnly.txt"
cutfile="w-helicity-13TeV/wmass_e/wenu_80X.txt"
plotfile="w-helicity-13TeV/wmass_e/wenu_plots.txt"
noChargeFlip=" -A tightCharge noChargeFlip 'LepGood1_mcMatchId*LepGood1_charge!=-24' "

cd ${plotterDir}
eval `scramv1 runtime -sh`

charges=("plus" "minus")

#cutname="pfmt"
cutname="pfmtSmearMET"
#cutFolderNameSuffix="_smearMt"
cutFolderNameSuffix=""
#additionalCut=" -A numSel ${cutname} 'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood1_phi) > XXX' "  # XXX will be replaced by value in additionalCutValues
additionalCut=" -A numSel ${cutname} 'mt_2(getSmearedVar(met_pt,0.2,evt,isData,0),met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood1_phi) > XXX' "
#additionalCutValues=("30" "40" "50") # keep empty if not needed to run with different cuts
additionalCutValues=("40") # keep empty if not needed to run with different cuts
#additionalCutValues=()

# check if it works
#
# for additionalCutValue in "${additionalCutValues[@]}"
# do
#     addcut="${additionalCut/XXX/${additionalCutValue}}"
#     echo "${addcut}"
# done
#
# return

orders=("NLO")
if [[ "${doAlsoLO}" == "y" ]]; then
    orders=("NLO" "LO")
fi


for order in "${orders[@]}"
do

    for charge in "${charges[@]}"
    do

	echo ""
	echo "###############################"
	echo "# Charge: ${charge}"
	echo "# Sample: ${order}"
	echo "###############################"
	echo ""

	mcafile="${mca_W_NLO}"
	outfolder="wgen_nosel_${charge}"
	if [[ "${order}" == "LO" ]]; then
	    mcafile="${mca_W_LO}"
	    outfolder="${outfolder}_LO"
	fi
	
        ### gen selection no cuts
	command="python mcPlots.py --pdir ${outDir}/${outfolder} -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P ${treepath} -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mcafile} ${cutfile} -p W${charge}_long,W${charge}_left,W${charge}_right --plotmode=nostack  --sP w${charge}_wy ${plotfile}   -U 'alwaystrue'"
	echo "${command}"
	if [[ "${justPrint}" != "y" ]]; then
	    echo "${command}" | bash
	fi

	echo ""

        ### gen selection all cuts       
	outfolder="${outfolder/wgen_nosel/wgen_fullsel}"

	command="python mcPlots.py --pdir ${outDir}/${outfolder} -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P ${treepath} -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 ${mcafile} ${cutfile}  -p W${charge}_long,W${charge}_left,W${charge}_right --plotmode=nostack  --sP w${charge}_wy  ${plotfile}   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' ${noChargeFlip}"   
	echo "${command}"
	if [[ "${justPrint}" != "y" ]]; then
	    echo "${command}" | bash
	fi

	echo ""

	for additionalCutValue in "${additionalCutValues[@]}"
	do
	    addcut="${additionalCut/XXX/${additionalCutValue}}"
	    outfolderWithCut="${outfolder/wgen_fullsel/wgen_fullsel_${cutname}${additionalCutValue}${cutFolderNameSuffix}}"
	    newcommand="${command/${outfolder}/${outfolderWithCut}}"
	    newcommand="${newcommand} ${addcut}"
	    echo "${newcommand}"
	    if [[ "${justPrint}" != "y" ]]; then
		echo "${newcommand}" | bash
	    fi
	    echo ""
	done

	echo ""

    done

done


