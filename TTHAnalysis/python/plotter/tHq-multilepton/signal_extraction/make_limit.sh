#!/bin/bash

# Set environment for combine
COMBINEDIR="/afs/cern.ch/user/s/stiegerb/combine/"
cd $COMBINEDIR; eval `scramv1 runtime -sh`; cd -;

# Run the limit
combine -M Asymptotic --run blind --rAbsAcc 0.0005 --rRelAcc 0.0005 $1;

# Set back environment
eval `scramv1 runtime -sh`;

