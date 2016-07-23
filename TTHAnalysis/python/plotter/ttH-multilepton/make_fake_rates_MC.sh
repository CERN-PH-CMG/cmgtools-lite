################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/lepton-mca-frstudies.txt object-studies/lepton-perlep.txt  "
T="/afs/cern.ch/user/m/mmarionn/workspace/public/SUSYSamples/809_June9_1lep"
if hostname | grep -q cmsco01; then
#    T="/data1/gpetrucc/TREES_TTH_260116_76X_1L"

#    T="/data1/peruzzi/TREES_TTH_260116_76X_1L --Fs {P}/fr_mvaSUSY"
#    PBASE="~/www/plots_FR/76X/lepMVA/v1.3_160616"
#    PBASE="~/www/plots_FR/76X/lepMVA/TEST"

    #T="/data1/peruzzi/TREES_80X_210616_1lep"
    T="/data1/gpetrucc/TREES_80X_TTH_180716_1L_MC" # warning: QCDEl from 76X
    PBASE="plots/80X/ttH/fr-mc/v2.1"

fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PLOTTER="python mcPlots.py $BCORE   "



BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" -j 4 & "; shift; fi

if [[ "$*" == "" ]]; then WPs="075ib1f30E2ptc30"; else WPs="$*"; fi;
for WP in $WPs; do
        MuIdDen=0; EleRecoPt=7; MuRecoPt=5; AwayJetPt=30;
        SIP8="LepGood_sip3d < 8"; SIP4="LepGood_sip3d < 4"
        VCSVT="LepGood_jetBTagCSV < 0.935"
        VCSVM="LepGood_jetBTagCSV < 0.80"
        VCSVL="LepGood_jetBTagCSV < 0.460"
        VCSVVL="LepGood_jetBTagCSV < 0.300"
        PTF30="LepGood_jetPtRatiov2 > 0.3"
	ELEMVAPRESEL="(abs(LepGood_pdgId)!=11 || abs(LepGood_eta)<1.479 || LepGood_mvaIdSpring15>0.0)"
	ELEMVAPRESEL2="(abs(LepGood_pdgId)!=11 || (abs(LepGood_eta)<1.479 && LepGood_mvaIdSpring15>0.0) || (abs(LepGood_eta)>1.479 && LepGood_mvaIdSpring15>0.3))"
	OLDTRIGGERS="((abs(LepGood_pdgId)!=11 || HLT_BIT_HLT_Ele12_CaloIdM_TrackIdM_PFJet30_v) && (abs(LepGood_pdgId)!=13 || (HLT_FR_Mu8 && LepGood_pt<20) || (HLT_FR_Mu17 && LepGood_pt>=20)))"
	VETOCONVERSIONS="LepGood_mcPromptGamma==0"
        case $WP in 
            000*) WNUM="0.00" ;; 030*) WNUM="0.30" ;; 060*) WNUM="0.60" ;;
            075*) WNUM="0.75" ;; 080*) WNUM="0.80" ;; 085*) WNUM="0.85" ;;
	    sM*) WNUM="if3(abs(LepGood_pdgId)==13,-0.2,0.5)";; sV*) WNUM="if3(abs(LepGood_pdgId)==13,0.45,0.75)";;
        esac
        case $WP in # 075ib1f30E2ptc30
            0??)     SelDen="-A pt20 den '$SIP8'"; MuIdDen=1 ; Num="mvaPt_$WP" ; XVar="mvaPt${WP}";;
            0??i)    SelDen="-A pt20 den '$SIP8'"; Num="mvaPt_$WP" ; XVar="mvaPt${WP}";; 
            0??ib1*) SelDen="-A pt20 den '$SIP8 && $VCSVM && (LepGood_mvaTTH > $WNUM || $VCSVL)'";           Num="mvaPt_${WP%%b*}"; XVar="mvaPt${WP%%i*}";;
            0??ib2*) SelDen="-A pt20 den '$SIP8 && $VCSVM && (LepGood_mvaTTH > $WNUM || $SIP4 && $VCSVVL)'"; Num="mvaPt_${WP%%b*}"; XVar="mvaPt${WP%%i*}";;
            0??ibb*) SelDen="-A pt20 den '$SIP8 && $VCSVL'"; Num="mvaPt_${WP%%b*}"; XVar="mvaPt${WP%%i*}";;
            0??ib*)  SelDen="-A pt20 den '$SIP8 && $VCSVM'"; Num="mvaPt_${WP%%b*}"; XVar="mvaPt${WP%%i*}";;
            0??iB*)  SelDen="-A pt20 den '$SIP8 && $VCSVT'"; Num="mvaPt_${WP%%B*}"; XVar="mvaPt${WP%%i*}";;
	    RA5*)    SelDen="-A pt20 den '$SIP4'"; MuIdDen=1 ; Num="ra5_tight"; XVar="${WP}";;
	    RA7*)    SelDen="-A pt20 den '$SIP4 && met_pt<20 && mt_2(LepGood_pt,LepGood_phi,met_pt,met_phi)<20 && ${OLDTRIGGERS}'"; MuIdDen=1 ; MuRecoPt=10; EleRecoPt=10; AwayJetPt=40; Num="ra7_tight"; XVar="${WP}";;
	    s?i*)   SelDen="-A pt20 den '$SIP8'"; Num="mvaSusy_${WP}" ; XVar="mvaSusy_${WP}";;
        esac
        case $WP in
            *f30*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || $PTF30)' " ;;
        esac
	case $WP in
	    *X0*) Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X1*) SelDen="$SelDen -A pt20 vcsvm '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || ($VCSVM && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X2*) SelDen="$SelDen -A pt20 vcsvl '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || ($VCSVL && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X3k*) SelDen="$SelDen -A pt20 vcsvvl '$VCSVM && ((LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || ($VCSVVL && $PTF30))'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X3*) SelDen="$SelDen -A pt20 vcsvvl '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || ($VCSVVL && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X4v*) SelDen="$SelDen -A pt20 noconv '${VETOCONVERSIONS}' -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X4mr*) SelDen="$SelDen -A pt20 noconv '${VETOCONVERSIONS}' -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL2} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}"; MuIdDen=1; MuRecoPt=10; EleRecoPt=10;;
	    *X4*) SelDen="$SelDen -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X5*) SelDen="$SelDen -A pt20 vcsvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_ICHEPmediumMuonId>0) || (${VCSVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	esac
        case $WP in
            *E)  SelDen="$SelDen -A pt20 eidden LepGood_idEmu "; XVar="${XVar%%E*}";;
            *Eptc30) SelDen="$SelDen -A pt20 eidden '(abs(LepGood_pdgId) == 13 || LepGood_idEmu || LepGood_pt*if3(LepGood_mvaTTH>0.75, 1.0, 0.85/LepGood_jetPtRatiov2) < 30)'"; XVar="${XVar%%E*}";;
            *E2) SelDen="$SelDen -A pt20 eidden LepGood_idEmu2"; Num="${Num%%E*}"; XVar="${XVar%%E*}";;
            *E2ptc30) SelDen="$SelDen -A pt20 eidden '(abs(LepGood_pdgId) == 13 || LepGood_idEmu2 || LepGood_pt*if3(LepGood_mvaTTH>0.75, 1.0, 0.85/LepGood_jetPtRatiov2) < 30)'"; XVar="${XVar%%E*}";;
        esac
	case $WP in
	    0*)    ptJI="ptJI85";;
	    RA*)  ptJI="conePt";;
	    sViX0*)    ptJI="ptJI85";;
	    sMiX0*)    ptJI="ptJI85";;
	    sVi*)    ptJI="ptJIMIX3";;
	    sMi*)    ptJI="ptJIMIX4";;
	esac
        B0="$BASE -P $T ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        B0="$B0 --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
        B0="$B0 --legend=TR --showRatio --ratioRange 0.51 1.49 --xcut 10 999  --yrange 0 0.30 "
	B1="${PLOTTER} -P $T ttH-multilepton/make_fake_rates_plots.txt"
	B1="${B1} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
        B1="$B1 --showRatio --plotmode=norm -f "
        JetDen="-A pt20 mll 'nLepGood == 1'"
        CommonDen="${JetDen} ${SelDen} -A pt20 fake 'LepGood_mcMatchId==0' "
        MuDen="${CommonDen} -A pt20 mmuid 'LepGood_ICHEPmediumMuonId>=${MuIdDen}' -A pt20 mpt 'LepGood_pt > ${MuRecoPt}' "
        ElDen="${CommonDen} -I mu -A pt20 convveto 'LepGood_convVeto' -A pt20 lh0 'LepGood_lostHits == 0' -A pt20 elpt 'LepGood_pt > ${EleRecoPt}' "
        MuDen="${MuDen} --mcc ttH-multilepton/mcc-ichepMediumMuonId.txt "
        ElDen="${ElDen} --mcc ttH-multilepton/mcc-ichepMediumMuonId-fake.txt "
        for BVar in bAny; do # bMedium; do 
        RVar=${AwayJetPt}; 
        case $BVar in
            bAny)    BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar ' " ;;
            bVeto)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV < 0.46' " ;;
            bLoose)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.46' " ;;
            bMedium) BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.80'  " ;;
            bTight)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.935'  " ;;
        esac;
        Me="wp${WP}_rec${RVar}_${BVar}"

        MuFakeVsPt="$MuDen ${BDen} --sP '${ptJI}_${XVar}_coarse' --sp TT_red " 
        ElFakeVsPt="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarse' --sp TT_red " 

