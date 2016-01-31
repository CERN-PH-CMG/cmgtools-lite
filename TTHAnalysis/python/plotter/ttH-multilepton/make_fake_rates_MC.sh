################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/lepton-mca-frstudies.txt object-studies/lepton-perlep.txt  "
T="/afs/cern.ch/work/p/peruzzi/tthtrees/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA_1lepFR/"
if hostname | grep -q cmsphys10; then
    T="/data/p/peruzzi/TREES_74X_140116_MiniIso_tauClean_Mor16lepMVA_1lepFR"
elif hostname | grep -q vinavx0.cern.ch; then
    T="/home/gpetrucc/SKIM_TREES_140116_1lepFR"
fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PBASE="plots/74X/lepMVA/v4.5"

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

what=$1;
if [[ "$what" == "" ]]; then what=mvaTTH-test-QCD; fi;
case $what in
    mvaTTH-test-QCD)
        WP=060ibf30E; if [[ "$2" != "" ]]; then WP=$2; fi;
        XVar="mvaPt"; Num="mvaPt_$WP"; MuIdDen=0; EleRecoPt=7;
        case $WP in
            000i) SelDen="-A pt20 den 'LepGood_sip3d < 8'";; 
            030i) SelDen="-A pt20 den 'LepGood_sip3d < 8'";;
            060i) SelDen="-A pt20 den 'LepGood_sip3d < 8'";;
            060iB) SelDen="-A pt20 den 'LepGood_sip3d < 8 && LepGood_jetBTagCSV < 0.97'"; Num="mvaPt_${WP%%B*}";;
            060ib) SelDen="-A pt20 den 'LepGood_sip3d < 8 && LepGood_jetBTagCSV < 0.89'"; Num="mvaPt_${WP%%b*}";;
            060ibf30) SelDen="-A pt20 den 'LepGood_sip3d < 8 && LepGood_jetBTagCSV < 0.89 && (LepGood_mvaTTH > 0.6 || LepGood_jetPtRatiov2 > 0.3)'"; Num="mvaPt_${WP%%b*}";;
            060ibf30E) SelDen="-A pt20 den 'LepGood_sip3d < 8 && LepGood_jetBTagCSV < 0.89 && (LepGood_mvaTTH > 0.6 || LepGood_jetPtRatiov2 > 0.3) && (LepGood_idEmu || LepGood_pt*if3(LepGood_mvaTTH>0.60&&LepGood_mediumMuonId>0, 1.0, 0.85/LepGood_jetPtRatiov2) < 30)'"; Num="mvaPt_${WP%%b*}";;
            060ibE10) SelDen="-A pt20 den 'LepGood_sip3d < 8 && LepGood_jetBTagCSV < 0.89'"; Num="mvaPt_${WP%%b*}"; EleRecoPt=10;;
            060) SelDen="-A pt20 den 'LepGood_sip3d < 8'"; MuIdDen=1;;
        esac
        B0="$BASE -P $T ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        B0="$B0 --legend=TR  --yrange 0 0.25 --showRatio --ratioRange 0.0 1.99 "
        JetDen="-A pt20 mll 'minMllAFAS > 12 || minMllAFAS <= 0'"
        CommonDen="${JetDen} ${SelDen}  "
        MuDen="${CommonDen} -A pt20 den 'LepGood_mediumMuonId>=${MuIdDen} && LepGood_pt > 5'   --xcut 10 999"
        #ElDen="${CommonDen} -I mu -A pt20 den 'LepGood_convVeto && LepGood_tightCharge >= 2 && LepGood_lostHits == 0 && LepGood_pt > ${EleRecoPt}' --xcut 10 999"
        ElDen="${CommonDen} -I mu -A pt20 den 'LepGood_convVeto && LepGood_lostHits == 0 && LepGood_pt > ${EleRecoPt}' --xcut 10 999"
        for BVar in bAny bMedium; do 
        RVar=30; 
        case $BVar in
            bAny)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar ' " ;;
            bVeto)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV < 0.605' " ;;
            bLoose)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.605' " ;;
            bMedium)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.89' " ;;
            bTight) BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.97' " ;;
        esac;
        Me="wp${WP}_rec${RVar}_${BVar}"

        MuFakeVsPt="$MuDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BZ $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        BZ=${B0/yrange 0 0.25/yrange 0 0.15}; 
        echo "( $BZ $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BZ $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #AwayJet pt variations
        MuFakeVsPt="$MuDen --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        echo "( $B0 $MuFakeVsPt -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet b-tag
        MuFakeVsPt="$MuDen --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        BZ=${BZ/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $MuFakeVsPt -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BZ $MuFakeVsPt -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        MuFakeVsPt="$MuDen --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_SSbt_black " 
        ElFakeVsPt="$ElDen --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_SSbt_black " 
        echo "( $BZ $MuFakeVsPt -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BZ $MuFakeVsPt -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # TTbar by composition
        MuFakeVsPt="$MuDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        BZ=${B0/ratioRange 0.31 1.69/ratioRange 0.77 1.29}; BZ=${BZ/yrange 0 0.4/yrange 0 0.15}; BZ=${BZ/legend=TL/legend=TR}
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        BZ=${B0/ratioRange 0.31 1.69/ratioRange 0.67 1.39}; BZ=${BZ/yrange 0 0.4/yrange 0 0.25}; BZ=${BZ/legend=TL/legend=TR}
        echo "( $BZ $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $BZ $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #QCD by flavour
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        BZ=${B0/yrange 0 0.25/yrange 0 0.15}; 
        echo "( $BZ $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/el_ftt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        # TT by flavour
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ ${MuFakeVsPt/TT_red/QCDMu_red} -p QCDMu_red,QCDMu_bjets,QCDMu_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        BZ=${B0/yrange 0 0.25/yrange 0 0.15}; 
        echo "( $BZ ${ElFakeVsPt/TT_red/QCDEl_red} -p QCDEl_red,QCDEl_bjets,QCDEl_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"

        # HLT
        MuFakeVsPt="$MuDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu.* -o $PBASE/$what/mu_hlt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BZ $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu.* -o $PBASE/$what/mu_hlt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        BZ=${B0/yrange 0 0.25/yrange 0 0.15}; 
        echo "( $BZ $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El.* -o $PBASE/$what/el_hlt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BZ $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El.* -o $PBASE/$what/el_hlt_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT
        MuFakeVsPt="$MuDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp QCDMu_red_pt8 " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp QCDEl_red_pt12 " 
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $MuFakeVsPt -p QCDMu_red,QCDMu_red_pt.*,QCDMu_red_Mu.* -o $PBASE/$what/mu_hltpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BZ $MuFakeVsPt -p QCDMu_red,QCDMu_red_pt.*,QCDMu_red_Mu.* -o $PBASE/$what/mu_hltpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        BZ=${B0/yrange 0 0.25/yrange 0 0.25}; 
        echo "( $BZ $ElFakeVsPt -p QCDEl_red,QCDEl_red_pt.*,QCDEl_red_El.* -o $PBASE/$what/el_hltpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BZ $ElFakeVsPt -p QCDEl_red,QCDEl_red_pt.*,QCDEl_red_El.* -o $PBASE/$what/el_hltpt_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"


        MuFakeVsPt="$MuDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_mid' --sp TT_red " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_mid' --sp TT_red " 
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $MuFakeVsPt -p 'TT_red,TT_pt(8|17)_red'  -o $PBASE/$what/mu_ttpt_${Me}_eta_00_12_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        echo "( $BZ $ElFakeVsPt -p 'TT_red,TT_pt(8|12|23)_red' -o $PBASE/$what/el_ttpt_${Me}_eta_00_15_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"

        #MuFakeVsPt="$MuDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        #ElFakeVsPt="$ElDen ${BDen} --sP 'ptJI_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        #BZ=${B0/yrange 0 0.25/yrange 0 0.10}; 
        #BZ=${BZ/_1lepFR/}; # Important
        #echo "( $BZ $MuFakeVsPt -p 'TT_red,Z3l_red'  -o $PBASE/$what/mu_z3l_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $BZ $MuFakeVsPt -p 'TT_red,Z3l_red'  -o $PBASE/$what/mu_z3l_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #BZ=${B0/yrange 0 0.25/yrange 0 0.20}; 
        #BZ=${BZ/_1lepFR/}; # Important
        #echo "( $BZ $ElFakeVsPt -p 'TT_red,Z3l_red' -o $PBASE/$what/el_z3l_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        #echo "( $BZ $ElFakeVsPt -p 'TT_red,Z3l_red' -o $PBASE/$what/el_z3l_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        done;

        ;;
    mvaTTH-prod)
        WP=06i; if [[ "$2" != "" ]]; then WP=$2; fi;
        case $WP in
            06i)  SelDen="-A pt20 den '(LepGood_relIso03 < 0.4) && LepGood_sip3d < 6                               && (LepGood_mvaTTH>${WP/i*/} || LepGood_jetPtRatio > 0.5*0.85)'"; Num="mvaTTH_${WP/i*/i}"; MuIdDen=0;;
            06ib) SelDen="-A pt20 den '(LepGood_relIso03 < 0.4) && LepGood_sip3d < 6 && LepGood_jetBTagCSV < 0.814 && (LepGood_mvaTTH>${WP/i*/} || LepGood_jetPtRatio > 0.5*0.85)'"; Num="mvaTTH_${WP/i*/i}"; MuIdDen=0;;
        esac
        B0="$BASE -P $T  ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        B0="$B0  --legend=TL  --yrange 0 0.4 --showRatio --ratioRange 0.31 1.69 --xcut 10 999 "
        JetDen="-A pt20 jet 'LepGood_awayJet_pt > 40 && minMllAFAS > 12'"
        CommonDen="${JetDen} ${SelDen}"
        MuDen="${CommonDen} -A pt20 den 'LepGood_mediumMuonId>=${MuIdDen}' -A pt20 mc 'LepGood_pt > 5' "
        ElDen="${CommonDen} -I mu -A pt20 den 'LepGood_convVeto && LepGood_tightCharge >= 2 && LepGood_lostHits == 0'  -A pt20 mc 'LepGood_pt > 7'"
        MuFakeVsPt="$B0 $MuDen --sP ptJI_mvaTTH${WP%%i*}_coarse --sp 'TT.*' " 
        ElFakeVsPt="$B0 $ElDen --sP ptJI_mvaTTH${WP%%i*}_coarse --sp 'TT.*' " 
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.5'   ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.5'   ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_00_15_pt8.root -R pt20 eta 'abs(LepGood_eta)<1.5 && LepGood_pt > 8'   ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_15_24_pt8.root -R pt20 eta 'abs(LepGood_eta)>1.5 && LepGood_pt > 8'   ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_00_15_pt12.root -R pt20 eta 'abs(LepGood_eta)<1.479 && LepGood_pt > 12' ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_15_24_pt12.root -R pt20 eta 'abs(LepGood_eta)>1.479 && LepGood_pt > 12' ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_00_15_pt17.root -R pt20 eta 'abs(LepGood_eta)<1.5 && LepGood_pt > 17'   ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_15_24_pt17.root -R pt20 eta 'abs(LepGood_eta)>1.5 && LepGood_pt > 17'   ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_00_15_pt23.root -R pt20 eta 'abs(LepGood_eta)<1.479 && LepGood_pt > 23' ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_15_24_pt23.root -R pt20 eta 'abs(LepGood_eta)>1.479 && LepGood_pt > 23' ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_00_15_pt24.root -R pt20 eta 'abs(LepGood_eta)<1.5 && LepGood_pt > 17'   ${BG} )"
        echo "( $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_wp${WP}_a_eta_15_24_pt24.root -R pt20 eta 'abs(LepGood_eta)>1.5 && abs(LepGood_eta)< 2.1 && LepGood_pt > 24'   ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_00_15_pt32.root -R pt20 eta 'abs(LepGood_eta)<1.479 && LepGood_pt > 32' ${BG} )"
        echo "( $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_wp${WP}_a_eta_15_24_pt32.root -R pt20 eta 'abs(LepGood_eta)>1.479 && abs(LepGood_eta)< 2.1 && LepGood_pt > 32' ${BG} )"
        ;;

esac;
