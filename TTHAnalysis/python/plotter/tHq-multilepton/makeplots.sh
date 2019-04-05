#!/bin/bash
USAGE="
makeplots.sh outdir plottag

Where plottag is one of:
 3l, 3l-zcontrol, 3l-ttcontrol,
 2lss-mm, 2lss-mm-ttcontrol,
 2lss-em, 2lss-em-ttcontrol,
 2lss-ee, 2lss-ee-ttcontrol,
 2los-em-ttcontrol

And the plots will be stored in outdir/
"
function DONE {
    echo -e "\e[92mDONE\e[0m"
    exit 0
}

if [[ "X$1" == "X" ]]; then echo "Please provide output directory name: [makeplots.sh outdir plottag]"; exit; fi
OUTDIR=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Please Provide plottag (e.g. 2lss-mm): [makeplots.sh outdir plottag]"; exit; fi
PLOTTAG=$1; shift;

# Note: tthtrees is a symlink to /afs/cern.ch/work/p/peruzzi/tthtrees/
#       thqtrees is a symlink to /eos/user/p/pdas/skimmedFriends/
#       fulltrees is a symlink to /eos/user/s/stiegerb/TTHTrees/13TeV/TREES_TTH_190418_Fall17/
#       fullfriendtrees is a symlink to /eos/user/p/pdas/fullFriends/

LUMI=41.5
BASEOPTIONS=" -f -j 8 -l ${LUMI} --s2v"\
" -L ttH-multilepton/functionsTTH.cc"\
" -L tHq-multilepton/functionsTHQ.cc"\
" --tree treeProducerSusyMultilepton"\
" --mcc ttH-multilepton/lepchoice-ttH-FO.txt"
TREEINPUTS="-P fulltrees/"
FRIENDTREES=" -F sf/t fullfriendtrees/1_thq_recleaner_FULL_041218/evVarFriend_{cname}.root"\
" -F sf/t fullfriendtrees/2_thq_eventvars_FULL_150319/evVarFriend_{cname}.root"\
" -F sf/t fulltrees/5_triggerDecision_230418_v1/evVarFriend_{cname}.root"\
" --FMC sf/t fulltrees/6_bTagSF_v2/evVarFriend_{cname}.root"\
" -F sf/t fulltrees/7_tauTightSel_v2/evVarFriend_{cname}.root"\
" --FMC sf/t fulltrees/8_vtxWeight2017_v1/evVarFriend_{cname}.root"
DRAWOPTIONS=" --split-factor=-1 --WA prescaleFromSkim  --maxRatioRange 0.0  1.99 --ratioYNDiv 505"\
" --showRatio --attachRatioPanel --fixRatioRange --showMCError"\
" --legendColumns 3 --legendWidth 0.42  --legendFontSize 0.042"\
" --noCms --topSpamSize 1.1 --lspam #scale[1.1]{#bf{CMS}}#scale[1.0]{#it{Preliminary}}"\
" --plotgroup data_fakes+='.*_promptsub' --neglist '.*_promptsub.*'"


# Pileup weight, btag SFs, trigger SFs, lepton Eff SFs:
#OPT2L="-W vtxWeight2017*eventBTagSF*"\
#"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)*"\
#"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*"\
#"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)"
#OPT3L="-W vtxWeight2017*eventBTagSF*"\
#"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)*"\
#"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*"\
#"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*"\
#"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)"
OPT2L="-W vtxWeight2017*eventBTagSF*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*"\
"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"
OPT3L="-W vtxWeight2017*eventBTagSF*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*"\
"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"

OPTIONS="--pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}"
MCA=""
CUTS=""
PLOTS=""
case "$PLOTTAG" in
    "3l" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L} --xp data"
        MCA="tHq-multilepton/mca-3l-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-3l.txt"
        PLOTS="tHq-multilepton/plots-thq-3l-kinMVA.txt"
        ;;
    "3l-zcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L}"
        MCA="tHq-multilepton/mca-3l-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-3l-Zcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-3l-zcontrol.txt"
        ;;
    "3l-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L}"
        MCA="tHq-multilepton/mca-3l-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-3l-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-3l-kinMVA.txt"
        ;;
    "2lss-mm" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E mm_chan --xp Flips --xp data"
        OPTIONS="${OPTIONS} --xP finalBins_log_em_40 --xP finalBins_log_ee_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-em" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E em_chan --xp data"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_40 --xP finalBins_log_ee_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-ee" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E ee_chan --xp data"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_40 --xP finalBins_log_em_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L}"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_40 --xP finalBins_log_em_40 --xP finalBins_log_ee_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-mm-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E mm_chan --xp Flips"
        OPTIONS="${OPTIONS} --xP finalBins_log_em_40 --xP finalBins_log_ee_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-em-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E em_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_40 --xP finalBins_log_ee_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-ee-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E ee_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_40 --xP finalBins_log_em_40"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2los-em-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L}"
        OPTIONS="${OPTIONS} --scaleBkgToData TT --scaleBkgToData DY --scaleBkgToData WJets --scaleBkgToData SingleTop --scaleBkgToData WW"
	OPTIONS="${OPTIONS} -E fwdjetpt40 --sP maxEtaJet25_40"
        MCA="tHq-multilepton/mca-2los-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-ttbar-fwdjet.txt"
        PLOTS="tHq-multilepton/plots-thq-ttbar-fwdjet.txt"
        ;;
    *)
        echo "${USAGE}"
        echo -e "\e[31mUnknown plottag\e[0m"
        exit 1
esac

echo "Storing output in ${OUTDIR}/";
echo "Normalizing to ${LUMI}/fb";

ARGUMENTS="${MCA} ${CUTS} ${PLOTS}"
OPTIONS="${TREEINPUTS} ${FRIENDTREES} ${BASEOPTIONS} ${OPTIONS}"

echo "mca  : ${MCA}"
echo "cuts : ${CUTS}"
echo "plots: ${PLOTS}"
echo python mcPlots.py ${ARGUMENTS} ${OPTIONS}

python mcPlots.py ${ARGUMENTS} ${OPTIONS}

#if [[ "X$1" != "X" ]]; then
#    SELECTPLOT=$1; shift;
#    echo "Running a single plot: ${SELECTPLOT}";
#    python mcPlots.py ${ARGUMENTS} ${OPTIONS} --select-plot ${SELECTPLOT}
#else
#    # python mcPlots.py ${ARGUMENTS} ${OPTIONS} --enable-cut 2bl --select-plot dEtaFwdJet2BJet_40
#    python mcPlots.py ${ARGUMENTS} ${OPTIONS} --exclude-plot dEtaFwdJet2BJet_40
#fi

DONE