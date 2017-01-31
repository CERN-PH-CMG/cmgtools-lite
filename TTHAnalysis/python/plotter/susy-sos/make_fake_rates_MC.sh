################################
#  use mcEfficiencies.py to make plots of the fake rate
################################

BCORE=" --s2v --tree treeProducerSusyMultilepton susy-sos/lepton-mca-frstudies.txt susy-sos/qcd1l.txt -X minimal -L susy-sos/functionsSOS.cc  "
if hostname | grep -q cmsco01; then
     T="/data1/gpetrucc/TREES_80X_SOS_171116_NoIso_1L"
else
    T="/afs/cern.ch/user/g/gpetrucc/w/LINKS_80X_SOS_171116_NoIso_1L "
fi
BASE="python mcEfficiencies.py $BCORE --ytitle 'Fake rate'   "
PLOTTER="python mcPlots.py $BCORE   "
PBASE="plots/80X/sos/fr-mc/v3.1"

BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" -j 4 & "; shift; fi

for WP in $*; do
        ElRecoPt=5; MuRecoPt=3.5; AwayJetPt=90; MuFrMax=1.0; ElFrMax=1.0;  MaxR=1.99
        SOS_DXYZ="abs(LepGood_dxy)<0.01 && abs(LepGood_dz)<0.01"
        CONVVETO="abs(LepGood_pdgId)==13 || (LepGood_lostHits==0 && LepGood_convVeto)"
        ICHEP_LOOSE="-A entry icheploose 'LepGood_sip3d < 8 && LepGood_RelIsoMIV04*LepGood_pt < 10' "
        DXYDZ_LOOSE="-A entry dxyzs 'LepGood_sip3d < 8 && ${SOS_DXYZ} && LepGood_jetBTagCSV < 0.46' "
        IP3D_LOOSE="-A entry dxyzs 'abs(LepGood_ip3d)<0.01 && LepGood_sip3d < 2 && LepGood_jetBTagCSV < 0.46' "
        IP3D_VLOOSE="-A entry dxyzs 'abs(LepGood_ip3d)<0.0175 && LepGood_sip3d < 2.5 && LepGood_jetBTagCSV < 0.46' "
        IP3D_VVLOOSE="-A entry dxyzs 'abs(LepGood_ip3d)<0.04 && LepGood_sip3d < 4 && LepGood_jetBTagCSV < 0.46' "
        ID_LOOSE="-A entry iloose '(abs(LepGood_pdgId)==13 && LepGood_ICHEPsoftMuonId || abs(LepGood_pdgId)==11 && eleWPVVL(LepGood_pt,LepGood_etaSc,LepGood_mvaIdSpring15))' "
        EID_LOOSE="-A entry iloose '(abs(LepGood_pdgId)==13 || abs(LepGood_pdgId)==11 && eleWPVVL(LepGood_pt,LepGood_etaSc,LepGood_mvaIdSpring15))' "
        SelDen=" -A entry cveto '${CONVVETO}' "
        case $WP in 
            SOS_ichep) Num=ICHEP_IdIsoDxyz; 
                SelDen="${SelDen} ${ICHEP_LOOSE} ${EID_LOOSE} " ; 
                ;;
            SOS_dxyzden) Num=ICHEP_Full;  MuFrMax=0.2; ElFrMax=0.3; MaxR=4.99
                SelDen="${SelDen} ${DXYDZ_LOOSE} ${EID_LOOSE}  " ; 
                ;;
            SOS_ip3d*) Num=IP3D_Full;  MuFrMax=0.5; ElFrMax=0.5;  MaxR=1.99
                SelDen="${SelDen} ${ID_LOOSE}  " ; 
                case $WP in
                    ## Anti-diagonal cut ptd_xx_yy := (pt-5)/xx + abiso < yy 
                    ##    the v3.0 fake rates correspond to xx = 3, yy = 20, as used for the presentation on the leptonic meeting on 25/11/16 (AwayJetPt 50)
                    *_ptd_*)    CUT1=$(perl -e "qq^$WP^ =~ /.*_ptd_([0-9\.]+)_([0-9\.]+)/ and print \$1"); 
                                CUT2=$(perl -e "qq^$WP^ =~ /.*_ptd_([0-9\.]+)_([0-9\.]+)/ and print \$2"); 
                                SelDen="${SelDen}  -A entry ptd '(LepGood_pt-5)/$CUT1 + LepGood_pt*LepGood_relIso03 < $CUT2' ";; 
                    ## Hyperbolic cut: pti_xx_yy := absiso < xx / pt + yy
                    ##    the v3.1 fake rates correspond to xx = 300, yy = 20, and are to be used with AwayJetPt > 90
                    *_pti_*)    CUT1=$(perl -e "qq^$WP^ =~ /.*_pti_([0-9\.]+)_([0-9\.]+)/ and print \$1"); 
                                CUT2=$(perl -e "qq^$WP^ =~ /.*_pti_([0-9\.]+)_([0-9\.]+)/ and print \$2"); 
                                SelDen="${SelDen}  -A entry pti 'LepGood_pt*LepGood_relIso03 < $CUT1/LepGood_pt + $CUT2' ";; 
                    ## Cone pt cut:  ptcXYZ := (pt + absiso) < XYZ; XYZ must be an integer
                    *_ptc[0-9]*) CUT=$(perl -e "qq^$WP^ =~ /.*_ptc(\d+)/ and print \$1");
                                 SelDen="${SelDen} -A entry ptc '(1+LepGood_relIso03)*LepGood_pt < $CUT' ";;
                    ## Absolute isolation cut:  aisoXYZ := absiso < XYZ; XYZ must be an integer
                    *_aiso[0-9]*) CUT=$(perl -e "qq^$WP^ =~ /.*_aiso(\d+)/ and print \$1");
                                 SelDen="${SelDen} -A entry aiso 'LepGood_relIso03*LepGood_pt < $CUT' ";;
                    ## Relative isolation cut:  risoXYZ := reliso < XYZ; XYZ can be a float
                    *_riso[0-9.]*) CUT=$(perl -e "qq^$WP^ =~ /.*_riso([0-9.]+)/ and print \$1");
                                 SelDen="${SelDen} -A entry riso 'LepGood_relIso03 < $CUT' ";;
                esac;
                ### Further postfix can be specified to change the IP3D sideband
                case $WP in
                    ## VVLoose: ip3d < 0.04 , sip3d < 4.0  (doesn't close that well)
                    *_ipvvl) SelDen="${SelDen} ${IP3D_VVLOOSE}" ;;
                    ## Loose: ip3d < 0.01 , sip3d < 2.0 (fake rate is a bit larger)
                    *_ipl) SelDen="${SelDen} ${IP3D_LOOSE}" ;;
                    ## DEFAULT = VLoose: ip3d < 0.0175 , sip3d < 2.5 (closes fine)
                    *) SelDen="${SelDen} ${IP3D_VLOOSE}";;
                esac;
                ;;
            *)
                echo "Missing ID $WP";
                exit 1;;
        esac
        B0="$BASE -P $T susy-sos/make_fake_rates_sels.txt susy-sos/make_fake_rates_xvars.txt --groupBy cut --sP ${Num} " 
        B0="$B0 --legend=TR --showRatio --ratioRange 0.0 ${MaxR}  "
	P0="${PLOTTER} -P $T susy-sos/make_fake_rates_xvars.txt"
        P0="$P0 --showRatio  -f "
        P1="$P0 --plotmode=norm  "
        P2="$P0 --plotmode=nostack -e "
        CommonDen="${SelDen} -A entry mll 'nLepGood == 1' "
        MuDen="${CommonDen} -E ^mu -A entry mupt 'LepGood_pt > ${MuRecoPt}'  "
        ElDen="${CommonDen} -E ^el -A entry elpt 'LepGood_pt > ${ElRecoPt}'"

        BVar="bAny" 
        case $BVar in
            bAny)    BDen="-A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} ' " ;;
            bVeto)   BDen="-A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} && LepGood_awayJet_btagCSV < 0.605' " ;; ## FIXME to be updated
            bLoose)  BDen="-A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} && LepGood_awayJet_btagCSV > 0.605' " ;;
            bMedium) BDen="-A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} && LepGood_awayJet_btagCSV > 0.89'  " ;;
            bTight)  BDen="-A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} && LepGood_awayJet_btagCSV > 0.97'  " ;;
        esac;
        if (( ${AwayJetPt} >=  80 )); then BDen="${BDen} --xf QCD_Pt30to50"; fi
        if (( ${AwayJetPt} >= 120 )); then BDen="${BDen} --xf QCD_Pt50to80"; fi

        Me="wp${WP}_rec${AwayJetPt}_${BVar}"

        MuFakeVsPt="$MuDen ${BDen} --sP 'pt_fine' --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999 " 
        ElFakeVsPt="$ElDen ${BDen} --sP 'pt_fine' --yrange 0 ${ElFrMax} --xcut ${ElRecoPt} 999 " 

        ## ============== DISTRIBUTION PLOTS ===============
        #
        #for PlotPtMin in 6 10 15; do
        #    PlotPtMax=$((PlotPtMin + 2))
        #    PtBin="pt_${PlotPtMin}_${PlotPtMax}"; PtCut="${PlotPtMin} < LepGood_pt && LepGood_pt <= ${PlotPtMax}"
        #    Procs="-p QCD_red,WJ_red,TT_red --ratioDen WJ_red --ratioNums '.*' --maxRatioRange 0 2";
        #    echo "( $P1 $MuDen ${BDen} --sP 'lep_.*,mu_.*' ${Procs} --pdir $PBASE/$what/mu_${Me}_eta_00_12_${PtBin}/ -A entry eta 'abs(LepGood_eta)<1.2 && ${PtCut}' ${BG} )"
        #    echo "( $P1 $MuDen ${BDen} --sP 'lep_.*,mu_.*' ${Procs} --pdir $PBASE/$what/mu_${Me}_eta_12_24_${PtBin}/ -A entry eta 'abs(LepGood_eta)>1.2 && ${PtCut}' ${BG} )"
        #    echo "( $P1 $ElDen ${BDen} --sP 'lep_.*,el_.*' ${Procs} --pdir $PBASE/$what/el_${Me}_eta_00_15_${PtBin}/ -A entry eta 'abs(LepGood_eta)<1.479 && ${PtCut}' ${BG} )"
        #    echo "( $P1 $ElDen ${BDen} --sP 'lep_.*,el_.*' ${Procs} --pdir $PBASE/$what/el_${Me}_eta_15_25_${PtBin}/ -A entry eta 'abs(LepGood_eta)>1.479 && ${PtCut}' ${BG} )"
        #done

        ## === BASIC MC CLOSURE TEST ====	
        echo "( $B0 $MuFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/mu_${Me}_eta_00_12.root    -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/mu_${Me}_eta_12_24.root    -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/el_${Me}_eta_00_15.root    -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,TT_red,QCD_red --sp WJ_red -o $PBASE/$what/el_${Me}_eta_15_25.root    -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"

        echo "( $B0 $MuFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/mu_met_${Me}_eta_00_12.root    -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/mu_met_${Me}_eta_12_24.root    -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/el_met_${Me}_eta_00_15.root    -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red_met100,TT_red_met100,QCD_red --sp WJ_red_met100 -o $PBASE/$what/el_met_${Me}_eta_15_25.root    -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"

        # Closure VS MET
        echo "( $B0 $MuFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/mu_wjmet_${Me}_eta_00_12.root    -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/mu_wjmet_${Me}_eta_12_24.root    -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/el_wjmet_${Me}_eta_00_15.root    -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p WJ_red,WJ_red_met.* --sp WJ_red -o $PBASE/$what/el_wjmet_${Me}_eta_15_25.root    -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/mu_ttmet_${Me}_eta_00_12.root    -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/mu_ttmet_${Me}_eta_12_24.root    -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/el_ttmet_${Me}_eta_00_15.root    -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPt -p TT_red,TT_red_met.* --sp TT_red -o $PBASE/$what/el_ttmet_${Me}_eta_15_25.root    -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"

       ## Z+l closure 
       #MuFakeVsPtZ="$MuDen ${BDen} --sP 'pt_fine' --sp WJ_red --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999 " 
       #ElFakeVsPtZ="$ElDen ${BDen} --sP 'pt_fine' --sp WJ_red --yrange 0 ${ElFrMax} --xcut ${ElRecoPt} 999 " 
       #echo "( $B0 $MuFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_T -o $PBASE/$what/mu_z3l_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
       #echo "( $B0 $MuFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_T -o $PBASE/$what/mu_z3l_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
       #echo "( $B0 $ElFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_80,Z3l_red_T -o $PBASE/$what/el_z3l_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479'   ${BG} )"
       #echo "( $B0 $ElFakeVsPtZ -p WJ_red,TT_red,Z3l_red,Z3l_red_80,Z3l_red_T -o $PBASE/$what/el_z3l_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet pt variations
        MuFakeVsPt0J="$MuDen --sP 'pt_fine' --sp WJ_red --yrange 0 ${MuFrMax} --xcut ${MuRecoPt}  999" 
        ElFakeVsPt0J="$ElDen --sP 'pt_fine' --sp WJ_red --yrange 0 ${ElFrMax} --xcut ${ElRecoPt}  999" 
        if (( ${AwayJetPt} >=  80 )); then QCDjpt="QCD_red_aj[67891].*"; else QCDjpt="QCD_red_aj[34567].*"; fi;
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,WJ_red,$QCDjpt' -o $PBASE/$what/mu_ajpt_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p 'TT_red,WJ_red,$QCDjpt' -o $PBASE/$what/mu_ajpt_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,WJ_red,$QCDjpt' -o $PBASE/$what/el_ajpt_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p 'TT_red,WJ_red,$QCDjpt' -o $PBASE/$what/el_ajpt_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p '$QCDjpt' --sp QCD_red_aj${AwayJetPt} -o $PBASE/$what/mu_qajpt_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPt0J -p '$QCDjpt' --sp QCD_red_aj${AwayJetPt} -o $PBASE/$what/mu_qajpt_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p '$QCDjpt' --sp QCD_red_aj${AwayJetPt} -o $PBASE/$what/el_qajpt_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479'   ${BG} )"
        echo "( $B0 $ElFakeVsPt0J -p '$QCDjpt' --sp QCD_red_aj${AwayJetPt} -o $PBASE/$what/el_qajpt_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479'   ${BG} )"

        #AwayJet b-tag
        MuFakeVsPtB="$MuDen --sP 'pt_fine' --sp WJ_red -A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} ' " 
        ElFakeVsPtB="$ElDen --sP 'pt_fine' --sp WJ_red -A entry jet 'LepGood_awayJet_pt > ${AwayJetPt} ' " 
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/mu_ajb_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'TT_red,WJ_red,QCD_red_ajb.*' -o $PBASE/$what/el_ajb_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $B0 $MuFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/mu_qajb_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $B0 $ElFakeVsPtB -p 'QCD_red,QCD_red_ajb.*' -o $PBASE/$what/el_qajb_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"

        ## Prompt rate (note: this one is tricky)
        BP="${B0/lepton-mca-frstudies.txt/mca-2los-test-mc.txt} --Fs {P}/0_both3dCleanLoose_noIso_v2 --mcc susy-sos/lepchoice-recleaner.txt"
        BP="${BP/data1/data}";
        BP="${BP/legend=TR/legend=BR}";
        BP="${BP/Fake rate/Prompt rate}";
        BP="${BP/TREES_80X_SOS_171116_NoIso_1L/TREES_80X_SOS_111016_NoIso}";
        BP="${BP/qcd1l.txt/2los_tight.txt} -X ^FF -X ^TT"
        BP="${BP} -A entry prompt 'LepGood_mcMatchId != 0'  "
        MuPR="${MuDen/nLepGood == 1/nLepGood == 2} -A entry mu 'abs(LepGood_pdgId) == 13' --sP 'pt_fine' --yrange 0.0 1.0 ";
        ElPR="${ElDen/nLepGood == 1/nLepGood == 2} -A entry mu 'abs(LepGood_pdgId) == 11' --sP 'pt_fine' --yrange 0.0 1.0 " 
        ### Prompt rate (tight SR cuts)
        echo "( $BP $MuPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/mu_pr_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BP $MuPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/mu_pr_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $BP $ElPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/el_pr_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BP $ElPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/el_pr_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"
        ### Prompt rate (relaxed SR cuts)
        BP="${BP} -X Upsilon -X METovHT -X ISRjet -X bveto -X mtautau  "
        echo "( $BP $MuPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/mu_prB_${Me}_eta_00_12.root -A entry eta 'abs(LepGood_eta)<1.2'   ${BG} )"
        echo "( $BP $MuPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/mu_prB_${Me}_eta_12_24.root -A entry eta 'abs(LepGood_eta)>1.2'   ${BG} )"
        echo "( $BP $ElPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/el_prB_${Me}_eta_00_15.root -A entry eta 'abs(LepGood_eta)<1.479' ${BG} )"
        echo "( $BP $ElPR --pg PromptBkg:=TT,DYJets,VV -p PromptBkg,T2tt_dm30 -o $PBASE/$what/el_prB_${Me}_eta_15_25.root -A entry eta 'abs(LepGood_eta)>1.479' ${BG} )"

done
