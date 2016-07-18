################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

BCORE=" --s2v --tree treeProducerSusyMultilepton susy-sos/lepton-mca-frstudies.txt object-studies/lepton-perlep.txt  "
if hostname | grep -q cmsco01; then
#    T="/data1/gpetrucc/TREES_TTH_260116_76X_1L"
    T="/data1/gpetrucc/TREES_80X_SOS_130716_1L "
#    T="/data1/peruzzi/2016-06-02_ewktrees76X_1LL"
else
    echo "No luck, sorry"
    exit 1
fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PLOTTER="python mcPlots.py $BCORE   "
PBASE="plots/80X/sos/fr-mc/v2.0"

BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" -j 4 & "; shift; fi

for WP in $*; do
        EleRecoPt=5; MuRecoPt=3.5; AwayJetPt=30; MuFrMax=1.0; ElFrMax=1.0
        SOS_ID="(abs(LepGood_pdgId)==13 && LepGood_softMuonId || abs(LepGood_pdgId)==11 && LepGood_eleIdHZZ)"
        SOS_DXYZ="abs(LepGood1_dxy)<0.01 && abs(LepGood_dz)<0.01"
        CONVVETO="abs(LepGood_pdgId)==13 || (LepGood_lostHits==0 && LepGood_convVeto)"
        SelDen=" -A pt20 cveto '${CONVVETO}' "
        case $WP in 
            #SOS_Iso) Num=SOS_Iso;
            #    SelDen="${SelDen} -A pt20 id '${SOS_ID}' " ;
            #    SelDen="${SelDen} -A pt20 dxyz '${SOS_DXYZ}' " ;
            #    ;;
            #SOS_IsoDxyz|SOS_noid) Num=SOS_IsoDxyz;
            #    SelDen="${SelDen} -A pt20 id '${SOS_ID}' " ; ElFrMax=0.6;
            #    ;;
            SOS_eeid) Num=SOS_IdIsoDxyz;
                SelDen="${SelDen} -A pt20 id 'abs(LepGood_pdgId)==13 || abs(LepGood_pdgId)==11 && eleWPVVL(LepGood_pt,LepGood_etaSc,LepGood_mvaIdSpring15)' " ; 
                ;;
            #SOS_eeid_sip6) Num=SOS_IdIsoDxyz;
            #    SelDen="${SelDen} -A pt20 id 'abs(LepGood_pdgId)==13 || abs(LepGood_pdgId)==11 && eleWPVVL(LepGood_pt,LepGood_etaSc,LepGood_mvaIdSpring15)' " ;  
            #    SelDen="${SelDen} -A pt20 dxyz '(${SOS_DXYZ} || LepGood_sip3d < 4)' " ;
            #    ElFrMax=0.6;
            #    ;;
            #SOS_IdIsoDxyz|SOS_full) Num=SOS_IdIsoDxyz; ElFrMax=0.6
            #    ;;
            *)
                echo "Missing ID $WP";
                exit 1;;
        esac
        B0="$BASE -P $T susy-sos/make_fake_rates_sels.txt susy-sos/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        B0="$B0 --legend=TR --showRatio --ratioRange 0.0 1.99  "
	P0="${PLOTTER} -P $T susy-sos/make_fake_rates_xvars.txt"
	#B1="${B1} --mcc susy-sos/mcc-eleIdEmu2.txt  "
        P0="$P0 --showRatio  -f "
        P1="$P0 --plotmode=norm  "
        P2="$P0 --plotmode=nostack -e "
        JetDen="-A pt20 mll 'nLepGood == 1'"
        CommonDen="${JetDen} ${SelDen}  "
        #CommonDen="${CommonDen} -A pt20 fake 'LepGood_mcMatchId==0' "
        MuDen="${CommonDen}       -A pt20 mupt 'LepGood_pt > ${MuRecoPt}'  "
        ElDen="${CommonDen} -I mu -A pt20 elpt 'LepGood_pt > ${EleRecoPt}'"
        for BVar in bAny; do # bMedium; do 
        RVar=${AwayJetPt}; 
        case $BVar in
            bAny)    BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar ' " ;;
            bVeto)   BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV < 0.605' " ;;
            bLoose)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.605' " ;;
            bMedium) BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.89'  " ;;
            bTight)  BDen="-A pt20 jet 'LepGood_awayJet_pt > $RVar && LepGood_awayJet_btagCSV > 0.97'  " ;;
        esac;
        Me="wp${WP}_rec${RVar}_${BVar}"

        MuFakeVsPt="$MuDen ${BDen} --sP 'pt_fine' --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999 " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'pt_fine' --yrange 0 ${ElFrMax} --xcut ${EleRecoPt} 999 " 

        #for J in ljets bjets red; do 
        #    echo "( $P2 $MuDen ${BDen} --sP 'pt_fine' --ratioDen QCD_${J} --ratioNums QCD_${J} -p QCD_${J},QCD_${J} --pdir $PBASE/$what/mu_${Me}_eta_00_12/QCD_${J} -R pt20 eta 'abs(LepGood_eta)<1.2' ${BG} )"
        #    echo "( $P2 $MuDen ${BDen} --sP 'pt_fine' --ratioDen QCD_${J} --ratioNums QCD_${J} -p QCD_${J},QCD_${J} --pdir $PBASE/$what/mu_${Me}_eta_12_24/QCD_${J} -R pt20 eta 'abs(LepGood_eta)>1.2' ${BG} )"
        #done
        for PlotPtMin in 5 10 15; do
            continue
            PlotPtMax=$((PlotPtMin + 5))
            PtBin="pt_${PlotPtMin}_${PlotPtMax}"; PtCut="${PlotPtMin} < LepGood_pt && LepGood_pt <= ${PlotPtMax}"
            Procs="-p QCD_red,WJ_red,TT_red,Z3l_red_80 --ratioDen WJ_red --ratioNums '.*' --maxRatioRange 0 2";
            echo "( $P1 $MuDen ${BDen} --sP 'lep_.*,mu_.*' ${Procs} --pdir $PBASE/$what/mu_${Me}_eta_00_12_${PtBin}/ -R pt20 eta 'abs(LepGood_eta)<1.2 && ${PtCut}' ${BG} )"
            echo "( $P1 $MuDen ${BDen} --sP 'lep_.*,mu_.*' ${Procs} --pdir $PBASE/$what/mu_${Me}_eta_12_24_${PtBin}/ -R pt20 eta 'abs(LepGood_eta)>1.2 && ${PtCut}' ${BG} )"
            echo "( $P1 $ElDen ${BDen} --sP 'lep_.*,el_.*' ${Procs} --pdir $PBASE/$what/el_${Me}_eta_00_15_${PtBin}/ -R pt20 eta 'abs(LepGood_eta)<1.479 && ${PtCut}' ${BG} )"
            echo "( $P1 $ElDen ${BDen} --sP 'lep_.*,el_.*' ${Procs} --pdir $PBASE/$what/el_${Me}_eta_15_25_${PtBin}/ -R pt20 eta 'abs(LepGood_eta)>1.479 && ${PtCut}' ${BG} )"
        done
	
        echo "( $B0 $MuFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/mu_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/mu_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/el_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/el_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        continue

        echo "( $B0 $MuFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/mu_met_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/mu_met_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/el_met_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/el_met_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        #echo "( $B0 $MuFakeVsPt -p WJ_bjets,TT_bjets,QCD_bjets --sp WJ_red -o $PBASE/$what/mu_b_${Me}_eta_00_12.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        #echo "( $B0 $MuFakeVsPt -p WJ_bjets,TT_bjets,QCD_bjets --sp WJ_red -o $PBASE/$what/mu_b_${Me}_eta_12_24.root  -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p WJ_bjets,TT_bjets,QCD_bjets --sp WJ_red -o $PBASE/$what/el_b_${Me}_eta_00_15.root  -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        #echo "( $B0 $ElFakeVsPt -p WJ_bjets,TT_bjets,QCD_bjets --sp WJ_red -o $PBASE/$what/el_b_${Me}_eta_15_25.root  -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # Closure VS MET
        echo "( $B0 $MuFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/mu_wjmet_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/mu_wjmet_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/el_wjmet_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/el_wjmet_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/mu_ttmet_${Me}_eta_00_12.root    -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/mu_ttmet_${Me}_eta_12_24.root    -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/el_ttmet_${Me}_eta_00_15.root    -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/el_ttmet_${Me}_eta_15_25.root    -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # Z+l closure 
        MuFakeVsPtZ="$MuDen ${BDen} --sP 'pt_fine' --sp WJ_red --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999 " 
        ElFakeVsPtZ="$ElDen ${BDen} --sP 'pt_fine' --sp WJ_red --yrange 0 ${ElFrMax} --xcut ${EleRecoPt} 999 " 
        echo "( $B0 $MuFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_T -o $PBASE/$what/mu_z3l_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_T -o $PBASE/$what/mu_z3l_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_80,Z3l_red_T -o $PBASE/$what/el_z3l_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_80,Z3l_red_T -o $PBASE/$what/el_z3l_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet pt variations
        MuFakeVsPt0J="$MuDen --sP 'pt_fine' --sp WJ_red --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999" 
        ElFakeVsPt0J="$ElDen --sP 'pt_fine' --sp WJ_red --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999" 
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,WJ_red,QCD_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,WJ_red,QCD_red_aj[2-6].*' -o $PBASE/$what/mu_ajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,WJ_red,QCD_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,WJ_red,QCD_red_aj[2-6].*' -o $PBASE/$what/el_ajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'QCD_red,QCD_red_aj[2-6].*' -o $PBASE/$what/mu_qajpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'QCD_red,QCD_red_aj[2-6].*' -o $PBASE/$what/mu_qajpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'QCD_red,QCD_red_aj[2-6].*' -o $PBASE/$what/el_qajpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'QCD_red,QCD_red_aj[2-6].*' -o $PBASE/$what/el_qajpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet b-tag
        MuFakeVsPtB="$MuDen --sP 'pt_fine' --sp WJ_red -A pt20 jet 'LepGood_awayJet_pt > $RVar ' " 
        ElFakeVsPtB="$ElDen --sP 'pt_fine' --sp WJ_red -A pt20 jet 'LepGood_awayJet_pt > $RVar ' " 
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        break
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
        echo "( $B0 $MuFakeVsPt -p QCD_red,QCD_bjets,QCD_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCD_red,QCD_bjets,QCD_ljets -o $PBASE/$what/mu_fqcd_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCD_red,QCD_bjets,QCD_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCD_red,QCD_bjets,QCD_ljets  -o $PBASE/$what/el_fqcd_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT
        echo "( $B0 $MuFakeVsPt -p TT_red,QCD_red,QCD_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,QCD_red,QCD_red_Mu[0-9]+ -o $PBASE/$what/mu_hlt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCD_red,QCD_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,QCD_red,QCD_red_El[0-9]+ -o $PBASE/$what/el_hlt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # HLT tuning (qcd)
        echo "( $B0 $MuFakeVsPt -p QCD_red,QCD_red_pt[0-9]+,QCD_red_Mu[0-9]+,QCD_red_pt17+ -o $PBASE/$what/mu_hltpt_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCD_red,QCD_red_pt[0-9]+,QCD_red_Mu[0-9]+,QCD_red_pt17+ -o $PBASE/$what/mu_hltpt_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCD_red,QCD_red_pt[0-9]+,QCD_red_El[0-9]+ -o $PBASE/$what/el_hltpt_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCD_red,QCD_red_pt[0-9]+,QCD_red_El[0-9]+ -o $PBASE/$what/el_hltpt_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # pT cut (ttbar)
        echo "( $B0 $MuFakeVsPt -p 'TT_red,TT_pt(8|17)_red'  -o $PBASE/$what/mu_ttpt_${Me}_eta_00_12_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p 'TT_red,TT_pt12_red' -o $PBASE/$what/el_ttpt_${Me}_eta_00_15_ttpt.root  -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"

        # TTbar conversions 
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/mu_ttwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/mu_ttwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/el_ttwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_redNC -o $PBASE/$what/el_ttwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        #QCD conversions
        echo "( $B0 $MuFakeVsPt -p QCD_red,QCD_redNC -o $PBASE/$what/mu_qcdwcnc_${Me}_eta_00_12.root -R pt20 eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p QCD_red,QCD_redNC -o $PBASE/$what/mu_qcdwcnc_${Me}_eta_12_24.root -R pt20 eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCD_red,QCD_redNC -o $PBASE/$what/el_qcdwcnc_${Me}_eta_00_15.root -R pt20 eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p QCD_red,QCD_redNC -o $PBASE/$what/el_qcdwcnc_${Me}_eta_15_25.root -R pt20 eta 'abs(LepGood_eta)>1.479' ${BG} )"

        done;
done
