#!/bin/bash

year=2017

if [ "${year}" == 2016 ]; then
    P=/afs/cern.ch/user/g/gpetrucc/w/TREES_80X_SOS_130716_TnP
    case $HOSTNAME in
        cmsco01*) P=/data/g/gpetrucc/TREES_80X_SOS_080217_TnP ;;
    esac;
else
    P=/eos/cms/store/user/bschneid/sos/TnP_trees_run10
fi

if [ "${year}" == 2016 ]; then
    PDIR="plots/80X/TnP_Moriond17/"
else
    PDIR="plots/94X/TnP_ICHEP18/"
fi
JOB="zee_sos_v5.0"
XBINS="[5,12.5,16,20,25,30,40,60]" #25,40,70,120]"
EBINS="[-2.5,-2.0,-1.52,-1.44,-1,0,1,1.44,1.52,2.0,2.5]"
VBINS="[0.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,24.5,26.5,28.5,30.5,34.5]"
DATA=""
if [ "${year}" == 2016 ]; then
    for L in B C D E F G; do DATA="$DATA $P/SingleElectron_Run2016${L}_23Sep2016/treeProducerTnP/tree.root"; done
    for V in 2 3; do DATA="$DATA $P/SingleElectron_Run2016H_PromptReco_v${V}/treeProducerTnP/tree.root"; done
else
    for L in B C D E F; do DATA="$DATA $P/SingleElectron_Run2017${L}_17Nov2017/treeProducerTnP/tree.root"; done
fi
MC="--refmc  $P/DYJetsToLL_M50/treeProducerTnP/tree.root"
PDS="$DATA $MC"

OPTS=" --doRatio  --pdir $PDIR/$JOB  "
OPTS="$OPTS -t tree  --mc-cut TnP_tag_mcMatchId&&TnP_probe_mcMatchId --mc-mass TnP_mass   "
OPTS="$OPTS -L $CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/susy-sos/functionsSOS.cc "
case $HOSTNAME in
    cmsphys10|cmsco01.cern.ch) OPTS="$OPTS -j 16 ";;
    lxplus*.cern.ch) OPTS="$OPTS -j 0" ;;
esac;

LAUNCHER="bash"
if [[ "$1" == "-q" ]]; then
    LAUNCHER="bsub -q $2 $PWD/runBatch $PWD $SCRAM_ARCH bash ";
    shift; shift;
fi;

if [[ "$1" == "all" ]]; then
    shift;
    for ID in SOS SOS_FO SOS_PR SOS_NM1_{ID,ISO,IP}; do # SOS_NM1_{Id,Iso,Ip} # SOS_003 SOS_NoIP SOS_presel SOS_FO SOS SOS_PR
        for SMOD in MCTG BWDCB2; do
            for BMOD in bern4 bern3; do
                for X in barrel endcap eta vtx; do
                    echo $LAUNCHER $0 $ID $SMOD $BMOD $X;
                done
            done
        done
    done
    exit
