import ROOT, os, datetime, re, operator


## ===================================================================
## USAGE:
## needs the combine command available
## takes a comma separated list of regular expressions as input via --scan-parameters

## example:
## python w-helicity-13TeV/scanParamteters.py -i <combine_workspace> --scan-parameters CMS_lumi_13TeV,norm.*left.*Ybin.*12 --outdir <outdir> --npoints 25 --pretend
## ===================================================================

jobstring  = '''#!/bin/sh
ulimit -s unlimited
set -e
cd CMSSWBASE
export SCRAM_ARCH=slc6_amd64_gcc530
eval `scramv1 runtime -sh`
cd OUTDIR
COMBINESTRING

'''

if __name__ == "__main__":

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat('.3f')

    date = datetime.date.today().isoformat()

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] ')
    parser.add_option('-i', '--infile'         , dest='infile' , default=''   , type='string', help='workspace converted from datacard')
    parser.add_option('-o', '--outdir'         , dest='outdir' , default=''   , type='string', help='outdput directory to make jobs and run combine in.')
    parser.add_option('-n', '--npoints'        , dest='npoints', default=50   , type='int'   , help='total number of points to run on scan')
    parser.add_option(      '--points-per-job' , dest='ppj'    , default=1    , type='int'   , help='points of the scan to run per job')
    parser.add_option(      '--scan-parameters', dest='pois'   , default=''   , type='string', help='comma separated list of regexp parameters to run. default is all parameters!')
    parser.add_option(      '--suffix'         , dest='suffix' , default=''   , type='string', help='suffix')
    parser.add_option('-q', '--queue'          , dest='queue'  , default='8nh', type='string', help='use this queue. default 8nh')
    parser.add_option('-p', '--pretend'        , dest='pretend', action='store_true'         , help='only pretend. print commands, don\'t submit')
    parser.add_option('-v', '--verbose'        , dest='verbose', action='store_true'         , help='verbosity level 10. this leads to large outputs.')
    (options, args) = parser.parse_args()

    absopath  = os.path.abspath(os.path.dirname(options.outdir))
    absinfile = os.path.abspath(options.infile)

    if not options.outdir:
        print 'ERROR: give at least an output directory. there will be a YUGE number of jobs!'
    else:
        if not os.path.isdir(absopath):
            print 'making a directory and running in it'
            os.system('mkdir -p {od}'.format(od=absopath))


    jobdir = absopath+'/jobs/'
    if not os.path.isdir(jobdir):
        os.system('mkdir {od}'.format(od=jobdir))

    infile = ROOT.TFile(absinfile, 'read')
    ws = infile.Get('w')

    ## get all the nuisance parameters from the workspace
    #nuisances = w.set('nuisances')
    pars = ws.allVars()
    pars = ROOT.RooArgList(pars)
    ## this has to be a loop over a range... doesn't work otherwise
    parameters = []
    all_parameters = []
    pois_regexps = list(options.pois.split(','))

    ## get the parameters to scan from the list of allVars and match them
    ## to the given regexp
    for i in range(len(pars)):
        tmp_name = pars[i].GetName()
        if '_In' in tmp_name: ## those are the input parameters
            continue
        if tmp_name in ['CMS_th1x', 'r']: ## don't want those
            continue
        all_parameters.append(tmp_name)
        for poi in pois_regexps:
            if re.match(poi, tmp_name): 
                parameters.append(pars[i].GetName())



    for par in parameters:
        pardir = absopath+'/'+par+'/'
        os.system('mkdir -p '+pardir)
        for point in range(options.npoints):
            cmd_base  = 'combine {ws} -M MultiDimFit -t -1 --algo grid --points {np} '.format(ws=absinfile,np=options.npoints)
            cmd_base += ' --cminDefaultMinimizerType GSLMultiMin --cminDefaultMinimizerAlgo BFGS2 '
            cmd_base += ' -P {par} --floatOtherPOIs=1 '.format(par=par)
            #cmd_base+= ' --setParameterRanges <whatever> '
            cmd_base += ' --keepFailures -n _{name}_point{n} '.format(name=par,n=point)
            cmd_base += ' --firstPoint {n} --lastPoint {n} '.format(n=point)
            if options.verbose:
                cmd_base += ' -v 10 '

            ## make new file for evert parameter and point
            job_file_name = jobdir+'/job_{p}_point{n:.0f}.sh'.format(p=par,n=point)
            tmp_file = open(job_file_name, 'w')

            ## fill the whole shebang in there
            tmp_filecont = jobstring
            tmp_filecont = tmp_filecont.replace('COMBINESTRING', cmd_base)
            tmp_filecont = tmp_filecont.replace('CMSSWBASE', os.environ['CMSSW_BASE']+'/src/')
            tmp_filecont = tmp_filecont.replace('OUTDIR', pardir)
            tmp_file.write(tmp_filecont)
            tmp_file.close()
            os.system('chmod u+x {f}'.format(f=job_file_name))

            ## submit the jobs!
            cmd_submit  = 'bsub -q {q} '.format(q=options.queue)
            cmd_submit += ' -o {of} '.format(of=job_file_name.replace('.sh','.log'))
            cmd_submit += ' {jf} '.format(jf=job_file_name)

            if not options.pretend:
                os.system(cmd_submit)
            else:
                print cmd_submit

