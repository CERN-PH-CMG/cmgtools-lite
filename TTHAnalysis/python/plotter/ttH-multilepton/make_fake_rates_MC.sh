################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

ANALYSIS=$1; if [[ "$1" == "" ]]; then exit 1; fi; shift;
case $ANALYSIS in
ttH) 
    YEAR=$1; shift; 
    case $YEAR in 2016) L=35.9;; 2017) L=41.5;; 2018) L=59.7;; esac
    T=/eos/cms/store/cmst3/group/tthlep/gpetrucc/TREES_ttH_FR_nano_v5/$YEAR
    test -d /tmp/$USER/TREES_ttH_FR_nano_v5/$YEAR && T="/tmp/$USER/TREES_ttH_FR_nano_v5/$YEAR -P $T"
    test -d /data/$USER/TREES_ttH_FR_nano_v5/$YEAR && T="/data/$USER/TREES_ttH_FR_nano_v5/$YEAR -P $T"
    #hostname | grep -q cmsco01 && T=/data1/gpetrucc/TREES_94X_FR_240518
    #hostname | grep -q cmsphys10 && T=/data/g/gpetrucc/TREES_94X_FR_240518
    PBASE="plots/104X/${ANALYSIS}/lepMVA/v1.1/fr-mc/$YEAR"
    TREE="NanoAOD";
    ;;
old_ttH)
    YEAR=2017;
    T=/eos/cms/store/cmst3/group/tthlep/gpetrucc/TREES_94X_FR_240518
    PBASE="plots/104X/ttH/lepMVA/dev-v1.1/fr-mc/$YEAR"
    TREE="treeProducerSusyMultilepton";
    ;;
susy) 
    echo "NOT UP TO DATE"; exit 1; 
    ;;
*)
    echo "Unknown analysis '$ANALYSIS'";
    exit 1;
esac;


BCORE=" --s2v --tree ${TREE} ttH-multilepton/lepton-fr/lepton-mca-frstudies.txt object-studies/lepton-perlep.txt"
BCORE="${BCORE} -L ttH-multilepton/functionsTTH.cc"
if [[ "$TREE" == "treeProducerSusyMultilepton" ]]; then
    BCORE="${BCORE} --mcc ttH-multilepton/validation/mcc-cmg_as_nanoaod.txt"
    BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
else
    BCORE="${BCORE} --Fs {P}/1_frFriends_v1"
    BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "
fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PLOTTER="python mcPlots.py $BCORE   "


BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" -j 4 & "; shift; fi
HAS_CUSTOM_RECOIL=false
if [[ "$2" == "--recoil" ]]; then
    HAS_CUSTOM_RECOIL=true
    RECOIL_NAME="$3"
    RECOIL_VALUE="$4"
fi;

