#!/bin/bash
## -------------------------------------------------------------------------------------------------------------------------------  ##
## TODO this should be your directory: /nfs/user/elfaham/104X/2016/2lss_Top-tagged or /nfs/user/elfaham/104X/2016/2lss_NoTop-tagged ##TODO
## -------------------------------------------------------------------------------------------------------------------------------- ##
## THQ THW have no friends in most of the Friend dirs --> removed from command line
## the only sample from below that has a friend in higgs decay is TTHnobb (the signal) so I have a seperate command line for that
## -------------------------------------------------------------------------------------------------------------------------------- ##
if [ "$1" == "bkg_16_TopTagged" ]; then
for i in TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll  WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done
fi
######################################
if [ "$1" == "bkg_16_NoTopTagged" ]; then
for i in TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll  WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done
fi
######################################
######################################
if [ "$1" == "sig_16_TopTagged" ]; then
for i in TTHnobb_pow 
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3 
done
fi
#####################################
if [ "$1" == "sig_16_NoTopTagged" ]; then
for i in TTHnobb_pow 
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3 
done
fi
## that is for taking the files from 3_recleaner_v2 and creating FTs with BDThtt ##
## ----------------------------------------------------------------------------- ##
#for i in TTHnobb_pow TBar_tch TBar_tWch_noFullyHad TGJets_lep THQ THW T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/6_BDThtt -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules BDThttTT_Hj -j 4 -F Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/3_recleaner_v2/{cname}_Friend.root --env uclouvain -q cp3
#done

## -----##
## 2017 ##
## ---- ##

if [ "$1" == "bkg_17_TopTagged" ]; then
for i in DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTWToLNu_fxfx TTWW TTZ_LO TTZToLLNuNu_amc TTZToLLNuNu_m1to10 tWll TZQToLL VHToNonbb_ll WJetsToLNu_LO WpWpJJ WW_DPS WWTo2L2Nu WWW_ll WWZ WZG WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done 
fi
#####################################
if [ "$1" == "bkg_17_NoTopTagged" ]; then
for i in DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTWToLNu_fxfx TTWW TTZ_LO TTZToLLNuNu_amc TTZToLLNuNu_m1to10 tWll TZQToLL VHToNonbb_ll WJetsToLNu_LO WpWpJJ WW_DPS WWTo2L2Nu WWW_ll WWZ WZG WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done
fi
#####################################
if [ "$1" == "sig_17_TopTagged" ]; then
for i in TTHnobb_pow #TODO didn't use TTH_synch nor TTH_ctcvcp
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done
fi
#####################################
if [ "$1" == "sig_17_NoTopTagged" ]; then
for i in TTHnobb_pow #TODO didn't use TTH_synch nor TTH_ctcvcp
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3 
done
fi
#####################################
## that is for taking the files from 3_recleaner_v2 and creating FTs with BDThtt ##
## ----------------------------------------------------------------------------- ##
#for i in TTHnobb_pow DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTWToLNu_fxfx TTWW TTZ_LO TTZToLLNuNu_amc TTZToLLNuNu_m1to10 tWll TZQToLL VHToNonbb_ll WJetsToLNu_LO WpWpJJ WW_DPS WWTo2L2Nu WWW_ll WWZ WZG WZTo3LNu_fxfx WZZ ZZTo4L ZZZ
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/6_BDThtt -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules BDThttTT_Hj -j 4 -F Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/3_recleaner_v2/{cname}_Friend.root --env uclouvain -q cp3
#done

## -----##
## 2018 ##
## ---- ##
if [ "$1" == "bkg_18_TopTagged" ]; then
for i in DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTWToLNu_fxfx TTWW TTZ_LO TTZToLLNuNu_amc TTZToLLNuNu_m1to10 tWll TZQToLL VHToNonbb_ll WJetsToLNu_LO WpWpJJ WW_DPS WWTo2L2Nu WWW_ll WWZ WZG WZTo3LNu_fxfx WZZ ZZTo4L ZZZ 
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done 
fi
#####################################
if [ "$1" == "bkg_18_NoTopTagged" ]; then
for i in DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTWToLNu_fxfx TTWW TTZ_LO TTZToLLNuNu_amc TTZToLLNuNu_m1to10 tWll TZQToLL VHToNonbb_ll WJetsToLNu_LO WpWpJJ WW_DPS WWTo2L2Nu WWW_ll WWZ WZG WZTo3LNu_fxfx WZZ ZZTo4L ZZZ 
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done
fi
#####################################
if [ "$1" == "sig_18_TopTagged" ]; then
for i in TTHnobb_pow #TODO didn't use TTH_synch nor TTH_ctcvcp
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3
done
fi
#####################################
if [ "$1" == "sig_18_NoTopTagged" ]; then
for i in TTHnobb_pow #TODO didn't use TTH_synch nor TTH_ctcvcp
do
python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3 
done
fi
#####################################
## that is for taking the files from 3_recleaner_v2 and creating FTs with BDThtt ##
## ----------------------------------------------------------------------------- ##

#for i in TTHnobb_pow DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L TBar_tch TBar_tWch_noFullyHad TGJets_lep T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTWToLNu_fxfx TTWW TTZ_LO TTZToLLNuNu_amc TTZToLLNuNu_m1to10 tWll TZQToLL VHToNonbb_ll WJetsToLNu_LO WpWpJJ WW_DPS WWTo2L2Nu WWW_ll WWZ WZG WZTo3LNu_fxfx WZZ ZZTo4L ZZZ 
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/6_BDThtt -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules BDThttTT_Hj -j 4 -F Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2018/3_recleaner_v2/{cname}_Friend.root --env uclouvain -q cp3
#done


