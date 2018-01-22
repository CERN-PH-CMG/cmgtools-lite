#!/usr/bin/env python
import sys, os
import os.path as osp

def getEOSlslist(directory, mask='', prepend='root://eoscms//eos/cms'):
    '''Takes a directory on eos (starting from /store/...) and returns
    a list of all files with root://eoscms//eos/cms/ prepended'''
    from subprocess import Popen, PIPE
    print 'looking into:',directory,'...'

    eos_cmd = 'eos'
    if not osp.exists(eos_cmd):
        raise RuntimeError('check eos alias: %s'%eos_cmd)
    data = Popen([eos_cmd, 'ls', '/eos/cms/'+directory],
                stdout=PIPE)
    out,err = data.communicate()

    full_list = []

    ## if input file was single root file:
    if directory.endswith('.root'):
        if len(out.split('\n')[0]) > 0:
            return [prepend + directory]

    for line in out.split('\n'):
        if len(line.split()) == 0: continue
        ## instead of only the file name append the string
        ## to open the file in ROOT
        full_list.append('/'.join([prepend,directory,line]))

    ## strip the list of files
    if mask != '':
        stripped_list = [x for x in full_list if mask in x]
        return stripped_list
    ## if no mask given, run over all files
    else:
        return full_list

def cacheLocally(infile, tmpDir='/tmp/'):
    tmpfile = osp.join(tmpDir, osp.basename(infile))

    # Copy locally if it's not there already
    if not osp.exists(tmpfile):
        xrcmd = "xrdcp %s %s" % (infile, tmpfile)
        print " transferring to %s" % tmpDir
        os.system(xrcmd)
        print "... copied successfully"

    infile = tmpfile
    return infile

def run((infile, outfile, options)):
    if infile.startswith("root://"):
        infile = cacheLocally(infile, os.environ.get('TMPDIR', '/tmp'))

    from ROOT import TFile
    fb = TFile.Open(infile)
    tree = fb.Get("tree")

    try: tree.GetName()
    except ReferenceError:
        print "Error: tree not found in %s" % infile
        return False
    print "... processing %s" %infile


    from ROOT import gSystem, TChain

    ## Load the previously compiled shared object library into ROOT
    libfile = "lepTnPFriendTreeMaker_cc.so"
    print '... loading shared object library from %s'%libfile
    gSystem.Load(libfile)
    ## Load it into PyROOT (this is where the magic happens)
    from ROOT import lepTnPFriendTreeMaker

    ana = lepTnPFriendTreeMaker(tree)
    if options.maxEntries > 0:
        ana.setMaxEvents(options.maxEntries)

    ## Check if it's data or MC
    isdata = '2016' in osp.basename(infile)

    ## Run the loop
    ana.RunJob(outfile, isdata)

    return True

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """%prog [options] inputDir

    Notes:
    - Compile lepTnPFriendTreeMaker.cc first with ACLiC like so:
       > root -l -b -q -n lepTnPFriendTreeMaker.cc+
      This will produce lepTnPFriendTreeMaker_cc.so
    - Errors of <TTree::SetBranchAddress>: unknown branch occur
      for the MC-only branches when running on data.
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--maxEntries", dest="maxEntries", type="int",
                      default=-1, help="Max entries to process");
    parser.add_option("-j", "--jobs", dest="jobs", type="int",
                      default=0,
                      help="Use N threads");
    parser.add_option("-o", "--outDir", default="tnptrees",
                      action="store", type="string", dest="outDir",
                      help=("Output directory for tnp trees "
                            "[default: %default/]"))
    parser.add_option("-q", "--queue", default="",
                      action="store", type="string", dest="queue",
                      help=("Run on lxbatch in this queue "
                            "[default: run locally]"))
    parser.add_option("-f", "--filter",
                      default='2016,-DCSonly,-MuonEG,-Single,DYJetsToLL_M50',
                      type="string", dest="filter",
                      help=("Comma separated list of filters to apply. "
                            "Use '-' at beginning to veto files. "
                            "[default: %default/]"))
    (options, args) = parser.parse_args()

    # Collect all input:
    idir = args[0]
    if osp.exists(idir):
        if osp.isdir(idir):
            inputfiles = [osp.join(idir,f) for f in os.listdir(idir)
                                     if osp.splitext(f)[1] == '.root']
        elif osp.isfile(idir) and idir.endswith('.root'):
            inputfiles = [idir]
    elif idir.startswith('/store/') or idir.startswith('root://'):
        if idir.endswith('.root'):
            inputfiles = [idir]
        else:
            inputfiles = getEOSlslist(idir)
    else:
        parser.print_help()
        sys.exit(-1)

    # Apply filter (if more than one file)
    if len(inputfiles) > 1 and len(options.filter.split(','))>0:
        filters = options.filter.split(',')
        print "Will filter for", filters
        posfilters = [f     for f in filters if not f.startswith('-')]
        negfilters = [f[1:] for f in filters if     f.startswith('-')]

        inputfiles = [i for i in inputfiles if
                                    any([(f in i) for f in posfilters])]

        inputfiles = [i for i in inputfiles if not
                                    any([(f in i) for f in negfilters])]

    print "Will process the following files:"
    for ifile in inputfiles: print ifile

    os.system('mkdir -p %s'%options.outDir)

    # Assemble tasks
    tasks = []
    for ifile in inputfiles:
        oname = '%s.root' % osp.splitext(osp.split(ifile)[1])[0]
        ofile = osp.join(options.outDir, oname)
        tasks.append((ifile,ofile,options))

    if options.queue:
        runner = osp.join(os.environ['CMSSW_BASE'],
                              'src/CMGTools/TTHAnalysis/macros/lxbatch_runner.sh')

        basecmd = "{runner} {dir} {cmssw} {self} ".format(
                    dir=os.getcwd(),
                    runner=runner,
                    cmssw=os.environ['CMSSW_BASE'],
                    self=osp.abspath(__file__))

        for (ifile,ofile,opt) in tasks:
            cmd = 'bsub -q {queue} {basecmd} {ifile} -o {odir}'.format(
                              queue=options.queue,
                              basecmd=basecmd,
                              ifile=ifile,
                              odir=osp.abspath(options.outDir))
            os.system(cmd)
        print "Submitted %d jobs to queue <%s>" % (len(tasks), options.queue)


    elif options.jobs > 0 and len(tasks) > 1:
        print "Running in parallel using %d jobs" % options.jobs
        from multiprocessing import Pool
        pool = Pool(options.jobs)
        pool.map(run, tasks)

    else:
        print "Running sequentially"
        map(run, tasks)

