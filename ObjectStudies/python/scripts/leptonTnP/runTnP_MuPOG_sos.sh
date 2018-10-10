#!/bin/bash

year=2017

if [ "${year}" == 2016 ]; then
    case $HOSTNAME in
        cmsphys10*) P=/data1/g/gpetrucc/MuTnP80X/ ;;
        *) P=root://eoscms//eos/cms/store/cmst3/user/gpetrucc/MuTnP80X/80X_v3/ ;;
    esac;
    DATA=""
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016B_GoldenJSON_Run276098to276384.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016C_GoldenJSON_Run276098to276384.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016D_GoldenJSON_Run276098to276384.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016E_GoldenJSON_Run276098to276384.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016F_GoldenJSON_Run276098to276384.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016G_GoldenJSON_Run278819to280384.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016H_GoldenJSON_Run284036to284044.root"
    DATA="$DATA $P/${KIND}_TnPTree_80XRereco_Run2016H_v2_GoldenJSON_Run281613to284035.root"
    KIND="slimTree"
    KIND="superSlim_sos_slimTree"
    MC=$(for I in $(seq 1 11); do echo -n " --refmc $P/${KIND}_MC_Moriond17_DY_tranch4Premix_part${I}.root "; done)
    PDIR="plots/80X/TnP_Moriond17/"
else
    DATA=/eos/cms/store/group/phys_muon/TagAndProbe/Run2017/94X/Run?/TnPTree_17Nov2017_SingleMuon_Run2017?v1_Full_GoldenJSON.root
    MC=/eos/cms/store/group/phys_muon/TagAndProbe/Run2017/94X/MC/TnPTree_94X_DYJetsToLL_M50_Madgraph.root
    PDIR=plots/94X/TnP_ICHEP18/
fi

JOB="mupog_sos_v3.0"
XBINS="[3.5,7.5,10,15,20,30,40,60]" #,45,70,120]"
EBINS="[-2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4]"
VBINS="[0.5,7.5,11.5,14.5,17.5,20.5,23.5,26.5,30.5,35.5]"
PDS="$DATA --refmc $MC"

OPTS=" --doRatio  --pdir $PDIR/$JOB  "
OPTS="$OPTS -t tpTree/fitter_tree  --mc-cut mcTrue --mc-mass mass   "
case $HOSTNAME in
    cmsphys10) OPTS="$OPTS -j 8 ";;
    lxplus*.cern.ch) OPTS="$OPTS -j 0" ;;
esac;

LAUNCHER="bash"
if [[ "$1" == "-q" ]]; then
    LAUNCHER="bsub -q $2 $PWD/runBatch $PWD $SCRAM_ARCH bash ";
    shift; shift;
fi;

if [[ "$1" == "all" ]]; then
    shift;
    for ID in SOS SOS_PR SOS_ID SOS_ISO SOS_IP; do #SOS_NM1_{Id,Iso,Ip} SOS_003 SOS_NoIP SOS_presel; do
        for SMOD in MCTG dvoigt2 ; do # MCTG dvoigt2 BWDCB2 BWDCB; do
            for BMOD in bern4 bern3 ; do # expo bern3; do
                for W in all; do  # eta vtx
                    echo $LAUNCHER $0 $ID $SMOD $BMOD $W
                done
            done
        done
    done
    exit
else
    if [[ "$4" == "" ]]; then echo "usage: $0 all || $0 ID SMOD  BMOD [ bin | all ]"; exit 1; fi;
        ID=$1; SMOD=$2; BMOD=$3; shift; shift; shift;
        bin=$1; shift;
    fi;

    if [[ "$1" != "" ]]; then OPTS="$OPTS $* "; fi

    MASS="  -m mass 80,75,115 "
    #CDEN0="(tag_IsoMu22 || tag_IsoMu24) && tag_pt > 20 && tag_SIP < 4"
    CDEN0="1"
    #SOS_ID="PF && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0"
    SOS_ID="PF && TMOST && tkTrackerLay > 5 && tkValidPixelHits  > 0"
    SOS_FO_ID="PF"
    SOS_IP="SIP < 2 && IP < 0.01" # FIXME
    SOS_FO_IP="SIP < 2.5 && IP < 0.0175" # FIXME
    SOS_PRESEL_IP="abs(dzPV) < 1.0 && abs(dB) < 0.50"
    SOS_ISO="combRelIsoPF03dBeta < 0.5 && combRelIsoPF03dBeta*pt < 5"
    SOS_FO_ISO="combRelIsoPF03dBeta*pt < 20 + 300/pt"
    RECO="(Glb||TM)"
    ARB_PT="pair_probeMultiplicity_Pt10_M60140 == 1"
    ARB_ID="pair_probeMultiplicity_TMGM == 1"

    case $ID in
        SOS) NUM="$SOS_ID && $SOS_IP && $SOS_ISO && $SOS_PRESEL_IP" ; CDEN="$CDEN0 && $ARB_ID && PF";;
        SOS_ID) NUM="$SOS_ID" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_PRESEL_IP";;
        SOS_ISO) NUM="$SOS_ISO" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_PRESEL_IP && $SOS_ID";;
        SOS_IP) NUM="$SOS_IP" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_PRESEL_IP && $SOS_ID && $SOS_ISO";;
        SOS_FO) NUM="$SOS_FO_ID && $SOS_FO_ISO && $SOS_FO_IP && $SOS_PRESEL_IP" ; CDEN="$CDEN0 && $ARB_ID && PF";;
        SOS_PR) NUM="$SOS_ID && $SOS_ISO && $SOS_IP" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_FO_ID && $SOS_FO_ISO && $SOS_FO_IP && $SOS_PRESEL_IP";;
        *) echo "Uknown ID $ID"; exit 2;;
    esac;

    DEN="$CDEN"; POST="";
    if [[ "$SMOD" == "MCTG" ]]; then OPTS="${OPTS} --fine-binning 100  "; fi

    function getcut() { case $1 in
    barrel) CUT="abseta < 1.2";;
    endcap) CUT="abseta > 1.2";;
    pt520) CUT="pt > 3.5 && pt < 20";;
    pt20)  CUT="pt > 20";;
    *) echo "Unknown ptCut $1"; exit 3;
esac; }

case $bin in
    barrel|endcap) getcut $bin;
        python tnpEfficiency.py $PDS -d "$CUT && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_$bin -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;;
    eta_*) getcut ${bin/eta_};
        python tnpEfficiency.py $PDS -d "$CUT && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_$bin   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";;
    vtx_*) getcut ${bin/vtx_};
        python tnpEfficiency.py $PDS -d "$CUT && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_$bin   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";;
        # ---------------------------------
    all)
        for B in barrel endcap eta_pt520 vtx_pt520 eta_pt20 vtx_pt20; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    eta)
        for B in eta_pt520 eta_pt20; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    vtx)
        for B in vtx_pt520 vtx_pt20; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    be)
        for B in barrel endcap; do bash $0 $ID $SMOD $BMOD $B $*; done;;
        # ---------------------------------
    *)
        echo "I don't know the bin $bin"; exit 4;
esac;

#if [[ "$ID" == "Loose" ]]; then
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
#fi;


if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
MASS2=" -m mass 100,65,125"; POST="_mass"
#python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
#python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
fi

if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
DEN="$CDEN && tag_pt > 25 && tag_combRelIsoPF04dBeta < 0.15"; POST="_tightTag"
#python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
#python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";

DEN="$CDEN && isoTrk03Rel < 0.5"; POST="_looseIso"
#python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";


DEN="$CDEN && SIP < 2"; POST="_tightSIP"
#python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
#python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
fi;
