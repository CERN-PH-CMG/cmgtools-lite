#!/bin/bash
PDIR="plots/80X/TnP/"
JOB="mupog_tracking_hip_v0/mc_1p2"
OPTS=" --doRatio  --idir $PDIR/$JOB  " 
for match in dr03e03; do
    for tk in tk0 tk; do
        for x in pt15_two pt15_eta pt15eta24_vtx; do
            python tnpTrackingCorrection.py $OPTS -N mu_${match}_${tk}_corr_$x ${tk}_corr ${tk} ${tk}_NoZ
        done;
    done;
done
