# usage: step 1. INITIAL FITS: python impacts.py Wel_plus_ws.root initial --channel el [--params 'CMS_lumi_13TeV']
# usage: step 2 (when 1 is done). SCANS: python impacts.py Wel_plus_ws.root scan --channel el [--params 'CMS_lumi_13TeV']

import ROOT, random, array, os

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog workspace what [options] ')
    parser.add_option('-c','--channel', dest='channel', default='el', type='string', help='name of the channel')
    parser.add_option('-p','--params', dest='params', default='', type='string', help='parameters for which you want to show the impacts. comma separated list of. If not given, POIs are the normalizations')
    parser.add_option(     '--dry-run', dest='dryRun',   action='store_true', default=False, help='Do not run the job, only print the command');
    (options, args) = parser.parse_args()

    if(len(args)<2):
        raise RuntimeError, "Arguments should be workspace.root what (what=initial or scan)"
    if args[1] not in ['initial','scan']:
        raise RuntimeError, "what should be initial for intial fits or scan (need the initial fits to be done)"

    workspace = args[0]; wsbase = os.path.basename(workspace).split('.')[0]; inputdir = os.path.dirname(os.path.abspath(workspace))
    charge = 'plus' if 'plus' in wsbase else 'minus'
    what = args[1]

    ## look for the maximum ybin bin number in each charge/helicity state
    binningFile = open(os.path.join(inputdir, 'binningYW.txt'),'r')
    binningYW = eval(binningFile.read())
    nbins = {}
    for i,j in binningYW.items():
        nbins[i] = len(j)-1

    POIs = []
    if not options.params:
        hels = ['left','right']
        for h in hels:
            for b in xrange(nbins['{charge}_{pol}'.format(charge=charge,pol=h)]):
                chhel = "{ch}{shorthel}".format(ch=charge,shorthel='L' if 'left' in h else 'R')
                POIs.append( 'norm_W{ch}_{hel}_W{ch}_{channel}_Ybin_{bin}'.format(ch=charge,hel=h,channel=options.channel,bin=b) )
    else:
        POIs += [p for p in options.params.split(',')]
    print "Running impacts on the following POIs: ",POIs

    cmdBase = "combineTool.py -d {ws} -M Impacts -t -1 --expectSignal=1 -m 999 -n {name} {whichfit} --robustFit=1 --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1 --redefineSignalPOIs {poi} {floatOthers} --freezeNuisanceGroups efficiencies -v 9 --job-mode lxbatch --task-name {taskname} --sub-opts='-q 8nh' %s" % ('--dry-run' if options.dryRun else '')

    for poi in POIs:
        # first run the initial fit
        cmdInitialFit = cmdBase.format(ws=workspace,whichfit='--doInitialFit',poi=poi,name=poi,taskname='InitialFit_%s'%poi,floatOthers='--floatOtherPOIs=0')
        # then run the likelihood scan for each nuisance parameter (a large number of jobs if you have many nuisances!)
        cmdScan = cmdBase.format(ws=workspace,whichfit='--doFits',poi=poi,name=poi,taskname='Scan_%s'%poi,floatOthers='')
        if what=='initial': os.system(cmdInitialFit)
        elif what=='scan':  os.system(cmdScan)
