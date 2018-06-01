#!/bin/env python

# usage: python submitToys.py ../cards/helicity_2018_03_09_testpdfsymm/Wel_plus_ws.root 1000 plus -n 10

jobstring  = '''#!/bin/sh
ulimit -c 0 -S
ulimit -c 0 -H
set -e
cd CMSSWBASE
export SCRAM_ARCH=slc6_amd64_gcc530
eval `scramv1 runtime -sh`
cd OUTDIR
COMBINESTRING

'''

import ROOT, random, array, os

if __name__ == "__main__":
    
    from optparse import OptionParser
    parser = OptionParser(usage='%prog workspace ntoys [prefix] [options] ')
    parser.add_option('-n'  , '--ntoy-per-job'  , dest='nTj'           , type=int           , default=None , help='split jobs with ntoys per batch job')
    parser.add_option(        '--dry-run'       , dest='dryRun'        , action='store_true', default=False, help='Do not run the job, only print the command');
    parser.add_option('-q'  , '--queue'         , dest="queue"         , type="string"      , default="2nd", help="Select the queue to use");
    parser.add_option(        '--norm-only'     , dest='normonly'      , action='store_true', default=False, help='Run the fit fixing the PDF uncertainties');
    parser.add_option('--fd', '--fitDiagnostics', dest='fitDiagnostics', action='store_true'               , help='run FitDiagnostics instead of MultiDimFit');
    parser.add_option('--outdir', dest='outdir', type="string", default=None, help='outdirectory');
    (options, args) = parser.parse_args()
    
    workspace = args[0]; wsbase = os.path.basename(workspace).split('.')[0]
    ntoys = int(args[1])
    prefix = args[2] if len(args)>2 else wsbase
    charge = 'plus' if 'plus' in wsbase else 'minus'

    comMethod = ('MultiDimFit' if not options.fitDiagnostics else 'FitDiagnostics')
    
    binningFile = open(os.path.dirname(workspace)+'/binningYW.txt')
    binningYW = eval(binningFile.read())
    nbins={}
    for i,j in binningYW.items():
        nbins[i] = len(j)-1

    wsfile = ROOT.TFile(workspace, 'read')
    rws = wsfile.Get('w')
    pars = ROOT.RooArgList(rws.allVars())
        
    POIs = ['r_W{charge}_long'.format(charge=charge)]
    for pol in ['left','right']:
       POIs += ['r_W{charge}_{pol}_W{charge}_{pol}_Ybin_{ib}'.format(charge=charge,pol=pol,ib=i) for i in xrange(nbins[charge+'_left']-1)]
    poiOpt = ' --redefineSignalPOIs '+','.join(POIs)

    trackPars = ' \'rgx{pdf.*|mu.*|alphaS.*|wpt.*|CMS.*}\''
    raiseNormPars = "\"''rgx{r_.*}=1,10''\""
    #cmdBase = "combineTool.py -d {ws} -M {md} -t {nt} -m 999  " # combine method
    cmdBase = "combine -d {ws} -M {md} -t {nt} -m 999 " # combine method
    cmdBase += " --cminDefaultMinimizerType GSLMultiMinMod --cminDefaultMinimizerAlgo BFGS2 --cminDefaultMinimizerTolerance=0.001 " # minimizer
    cmdBase += " --toysFrequentist --bypassFrequentistFit -s {seed} --trackParameters {track} " # toys options
    cmdBase += " %s " % poiOpt # POIs "
    if not options.fitDiagnostics:
        cmdBase+= ' --floatOtherPOIs=1 '
    else:
        cmdBase+= ' --saveNormalizations --skipBOnlyFit --savePredictionsPerToy '

    if options.normonly: cmdBase += " --freezeNuisanceGroups pdfs,scales,alphaS,wpt " # nuisances to freeze
    
    #cmdBase += " -n _{pfx} -s {seed}  --job-mode lxbatch --task-name {taskname} --sub-opts='-q 1nd' %s " % ('--dry-run' if options.dryRun else '') # jobs configuration


    print "Submitting {nt} toys with workspace {ws} and prefix {pfx}...".format(nt=ntoys,ws=workspace,pfx=prefix)

    absopath  = os.path.abspath(options.outdir)
    if not options.outdir:
        raise RuntimeError, 'ERROR: give at least an output directory. there will be a YUGE number of jobs!'
    else:
        if not os.path.isdir(absopath):
            print 'making a directory and running in it'
            os.system('mkdir -p {od}'.format(od=absopath))

    jobdir = absopath+'/jobs/'
    if not os.path.isdir(jobdir):
        os.system('mkdir {od}'.format(od=jobdir))

    random.seed()
    nTj = int(options.nTj)
    jobs = range(int(ntoys/nTj))
    resT = int(ntoys%nTj)
    for j in xrange(int(ntoys/nTj)):
        cmd = cmdBase.format(nt=nTj,ws=os.path.abspath(workspace),pfx=prefix+"_%d"%j,seed=int(random.uniform(0,1000*len(jobs))),md=comMethod,
                             taskname="toys_%s_%d"%(prefix,j),track=trackPars,norm=raiseNormPars)
        cmd += ' -n {name} '.format(name='_toy'+str(j))
        # randomizing initial parameters
        params = list(pars.at(i).GetName() for i in range(len(pars)))
        params = filter(lambda x: not x.startswith('r_') and not x.endswith('_xsec'),params)  # POIs
        params = filter(lambda x: not x.endswith('_In') and not x.endswith('th1x') and x!='MH',params) # inputs and combine internal stuff
        params = filter(lambda x: 'mask' not in x, params) # channel masking
        rndpars = {}
        for p in params:
            par = pars.find(p)
            rndpars[p] = par.getVal() * random.gauss(1,0.2) + random.gauss(0,1.0)
        setParams = ' --setParameters='+','.join(['{param}={val:.2f}'.format(param=k,val=v) for k,v in rndpars.iteritems()])
        ## this is constructed from the ws name. it *should* work. but it's not the most elegant way of doing this
        if options.fitDiagnostics:
            masking_par = '_'.join(['mask']+os.path.basename(workspace).split('_')[:2]+['xsec'])
            setParams += ",{mp}=1 ".format(mp=masking_par)
        cmd += setParams
        
        ## make new file for evert parameter and point
        job_file_name = jobdir+'/job_{j}_toy{n:.0f}To{nn:.0f}.sh'.format(j=j,n=j*nTj,nn=(j+1)*nTj)
        tmp_file = open(job_file_name, 'w')

        ## fill the whole shebang in there
        tmp_filecont = jobstring
        tmp_filecont = tmp_filecont.replace('COMBINESTRING', cmd)
        tmp_filecont = tmp_filecont.replace('CMSSWBASE', os.environ['CMSSW_BASE']+'/src/')
        tmp_filecont = tmp_filecont.replace('OUTDIR', absopath+'/')
        tmp_file.write(tmp_filecont)
        tmp_file.close()
        os.system('chmod u+x {f}'.format(f=job_file_name))
        cmd = 'bsub -o {log} -q {queue} {job}'.format(log=job_file_name.replace('.sh','.log'),queue=options.queue,job=job_file_name)
        if options.dryRun:
            print cmd
        else:
            os.system(cmd)
    #cmd = cmdBase.format(nt=resT,ws=workspace,pfx=prefix+"_%d"%len(jobs),seed=int(random.uniform(0,1000*len(jobs))),md=comMethod,
    #                     taskname="toys_%s_%d"%(prefix,len(jobs)),track=trackPars,norm=raiseNormPars)
    #os.system(cmd)

