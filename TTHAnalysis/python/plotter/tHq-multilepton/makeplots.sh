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
#       skimtrees is a symlink to /afs/cern.ch/work/p/pdas/tth/TTHTrees/2017/skimTrees/

LUMI=41.5
BASEOPTIONS=" -f -j 8 -l ${LUMI} --s2v"\
" -L ttH-multilepton/functionsTTH.cc"\
" -L tHq-multilepton/functionsTHQ.cc"\
" --tree treeProducerSusyMultilepton"\
" --mcc ttH-multilepton/lepchoice-ttH-FO.txt"
TREEINPUTS="-P skimtrees/"
FRIENDTREES=" -F sf/t skimtrees/1_recleaner_290319/evVarFriend_{cname}.root"\
" -F sf/t skimtrees/2_thq_eventvars_290319/evVarFriend_{cname}.root"\
" -F sf/t skimtrees/5_triggerDecision/evVarFriend_{cname}.root"\
" --FMC sf/t skimtrees/6_bTagSF/evVarFriend_{cname}.root"\
" -F sf/t skimtrees/7_tauTightSel/evVarFriend_{cname}.root"\
" --FMC sf/t skimtrees/8_vtxWeight2017/evVarFriend_{cname}.root"
DRAWOPTIONS=" --split-factor=-1 --WA prescaleFromSkim  --maxRatioRange 0.0  1.99 --ratioYNDiv 505"\
" --showRatio --attachRatioPanel --fixRatioRange --showMCError"\
" --unc tHq-multilepton/signal_extraction/systsUnc.txt"\
" --legendColumns 3 --legendWidth 0.6  --legendFontSize 0.042"\
" --noCms --topSpamSize 1.1 --lspam #scale[1.1]{#bf{CMS}}#scale[1.0]{#it{Preliminary}}"\
" --plotgroup data_fakes+=.*_promptsub --neglist .*_promptsub.*"

# Pileup weight, btag SFs, trigger SFs, lepton Eff SFs, L1 prefiring SFs:
OPT2L="-W vtxWeight2017*eventBTagSF*NonPrefiringProb*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)*"\
"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"
OPT3L="-W vtxWeight2017*eventBTagSF*NonPrefiringProb*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)*"\
"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)"

