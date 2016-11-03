#!/bin/bash
if [[ "$VO_CMS_SW_DIR" != "" ]] && test -f $VO_CMS_SW_DIR/cmsset_default.sh; then 
  source $VO_CMS_SW_DIR/cmsset_default.sh
fi;
export SCRAM_ARCH=slc6_amd64_gcc530
WORK=$1; shift
SRC=$1; shift
cd $SRC; 
eval $(scramv1 runtime -sh);
cd $WORK;
ulimit -c 0
exec $*
