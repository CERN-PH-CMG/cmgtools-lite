#!/bin/zsh

if [  $# = 0 ]; then
    echo "Usage:"
    echo "./mergeChunk.sh [INDIR] [OUTDIR]"
    exit 0
else
    InDir=$(readlink -f $1)
fi

if [ $# -ge 1 ]; then
    OutDir=$2
else
    OutDir="."
fi

OutDir=$(readlink -f $OutDir)

if [ ! -d $OutDir ]; then
    mkdir -p $OutDir
fi

echo "#################"
echo "Input dir is" $InDir
echo "Output dir is" $OutDir

longList=longList

echo "#################"
echo "Retrieving the sample list"

#for f in $(ls $InDir/*chunk*.root);
#for f in  $InDir/*chunk*.root;
#do
#    name=$(basename $f)
#    name=${f/.chunk/!}
#    name=$(echo $name | cut -d '!' -f 1)
#    echo $name >> $longList
#done
find $InDir  -name "*.chunk*.root" -type f -printf "%f\n" | cut -d "." -f1 | sort -u >> $longList

shortList=$(cat $longList | sort -u)

echo "#################"
echo 'Here is the short list'
echo $shortList

echo "#################"
echo "Going to submit $(echo $shortList |wc -l ) task(s) for merging"

for f in $(echo $shortList);
do
    samp=$(basename $f)
    echo "Going to hadd" $samp

    nohup hadd -f -k $OutDir/$samp'.root' $InDir/$samp.chunk* 2>&1 > $OutDir/$samp.log &
done

rm longList
