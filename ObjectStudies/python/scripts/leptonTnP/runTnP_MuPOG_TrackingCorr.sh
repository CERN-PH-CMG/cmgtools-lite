#!/bin/bash
PDIR="plots/80X/TnP/"
JOB="$1"
test -d $PDIR/$1 || exit 1;
for match in dr03e03; do
    for tk in tk0 tk; do
        OPTS=" --doRatio  --idir $PDIR/$JOB  " 
        if [[ "$tk" == "tk0" ]]; then OPTS="$OPTS --yrange 0.936 1.0049 --rrange 0.968 1.0019"; else OPTS="$OPTS --yrange 0.936 1.0049 --rrange 0.968 1.0019"; fi; 
        for x in pt15_two pt15_eta pt15eta24_vtx pt15eta24_ilumi; do
            echo python tnpTrackingCorrection.py $OPTS -N mu_${match}_${tk}_corr_$x ${tk}_corr ${tk} ${tk}_NoZ 
        done;
    done;
done
