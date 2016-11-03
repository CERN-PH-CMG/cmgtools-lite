#!/bin/bash
cd [SRC] 
eval $(scramv1 runtime -sh);
cd [WORK]
[PLACEHOLDER]
echo "Job for SUSY-Interface task [INST] is done."
echo "Log files can be found at [WORK]/susy-interface/tmp/[INST]/log"
touch [JOBDIR]/[JOBID]
