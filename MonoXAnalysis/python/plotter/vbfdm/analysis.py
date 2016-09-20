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
    (options, args) = parser.parse_args()

    T='/data1/emanuele/monox/TREES_MET_80X_V4/'
    anaOpts = []

    corey = 'mcAnalysis.py '
    coreopt = ' -P '+T+' --s2v -j 6 -l 2.3 -G'
    anaOpts += [coreopt]

    fev = ' -F mjvars/t \"'+T+'/friends/evVarFriend_{cname}.root\" '
    fsf = ' --FM sf/t \"'+T+'/friends/sfFriend_{cname}.root\" '
    anaOpts += [fev, fsf]
    if options.synch == True: anaOpts += '-u'
    
    anaOptsString = ' '.join(anaOpts)

    runy = corey + 'vbfdm/mca-80X-sync.txt --s2v '
    cuts = {
        'signal': 'vbfdm/vbfdm.txt',
        'zmumu': 'vbfdm/zmumu.txt',
        'wmunu': 'vbfdm/wmunu.txt',
        'zee': 'vbfdm/zee.txt',
        'wenu': 'vbfdm/wenu.txt',
        'gjets': 'vbfdm/gjets.txt',
        }

    if options.region not in cuts: raise RuntimeError, "Region "+options.region+" not in the foreseen ones: "+cuts
    weights = ['puw']
    if options.region in 'signal': weights += ['SF_NLO_QCD','SF_NLO_EWK']
    
    weightsString = " -W '" + "*".join(weights) + "'"

    command = 'python ' + runy + cuts[options.region] + anaOptsString + weightsString + ' --sp vbfH125 -X trigger -X metfilters '
    if options.dryrun: print command
    else: os.system(command)
