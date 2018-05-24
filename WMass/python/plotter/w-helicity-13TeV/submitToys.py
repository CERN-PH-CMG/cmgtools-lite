#!/bin/env python

# usage: python submitToys.py ../cards/helicity_2018_03_09_testpdfsymm/Wel_plus_ws.root 1000 plus -n 10

import ROOT, random, array, os

if __name__ == "__main__":
    
    from optparse import OptionParser
    parser = OptionParser(usage='%prog workspace ntoys [prefix] [options] ')
    parser.add_option('-n','--ntoy-per-job', dest='nTj', default=None, type=int, help='split jobs with ntoys per batch job')
    parser.add_option(     '--dry-run', dest='dryRun',   action='store_true', default=False, help='Do not run the job, only print the command');
    parser.add_option(     '--norm-only', dest='normonly',   action='store_true', default=False, help='Run the fit fixing the PDF uncertainties');
    (options, args) = parser.parse_args()
    
    workspace = args[0]; wsbase = os.path.basename(workspace).split('.')[0]
    ntoys = int(args[1])
    prefix = args[2] if len(args)>2 else wsbase
    charge = 'plus' if 'plus' in wsbase else 'minus'
    
    binningFile = open(os.path.dirname(workspace)+'/binningYW.txt')
    binningYW = eval(binningFile.read())
    nbins={}
    for i,j in binningYW.items():
        nbins[i] = len(j)-1
        
    POIs = ['r_W{charge}_long'.format(charge=charge)]
    for pol in ['left','right']:
       POIs += ['r_W{charge}_{pol}_W{charge}_{pol}_Ybin_{ib}'.format(charge=charge,pol=pol,ib=i) for i in xrange(nbins[charge+'_left']-1)]
    poiOpt = ' --redefineSignalPOIs '+','.join(POIs)

    trackPars = "'\"''rgx{pdf.*|mu.*|alphaS.*|wpt.*|CMS.*}''\"'"
    raiseNormPars = "'\"''rgx{r_.*}=1,10''\"'"
    cmdBase = "combineTool.py -d {ws} -M MultiDimFit -t {nt} -m 999 {savefr} " # combine method
    cmdBase += " --cminDefaultMinimizerType GSLMultiMinMod --cminDefaultMinimizerAlgo BFGS2 --cminDefaultMinimizerTolerance=0.001 " # minimizer
    cmdBase += " --toysFrequentist --bypassFrequentistFit -s {seed} --trackParameters {track} " # toys options
    cmdBase += " %s --floatOtherPOIs=1 " % poiOpt # POIs
    if options.normonly: cmdBase += " --freezeNuisanceGroups pdfs,scales,alphaS,wpt " # nuisances to freeze
    cmdBase += " -n _{pfx} -s {seed}  --job-mode lxbatch --task-name {taskname} --sub-opts='-q 8nh' %s " % ('--dry-run' if options.dryRun else '') # jobs configuration

    print "Submitting {nt} toys with workspace {ws} and prefix {pfx}...".format(nt=ntoys,ws=workspace,pfx=prefix)

    if options.nTj==None or ntoys<options.nTj:
        cmd = cmdBase.format(nt=ntoys,ws=workspace,pfx=prefix,seed=12345,taskname='toys_'+prefix,track=trackPars,norm=raiseNormPars,savefr='--saveFitResult')
        os.system(cmd)
    else:
        random.seed()
        nTj = int(options.nTj)
        jobs = range(int(ntoys/nTj))
        resT = int(ntoys%nTj)
        for j in xrange(int(ntoys/nTj)):
            cmd = cmdBase.format(nt=nTj,ws=workspace,pfx=prefix+"_%d"%j,seed=int(random.uniform(0,1000*len(jobs))),
                                 taskname="toys_%s_%d"%(prefix,j),track=trackPars,norm=raiseNormPars,savefr='--saveFitResult' if j==0 else '')
            os.system(cmd)
        cmd = cmdBase.format(nt=resT,ws=workspace,pfx=prefix+"_%d"%len(jobs),seed=int(random.uniform(0,1000*len(jobs))),
                             taskname="toys_%s_%d"%(prefix,len(jobs)),track=trackPars,norm=raiseNormPars,savefr='')
        os.system(cmd)

