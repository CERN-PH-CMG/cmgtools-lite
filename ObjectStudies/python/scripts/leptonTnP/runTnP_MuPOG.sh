#!/bin/bash

case $HOSTNAME in
cmsco01*) exit 1; P=/data1/gpetrucc/MUPOG_TnP_76X/ ;;
cmsphys10*) P=/data1/g/gpetrucc/MuTnP80X/ ;;
*) exit 1; P=root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/ ;;
esac;

PDIR="plots/80X/TnP/"
JOB="mupog_v0"
XBINS="[5,10,15,20,30,40,60,80,120]"
EBINS="[-2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4]"
VBINS="[0.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,24.5,26.5,28.5,30.5,34.5]"
DATA="$P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run271036to273730_NotCompleted.root"
DATA="$DATA $P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root"
DATA="$DATA $P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274241to274421.root"
DATA="$DATA $P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274422to274443.root"
MC=$(for I in $(seq 1 7); do echo -n " --refmc $P/TnPTree_80X_DYLL_M50_MadGraphMLM_part${I}.root "; done)
#DATA=$(for I in $(seq 1 7); do echo $P/TnPTree_v41_76X_RunD_part${I}_withEAMiniIso.root; done)
#MC=$(for I in $(seq 1 2); do echo " --refmc $P/TnPTree_76X_DYLL_M50_MadGraphMLM_part${I}_withEAMiniIso.root"; done)
PDS="$DATA $MC"
#PDS=$(echo "$PDS" | sed 's/.root/_withEAMiniIso.root/g')
OPTS=" --doRatio  --pdir $PDIR/$JOB -j 5 " #--mcw vtxWeight2015(nVert)"
OPTS="$OPTS -t tpTree/fitter_tree  -m mass 80,70,115 --mc-cut mcTrue --mc-mass mass   "
if [[ "$1" != "" ]]; then SEL=$1; OPTS="$OPTS --reqname mu_${1/mu_/} "; OPTS="${OPTS/-j 5/-j 0}"; shift; fi
if [[ "$1" != "" ]]; then OPTS="$OPTS $* "; shift; fi
MASS="  -m mass 80,70,115 "
CDEN="(tag_IsoMu20 || tag_IsoMu20_eta2p1 ) && tag_pt > 20 && tag_SIP < 4"
#for ID in SOS_Id_vs{Loose,Reco,LooseIso,RecoIso} SOS_Iso_vsId SOS_Ip_vsIdIso SOS; do # SIP4 SIP8 LooseFromIso LooseIdOnly; do # LooseIdOnly
for ID in SOS_PR ; do # SIP4 SIP8 LooseFromIso LooseIdOnly; do # LooseIdOnly
  if [[ "$SEL" != "" ]] && echo $SEL | grep -q -v $ID; then continue; fi
  case $ID in
      SOS) NUM="combRelIsoPF04dBeta*pt < 10 && abs(dzPV) < 1.0 && abs(dB) < 0.50 && SIP < 8" ; 
           NUM="$NUM && abs(dzPV) < .01 && abs(dB) < 0.01 "
           NUM="$NUM && combRelIsoPF03dBeta < 0.5 && (combRelIsoPF03dBeta*pt < 5 || combRelIsoPF03dBeta < 0.1)" 
           NUM="$NUM && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && Loose " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_003) NUM="combRelIsoPF04dBeta*pt < 10 && abs(dzPV) < 1.0 && abs(dB) < 0.50 && SIP < 8" ; 
           NUM="$NUM && abs(dzPV) < .03 && abs(dB) < 0.03 "
           NUM="$NUM && combRelIsoPF03dBeta < 0.5 && (combRelIsoPF03dBeta*pt < 5 || combRelIsoPF03dBeta < 0.1)" 
           NUM="$NUM && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && Loose " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_NoIP) NUM="combRelIsoPF04dBeta*pt < 10" ; 
           NUM="$NUM && combRelIsoPF03dBeta < 0.5 && (combRelIsoPF03dBeta*pt < 5 || combRelIsoPF03dBeta < 0.1)" 
           NUM="$NUM && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && Loose " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_PR) 
           NUM="combRelIsoPF03dBeta < 0.5 && (combRelIsoPF03dBeta*pt < 5 || combRelIsoPF03dBeta < 0.1)" 
           NUM="$NUM && abs(dzPV) < .01 && abs(dB) < 0.01 "
           NUM="$NUM && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && Loose " ;
           CDEN="$CDEN && combRelIsoPF04dBeta*pt < 10 && abs(dzPV) < 1.0 && abs(dB) < 0.50 && SIP < 8" ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_Id_vsLoose) NUM="TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && Loose " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_Id_vsReco) NUM="Loose && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && (Glb || TM) " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_Id_vsRecoIso) NUM="Looose"
           NUM="$NUM && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && combRelIsoPF04dBeta*pt < 10 && combRelIsoPF03dBeta < 0.5 && combRelIsoPF03dBeta*pt < 5" 
           CDEN="$CDEN && (Glb || TM) " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_Id_vsLooseIso) NUM="TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           CDEN="$CDEN && combRelIsoPF04dBeta*pt < 10 && combRelIsoPF03dBeta < 0.5 && combRelIsoPF03dBeta*pt < 5" 
           CDEN="$CDEN && Loose " ;
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_Iso_vsId) 
           NUM="combRelIsoPF04dBeta*pt < 10 && combRelIsoPF03dBeta < 0.5 && combRelIsoPF03dBeta*pt < 5" 
           CDEN="$CDEN && Loose " ;
           CDEN="$CDEN && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      SOS_Ip_vsIdIso) NUM="abs(dzPV) < 1.0 && abs(dB) < 0.50 && SIP < 8" ; 
           NUM="$NUM && abs(dzPV) < .01 && abs(dB) < 0.01 "
           CDEN="$CDEN && ccombRelIsoPF04dBeta*pt < 10 && ombRelIsoPF03dBeta < 0.5 && combRelIsoPF03dBeta*pt < 5" 
           CDEN="$CDEN && Loose " ;
           CDEN="$CDEN && TMOST && Track_HP && tkTrackerLay > 5 && tkValidPixelHits  > 0" # AKA SOFT ID
           XBINS="[3.5,6.5,10,15,20,25,40,70,120]" ;;
      ttHPresel) NUM="SIP < 8 && pfCombRelMiniIsoEACorr < 0.4"; CDEN="$CDEN && Loose "; ;; 
      Loose)        NUM="Loose" ; CDEN="$CDEN"; XBINS=[25,30,40,60,80,120] ;;
      LooseIdOnly)  NUM="Loose" ; CDEN="$CDEN && (Glb || TM) ";;
      LooseFromIso) NUM="Loose" ; CDEN="$CDEN && isoTrk03Rel < 0.2 " ;;
  esac;
  for BMOD in bern4 ; do # bern3 bern4 expo #
    if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
    SMODs="MCTG"; if expr match $ID Loose > /dev/null; then SMODs="dvoigt2"; fi;
    for SMOD in $SMODs; do # dvoigt BWDCB  MCTG
        if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $SMOD; then continue; fi
        DEN="$CDEN"; POST=""; OPTSGO="${OPTS}"
        if [[ "$SMOD" == "MCTG" ]]; then OPTSGO="${OPTSGO} --fine-binning 100  "; fi
        python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
        python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
        #if [[ "$ID" == "Loose" ]]; then
        #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        #fi;
        continue
        if [[ "$ID" == "SOS" ]]; then
            python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        fi;
        continue;
        if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
            MASS2=" -m mass 100,65,125"; POST="_mass"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
            python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
        fi
        if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
            DEN="$CDEN && tag_pt > 25 && tag_combRelIsoPF04dBeta < 0.15"; POST="_tightTag"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
            python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";

            DEN="$CDEN && isoTrk03Rel < 0.5"; POST="_looseIso"
            #python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";


            DEN="$CDEN && SIP < 2"; POST="_tightSIP"
            #python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTSGO --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTSGO --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";

        fi;
    done;
  done;
done
