#!/bin/bash

if [[ "$1" == "SingleLepAFS" ]]; then
    shift # shift register
    T="/afs/cern.ch/work/k/kirschen/public/PlotExampleSamples/V3";
    FT="/afs/cern.ch/work/k/kirschen/public/PlotExampleSamples/PHYS14_V3_FriendsRefinedIds"
    J=4;
elif [[ "$HOSTNAME" == *"lxplus"* ]] ; then
    T="/afs/cern.ch/work/k/kirschen/public/PlotExampleSamples/V3";
    FT="/afs/cern.ch/work/a/alobanov/public/SUSY/CMG/CMGtuples/FriendTrees/phys14_v3_btagCSVv2"
    J=4;
elif [[ "$1" == "DESYV3" ]] ; then
    shift # shift register
    T="/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Phys14_v3/ForCMGplot";
    FT="/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Phys14_v3/Phys14_V3_Friend_CSVbtag"
    J=8;
elif [[ "$1" == "QCDLp" ]] ; then
    shift # shift register
    T="/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Phys14_v3/ForCMGplot";
    FT="/nfs/dust/cms/user/lobanov/SUSY/Run2/RA4/MC/CMGtuples/FriendTrees/phys14_v3_Lp"
    J=8;
elif [[ "$HOSTNAME" == *"naf"* ]] ; then
    T="/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Phys14_v3/ForCMGplot";
    FT="/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/Phys14_v3/Phys14_V3_Friend_CSVbtag"
    J=8;
else
    echo "Didn't specify location!"
    echo "Usage: ./make_cards.sh location analysis "
    exit 0
fi

echo "Going to use these directories:"
echo "CMG tuples:" $T
echo "Friend Trees:" $FT

LUMI=3.0
OUTDIR="yields/QCD_yields_3fb_AllBins"
OPTIONS=" -P $T -j $J -l $LUMI -f --s2v --tree treeProducerSusySingleLepton --od $OUTDIR --asimov "

# Get current plotter dir
#PLOTDIR="$CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/"
PLOTDIR=$(pwd -P)
PLOTDIR=${PLOTDIR/plotter/plotterX}
PLOTDIR=$(echo $PLOTDIR |  cut -d 'X' -f 1 )

# Append FriendTree dir
OPTIONS=" $OPTIONS -F sf/t $FT/evVarFriend_{cname}.root "

