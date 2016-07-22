#!/usr/bin/env python
import ROOT
import pickle, os, random, sys
from PhysicsTools.HeppyCore.statistics.counter import Counter

# FIXME: there is a problem with the friend trees
# the idea was to include the friend trees using the option -F and
# to split them in parallel to the main tree, but for some reason
# ROOT has a problem with the TEventList; so for now, this option
# is commented and not working, still keep it for later in order 
# to be able to make it run once we have more time

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] outputDir inputDirs")
    parser.add_option("-t", "--tree",  dest="tree", default='treeProducerSusyMultilepton', help="Pattern for tree name");
    parser.add_option("-u", "--url",  dest="url", default=None, help="Url to remotely save the produced trees")
    parser.add_option("-q", dest="queue", default=None, help="Queue to send jobs (one per dataset/chunk)")
    parser.add_option("-D", "--drop",  dest="drop", type="string", default=[], action="append",  help="Branches to drop, as per TTree::SetBranchStatus") 
    parser.add_option("-K", "--keep",  dest="keep", type="string", default=[], action="append",  help="Branches to keep, as per TTree::SetBranchStatus") 
    parser.add_option("--pdgId1",  dest="pdgId1", type="int", default=1000023, help="PdgId of the first particle in the scan.") 
    parser.add_option("--pdgId2",  dest="pdgId2", type="int", default=1000022, help="PdgId of the second particle in the scan.") 
    #parser.add_option("-F", "--add-friend",    dest="friendTrees",  action="append", default=[], nargs=2, help="Add a friend tree (treename, filename). Can use {name}, {cname} patterns in the treename") 

    (options, args) = parser.parse_args()

    for _in in args[1:]:

        if options.queue:
            basecmd = "echo bsub -q {queue} {macros}/lxbatch_runner_noWorkDir.sh {cmssw} python {self} -t {tree} {output} {idir}".format(
                macros = '/'.join(sys.argv[0].split('/')[:-1])+'/../../macros', queue = options.queue, cmssw = os.environ['CMSSW_BASE'],
                self=sys.argv[0], tree=options.tree, output=args[0], idir=_in
                )
            for br in options.drop: basecmd+=' -D %s'%br
            for br in options.keep: basecmd+=' -K %s'%br
            if options.url: basecmd+=' -u %s'%options.url
            os.system(basecmd)
            continue


        indir = _in.strip()
        dset = indir.strip().split('/')[-1]
        remdir = args[0].strip()
        outdir = 'splitoutput'
        treename = options.tree
        allmasses={}
        #allmassesfriends=[]

        if not os.path.exists(outdir):
            os.system("mkdir -p "+outdir)

        print "Will write selected trees to "+remdir
        if not os.path.exists(remdir):
            os.system("mkdir -p "+remdir)

        #thename = indir.rstrip("/")
        #thepath = thename[0:thename.rfind("/")]
        #thename = thename[thename.rfind("/")+1:]
        #_friends = []
        #fnames = []
        #friendOpts = options.friendTrees[:]
        #for tf_tree,tf_file in friendOpts:
        #    fname = tf_file.format(name=thename, cname=thename, P=thepath)
        #    tf = ROOT.TFile.Open(fname, "read")
        #    _friends.append(getattr(tf, tf_tree))
        #    allmassesfriends.append({})
        #    fnames.append(fname)

        fname = '%s/%s/tree.root'%(indir,treename)
        if not os.path.exists(fname) and os.path.exists(fname+'.url'):
            fname = open(fname+".url","r").readline().strip()
        f = ROOT.TFile.Open(fname,'read')
        t = f.tree

        print 'Total events: %d originally, %d after production skim'%(t.GetEntries(),t.GetEntries())

        t.SetBranchStatus('*',0)
        t.SetBranchStatus('nGenPart',1)
        t.SetBranchStatus('GenPart_pdgId',1)
        t.SetBranchStatus('GenPart_mass' ,1)
        for nev in xrange(t.GetEntries()):
            if nev%1000==0: print 'Scanning event %d'%nev
            t.GetEntry(nev)
            mass1 = 0
            mass2 = 0
            for i in range(t.nGenPart):
                if abs(t.GenPart_pdgId[i]) == options.pdgId1: 
                    mass1 = t.GenPart_mass[i]
                    continue
                if abs(t.GenPart_pdgId[i]) == options.pdgId2: 
                    mass2 = t.GenPart_mass[i]
                    continue
            m = (mass1,mass2)
            if m not in allmasses:
                mname = '%s_%s'%(m[0],m[1])
                allmasses[m] = ROOT.TEventList(mname,mname)
                #for f in range(len(_friends)): 
                #    mname += "_%d"%f
                #    allmassesfriends[f][m] = ROOT.TEventList(mname,mname)
            allmasses[m].Enter(nev)
            #for f in range(len(_friends)): allmassesfriends[f][m].Enter(nev)

        #for f in range(len(_friends)): sorted(allmassesfriends[f].keys())        
        for m in sorted(allmasses.keys()): print '(%d,%d): %d events'%(m[0],m[1],allmasses[m].GetN())

        t.SetBranchStatus("*",1)
        for drop in options.drop: t.SetBranchStatus(drop,0)
        for keep in options.keep: t.SetBranchStatus(keep,1)

        for m,elist in allmasses.iteritems():
            splitdir = '%s/SMS_%d_%d_%s_Chunk%d'%(outdir,m[0],m[1],dset,random.randint(1e5,1e10))
            os.system("mkdir -p "+splitdir)
            os.system("mkdir -p %s/%s"%(splitdir,treename))
            if os.path.exists('%s/%s/%s/tree.root'%(remdir,splitdir.split('/')[-1],treename)): raise RuntimeError, 'Output file already exists'
            fout = ROOT.TFile('%s/%s/tree.root'%(splitdir,treename),'recreate')
            fout.cd()
            t.SetEventList(elist)
            out = t.CopyTree('1')
            fout.WriteTObject(out,'tree')
            fout.Close()

            cx = Counter('SkimReport')
            cx.register('All Events')
            cx.register('Sum Weights')
            cx.inc('All Events', elist.GetN())
            cx.inc('Sum Weights', elist.GetN())
            #cx.inc('All Events', h.GetBinContent(h.GetXaxis().FindBin(m[0]),h.GetYaxis().FindBin(m[1]),1))
            #cx.inc('Sum Weights', hw.GetBinContent(hw.GetXaxis().FindBin(m[0]),hw.GetYaxis().FindBin(m[1]),1))
            os.system("mkdir -p %s/skimAnalyzerCount"%splitdir)
            cx.write('%s/skimAnalyzerCount'%splitdir)
            if options.url:
                os.system('archiveTreesOnEOS.py --auto -t %s --dset %s %s %s'%(treename,splitdir.split('/')[-1],outdir,options.url))
            os.system('rsync -av %s %s'%(splitdir.rstrip('/'),remdir))
            os.system('rm %s/%s/tree.root'%(splitdir,treename))
            os.system('rm %s/%s/tree.root.url'%(splitdir,treename))
            os.system('rm %s/skimAnalyzerCount/SkimReport.pck'%splitdir)
            os.system('rm %s/skimAnalyzerCount/SkimReport.txt'%splitdir)
            os.system('rmdir %s/%s'%(splitdir,treename))
            os.system('rmdir %s/skimAnalyzerCount'%splitdir)
            os.system('rmdir %s'%splitdir)
            os.system('rmdir %s'%outdir)

        #for f, t in enumerate(_friends): 
        #    t.SetBranchStatus("*",1)
        #    tf_tree, tf_file = friendOpts[f]
        #    fname = fnames[f].rstrip(".root")
        #    for m,elist in allmassesfriends[f].iteritems():
        #        fout = ROOT.TFile("%s/splittedFriends%d/%s_%d_%d.root"%(outdir,f,fname,m[0],m[1]), "recreate")
        #        fout.cd()
        #        t.SetEventList(elist)
        #        out = t.CopyTree("1") 
        #        fout.WriteTObject(out,tf_tree)
        #        fout.Close()
