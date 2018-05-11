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
splitHelicity="n"
outDir="plots/gen_eff_etaPt"
plotterDir="/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter"
treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
#treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5" 
#mca_W_NLO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_lessFiles_genCutOnly.txt"    # less statistics
mca_W_NLO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_genCutOnly.txt"       # all statistics
mca_W_LO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_LO_genCutOnly.txt"
if [[ "${splitHelicity}" != "y" ]]; then
    mca_W_NLO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_genCutOnly_noHel.txt"     # not splitted in helicity, only in charge
    mca_W_LO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_LO_genCutOnly_noHel.txt"   # not splitted in helicity, only in charge
fi

cutfile="w-helicity-13TeV/wmass_e/wenu_80X.txt"
plotfile="w-helicity-13TeV/wmass_e/wenu_plots.txt"
#plotvar="abswy"
plotvar="etaPtGen"
#plotvar="wy"
noChargeFlip=" -A tightCharge noChargeFlip 'LepGood1_mcMatchId*LepGood1_charge!=-24' "

doAlsoSmear="y"
smearFolderTag="_SmearPFMET"
replaceCutAddSmear=" -R mt pfmtSmearMET 'mt_2(getSmearedVar(met_pt,0.2,evt,isData,0),met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood1_phi) > 40' "

cd ${plotterDir}
eval `scramv1 runtime -sh`

charges=("plus" "minus")

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

	processes=""
	if [[ "${splitHelicity}" == "y" ]]; then
	    processes=" -p W${charge}_long,W${charge}_left,W${charge}_right "
	else
	    processes=" -p W${charge} "
	fi
	
        ### gen selection no cuts
	command="python mcPlots.py --pdir ${outDir}/${outfolder} -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P ${treepath} -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mcafile} ${cutfile} ${processes} --plotmode=nostack  --sP w${charge}_${plotvar} ${plotfile}   -U 'alwaystrue' --noCms  "

	echo "${command}"
	if [[ "${justPrint}" != "y" ]]; then
	    echo "${command}" | bash
	fi

	echo ""

        ### reco selection all cuts       
	outfolder="${outfolder/wgen_nosel/wgen_fullsel}"

	command="python mcPlots.py --pdir ${outDir}/${outfolder} -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P ${treepath} -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 ${mcafile} ${cutfile}  ${processes} --plotmode=nostack  --sP w${charge}_${plotvar}  ${plotfile}   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' ${noChargeFlip} --noCms  "   

	echo "${command}"
	if [[ "${justPrint}" != "y" ]]; then
	    echo "${command}" | bash
	fi

	echo ""

	if [[ "${order}" == "NLO" ]] && [[ "${doAlsoSmear}" == "y" ]]; then

            ### reco selection all cuts, but smear something (in case removing something else)
	    outfolderWithSmear="${outfolder}${smearFolderTag}"
	    newcommand="${command/${outfolder}/${outfolderWithSmear}}"
	    newcommand="${newcommand} ${replaceCutAddSmear}"
	    echo "${newcommand}"
	    if [[ "${justPrint}" != "y" ]]; then
		echo "${newcommand}" | bash
	    fi
	    echo ""	    		

	fi

	echo ""

    done

done