function makeCard_1l {
    local EXPR=$1; local BINS=$2; local SYSTS=$3; local OUT=$4; local GO=$5

    # choose CF and MCA files
    CutFlowCard="qcd-est/cards_qcd_cf.txt"
    McaFile="mca-QCDonly_split.txt"

    EXTRALABEL=""

    # b-jet cuts
    case $nB in
	0B)  GO="${GO} -R nBtags 0nB nBJetMedium30==0 "; EXTRALABEL="${EXTRALABEL} nB=0\n" ;;
	1B)  GO="${GO} -R nBtags nBtags nBJetMedium30==1 "; EXTRALABEL="${EXTRALABEL} nB=1\n" ;;
	2B)  GO="${GO} -R nBtags 2nB nBJetMedium30==2 "; EXTRALABEL="${EXTRALABEL} nB=2\n" ;;
	2Btop)  GO="${GO} -R nBtags 2nB nBJetMedium30==2&&Topness>5 "; EXTRALABEL="${EXTRALABEL} nB=2(+topness)\n" ;;
	1p)  GO="${GO} -R nBtags nBtagsp nBJetMedium30>=1 "; EXTRALABEL="${EXTRALABEL} nB#geq1\n" ;;
	2p)  GO="${GO} -R nBtags 2nBp nBJetMedium30>=2 "; EXTRALABEL="${EXTRALABEL} nB#geq2\n" ;;
	3p)  GO="${GO} -R nBtags 3nBp nBJetMedium30>=3 "; EXTRALABEL="${EXTRALABEL} nB#geq3\n" ;;
    esac;

    # ST categories
    case $ST in
	STi)  GO="${GO} -R STcut st200Inf ST>200 "; EXTRALABEL="${EXTRALABEL} ST>200 GeV\n" ;;
	ST0)  GO="${GO} -R STcut st200250 ST>200&&ST<250 "; EXTRALABEL="${EXTRALABEL} 200<ST<250 GeV\n" ;;
	ST1)  GO="${GO} -R STcut st250350 ST>250&&ST<350 "; EXTRALABEL="${EXTRALABEL} 250<ST<350 GeV\n" ;;
	ST2)  GO="${GO} -R STcut st350450 ST>350&&ST<450 "; EXTRALABEL="${EXTRALABEL} 350<ST<450 GeV\n" ;;
	ST3)  GO="${GO} -R st200 st450600 ST>450&&ST<600 "; EXTRALABEL="${EXTRALABEL} 450<ST<600 GeV\n" ;;
	ST4)  GO="${GO} -R st200 st600Inf ST>600 "; EXTRALABEL="${EXTRALABEL} ST>600 GeV\n" ;;
	STDynDP0)  GO="${GO} -R STcut st200250 ST>200&&ST<250 -R dphi dp10 fabs(DeltaPhiLepW)>1.0 "; EXTRALABEL="${EXTRALABEL} 200<ST<250 GeV\n #Delta#phi>1.0\n" ;;
	STDynDP1)  GO="${GO} -R STcut st250350 ST>250&&ST<350 -R dphi dp10 fabs(DeltaPhiLepW)>1.0 "; EXTRALABEL="${EXTRALABEL} 250<ST<350 GeV\n #Delta#phi>1.0\n" ;;
	STDynDP2)  GO="${GO} -R STcut st350450 ST>350&&ST<450 -R dphi dp075 fabs(DeltaPhiLepW)>0.75 "; EXTRALABEL="${EXTRALABEL} 350<ST<450 GeV\n #Delta#phi>0.75\n" ;;
	STDynDP3)  GO="${GO} -R STcut st450550 ST>450&&ST<550 -R dphi dp075 fabs(DeltaPhiLepW)>0.75 "; EXTRALABEL="${EXTRALABEL} 450<ST<550 GeV\n #Delta#phi>0.75\n" ;;
	STDynDP4)  GO="${GO} -R STcut st550700 ST>550&&ST<700 -R dphi dp05 fabs(DeltaPhiLepW)>0.5 "; EXTRALABEL="${EXTRALABEL} 550<ST<700 GeV\n #Delta#phi>0.5\n" ;;
	STDynDP5)  GO="${GO} -R STcut st700Inf ST>700 -R dphi dp05 fabs(DeltaPhiLepW)>0.5 "; EXTRALABEL="${EXTRALABEL} ST>700 GeV\n #Delta#phi>0.5\n" ;;
    esac;

    # jet multiplicities
    case $nJ in
	23j)  GO="${GO} -R nJets 23j nCentralJet30>=2&&nCentralJet30<=3"; EXTRALABEL="${EXTRALABEL} 2-3 jets\n"  ;;
	34j)  GO="${GO} -R nJets 34j nCentralJet30>=3&&nCentralJet30<=4"; EXTRALABEL="${EXTRALABEL} 3-4 jets\n"  ;;
	45j)  GO="${GO} -R nJets 45j nCentralJet30>=4&&nCentralJet30<=5"; EXTRALABEL="${EXTRALABEL} 4-5 jets\n"  ;;
	68j)  GO="${GO} -R nJets 67j nCentralJet30>=6&&nCentralJet30<=8"; EXTRALABEL="${EXTRALABEL} 6-8 jets\n"  ;;
	6Infj)  GO="${GO} -R nJets geq6j nCentralJet30>=6"; EXTRALABEL="${EXTRALABEL} #geq6 jets\n"  ;;
	9Infj)  GO="${GO} -R nJets geq8j nCentralJet30>=9"; EXTRALABEL="${EXTRALABEL} #geq9 jets\n"  ;;
	68TTj)  GO="${GO} -R nJets 68TTj nCentralJet30+2*nHighPtTopTagPlusTau23>=6&&nCentralJet30+2*nHighPtTopTagPlusTau23<9"; EXTRALABEL="${EXTRALABEL} 6-8 TT enh. jets\n"  ;;
	9InfTTj)  GO="${GO} -R nJets 9InfTTj nCentralJet30+2*nHighPtTopTagPlusTau23>=9"; EXTRALABEL="${EXTRALABEL} #geq9 TT enh. jets\n"  ;;
    esac;

    # HT and "R&D" categories
    case $HT in
	HTi) GO="${GO} -R HTcut ht500Inf HT>500"; EXTRALABEL="${EXTRALABEL} HT>500 GeV\n"  ;;
	HT0) GO="${GO} -R HTcut ht500750 HT>500&&HT<=750"; EXTRALABEL="${EXTRALABEL} 500<HT<750 GeV\n"  ;;
	HT1) GO="${GO} -R HTcut ht7501250 HT>750&&HT<=1250"; EXTRALABEL="${EXTRALABEL} 750<HT<1250 GeV\n"  ;;
	HT2) GO="${GO} -R HTcut ht1250Inf HT>1250"; EXTRALABEL="${EXTRALABEL} HT>1250 GeV\n"  ;;
    esac;

    echo $EXTRALABEL

    if [[ "$PRETEND" == "1" ]]; then
	echo "making datacard $OUT from makeShapeCardsSusy.py $McaFile $CutFlowCard \"$EXPR\" \"$BINS\" $SYSTS $GO --dummyYieldsForZeroBkg;"
    else
	#echo "making datacard $OUT from makeShapeCardsSusy.py $McaFile $CutFlowCard \"$EXPR\" \"$BINS\" $SYSTS $GO --dummyYieldsForZeroBkg;"
	python $PLOTDIR/makeShapeCardsSusy.py $PLOTDIR/$McaFile $PLOTDIR/susy-1lep/$CutFlowCard "$EXPR" "$BINS" $SYSTS -o $OUT $GO --dummyYieldsForZeroBkg;
	echo "  -- done at $(date)";
    fi;
}

