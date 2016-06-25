#!/bin/bash

if [  $# = 0 ]; then
    echo "Usage:"
    echo "./makeDirStruct.sh DIR"
    exit 0
else
    InDir=$1
fi

for t in `find $InDir -name "tree.root"`;
do
    fdir=$(basename $(dirname $t))
    tdir=$(dirname $(dirname $t))
    echo "Going into "$tdir
    cd $tdir
    cd $fdir

    if [ ! -d JSONAnalyzer ]; then
	mkdir JSONAnalyzer
	mv JSON.* JSONAnalyzer
	mv RLTInfo.root JSONAnalyzer
    fi

    if [ ! -d VertexAnalyzer ]; then
	mkdir VertexAnalyzer
	mv pileup.* VertexAnalyzer
	mv GoodVertex.* VertexAnalyzer
    fi

    if [ ! -d PileUpAnalyzer ]; then
	mkdir PileUpAnalyzer
	mv vertexWeight.* PileUpAnalyzer
    fi

    if [ ! -d skimAnalyzerCount ]; then
	mkdir skimAnalyzerCount
	mv events.* skimAnalyzerCount
	mv SkimReport.* skimAnalyzerCount
    fi

    if [ ! -d treeProducerSusySingleLepton ]; then
	mkdir treeProducerSusySingleLepton
	mv tree.root treeProducerSusySingleLepton
    fi

    cd -
done
