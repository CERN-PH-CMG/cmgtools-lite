#for i in TTHnobb_fxfx TTJets_DiLepton TTJets_SingleLeptonFromT TTJets_SingleLeptonFromTbar TTWToLNu_fxfx TTZToLLNuNu_m1to10 TTZToLLNuNu_m1to10; do
for i in TTHnobb_fxfx; do
    python prepareEventVariablesFriendTree.py -t NanoAOD /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ /home/ucl/cp3/pvischia/cmssw/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/mycensoredword_dnn -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules higgsDiffRegressionTTH -j 4 -F Friend {P}/0_jmeUnc_v1/{cname}_Friend.root -F Friend {P}/1_recl/{cname}_Friend.root -F Friend {P}/2_scalefactors/{cname}_Friend.root -F Friend {P}/3_tauCount/{cname}_Friend.root -F Friend {P}/5_BDThtt_reco/{cname}_Friend.root -F Friend {P}/6_higgsDiffGenTTH/{cname}_Friend.root  -D $i 
#--env uclouvaindef -q cp3
done



#-F Friend {P}/0_jmeUnc_v1/{cname}_Friend.root -F Friend {P}/0_mcFlags_v0/{cname}_Friend.root -F Friend {P}/1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friend {P}/2_triggerSequence_v2/{cname}_Friend.root -F Friend {P}/3_recleaner_v2/{cname}_Friend.root -F Friend {P}/4_btag_v2/{cname}_Friend.root -F Friend {P}/4_leptonSFs_v0/{cname}_Friend.root  -F Friend {P}/6_BDThtt/{cname}_Friend.root
#/nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/
 
#x-F Friend {P}/5_higgsDecay/{cname}_Friend.root
# python prepareEventVariablesFriendTree.py -t NanoAOD -d $i /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2017/ $2 -I CMGTools.TTHAnalysis.tools.higgsRecoTTH_NoTopTag HiggsRecoTTH -j 4 -F Friends {P}0_jmeUnc_v1/{cname}_Friend.root -F Friends {P}0_mcFlags_v0/{cname}_Friend.root -F Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v1/{cname}_Friend.root -F Friends {P}2_triggerSequence_v2/{cname}_Friend.root -F Friends {P}3_recleaner_v1/{cname}_Friend.root -F Friends {P}3_recleaner_v2/{cname}_Friend.root -F Friends {P}4_btag/{cname}_Friend.root -F Friends {P}4_btag_v2/{cname}_Friend.root -F Friends {P}4_leptonSFs_v0/{cname}_Friend.root -F Friends {P}5_higgsDecay/{cname}_Friend.root -F Friends {P}6_BDThtt/{cname}_Friend.root --env uclouvain -q cp3 

#[pvischia@ingrid-ui1 plotter]$ 

#python skimTreesNew.py -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ --skim-friends  -F Friend {P}/0_jmeUnc_v1/{cname}_Friend.root -F Friend {P}/1_recl/{cname}_Friend.root -F Friend {P}/2_scalefactors/{cname}_Friend.root -F Friend {P}/3_tauCount/{cname}_Friend.root -F Friend {P}/5_BDThtt_reco/{cname}_Friend.root -F Friend /home/ucl/cp3/pvischia/cmssw/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/mycensoredword_dnn/ --mcc ttH-multilepton/lepchoice-ttH-FO.txt -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/mcc-METFixEE2017.txt -E trigger   -p ttH --tree NanoAOD --elist stocazzo skim.txt mytest.txt --year 2016 ./withvisiblept

cd ../python/plotter/
#python skimTreesNew.py -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ --skim-friends  --Fs {P}/0_jmeUnc_v1/ --Fs {P}/1_recl/ --Fs {P}/2_scalefactors/ --Fs {P}/3_tauCount/ --Fs {P}/5_BDThtt_reco/ --Fs /home/ucl/cp3/pvischia/cmssw/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/mycensoredword_dnn/ --mcc ttH-multilepton/lepchoice-ttH-FO.txt -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/mcc-METFixEE2017.txt   --tree NanoAOD --elist stocazzo --year 2016  ttH-multilepton/mca-2lss-mc.txt mytest.txt /nfs/user/pvischia/tth/dnn/2016_skimmed_drll_fixthefix_skimmed_v2/
python skimTreesNew.py -P /nfs/user/pvischia/tth/v6/NanoTrees_TTH_091019_v6pre_skim2lss/2016/ --skim-friends  --Fs {P}/0_jmeUnc_v1/ --Fs {P}/1_recl/ --Fs {P}/2_scalefactors/ --Fs {P}/3_tauCount/ --Fs {P}/5_BDThtt_reco/ --Fs /home/ucl/cp3/pvischia/cmssw/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/mycensoredword_dnn/ --mcc ttH-multilepton/lepchoice-ttH-FO.txt -L ttH-multilepton/functionsTTH.cc --mcc ttH-multilepton/mcc-METFixEE2017.txt   --tree NanoAOD --elist stocazzo --year 2016  ttH-multilepton/mca-2lss-mc.txt ttH-multilepton/2lss_tight.txt /nfs/user/pvischia/tth/dnn/2016_skimmed_drll_fixthefix_skimmed_v2/



### [pvischia@ingrid-ui1 macros]$ python prepareEventVariablesFriendTree.py -t NanoAOD ../python/plotter/fornn_2016_masses/ ../python/plotter/fornn_2016_masses/6_higgsrecotest -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules higgsRecoTTH -j 20 -F Friend {P}/0_jmeUnc_v1/{cname}_Friend.root -F Friend {P}/1_recl/{cname}_Friend.root -F Friend {P}/2_scalefactors/{cname}_Friend.root -F Friend {P}/3_tauCount/{cname}_Friend.root -F Friend {P}/5_BDThtt_reco/{cname}_Friend.root -D TTH 