function combineCardsSmart {

    DummyC=0
    AllC=0
    CMD=""
    for C in $*; do
	# missing datacards
	test -f $C || continue;

	if grep -q "DummyContent" $C; then
	    echo "empty bin ${C}" >&2
	    DummyC=$(($DummyC+1))
	    if grep -q "observation 0.0$" $C; then
		echo "this is not the way it was intended..."
	    fi
	fi

	grep -q "observation 0.0$" $C && continue # skip empty bins
#       grep -q "observation 0.01$" $C && grep -q "DummyContent" $C && continue #skip bins with only DummyContent as well
	AllC=$((AllC+1))
	CMD="${CMD} $(basename $C .card.txt)=$C ";
    done
    if [[ "$CMD" == "" ]]; then
	echo "Not any card found in $*" 1>&2 ;
    else
	echo "combineCards.py $CMD" >&2
	combineCards.py $CMD
    fi
    if [[ "$DummyC" != "0" ]]; then
	echo "In total $DummyC out of $AllC are empty, but taken into account by adding DummyContent." >&2
    fi
    #echo "In total $DummyC out of $AllC are empty, but taken into account by adding DummyContent." >&2
}

if [[ "$1" == "--pretend" ]]; then
    PRETEND=1; shift;
    echo "# Pretending to run" $1
fi;

if [[ "$1" == "--makeCards" ]]; then

    SYSTS="../limits/syst/susyDummy.txt"
    CnC_expr="1" #not used as of now
    CnC_bins="[0.5,1.5]"

    STValue="$2"
    echo "$STValue"

    echo "Making individual datacards"

#for baseline analysis:
#    for ST in "$STValue"; do for nJ in 45j 68j 6Infj 9Infj; do for nB in 1p 1B 2B 3p; do for HT in HT0 HT1 HT2; do for RD in Def; do
#    for ST in STDynDP0 STDynDPHI STDynDP2 STDynDP3 STDynDP4 STDynDP5; do for nJ in 45j 68j 6Infj 9Infj; do for nB in 1p 1B 2B 3p; do for HT in HT0 HT1 HT2; do for RD in Def; do

    # for QCD
    for ST in ST0 ST1 ST2 ST3 ST4; do
	for nJ in 45j 68j; do
	    for nB in 0B 1B 2B 3p; do
		for HT in HT0 HT1 HT2; do
		    echo "###################################################################"
		    echo " --- QCDyield_${nB}_${ST}_${nJ}_${HT} ---"
		    makeCard_1l $CnC_expr $CnC_bins $SYSTS QCDyield_${nB}_${ST}_${nJ}_${HT} "$OPTIONS";
		done;
	    done;
	done;
    done;
    exit 0

fi

echo "Done at $(date)";
