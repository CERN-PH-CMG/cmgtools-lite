#!/bin/bash
P=plots/94X/TnP_ICHEP18
IN="zee_sos_v5.0"; OUT="$IN/00_harvest"

MEAS="SOS SOS_PR SOS_NM1_ID SOS_NM1_ISO SOS_NM1_IP SOS_FO"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    RANGES_PT="--rrange 0.955 1.035  --yrange 0.9 1.005"
    RANGES_OTHER="--rrange 0.975 1.025  --yrange 0.9 1.005"
    MAIN="tnpHarvest.py"
    case $M in
        SOS_comb)
                MAIN="tnpCombiner.py"; IN=$OUT;
                MODS=" SOS_comb  SOS_NM1_ID SOS_NM1_ISO SOS_NM1_IP  "; TIT='SOS comb. efficiency';
                RANGES_PT="   --rrange 0.60 1.175  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.60 1.175  --yrange 0.0 1.005"; ;;
        SOS*) MODS=" -s MCTG -b bern4 --salt BWDCB2 --balt bern3 "; TIT="$(echo $M | sed 's/_/ /g') efficiency";
                RANGES_PT="   --rrange 0.60 1.175  --yrange 0.0 1.005";
                RANGES_OTHER="--rrange 0.60 1.175  --yrange 0.0 1.005"; ;;
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        python $MAIN -N el_${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"  $RANGES_PT
        #if echo $M | grep -q SOS; then
        #    python $MAIN -N el_${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT" --xrange 0 25 --postfix _zoom $RANGES_PT
        #fi
    done
    continue
    #python $MAIN -N el_${M}_eta_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
    #python $MAIN -N el_${M}_vtx_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER
    #if echo $M | grep -q SOS; then
        python $MAIN -N el_${M}_eta_pt520 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
        python $MAIN -N el_${M}_vtx_pt520 $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER
    #fi;
done

