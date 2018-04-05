# Can run as:
#
# bsub -q cmscaf1nw -oo /afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/runEfficiencyElectron.log  "source /afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter/runEfficiencyElectron.sh"                                                                
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

justPrint="n"   # if "y", it just prints commands (useful before submitting the job)
doAlsoLO="y"    # decide to run also on LO samples, by default only NLO is done
outDir="plots/gen_eff_tightCharge"
plotterDir="/afs/cern.ch/work/m/mciprian/w_mass_analysis/heppy/CMSSW_8_0_25/src/CMGTools/WMass/python/plotter"
treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
mca_W_NLO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_lessFiles.txt"
mca_W_LO="w-helicity-13TeV/wmass_e/mca-includes/mca-80X-wenu-sig_LO.txt"
cutfile="w-helicity-13TeV/wmass_e/wenu_80X.txt"
plotfile="w-helicity-13TeV/wmass_e/wenu_plots.txt"

cd ${plotterDir}
eval `scramv1 runtime -sh`

charges=("plus" "minus")

cutname="pfmt"
additionalCut=" -A numSel ${cutname} 'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood1_phi) > XXX' "  # XXX will be replaced by value in additionalCutValues
additionalCutValues=("30" "40" "50") # keep empty if not needed to run with different cuts
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

	command="python mcPlots.py --pdir ${outDir}/${outfolder} -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P ${treepath} -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 ${mcafile} ${cutfile}  -p W${charge}_long,W${charge}_left,W${charge}_right --plotmode=nostack  --sP w${charge}_wy  ${plotfile}   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' "   
	echo "${command}"
	if [[ "${justPrint}" != "y" ]]; then
	    echo "${command}" | bash
	fi

	echo ""

	for additionalCutValue in "${additionalCutValues[@]}"
	do
	    addcut="${additionalCut/XXX/${additionalCutValue}}"
	    outfolderWithCut="${outfolder/wgen_fullsel/wgen_fullsel_${cutname}${additionalCutValue}}"
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



## gen 

#no sel

# command="python mcPlots.py --pdir plots/${outDir}/wgen_nosel_minus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_NLO} w-helicity-13TeV/wmass_e/wenu_80X.txt -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -U 'alwaystrue'"

# echo "${command}" | bash    

# command="python mcPlots.py --pdir plots/${outDir}/wgen_nosel_plus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 ${mca_W_NLO} w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -U 'alwaystrue'"   

# echo "${command}" | bash



# # python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_minus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)'    

# # python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_plus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)'    



# ## gen (LO)

# #no sel

# command="python mcPlots.py --pdir plots/${outDir}/wgen_nosel_minus_LO -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_LO} w-helicity-13TeV/wmass_e/wenu_80X.txt -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -U 'alwaystrue'"

# echo "${command}" | bash    

# command="python mcPlots.py --pdir plots/${outDir}/wgen_nosel_plus_LO -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_LO} w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -U 'alwaystrue'"    

# echo "${command}" | bash


# ## reco (LO)

# # no pfmt

# #command="python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_minus_LO -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)'"    

# #echo "${command}" | bash

# #command="python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_plus_LO -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)'"    

# #echo "${command}" | bash

# #reco (LO)

# # pfmt > 40

# command="python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt40_minus_LO -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_LO} w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_40  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 40'"    


# echo "${command}" | bash

# command="python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt40_plus_LO -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_LO} w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_40  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 40'"    


# echo "${command}" | bash


# ## reco

# # no pfmt


# # # pfmt > 30
# # python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt30_minus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_30  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 30'   

# # python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt30_plus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_30  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 30'

# # # pfmt > 40
# command="python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt40_minus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_NLO} w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_40  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 40'"   

# echo "${command}" | bash

# command="python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt40_plus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  ${mca_W_NLO} w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_40  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 40'"

# echo "${command}" | bash

# # # pfmt > 50
# # python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt50_minus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wminus_long,Wminus_left,Wminus_right --plotmode=nostack  --sP wminus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_50  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 50'   

# # python mcPlots.py --pdir plots/${outDir}/wgen_fullsel_pfmt50_plus -F Friends '{P}/friends/tree_Friend_{cname}.root'  -P /eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY -f -j 8 -l 35.9 --s2v  --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035  w-helicity-13TeV/wmass_e/mca-80X-wenu-helicity.txt w-helicity-13TeV/wmass_e/wenu_80X.txt  -p Wplus_long,Wplus_left,Wplus_right --plotmode=nostack  --sP wplus_wy  w-helicity-13TeV/wmass_e/wenu_plots.txt   -W 'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)' -A numSel pfmt_50  'mt_2(met_pt,met_phi,ptElFull(LepGood1_calPt,LepGood1_eta),LepGood_phi) > 50'
