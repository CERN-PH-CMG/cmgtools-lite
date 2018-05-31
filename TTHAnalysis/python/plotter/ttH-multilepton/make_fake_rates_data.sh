################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T_SUSY="/data1/peruzzi/TREES_80X_011216_Spring16MVA_1lepFR --FDs /data1/peruzzi/frQCDVars_skimdata"
T_TTH=/afs/cern.ch/work/g/gpetrucc/TREES_94X_FR_240518
if hostname | grep -q cmsco01; then
    T_TTH=/data1/gpetrucc/TREES_94X_FR_240518
elif hostname | grep -q cmsphys10; then
    T_TTH=/data/g/gpetrucc/TREES_94X_FR_240518
fi
ANALYSIS=$1; if [[ "$1" == "" ]]; then exit 1; fi; shift;
case $ANALYSIS in
ttH) T="${T_TTH}"; CUTFILE="ttH-multilepton/qcd1l.txt"; XVAR="ptJI90_mvaPt090_coarse"; NUM="mvaPt_090i";;
#susy_wpM) T="${T_SUSY}"; CUTFILE="susy-ewkino/qcd1l_wpM.txt"; XVAR="ptJIMIX4_mvaSusy_sMi_coarselongbin"; NUM="mvaSusy_sMi";;
#susy_wpV) T="${T_SUSY}"; CUTFILE="susy-ewkino/qcd1l_wpV.txt"; XVAR="ptJIMIX3_mvaSusy_sVi_coarselongbin"; NUM="mvaSusy_sVi";;
#susy_RA7) T="${T_SUSY}"; CUTFILE="susy-ewkino/qcd1l_RA7.txt"; XVAR="conePt_RA7_coarselongbin"; NUM="ra7_tight";;
susy*) echo "NOT UP TO DATE"; exit 1;;
*) echo "You did not specify the analysis"; exit 1;;
esac;
BCORE=" --s2v --tree treeProducerSusyMultilepton ttH-multilepton/mca-qcd1l.txt ${CUTFILE} -P $T -l 41.7 --AP  --WA prescaleFromSkim  "
BCORE="${BCORE} --Fs {P}/1_jetPtRatiov3_v1 --mcc ttH-multilepton/mcc-ptRatiov3.txt "
BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt  "; 
#BCORE="${BCORE} --mcc ttH-multilepton/mcc-noHLTinMC-some.txt  "; 

MVAWP=90

BG=" -j 8 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
lepdir=${lepton};
case $lepton in
mu) BCORE="${BCORE} -E ^${lepton} --xf 'SingleEl.*'  "; QCD=QCDMu; ;;
el) BCORE="${BCORE} -E ^${lepton} --xf 'DoubleMu.*,SingleMu.*' "; QCD=QCDEl; ;;
loose_mu) 
    lepdir=$1; lepton="mu"; MVAWP=75; CUTPREFIX="mva0${MVAWP}_"; NUM="mvaPt_0${MVAWP}i";
    BCORE="${BCORE} -E ^${lepton} --xf 'SingleEl.*'  "; QCD=QCDMu; ;;
loose_el) 
    lepdir=$1; lepton="el"; MVAWP=75; CUTPREFIX="mva0${MVAWP}_"; NUM="mvaPt_0${MVAWP}i";
    BCORE="${BCORE} -E ^${lepton} --xf 'DoubleMu.*,SingleMu.*' "; QCD=QCDEl; ;;
#mu_jet) lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 40'  "; QCD=QCDMu; ;;
#mu_jet6) lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*,JetHT_.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 60'  "; QCD=QCDMu; ;;
#mu_ht)  lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'Double.*' -X idEmuCut -R minimal ptj40 ' LepGood_awayJet_pt > 40'  "; QCD=QCDMu; ;;
#mu_any)  lepton="mu"; BCORE="${BCORE} -E ${lepton} --xf 'DoubleEG.*' -X idEmuCut  "; QCD=QCDMu; ;;
esac;

trigger=$2; if [[ "$2" == "" ]]; then exit 1; fi
conept="LepGood_pt*if3(LepGood_mvaTTH>0.${MVAWP}&&LepGood_mediumMuonId>0, 1.0, 0.90/LepGood_jetPtRatiov2)"
case $trigger in
#PFJet6)
#    BCORE="${BCORE} -E HLT_PFJet6   "; 
#    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
#    ;;
Mu3_PFJet40)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>4.0 && LepGood_awayJet_pt>45'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu8)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>8 && $conept > 13'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu17)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>17 && $conept > 25' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu20)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>20 && $conept > 30' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu27)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>27 && $conept > 40' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
Mu50)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>50 && $conept > 75' "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
MuX_Combined)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>8.5'  "; 
    PUW=" "
    ;;
