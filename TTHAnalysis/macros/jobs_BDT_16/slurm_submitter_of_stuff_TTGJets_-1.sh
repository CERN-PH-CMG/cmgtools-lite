#! /bin/bash
#SBATCH --ntasks=8

srun -N1 -n1 -c1 --exclusive python /home/users/e/l/elfaham/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/macros/prepareEventVariablesFriendTree.py -j 0 -N 500000 -t NanoAOD /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/ /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/6_BDThtt -d TTGJets -c -1   -F  Friends /nfs/user/pvischia/tth/v5pre/NanoTrees_TTH_300519_v5pre_skim2LSS/2016/3_recleaner_v2/{cname}_Friend.root   -I  'CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules' 'BDThttTT_Hj'  --compression 'ZLIB:3'  &
wait

