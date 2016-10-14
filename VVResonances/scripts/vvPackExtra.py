#!/usr/bin/env python
import os, sys, re, optparse,pickle,shutil



if __name__ == '__main__':
    parser = optparse.OptionParser()

    (options,args) = parser.parse_args()

    for directory in os.listdir("./"):
        if directory.find("ext")==-1:
            continue
        if directory.find(".")!=-1:
            continue
        dirOrig=directory.split("_ext")[0]
        dirNew = dirOrig+"_ext"
        print dirOrig,dirNew
        os.system("mv {orig} {orig}_Chunk0".format(orig=dirOrig))
        os.system("mv {orig}_ext {orig}_Chunk1".format(orig=dirOrig))
        os.system("rm -rf {orig}.*".format(orig=dirOrig))
        os.system("rm -rf {orig}_ext.*".format(orig=dirOrig))
    os.system("haddChunks .")
    
        
    
