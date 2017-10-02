bash ttH-multilepton/make_fake_rates_MC.sh 075ib1f30E2ptc30
bash ttH-multilepton/make_fake_rates_MC.sh sMiX4mrE2
bash ttH-multilepton/make_fake_rates_MC.sh sViX4mrE2
bash ttH-multilepton/make_fake_rates_MC.sh RA7E2

for AN in ttH susy_wpM susy_wpT susy_RA7; do
    for trig in Ele8_CaloIdM_TrackIdM_PFJet30 Ele12_CaloIdM_TrackIdM_PFJet30; do
	bash ttH-multilepton/make_fake_rates_data.sh $AN el $trig fakerates-mtW1R
    done
    for trig in Mu3_PFJet40 Mu8 Mu17; do
	bash ttH-multilepton/make_fake_rates_data.sh $AN mu $trig fakerates-mtW1R
    done
    bash ttH-multilepton/make_fake_rates_z3l.sh $AN el fakerates-mtW3R
    bash ttH-multilepton/make_fake_rates_z3l.sh $AN mu fakerates-mtW3R
    echo python ttH-multilepton/pack_fake_rates_data.py --pdir ~/www/plots_FR/80X/lepMVA_$AN/v1.4_250616/fr-meas/comb ~/www/plots_FR/80X/lepMVA_$AN/v1.4_250616/fr-meas/fr_comb.root $AN
done
