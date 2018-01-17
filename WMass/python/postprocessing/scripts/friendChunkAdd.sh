#!/bin/bash
clean=0
if [[ "$1" == "-c" ]]; then
    if test -d Chunks; then
        echo "Dir Chunks existing. Moving friend chunks there";
    else
        echo "Creating Chunks"
        mkdir /tmp/$USER/Chunks;
        ln -s /tmp/$USER/Chunks;
    fi
    clean=1; shift;
fi;

dir="./"
if [[ "$1" != "" ]]; then dir=$1; fi
for F in $(ls ${dir}/*_Friend_*.chunk*.root | sed 's/\.chunk[0-9]\+//' | sort | uniq); do
    if test -f $F; then echo "Merged file $F already exists. skipping."; continue; fi
    FILES=$(ls ${F/.root/.chunk*.root} | \
            perl -npe 's/\.chunk(\d+)\./sprintf(".%06d.",$1)/e' | \
            sort -n | \
            perl -npe 's/\.(\d+)\.root$/sprintf(".chunk%d.root",$1)/e' );
    echo -e "\nWill merge into $F:\n$FILES"; 
    hadd -ff $F $FILES
done

if [[ $clean == 1 ]]; then mv ${dir}/*_Friend_*.chunk*.root Chunks; fi
