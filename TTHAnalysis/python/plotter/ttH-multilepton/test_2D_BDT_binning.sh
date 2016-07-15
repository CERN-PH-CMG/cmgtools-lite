directory=${10} # something like cards_testWP_date
category=${11} # 2lss or 3l or all
echo "float cuts_2lss_ttbar0 = ${1};" > ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_2lss_ttbar1 = ${2};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_2lss_ttbar2 = ${3};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_2lss_ttV0 = ${4};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_2lss_ttV1 = ${5};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_2lss_ttV2 = ${6};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_3l_ttbar1 = ${7};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_3l_ttbar2 = ${8};" >> ttH-multilepton/binning_2d_thresholds.h
echo "float cuts_3l_ttV1 = ${9};" >> ttH-multilepton/binning_2d_thresholds.h

# run same command with save option first
echo "running: bash ttH-multilepton/make_cards.sh ${directory} 10 ${category} read"
bash ttH-multilepton/make_cards.sh ${directory} 10 ${category} read > /dev/null
cd cards/${directory}
cd ~peruzzi/work/cmgtools/combine/CMSSW_7_1_15/src/; eval `scramv1 runtime -sh`; cd -;
rm ${category}.txt; combineCards.py *card.txt > ${category}.txt
res=`combine -M Asymptotic --run blind --rAbsAcc 0.0005 --rRelAcc 0.0005 ${category}.txt | grep "Expected 50"`
cd ../..
eval `scramv1 runtime -sh`

echo "${1} ${2} ${3} ${4} ${5} ${6} ${7} ${8} ${9} ${10} ${11} ${res}" >> results_optMVAWP_${directory}.txt