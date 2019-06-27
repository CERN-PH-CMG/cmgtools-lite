import ROOT
import os, sys


if len(sys.argv) < 3:
    print "usage: python skimFTrees.py BIGTREE_DIR FTREE_DIR [ outdir [ DATASET_NAME ... ] ]"
    sys.exit(1)
elif len(sys.argv) == 3:
    sys.argv.append( sys.argv[1] + "/" + os.path.basename(sys.argv[2].rstrip("/")) )
    print "Will write output to %s " % sys.argv[3]

if len(sys.argv) == 4:
    dsets = [d.replace('_Friend.root','') for d in os.listdir(sys.argv[2]) if '_Friend' in d]
    if not dsets: raise RuntimeError("No friend trees found in %s" % sys.argv[2])
else:
    dsets = sys.argv[4:]

for d in dsets[:]:
    if not os.path.isfile(sys.argv[1]+"/"+d+".root"):
        print "WARNING: dataset %s missing in %s" % (d, sys.argv[1])
        dsets.remove(d)

out = sys.argv[3]
if '{P}' in out: out = out.format(P = sys.argv[1])
if not os.path.isdir(sys.argv[3]):
    os.system("mkdir -p "+sys.argv[3])

for dset in dsets:
    print dset,
    fsel = ROOT.TFile.Open(sys.argv[1]+'/'+dset+'.root')
    if not fsel: raise RuntimeError("Error opening %s"  % sys.argv[1]+'/'+dset+'.root')
    elist = fsel.Get("skimTrees_elist")
    if not elist:
        fsel.ls()
        raise RuntimeError("Can't find %s in %s"  % ("skimTrees_elist", sys.argv[1]+'/'+dset+'.root'))
    f_f = ROOT.TFile.Open(sys.argv[2]+'/'+dset+'_Friend.root')
    if not f_f: raise RuntimeError("Error opening %s"  % sys.argv[2]+'/'+dset+'_Friend.root')
    t_f = f_f.Get("Friends")
    if not t_f: raise RuntimeError("Can't find %s in %s"  % ("Friends", sys.argv[2]+'/'+dset+'_Friend.root'))
    t_f.SetEntryList(elist)
    f2 = ROOT.TFile('%s/%s_Friend.root'%(sys.argv[3],dset),'recreate')
    f2.cd()
    t2 = t_f.CopyTree('1')
    f2.Write()
    print ': skimmed friend trees put in %s'%f2.GetName()
    f2.Close()
    f_f.Close()
    fsel.Close()
