#!/bin/bash
P=../plotting/plots/76X_220116/zTnP/
IN="mupog_v3"; OUT="mupog_v3/00_harvest"

MEAS="mu_SIP4 mu_SIP8 mu_LooseIdOnly mu_LooseFromIso "
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    case $M in
        mu_SIP4) MODS=" -s dvoigt -b bern3 --salt BWDCB --balt expo --balt bern4 --alt mass --alt tightTag --alt looseIso"; TIT='Muon S_{IP3D} < 4 + dxy/dz efficiency' ;; 
        mu_SIP8) MODS=" -s dvoigt -b bern3 --salt BWDCB --balt expo --balt bern4 --alt mass --alt tightTag --alt looseIso"; TIT='Muon S_{IP3D} < 8 + dxy/dz efficiency' ;; 
        mu_MiniIso04) MODS=" -s dvoigt -b bern3 --salt BWDCB --salt BWDCB2 --balt expo --balt bern4 --alt mass --alt tightTag"; TIT='Muon isolation efficiency' ;; 
        mu_LooseIdOnly) MODS=" -s dvoigt -b bern4 --salt BWDCB  --balt expo --balt bern3  --alt mass --alt tightTag --alt tightSIP --alt looseIso"; TIT='Muon Loose Id efficiency' ;; 
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        python tnpHarvest.py -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"   --rrange 0.955 1.035  --yrange 0.9 1.005 
    done
    python tnpHarvest.py -N ${M}_pt20 $OPTS $MODS --ytitle "$TIT" --xtit "#eta"   --rrange 0.975 1.025  --yrange 0.9 1.005 
    python tnpHarvest.py -N ${M}_pt20_vtx $OPTS $MODS --ytitle "$TIT" --xtit "N(vertices)"  --rrange 0.985 1.015  --yrange 0.9 1.005 
    if [[ "$M" == "mu_MiniIso04" ]]; then 
        python tnpHarvest.py -N ${M}_pt20_njet $OPTS $MODS --ytitle "$TIT" --xtit "N(jets)"  --rrange 0.981 1.019  --yrange 0.9 1.005 
    fi;
done

