################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/lepton-mca-frstudies.txt object-studies/lepton-perlep.txt  "
T="/afs/cern.ch/user/g/gpetrucc/w/TREES_TTH_260116_76X_1L/"
if hostname | grep -q cmsco01; then
    T="/data1/gpetrucc/TREES_TTH_260116_76X_1L"
fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PBASE="plots/76X/lepMVA/v1.0"

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" -j 4 & "; shift; fi

for WP in $*; do
        XVar="mvaPt"; Num="mvaPt_$WP"; MuIdDen=0; EleRecoPt=7;
        SIP8="LepGood_sip3d < 8"; SIP4="LepGood_sip3d < 4"
        VCSVT="LepGood_jetBTagCSV < 0.97"
        VCSVM="LepGood_jetBTagCSV < 0.89"
        VCSVL="LepGood_jetBTagCSV < 0.605"
        VCSVVL="LepGood_jetBTagCSV < 0.300"
        PTF30="LepGood_jetPtRatiov2 > 0.3"
        case $WP in 
            000*) WNUM="0.00" ;; 030*) WNUM="0.30" ;; 060*) WNUM="0.60" ;;
            075*) WNUM="0.75" ;; 080*) WNUM="0.80" ;; 085*) WNUM="0.85" ;;
        esac
        case $WP in
            0??)     SelDen="-A pt20 den '$SIP8'"; MuIdDen=1 ;;
            0??i)    SelDen="-A pt20 den '$SIP8'";; 
            0??ib1*) SelDen="-A pt20 den '$SIP8 && $VCSVM && (LepGood_mvaTTH > $WNUM || $VCSVL)'";           Num="mvaPt_${WP%%b*}";;
            0??ib2*) SelDen="-A pt20 den '$SIP8 && $VCSVM && (LepGood_mvaTTH > $WNUM || $SIP4 && $VCSVVL)'"; Num="mvaPt_${WP%%b*}";;
            0??ibb*) SelDen="-A pt20 den '$SIP8 && $VCSVL'"; Num="mvaPt_${WP%%b*}";;
            0??ib*)  SelDen="-A pt20 den '$SIP8 && $VCSVM'"; Num="mvaPt_${WP%%b*}";;
            0??iB*)  SelDen="-A pt20 den '$SIP8 && $VCSVT'"; Num="mvaPt_${WP%%B*}";;
        esac
        case $WP in
            *f30*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || $PTF30)' " ;;
        esac
        case $WP in
            *E)  SelDen="$SelDen -A pt20 eidden LepGood_idEmu "; Num="mvaPt_${WP%%b*}";;
            *E2) SelDen="$SelDen -A pt20 eidden LepGood_idEmu2"; Num="mvaPt_${WP%%b*}";;
            *E2ptc30) SelDen="$SelDen -A pt20 eidden '(LepGood_idEmu2 || LepGood_pt*if3(LepGood_mvaTTH>0.75&&LepGood_mediumMuonId>0, 1.0, 0.85/LepGood_jetPtRatiov2) < 30)'"; Num="mvaPt_${WP%%b*}";;
        esac
        ptJI="ptJI85"
        B0="$BASE -P $T ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        B0="$B0 --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
        B0="$B0 --legend=TR  --yrange 0 0.25 --showRatio --ratioRange 0.0 1.99 "
        JetDen="-A pt20 mll 'nLepGood == 1'"
        CommonDen="${JetDen} ${SelDen}  "
        MuDen="${CommonDen} -A pt20 den 'LepGood_mediumMuonId>=${MuIdDen} && LepGood_pt > 5'   --xcut 10 999  --yrange 0 0.15 "
        ElDen="${CommonDen} -I mu -A pt20 den 'LepGood_convVeto && LepGood_lostHits == 0 && LepGood_pt > ${EleRecoPt}' --xcut 10 999  --yrange 0 0.25 "
        for BVar in bAny; do # bMedium; do 
        RVar=30; 
        case $BVar in
            bAny)    BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar ' " ;;
            bVeto)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV < 0.605' " ;;
            bLoose)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.605' " ;;
            bMedium) BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.89'  " ;;
            bTight)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.97'  " ;;
        esac;
        Me="wp${WP}_rec${RVar}_${BVar}"

        MuFakeVsPt="$MuDen ${BDen} --sP '${ptJI}_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen ${BDen} --sP '${ptJI}_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red -o $PBASE/$what/mu_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_bjets,QCDMu_bjets -o $PBASE/$what/mu_b_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_bjets,QCDMu_bjets -o $PBASE/$what/mu_b_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red -o $PBASE/$what/el_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_bjets,QCDEl_bjets -o $PBASE/$what/el_b_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_bjets,QCDEl_bjets -o $PBASE/$what/el_b_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #AwayJet pt variations
        MuFakeVsPt0J="$MuDen --sP '${ptJI}_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        ElFakeVsPt0J="$ElDen --sP '${ptJI}_${XVar}${WP%%i*}_coarse' --sp TT_red " 
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet b-tag
        MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}${WP%%i*}_coarse' --sp TT_red,TT_SSbt_black -A pt20 jet 'LepGood_awayJet_pt > $RVar ' " 
        ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}${WP%%i*}_coarse' --sp TT_red,TT_SSbt_black -A pt20 jet 'LepGood_awayJet_pt > $RVar ' " 
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # TTbar by composition
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #QCD by flavour
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/el_ftt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/el_ftt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        # TT by flavour
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_bjets,QCDMu_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_bjets,QCDMu_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_bjets,QCDEl_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_bjets,QCDEl_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT tuning (qcd)
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_red_pt[0-9]+,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hltpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_red_pt[0-9]+,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hltpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_red_pt[0-9]+,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hltpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_red_pt[0-9]+,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hltpt_${Me}_eta_15_24.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # pT cut (ttbar)
        echo "( $B0 $MuFakeVsPt -p 'TT_red,TT_pt(8|17)_red'  -o $PBASE/$what/mu_ttpt_${Me}_eta_00_12_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_red,TT_pt12_red' -o $PBASE/$what/el_ttpt_${Me}_eta_00_15_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"

        done;
done
