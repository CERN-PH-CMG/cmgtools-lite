#! /bin/bash

# lumi = 35.5/fb if using run2016 B to H, otherwise it is 19.3
# check in mca file which MC is being used for Z, amc@NLO, madgraph or powheg
# selection and mca of fake rate to see how plots look like

echo ""
doCompRegion="y" # y or n (or any key but y for no)
doApplRegion="y"
doClosureTest="n"
useDataGH="y"

# SR trees
treepath="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco"
treedir="TREES_1LEP_80X_V3"
mcafile="mca-80X_V3.txt"
cutfile="qcd1l_SRtrees.txt"
plotfile="test_plots.txt"
#excludeprocesses="Z_LO,W_LO,Z,Top,DiBosons"
excludeprocesses="Z_LO,W_LO" # decide whether to use NLO (amc@NLO) or LO (MadGraph) MC, non both! 
maxentries="2000000000" # max int number is > 2*10^9
#maxentries="100"
outdirComp="full2016dataBH_puAndTrgSf"
outdirAppl="full2016dataBH_puAndTrgSf_looseWPiso0p2"

luminosity=""
dataOption=""
MCweightOption=""
if [[ "${useDataGH}" == "y" ]]; then
    dataOption=" --pg 'data := data_B,data_C,data_D,data_E,data_F,data_G,data_H' "
    luminosity="35.5"
    MCweigthOption=" -W 'puw2016_nTrueInt_36fb(nTrueInt)*LepGood1_trgSF' "
else 
    dataOption=" --pg 'data := data_B,data_C,data_D,data_E,data_F' --xp data_G,data_H "
    luminosity="19.3"
    MCweigthOption=" -W 'puw2016_nTrueInt_BF(nTrueInt)*LepGood1_trgSF' "
fi

##############################
## WARNING ##
# to use a python command with options froma bash script, do
# command="python [args] [options]"
# echo "${command}" | bash
# otherwise the parsing of the option parameters is not done correctly

commonCommand="python mcPlots.py -P ${treepath}/${treedir}/ -f -j 4 -l ${luminosity} --s2v --tree treeProducerWMass --obj tree -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root --lspam '#bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0.75 1.25 --fixRatioRange wmass/wmass_e/${mcafile} wmass/wmass_e/${cutfile} wmass/wmass_e/${plotfile} --max-entries ${maxentries} ${dataOption} ${MCweigthOption} "

if [[ "X${excludeprocesses}" != "X" ]]; then
    commonCommand="${commonCommand} --xp ${excludeprocesses}"
fi

#jetCleanSel=" -R nJet30 nJet30 'nJet_Clean > 0 && Jet_Clean1_pt > 30 && abs(deltaR(LepGood1_eta,LepGood1_phi, Jet_Clean1_eta,Jet_Clean1_phi))> 0.7' "
jetCleanSel="" # if empty, use the away jet
inEB=" -A eleKin EB 'abs(LepGood1_eta) < 1.479' "
inEE=" -A eleKin EE 'abs(LepGood1_eta) > 1.479' "

# computation region
if [[ "${doCompRegion}" == "y" ]]; then
    echo "${commonCommand} --pdir plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/EB/ ${inEB} ${jetCleanSel}" | bash
    echo "${commonCommand} --pdir plots/test/${treedir}/fakeRateSel/computation_region/${outdirComp}/EE/ ${inEE} ${jetCleanSel}" | bash
fi

# application region

not_pass_tightWP="-A eleKin not-fullTightID 'LepGood1_tightId < 3 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.0588 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.0571 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_mediumWP="-A eleKin not-fullMediumID 'LepGood1_tightId < 2 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.0695 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.0821 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_looseWP="-A eleKin not-fullLooseID 'LepGood1_tightId < 1 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.0994 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.107 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

