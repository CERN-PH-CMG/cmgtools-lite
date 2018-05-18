import ROOT, os, datetime, re, operator
from array import array


## ===================================================================
## USAGE:
## needs the combine command available
## takes a comma separated list of regular expressions as input via --scan-parameters

## example:
## python w-helicity-13TeV/scanParamteters.py -i <combine_workspace> --scan-parameters CMS_lumi_13TeV,norm.*left.*Ybin.*12 --outdir <outdir> --npoints 25 --pretend
## ===================================================================

def graphStyle(graph):
    graph.SetMarkerStyle(20)
    graph.SetMarkerColor(ROOT.kOrange+7)
    graph.SetLineColor  (ROOT.kAzure-4)
    graph.SetLineWidth  (2)
    graph.SetMarkerSize(1.0)
    graph.GetYaxis().SetTitle('-2 #Delta ln L')
    graph.GetYaxis().SetRangeUser(-0.01, 4.0)


def getGraph(infile, par, norm, treename='limit'):
    f = ROOT.TFile(infile,'read')
    tree = f.Get(treename)
    vals = []
    normval = norm if norm else 1.
    for ev in tree:
        vals.append( [getattr(ev, par)/normval, 2.*ev.deltaNLL] )
    vals = sorted(vals)
    graph = ROOT.TGraph(len(vals), array('d', [x[0] for x in vals]), array('d', [y[1] for y in vals]) )
    graphStyle(graph)
    graph.GetXaxis().SetTitle(par)
    graph.SetTitle('scan for '+par)
    return graph

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
    parser.add_option('-i', '--infile'         , dest='infile'     , default=''   , type='string', help='workspace converted from datacard')
    parser.add_option('-o', '--outdir'         , dest='outdir'     , default=''   , type='string', help='outdput directory to make jobs and run combine in.')
    parser.add_option('-n', '--npoints'        , dest='npoints'    , default=50   , type='int'   , help='total number of points to run on scan')
    parser.add_option(      '--points-per-job' , dest='ppj'        , default=5    , type='int'   , help='points of the scan to run per job')
    parser.add_option(      '--scan-parameters', dest='pois'       , default=''   , type='string', help='comma separated list of regexp parameters to run. default is all parameters!')
    parser.add_option(      '--suffix'         , dest='suffix'     , default=''   , type='string', help='suffix')
    parser.add_option('-q', '--queue'          , dest='queue'      , default='8nh', type='string', help='use this queue. default 8nh')
    parser.add_option('-p', '--pretend'        , dest='pretend'    , action='store_true'         , help='only pretend. print commands, don\'t submit')
    parser.add_option('-v', '--verbose'        , dest='verbose'    , action='store_true'         , help='verbosity level 10. this leads to large outputs.')
    parser.add_option(      '--postprocess'    , dest='postprocess', action='store_true'         , help='hadd all files in the output directories')
    parser.add_option(      '--overwrite'      , dest='overwrite'  , action='store_true'         , help='overwrite the hadding')
    parser.add_option(      '--webdir'         , dest='webdir'     , default=''   , type='string', help='web directory to save the likelihood scans')
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


    if not options.postprocess:

        for par in parameters:
            pardir = absopath+'/'+par+'/'
            os.system('mkdir -p '+pardir)
            print 'at parameter {p} running {n} points'.format(p=par, n=options.npoints)
            tmp_val = ws.var(par).getVal()
            tmp_dn = 0.8*tmp_val if tmp_val else -2.
            tmp_up = 1.2*tmp_val if tmp_val else  2.
            firstpoint = 0
            while firstpoint <= options.npoints-1:
                lastpoint = min(firstpoint+options.ppj-1,options.npoints-1)
                cmd_base  = 'combine {ws} -M MultiDimFit -t -1 --algo grid --points {np} '.format(ws=absinfile,np=options.npoints)
                #cmd_base += ' --cminDefaultMinimizerType GSLMultiMin --cminDefaultMinimizerAlgo BFGS2 '
                # josh's magic options:
                cmd_base += ' --cminDefaultMinimizerType GSLMultiMinMod --cminDefaultMinimizerAlgo BFGS2 '
                cmd_base += ' --setParameterRanges "{p}={dn:.2f},{up:.2f}" '.format(p=par,dn=tmp_dn,up=tmp_up)
                cmd_base += ' -P {par} --floatOtherPOIs=1 '.format(par=par)
                #cmd_base+= ' --setParameterRanges <whatever> '
                cmd_base += ' --keepFailures -n _{name}_point{n}To{nn} '.format(name=par,n=firstpoint,nn=lastpoint)
                cmd_base += ' --firstPoint {n} --lastPoint {nn} '.format(n=firstpoint,nn=lastpoint)
                #cmd_base += ' --redefineSignalPOIs '+','.join( [i for i in all_parameters if 'norm_' in i] )
                if options.verbose:
                    cmd_base += ' -v 10 '

                ## make new file for evert parameter and point
                job_file_name = jobdir+'/job_{p}_point{n:.0f}To{nn:.0f}.sh'.format(p=par,n=firstpoint,nn=lastpoint)
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

                firstpoint = lastpoint+1

    ## end the submission, now move to what to do during postprocessing
    else:
        ROOT.gROOT.SetBatch()
        c1 = ROOT.TCanvas('foo','bar',800,800)
        if not os.path.isdir(options.webdir):
            os.system('mkdir -p {wd} '.format(wd=options.webdir))
            os.system('cp /afs/cern.ch/user/g/gpetrucc/php/index.php '+options.webdir)
        for ip,par in enumerate(parameters):
            ## first hadd all the point files into one scan file named scan_<par>.root
            pardir = absopath+'/'+par+'/'
            print 'at parameter {p} doing some postprocessing'.format(p=par)
            fs = list([f for f in os.listdir(pardir) if 'higgs' in f])
            fs = sorted(fs, key= lambda x: int(x.split('.')[0].split('_')[-1].replace('point','').split('To')[0]))
            fs = list([pardir+f for f in fs])
            
            ofn = '{pd}/scan_{p}.root'.format(pd=pardir,p=par)

            ## run the hadd command only if the file doesn't exist or specified by user
            if not os.path.isfile(ofn) or options.overwrite:
                cmd_hadd = 'hadd -f {ofn} {fs}'.format(ofn=ofn, fs = ' '.join(fs))
                os.system(cmd_hadd)

            ## get the central value to normalize the norm parameters
            tmp_val = ws.var(par).getVal()

            ## make some plots of the likelihood scans
            tmp_graph = getGraph(ofn, par, norm=tmp_val)
            tmp_graph.Draw('ap')
            ## draw a line at 2.*deltaNLL = 1.
            tmp_line = ROOT.TLine(tmp_graph.GetXaxis().GetXmin(), 1., tmp_graph.GetXaxis().GetXmax(), 1.)
            tmp_line.SetLineStyle(7); tmp_line.SetLineWidth(2);
            tmp_line.Draw('same')

            if not options.webdir:
                print 'ERROR: specify a directory to save the plots!'
                sys.exit() ## sys isn't even loaded, so this will most definitely fail
            ## save the plots in the specified webdir
            c1.SaveAs(options.webdir+'/'+os.path.basename(ofn).replace('.root','.pdf'))
            c1.SaveAs(options.webdir+'/'+os.path.basename(ofn).replace('.root','.png'))

