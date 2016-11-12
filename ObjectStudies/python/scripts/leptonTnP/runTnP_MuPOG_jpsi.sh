#!/bin/bash

case $HOSTNAME in
cmsco01*) exit 1; P=/data1/gpetrucc/MUPOG_TnP_76X/ ;;
cmsphys10*) P=/data1/g/gpetrucc/MuTnP80X/ ;;
*) exit 1; P=root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/ ;;
esac;

PDIR="plots/80X/TnP/"
JOB="mupog_v1.0_jpsi"
XBINS="[3,3.5,4,4.5,5,6,7,8,10,12,18,25]"
EBINS="[-2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4]"
VBINS="[0.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,24.5,26.5,28.5,30.5,34.5]"

MC=$P/jpsi/TnPTree_80X_TuneCUEP8M1.root
DATA=$P/jpsi/TnPTree_80X_Run2016B_v2_GoldenJSON_Run271036to275376.root
DATA="$DATA $P/jpsi/TnPTree_80X_Run2016C_v2_GoldenJSON_Run275377to276097.root"
PDS="$DATA --refmc $MC"

OPTS=" --doRatio  --pdir $PDIR/$JOB -j 5 " #--mcw vtxWeight2015(nVert)"
OPTS="$OPTS -t tpTree/fitter_tree  --mc-cut 1 --mc-mass mass   "
if [[ "$1" != "" ]]; then SEL=$1; OPTS="$OPTS --reqname $1 "; shift; fi
if [[ "$1" != "" ]]; then OPTS="$OPTS $* "; shift; fi
MASS="  -m mass 80,2.85,3.34"
CDEN=" tag_Mu7p5_Track2_Jpsi_MU && pair_drM1 > 0.5 "
for ID in Loose Reco ; do
  if [[ "$SEL" != "" ]] && echo $SEL | grep -q -v $ID; then continue; fi
  NUM="$ID"
  if [[ "$ID" == "Reco" ]]; then NUM="(Glb || TM)"; fi
  if [[ "$ID" == "LooseIdOnly" ]]; then NUM="Loose"; CDEN="$CDEN && (Glb || TM)"; fi
  for BMOD in bern3 ; do # bern4 expo
    if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
    for SMOD in  JDGauss; do # JGauss  JCB
        if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
        DEN="$CDEN"; POST=""
        python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
        python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
        python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
        python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        exit
        if [[ "$SMOD" == "JDGauss" && "$BMOD" == "bern3" ]]; then
            MASS2=" -m mass 80,2.9,3.28"; POST="_mass"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)" ;
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";

            DEN="$CDEN && SIP < 4"; POST="_sip4"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
            
            DEN="$CDEN && pair_distM2 > 200 && pair_dphiVtxTimesQ < 0"; POST="_sep"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 7 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt7_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        fi;
    done    
  done
done
