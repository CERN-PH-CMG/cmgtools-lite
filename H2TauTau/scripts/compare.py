import sys
import numpy as np

import ROOT
from optparse import OptionParser

from varCfg import var_dict
from DisplayManager import DisplayManager

# TODO (welcome by everybody):
# - Please add more variables to varCfg.py if the default range finding doesn't
#   give good results
# - Add ratio plots (YT : 25 Jul done ... please feel free to modify)
# - Extend this list :-)


ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

colours = [1, 2, 3, 6, 8]
styles = [2, 1, 3, 4, 5]

def findTree(f):
    for key in f.GetListOfKeys():
        tree = f.Get(key.GetName())
        if isinstance(tree, ROOT.TTree):
            return tree
        elif isinstance(tree, ROOT.TDirectory):
            return findTree(tree)
    print 'Failed to find a TTree in file', f
    return None

def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetLineStyle(styles[i])
    h.SetLineWidth(3)
    h.SetStats(False)


def comparisonPlots(u_names, trees, titles, pname='sync.pdf', ratio=True):

    display = DisplayManager(pname, ratio)
   
    for branch in u_names:
        nbins = 50
        min_x = min(t.GetMinimum(branch) for t in trees)
        max_x = max(t.GetMaximum(branch) for t in trees)
        title_x = branch

        if min_x == max_x or all(t.GetMinimum(branch) == t.GetMaximum(branch) for t in trees):
            continue

        if min_x < -900 and max_x < -min_x * 1.5:
            min_x = - max_x

        min_x = min(0., min_x)

        if branch in var_dict:
            b_d = var_dict[branch]
            nbins = b_d['nbinsx'] if 'nbinsx' in b_d else nbins
            min_x = b_d['xmin'] if 'xmin' in b_d else min_x
            max_x = b_d['xmax'] if 'xmax' in b_d else max_x
            title_x = b_d['title'] if 'title' in b_d else title_x


        hists = []
        for i, t in enumerate(trees):
            h_name = branch+t.GetName()+str(i)
            h = ROOT.TH1F(h_name, branch, nbins, min_x, max_x + (max_x - min_x) * 0.01)
            h.Sumw2()
            h.GetXaxis().SetTitle(title_x)
            h.GetYaxis().SetTitle('Entries')
            applyHistStyle(h, i)
            t.Project(h_name, branch, '1') # Should introduce weight...
            hists.append(h)


        display.Draw(hists, titles)


def interSect(tree1, tree2, var='evt', common=False, save=False,  titles=[]):
    # run, lumi, evt
    tlist1 = ROOT.TEntryList()
    tlist2 = ROOT.TEntryList()
    
    tree1.Draw(var)
    r_evt1 = tree1.GetV1()
    if len(titles) > 0 and titles[0] == 'Imperial':
        evt1 = np.array([int(r_evt1[i]) & 0xffffffff for i in xrange(tree2.GetEntries())], dtype=int)
    else:
        evt1 = np.array([r_evt1[i] for i in xrange(tree1.GetEntries())], dtype=int)

    tree2.Draw(var)
    r_evt2 = tree2.GetV1()
    if len(titles) > 1 and titles[1] == 'Imperial':
        evt2 = np.array([int(r_evt2[i]) & 0xffffffff for i in xrange(tree2.GetEntries())], dtype=int)
    else:
        evt2 = np.array([int(r_evt2[i]) for i in xrange(tree2.GetEntries())], dtype=int)

    if common:
        indices1 = np.nonzero(np.in1d(evt1, evt2))
        indices2 = np.nonzero(np.in1d(evt2, evt1))
    else:
        indices1 = np.nonzero(np.in1d(evt1, evt2) == 0)
        indices2 = np.nonzero(np.in1d(evt2, evt1) == 0)

    if save:
        if len(titles) < 2:
            titles = ['tree1', 'tree2']

        evt1[indices1].tofile(titles[0]+'.csv', sep=',', format='%d')
        evt2[indices2].tofile(titles[1]+'.csv', sep=',', format='%d')

    for ind1 in indices1[0]:
        tlist1.Enter(ind1)

    for ind2 in indices2[0]:
        tlist2.Enter(ind2)

    return tlist1, tlist2


