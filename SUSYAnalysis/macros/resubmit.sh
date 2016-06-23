#!/bin/zsh

if [  $# = 0 ]; then
    echo "Usage:"
    echo "./resubmit.sh [Pattern]"
    echo "Pattern like: logs/CMGrunner.o11"
    exit 0
else
    #InDir=$(readlink -f $1)
    pattern=$1
fi

# settings
matchString="Complete"
jobList="resub.list"

if [ -f $jobList ]; then
    rm $jobList
fi

touch $jobList

# get list of logs
for log in `ls $pattern*`;
do
    lastline=$(tail -1 $log)
    if [[ $lastline != *$matchString* ]]; then
	#echo "Checking $log"
	subcmd=$(grep "prepareEventVariablesFriendTree.py" $log)
	#subcmd=$(cat $log | grep prepare)
	echo $subcmd
	echo $subcmd >> $jobList
    fi
done

# modify joblist
njobs=0
njobs=$(cat $jobList | wc -l)

echo "Found $njobs incomplete jobs in" $jobList

if [ $njobs -ne 0 ] ; then
    # clean strings
    sed -i 's/Going to execute //' $jobList
    # submit
    qsub -t 1-$njobs -o logs nafbatch_runner.sh $jobList
fi
