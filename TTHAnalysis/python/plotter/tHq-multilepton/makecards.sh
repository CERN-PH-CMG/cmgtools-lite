#!/bin/bash
USAGE="
makecards.sh outdir channel filename

Where channel is one of:
 3l, 2lss_mm, 2lss_em, 2lss_ee

And the cards will be stored in outdir/channel
"

function DONE {
    echo -e "\e[92mDONE\e[0m"
    exit 0
}

if [[ "X$1" == "X" ]]; then echo "Please provide output directory name: [makecards.sh outdir channel]"; exit; fi
OUTNAME=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Please provide channel (e.g. 2lss-mm): [makecards.sh outdir channel]"; exit; fi
CHANNEL=$1; shift;
if [[ "X$1" == "X" ]]; then echo "Please provide filename: [makecards.sh outdir channel filename]"; exit; fi
FILENAME=$1; shift;

LUMI=41.5
# Note: tthtrees is a symlink to /afs/cern.ch/work/p/peruzzi/tthtrees/
#       thqtrees is a symlink to /afs/cern.ch/work/p/pdas/tth/TTHTrees/2017/


TREEINPUTS="-P tthtrees/TREES_TTH_190418_Fall17_skim2lss3l/"
FRIENDTREES=" -F sf/t thqtrees/1_thq_recleaner_071118/evVarFriend_{cname}.root"\
" -F sf/t thqtrees/2_thq_eventvars_071118/evVarFriend_{cname}.root"\
" -F sf/t tthtrees/TREES_TTH_190418_Fall17_skim2lss3l/5_triggerDecision_230418_v1/evVarFriend_{cname}.root"\
" --FMC sf/t tthtrees/TREES_TTH_190418_Fall17_skim2lss3l/6_bTagSF_v2/evVarFriend_{cname}.root"\
" -F sf/t tthtrees/TREES_TTH_190418_Fall17_skim2lss3l/7_tauTightSel_v2/evVarFriend_{cname}.root"\
" --FMC sf/t tthtrees/TREES_TTH_190418_Fall17_skim2lss3l/8_vtxWeight2017_v1/evVarFriend_{cname}.root"\

BASEOPTIONS="-f -j 8 -l ${LUMI} --s2v -v 2"\
" -L ttH-multilepton/functionsTTH.cc"\
" -L tHq-multilepton/functionsTHQ.cc"\
" --tree treeProducerSusyMultilepton"\
" --mcc ttH-multilepton/lepchoice-ttH-FO.txt"\
" --neg"\
" --xp data --asimov"

# Pileup weight, btag SFs, trigger SFs, lepton Eff SFs:
OPT2L="-W vtxWeight2017*eventBTagSF*"\
"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],2)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],2)"
OPT3L="-W vtxWeight2017*eventBTagSF*"\
"triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],nLepTight_Recl,0)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[0]],LepGood_pt[iLepFO_Recl[0]],LepGood_eta[iLepFO_Recl[0]],3)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[1]],LepGood_pt[iLepFO_Recl[1]],LepGood_eta[iLepFO_Recl[1]],3)*"\
"leptonSF_ttH(LepGood_pdgId[iLepFO_Recl[2]],LepGood_pt[iLepFO_Recl[2]],LepGood_eta[iLepFO_Recl[2]],3)"

MCA="tHq-multilepton/signal_extraction/mca-thq-2lss-mcdata-frdata_limits.txt"
CUTS="tHq-multilepton/cuts-thq-2lss.txt"
BINNING="thqMVA_ttv_2lss_40:thqMVA_tt_2lss_40 40,-1,1,40,-1,1"        
SYSTFILE="tHq-multilepton/signal_extraction/systsEnv.txt"
FUNCTION="--2d-binning-function 10:tHq_MVAto1D_2lss_10"
# FUNCTION="--2d-binning-function 10:tHq_MVAto1D_2lss_sbratio"
# FUNCTION="--2d-binning-function 11:tHq_MVAto1D_2lss_kmeans"
# NTUPLEFOLDER="thqtrees/finaltrees_Mar17/2lss/"

