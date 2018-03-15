# usage: python submitToys.py ../cards/helicity_2018_03_09_testpdfsymm/Wel_plus_ws.root 1000 plus -n 10

import ROOT, random, array, os

if __name__ == "__main__":
    
    from optparse import OptionParser
    parser = OptionParser(usage='%prog workspace ntoys [prefix] [options] ')
    parser.add_option('-n','--ntoy-per-job', dest='nTj', default=None, type=int, help='split jobs with ntoys per batch job')
    parser.add_option(     '--dry-run', dest='dryRun',   action='store_true', default=False, help='Do not run the job, only print the command');
    (options, args) = parser.parse_args()
    
    workspace = args[0]
    ntoys = int(args[1])
    prefix = args[2] if len(args)>2 else 'toys'
    
    print "Submitting {nt} toys with workspace {ws} and prefix {pfx}...".format(nt=ntoys,ws=workspace,pfx=prefix)

    trackPars = "'\"''rgx{norm_.*|pdf.*}''\"'"
    cmdBase = "combineTool.py -d {ws} -M MultiDimFit -t {nt} --expectSignal=1 -m 999 --saveFitResult --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1 --redefineSignalPOIs norm_Wplus_long --floatOtherPOIs=0 --freezeNuisanceGroups efficiencies,fixedY --toysNoSystematics -n _{pfx} -s {seed} --trackParameters {track} --job-mode lxbatch --task-name {taskname} --sub-opts='-q 8nh' {dry}"
    
    if options.nTj==None or ntoys<options.nTj:
        cmd = cmdBase.format(nt=ntoys,ws=workspace,pfx=prefix,seed=12345,taskname='toys_'+prefix,dry='--dry-run' if options.dryRun else '',track=trackPars)
        print cmd
        os.system(cmd)
    else:
        random.seed()
        nTj = int(options.nTj)
        jobs = range(int(ntoys/nTj))
        resT = int(ntoys%nTj)
        for j in xrange(int(ntoys/nTj)):
            cmd = cmdBase.format(nt=nTj,ws=workspace,pfx=prefix+"_%d"%j,seed=int(random.uniform(0,1000*len(jobs))),taskname="toys_%s_%d"%(prefix,j),
                                 dry='--dry-run' if options.dryRun else '',track=trackPars)
            os.system(cmd)
        cmd = cmdBase.format(nt=resT,ws=workspace,pfx=prefix+"_%d"%len(jobs),seed=int(random.uniform(0,1000*len(jobs))),taskname="toys_%s_%d"%(prefix,len(jobs)),
                             dry='--dry-run' if options.dryRun else '',track=trackPars)
        os.system(cmd)

