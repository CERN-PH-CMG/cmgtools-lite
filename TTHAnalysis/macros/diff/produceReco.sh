#!/bin/bash
## this should be your directory: /nfs/user/elfaham/104X/v6/2016/2lss_diff_Top-tagged or /nfs/user/elfaham/104X/v6/2016/2lss_diff_NoTop-tagged, or 2017 or 2018. 
if [ "$1" == "bkg_16_TopTagged" ]; then
for i in TBar_tWch_noFullyHad TBar_tch TBar_tch_PS TGJets_lep THQ_ctcvcp THW_ctcvcp TTGJets TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTTT TTWToLNu_fxfx TTWW TTZH TTZToLLNuNu_amc TTZToLLNuNu_m1to10 TZQToLL TZQToLL_PS T_sch_lep T_sch_lep_PS T_tWch_noFullyHad T_tch VHToNonbb WGToLNuG WJetsToLNu_LO WWTo2L2Nu WWTo2L2Nu_DPS WWW WWW_ll WWZ WZG WZTo3LNu_fxfx WZTo3LNu_pow WZZ WpWpJJ GGHZZ4L DYJetsToLL_M10to50_LO DYJetsToLL_M50 ZGTo2LG ZGTo2LG ZHTobb_ll ZZTo4L ZZZ tWll
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3   
done
fi
######################################
if [ "$1" == "bkg_16_NoTopTagged" ]; then
for i in TBar_tWch_noFullyHad TBar_tch TBar_tch_PS TGJets_lep THQ_ctcvcp THW_ctcvcp TTGJets TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTTT TTWToLNu_fxfx TTWW TTZH TTZToLLNuNu_amc TTZToLLNuNu_m1to10 TZQToLL TZQToLL_PS T_sch_lep T_sch_lep_PS T_tWch_noFullyHad T_tch VHToNonbb WGToLNuG WJetsToLNu_LO WWTo2L2Nu WWTo2L2Nu_DPS WWW WWW_ll WWZ WZG WZTo3LNu_fxfx WZTo3LNu_pow WZZ WpWpJJ GGHZZ4L DYJetsToLL_M10to50_LO DYJetsToLL_M50 ZGTo2LG ZGTo2LG ZHTobb_ll ZZTo4L ZZZ tWll
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3    
done
fi
######################################
######################################
if [ "$1" == "sig_16_TopTagged" ]; then
for i in TTHnobb_fxfx TTH_ctcvcp
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3 
done
fi
#####################################
if [ "$1" == "sig_16_NoTopTagged" ]; then
for i in TTHnobb_fxfx TTH_ctcvcp
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3   
done
fi
## that is for taking the files from 3_recleaner_v2 and creating FTs with BDThtt (it was used with v5) ##
## --------------------------------------------------------------------------------------------------- ##
#for i in TTHnobb_pow TBar_tch TBar_tWch_noFullyHad TGJets_lep THQ THW T_sch_lep T_tch TTGJets TTJets_DiLepton TTJets_SingleLeptonFromTbar TTJets_SingleLeptonFromT TTTT T_tWch_noFullyHad TTW_LO TTZ_LO TTZToLLNuNu_m1to10 tWll WJetsToLNu_LO WpWpJJ WWTo2L2Nu WWZ WZTo3LNu_fxfx WZZ ZZTo4L ZZZ DYJetsToLL_M10to50_LO DYJetsToLL_M50 GGHZZ4L
#do
#python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/6_BDThtt -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules BDThttTT_Hj -j 4 -F Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/3_recleaner_v2/{cname}_Friend.root --env uclouvain -q cp3
#done
## -----##
## 2017 ##
## ---- ##
if [ "$1" == "bkg_17_TopTagged" ]; then
for i in TBar_tWch_noFullyHad TBar_tch TBar_tch_PS TGJets_lep THQ_ctcvcp THW_ctcvcp TTGJets TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTTT TTTT_PS TTWH TTWToLNu_fxfx TTWToLNu_fxfx_PS TTWW TTZH TTZToLLNuNu_amc TTZToLLNuNu_amc_PS TTZToLLNuNu_m1to10 TZQToLL T_sch_lep T_sch_lep_PS T_tWch_noFullyHad T_tch T_tch_PS VHToNonbb VHToNonbb_ll WGToLNuG WJetsToLNu_LO WWTo2L2Nu WWTo2L2Nu_DPS WWTo2L2Nu_PS WWW WWW_ll WWZ WW_DPS WZG WZTo3LNu_fxfx WZZ WpWpJJ ZGTo2LG ZHToTauTau ZHTobb_ll ZZTo4L ZZZ tWll GGHZZ4L DYJetsToLL_M10to50_LO DYJetsToLL_M50 
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3
done 
fi
#####################################
if [ "$1" == "bkg_17_NoTopTagged" ]; then
for i in TBar_tWch_noFullyHad TBar_tch TBar_tch_PS TGJets_lep THQ_ctcvcp THW_ctcvcp TTGJets TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTTT TTTT_PS TTWH TTWToLNu_fxfx TTWToLNu_fxfx_PS TTWW TTZH TTZToLLNuNu_amc TTZToLLNuNu_amc_PS TTZToLLNuNu_m1to10 TZQToLL T_sch_lep T_sch_lep_PS T_tWch_noFullyHad T_tch T_tch_PS VHToNonbb VHToNonbb_ll WGToLNuG WJetsToLNu_LO WWTo2L2Nu WWTo2L2Nu_DPS WWTo2L2Nu_PS WWW WWW_ll WWZ WW_DPS WZG WZTo3LNu_fxfx WZZ WpWpJJ ZGTo2LG ZHToTauTau ZHTobb_ll ZZTo4L ZZZ tWll GGHZZ4L DYJetsToLL_M10to50_LO DYJetsToLL_M50 
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3   
done
fi
#####################################
if [ "$1" == "sig_17_TopTagged" ]; then
for i in TTHnobb_fxfx TTH_ctcvcp 
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3
done
fi
#####################################
if [ "$1" == "sig_17_NoTopTagged" ]; then
for i in TTHnobb_fxfx TTH_ctcvcp
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3   
done
fi
## -----##
## 2018 ##
## ---- ##
if [ "$1" == "bkg_18_TopTagged" ]; then
for i in TBar_tWch_noFullyHad TBar_tch TGJets_lep THQ_ctcvcp THW_ctcvcp TTGJets TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTTT TTWH TTWToLNu_fxfx TTWW TTZH TTZToLLNuNu_amc TTZToLLNuNu_m1to10 TZQToLL T_sch_lep T_tWch_noFullyHad T_tch VHToNonbb VHToNonbb_ll WGToLNuG WJetsToLNu_LO WWTo2L2Nu WWTo2L2Nu_DPS WWW WWW_ll WWZ WW_DPS WZG WZTo3LNu_fxfx WZTo3LNu_pow WZZ WpWpJJ ZGTo2LG ZHToTauTau ZHTobb_ll ZZTo4L ZZZ tWll  GGHZZ4L DYJetsToLL_M10to50_LO DYJetsToLL_M50
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3
done 
fi
#####################################
if [ "$1" == "bkg_18_NoTopTagged" ]; then
for i in TBar_tWch_noFullyHad TBar_tch TGJets_lep THQ_ctcvcp THW_ctcvcp TTGJets TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTTT TTWH TTWToLNu_fxfx TTWW TTZH TTZToLLNuNu_amc TTZToLLNuNu_m1to10 TZQToLL T_sch_lep T_tWch_noFullyHad T_tch VHToNonbb VHToNonbb_ll WGToLNuG WJetsToLNu_LO WWTo2L2Nu WWTo2L2Nu_DPS WWW WWW_ll WWZ WW_DPS WZG WZTo3LNu_fxfx WZTo3LNu_pow WZZ WpWpJJ ZGTo2LG ZHToTauTau ZHTobb_ll ZZTo4L ZZZ tWll  GGHZZ4L DYJetsToLL_M10to50_LO DYJetsToLL_M50
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3   
done
fi
#####################################
if [ "$1" == "sig_18_TopTagged" ]; then
for i in TTH_ctcvcp TTHnobb_fxfx
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3
done
fi
#####################################
if [ "$1" == "sig_18_NoTopTagged" ]; then
for i in TTH_ctcvcp TTHnobb_fxfx
do
python ../prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2018/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}2_scalefactors/{cname}_Friend.root -F Friends {P}3_tauCount/{cname}_Friend.root -F Friends {P}1_recl/{cname}_Friend.root -F Friends {P}5_BDThtt_reco/{cname}_Friend.root --env uclouvain -q cp3   
done
fi
