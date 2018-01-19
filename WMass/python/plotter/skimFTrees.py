import ROOT
import os, sys

# usage: python skimFTrees.py BIGTREE_DIR FTREE_DIR outdir
# for event variables: python skimFTrees.py skims /data1/emanuele/monox/TREES_25ns_1LEPSKIM_76X/friends skims/friends
# for scale factors: python skimFTrees.py skims /data1/emanuele/monox/TREES_25ns_1LEPSKIM_76X/friends skims/friends -f sfFriend -t "sf/t"

def _runIt(args,excludeProcesses=[]):
    (treedir,ftreedir,outdir,treename,ffilename) = args
    dsets = [d.replace(ffilename+'_','').replace('.root','') for d in os.listdir(sys.argv[2]) if ffilename in d]
    dsets = [d for d in dsets if d in os.listdir(treedir)]
    procsToExclude = []
    for p0 in excludeProcesses:
        for p in p0.split(","):
            procsToExclude.append(p)
    if len(excludeProcesses)>0: print "skimFTrees: exlude the following datasets: ", ", ".join(procsToExclude)

    for dset in dsets:
        skipMe = False
        for p in procsToExclude:
            if p in dset: skipMe = True
        if skipMe: continue
        print dset,
        fsel = ROOT.TFile.Open(treedir+'/'+dset+'/selection_eventlist.root')
        elist = fsel.elist
        f_f = ROOT.TFile.Open(ftreedir+'/'+ffilename+'_'+dset+'.root')
        t_f = f_f.Get(treename)
        t_f.SetEventList(elist)
        os.system('mkdir -p %s'%outdir)
        f2 = ROOT.TFile('%s/%s_%s.root'%(outdir,ffilename,dset),'recreate')
        f2.cd()
        #fdirname = [x for x in treename.split('/') if x!=''][0]
        #f2.mkdir(fdirname)
        #f2.cd(fdirname)
        t2 = t_f.CopyTree('1')
        f2.Write()
        print ': skimmed friend trees put in %s'%f2.GetName()
        f2.Close()
        f_f.Close()
        fsel.Close()

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] BIGTREE_DIR FTREE_DIR outdir")
    parser.add_option("-t", "--tree", dest="tree", type="string", default="Friends", help="Name of the friend tree")
    parser.add_option("-f", "--friend", dest="friend", type="string", default="tree_Friend", help="Prefix of the friend ROOT file name")
    parser.add_option("-x", "--exclude-process", dest="excludeProcess", action="append", default=[], help="exclude some processes with a given pattern (comma-separated patterns)")
    (options, args) = parser.parse_args()
    if len(args)<3:
        print "Usage: program <BIGTREE_DIR> <FTREE_DIR> <outdir>"
        exit()

    allargs = (args + [options.tree,options.friend])

    print "Will write the selected friend trees to "+args[2]
    _runIt(allargs,options.excludeProcess)
