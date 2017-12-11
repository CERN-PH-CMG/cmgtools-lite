#!/bin/bash
if [[ "$VO_CMS_SW_DIR" != "" ]] && test -f $VO_CMS_SW_DIR/cmsset_default.sh; then 
  source $VO_CMS_SW_DIR/cmsset_default.sh
fi;
export SCRAM_ARCH=slc6_amd64_gcc530
WORK=$1; shift
SRC=$1; shift
cd $SRC; 
eval $(scramv1 runtime -sh);
export LD_LIBRARY_PATH=${CMSSW_BASE}/src/CMGTools/MonoXAnalysis/python/postprocessing/helpers:${LD_LIBRARY_PATH}
cd $WORK;
ulimit -c 0
exec $*
