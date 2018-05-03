#!/bin/bash
# usage: linkChunks.sh <DIR> [<MATCH> <NEWMATCH>]

# last two arguments are optional:
# first is a match used to select only some folders by name
# second is a new match that will substitute $MATCH in the link name

# example:
# > ls folder
# > WJetsToLNu_part1 WJetsToLNu_part2 DYJetsToLL_M50_part1
# linkChunks.sh folder WJetsToLNu_ WJetsToLNu_NLO_ 
# will select only folders matching WJetsToLNu_, changing this prefix to WJetsToLNu_NLO_

DIR=$1
MATCH=$2
NEWMATCH=$3

chunks=""
if [[ "X${MATCH}" == "X" ]]; then
    chunks=`ls $DIR`
else
    chunks=`ls $DIR | grep $MATCH`
fi

for c in $chunks 
do 
    echo "Linking $c ..." 
    if [[ "X${NEWMATCH}" == "X" ]]; then
	ln -s $DIR/$c
    else
	echo "Link name: ${c/${MATCH}/${NEWMATCH}}"
	ln -s $DIR/$c ${c/${MATCH}/${NEWMATCH}}
    fi
done

echo "DONE."
