#!/bin/bash
source /mnt/t3nfs01/data01/swshare/psit3/etc/profile.d/cms_ui_env.sh
source $VO_CMS_SW_DIR/cmsset_default.sh
cd [SRC] 
eval $(scramv1 runtime -sh);
cd [WORK]
[PLACEHOLDER]
echo "Job for SUSY-Interface task [INST] is done."
echo "Log files can be found at [WORK]/susy-interface/tmp/[INST]/log"
touch [JOBDIR]/[JOBID]
