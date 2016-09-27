#!/bin/bash

case $HOSTNAME in
cmsphys10*) P=/data1/g/gpetrucc/MuTnP80X/80X_v3/ ;;
*) P=root://eoscms//eos/cms/store/cmst3/user/gpetrucc/MuTnP80X/80X_v3/ ;;
esac;

PDIR="plots/80X/TnP/"
JOB="mupog_sos_v2.0"
XBINS="[3.5,7.5,10,15,20,30,45,70,120]"
EBINS="[-2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4]"
VBINS="[0.5,5.5,8.5,11.5,14.5,17.5,20.5,23.5,26.5,30.5,34.5]"
DATA=""
DATA="$DATA $P/data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run271036to275125_incomplete_slim2_withEAMiniIso.root"
DATA="$DATA $P/data/TnPTree_80X_Run2016B_v2_GoldenJSON_Run275126to275783_slim2_withEAMiniIso.root"
DATA="$DATA $P/data/TnPTree_80X_Run2016C_v2_GoldenJSON_Run275126to275783_slim2_withEAMiniIso.root"
DATA="$DATA $P/data/TnPTree_80X_Run2016C_v2_GoldenJSON_Run275784to276097_slim2_withEAMiniIso.root"
DATA="$DATA $P/data/TnPTree_80X_Run2016C_v2_GoldenJSON_Run276098to276384_slim2_withEAMiniIso.root"
DATA="$DATA $P/data/TnPTree_80X_Run2016D_v2_GoldenJSON_Run276098to276384_slim2_withEAMiniIso.root"
MC=$(for I in $(seq 1 5); do echo -n " --refmc $P/DY_madgraphMLM/TnPTree_80X_DYLL_M50_MadGraphMLM_part${I}_slim2_withEAMiniIso.root "; done)
PDS="$DATA $MC"

OPTS=" --doRatio  --pdir $PDIR/$JOB  " 
OPTS="$OPTS -t tpTree/fitter_tree  --mc-cut mcTrue --mc-mass mass   "
case $HOSTNAME in
cmsphys10) OPTS="$OPTS -j 8 ";;
lxplus*.cern.ch) OPTS="$OPTS -j 4" ;;
esac;

LAUNCHER="bash"
if [[ "$1" == "-q" ]]; then
    LAUNCHER="bsub -q $2 $PWD/runBatch $PWD $SCRAM_ARCH bash ";
    shift; shift;
fi;

if [[ "$1" == "all" ]]; then
  shift;
  for ID in SOS SOS_PR; do #SOS_NM1_{Id,Iso,Ip} SOS_003 SOS_NoIP SOS_presel; do 
     for SMOD in MCTG dvoigt2; do # dvoigt2 BWDCB2 BWDCB; do  
        for BMOD in bern4 bern3; do # expo ; do
            for W in be eta vtx; do 
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

MASS="  -m mass 80,70,115 "
CDEN0="tag_IsoMu22 && tag_pt > 20 && tag_SIP < 4"
SOS_OLD_ID="PF && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0"
SOS_ID="PF && TMOST && tkTrackerLay > 5 && tkValidPixelHits  > 0"
SOS_PRESEL_ID="PF"
SOS_IP="abs(dzPV) < .01 && abs(dB) < 0.01 && SIP < 8"
SOS_IP3="abs(dzPV) < .03 && abs(dB) < 0.03 && SIP < 8"
SOS_PRESEL_IP="abs(dzPV) < 1.0 && abs(dB) < 0.50 && SIP < 8"
SOS_ISO="combRelIsoPF04dBeta*pt < 10 && combRelIsoPF03dBeta < 0.5 && (combRelIsoPF03dBeta*pt < 5 || combRelIsoPF03dBeta < 0.1)"
SOS_PRESEL_ISO="combRelIsoPF04dBeta*pt < 10"
RECO="(Glb||TM)"
ARB_PT="pair_probeMultiplicity_Pt10_M60140 == 1"
ARB_ID="pair_probeMultiplicity_TMGM == 1"

case $ID in
  SOS) NUM="$SOS_ID && $SOS_IP && $SOS_ISO" ; CDEN="$CDEN0 && $ARB_ID && PF";;
  SOS_003) NUM="$SOS_ID && $SOS_IP3 && $SOS_ISO" ; CDEN="$CDEN0 && $ARB_ID && PF";;
  SOS_NoIP) NUM="$SOS_ID && $SOS_ISO" ; CDEN="$CDEN0 && $ARB_ID && PF";;
  SOS_presel) NUM="$SOS_PRESEL_ID && $SOS_PRESEL_ISO && $SOS_PRESEL_IP" ; CDEN="$CDEN0 && $ARB_ID && PF";;
  SOS_PR) NUM="$SOS_ID && $SOS_ISO && $SOS_IP" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_PRESEL_ID && $SOS_PRESEL_ISO && $SOS_PRESEL_IP";;
  SOS_Id) NUM="$SOS_ID" ; CDEN="$CDEN0 && $ARB_ID && PF";;
  SOS_NM1_Id) NUM="$SOS_ID" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_ISO && $SOS_IP";;
  SOS_NM1_Iso) NUM="$SOS_ISO" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_ID && $SOS_IP";;
  SOS_NM1_Ip) NUM="$SOS_IP" ; CDEN="$CDEN0 && $ARB_ID && PF && $SOS_ISO && $SOS_ID";;
  Loose)        NUM="PF" ; CDEN="$CDEN0 && $ARB_PT"     ;                       XBINS=[10,25,40] ;;
  LooseFromIso) NUM="PF" ; CDEN="$CDEN0 && $ARB_PT && isoTrk03Rel < 0.2 ";      XBINS=[10,25,40] ;;
  LooseIdOnly)  NUM="PF" ; CDEN="$CDEN0 && $ARB_ID && $ARB_PT && (Glb || TM) "; XBINS=[10,25,40] ;;
  *) echo "Uknown ID $ID"; exit 2;;
esac;

DEN="$CDEN"; POST=""; 
if [[ "$SMOD" == "MCTG" ]]; then OPTS="${OPTS} --fine-binning 100  "; fi

function getcut() { case $1 in
        barrel) CUT="abseta < 1.2";;
        endcap) CUT="abseta > 1.2";;
        pt520) CUT="pt > 5 && pt < 20";;
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