MuX_OR)
    BCORE="${BCORE} -E ^${CUTPREFIX}trigMu -E ^${CUTPREFIX}conePt10 -E ^${CUTPREFIX}notConePt100 "; 
    CONEPTVAR="ptJI90_mvaPt0${MVAWP}_coarsecomb"
    PUW="-L ttH-multilepton/frPuReweight.cc -W 'coneptw$trigger($conept,nVert)' "
    ;;
Ele8|Ele8_CaloIdM_TrackIdM_PFJet30)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_Ele8_CaloIdM_TrackIdM_PFJet30' -A veto recoptfortrigger 'LepGood_pt>8 && $conept > 13'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puwEle8(nVert)' "
    ;;
Ele17|Ele17_CaloIdM_TrackIdM_PFJet30)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_Ele17_CaloIdM_TrackIdM_PFJet30' -A veto recoptfortrigger 'LepGood_pt>17 && $conept > 25'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puwEle17(nVert)' "
    ;;
Ele23|Ele23_CaloIdM_TrackIdM_PFJet30)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_Ele23_CaloIdM_TrackIdM_PFJet30' -A veto recoptfortrigger 'LepGood_pt>23 && $conept > 32'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puwEle23(nVert)' "
    ;;
EleX_Combined)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}' -A veto recoptfortrigger 'LepGood_pt>8.5' --xf 'SingleMu.*'  "; 
    PUW=" "
    ;;
EleX_OR)
    BCORE="${BCORE} -E ^${CUTPREFIX}trigEl -E ^${CUTPREFIX}conePt15 -E ^${CUTPREFIX}notConePt100 "; 
    CONEPTVAR="ptJI90_mvaPt0${MVAWP}_coarseelcomb"
    PUW="-L ttH-multilepton/frPuReweight.cc -W 'coneptw$trigger($conept,nVert)' "
    ;;
*)
    BCORE="${BCORE} -A veto trigger 'HLT_FR_${trigger}'  "; 
    PUW=" -L ttH-multilepton/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
esac;


what=$3;
more=$4
PBASE="plots/94X/${ANALYSIS}/lepMVA/v2.0-dev/fr-meas/qcd1l/$lepdir/HLT_$trigger/$what/$more"

EWKONE="-p ${QCD}_red,EWK,data"
EWKSPLIT="-p ${QCD}_red,WJets,DYJets,Top,data"
QCDEWKSPLIT="-p ${QCD}_[bclg]jets,WJets,DYJets,Top,data"
FITEWK=" $EWKSPLIT --flp WJets,DYJets,Top,${QCD}_red --peg-process DYJets WJets --peg-process Top WJets "
QCDNORM=" $QCDEWKSPLIT --sp WJets,DYJets,${QCD}_.jets --scaleSigToData  "
QCDFITEWK=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[clg]jets ${QCD}_bjets "
QCDFITQCD=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[gl]jets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "
QCDFITALL=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_gjets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "

case $lepton in
    el) BARREL="00_15"; ENDCAP="15_25"; ETA="1.479";;
    mu) BARREL="00_12"; ENDCAP="12_24"; ETA="1.2";;
esac;

if [[ "$more" != "" ]]; then
    shift 4; BCORE="$BCORE $*";
    echo "Adding the following options for $more: $*" 1>&2 
fi;

