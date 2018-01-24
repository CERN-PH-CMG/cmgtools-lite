#!/usr/bin/env python
import sys,os.path
args = sys.argv[:]
sys.argv = ['-b']
import ROOT
sys.argv = args
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

class CheckOneFriend:
    def __init__(self,inputdir,dataset,treeProducer="treeProducerWMass",tree="tree",frienddir="friends",friendPrefix="tree_Friend_",friendTree="Friends"):
        self.file = "/".join([inputdir,dataset,treeProducer,tree+".root"])
        self.friendfile = inputdir+"/"+frienddir+"/"+friendPrefix+dataset+".root"
        self.tree = tree
        self.ftree = friendTree
    def check(self,verbose=0):
        if not os.path.isfile(self.file): 
            print "File %s does not exist!" % self.file
            return False
        tf = ROOT.TFile.Open(self.file)
        tree = tf.Get(self.tree)
        tentries = tree.GetEntries()
        tf.Close()
        if not os.path.isfile(self.file): 
            print "Friend file %s does not exist!" % self.friendfile
            return False
        ff = ROOT.TFile.Open(self.friendfile)
        ftree = ff.Get(self.ftree)
        fentries = ftree.GetEntries()
        ff.Close()
        if tentries != fentries:
            print "ERROR! Friend tree for dataset %s has %d entries, while tree has %d entries!" % (self.file,fentries,tentries)
            return False
        else:
            if verbose>0:
                print "%s OK." % self.file
            return True

if __name__ == "__main__":

    if len(args)<2:
        print "Usage: python checkMergedFriends.py <dir_with_trees>.\n"
        exit(1)

    inputdir = args[1]
    for root,dirs,files in os.walk(inputdir):
        for d in dirs:
            if "friends" in d: continue
            print "Checking dataset %s..." % d
            cf = CheckOneFriend(inputdir,d)
            cf.check(1)
        break
