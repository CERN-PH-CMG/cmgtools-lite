#!/usr/bin/env python

import sys, os
import re
from optparse import OptionParser

if __name__ == "__main__":
    usage="%prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--region", dest="region", default='signal', help='Find the yields for this phase space')
    parser.add_option("-c", "--category", dest="category", default=None, help='Add the categorization for monoj or monov')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    (options, args) = parser.parse_args()

    #T='/afs/cern.ch/work/e/emanuele/TREES/SYNCH_80X/'
    T='/afs/cern.ch/work/e/emanuele/monox/heppy/CMSSW_8_0_5/src/CMGTools/MonoXAnalysis/cfg/SynchTrees/'

    coreopt = '-P '+T+' --s2v -j 6 -l 1.0'
    corey = 'mcAnalysis.py ' + coreopt + ' -G '
    fev = ' -F mjvars/t \"'+T+'/friends/evVarFriend_{cname}.root\" '

    runy = corey + 'monojet/mca-80X-sync.txt --s2v -u '
    cuts = {
        'signal': 'monojet/monojet_synch.txt',
        'zmumu': 'monojet/zmumu_twiki.txt',
        'wmunu': 'monojet/wmunu_twiki.txt',
        'zee': 'monojet/zee_twiki.txt',
        'wenu': 'monojet/wenu_twiki.txt',
        'gjets': 'monojet/gjets_twiki.txt',
        }

    # categorization
    monov_cut="-A dphijm monoV 'nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4 && abs(FatJetClean1_prunedMass-85)<20 && FatJetClean1_tau2/FatJetClean1_tau1<0.6"
    monoj_cut="-A dphijm monoJ '!(nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4 && abs(FatJetClean1_prunedMass-85)<20 && FatJetClean1_tau2/FatJetClean1_tau1<0.6)"
    if options.category != None: cat_cut = monoj_cut if options.category=='monoj' else 'monov'
    else: cat_cut = ''

    if options.region not in cuts: raise RuntimeError, "Region "+options.region+" not in the foreseen ones: "+cuts

    command = 'python ' + runy + cuts[options.region] + fev + ' --sp TTbarDM -X trigger -X metfilters ' + cat_cut
    if options.dryrun: print command
    else: os.system(command)