def scanForDiff(tree1, tree2, branch_names, scan_var='pt_1', index_var='evt'):
    # tree1.BuildIndex(index_var)
    # index1 = tree1.GetTreeIndex()
    tree2.BuildIndex(index_var)

    diff_events = []

    for entry_1 in tree1:
        ind = int(getattr(tree1, index_var))
        tree2.GetEntryWithIndex(ind)

        var1 = getattr(tree1, scan_var)
        var2 = getattr(tree2, scan_var)

        if tree1.evt != tree2.evt:
            continue

        if round(var1, 4) != round(var2, 4): 
            diff_events.append(ind)
            print 'Event', ind
            for branch in branch_names:
                v1 = getattr(tree1, branch)
                v2 = getattr(tree2, branch)
                if round(v1, 4) != round(v2, 4) and v1 > -99.:
                    print '{b:>43}: {v1:>8.5f}, {v2:>8.5f}'.format(b=branch, v1=v1, v2=v2)
            print

    print 'Found', len(diff_events), 'events with differences in', scan_var
    print diff_events


if __name__ == '__main__':
        
    usage = '''
%prog [options] arg1 arg2 ... argN

    Compares first found trees in N different root files; 
    in case of two root files, additional information about the event overlap
    will be calculated.

    Example run commands:

> python compare.py /afs/cern.ch/user/s/steggema/public/Sync2015/mt/SUSYGluGluToHToTauTau_M-160_spring15.root /afs/cern.ch/work/a/adewit/public/syncNtuples/sync-100715/SYNCFILE_SUSYGluGluToHToTauTau_M-160_mt_spring15.root -t CERN,Imperial

> python compare.py /afs/cern.ch/user/s/steggema/public/Sync2015/mt/SUSYGluGluToHToTauTau_M-160_spring15.root /afs/cern.ch/user/f/fcolombo/public/SUSYGluGluToHToTauTauM160_mt_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM.root /afs/cern.ch/work/a/adewit/public/syncNtuples/sync-100715/SYNCFILE_SUSYGluGluToHToTauTau_M-160_mt_spring15.root -t CERN,KIT,Imperial
'''

    parser = OptionParser(usage=usage)

    parser.add_option('-t', '--titles', type='string', dest='titles', default='Imperial,KIT', help='Comma-separated list of titles for the N input files (e.g. Imperial,KIT)')
    parser.add_option('-i', '--no-intersection', dest='do_intersect', action='store_false', default=True, help='Do not produce plots for events not in common')
    parser.add_option('-c', '--no-common', dest='do_common', action='store_false', default=True, help='Do not produce plots for events in common')
    parser.add_option('-r', '--no-ratio', dest='do_ratio', action='store_false', default=True, help='Do not show ratio plots')
    parser.add_option('-d', '--diff', dest='do_diff', action='store_true', default=False, help='Print events where single variable differs')
    parser.add_option('-v', '--var-diff', dest='var_diff', default='pt_1', help='Variable for printing single event diffs')

    (options,args) = parser.parse_args()

    if len(args) < 2:
        print 'provide at least 2 input root files'
        sys.exit(1)

    titles = options.titles.split(',')
    
    if len(titles) < len(args):
        print 'Provide at least as many titles as input files'
        sys.exit(1)

    for i, arg in enumerate(args):
        if arg.endswith('.txt'):
            f_txt = open(arg)
            for line in f_txt.read().splitlines():
                line.strip()
                if line.startswith('/afs'):
                    args[i] = line
                    break

    tfiles = [ROOT.TFile(arg) for arg in args]

    trees = [findTree(f) for f in tfiles]

    # find all branches that exist in all files

    b_names = [set([b.GetName() for b in t.GetListOfBranches()]) for t in trees]

    u_names = set.intersection(*b_names)

    u_names = sorted(u_names)

    print 'Making plots for all common branches', u_names

    comparisonPlots(u_names, trees, titles, 'sync.pdf', options.do_ratio)


    if len(trees) == 2 and options.do_intersect:
        intersect = interSect(trees[0], trees[1], save=True, titles=titles)
        trees[0].SetEntryList(intersect[0])
        trees[1].SetEntryList(intersect[1])
        if not all(l.GetN() == 0 for l in intersect):
            comparisonPlots(u_names, trees, titles, 'intersect.pdf', options.do_ratio)


    if len(trees) == 2 and options.do_common:
        intersect = interSect(trees[0], trees[1], common=True)
        trees[0].SetEntryList(intersect[0])
        trees[1].SetEntryList(intersect[1])
        comparisonPlots(u_names, trees, titles, 'common.pdf', options.do_ratio)

    if len(trees) == 2 and options.do_diff:
        scanForDiff(trees[0], trees[1], u_names, scan_var=options.var_diff)
    