case "$CHANNEL" in
    "3l" )
        OPTIONS="${OPTIONS} ${OPT3L} --xp Gstar"
        MCA="tHq-multilepton/signal_extraction/mca-thq-3l-mcdata-frdata_limits.txt"
        CUTS="tHq-multilepton/cuts-thq-3l.txt"
        BINNING="thqMVA_ttv_3l_40:thqMVA_tt_3l_40 40,-1,1,40,-1,1"
        FUNCTION="--2d-binning-function 10:tHq_MVAto1D_3l_10"
        # NTUPLEFOLDER="thqtrees/finaltrees_Mar17/3l/"
        # FUNCTION="--2d-binning-function 10:tHq_MVAto1D_3l_sbratio"
        # FUNCTION="--2d-binning-function 5:tHq_MVAto1D_3l_kmeans"
        ;;
    "2lss_mm" )
        OPTIONS="${OPTIONS} ${OPT2L} -E mm_chan --xp Convs --xp Gstar --xp data_flips" # remove conversions for mm channel
        ;;
    "2lss_em" )
        OPTIONS="${OPTIONS} ${OPT2L} -E em_chan --xp Gstar"
        ;;
    "2lss_ee" )
        OPTIONS="${OPTIONS} ${OPT2L} -E ee_chan --xp Gstar"
        ;;
    "all" )
        ./$0 ${OUTNAME} 3l
        ./$0 ${OUTNAME} 2lss_mm
        ./$0 ${OUTNAME} 2lss_em
        ./$0 ${OUTNAME} 2lss_ee
        DONE
        ;;
    *)
        echo "${USAGE}"
        echo -e "\e[31mUnknown CHANNEL\e[0m"
        exit 1
esac

test -d $OUTNAME/$CHANNEL || mkdir -p $OUTNAME/$CHANNEL
echo "Storing output in ${OUTNAME}/${CHANNEL}/";
OPTIONS="${OPTIONS} --od ${OUTNAME}/${CHANNEL} -o ${CHANNEL}"

ARGUMENTS="${MCA} ${CUTS} ${BINNING} ${SYSTFILE}"
OPTIONS="${TREEINPUTS} ${FRIENDTREES} ${BASEOPTIONS} ${FUNCTION} ${OPTIONS}"
OPTIONS="${OPTIONS} --savefile ${FILENAME}"

echo "Normalizing to ${LUMI}/fb";
echo "mca      : ${MCA}"
echo "cuts     : ${CUTS}"
echo "binning  : ${BINNING}"
echo "systfile : ${SYSTFILE}"
echo "function : ${FUNCTION}"
echo "saving to: ${FILENAME}"

echo python makeShapeCardsTHQ.py ${ARGUMENTS} ${OPTIONS}

python makeShapeCardsTHQ.py ${ARGUMENTS} ${OPTIONS}

#if [[ "X$1" != "X" ]]; then
#    INPUTFILE=$1; shift;
#    if [[ ! -f ${INPUTFILE} ]]; then
#        echo "File ${INPUTFILE} does not exist"
#        exit 1
#    fi
#    echo "Reading from an input file: ${INPUTFILE}";
#    OPTIONS="${OPTIONS} --infile ${INPUTFILE}"
#    echo python makeShapeCardsTHQ.py ${ARGUMENTS} ${OPTIONS}
#else
#    echo "ntuples  : ${NTUPLEFOLDER}"
#    OPTIONS="${OPTIONS} --savefile ${OUTNAME}/${CHANNEL}/report_thq_${CHANNEL}.root"
#    OPTIONS="${OPTIONS} --ntuple_folder ${NTUPLEFOLDER}"
#    python makeShapeCardsTHQ.py ${ARGUMENTS} ${OPTIONS}
#fi


DONE