else
    if [[ "$4" == "" ]]; then echo "usage: $0 all || $0 ID SMOD  BMOD [ bin | all ]"; exit 1; fi;
        ID=$1; SMOD=$2; BMOD=$3; shift; shift; shift;
        bin=$1; shift;
    fi;

    if [[ "$1" != "" ]]; then OPTS="$OPTS $* "; fi

    MASS=" -m TnP_mass 80,70,115 "

    SOS_PRESEL_ID="TnP_probe_SUSYVLooseFall17"
    SOS_FO_ID="TnP_probe_SUSYVLooseFOFall17"
    SOS_SEL_ID="TnP_probe_SOSTightID2017"

    SOS_FO_IDCV="${SOS_FO_ID}   && TnP_probe_convVeto && TnP_probe_lostHits <= 1"
    SOS_SEL_IDCV="${SOS_SEL_ID} && TnP_probe_convVeto && TnP_probe_lostHits <= 1"
    SOS_FO_ISO="TnP_probe_relIso03*TnP_probe_pt < 20 + 300/TnP_probe_pt"
    SOS_SEL_ISO="TnP_probe_relIso03 < 0.5 && TnP_probe_relIso03*TnP_probe_pt < 5"
    SOS_PRESEL_IP="abs(TnP_probe_dz) < 1.0 && abs(TnP_probe_dxy) < 0.50"
    SOS_FO_IP=" ${SOS_PRESEL_IP} && abs(TnP_probe_sip3d) < 2.5 && abs(TnP_probe_ip3d) < 0.0175"
    SOS_SEL_IP="${SOS_PRESEL_IP} && abs(TnP_probe_sip3d) < 2.0 && abs(TnP_probe_ip3d) < 0.0100"
    #MET_PRESEL="met_pt < 40 && mt_2(met_pt,met_phi,TnP_tag_pt,TnP_tag_phi) < 50 && TnP_tag_relIso04 < 0.1"
    MET_PRESEL="met_pt < 40 && sqrt(2*met_pt*TnP_tag_pt*(1-cos(met_phi-TnP_tag_phi))) < 50"

    CDEN="TnP_tag_sip3d < 2.5 && TnP_tag_relIso04 < 0.1 "
    case $ID in
        SOS) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV && $SOS_SEL_IP" ; CDEN="$CDEN && $MET_PRESEL" ;;
        SOS_FO) NUM="$SOS_FO_IDCV && $SOS_FO_IP && $SOS_FO_ISO"; CDEN="$CDEN && $MET_PRESEL" ;;
        SOS_PR) NUM="$SOS_SEL_ISO && $SOS_SEL_ID && $SOS_SEL_IP" ;
            CDEN="$CDEN &&  $SOS_FO_IDCV && $SOS_FO_IP && $SOS_FO_ISO && $MET_PRESEL" ;;
        SOS_NM1_ID)  NUM="$SOS_SEL_IDCV" ; CDEN="$CDEN && $SOS_SEL_ISO  && $SOS_SEL_IP  && $MET_PRESEL"  ;;
        SOS_NM1_IP)  NUM="$SOS_SEL_IP" ;   CDEN="$CDEN && $SOS_SEL_IDCV && $SOS_SEL_ISO && $MET_PRESEL" ;;
        SOS_NM1_ISO) NUM="$SOS_SEL_ISO" ;  CDEN="$CDEN && $SOS_SEL_IDCV && $SOS_SEL_IP  && $MET_PRESEL"  ;;
        *) echo "Unknown ID $ID"; exit 2;;
    esac;

    DEN="$CDEN"; POST="";
    if [[ "$SMOD" == "MCTG" ]]; then OPTS="${OPTS} --fine-binning 100  "; fi

    function getcut() { case $1 in
    barrel) CUT="abs(TnP_probe_etaSc) < 1.479";;
    endcap) CUT="abs(TnP_probe_etaSc) > 1.479";;
    pt520) CUT="TnP_probe_pt > 5 && TnP_probe_pt < 20";;
    pt20)  CUT="TnP_probe_pt > 20";;
    *) echo "Unknown ptCut $1"; exit 3;
esac; }

case $bin in
    barrel|endcap) getcut $bin;
        python tnpEfficiency.py $PDS -d "$CUT && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_$bin -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;;
    eta_*) getcut ${bin/eta_};
        python tnpEfficiency.py $PDS -d "$CUT && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_$bin   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";;
    vtx_*) getcut ${bin/vtx_};
        python tnpEfficiency.py $PDS -d "$CUT && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_$bin   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";;
    all)
        for B in barrel endcap eta_pt520 vtx_pt520 eta_pt20 vtx_pt20; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    vtx)
        for B in vtx_pt520 vtx_pt20; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    eta)
        for B in eta_pt520 eta_pt20; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    be)
        for B in barrel endcap; do bash $0 $ID $SMOD $BMOD $B $*; done;;
    *)
        echo "I don't know the bin $bin"; exit 4;
esac;

#python tnpEfficiency.py $PDS -d "TnP_probe_pt > 20 && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta" ;
#python tnpEfficiency.py $PDS -d "TnP_probe_pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)" ;

if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
    MASS2=" -m TnP_mass 100,65,125"; POST="_mass";
    #echo "python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)" ;
    #echo "python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)" ;
fi
if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
    DEN="$CDEN && TnP_tag_pt > 25 && TnP_tag_relIso03 < 0.1"; POST="_tightTag";
    #echo "python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
    #echo "python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS  --xtitle "#eta" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)" ;

    DEN="$CDEN && SIP < 2"; POST="_tightSIP";
    #echo "python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
    #echo "python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta" ;
    #echo "python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)" ;
fi;
