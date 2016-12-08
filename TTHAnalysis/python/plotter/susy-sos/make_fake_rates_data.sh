################################
#  use mcEfficiencies.py to make plots of the fake rate
################################
T="/afs/cern.ch/user/g/gpetrucc/w/LINKS_80X_SOS_171116_NoIso_1L "
if hostname | grep -q cmsco01; then
     T="/data1/gpetrucc/TREES_80X_SOS_171116_NoIso_1L"
fi
BCORE=" --s2v --tree treeProducerSusyMultilepton susy-sos/mca-qcd1l.txt susy-sos/qcd1l.txt -P $T -l 35 --AP   -L susy-sos/functionsSOS.cc "
### Selection for no-iso trees for V3.0 fake rates
#BCORE="${BCORE}  -E ptd_3_20    -E muonid -E ip3dloose -R recoil recoil 'LepGood_awayJet_pt > 50'  "
### Selection for no-iso trees for V3.1 fake rates
BCORE=" ${BCORE}  -E pti_300_20  -E muonid -E ip3dloose -R recoil recoil 'LepGood_awayJet_pt > 90'  "

BG=" -j 6 "; if [[ "$1" == "-b" ]]; then BG=" & "; shift; fi

lepton=$1; if [[ "$1" == "" ]]; then exit 1; fi
case $lepton in
mu) BCORE="${BCORE} -E ^${lepton} --xf 'DoubleEG.*'  "; QCD=QCD; ;;
el) BCORE="${BCORE} -E ^${lepton} --xf 'DoubleMu.*'  "; QCD=QCD; ;;
esac;

trigger=$2; if [[ "$2" == "" ]]; then exit 1; fi
case $trigger in
PFJetAny)
    BCORE="${BCORE} -E HLT_FR_$trigger  --xf 'DoubleMu.*'  "; 
    PUW=" -L susy-sos/frPuReweight.cc -W 'puw$lepton$trigger(nVert)' "
    ;;
Mu8|Mu3_PFJet40)
    BCORE="${BCORE} -E HLT_FR_$trigger  --xf 'JetHT.*'  "; 
    PUW=" -L susy-sos/frPuReweight.cc -W 'puw$trigger(nVert)' "
    ;;
esac;

what=$3;
more=$4
PBASE="plots/80X/sos/fr-meas/qcd1l/v3.1/$lepton/HLT_$trigger/$what/$more"

EWKONE="-p ${QCD}_red,EWK,data"
EWKSPLIT="-p ${QCD}_red,WJets,DYJets,data"
QCDEWKSPLIT="-p ${QCD}_[bclg]jets,WJets,DYJets,data"
FITEWK=" $EWKSPLIT --flp WJets,DYJets,${QCD}_red --peg-process DYJets WJets "
QCDNORM=" $QCDEWKSPLIT --sp WJets,DYJets,${QCD}_.jets --scaleSigToData  "
## these below are not used in this version of the script
#QCDFITEWK=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[clg]jets ${QCD}_bjets "
#QCDFITQCD=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[gl]jets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "
#QCDFITALL=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_gjets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "

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
        echo "python mcPlots.py -f -j 6 $BCORE susy-sos/make_fake_rates_xvars.txt --pdir $PBASE --sP nvtx $EWKONE " 
        echo "echo; echo; ";
        echo "python ../tools/vertexWeightFriend.py no $PBASE/make_fake_rates_xvars.root ";
        echo "echo; echo ' ---- Now you should put the normalization and weight into frPuReweight.cc defining a puw$trigger ----- ' ";
        ;;
    nvtx-closure)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE --sP nvtx $EWKONE  --showRatio --maxRatioRange 0.9 1.1 " 
        ;;
    den-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit/} --showRatio --maxRatioRange 0.0 1.99 --sP ev_.*,nvtx,pt_fine,lep_.*,mtW3.*,awayJet_.*" 
        ;;
    num-fit*)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit/} --showRatio --maxRatioRange 0.0 1.99 -E num --sP ev_.*,nvtx,pt_fine,lep_.*,mtW3.*,awayJet_.*" 
        ;;
    qcdflav-norm)
        echo "python mcPlots.py -f -j 6 $BCORE $PUW susy-sos/make_fake_rates_xvars.txt --pdir $PBASE -E $what $QCDNORM --showRatio --maxRatioRange 0.0 1.99 " 
        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}
        Num=IP3D_Full;
        XVAR="pt_fine"
        MCEFF="  python ttH-multilepton/dataFakeRate.py -f  $BCORE $PUW $EWKONE  --groupBy cut susy-sos/make_fake_rates_sels.txt susy-sos/make_fake_rates_xvars.txt  "
        MCEFF="$MCEFF --sp ${QCD}_red  "
        MCEFF="$MCEFF --sP ${XVAR} --sP ${Num} --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        MCEFF="$MCEFF  " # ratio for fake rates
        MCEFF="$MCEFF --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots
        LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
        RANGES=" --showRatio  --ratioRange 0.00 1.99 "
        case $lepton in  
           el) RANGES="$RANGES  --yrange 0 1.0  --xcut 5 100 --xline 0 " ;;
           mu)
                 RANGES="$RANGES  --yrange 0 1.0 " ;
                 if [[ "$trigger" == "Mu8" ]]; then 
                     RANGES="${RANGES} --xcut 7.5 100 --xline 10"; 
                 elif [[ "$trigger" == "Mu3_PFJet40" ]]; then
                     RANGES="${RANGES} --xcut 2.5 100 --xline 10"; 
                 fi;
            ;;
        esac;
        MCEFF="$MCEFF $LEGEND $RANGES"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A entry eta 'abs(LepGood_eta)<$ETA' $BG )"
        echo " ( $MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A entry eta 'abs(LepGood_eta)>$ETA' $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_prefit,total_prefit,data_sub_syst_prefit,data_sub_prefit --algo=globalFit "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_globalFit_full.root --algo=globalFit --fcut 0 20 --subSyst 0.1 $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fit --algo=fitSimND --shapeSystSignal=l:0.2,s:0.1,b:0.01 --shapeSystBackground=l:0.1,s:0.05,b:0.01 "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fitSimND.root  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fitSimND.root  $BG )"
        MCGO="$MCEFF --compare ${QCD}_red_prefit,data_fqcd --algo=fQCD "
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${BARREL}.root -o $PBASE/fr_sub_eta_${BARREL}_fQCD.root --algo=fQCD  $BG )"
        echo " ( $MCGO -i $PBASE/fr_sub_eta_${ENDCAP}.root -o $PBASE/fr_sub_eta_${ENDCAP}_fQCD.root --algo=fQCD  $BG )"
        STACK="python ttH-multilepton/stack_fake_rates_data.py $RANGES $LEGEND   --xtitle 'lepton p_{T} (GeV)' "
        PATT="${Num}_vs_${XVAR}_${fitVar}_%s"
        for E in ${BARREL} ${ENDCAP}; do
            echo "( $STACK -o $PBASE/fr_sub_eta_${E}_comp.root    $PBASE/fr_sub_eta_${E}_globalFit.root:$PATT:${QCD}_red_prefit,data_sub_syst_prefit  $PBASE/fr_sub_eta_${E}_fQCD.root:$PATT:${QCD}_red_prefit,data_fqcd   $PBASE/fr_sub_eta_${E}_fitSimND.root:$PATT:data_fit   )";
        done
       ;;

esac;
