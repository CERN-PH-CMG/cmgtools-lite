#!/bin/bash

P=/afs/cern.ch/user/g/gpetrucc/w/TREES_80X_SOS_230616/TnP/Ele/
#case $HOSTNAME in
#cmsco01*) P=data1/gpetrucc/MUPOG_TnP_76X/ ;;
#*) exit 1; P=root://eoscms//eos/cms/store/group/phys_muon/TagAndProbe/76XtreeProduction/v41/ ;;
#esac;

PDIR="plots/80X/TnP/"
JOB="zee_v0.3"
XBINS="[5,12.5,20,25,40,70,120]"
EBINS="[-2.5,-2.0,-1.52,-1.44,-1,0,1,1.44,1.52,2.0,2.5]"
VBINS="[0.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,22.5,24.5,26.5,28.5,30.5,34.5]"
DATA=$P/SingleElectron_Run2016B_PromptReco_v2/treeProducerTnP/tree.root
MC="--refmc  $P/DYJetsToLL_M50_LO/treeProducerTnP/tree.root"
PDS="$DATA $MC"

OPTS=" --doRatio  --pdir $PDIR/$JOB -j 8 " #--mcw vtxWeight2015(nVert)"
OPTS="$OPTS -t tree  -m TnP_mass 80,70,115 --mc-cut TnP_tag_mcMatchId&&TnP_probe_mcMatchId --mc-mass TnP_mass   "
#if [[ "$1" != "" ]]; then SEL=$1; OPTS="$OPTS --reqname el_${1/el_/} "; shift; fi
if [[ "$1" != "" ]]; then OPTS="$OPTS $* "; shift; fi
MASS=" -m TnP_mass 80,70,115 "

