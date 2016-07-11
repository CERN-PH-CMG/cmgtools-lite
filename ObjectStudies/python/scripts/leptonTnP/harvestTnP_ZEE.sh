#!/bin/bash
P=plots/80X/TnP
IN="zee_v0.3"; OUT="$IN/00_harvest"

MEAS="el_SOS el_SOS_presel el_SOS_Ip el_SOS_Iso el_SOS_IdCV_tkIsoSip4"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    RANGES_PT="--rrange 0.955 1.035  --yrange 0.9 1.005"
    RANGES_OTHER="--rrange 0.975 1.025  --yrange 0.9 1.005"
    MAIN="tnpHarvest.py"
    case $M in
        el_SOS|el_SOS_003|el_SOS_NoIP|el_SOS_PR_[12]) MODS=" -s MCTG -b bern4 --salt BWDCB --balt bern3 "; TIT="${M/el_/} efficiency"; 
                RANGES_PT="   --rrange 0.60 1.175  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.60 1.175  --yrange 0.0 1.005"; ;; 
        el_SOS_presel) MODS=" -s MCTG -b bern4 --salt BWDCB --balt bern3 "; TIT='SOS presel. efficiency'; 
                RANGES_PT="   --rrange 0.60 1.175  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.60 1.175  --yrange 0.0 1.005"; ;; 
        el_SOS_Ip) MODS=" -s MCTG -b bern4 --salt BWDCB --balt bern3 "; TIT='SOS IP efficiency'; 
                RANGES_PT="   --rrange 0.775 1.075  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.775 1.075  --yrange 0.0 1.005"; ;; 
        el_SOS_Iso) MODS=" -s MCTG -b bern4 --salt BWDCB --balt bern3 "; TIT='SOS Iso efficiency'; 
                RANGES_PT="   --rrange 0.775 1.075  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.775 1.075  --yrange 0.0 1.005"; ;; 
        el_SOS_IdCV_tkIsoSip4) MODS=" -s MCTG -b bern4 --salt BWDCB --balt bern3 "; TIT='SOS ID efficiency'; 
                RANGES_PT="   --rrange 0.775 1.075  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.775 1.075  --yrange 0.0 1.005"; ;; 
        el_SOS_comb)
                MODS=" SOS_comb  SOS_IdCV_tkIsoSip4 SOS_Iso SOS_Ip  "; TIT='SOS comb. efficiency'; 
                MAIN="tnpCombiner.py"; IN=$OUT;
                RANGES_PT="   --rrange 0.60 1.175  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.60 1.175  --yrange 0.0 1.005"; ;; 
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        python $MAIN -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"  $RANGES_PT 
        if echo $M | grep -q SOS; then
            python $MAIN -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT" --xrange 0 25 --postfix _zoom $RANGES_PT
        fi
    done
    continue
    python $MAIN -N ${M}_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
    python $MAIN -N ${M}_pt20_vtx $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER 
    if [[ "$M" == "mu_SOS" ]]; then
        python $MAIN -N ${M}_pt520 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
        python $MAIN -N ${M}_pt520_vtx $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER
    fi;
    if [[ "$M" == "mu_MiniIso04" ]]; then 
        python $MAIN -N ${M}_pt20_njet $OPTS $MODS --ytitle "$TIT" --xtit "N(jets)" $RANGES_OTHER
    fi;
done

