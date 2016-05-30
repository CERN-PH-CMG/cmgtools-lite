#!/bin/zsh

file=$1

verb=0
lumi=2.3

./makeQCDtemplateFit.py $file -b -l $lumi -v $verb
./makeQCDtemplateFit.py $file -b -l $lumi -v $verb --mc
./makeQCDtemplateFit.py $file -b -l $lumi -v $verb --mc -c

./makeQCDtemplateFit.py $file -b -l $lumi -v $verb -i
./makeQCDtemplateFit.py $file -b -l $lumi -v $verb -i --mc
./makeQCDtemplateFit.py $file -b -l $lumi -v $verb -i --mc -c
