#!/bin/bash
P=plots/94X/TnP_ICHEP18/
IN="mupog_jpsi_v1"; OUT="$IN/00_harvest"

MEAS="mu_Loose mu_Reco mu_LooseIdOnly"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    case $M in
        mu_Loose)  MODS=" -s JDGauss -b bern3  --salt JCB --balt bern4  --alt mass --alt sip4 --alt sep "; TIT='Muon Loose id + reco efficiency' ;; 
        #mu_Loose)  MODS=" -s JDGauss -b bern3  "; TIT='Muon Loose id + reco efficiency' ;; 
        mu_LooseIdOnly)  MODS=" -s JDGauss -b bern3 --salt JGauss --salt JCB --balt bern4 --balt expo --alt mass --alt sip4 --alt sep "; TIT='Muon Loose id efficiency' ;; 
        mu_Reco)   MODS=" -s JDGauss -b bern3 --salt JGauss --salt JCB --balt bern4 --balt expo --alt mass --alt sip4 --alt sep "; TIT='Muon reco efficiency' ;; 
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN  --rrange 0.97 1.005  --yrange 0.9 1.005 "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        python tnpHarvest.py -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"
    done
    python tnpHarvest.py -N ${M}_pt7 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"
    python tnpHarvest.py -N ${M}_pt7_vtx $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"
done