if [[ "$*" == "" ]]; then WPs="090iv01f60E3"; else WPs="$1"; fi;
for WP in $WPs; do
        MuIdDen=0; EleRecoPt=7; MuRecoPt=5; AwayJetPt=30; EleTC=0; IDEMu=1
        SIP8="LepGood_sip3d < 8"; SIP4="LepGood_sip3d < 4"
        case $YEAR in 
            2016) # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation2016Legacy
                VDCSVT="LepGood_jetBTagDeepCSV < 0.8953"
                VDCSVM="LepGood_jetBTagDeepCSV < 0.6321"
                VDCSVL="LepGood_jetBTagDeepCSV < 0.2217"
                VDCSVVL="LepGood_jetBTagDeepCSV < 0.07" ## ttH-specific
                VDFT="LepGood_jetBTagDeepFlav < 0.7221 "
                VDFM="LepGood_jetBTagDeepFlav < 0.3093"
                VDFL="LepGood_jetBTagDeepFlav < 0.0614"
                ;;
            2017) # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
                VDCSVT="LepGood_jetBTagDeepCSV < 0.8001"
                VDCSVM="LepGood_jetBTagDeepCSV < 0.4941"
                VDCSVL="LepGood_jetBTagDeepCSV < 0.1522"
                VDCSVVL="LepGood_jetBTagDeepCSV < 0.07" ## ttH-specific
                VDFT="LepGood_jetBTagDeepFlav < 0.7489"
                VDFM="LepGood_jetBTagDeepFlav < 0.3033"
                VDFL="LepGood_jetBTagDeepFlav < 0.0521"
                ;;
            2018) # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
                VDCSVT="LepGood_jetBTagDeepCSV < 0.7527"
                VDCSVM="LepGood_jetBTagDeepCSV < 0.4184"
                VDCSVL="LepGood_jetBTagDeepCSV < 0.1241"
                VDCSVVL="LepGood_jetBTagDeepCSV < 0.07" ## ttH-specific
                VDFT="LepGood_jetBTagDeepFlav < 0.7264"
                VDFM="LepGood_jetBTagDeepFlav < 0.2770"
                VDFL="LepGood_jetBTagDeepFlav < 0.0494"
                ;;
        esac
        PTF30="1/(1+LepGood_jetRelIso) > 0.3"
	VETOCONVERSIONS="LepGood_mcPromptGamma==0"
        case $WP in 
            000*) WNUM="0.00" ;; 030*) WNUM="0.30" ;; 060*) WNUM="0.60" ;;
            075*) WNUM="0.75" ;; 080*) WNUM="0.80" ;; 085*) WNUM="0.85" ;;  090*) WNUM="0.90" ;;
	    sM*) WNUM="if3(abs(LepGood_pdgId)==13,-0.2,0.5)";; sV*) WNUM="if3(abs(LepGood_pdgId)==13,0.45,0.75)";;
        esac
        case $WP in
            0??)     SelDen="-A pt20 den '$SIP8'"; MuIdDen=1 ; Num="mvaPt_$WP" ; XVar="mvaPt${WP}";;
            0??i)    SelDen="-A pt20 den '$SIP8'"; Num="mvaPt_$WP" ; XVar="mvaPt${WP}";; 
            # This below was the 2017 version
            #0??ov010*) SelDen="-A pt20 den '$SIP8 && $VDCSVM && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VDCSVVL && LepGood_segmentComp > 0.3) || (abs(LepGood_pdgId)==11 && $VDCSVVL && LepGood_mvaIdFall17noIso > +0.5))'"; Num="mvaPt_${WP%%o*}"i; XVar="mvaPt${WP%%o*}";;

            0??v00*) SelDen="-A pt20 den '$SIP8 && $VDFM'"; MuIdDen=1 ; Num="mvaPt_${WP%%v*}"i; XVar="mvaPt${WP%%v*}";;
            0??iv00*) SelDen="-A pt20 den '$SIP8 && $VDFM'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";;
            0??iv01*) SelDen="-A pt20 den '$SIP8 && $VDFM && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VDFL) || (abs(LepGood_pdgId)==11 && $VDFL))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";;
            0??iv070*) VSMOOTH="LepGood_jetBTagDeepFlav < smoothBFlav(0.9*LepGood_pt*(1+LepGood_jetRelIso), 20, 45, year)";
                       SelDen="-A pt20 den '$SIP8 && $VDFM && PV_ndof > 100 && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VSMOOTH) || (abs(LepGood_pdgId)==11 && $VSMOOTH))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";; 
            0??iv08WP80*) VSMOOTH="LepGood_jetBTagDeepFlav < smoothBFlav(0.9*LepGood_pt*(1+LepGood_jetRelIso), 20, 45, year)";
                       SelDen="-A pt20 den '$SIP8 && $VDFM && PV_ndof > 100 && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $VSMOOTH) || (abs(LepGood_pdgId)==11 && LepGood_mvaFall17V2noIso_WP80))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";; 
            0??iRun2v1.0*) 
                       IDEmu="LepGood_idEmu3"
                       MUEXTRA="LepGood_jetBTagDeepFlav < smoothBFlav(0.9*LepGood_pt*(1+LepGood_jetRelIso), 20, 45, year) && LepGood_jetRelIso < 0.50";
                       ELEXTRA="LepGood_mvaFall17V2noIso_WP80 && LepGood_jetRelIso < 0.70"
                       SelDen="-A pt20 den '$SIP8 && $VDFM && PV_ndof > 100 && (LepGood_mvaTTH > $WNUM || (abs(LepGood_pdgId)==13 && $MUEXTRA) || (abs(LepGood_pdgId)==11 && $ELEXTRA))'"; Num="mvaPt_${WP%%i*}"i; XVar="mvaPt${WP%%i*}";; 

 	    RA5*)    SelDen="-A pt20 den '$SIP4'"; MuIdDen=1 ; Num="ra5_tight"; XVar="${WP}";;
	    RA7*)    SelDen="-A pt20 den '$SIP4 && met_pt<20 && mt_2(LepGood_pt,LepGood_phi,met_pt,met_phi)<20'"; MuIdDen=1 ; MuRecoPt=10; EleRecoPt=10; AwayJetPt=40; Num="ra7_tight"; XVar="${WP}";;
	    s?i*)   SelDen="-A pt20 den '$SIP8'"; Num="mvaSusy_${WP}" ; XVar="mvaSusy_${WP}";;
        esac
        case $WP in
            *f30*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.30)' " ;;
            *f40*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.40)' " ;;
            *f45*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.45)' " ;;
            *f50*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.50)' " ;;
            *f60*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.60)' " ;;
            *f65*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || 1/(1+LepGood_jetRelIso) > 0.65)' " ;;
            *j40*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.40)' " ;;
            *j50*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.50)' " ;;
            *j60*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.60)' " ;;
            *j70*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.70)' " ;;
            *j80*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.80)' " ;;
            *j90*) SelDen="$SelDen -A pt20 ptfden '(LepGood_mvaTTH > $WNUM || LepGood_jetRelIso < 0.90)' " ;;
        esac
	case $WP in
	    *X0*) Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X1*) SelDen="$SelDen -A pt20 vcsvm '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVM && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X2*) SelDen="$SelDen -A pt20 vcsvl '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVL && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X3k*) SelDen="$SelDen -A pt20 vcsvvl '$VCSVM && ((LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVVL && $PTF30))'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X3*) SelDen="$SelDen -A pt20 vcsvvl '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || ($VCSVVL && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X4v*) SelDen="$SelDen -A pt20 noconv '${VETOCONVERSIONS}' -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X4mr*) SelDen="$SelDen -A pt20 noconv '${VETOCONVERSIONS}' -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL2} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}"; MuIdDen=1; MuRecoPt=10; EleRecoPt=10;;
	    *X4*) SelDen="$SelDen -A pt20 vcsvvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	    *X5*) SelDen="$SelDen -A pt20 vcsvle '(LepGood_mvaSUSY > ${WNUM} && LepGood_mediumMuonId>0) || (${VCSVL} && ${ELEMVAPRESEL} && $PTF30)'"; Num="${Num%%X*}"; XVar="${XVar%%X*}";;
	esac
        case $WP in
            *E2) IDEMu="LepGood_idEmu2";;
            *E2ptc30) IDEMu="LepGood_idEmu2 || LepGood_pt*if3(LepGood_mvaTTH>${WNUM}, 1.0, 0.90*(1+LepGood_jetRelIso)) < 30" ;;
            *E3) IDEMu="LepGood_idEmu3";;
        esac
	case $WP in
	    *ptJ75*)    ptJI="ptJI75";;
	    *ptJ80*)    ptJI="ptJI80";;
	    *ptJ85*)    ptJI="ptJI85";;
	    *ptJ90*)    ptJI="ptJI90";;
	    *ptJ95*)    ptJI="ptJI95";;
	    090*)    ptJI="ptJI90";;
	    085*)    ptJI="ptJI90";;
	    080*)    ptJI="ptJI90";;
	    075*)    ptJI="ptJI90";;
	    RA*)  ptJI="conePt";;
	    sViX0*)    ptJI="ptJI85";;
	    sMiX0*)    ptJI="ptJI85";;
	    sVi*)    ptJI="ptJIMIX3";;
	    sMi*)    ptJI="ptJIMIX4";;
	esac
        B0="$BASE -P $T ttH-multilepton/lepton-fr/make_fake_rates_sels.txt ttH-multilepton/lepton-fr/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        #B0="$B0 --legend=TR --showRatio --ratioRange 0.41 1.59   --yrange 0 0.20 " 
        B0="$B0 --legend=TR --showRatio --ratioRange 0.00 1.99   --yrange 0 0.35 " 
	B1="${PLOTTER} -P $T ttH-multilepton/lepton-fr/make_fake_rates_plots.txt"
        B1="$B1 --showRatio --maxRatioRange 0 2 --plotmode=norm -f "
        JetDen="-A pt20 mll 'nLepGood == 1'"
        CommonDen="${JetDen} ${SelDen}"
        MuDen="${CommonDen} -A pt20 mmuid 'LepGood_mediumId>=${MuIdDen}' -A pt20 mpt 'LepGood_pt > ${MuRecoPt}' "
        ElDen="${CommonDen} -I mu -A pt20 convveto 'LepGood_convVeto && LepGood_lostHits == 0 && LepGood_tightCharge >= ${EleTC} && ${IDEmu}' -A pt20 elpt 'LepGood_pt > ${EleRecoPt}'  "
        #for BVar in bAny; do # bMedium; do 
        #RVar=${AwayJetPt}; 
        #case $BVar in
        #    bAny)    BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar ' " ;;
        #    bVeto)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV < 0.5426' " ;;
        #    bLoose)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.5426' " ;;
        #    bMedium) BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.8484'  " ;;
        #    bTight)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.9535'  " ;;
        #esac;
        #Me="wp${WP}_rec${RVar}_${BVar}"
        Me="wp${WP}_recJet30"
        BDen="-A pt20 jet 'LepGood_awayJet_pt >= 30'"
        #Me="wp${WP}_twoOrThreeLoose"
        #BDen="-A pt20 jet 'LepGood_awayNBJetLoose25 == 1 && LepGood_awayNJet25 > 1 && LepGood_awayNJet25 <= 3'"
        #Me="wp${WP}_oneM"
        #BDen="-A pt20 jet 'LepGood_awayNJet30 >= 1 && LepGood_awayNJet25 <= 2 && LepGood_awayNBJetLoose25 == 1 && LepGood_awayNBJetMedium25 == 1' "
        #Me="wp${WP}_oneT"
        #BDen="-A pt20 jet 'LepGood_awayNJet30 >= 1 && LepGood_awayNJet25 <= 2 && LepGood_awayNBJetLoose25 == 1 && LepGood_awayNBJetTight25 == 1' "
        #Me="wp${WP}_oneExT"
        #BDen="-A pt20 jet 'LepGood_awayNJet30 >= 1 && LepGood_awayNJet25 <= 1 && LepGood_awayNBJetLoose25 == 1 && LepGood_awayNBJetTight25 == 1' "
        if $HAS_CUSTOM_RECOIL; then
            Me="wp${WP}_${RECOIL_NAME}"
            BDen="-A pt20 jet '${RECOIL_VALUE}'"
        fi

        MuFakeVsPt="$MuDen ${BDen} --sP '${ptJI}_${XVar}_coarsecomb' --sp TT_SS_red --xcut 10 999 --xline 15 " 
        ElFakeVsPt="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarseelcomb' --sp TT_SS_redNC --xcut 10 999 --xline 15 --xline 30 " 

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

        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red     -o $PBASE/$what/mu_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red     -o $PBASE/$what/mu_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red     -o $PBASE/$what/el_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red     -o $PBASE/$what/el_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        MuFakeVsPtLongBin="$MuDen ${BDen} --sP '${ptJI}_${XVar}_coarselongbin' --sp TT_red   --xcut 10 999 --xline 15 " 
        ElFakeVsPtLongBin="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarselongbin' --sp TT_redNC --xcut 10 999 --xline 15 " 
        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red,QCDMu_red -o $PBASE/$what/mu_lbin_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red,QCDMu_red -o $PBASE/$what/mu_lbin_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtLongBin -p TT_SS_red,TT_SS_redNC,QCDEl_red_El8,QCDEl_redNC_El8 -o $PBASE/$what/el_lbin_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtLongBin -p TT_SS_red,TT_SS_redNC,QCDEl_red_El8,QCDEl_redNC_El8 -o $PBASE/$what/el_lbin_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
	#break;

        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red -o $PBASE/$what/mu_etabins_${Me}_eta_00_08.root    -R pt20 eta 'abs(LepGood_eta)<0.8'   ${BG} )"
        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red -o $PBASE/$what/mu_etabins_${Me}_eta_08_12.root    -R pt20 eta '0.8<abs(LepGood_eta)&&abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red -o $PBASE/$what/mu_etabins_${Me}_eta_12_15.root    -R pt20 eta '1.2<abs(LepGood_eta)&&abs(LepGood_eta)<1.5'   ${BG} )"
        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red -o $PBASE/$what/mu_etabins_${Me}_eta_15_21.root    -R pt20 eta '1.5<abs(LepGood_eta)&&abs(LepGood_eta)<2.1'   ${BG} )"
        echo "( $B0 $MuFakeVsPtLongBin -p TT_SS_red -o $PBASE/$what/mu_etabins_${Me}_eta_21_24.root    -R pt20 eta 'abs(LepGood_eta)>2.1'   ${BG} )"

        #ElFakeVsPtZBin="$ElDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse2' --sp TT_red " 
        #echo "( $B0 $ElFakeVsPtZBin -p TT_red,QCDEl_red     -o $PBASE/$what/el_zc2bin_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPtZBin -p TT_red,QCDEl_red     -o $PBASE/$what/el_zc2bin_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #echo "( $B0 $MuFakeVsPt -p TT_redNC,QCDMu_redNC -o $PBASE/$what/mu_nc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_redNC,QCDMu_redNC -o $PBASE/$what/mu_nc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_redNC,QCDEl_redNC -o $PBASE/$what/el_nc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_redNC,QCDEl_redNC -o $PBASE/$what/el_nc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_bjets,QCDMu_bjets -o $PBASE/$what/mu_b_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_bjets,QCDMu_bjets -o $PBASE/$what/mu_b_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_bjets,QCDEl_bjets -o $PBASE/$what/el_b_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_bjets,QCDEl_bjets -o $PBASE/$what/el_b_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        #MuFakeVsPtL="$MuDen ${BDen} --sP '${ptJI}_${XVar}_flow' --sp TT_red " 
        #echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_flow_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_flow_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #MuFakeVsPtL="$MuDen ${BDen} --sP '${ptJI}_${XVar}_low' --sp TT_red " 
        #echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_low_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPtL -p TT_red,QCDMu_red     -o $PBASE/$what/mu_low_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"

        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets,QCDMu_cjets -o $PBASE/$what/mu_blc_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets,QCDMu_cjets -o $PBASE/$what/mu_blc_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets,QCDEl_cjets -o $PBASE/$what/el_blc_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets,QCDEl_cjets -o $PBASE/$what/el_blc_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,Wjets_red,Wjets_ljets -o $PBASE/$what/mu_withW_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,Wjets_red,Wjets_ljets -o $PBASE/$what/mu_withW_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,Wjets_red,Wjets_ljets -o $PBASE/$what/el_withW_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,Wjets_red,Wjets_ljets -o $PBASE/$what/el_withW_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,DY_red,DY_ljets -o $PBASE/$what/mu_withDY_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,DY_red,DY_ljets -o $PBASE/$what/mu_withDY_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,DY_red,DY_ljets -o $PBASE/$what/el_withDY_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,DY_red,DY_ljets -o $PBASE/$what/el_withDY_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_SS.*_red,TT_redCharmless -o $PBASE/$what/mu_ttbnb_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_SS.*_red,TT_redCharmless -o $PBASE/$what/mu_ttbnb_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_SS_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_SS_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_SS_red,TT_SS.*_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_sum_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_SS_red,TT_SS.*_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_sum_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,QCDEl_redNC,QCDEl_bjets -o $PBASE/$what/el_bnbNC_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,QCDEl_redNC,QCDEl_bjets -o $PBASE/$what/el_bnbNC_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,QCDEl_redNC_El17,QCDEl_bjets -o $PBASE/$what/el_bnbe_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,QCDEl_redNC_El17,QCDEl_bjets -o $PBASE/$what/el_bnbe_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,QCDEl_redNC_El17,QCDEl_bjets -o $PBASE/$what/el_bnbe_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El8,QCDEl_redNC_El8 -o $PBASE/$what/el_sum8_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El8,QCDEl_redNC_El8 -o $PBASE/$what/el_sum8_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El17,QCDEl_redNC_El17 -o $PBASE/$what/el_sum17_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El17,QCDEl_redNC_El17 -o $PBASE/$what/el_sum17_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red,QCDEl_redNC -o $PBASE/$what/el_sumnt_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red,QCDEl_redNC -o $PBASE/$what/el_sumnt_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,QCDEl_red_El17,QCDEl_redNC_El17 -o $PBASE/$what/el_sumold_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 ${ElFakeVsPt/TT_SS_redNC/TT_SS_redNC_pink} -p TT_SS_red_viol,TT_SS_redNC_pink,QCDEl_red_El17,QCDEl_redNC_El17 -o $PBASE/$what/el_sumold_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
     
        PlotX="${B1/--plotmode=norm/}"; 
        PlotX="${PlotX/make_fake_rates_plots.txt/make_fake_rates_xvars.txt}"
        MuNormPlot="$PlotX $MuDen ${BDen} --sP '${ptJI}_${XVar}_coarsecomb'" 
        ElNormPlot="$PlotX $ElDen ${BDen} --sP '${ptJI}_${XVar}_coarseelcomb'" 
        echo "( $MuNormPlot -p TT_SS_red --pdir $PBASE/$what   -o {O}/mu_ttnorm_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $MuNormPlot -p TT_SS_red --pdir $PBASE/$what   -o {O}/mu_ttnorm_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $ElNormPlot -p TT_SS_redNC_pink --pdir $PBASE/$what -o {O}/el_ttnorm_${Me}_eta_00_15.root   -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $ElNormPlot -p TT_SS_redNC_pink --pdir $PBASE/$what -o {O}/el_ttnorm_${Me}_eta_15_25.root   -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        CElFakeVsPt="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarse' --sp TT_conv --xcut 10 999"; BC="${B0/--yrange 0 0.??/--yrange 0 1.0}"
        echo "( $BC $CElFakeVsPt -p TT_conv,QCDEl_conv_El12 -o $PBASE/$what/el_conv_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BC $CElFakeVsPt -p TT_conv,QCDEl_conv_El12 -o $PBASE/$what/el_conv_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        CElConvVsPt="$ElDen ${BDen} --sP '${ptJI}_${XVar}_coarse' --sp QCDEl_red_El12 --xcut 20 999 "; BC="${B0/--sP ${Num}/--sP isConv}"
        echo "( $BC $CElConvVsPt -p TT_red,QCDEl_red_El12 -o $PBASE/$what/el_isconv_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BC $CElConvVsPt -p TT_red,QCDEl_red_El12 -o $PBASE/$what/el_isconv_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb3_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb3_${Me}_eta_12_21.root  -R pt20 eta 'abs(LepGood_eta)>1.2 && abs(LepGood_eta)<2.1'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,QCDMu_red,QCDMu_bjets -o $PBASE/$what/mu_bnb3_${Me}_eta_21_24.root  -R pt20 eta 'abs(LepGood_eta)>2.1'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb4_${Me}_eta_00_08.root  -R pt20 eta 'abs(LepGood_eta)<0.8' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb4_${Me}_eta_08_15.root  -R pt20 eta 'abs(LepGood_eta)>0.8 && abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb4_${Me}_eta_15_20.root  -R pt20 eta 'abs(LepGood_eta)>1.479 && abs(LepGood_eta)<2.0' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,QCDEl_red,QCDEl_bjets -o $PBASE/$what/el_bnb4_${Me}_eta_20_25.root  -R pt20 eta 'abs(LepGood_eta)>2.000' ${BG} )"
        for C in 15_17.5 17.5_22.5 20_30 45_60 45_999; do
            conePtCut="-A pt20 conePt '${C%_*} < LepGood_pt*if3(LepGood_mvaTTH>${WNUM},1,0.9*(1+LepGood_jetRelIso)) && LepGood_pt*if3(LepGood_mvaTTH>${WNUM},1,0.9*(1+LepGood_jetRelIso)) < ${C#*_}' ";
            echo "( $B1 $MuDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets --pdir $PBASE/$what/mu_bnb_${Me}_eta_00_12_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.2'   --sP 'lep_.*' ${BG} )"
            echo "( $B1 $MuDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDMu_red,QCDMu_bjets,QCDMu_ljets --pdir $PBASE/$what/mu_bnb_${Me}_eta_12_24_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.2'   --sP 'lep_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets --pdir $PBASE/$what/el_bnb_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_red --ratioNums ".*" -p TT_SS_red,TT_bjets,QCDEl_red,QCDEl_bjets,QCDEl_ljets --pdir $PBASE/$what/el_bnb_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sum_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,TT_SSb._redNC,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sum_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sumold_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen TT_SS_redNC_pink --ratioNums ".*" -p TT_SS_red_viol,TT_SS_redNC_pink,QCDEl_red_El17,QCDEl_redNC_El17 --pdir $PBASE/$what/el_sumold_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_.*' ${BG} )"
            echo "( $B1 $MuDen ${BDen} ${conePtCut} --ratioDen TT_SS_redB --ratioNums ".*" -p TT_SS_red[BE],QCDMu_red[BE],QCDMu_bjets[BE] --pdir $PBASE/$what/mu_BE_${Me}_ptC_${C}/ -X pt20  --sP 'lep_.*' ${BG} )"
        done

       ##AwayJet pt variations
       MuFakeVsPt0J="$MuDen --sP '${ptJI}_${XVar}_coarsecomb' --sp TT_red --xcut 10 999 --xline 15" 
       ElFakeVsPt0J="$ElDen --sP '${ptJI}_${XVar}_coarseelcomb' --sp TT_red --xcut 10 999 --xline 15" 
       #echo "( $B0 $MuFakeVsPt0J -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPt0J -p 'TT_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt0J -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt0J -p 'TT_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
       #echo "( $B0 $MuFakeVsPt0J -p 'QCDMu_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_qajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPt0J -p 'QCDMu_red,QCDMu_red_aj[2-6].*' -o $PBASE/$what/mu_qajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt0J -p 'QCDEl_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_qajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt0J -p 'QCDEl_red,QCDEl_red_aj[2-6].*' -o $PBASE/$what/el_qajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

       ##AwayJet b-tag
       MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}_coarsecomb' --sp TT_red,TT_SSbt_black ${BDen} --xcut 10 999 --xline 15" 
       ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}_coarseelcomb' --sp TT_red,TT_SSbt_black ${BDen} --xcut 10 999 --xline 15" 
       #echo "( $B0 $MuFakeVsPtB -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPtB -p 'TT_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPtB -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
       #echo "( $B0 $ElFakeVsPtB -p 'TT_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
       #echo "( $B0 $MuFakeVsPtB -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPtB -p 'TT_SSbt_black,QCDMu_red_ajb[vlt]' -o $PBASE/$what/mu_ajbt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPtB -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
       #echo "( $B0 $ElFakeVsPtB -p 'TT_SSbt_black,QCDEl_red_ajb[vlt]' -o $PBASE/$what/el_ajbt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
       #echo "( $B0 $MuFakeVsPtB -p 'QCDMu_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPtB -p 'QCDMu_red,QCDMu_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPtB -p 'QCDEl_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
       #echo "( $B0 $ElFakeVsPtB -p 'QCDEl_red,QCDEl_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        ## Efficiencies 
        #BE="${B0/--yrange 0 0.25/--yrange 0 1.25}"
        #echo "( $BE $MuFakeVsPt -p TT_SS_red,TT_red,TT_fromW,TT_fromTau -o $PBASE/$what/mu_tteff_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2' -X jet -X mll  ${BG} )"

        MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}_fine' --sp TT_SS_red ${BDen} --xcut 10 999 --xline 15" 
        ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}_fine' --sp TT_SS_redNC ${BDen} --xcut 10 999 --xline 15" 
        # TTbar by composition
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/mu_ttvars_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_SS.*_red -o $PBASE/$what/el_ttvars_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC,TT_SS.*_redNC -o $PBASE/$what/el_ttvarsNC_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC,TT_SS.*_redNC -o $PBASE/$what/el_ttvarsNC_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        # TT by flavour
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_bjets,TT_ljets -o $PBASE/$what/mu_ftt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets,TT_ljetsNC -o $PBASE/$what/el_ftt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_bjets,TT_ljets,TT_ljetsNC -o $PBASE/$what/el_ftt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,TT_cjets,TT_ljetsNC -o $PBASE/$what/el_fttNC_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_SS_redNC,TT_bjets,TT_cjets,TT_ljetsNC -o $PBASE/$what/el_fttNC_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #QCD by flavour
        MuFakeVsPtB="$MuDen --sP '${ptJI}_${XVar}_fine' --sp QCDMu_red ${BDen} --xcut 10 999 --xline 15" 
        ElFakeVsPtB="$ElDen --sP '${ptJI}_${XVar}_fine' --sp QCDEl_redNC ${BDen} --xcut 10 999 --xline 15" 
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_bjets,QCDMu_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_bjets,QCDMu_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_redNC,QCDEl_bjets,QCDEl_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_redNC,QCDEl_bjets,QCDEl_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p TT_red,QCDMu_red,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p TT_red,QCDEl_red,QCDEl_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT tuning (qcd)
        MuFakeVsPtH="$MuDen ${BDen} --sP '${ptJI}_${XVar}_fine' --sp TT_red --xcut 10 999 --xline 15 --xline 30 --xline 45 " 
        echo "( $B0 $MuFakeVsPtH -p QCDMu_red,QCDMu_red_pt[0-9]+,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hltpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtH -p QCDMu_red,QCDMu_red_pt[0-9]+,QCDMu_red_Mu[0-9]+ -o $PBASE/$what/mu_hltpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPtH -p QCDEl_redNC_pt8,QCDEl_red_pt8,QCDEl_redNC_El8,QCDEl_red_El8 -o $PBASE/$what/el_hltid_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPtH -p QCDEl_redNC_pt8,QCDEl_red_pt8,QCDEl_redNC_El8,QCDEl_red_El8 -o $PBASE/$what/el_hltid_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        ElFakeVsPtH="$ElDen ${BDen} --sP '${ptJI}_${XVar}_fine,${ptJI}_${XVar}_coarseelcomb' --sp QCDEl_redNC_pt17 --xcut 20 999 --xline 30 " 
        echo "( $B0 $ElFakeVsPtH -p QCDEl_redNC_pt17,QCDEl_red_pt17,QCDEl_redNC_El17,QCDEl_red_El17 -o $PBASE/$what/el_hltid17_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtH -p QCDEl_redNC_pt17,QCDEl_red_pt17,QCDEl_redNC_El17,QCDEl_red_El17 -o $PBASE/$what/el_hltid17_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        ElFakeVsPtH="$ElDen ${BDen} --sP '${ptJI}_${XVar}_fine,${ptJI}_${XVar}_coarseelcomb' --sp QCDEl_redNC_pt8 --xcut 10 999 --xline 15 --xline 30 " 
        echo "( $B0 $ElFakeVsPtH -p QCDEl_redNC_pt8,QCDEl_red_pt8,QCDEl_redNC_El8,QCDEl_red_El8 -o $PBASE/$what/el_hltid8_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtH -p QCDEl_redNC_pt8,QCDEl_red_pt8,QCDEl_redNC_El8,QCDEl_red_El8 -o $PBASE/$what/el_hltid8_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        for C in 30_50 45_999; do
            conePtCut="-A pt20 conePt '${C%_*} < LepGood_pt*if3(LepGood_mvaTTH>${WNUM},1,0.9*(1+LepGood_jetRelIso)) && LepGood_pt*if3(LepGood_mvaTTH>${WNUM},1,0.9*(1+LepGood_jetRelIso)) < ${C#*_}' ";
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen QCDEl_red_pt17 --ratioNums '.*' -p QCDEl_red_pt17,QCDEl_red_El17,QCDEl_red_noEl17 --pdir $PBASE/$what/el_hltid_${Me}_eta_00_15_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)<1.479' --sP 'lep_id.*,idemu_.*' ${BG} )"
            echo "( $B1 $ElDen ${BDen} ${conePtCut} --ratioDen QCDEl_red_pt17 --ratioNums '.*' -p QCDEl_red_pt17,QCDEl_red_El17,QCDEl_red_noEl17 --pdir $PBASE/$what/el_hltid_${Me}_eta_15_25_ptC_${C}/ -R pt20 eta 'abs(LepGood_eta)>1.479' --sP 'lep_id.*,idemu_.*' ${BG} )"
        done



        # pT cut (ttbar)
        #echo "( $B0 $MuFakeVsPt -p 'TT_red,TT_pt(8|17)_red'  -o $PBASE/$what/mu_ttpt_${Me}_eta_00_12_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p 'TT_red,TT_pt12_red' -o $PBASE/$what/el_ttpt_${Me}_eta_00_15_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"

       ## TTbar conversions 
       #echo "( $B0 $MuFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/mu_ttwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/mu_ttwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/el_ttwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/el_ttwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
       ##QCD conversions
       #echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_redNC -o $PBASE/$what/mu_qcdwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPt -p QCDMu_red,QCDMu_redNC -o $PBASE/$what/mu_qcdwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_redNC -o $PBASE/$what/el_qcdwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
       #echo "( $B0 $ElFakeVsPt -p QCDEl_red,QCDEl_redNC -o $PBASE/$what/el_qcdwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #Z3l conversions
        MuFakeVsPtZ="$MuDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse' --sp TT_red --xcut 10 45" 
        ElFakeVsPtZ="$ElDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse' --sp TT_red --xcut 10 45" 
        #echo "( $B0 $MuFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/mu_z3lwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/mu_z3lwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/el_z3lwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPtZ -p Z3l_red.* -o $PBASE/$what/el_z3lwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # TTbar vs Z3l closure 
        MuFakeVsPtZ="$MuDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse2' --sp TT_red --xcut 10 30 " 
        ElFakeVsPtZ="$ElDen ${BDen} --sP '${ptJI}_${XVar}_zcoarse2' --sp TT_red --xcut 10 30 " 
        #echo "( $B0 $MuFakeVsPtZ -p TT_red,Z3l_red,Z3l_red_80 -o $PBASE/$what/mu_ttz3l_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPtZ -p TT_red,Z3l_red,Z3l_red_80 -o $PBASE/$what/mu_ttz3l_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtZ -p TT_red,Z3l_red_70  -o $PBASE/$what/el_ttz3l_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPtZ -p TT_red,Z3l_red_70  -o $PBASE/$what/el_ttz3l_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPtZ -p TT_red,TT_redNC,Z3l_red,Z3l_red_80,Z3l_redNC,Z3l_red_m3l  -o $PBASE/$what/el_ttz3lplus_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPtZ -p TT_red,TT_redNC,Z3l_red,Z3l_red_80,Z3l_redNC,Z3l_red_m3l  -o $PBASE/$what/el_ttz3lplus_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"



        #done;
done
