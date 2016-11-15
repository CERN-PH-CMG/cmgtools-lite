#!/usr/bin/env python
import ROOT
import os, fnmatch
 

def _runIt(args):
    (file,options) = args
    print file

    if os.path.isfile(file+".url") and options.override==False:
        print 'root.url file already exists... exiting'
        exit()
    
    fcmd = open(file+".url","w")
    
    eosSnippet = file.split('/eos/cms')
    if len(eosSnippet)==2:
        print "Split seems to have worked; will stitch together root://eoscms.cern.ch/eos/cms/%s"%eosSnippet[1]
    fcmd.write("root://eoscms.cern.ch//eos/cms%s\n" % eosSnippet[1])
    fcmd.close()                                                                                                                                                                                    


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] searchDirCreatingROOTURLFiles")
    parser.add_option("--override",    dest="override", default=False, action="store_true",  help="Overwrite root.url files, if existing") 
    (options, args) = parser.parse_args()

    singleThread = True
    
    inDIR = args[0]
    print inDIR
    pattern = 'tree.root'
    taskList = []
 
    # Walk through directory
    for dName, sdName, fList in os.walk(inDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern): # Match search string
                taskList.append( (os.path.abspath(os.path.join(dName, fileName)), options))

    if singleThread == True: 
        map(_runIt, taskList)
    else:
        from multiprocessing import Pool
        Pool(options.jobs).map(_runIt, fileList)
