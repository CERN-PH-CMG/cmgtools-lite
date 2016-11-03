#!/usr/bin/env python
#from mcPlots import *
from CMGTools.TTHAnalysis.plotter.mcAnalysis import *

import array
import json
import ROOT

class CheckEventVetoList:
    _store={}
    def __init__(self,fname):
        self.loadFile(fname)
        print 'Initialized CheckEventVetoList from %s'%fname
        self.name = fname.strip().split('/')[-1]
    def loadFile(self,fname):
        with open(fname, 'r') as f:
            for line in f:
                if len(line.strip()) == 0 or line.strip()[0] == '#': continue
                run,lumi,evt = line.strip().split(':')
                self.addEvent(int(run),int(lumi),long(evt))
    def addEvent(self,run,lumi,evt):
        if (run,lumi) not in self._store:
            self._store[(run,lumi)]=array.array('L')
        self._store[(run,lumi)].append(evt)
    def filter(self,run,lumi,evt):
        mylist=self._store.get((run,lumi),None)
        return ((not mylist) or (long(evt) not in mylist))

class JSONSelector:
    jsonmap = {}
    def __init__(self,jsonfile):
        self.name = "jsonSelector"
        J = json.load(open(jsonfile, 'r'))
        for r,l in J.iteritems():
            self.jsonmap[long(r)] = l
        print "Loaded JSON %s with %d runs\n" % (jsonfile, len(self.jsonmap))
    def filter(self,run,lumi,evt):
        try:
            lumilist = self.jsonmap[run]
            for (start,end) in lumilist:
                if start <= lumi and lumi <= end:
                    return True
            return False
        except KeyError:
            return False

def _runIt(args):
        (tty,mysource,myoutpath,cut,mycut,options,selectors) = args
        mytree = tty.getTree()
        ntot  = mytree.GetEntries() 
        if not options.justcount: print "  Start  %-40s: %8d" % (tty.cname(), ntot)
        timer = ROOT.TStopwatch(); timer.Start()
        # now we do
        os.system("mkdir -p "+myoutpath)
        os.system("cp -r %s/skimAnalyzerCount %s/" % (mysource,myoutpath))
        os.system("mkdir -p %s/%s" % (myoutpath,options.tree))
        histo = ROOT.gROOT.FindObject("Count")
        if not options.oldstyle:
            fout = ROOT.TFile("%s/%s/tree.root" % (myoutpath,options.tree), "RECREATE");
        else:
            fout = ROOT.TFile("%s/%s/%s_tree.root" % (myoutpath,options.tree,options.tree), "RECREATE");
        mytree.Draw('>>elist',mycut)
        elist = ROOT.gDirectory.Get('elist')
        if len(selectors)>0:
            mytree.SetBranchStatus("*",0)
            mytree.SetBranchStatus("run",1)
            mytree.SetBranchStatus("lumi",1)
            mytree.SetBranchStatus("evt",1)
            mytree.SetBranchStatus("isData",1)
            elistveto = ROOT.TEventList("vetoevents","vetoevents")
            for ev in xrange(elist.GetN()):
                tev = elist.GetEntry(ev)
                mytree.GetEntry(tev)
                if not mytree.isData:
                    print "You don't want to filter by event number on MC, skipping for this sample"
                    break
                for selector in selectors:
                    if not selector.filter(mytree.run,mytree.lumi,mytree.evt):
                        if not ('json' in selector.name): print 'Selector %s rejected tree entry %d (%d among selected): %d:%d:%d'%(selector.name,tev,ev,mytree.run,mytree.lumi,mytree.evt)
                        elistveto.Enter(tev)
                        break
            mytree.SetBranchStatus("*",1)
            elist.Subtract(elistveto)
            print '%d events survived vetoes'%(elist.GetN(),)
        if options.justcount:
            print "  As if it were Done   %-40s: %8d/%8d" % (tty.cname(), elist.GetN(), ntot)
            return

        # drop and keep branches
        for drop in options.drop: mytree.SetBranchStatus(drop,0)
        for keep in options.keep: mytree.SetBranchStatus(keep,1)
        f2 = ROOT.TFile("%s/selection_eventlist.root"%myoutpath,"recreate")
        f2.cd()
        elist.Write()
        f2.Close()
        fout.cd()
        mytree.SetEventList(elist)
        out = mytree.CopyTree('1')
        npass = out.GetEntries()
        friends = out.GetListOfFriends() or []
        while friends and friends.GetSize() > 0:
            out.RemoveFriend(friends.At(0).GetTree())
            friends = out.GetListOfFriends() or []
        fout.WriteTObject(out,options.tree if options.oldstyle else "tree")
        if histo: histo.Write()
        fout.Close(); timer.Stop()
        print "  Done   %-40s: %8d/%8d %8.1f min" % (tty.cname(), npass, ntot, timer.RealTime()/60.)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt outputDir")
    parser.add_option("-D", "--drop",  dest="drop", type="string", default=[], action="append",  help="Branches to drop, as per TTree::SetBranchStatus") 
    parser.add_option("-K", "--keep",  dest="keep", type="string", default=[], action="append",  help="Branches to keep, as per TTree::SetBranchStatus") 
    parser.add_option("--oldstyle",    dest="oldstyle", default=False, action="store_true",  help="Oldstyle naming (e.g. file named as <analyzer>_tree.root)") 
    parser.add_option("--vetoevents",  dest="vetoevents", type="string", default=[], action="append",  help="File containing list of events to filter out")
    parser.add_option("--json",        dest="json", type="string", default=None, help="JSON file selecting events to keep")
    parser.add_option("--pretend",    dest="pretend", default=False, action="store_true",  help="Pretend to skim, don't actually do it") 
    parser.add_option("--justcount",  dest="justcount", default=False, action="store_true",  help="Pretend to skim, up to the point of counting passing events") 
    addMCAnalysisOptions(parser)
    (options, args) = parser.parse_args()
    options.weight = False
    options.final = True
    mca  = MCAnalysis(args[0],options)
    cut = CutsFile(args[1],options)
    outdir = args[2]

    print "Will write selected trees to "+outdir
    if not os.path.exists(outdir):
        os.system("mkdir -p "+outdir)

    selectors=[CheckEventVetoList(fname) for fname in options.vetoevents]
    if options.json: selectors.append(JSONSelector(options.json))

    tasks = []
    for proc in mca.listProcesses():
        print "Process %s" % proc
        for tty in mca._allData[proc]:
            print "\t component %-40s" % tty.cname()
            myoutpath = outdir+"/"+tty.cname()
            mysource  = options.path+"/"+tty.cname()
            mycut = tty.adaptExpr(cut.allCuts(),cut=True)
            if options.doS2V: mycut  = scalarToVector(mycut)
            if options.pretend: continue
            tasks.append((tty,mysource,myoutpath,cut,mycut,options,selectors))
    if options.jobs == 0: 
        map(_runIt, tasks)
    else:
        from multiprocessing import Pool
        Pool(options.jobs).map(_runIt, tasks)

