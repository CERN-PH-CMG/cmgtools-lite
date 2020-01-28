#!/bin/bash
 ##for 2016 v5 with top tagger used
 ##--------------------------------
 ## bkg
 ## ---
#for i in DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep THQ THW T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
 ## sig
 ## ---
for i in TTHnobb_pow
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/elfaham/104X/2016/2lss_diff_Top-tagged -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules higgsRecoTTH_v5 -j 4 -F Friends {P}/0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}/3_recleaner_v1/{cname}_Friend.root -F Friends {P}/3_recleaner_v2/{cname}_Friend.root -F Friends {P}/4_btag/{cname}_Friend.root -F Friends {P}/4_btag_v2/{cname}_Friend.root -F Friends {P}/0_mcFlags_v0/{cname}_Friend.root -F Friends {P}/2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}/2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}/6_BDThtt/{cname}_Friend.root -F Friends {P}/1_lepJetBTagDeepFlav_v1/{cname}_Friend.root --env uclouvain -q cp3
done

 ##for 2016 v5 with no top tagger used
 ##------------------------------------
 ## bkg
 ## ---
#for i in DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep THQ THW T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
 ## sig
 ## ---
#for i in TTHnobb_pow
#do
#python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/elfaham/104X/2016/2lss_diff_NoTop-tagged -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules higgsRecoTTH_v5NoTopTagger -j 4 -F Friends {P}/0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}/3_recleaner_v1/{cname}_Friend.root -F Friends {P}/3_recleaner_v2/{cname}_Friend.root -F Friends {P}/4_btag/{cname}_Friend.root -F Friends {P}/4_btag_v2/{cname}_Friend.root -F Friends {P}/0_mcFlags_v0/{cname}_Friend.root -F Friends {P}/2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}/2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}/6_BDThtt/{cname}_Friend.root -F Friends {P}/1_lepJetBTagDeepFlav_v1/{cname}_Friend.root --env uclouvain -q cp3
#done




