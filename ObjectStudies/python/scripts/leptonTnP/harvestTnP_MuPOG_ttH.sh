#!/bin/bash
P=plots/80X/TnP
IN="mupog_ttH_v2.0"; OUT="$IN/00_harvest"

MEAS="mu_ttH_presel"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    RANGES_PT="--rrange 0.975 1.015  --yrange 0.9 1.005"
    RANGES_OTHER="--rrange 0.975 1.015  --yrange 0.9 1.005"
    case $M in
        mu_ttH_presel) MODS=" -s MCTG --salt dvoigt2 -b bern4 "; TIT="ttH presel. eff.";;
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
    python tnpHarvest.py -N ${M}_eta_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   $RANGES_OTHER
    python tnpHarvest.py -N ${M}_vtx_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  $RANGES_OTHER 
    python tnpHarvest.py -N ${M}_jet_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "N(jets)" $RANGES_OTHER
done

