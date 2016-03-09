#!/bin/bash

case $HOSTNAME in
cmsco01*) P=/data1/gpetrucc/TREES_HZZ4L_220116/2L/TnP ;;
*) P=/afs/cern.ch/user/g/gpetrucc/w/TREES_HZZ4L_220116/2L/TnP ;;
esac;

T=twoLeptonTreeProducerTnP/tree.root
PDIR="../plotting/plots/76X_220116/zTnP/"
JOB="v4"
LEPS="mu"
if [[ "$1" != "" ]]; then LEPS="$*"; fi
for Lep in $LEPS; do
    SALT=""; BALT="";
    case $Lep in
        el) ID=11; ETA=1.479; ISOWP=0.35; PD="SingleElectron"; 
            XBINS="[7,12,16,20,25,30,35,40,50,60,80]"
            #XBINS="[7,16,25,40]"
            ;;
        mu) ID=13; ETA=1.2;   ISOWP=0.35; PD="SingleMuon"; 
            XBINS="[5,10,13,16,20,25,30,35,40,50,60,80]"
            ;;
    esac;
    MC=$P/${Lep}/DYJetsToLL_LO_M50/$T
    DATA="$( ls $P/${Lep}/${PD}_Run2015D*/$T )"
    PDS="$DATA --refmc $MC"
    OPTS=" --doRatio  --pdir $PDIR/$JOB -j 8 " #--mcw vtxWeight2015(nVert)"
    #OPTS="${OPTS} --request mu_dvoigt_bern3_iso_barrel_bin1_ref "
    for BMOD in bern3 bern4 expo; do # 
        for SMOD in MCTG ; do  #  BWDCB dvoigt
            if [[ "$SMOD" == "MCTG" ]]; then OPTS="${OPTS} --fine-binning 100  "; fi
            NUM="TnP_l2_tightId && TnP_l2_relIsoAfterFSR < $ISOWP"
            if [[ "${Lep}" == "el" ]]; then
                XBINS1="[7,13,20,25,30,35,40,50,60,80]"
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)<$ETA"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS1 -N ${Lep}_${SMOD}_${BMOD}_barrel -b $BMOD -s $SMOD  ;
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)>$ETA"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS1 -N ${Lep}_${SMOD}_${BMOD}_endcap -b $BMOD -s $SMOD  ;
                #XBINS2="[7,10,13,15,20,25,30,35,40,50,60,80]"
                XBINS2="$XBINS"
                NUM="TnP_l2_tightId"
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)<$ETA && TnP_l2_relIsoAfterFSR < $ISOWP"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS2 -N ${Lep}_${SMOD}_${BMOD}_idonly_preIso_barrel -b $BMOD -s $SMOD  ;
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)>$ETA && TnP_l2_relIsoAfterFSR < $ISOWP"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS2 -N ${Lep}_${SMOD}_${BMOD}_idonly_preIso_endcap -b $BMOD -s $SMOD  ;
            else
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)<$ETA"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_barrel -b $BMOD -s $SMOD  ;
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)>$ETA"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_endcap -b $BMOD -s $SMOD  ;
                NUM="TnP_l2_tightId"
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)<$ETA"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_idonly_barrel -b $BMOD -s $SMOD  ;
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)>$ETA"
                #python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_idonly_endcap -b $BMOD -s $SMOD  ;
            fi
            NUM="TnP_l2_tightId && TnP_l2_relIsoAfterFSR < $ISOWP"
            DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)<$ETA && TnP_l2_tightId"
            python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_iso_barrel -b $BMOD -s $SMOD  ;
            DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)>$ETA && TnP_l2_tightId"
            python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_iso_endcap -b $BMOD -s $SMOD  ;
            if [[ "${BMOD}" == "bern3" && "${SMOD}" == "MCTG" ]]; then 
                MASS2=" -m TnP_mass 100,65,125 "
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)<$ETA && TnP_l2_tightId"
                python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_mass_iso_barrel -b $BMOD -s $SMOD $MASS2 ;
                DEN="abs(TnP_l2_pdgId)==$ID && abs(TnP_l2_eta)>$ETA && TnP_l2_tightId"
                python tnpEfficiency.py $PDS -d "$DEN" -n "$NUM" $OPTS --x-var TnP_l2_pt $XBINS -N ${Lep}_${SMOD}_${BMOD}_mass_iso_endcap -b $BMOD -s $SMOD $MASS2 ;
            fi
        done
    done;
done
