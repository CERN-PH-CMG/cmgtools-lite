#!/usr/bin/env python

import sys, os
import re
from optparse import OptionParser

if __name__ == "__main__":
    usage="%prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--region", dest="region", default='signal', help='Find the yields for this phase space')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    parser.add_option("-s", "--synch", dest="synch", action="store_true", default=False, help='Do not apply any scale factor, bare yields')
    parser.add_option("-p", "--plot", dest="plot", type="string", default="", help='If given, make the plots and put them in the specified directory')
    parser.add_option("-U", "--up-to-cut",      dest="upToCut",   type="string", help="Run selection only up to the cut matched by this regexp, included.") 
    (options, args) = parser.parse_args()
 
    TREEDIR='/data1/emanuele/monox/'
    anaOpts = []

    region = options.region
    if region in ['signal','zmumu','wmunu']: 
        T=TREEDIR+'TREES_MET_80X_V4'
        MCA='vbfdm/mca-80X-muonCR.txt'
    elif region in ['zee','wenu']: 
        T=TREEDIR+'TREES_1LEP_80X_V4'
        MCA='monojet/mca-80X-Ve.txt'
    elif region in ['gjets']: 
        T=TREEDIR+'TREES_1G_80X_V4'
        MCA='monojet/mca-80X-Gj.txt'        


    corey = 'mcAnalysis.py ' if len(options.plot)==0 else 'mcPlots.py '
    coreopt = ' -P '+T+' --s2v -j 6 -l 24.47 -G'
    plotopt = ' -f --poisson --pdir ' + options.plot + ' --showRatio --maxRatioRange 0.5 1.5 '
    anaOpts += [coreopt]

    if options.upToCut: anaOpts.append('-U '+options.upToCut)

    fev = ' -F mjvars/t \"'+T+'/friends/evVarFriend_{cname}.root\" '
    fsf = ' --FMC sf/t \"'+T+'/friends/sfFriend_{cname}.root\" '
    anaOpts += [fev, fsf]
    if options.synch == True: anaOpts += '-u'
    
    runy = ' '.join([corey,MCA,' '])
    cuts = {
        'signal': 'vbfdm/vbfdm.txt',
        'zmumu': 'vbfdm/zmumu.txt',
        'wmunu': 'vbfdm/wmunu.txt',
        'zee': 'vbfdm/zee.txt',
        'wenu': 'vbfdm/wenu.txt',
        'gjets': 'vbfdm/gjets.txt',
        }
    
    plotfile = re.split(".txt",cuts[region])[0]+"_plots.txt"
    if options.plot: 
        anaOpts += [plotfile, plotopt]

    anaOptsString = ' '.join(anaOpts)

    if region not in cuts: raise RuntimeError, "Region "+region+" not in the foreseen ones: "+cuts
    weights = ['puw']
    if region in 'signal': weights += ['SF_NLO_QCD','SF_NLO_EWK','SF_trigmetnomu']
    elif region in ['zmumu','zee']: weights += ['SF_trigmetnomu','SF_LepTightLoose','SF_NLO_QCD','SF_NLO_EWK']

    weightsString = " -W '" + "*".join(weights) + "'"

    command = 'python ' + runy + cuts[region] + anaOptsString + weightsString + ' -X trigger -X metfilters '
    if options.dryrun: print command
    else: os.system(command)
