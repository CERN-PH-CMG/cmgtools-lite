for i in TTHnobb_pow 
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ . -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root 
done
