#! /bin/bash
#SBATCH --ntasks=8

srun -N1 -n1 -c1 --exclusive python /home/users/e/l/elfaham/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/prepareEventVariablesFriendTree.py -j 0 -N 500000 -t NanoAOD /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ . -d WZTo3LNu_fxfx -c 1   -F  Friends {P}0_jmeUnc_v1/{cname}_Friend.root   -F  Friends {P}0_mcFlags_v0/{cname}_Friend.root   -F  Friends {P}1_lepJetBTagDeepFlav_v1/{cname}_Friend.root   -F  Friends {P}2_triggerSequence_v1/{cname}_Friend.root   -F  Friends {P}2_triggerSequence_v2/{cname}_Friend.root   -F  Friends {P}3_recleaner_v1/{cname}_Friend.root   -F  Friends {P}3_recleaner_v2/{cname}_Friend.root   -F  Friends {P}4_btag/{cname}_Friend.root   -F  Friends {P}4_btag_v2/{cname}_Friend.root   -F  Friends {P}4_leptonSFs_v0/{cname}_Friend.root   -F  Friends {P}6_BDThtt/{cname}_Friend.root   -I  'CMGTools.TTHAnalysis.tools.higgsRecoTTH' 'HiggsRecoTTH'  --compression 'ZLIB:3'  &
wait

