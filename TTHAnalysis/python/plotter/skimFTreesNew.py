import ROOT
import os, sys, re

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] skimmed_trees_dir input_friends_dir [ out_dir [ dataset_name ... ] ]")
parser.add_option("--pretend",    dest="pretend", default=False, action="store_true",  help="Pretend to skim, don't actually do it") 
parser.add_option("--verbose",    dest="verbose", default=False, action="store_true",  help="More verbose output") 
parser.add_option("--elist", dest="elist", type="string", default="skimTrees_elist", help="Name of the skim elist (default: skimTrees_elist)")
parser.add_option("--new","--skip-existing", dest="skipExisting", default=False, action="store_true",  help="Don't skim samples that already exist in the output directory") 
parser.add_option("--rename", dest="renamePatterns", type="string", default=[], nargs=2, action="append", help="Use --rename from_name to_name to handle cases where a dataset was renamed after skimming; regexp supported (uses re.sub)")
(options, args) = parser.parse_args()

if len(args) < 2:
    print "usage: python skimFTrees.py BIGTREE_DIR FTREE_DIR [ outdir [ DATASET_NAME ... ] ]"
    sys.exit(1)
elif len(args) == 2:
    args.append( args[0] + "/" + os.path.basename(args[1].rstrip("/")) )
    if options.verbose: print "Will write output to %s " % args[2]

if len(args) == 3:
    dsets = [d.replace('_Friend.root','') for d in os.listdir(args[1]) if '_Friend' in d ]
    if not dsets: raise RuntimeError("No friend trees found in %s" % args[1])
else:
    dsets = args[3:]

toDataset = {}
for from_name in dsets:
    to_name = from_name
    for from_pat, to_pat in options.renamePatterns:
        to_name = re.sub(from_pat, to_pat, to_name)
    toDataset[from_name] = to_name

for d in dsets[:]:
    if not os.path.isfile(args[0]+"/"+d+".root"):
        print "WARNING: dataset %s missing in %s" % (d, args[0])
        dsets.remove(d)
    elif options.skipExisting and os.path.isfile(args[2]+"/"+toDataset[d]+"_Friend.root"):
        if options.verbose: print "INFO: Skipping sample %s for which friend already exists" % d
        dsets.remove(d)

out = args[2]
if '{P}' in out: out = out.format(P = args[0])
if not os.path.isdir(args[2]):
    os.system("mkdir -p "+args[2])

for dset in dsets:
    print dset,
    if toDataset[dset] != dset:
        print " -> ",toDataset[dset],
    if options.pretend: 
        print ""; continue
    fsel = ROOT.TFile.Open(args[0]+'/'+toDataset[dset]+'.root')
    if not fsel: raise RuntimeError("Error opening %s"  % args[0]+'/'+toDataset[dset]+'.root')
    elist = fsel.Get(options.elist)
    if not elist:
        fsel.ls()
        raise RuntimeError("Can't find %s in %s"  % (options.elist, args[0]+'/'+toDataset[dset]+'.root'))
    f_f = ROOT.TFile.Open(args[1]+'/'+dset+'_Friend.root')
    if not f_f: raise RuntimeError("Error opening %s"  % args[1]+'/'+dset+'_Friend.root')
    t_f = f_f.Get("Friends")
    if not t_f: raise RuntimeError("Can't find %s in %s"  % ("Friends", args[1]+'/'+dset+'_Friend.root'))
    t_f.SetEntryList(elist)
    f2 = ROOT.TFile('%s/%s_Friend.root'%(args[2],toDataset[dset]),'recreate')
    f2.cd()
    t2 = t_f.CopyTree('1')
    f2.Write()
    print ': skimmed friend trees put in %s'%f2.GetName()
    f2.Close()
    f_f.Close()
    fsel.Close()
