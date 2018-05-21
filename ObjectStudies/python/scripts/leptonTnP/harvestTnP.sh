#!/bin/bash
P=../plotting/plots/76X_220116/zTnP/
IN="v4"; OUT="v4_harvest"

#python tnpHarvest.py mu_%s_%s_iso_barrel --idir ../plotting/plots/251115/zTnP/EcalCorr_v2/v4 --pdir ../plotting/plots/251115/zTnP/EcalCorr_v2/v4_harvest -N mu_iso_barrel -s MCTG -b bern3  --salt BWDCB2 --balt bern4  --doRatio

MEAS="el_iso mu_iso mu_idonly mu"
if [[ "$1" != "" ]]; then MEAS="$*"; fi
for M in $MEAS; do
    case $M in
        #el_iso) MODS=" -s MCTG -b bern3 --salt BWDCB2  --balt expo "; TIT='Electron isolation efficiency' ;;
        mu_iso) MODS=" -s MCTG -b bern3 --salt BWDCB2  --balt bern4 --balt expo  --alt mass "; TIT='Muon isolation efficiency' ;; 
        #mu_idonly)  MODS=" -s BWDCB2 -b bern3 --salt dvoigt --balt bern3  --balt expo "; TIT='Muon id efficiency' ;; 
        #mu)  MODS=" -s MCTG -b bern3 --salt BWDCB2 --salt dvoigt  --balt bern4 --balt expo"; TIT='Muon iso+id efficiency' ;; 
    esac;
    OPTS=" --doRatio --pdir ${P}/$OUT --idir ${P}/$IN   --rrange 0.945 1.035  --yrange 0.7 1.015 "; XTIT="p_{T} (GeV)"
    for BE in barrel endcap; do
        echo python tnpHarvest.py -N ${M}_${BE} $OPTS $MODS
        python tnpHarvest.py -N ${M}_${BE} $OPTS $MODS --ytitle "$TIT" --xtit "$XTIT"
    done
done

