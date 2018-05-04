#!/usr/bin/env python
import sys,os.path,re
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
        if not os.path.isfile(self.friendfile): 
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

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] dir_with_trees")
    parser.add_option(      "--sp", dest="selectProcess",  type="string", default=None, help="Process only datasets that match this regexp (or comma-separated list of regexp)");
    (options, args) = parser.parse_args()

    if len(args)<1:
        print "Usage: python checkMergedFriends.py <dir_with_trees>.\n"
        exit(1)

    sel_processes = []
    if options.selectProcess != None:
        sel_processes = options.selectProcess.split(',')

    inputdir = args[0]
    for root,dirs,files in os.walk(inputdir):
        for d in dirs:
            if "friends" in d: continue
            if options.selectProcess and not any(re.match(proc,d) for proc in sel_processes): continue
            print "Checking dataset %s..." % d
            cf = CheckOneFriend(inputdir,d)
            cf.check(1)
        break
