#!/usr/bin/env python
import os
import sys
import re
import optparse
import pickle
import shutil


if __name__ == '__main__':
    parser = optparse.OptionParser()

    (options, args) = parser.parse_args()
    # define output dictionary
    output = dict()
    rootFile = 'vvTreeProducer/tree.root'

    for directory in os.listdir("."):
        if directory.find("ext") == -1:
            continue

        # also store extension number to allow for several extensions
        [dirOrig, extOrig] = directory.split("_ext")
        if not extOrig:
            # if there is no numbered extension, there will only be one
            extOrig = 1

        # also need to move the non-extension directory if it exists
        if os.path.isdir(dirOrig):
            os.system("mv {orig} {orig}_Chunk0".format(orig=dirOrig))
        os.system("mv {dir} {orig}_Chunk{ext}".format(
            dir=directory, orig=dirOrig, ext=extOrig))


os.system("haddChunks.py .")
