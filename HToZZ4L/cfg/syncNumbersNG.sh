DIR=${1-TrashSync}
case $2 in
map)
    for F in $DIR/HZZ4L*/fourLeptonTreeProducer/tree.root; do
       ( echo "Start $F" && python ../python/scripts/eventDumper.py $F  -f '{run}:{lumi}:{evt}:{zz1_mass:.2f}:{zz1_z1_mass:.2f}:{zz1_z2_mass:.2f}:{zz1_D_bkg_kin:.3f}:{zz1_D_bkg:.3f}:{zz1_D_gg:.3f}:{zz1_Dkin_HJJ_VBF_2:.3f}:{zz1_D_0m:.3f}:{zz1_Dkin_HJJ_VBF_1:.3f}:{zz1_Dkin_HJJ_WH:.3f}:{zz1_Dkin_HJJ_ZH:.3f}:{zz1_nJet30:d}:{zz1_j1ptzs:.2f}:{zz1_j2ptzs:.2f}:{zz1_j1qglzs:.3f}:{zz1_j2qglzs:.3f}:{zz1_Dfull_HJJ_VBF_2:.3f}:{zz1_Dfull_HJJ_VBF_1:.3f}:{zz1_Dfull_HJJ_WH:.3f}:{zz1_Dfull_HJJ_ZH:.3f}:37:{zz1_z1_l1_pdgId:+.0f}:{zz1_z2_l1_pdgId:+.0f}' -C 'zz1_mass>70 ' --type asis > ${F}.txt  2> ${F}.err && echo "Done $F" || cat ${F}.err & );
    done
    ;;
map2)
    for F in $DIR/HZZ4L*/fourLeptonTreeProducer/tree.root; do
       ( echo "Start $F" && python ../python/scripts/eventDumper.py $F  -f '{run}:{lumi}:{evt}:{zz1_mass:.2f}:{zz1_z1_mass:.2f}:{zz1_z2_mass:.2f}:{zz1_D_bkg_kin:.3f}:{zz1_D_bkg:.3f}:{zz1_D_gg:.3f}:{zz1_Dfull_HJJ_VBF_2:.3f}:{zz1_D_0m:.3f}:{zz1_Dfull_HJJ_VBF_1:.3f}:{zz1_Dfull_HJJ_WH:.3f}:{zz1_Dfull_HJJ_ZH:.3f}:{zz1_nJet30:d}:{zz1_j1ptzs:.2f}:{zz1_j2ptzs:.2f}' -C 'zz1_mass>70 ' --type asis > ${F}.txt2  2> ${F}.err && echo "Done $F" || cat ${F}.err & );
    done
    ;;
reduce)
    for F in $DIR/HZZ4L*/fourLeptonTreeProducer/tree.root; do
        cat ${F}.txt
    done | sort -t: -k3,3 -n | sort -t: -k2,2 -n --stable | sort -t: -k1,1 -n --stable > mydump3-ext.txt
    cut -d: -f1-24  mydump3-ext.txt > mydump3.txt
    cut -d: -f25-26 mydump3-ext.txt | wc -l
    cut -d: -f25-26 mydump3-ext.txt | grep '.11:.11' | wc -l
    cut -d: -f25-26 mydump3-ext.txt | grep '.13:.13' | wc -l
    cut -d: -f25-26 mydump3-ext.txt | grep '.13:.11\|.11:.13' | wc -l
    ;;
reduce2)
    for F in $DIR/HZZ4L*/fourLeptonTreeProducer/tree.root; do
        cat ${F}.txt2
    done | sort -t: -k3,3 -n | sort -t: -k2,2 -n --stable | sort -t: -k1,1 -n --stable > mydump3-${3}.txt
    ;;
*)
    echo "Usage: $0 DIR [map|reduce]"
esac;
