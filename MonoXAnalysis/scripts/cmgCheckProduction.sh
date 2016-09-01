#!/bin/bash
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [ -r ] "
    echo "Will run cmgListChunksToResub on all the chunks and make a list of chunks to be resubmitted "
    echo "It runs on both treeProducerDarkMatterMonoJet/tree.root and JSONAnalyzer/RLTInfo.root " 
    echo "If -r option is given, it will print the command to remove the bad chunks. " 
    exit 1;
fi

RM=0
if [[ "$1" == "-r" ]]; then
    echo "# Will print the command to remove the bad chunks"
    RM=1; shift;
fi;

echo "# Check the trees..."
cmgListChunksToResub -t treeProducerDarkMatterMonoJet/tree.root -z > clean.sh
echo "# Check the RLTInfo.root..."
cmgListChunksToResub -t JSONAnalyzer/RLTInfo.root -z >> clean.sh
echo "# Preparing the script to run..."
sort clean.sh | uniq > clean2.sh

if [[ "$RM" == 0 ]]; then
    sed 's|cmgResubChunk -q 8nh |cmgResubChunk -q 2nd |g' clean2.sh
else
    sed 's|cmgResubChunk -q 8nh |rm -r |g' clean2.sh
fi;

rm clean.sh
rm clean2.sh
echo "# DONE."
