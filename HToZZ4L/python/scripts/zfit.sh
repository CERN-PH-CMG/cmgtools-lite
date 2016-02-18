#!/bin/bash
T=twoLeptonTreeProducer/tree.root
EXTRA="-l 2.46 -s Z-DCB"

if [[ "$1" == "" ]]; then echo "usage: $0 what"; exit 1; fi;

case $1 in
*-calib)   O=../plotting/plots/76X_220116/zfits/2015_all/calib ;;
*-calib2)   O=../plotting/plots/76X_220116/zfits/2015_all/calib2 ;;
*-calib3)   O=../plotting/plots/76X_220116/zfits/2015_all/calib3 ;;
*-uncalib) O=../plotting/plots/76X_220116/zfits/2015_all/uncalib ;;
esac;

P=/afs/cern.ch/user/g/gpetrucc/w/TREES_HZZ4L_220116/2L/Z/
if hostname | grep -q cmsco01; then
    P=/data1/gpetrucc/TREES_HZZ4L_220116/2L/Z
fi
case $1 in
mu*-calib) P=${P}/KaMuCa    ;;
mu*-calib2) P=${P}/KaMuCa_SmearNoEbE  ;;
mu*-calib3) P=${P}/KaMuCa_V2_pre1  ;;
el*-calib) P=${P}/ShervinV1 ;;
el*-calib2) P=${P}/ShervinV2 ;;
esac;
case $1 in
mu*) PD=DoubleMuon; SD=SingleMuon ;;
el*) PD=DoubleEG; SD=SingleElectron ;;
esac;

case $1 in
mu-x-*) CUTS="$(echo Zmm-B0E{1,2,3})" ;; 
el-132-*) CUTS="$(echo Zee-dm132)" ;;
el-r9-*) CUTS="$(echo Zee-{BB,EE}_{high,notHigh}R9)" ;;
mu-*) CUTS="$(echo Zmm-{BB,NonBB,BE,EE})" ;; 
el-*) CUTS="$(echo Zee-{BB,NonBB,BE,EE})" ;;
esac

case $1 in
*-2d-*)
    EXTRA="${EXTRA} -m 2D"
    O=${O}/fit2d
    ;;
mu-ebe-*)
    CUTS="Zmm"
    EXTRA="${EXTRA} -m 1D_DMSlices  $P/${SD}_Run2015*/$T "
    O=${O}/dmSlices
    ;;
mu-ebe2-*)
    CUTS="Zmm-BB Zmm-EE"
    EXTRA="${EXTRA} -m 1D_DMSlices"
    O=${O}/dmSlices
    ;;
mu-ht-*)
    CUTS="Zmm-BB Zmm-NonBB"
    EXTRA="${EXTRA} -m 1D_HTSlices  $P/${SD}_Run2015*/$T "
    O=${O}/htSlices
    ;;
el-ebe-*)
    CUTS="Zee"
    EXTRA="${EXTRA} -m 1D_DMSlices  $P/${SD}_Run2015*/$T "
    O=${O}/dmSlices
    ;;
el-ht-*)
    CUTS="ZeeBB Zee-NonBB"
    EXTRA="${EXTRA} -m 1D_HTSlices  $P/${SD}_Run2015*/$T "
    O=${O}/htSlices
    ;;
el-pteta-*)
    CUTS="Zee"
    EXTRA="${EXTRA} -m 1D_PtEtaSlices   $P/${SD}_Run2015*/$T "
    O=${O}/ptEtaSlices
    ;;
mu-pteta-*)
    CUTS="Zmm"
    EXTRA="${EXTRA} -m 1D_PtEtaSlices   $P/${SD}_Run2015*/$T  "
    O=${O}/ptEtaSlices
    ;;
esac

shift;
for C in $CUTS; do
    echo "python zFitter.py $P/${PD}_Run2015*/$T -r $P/DYJetsToLL_LO_M50/$T --pdir $O -n $C -c $C $EXTRA $* "
done


