#!/usr/bin/env python
import ROOT
import os, fnmatch
 

def _runIt(file):
    print file
    rootfile = open(file,"r").readline().strip()
    print rootfile
    f = ROOT.TFile.Open(rootfile)
    t = f.Get("tree")
#    t.Print()
    
    t.SetBranchStatus("*",0)
    t.SetBranchStatus("run",1)
    t.SetBranchStatus("lumi",1)
    t.SetBranchStatus("evt",1)
    t.SetBranchStatus("isData",1)

    
    #--- Write to new file 
    newFile = ROOT.TFile(file.replace(".url",""),"RECREATE") 
    t_new = t.CloneTree()

    t_new.Print()
    newFile.Write()



if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] searchDirForCreatingDummies")
#    parser.add_option("-D", "--drop",  dest="drop", type="string", default=[], action="append",  help="Branches to drop, as per TTree::SetBranchStatus") 
#    parser.add_option("-K", "--keep",  dest="keep", type="string", default=[], action="append",  help="Branches to keep, as per TTree::SetBranchStatus") 
#    parser.add_option("--pretend",    dest="pretend", default=False, action="store_true",  help="Pretend to skim, don't actually do it") 
    (options, args) = parser.parse_args()

    singleThread = True
    
    inDIR = args[0]
    print inDIR
    pattern = 'tree.root.url'
    fileList = []
 
    # Walk through directory
    for dName, sdName, fList in os.walk(inDIR):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern): # Match search string
                fileList.append(os.path.join(dName, fileName))


    if singleThread == True: 
        map(_runIt, fileList)
    else:
        from multiprocessing import Pool
        Pool(options.jobs).map(_runIt, fileList)
