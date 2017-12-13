#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [ option(s) ] directory"
    echo "Will run cmgListChunksToResub on all the chunks and make a list of chunks to be resubmitted "
    echo "It runs on both treeProducerWMass/tree.root and JSONAnalyzer/RLTInfo.root " 
    echo "If -r option is given, it will print the command to remove the bad chunks. " 
    echo "If -s option is given, it will save the command to resubmit/remove the bad chunks in a script file named chunksToResub.sh. " 
    echo "If -m option is given, it will save the command to move the good chunks in a script file named chunksToStore.sh. " 
    exit 1;
fi

RM=0
saveList=false # if option -s is passed, it is set to true. If true, the commands are saved in a bash script for later usage

# loop on all options passed and get flags
while true; do
    case "$1" in
        -r )  RM=1; echo "# Will print the command to remove the bad chunks"; shift ;;
        -s )  saveList=true; echo "# Will save the command to resubmit/remove the bad chunks in a script file named chunksToResub.sh"; shift ;;
        -m )  mv=true; echo "# Will save the command to move the good chunks in a script file named chunksToStore.sh"; shift ;;
        -- )            shift; break ;;
        *  )            break ;;
    esac
done

DIR=$1
MVDIR=$2

echo "# Check the trees..."
cmgListChunksToResub -t treeProducerWMass/tree.root -z -p $DIR > clean.sh
echo "# Check the RLTInfo.root..."
cmgListChunksToResub -t JSONAnalyzer/RLTInfo.root -z $DIR >> clean.sh
echo "# Preparing the script to run..."
sort clean.sh | uniq > clean2.sh

# if a file is zombie, a comment is added at the end of the line. 
#This is undesirable because there might be equal chunks not filtered by "uniq" due to the comment at the end of one
# To remove them, we can exploit the fact that the duplicated line with the comment would be sorted as the second line for each pair
# The algorithm compare each line with the previous one (for the very first line, a junk string is used as the previous one). 
# if the read line contains the previous, then it is not written in the file

echo "# File with commands to resubmit/remove failed chunks" > clean2polished.sh
currentLine="VeryFirstLineToBeUsedInTheAlgorithmBelow" # leave it as a junk string 
# starts reading clean2.sh
while read line
do
    previousLine=$currentLine  # backup the previous line
    currentLine=$line          # read the current line

    if [ "$currentLine" == "$previousLine    # zombie" ]; then
	echo "Skipping ====> $currentLine <====  because already present in file"
    else
	echo "$currentLine" >> clean2polished.sh  # save this line if it contains the previous one
    fi 
done < ./clean2.sh

if [[ "$RM" == 0 ]]; then
    echo "#Changing queue from 8nh to 2nd"
    sed 's|cmgResubChunk -q 8nh |cmgResubChunk -q 2nd |g' clean2polished.sh > chunksToResub.sh
else
    sed 's|cmgResubChunk -q 8nh |rm -r |g' clean2polished.sh > chunksToResub.sh
fi;

if [ $mv == "true" ]; then
    ls $DIR | sort > allChunks.txt
    grep $DIR chunksToResub.sh | awk -F "$DIR" '{print $2}' | awk -F "/" '{print $2}' | awk '{print $1}' | sort | uniq > runningChunks.txt
    grep -Fxvf runningChunks.txt allChunks.txt | awk '{print "mv '$DIR'/" $1 " '$MVDIR'"}' > chunksToStore.sh
    echo $DIR " has " `wc allChunks.txt | awk '{print $2}'` " chunks: " `wc runningChunks.txt | awk '{print $2}'` " running, " `wc chunksToStore.sh | awk '{print $1}'` " to be safely moved in " $MVDIR "."
    rm allChunks.txt runningChunks.txt
    if [ $saveList = "false" ]; then 
        cat chunksToStore.sh
        rm chunksToStore.sh
    fi
fi

if [ $saveList = "false" ]; then 
    cat chunksToResub.sh
    rm chunksToResub.sh 
fi

rm clean.sh
rm clean2.sh
rm clean2polished.sh

echo "# DONE."

