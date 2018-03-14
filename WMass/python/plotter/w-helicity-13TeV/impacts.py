# usage: python impacts.py ../cards/helicity_2018_03_09_testpdfsymm/Wel_plus_ws.root --channel el --fix-YBins "plusR=10,11,12;plusL=11,12" [--dry-run]

import ROOT, random, array, os

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog workspace [options] ')
    parser.add_option('-c','--channel', dest='channel', default='el', type='string', help='name of the channel')
    parser.add_option(     '--fix-YBins', dest='fixYBins', type='string', default='', help='add here replacement of default rate-fixing. with format plusR=10,11,12;plusL=11,12;minusR=10,11,12;minusL=10,11 ')
    parser.add_option(     '--dry-run', dest='dryRun',   action='store_true', default=False, help='Do not run the job, only print the command');
    (options, args) = parser.parse_args()

    workspace = args[0]; wsbase = os.path.basename(workspace).split('.')[0]; inputdir = os.path.dirname(os.path.abspath(workspace))
    charge = 'plus' if 'plus' in wsbase else 'minus'

    ybinfile = open(os.path.join(inputdir, 'binningYW.txt'),'r')
    ybinline = ybinfile.readlines()[0]
    ybins = list(float(i) for i in ybinline.split())
    ybinfile.close()
    nYBins = len(ybins)-1

    fixedYBins = {'plusR' : [nYBins-1,nYBins-2,nYBins-3],
                  'plusL' : [nYBins-1],
                  'minusR': [nYBins-1,nYBins-2,nYBins-3],
                  'minusL': [nYBins-1],
                  }

    if options.fixYBins:
        splitted = options.fixYBins.split(';')
        for comp in splitted:
            chhel = comp.split('=')[0]
            bins  = comp.split('=')[1]
            fixedYBins[chhel] = list(int(i) for i in bins.split(','))
    print fixedYBins

    POIs = []
    hels = ['left','right']
    for h in hels:
        for b in xrange(nYBins):
            chhel = "{ch}{shorthel}".format(ch=charge,shorthel='L' if 'left' in h else 'R')
            if b in fixedYBins[chhel]: continue
            POIs.append( 'norm_W{ch}_{hel}_W{ch}_{channel}_Ybin_{bin}'.format(ch=charge,hel=h,channel=options.channel,bin=b) )

    print "Running impacts on the following POIs: ",POIs

    cmdBase = "combineTool.py -d {ws} -M Impacts -t -1 --expectSignal=1 -m 999 -n {name} {whichfit} --robustFit=1 --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1 --redefineSignalPOIs {poi} {floatOthers} --freezeNuisanceGroups efficiencies,fixedY -v 9 --job-mode lxbatch --task-name {taskname} --sub-opts='-q 8nh' %s" % ('--dry-run' if options.dryRun else '')

    for poi in POIs:
        # first run the initial fit
        cmdInitialFit = cmdBase.format(ws=workspace,whichfit='--doInitialFit',poi=poi,name=poi,taskname='InitialFit_%s'%poi,floatOthers='--floatOtherPOIs=0')
        # print cmdInitialFit
        os.system(cmdInitialFit)
        # then run the likelihood scan for each nuisance parameter (a large number of jobs if you have many nuisances!)g
        cmdScan = cmdBase.format(ws=workspace,whichfit='--doFits',poi=poi,name=poi,taskname='Scan_%s'%poi,floatOthers='')
        # print cmdScan
        os.system(cmdScan)
