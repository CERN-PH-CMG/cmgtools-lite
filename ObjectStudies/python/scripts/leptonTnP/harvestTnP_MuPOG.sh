#!/bin/bash
P=plots/80X/TnP
IN="mupog_v0"; OUT="$IN/00_harvest"

MEAS="mu_SOS"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    RANGES_PT="--rrange 0.955 1.035  --yrange 0.9 1.005"
    RANGES_OTHER="--rrange 0.975 1.025  --yrange 0.9 1.005"
    case $M in
        #mu_SIP4) MODS=" -s dvoigt -b bern3 --salt BWDCB --balt expo --balt bern4 --alt mass --alt tightTag --alt looseIso"; TIT='Muon S_{IP3D} < 4 + dxy/dz efficiency' ;; 
        #mu_SIP8) MODS=" -s dvoigt -b bern3 --salt BWDCB --balt expo --balt bern4 --alt mass --alt tightTag --alt looseIso"; TIT='Muon S_{IP3D} < 8 + dxy/dz efficiency' ;; 
        #mu_MiniIso04) MODS=" -s dvoigt -b bern3 --salt BWDCB --salt BWDCB2 --balt expo --balt bern4 --alt mass --alt tightTag"; TIT='Muon isolation efficiency' ;; 
        #mu_LooseIdOnly) MODS=" -s dvoigt -b bern4 --salt BWDCB  --balt expo --balt bern3  --alt mass --alt tightTag --alt tightSIP --alt looseIso"; TIT='Muon Loose Id efficiency' ;; 
        mu_SOS) MODS=" -s MCTG -b bern4 "; TIT='SOS efficiency'; 
                RANGES_PT="--rrange 0.925 1.075  --yrange 0.5 1.005";
                RANGES_OTHER="--rrange 0.875 1.075  --yrange 0.7 1.005"; ;; 
        mu_SOS_003) MODS=" -s MCTG -b bern4 "; TIT='SOS efficiency'; 
                RANGES_PT="--rrange 0.925 1.075  --yrange 0.5 1.005";
                RANGES_OTHER="--rrange 0.875 1.075  --yrange 0.7 1.005"; ;; 
        mu_SOS_PR) MODS=" -s MCTG -b bern4 "; TIT='SOS prompt rate'; 
                RANGES_PT="--rrange 0.925 1.075  --yrange 0.5 1.005";
                RANGES_OTHER="--rrange 0.875 1.075  --yrange 0.7 1.005"; ;; 
        mu_ttHPresel) MODS=" -s MCTG -b bern4 "; TIT="ttH presel. eff.";;
        mu_LooseIdOnly) MODS=" -s dvoigt -b bern4 "; TIT="Loose id.";;
        mu_Loose) MODS=" -s dvoigt -b bern4 "; TIT="Loose id.";;
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        python tnpHarvest.py -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"  $RANGES_PT 
        if echo $M | grep -q SOS; then
            python tnpHarvest.py -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"  $RANGES_PT --xrange 0 25 --postfix _zoom
        fi
    done
    python tnpHarvest.py -N ${M}_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
    python tnpHarvest.py -N ${M}_pt20_vtx $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER 
    if [[ "$M" == "mu_SOS" ]]; then
        python tnpHarvest.py -N ${M}_pt520 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
        python tnpHarvest.py -N ${M}_pt520_vtx $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER
    fi;
    if [[ "$M" == "mu_MiniIso04" ]]; then 
        python tnpHarvest.py -N ${M}_pt20_njet $OPTS $MODS --ytitle "$TIT" --xtit "N(jets)" $RANGES_OTHER
    fi;
done

