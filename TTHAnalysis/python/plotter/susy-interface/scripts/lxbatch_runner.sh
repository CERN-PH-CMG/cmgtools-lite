#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc481
WORK=$1; shift
SRC=$1; shift
INST=$1; shift
cd $SRC; 
eval $(scramv1 runtime -sh);
cd $WORK;
[PLACEHOLDER]
echo "Job for SUSY-Interface task $INST is done."
echo "Log files can be found at $WORK/susy-interface/tmp/$INST/log"