case $what in
    nvtx)
        echo "python mcPlots.py -f -j 6 $BCORE ttH-multilepton/qcd1l_plots.txt --pdir $PBASE --sP nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ../tools/vertexWeightFriend.py _puw$trigger $PBASE/qcd1l_plots.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining a puw$trigger ----- ' ";
        ;;
    coneptw)
        echo "python mcPlots.py -f -j 6 $BCORE ttH-multilepton/make_fake_rates_xvars.txt --pdir $PBASE --sP ${CONEPTVAR}_nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ttH-multilepton/frConePtWeights.py coneptw$trigger $PBASE/make_fake_rates_xvars.root ${CONEPTVAR}_nvtx  ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining a coneptw$trigger ----- ' ";
        ;;
    coneptw-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/make_fake_rates_xvars.txt --pdir $PBASE --sP ${CONEPTVAR}_nvtx,$CONEPTVAR,nvtx $EWKONE " 
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.9 1.1 " 
        ;;
    mc-yields)
        echo "python mcAnalysis.py -f -j 6 $BCORE $PUW ${EWKSPLIT} --sp 'QCD.*' --fom S/B --fom S/errSB -G " 
        ;;
    fit-*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit-/} --showRatio --maxRatioRange 0.0 1.99 --fixRatioRange " 
        ;;
    num-fit-*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit-/} --showRatio --maxRatioRange 0.0 1.99 --fixRatioRange -E num" 
        ;;
    num-mcshapes)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what ${EWKSPLIT/,data/} -E num --plotmode=nostack" 
        ;;
    qcdflav-norm)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDNORM --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    qcdflav-fit)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDFITEWK --preFitData ${what/flav-fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    flav-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDFITQCD --preFitData ${what/flav-fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    flav3-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW ttH-multilepton/qcd1l_plots.txt --pdir $PBASE -E $what $QCDFITALL --preFitData ${what/flav3-fit/} --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}
        XVAR="ptJI90_mvaPt090_coarselongbin"
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 2.99 "
        STACK="python ttH-multilepton/stack_fake_rates_data.py "
        ISCOMB=false
        ISWIDE=false
        case $lepton in  
           el) 
               case $trigger in
                   Ele8)
                       XVAR="${XVAR/_coarselongbin/_coarseel8bin}"
                       RANGES="$RANGES  --yrange 0 0.25  --xcut 13 45 --xline 15 --xline 25 " ;;
                   Ele17)
                       XVAR="${XVAR/_coarselongbin/_coarseel17bin}"
                       RANGES="$RANGES  --yrange 0 0.25  --xcut 25 100 --xline 25 --xline 35 " ;;
                   Ele23)
                       XVAR="${XVAR/_coarselongbin/_coarseel23bin}"
                       RANGES="$RANGES  --yrange 0 0.25  --xcut 35 100  " ;;
                   EleX_Combined)
                       ISCOMB=true
                       ISWIDE=true
                       XVAR="${XVAR/_coarselongbin/_coarseelcomb}"
                       RANGES="${RANGES} --xcut 15 100  --xline 25 --xline 35 "; 
                       for E in ${BARREL} ${ENDCAP}; do
                           STACK=""
                           STACK="${STACK}  ${PBASE/EleX_Combined/Ele8}/fr_sub_eta_${E}.root:15-45"
                           STACK="${STACK}  ${PBASE/EleX_Combined/Ele17}/fr_sub_eta_${E}.root:25-100"
                           STACK="${STACK}  ${PBASE/EleX_Combined/Ele23}/fr_sub_eta_${E}.root:32-100"
                           echo "python ttH-multilepton/combine-fr-bins-prefit.py ${STACK} $PBASE/fr_sub_eta_${E}.root --oprefix ${NUM}_vs_${fitVar}_${XVAR}";
                       done;;
                   EleX_OR)
                       ISWIDE=true
                       XVAR="${CONEPTVAR}"
                       RANGES="${RANGES} --xcut 15 100  --xline 25 --xline 32 "; 
                 esac;; # ele trigger
           mu)
               RANGES="$RANGES  --yrange 0 0.25 " ;
               case $trigger in
                   Mu3_PFJet40)
                       RANGES="${RANGES} --xcut 10 30 --xline 10 --xline 15";;
                   Mu8)
                       XVAR="${XVAR/_coarselongbin/_coarsemu8bin}"
                       RANGES="${RANGES} --xcut 13 45 --xline 15 --xline 32";;
                   Mu17)
                       XVAR="${XVAR/_coarselongbin/_coarsemu17bin}"
                       RANGES="${RANGES} --xcut 25 100 --xline 32 ";;
                   Mu20)
                       XVAR="${XVAR/_coarselongbin/_coarsemu20bin}"
                       RANGES="${RANGES} --xcut 30 100 --xline 32 ";;
                   Mu27)
                       XVAR="${XVAR/_coarselongbin/_coarsemu27bin}"
                       RANGES="${RANGES} --xcut 40 100 --xline 45 ";;
                   #Mu50)
                   #    XVAR="${XVAR/_coarselongbin/_coarsemu50bin}"
                   #    RANGES="${RANGES} --xcut 81 100 ";;
                   MuX_Combined)
                       ISCOMB=true
                       ISWIDE=true
                       XVAR="${XVAR/_coarselongbin/_coarsecomb}"
                       RANGES="${RANGES} --xcut 10 100 --xline 10 --xline 15 --xline 32 --xline 45 "; 
                       for E in ${BARREL} ${ENDCAP}; do
                           STACK=""
                           STACK="${STACK}  ${PBASE/MuX_Combined/Mu3_PFJet40}/fr_sub_eta_${E}.root:10-32"
                           STACK="${STACK}  ${PBASE/MuX_Combined/Mu8}/fr_sub_eta_${E}.root:15-45"
                           STACK="${STACK}  ${PBASE/MuX_Combined/Mu17}/fr_sub_eta_${E}.root:32-100"
                           STACK="${STACK}  ${PBASE/MuX_Combined/Mu20}/fr_sub_eta_${E}.root:32-100"
                           STACK="${STACK}  ${PBASE/MuX_Combined/Mu27}/fr_sub_eta_${E}.root:45-100"
                           echo "python ttH-multilepton/combine-fr-bins-prefit.py ${STACK} $PBASE/fr_sub_eta_${E}.root --oprefix ${NUM}_vs_${fitVar}_${XVAR}";
                       done;;
                   MuX_OR)
                       ISWIDE=true
                       XVAR="${CONEPTVAR}"
                       RANGES="${RANGES} --xcut 10 100 --xline 15 --xline 32 --xline 45 ";; 
                 esac;; # mu trigger
        esac; ## electron or muon
        MCEFF="python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW $EWKONE  --groupBy cut ttH-multilepton/make_fake_rates_sels.txt ttH-multilepton/make_fake_rates_xvars.txt  "
        MCEFF="$MCEFF --sp ${QCD}_red  "
        MCEFF="$MCEFF --sP ${NUM} --sP ${XVAR}  --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots

	if [[ "$ANALYSIS" == "susy_wpM" ]]; then RANGES=${RANGES/--yrange 0 0.??/--yrange 0 0.50}; fi
        MCEFF="$MCEFF $LEGEND $RANGES"
        if ! $ISCOMB; then
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A veto eta 'abs(LepGood_eta)<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A veto eta 'abs(LepGood_eta)>$ETA' $BG )"
        fi;
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_prefit,total_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        MCGO="${MCGO/--yrange 0 0.??/--yrange 0 0.5}"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.05 $BG )"
        #MCGO="$MCEFF --compare ${QCD}_red_prefit,${QCD}_red --algo=fitND "
        #echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_full.root   $BG )"
        #echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_full.root   $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fit --algo=fitSimND --shapeSystSignal=l:0.15,s:0.05,b:0.02 --shapeSystBackground=l:0.07,s:0.02,b:0.02 --kappaBkg 1.1 --constrain theta_bkg --sigmaFBkg 0.05 --constrain fbkg "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitSimND.root  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitSimND.root  $BG )"
        if $ISWIDE; then
            MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fit --algo=fitGlobalSimND --shapeSystSignal=l:0.15,s:0.05,b:0.02 --shapeSystBackground=l:0.07,s:0.02,b:0.02"
            echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitGlobalSimND.root  $BG )"
            echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitGlobalSimND.root  $BG )"
            REG=" --regularize theta_sig 0.5 --regularize theta_bkg 0.5 --regularize fsig 0.07 --regularize fbkg 0.04 "
            echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitGlobalSimND_R1.root $REG $BG )"
            echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitGlobalSimND_R1.root $REG $BG )"
            REG=" --regularize theta_sig 0.25 --regularize theta_bkg 0.25 --regularize fsig 0.04 --regularize fbkg 0.02 "
            echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitGlobalSimND_R2.root $REG $BG )"
            echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitGlobalSimND_R2.root $REG $BG )"
        fi;
        #if ! $ISCOMB; then
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fqcd --algo=fQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fQCD.root  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fQCD.root  $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fqcd --algo=ifQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_ifQCD.root --subSyst 1.0 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_ifQCD.root --subSyst 1.0 $BG )"
        STACK="python ttH-multilepton/stack_fake_rates_data.py $RANGES $LEGEND --comb-mode=midpoint" # :_fit
        PATT="${NUM}_vs_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:${QCD}_red_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_ifQCD.root:$PATT:${QCD}_red_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
            if $ISWIDE; then
                echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp2.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:${QCD}_red_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_ifQCD.root:$PATT:${QCD}_red_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitGlobalSimND_R2.root:$PATT:data_fit   )";
            fi;
        done
        #fi
       ;;

esac;
