#!/usr/bin/env python
import os, sys, re, optparse,pickle,shutil



if __name__ == '__main__':
    parser = optparse.OptionParser()

    (options,args) = parser.parse_args()
    #define output dictionary
    output=dict()
    rootFile='vvTreeProducer/tree.root'


    for directory in os.listdir("."):
        if directory.find("ext")!=-1:
            dirOrig=directory.split("_ext")[0]
            dirNew = dirOrig+"_ext"
            os.system("mv {orig} {orig}_Chunk0".format(orig=dirOrig))
            os.system("mv {new} {orig}_Chunk1".format(new=dirNew,orig=dirOrig))
#            print("mv {orig} {orig}_Chunk0".format(orig=dirOrig))
#            print("mv {new} {orig}_Chunk1".format(new=dirNew,orig=dirOrig))


        
    