#        echo "( $B1 $MuDen ${BDen} --ratioDen TT_bjets --ratioNums QCDMu_bjets -p TT_ljets,TT_bjets,QCDMu_ljets,QCDMu_bjets --pdir $PBASE/$what/mu_convs_${Me}_eta_00_12/ -A pt20 conv 'LepGood_mcPromptGamma==1' -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
#        echo "( $B1 $MuDen ${BDen} --ratioDen TT_bjets --ratioNums QCDMu_bjets -p TT_ljets,TT_bjets,QCDMu_ljets,QCDMu_bjets --pdir $PBASE/$what/mu_convs_${Me}_eta_12_24/ -A pt20 conv 'LepGood_mcPromptGamma==1' -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
#        echo "( $B1 $ElDen ${BDen} --ratioDen TT_bjets --ratioNums QCDEl_bjets -p TT_ljets,TT_bjets,QCDEl_ljets,QCDEl_bjets --pdir $PBASE/$what/el_convs_${Me}_eta_00_15/ -A pt20 conv 'LepGood_mcPromptGamma==1' -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
#        echo "( $B1 $ElDen ${BDen} --ratioDen TT_bjets --ratioNums QCDEl_bjets -p TT_ljets,TT_bjets,QCDEl_ljets,QCDEl_bjets --pdir $PBASE/$what/el_convs_${Me}_eta_15_25/ -A pt20 conv 'LepGood_mcPromptGamma==1' -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
#        echo "( $B1 $ElDen ${BDen} -p QCDEl_ljets --pdir $PBASE/$what/el_convs_${Me}_eta_00_15/ -A pt20 conv 'LepGood_mcPromptGamma==1' -R pt20 eta 'abs(LepGood_eta)<1.479' -R lh0 lh1 'LepGood_lostHits<=1'  ${BG} )"
#        echo "( $B1 $ElDen ${BDen} -p QCDEl_ljets --pdir $PBASE/$what/el_convs_${Me}_eta_15_25/ -A pt20 conv 'LepGood_mcPromptGamma==1' -R pt20 eta 'abs(LepGood_eta)>1.479' -R lh0 lh1 'LepGood_lostHits<=1'  ${BG} )"
#        echo "( $B1 $ElDen ${BDen} -p QCDEl_ljets,QCDEl_ljets_noconv,QCDEl_ljets_conv --pdir $PBASE/$what/el_convs_${Me}_eta_00_15/  -R pt20 eta 'abs(LepGood_eta)<1.479' -R lh0 lh1 'LepGood_lostHits<=1'  ${BG} )"
#        echo "( $B1 $ElDen ${BDen} -p QCDEl_ljets,QCDEl_ljets_noconv,QCDEl_ljets_conv --pdir $PBASE/$what/el_convs_${Me}_eta_15_25/  -R pt20 eta 'abs(LepGood_eta)>1.479' -R lh0 lh1 'LepGood_lostHits<=1'  ${BG} )"
#
#	break;

	
#        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
#        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
#
#	break;

        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red     -o $PBASE/$what/mu_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red     -o $PBASE/$what/mu_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red     -o $PBASE/$what/el_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red     -o $PBASE/$what/el_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        MuFakeVsPtLongBin="$MuDen ${BDen} --sP '${ptJI}_${XVar}_coarselongbin' --sp TT_red " 
        ElFakeVsPtLongBin="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarselongbin' --sp TT_red " 
        echo "( $B0 $MuFakeVsPtLongBin -p TT_red,QCDMu_red     -o $PBASE/$what/mu_lbin_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtLongBin -p TT_red,QCDMu_red     -o $PBASE/$what/mu_lbin_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtLongBin -p TT_red,QCDEl_red     -o $PBASE/$what/el_lbin_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtLongBin -p TT_red,QCDEl_red     -o $PBASE/$what/el_lbin_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        ElFakeVsPtZBin="$ElDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse2' --sp TT_red " 
        echo "( $B0 $ElFakeVsPtZBin -p TT_red,QCDEl_red     -o $PBASE/$what/el_zc2bin_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtZBin -p TT_red,QCDEl_red     -o $PBASE/$what/el_zc2bin_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"


        echo "( $B0 $MuFakeVsPt -p TT_redNC,QCDMu_redNC -o $PBASE/$what/mu_nc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_redNC,QCDMu_redNC -o $PBASE/$what/mu_nc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_redNC,QCDEl_redNC -o $PBASE/$what/el_nc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_redNC,QCDEl_redNC -o $PBASE/$what/el_nc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_bjets,QCDMu_bjets -o $PBASE/$what/mu_b_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_bjets,QCDMu_bjets -o $PBASE/$what/mu_b_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_bjets,QCDEl_bjets -o $PBASE/$what/el_b_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_bjets,QCDEl_bjets -o $PBASE/$what/el_b_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        MuFakeVsPtL="$MuDen ${BDen} --sP '${ptJI}_${XVar}_flow' --sp TT_red " 
        echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_flow_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_flow_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        MuFakeVsPtL="$MuDen ${BDen} --sP '${ptJI}_${XVar}_low' --sp TT_red " 
        echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_low_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_low_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"

        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets,QCDMu_cjets -o $PBASE/$what/mu_bnb_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets,QCDMu_cjets -o $PBASE/$what/mu_bnb_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets,QCDEl_cjets -o $PBASE/$what/el_bnb_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets,QCDEl_cjets -o $PBASE/$what/el_bnb_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,Wjets_red,Wjets_ljets -o $PBASE/$what/mu_withW_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,Wjets_red,Wjets_ljets -o $PBASE/$what/mu_withW_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,Wjets_red,Wjets_ljets -o $PBASE/$what/el_withW_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,Wjets_red,Wjets_ljets -o $PBASE/$what/el_withW_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,DY_red,DY_ljets -o $PBASE/$what/mu_withDY_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,DY_red,DY_ljets -o $PBASE/$what/mu_withDY_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,DY_red,DY_ljets -o $PBASE/$what/el_withDY_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,DY_red,DY_ljets -o $PBASE/$what/el_withDY_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_12_21.root  -R pt20 eta 'abs(LepGood_eta)>1.2 && abs(LepGood_eta)<2.1'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_21_24.root  -R pt20 eta 'abs(LepGood_eta)>2.1'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb_${Me}_eta_00_08.root  -R pt20 eta 'abs(LepGood_eta)<0.8' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb_${Me}_eta_08_15.root  -R pt20 eta 'abs(LepGood_eta)>0.8 && abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"


        #AwayJet pt variations
        MuFakeVsPt0J="$MuDen --sP '${ptJI}_${XVar}_coarse' --sp TT_red " 
        ElFakeVsPt0J="$ElDen --sP '${ptJI}_${XVar}_coarse' --sp TT_red " 
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'QCDMu_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_qajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'QCDMu_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_qajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'QCDEl_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_qajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'QCDEl_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_qajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet b-tag
        MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}_coarse' --sp TT_red,TT_SSbt_black -A pt20 jet 'LepGood_awayJet_pt > $RVar ' " 
        ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}_coarse' --sp TT_red,TT_SSbt_black -A pt20 jet 'LepGood_awayJet_pt > $RVar ' " 
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'QCDMu_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'QCDMu_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'QCDEl_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'QCDEl_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

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
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT tuning (qcd)
        #echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_red_pt[0-9]+,QCDMu_red_Mu[0-9]+,QCDMu_red_pt17+ -o $PBASE/$what/mu_hltpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_red_pt[0-9]+,QCDMu_red_Mu[0-9]+,QCDMu_red_pt17+ -o $PBASE/$what/mu_hltpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_red_pt[0-9]+,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hltpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_red_pt[0-9]+,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hltpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # pT cut (ttbar)
        #echo "( $B0 $MuFakeVsPt -p 'TT_red,TT_pt(8|17)_red'  -o $PBASE/$what/mu_ttpt_${Me}_eta_00_12_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p 'TT_red,TT_pt12_red' -o $PBASE/$what/el_ttpt_${Me}_eta_00_15_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"

        # TTbar conversions 
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/mu_ttwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/mu_ttwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/el_ttwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/el_ttwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        #QCD conversions
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_redNC -o $PBASE/$what/mu_qcdwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_redNC -o $PBASE/$what/mu_qcdwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_redNC -o $PBASE/$what/el_qcdwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_redNC -o $PBASE/$what/el_qcdwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #Z3l conversions
        MuFakeVsPtZ="$MuDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse' --sp TT_red " 
        ElFakeVsPtZ="$ElDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse' --sp TT_red " 
        #echo "( $B0 $MuFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/mu_z3lwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/mu_z3lwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/el_z3lwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/el_z3lwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # TTbar vs Z3l closure 
        MuFakeVsPtZ="$MuDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse2' --sp TT_red " 
        ElFakeVsPtZ="$ElDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse2' --sp TT_red " 
        #echo "( $B0 $MuFakeVsPtZ -p TT_red,Z3l_red,Z3l_red_80 -o $PBASE/$what/mu_ttz3l_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPtZ -p TT_red,Z3l_red,Z3l_red_80 -o $PBASE/$what/mu_ttz3l_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPtZ -p TT_red,Z3l_red -o $PBASE/$what/el_ttz3l_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        #echo "( $B0 $ElFakeVsPtZ -p TT_red,Z3l_red -o $PBASE/$what/el_ttz3l_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"



        done;
done
