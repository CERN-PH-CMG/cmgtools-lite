#!/usr/bin/env python
import os, sys, re, optparse,pickle,shutil



if __name__ == '__main__':
    parser = optparse.OptionParser()

    (options,args) = parser.parse_args()
    #define output dictionary
    output=dict()
    rootFile='vvTreeProducer/tree.root'


    for directory in os.listdir("."):
        if directory.find("ext")==-1:
            continue
    
        dirOrig=directory.split("_ext")[0]



        os.system("mv {orig} {orig}_Chunk0".format(orig=dirOrig))
        os.system("mv {orig}_ext {orig}_Chunk1".format(orig=dirOrig))



os.system("haddChunks.py .")
        
    