OPTIONS="--pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}"
MCA=""
CUTS=""
PLOTS=""
case "$PLOTTAG" in
    "syst_test" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L}"
        MCA="tHq-multilepton/test/mca-syst-test.txt"
        CUTS="tHq-multilepton/cuts-thq-3l.txt"
        PLOTS="tHq-multilepton/test/plots-syst-test.txt --plotmode nostack"
        ;;
    "3l" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L}"
        #MCA="tHq-multilepton/mca-3l-mcdata.txt --xp data"
        MCA="tHq-multilepton/mca-3l-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-3l.txt"
        PLOTS="tHq-multilepton/plots-thq-3l-kinMVA.txt"
        ;;
    "3l-zcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L}"
        #MCA="tHq-multilepton/mca-3l-mcdata.txt"
	MCA="tHq-multilepton/mca-3l-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-3l-Zcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-3l-zcontrol.txt"
        ;;
    "3l-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT3L}"
        #MCA="tHq-multilepton/mca-3l-mcdata.txt"
	MCA="tHq-multilepton/mca-3l-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-3l-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-3l-kinMVA.txt"
        ;;
    "3l-frclosure" )
	DRAWOPTIONS="${DRAWOPTIONS} --ratioDen TT_FR_QCD --errors --AP --rebin 2 --ratioNums TT_fake"
	SELECTPLOT="--sP thqMVA_tt_3l_60 --sP thqMVA_ttv_3l_60"
	#SELECTPROCESS="-p incl_TT_FR_QCD -p incl_TT_FR_TT -p incl_TT_fake"
	OPTIONS="${TREEINPUTS} ${FRIENDTREES} ${BASEOPTIONS} ${DRAWOPTIONS} ${OPT3L} ${SELECTPROCESS} ${SELECTPLOT}"
	MCA="tHq-multilepton/mca-3l-mc-closuretest.txt"
	CUTS="tHq-multilepton/cuts-thq-3l.txt"
	PLOTS="tHq-multilepton/plots-thq-3l-kinMVA.txt"
	ARGOPTS="${MCA} ${CUTS} ${PLOTS} ${OPTIONS}"
	
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/3l_mufake_norm/  -E mufake --plotmode nostack --fitRatio 0
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/3l_mufake_shape/ -E mufake --plotmode norm --fitRatio 1
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/3l_elfake_norm/  -E elfake --plotmode nostack --fitRatio 0
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/3l_elfake_shape/ -E elfake --plotmode norm --fitRatio 1
	DONE
        ;;
    "2lss-mm" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E mm_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_em_60 --xP finalBins_log_ee_60"
        #MCA="tHq-multilepton/mca-2lss-mcdata.txt --xp Flips --xp data"
	MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt --xp Flips"
        CUTS="tHq-multilepton/cuts-thq-2lss.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-em" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E em_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_60 --xP finalBins_log_ee_60"
        #MCA="tHq-multilepton/mca-2lss-mcdata.txt --xp data"
	MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-ee" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E ee_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_60 --xP finalBins_log_em_60"
        MCA="tHq-multilepton/mca-2lss-mcdata.txt"
	#MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L}"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_60 --xP finalBins_log_em_60 --xP finalBins_log_ee_60"
        #MCA="tHq-multilepton/mca-2lss-mcdata.txt"
	MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-mm-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E mm_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_em_60 --xP finalBins_log_ee_60"
        #MCA="tHq-multilepton/mca-2lss-mcdata.txt --xp Flips"
	MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt --xp Flips"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-em-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E em_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_60 --xP finalBins_log_ee_60"
        #MCA="tHq-multilepton/mca-2lss-mcdata.txt"
	MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2lss-ee-ttcontrol" )
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L} -E ee_chan"
        OPTIONS="${OPTIONS} --xP finalBins_log_mm_60 --xP finalBins_log_em_60"
        #MCA="tHq-multilepton/mca-2lss-mcdata.txt"
	MCA="tHq-multilepton/mca-2lss-mcdata-frdata.txt"
        CUTS="tHq-multilepton/cuts-thq-2lss-ttbarcontrol.txt"
        PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
        ;;
    "2los-em-ttcontrol" )
	TREEINPUTS="-P fulltrees/"
	FRIENDTREES=" -F sf/t fullfriendtrees/1_thq_recleaner_FULL_050419/evVarFriend_{cname}.root"
	FRIENDTREES="${FRIENDTREES} -F sf/t fullfriendtrees/2_thq_eventvars_FULL_050419/evVarFriend_{cname}.root"
	FRIENDTREES="${FRIENDTREES} -F sf/t fullfriendtrees/5_triggerDecision_FULL_050419/evVarFriend_{cname}.root"
	FRIENDTREES="${FRIENDTREES} --FMC sf/t fullfriendtrees/6_bTagSF_FULL_050419/evVarFriend_{cname}.root"
	FRIENDTREES="${FRIENDTREES} -F sf/t fullfriendtrees/7_tauTightSel_FULL_050419/evVarFriend_{cname}.root"
	FRIENDTREES="${FRIENDTREES} --FMC sf/t 8_vtxWeight2017_FULL_050419/evVarFriend_{cname}.root"
        OPTIONS="${OPTIONS} ${DRAWOPTIONS} ${OPT2L}"
        OPTIONS="${OPTIONS} --scaleBkgToData TT --scaleBkgToData DY --scaleBkgToData WJets --scaleBkgToData SingleTop --scaleBkgToData WW"
        MCA="tHq-multilepton/mca-2los-mcdata.txt"
        CUTS="tHq-multilepton/cuts-thq-ttbar-fwdjet.txt -E modified3"
        PLOTS="tHq-multilepton/plots-thq-ttbar-fwdjet.txt --sP maxEtaJet25_60"
        ;;
    "2lss-frclosure" )
	DRAWOPTIONS="${DRAWOPTIONS} --ratioDen TT_FR_QCD --errors --AP --rebin 2 --ratioNums TT_fake"
	SELECTPLOT="--sP thqMVA_tt_2lss_60 --sP thqMVA_ttv_2lss_60"
	SELECTPROCESS="-p incl_FR_QCD_elonly -p incl_FR_QCD_muonly -p TT_FR_QCD -p TT_FR_TT -p TT_fake"
	OPTIONS="${TREEINPUTS} ${FRIENDTREES} ${BASEOPTIONS} ${DRAWOPTIONS} ${OPT3L} ${SELECTPROCESS} ${SELECTPLOT}"
	MCA="tHq-multilepton/mca-2lss-mc-closuretest.txt"
	CUTS="tHq-multilepton/cuts-thq-2lss.txt"
	PLOTS="tHq-multilepton/plots-thq-2lss-kinMVA.txt"
	ARGOPTS="${MCA} ${CUTS} ${PLOTS} ${OPTIONS}"
	
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_mm_norm/  -E mm_chan --plotmode nostack --fitRatio 0
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_mm_shape/ -E mm_chan --plotmode norm --fitRatio 1
	#python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_ee_norm/  -E ee_chan --plotmode nostack --fitRatio 0
	#python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_ee_shape/ -E ee_chan --plotmode norm --fitRatio 1
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_em_mufake_norm/  -E em_chan -E mufake --plotmode nostack --fitRatio 0
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_em_mufake_shape/ -E em_chan -E mufake --plotmode norm --fitRatio 1
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_em_elfake_norm/  -E em_chan -E elfake --plotmode nostack --fitRatio 0
	python mcPlots.py ${ARGOPTS} --pdir /afs/cern.ch/work/p/pdas/www/THQ2017/${OUTDIR}/2lss_em_elfake_shape/ -E em_chan -E elfake --plotmode norm --fitRatio 1
	DONE
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
