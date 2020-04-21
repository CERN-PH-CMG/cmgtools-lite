import ROOT
import os, sys

# this script can be used to verify that a friend tree has the same number of entries as the main tree
# (useful to check that all chunks in the friend tree production have been done successfully)
#
# usage: python verifyFTree BIGTREE_DIR FTREE_DIR DATASET_NAME ...

dsets = sys.argv[3:]
if len(sys.argv)<4:
    # dsets = [d.replace('_Friend','').replace('.root','') for d in os.listdir(sys.argv[2]) if ('_Friend' in d and 'chunk' not in d)]
    dsets = [ d.replace('.root','') for d in os.listdir(sys.argv[1]) if '.root' in d]

def openRootOrUrl(myfile):
    _f_t = None
    if os.path.exists(myfile):
        _f_t = ROOT.TFile.Open(myfile)
    elif os.path.exists(myfile+'.url'):
        with open(myfile+'.url','r') as urlf:
            myfile = urlf.readline().replace('\n','')
            if myfile.startswith("root://"):
                _f_t = ROOT.TXNetFile(myfile)
            else:
                _f_t = ROOT.TFile.Open(myfile)
    return _f_t

allok = True
tot_ev = 0
tot_comp = 0
for dset in dsets:
    if '.url' in dset: continue
    # print "running " + dset
    f_t = openRootOrUrl(sys.argv[1]+dset+'.root')
    t_t = f_t.Get("Events")
    n_t = t_t.GetEntries()
    f_t.Close()
    f_f = openRootOrUrl(sys.argv[2]+'/'+dset+'_Friend.root')
    if not f_f: 
        print dset, ' NOT THERE!', 'ERROR '*15
        continue
    t_f = f_f.Get("Friends")
    if not t_f: 
        print dset, ' NOT THERE!', 'ERROR '*15
        continue
    n_f = t_f.GetEntries()
    f_f.Close()
    print '%s: %d - %d : %s'%(dset,n_t,n_f,'OK' if n_t==n_f else 'ERROR '*15+' !!!')
    if not (n_t==n_f): allok = False
    tot_ev += n_f
    tot_comp += 1

if allok:
    print '--- ALL OK --- (%d components, %d events)'%(tot_comp,tot_ev)
    sys.exit(0)
else:
    sys.exit(1)
