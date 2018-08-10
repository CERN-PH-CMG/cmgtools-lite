#!/bin/bash

case $HOSTNAME in
cmsco01*) P=/data1/gpetrucc/MUPOG_TnP_76X/ ;;
*) exit 1; P=root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/ ;;
esac;

PDIR="../plotting/plots/76X_220116/zTnP/"
JOB="mupog_v3"
XBINS="[5,10,15,20,25,30,35,40,50,60,80]"
EBINS="[-2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,-0.2,0.2,0.3,0.6,0.9,1.2,1.6,2.1,2.4]"
VBINS="[0.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,17.5,20.5]"
JBINS="[-0.5,0.5,1.5,2.5,3.5,4.5,5.5]"
DATA=$(for I in $(seq 1 7); do echo $P/TnPTree_v41_76X_RunD_part${I}_withEAMiniIso.root; done)
MC=$(for I in $(seq 1 2); do echo " --refmc $P/TnPTree_76X_DYLL_M50_MadGraphMLM_part${I}_withEAMiniIso.root"; done)
PDS="$DATA $MC"

OPTS=" --doRatio  --pdir $PDIR/$JOB -j 5 " #--mcw vtxWeight2015(nVert)"
OPTS="$OPTS -t tpTree/fitter_tree  -m mass 80,70,115 --mc-cut mcTrue --mc-mass mass  --minimizer-strategy 1 "
if [[ "$1" != "" ]]; then SEL=$1; OPTS="$OPTS --reqname mu_${1/mu_/} "; shift; fi
if [[ "$1" != "" ]]; then OPTS="$OPTS $* "; shift; fi
MASS="  -m mass 80,70,115 "
CDEN="(tag_IsoMu20 || tag_IsoMu20_eta2p1 ) && tag_pt > 20 && tag_SIP < 4"
CDEN="$CDEN && Loose && SIP < 8 && abs(dzPV) < 0.1 && abs(dB) < 0.05"
for ID in MiniIso04; do
  if [[ "$SEL" != "" ]] && echo $SEL | grep -q -v $ID; then continue; fi
  case $ID in
      MiniIso04) NUM="pfCombRelMiniIsoEACorr < 0.4" ; 
  esac;
  for BMOD in bern3 bern4 expo; do  
    if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
    for SMOD in dvoigt BWDCB BWDCB2 ; do 
    if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
        DEN="$CDEN"; POST=""
        python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
        python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
        python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
        python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var pair_nJets30 $JBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_njet   -b $BMOD -s $SMOD $MASS --xtitle "N(jets)";
        if [[ "$SMOD" == "dvoigt" && "$BMOD" == "bern3" ]]; then
            MASS2=" -m mass 100,65,125"; POST="_mass"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
            python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var pair_nJets30 $JBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_njet   -b $BMOD -s $SMOD $MASS2 --xtitle "N(jets)";

            DEN="$CDEN && tag_pt > 25 && tag_combRelIsoPF04dBeta < 0.15"; POST="_tightTag"
            python tnpEfficiency.py $PDS -d "abs(eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "abs(eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
            python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var pair_nJets30 $JBINS -N mu_${SMOD}_${BMOD}${POST}_${ID}_pt20_njet   -b $BMOD -s $SMOD $MASS --xtitle "N(jets)";
        fi;
    done;
  done;
done
