#!/bin/bash
source /mnt/t3nfs01/data01/swshare/psit3/etc/profile.d/cms_ui_env.sh
source $VO_CMS_SW_DIR/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481
WORK=$1; shift
SRC=$1; shift
cd $SRC; 
eval $(scramv1 runtime -sh);
cd $WORK;
exec $*

