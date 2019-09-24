## that is for creating the final FTs running the higgsRecoTTH ##
## ----------------------------------------------------------------------------- ##
#for i in TTHnobb_pow TBar_tch TBar_tWch_noFullyHad TGJets_lep THQ THW T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ . -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDTht/{cname}_Friend.root
#done


## that is for taking the files from 3_recleaner_v2 and creating FTs with BDThtt ##
## ----------------------------------------------------------------------------- ##
#for i in TTHnobb_pow TBar_tch TBar_tWch_noFullyHad TGJets_lep THQ THW T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/6_BDThtt -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules BDThttTT_Hj -j 4 -F Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/3_recleaner_v2/{cname}_Friend.root
#done

## that is for trial ##
## ----------------- ##
#for i in TTHnobb_pow 
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ . -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root 
#done

## that is for trial ##
## ----------------- ##
for i in TTHnobb_pow 
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/6_BDThtt -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules BDThttTT_Hj -j 4 -F Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/3_recleaner_v2/{cname}_Friend.root
done