not_pass_looseWP_iso0p2="-A eleKin not-fullLooseID 'LepGood1_tightId < 1 || if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.1 || abs(LepGood1_dxy) > 0.05, LepGood1_relIso04EA > 0.2 || abs(LepGood1_dz) > 0.2 || abs(LepGood1_dxy) > 0.1) || LepGood1_lostHits > 1 || LepGood1_convVeto == 0'"

Wsel="-A eleKin WregionSel 'LepGood1_pt>30 && met_pt>20 && pt_2(LepGood1_pt, LepGood1_phi, met_trkPt, met_trkPhi ) < 40 && mt_2(met_trkPt,met_trkPhi,LepGood1_pt,LepGood1_phi) < 110'"

#commonApplReg="${commonCommand} -X nJet30 ${not_pass_mediumWP} ${Wsel}" 
commonApplReg="${commonCommand} -X nJet30 ${not_pass_looseWP_iso0p2} ${Wsel}" 

if [[ "${doApplRegion}" == "y" ]]; then
    echo "${commonApplReg} --pdir plots/test/${treedir}/fakeRateSel/application_region/${outdirAppl}/EB/ ${inEB}" | bash
    echo "${commonApplReg} --pdir plots/test/${treedir}/fakeRateSel/application_region/${outdirAppl}/EE/ ${inEE}" | bash
fi

echo ""
echo ""
echo ""

# QCD closure test
mca_clos="mca-80X-qcdClosureTest.txt"
sel_clos="wenu_80X.txt"
plot_clos="qcdClosureTest_plots.txt"
plotmode_clos="stack" # norm, nostack, stack (but with just MC we can define a signal and remove it from the stack with --noStackSig)
#subdir_clos="puBH_TrgSfBH"
subdir_clos="testagain"
maxentries_clos="2000000000"
#maxentries_clos="1000"

cmdClosure="python mcPlots.py -P ${treepath}/${treedir}/ -f -j 4 -l ${luminosity} --s2v --tree treeProducerWMass --obj tree -F Friends ${treepath}/${treedir}/friends/tree_Friend_{cname}.root -F Friends ${treepath}/${treedir}/friends/tree_FRFriend_{cname}.root --FMC Friends ${treepath}/${treedir}/friends/tree_TrgFriend_{cname}.root --lspam '     #bf{CMS} #it{Preliminary}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --maxRatioRange 0.0 2.0 --fixRatioRange wmass/wmass_e/${mca_clos} wmass/wmass_e/${sel_clos} wmass/wmass_e/${plot_clos} --plotmode ${plotmode_clos} --max-entries ${maxentries_clos} --sp QCD --ratioDen QCD --ratioNums QCD_mcfakes,background --ratioYLabel 'fake/MC' --noStackSig --showIndivSigs ${MCweigthOption} "

# --sp QCD --noStackSig --showSigShape --ratioNums background

qcdclosTest_cut=" -R id looseWP_iso0p2 'LepGood1_tightId >= 1 && if3(abs(LepGood1_etaSc)<1.479,LepGood1_relIso04EA < 0.2 && abs(LepGood1_dz) < 0.1 && abs(LepGood1_dxy) < 0.05, LepGood1_relIso04EA < 0.2 && abs(LepGood1_dz) < 0.2 && abs(LepGood1_dxy) < 0.1) && LepGood1_lostHits <= 1 && LepGood1_convVeto == 1' -R w_tkmt w_tkmt 'mt_2(met_trkPt,met_trkPhi,LepGood1_pt,LepGood1_phi) < 110' "

if [[ "${doClosureTest}" == "y" ]]; then
    echo "${cmdClosure} ${qcdclosTest_cut} --pdir plots/test/${treedir}/fakeRateSel/closureTest/${subdir_clos}/EB ${inEB}" | bash
    echo "${cmdClosure} ${qcdclosTest_cut} --pdir plots/test/${treedir}/fakeRateSel/closureTest/${subdir_clos}/EE ${inEE}" | bash
fi