SOS_PRESEL_ID="TnP_probe_eleMVASpring15_VLooseIdEmu"
SOS_PRESEL_IDCV="TnP_probe_eleMVASpring15_VLooseIdEmu && TnP_probe_convVeto && TnP_probe_lostHits == 0"
SOS_PRESEL_ISO="TnP_probe_relIso04*TnP_probe_pt < 10"
SOS_PRESEL_IP="abs(TnP_probe_dz) < 1.0 && abs(TnP_probe_dxy) < 0.50 && abs(TnP_probe_sip3d) < 8"
SOS_SEL_ISO="TnP_probe_relIso03 < 0.5 && (TnP_probe_relIso03*TnP_probe_pt < 5 || TnP_probe_relIso03 < 0.1) && $SOS_PRESEL_ISO"
SOS_SEL_ID="TnP_probe_eleMVASpring15_HZZ"
SOS_SEL_IDCV="TnP_probe_eleMVASpring15_HZZ && TnP_probe_convVeto && TnP_probe_lostHits == 0"
SOS_SEL_IP="abs(TnP_probe_dz) < 0.01 && abs(TnP_probe_dxy) < 0.01 && abs(TnP_probe_sip3d) < 8"
SOS_SEL_IP003="abs(TnP_probe_dz) < 0.03 && abs(TnP_probe_dxy) < 0.03 && abs(TnP_probe_sip3d) < 8"
SOS_FO_ID="eleWPVVL(TnP_probe_pt,TnP_probe_etaSc,TnP_probe_mvaIdSpring15)"
#for ID in SOS SOS_{Id,Ip,Iso}; do #  SOSPresel2 SOSPresel2_{Id,Iso,Ip}NM1; do
for ID in SOS_PR_2; do #  SOS_presel SOS_Ip SOS_Iso SOS_IdCV_tkIsoSip4
  #if [[ "$SEL" != "" ]] && echo $SEL | grep -q -v $ID; then continue; fi
  CDEN="TnP_tag_sip3d < 4 "
  case $ID in
      SOS) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV && $SOS_SEL_IP" ; CDEN="$CDEN" ;;
      SOS_003) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV && $SOS_SEL_IP003" ; CDEN="$CDEN" ;;
      SOS_NoIP) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV" ; CDEN="$CDEN" ;;
      SOS_presel) NUM="$SOS_PRESEL_ISO && $SOS_PRESEL_IDCV && $SOS_PRESEL_IP" ; CDEN="$CDEN" ;;
      SOS_PR) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV && $SOS_SEL_IP" ; 
              CDEN="$CDEN &&  $SOS_PRESEL_IDCV && $SOS_PRESEL_IP && $SOS_FO_ID" ;;
      SOS_PR_1) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV && $SOS_SEL_IP" ; 
                CDEN="$CDEN &&  $SOS_SEL_IDCV && $SOS_PRESEL_IP" ;;
      SOS_PR_2) NUM="$SOS_SEL_ISO && $SOS_SEL_IDCV && $SOS_SEL_IP" ; 
                CDEN="$CDEN &&  $SOS_PRESEL_IDCV && $SOS_PRESEL_IP" ;;
      #SOS_Id)  NUM="$SOS_SEL_ID" ; CDEN="$CDEN && TnP_probe_trkIso03 < max(0.5*TnP_probe_pt,5) " ;;
      SOS_Ip)  NUM="$SOS_SEL_IP" ; CDEN="$CDEN && $SOS_SEL_IDCV && $SOS_SEL_ISO" ;;
      SOS_Iso) NUM="$SOS_SEL_ISO && $SOS_SEL_IP" ; CDEN="$CDEN && $SOS_SEL_IDCV && $SOS_SEL_IP" ;;
      SOS_IdCV_tkIsoSip4)  NUM="$SOS_SEL_IDCV" ; CDEN="$CDEN && TnP_probe_trkIso045 < 0.2*TnP_probe_pt && abs(TnP_probe_sip3d) < 4" ;;
      #SOS_IsoIp) NUM="$SOS_SEL_ISO && $SOS_SEL_IP" ; CDEN="$CDEN && $SOS_SEL_IDCV";
  esac;
  for SMOD in MCTG BWDCB; do # dvoigt BWDCB  MCTG BWDCB
    #if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
    for BMOD in bern4 bern3; do # bern3 bern4 expo #
    #if [[ "$SEL" != "" ]] && echo $SEL | grep -q "_" && echo $SEL | grep -q -v $BMOD; then continue; fi
    if [[ "$SMOD" == "MCTG" ]]; then OPTS="${OPTS} --fine-binning 100  "; fi
        DEN="$CDEN"; POST=""
        python tnpEfficiency.py $PDS -d "abs(TnP_probe_etaSc)<1.479 && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)" ;
        python tnpEfficiency.py $PDS -d "abs(TnP_probe_etaSc)>1.479 && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
        #python tnpEfficiency.py $PDS -d "TnP_probe_pt > 20 && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
        continue
        #python tnpEfficiency.py $PDS -d "TnP_probe_pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        python tnpEfficiency.py $PDS -d "TnP_probe_pt > 5 && TnP_probe_pt < 20 && $DEN" -n "$NUM" $OPTS --x-var TnP_probe_eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
        python tnpEfficiency.py $PDS -d "TnP_probe_pt > 5 && TnP_probe_pt < 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
        if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
            MASS2=" -m TnP_mass 100,65,125"; POST="_mass"
            #python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS2 --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
            #python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS2  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS2 --xtitle "N(vertices)";
        fi
        if [[ "$SMOD" == "MCTG" && "$BMOD" == "bern4" ]]; then
            DEN="$CDEN && TnP_tag_pt > 25 && TnP_tag_relIso03 < 0.1"; POST="_tightTag"
            #python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";
            #python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 5 && pt < 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt520_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";

            DEN="$CDEN && SIP < 2"; POST="_tightSIP"
            #python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)<1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_barrel -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "abs(TnP_probe_eta)>1.2 && $DEN" -n "$NUM" $OPTS --x-var pt $XBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_endcap -b $BMOD -s $SMOD $MASS --xtitle "p_{T} (GeV)";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var eta $EBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20   -b $BMOD -s $SMOD $MASS  --xtitle "#eta";
            #python tnpEfficiency.py $PDS -d "pt > 20 && $DEN" -n "$NUM" $OPTS --x-var nVert $VBINS -N el_${SMOD}_${BMOD}${POST}_${ID}_pt20_vtx   -b $BMOD -s $SMOD $MASS --xtitle "N(vertices)";

        fi;
    done;
  done;
done
