#!/bin/bash

#case $HOSTNAME in
#cmsco01*) exit 1; P=/data1/gpetrucc/MUPOG_TnP_76X/ ;;
#cmsphys10*) P=/data1/g/gpetrucc/MuTnP80X/ ;;
#*) exit 1; P=root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/ ;;
#esac;
P=root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/Run2016/HIPs/810_pre9/

PDIR="plots/80X/TnP/"
JOB="mupog_tracking_hip_v0/mc_1p2"
TWOBINS="[0,1.2,2.4]"
EBINS="[-2.4,-2.1,-1.6,-1.2,-0.9,-0.6,-0.3,0.3,0.6,0.9,1.2,1.6,2.1,2.4]"
VBINS="[0.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,24.5,26.5,28.5,30.5,34.5]"
#DATA="$P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run271036to273730_NotCompleted.root"
#DATA="$DATA $P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run273731_to_274240_IncludingMissingLumi_Completed.root"
#DATA="$DATA $P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274241to274421.root"
#DATA="$DATA $P/TnPTree_80X_Run2016B_v2_GoldenJSON_Run274422to274443.root"
#MC=$(for I in $(seq 1 7); do echo -n " --refmc $P/TnPTree_80X_DYLL_M50_MadGraphMLM_part${I}.root "; done)
DATA="$P/tnpZ_MC_PU25ns_81X_mcRun2_asymptotic_v2_hip1p2-v1.root"
MC="--refmc $P/tnpZ_MC_PU25ns_81X_mcRun2_asymptotic_v2_hip1p2_mtoff-v1.root"
#DATA=$(for I in $(seq 1 7); do echo $P/TnPTree_v41_76X_RunD_part${I}_withEAMiniIso.root; done)
#MC=$(for I in $(seq 1 2); do echo " --refmc $P/TnPTree_76X_DYLL_M50_MadGraphMLM_part${I}_withEAMiniIso.root"; done)
PDS="$DATA $MC"
#PDS=$(echo "$PDS" | sed 's/.root/_withEAMiniIso.root/g')
OPTS=" --doRatio  --pdir $PDIR/$JOB -j 5 " #--mcw vtxWeight2015(nVert)"
OPTS="$OPTS -t tpTreeSta/fitter_tree  --mc-cut mcTrue --mc-mass mass   "
OPTS="$OPTS -s voigt -b expo "
MASS="  -m mass 40,60,130 "
CDEN="tag_IsoMu22 && tag_pt > 22 && outerValidHits "
for match in dr03e03; do
    for tk in tk0 tk; do
        for PostFix in '' _NoZ; do

            YTIT="Raw efficiency"
            if echo "X$PostFix" | grep -q "_No"; then YTIT="Fake match prob."; fi;
            case $match in
                dr03e03) NUM="${tk}_deltaR${PostFix} < 0.3" ;;
                *) echo "Matching $match not defined"; exit 1;; 
            esac;
            python tnpEfficiency.py $PDS -d "pt > 15 && $CDEN"                 -n "$NUM" $OPTS --x-var abseta $TWOBINS      -N mu_${match}_${tk}${PostFix}_pt15_two      $MASS --xtitle "|#eta|" --ytitle "$YTIT";
            python tnpEfficiency.py $PDS -d "pt > 15 && $CDEN"                 -n "$NUM" $OPTS --x-var eta $EBINS           -N mu_${match}_${tk}${PostFix}_pt15_eta      $MASS --xtitle "#eta"  --ytitle "$YTIT";
            python tnpEfficiency.py $PDS -d "pt > 15 && $CDEN && abseta < 2.4" -n "$NUM" $OPTS --x-var tag_nVertices $VBINS -N mu_${match}_${tk}${PostFix}_pt15eta24_vtx $MASS --xtitle "N(vertices)" --ytitle "$YTIT";
        done;
    done;
done
