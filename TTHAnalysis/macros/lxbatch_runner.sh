#!/bin/bash
if [[ "$VO_CMS_SW_DIR" != "" ]] && test -f $VO_CMS_SW_DIR/cmsset_default.sh; then 
  source $VO_CMS_SW_DIR/cmsset_default.sh
fi;
export SCRAM_ARCH=slc7_amd64_gcc700
WORK=$1; shift
SRC=$1; shift
cd $SRC; 
echo "Getting ENV from $SRC"
eval $(scramv1 runtime -sh);
echo "Running in $WORK"
cd $WORK;
ulimit -c 0
echo "Will execute $*"
exec $*
