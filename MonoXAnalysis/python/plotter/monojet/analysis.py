#!/usr/bin/env python

import sys, os
import re
from optparse import OptionParser

if __name__ == "__main__":
    usage="%prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--region", dest="region", default='signal', help='Find the yields for this phase space')
    parser.add_option("-c", "--category", dest="category", default='', help='Add the categorization for monoj or monov')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    (options, args) = parser.parse_args()

    region = options.region
    validregions = ['signal','zmumu','wmunu','zee','wenu','gjets']
    if region not in validregions: 
        print 'ERROR! The region has to be one among ',validregions
        sys.exit(1)

    TREEDIR='/data1/emanuele/monox/'
    if region in ['signal','zmumu','wmunu']: 
        T=TREEDIR+'TREES_METSKIM_80X'
        MCA='monojet/mca-76X-Vm.txt'
    elif region in ['zee','wenu']: 
        T=TREEDIR+'TREES_1LEPSKIM_80X'
        MCA='monojet/mca-76X-Ve.txt'
    elif region in ['gjets']: 
        T=TREEDIR+'TREES_1GSKIM_80X'
        MCA='monojet/mca-76X-Gj.txt'        

    coreopt = '-P '+T+' --s2v -j 6 -l 1.0'
    corey = 'mcAnalysis.py ' + coreopt + ' -G '
    fev = ' -F mjvars/t \"'+T+'/friends/evVarFriend_{cname}.root\" '

    runy = corey + MCA + ' --s2v -u '
    cuts = {
        'signal': 'monojet/monojet_twiki.txt',
        'zmumu': 'monojet/zmumu_twiki.txt',
        'wmunu': 'monojet/wmunu_twiki.txt',
        'zee': 'monojet/zee_twiki.txt',
        'wenu': 'monojet/wenu_twiki.txt',
        'gjets': 'monojet/gjets_twiki.txt',
        }

    # categorization
    monov_cut="-A recoil monoV 'nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4 && abs(FatJetClean1_prunedMass-85)<20 && FatJetClean1_tau2/FatJetClean1_tau1<0.6' "
    monoj_cut="-A recoil monoJ '!(nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4 && abs(FatJetClean1_prunedMass-85)<20 && FatJetClean1_tau2/FatJetClean1_tau1<0.6)' "
    # single cuts for monov
    monov_ak8jetAcc="-A recoil ak8jetAcc 'nFatJetClean>0 && FatJetClean1_pt>250 && abs(FatJetClean1_eta)<2.4' "
    monov_ak8jetT2T1="-A recoil ak8jetT2T1 'FatJetClean1_tau2/FatJetClean1_tau1<0.6' "
    monov_ak8jetMpruned="-A recoil ak8jetMpruned 'abs(FatJetClean1_prunedMass-85)<20' "
    if options.region in ['signal','zmumu','wmunu']: monov_tightMET="-A recoil tightMET 'metNoMu_pt>250' "
    elif options.region == 'zee': monov_tightMET="-A recoil tightMET 'pt_3(met_pt,met_phi,LepGood1_pt,LepGood1_phi,LepGood2_pt,LepGood2_phi)>250' "
    elif options.region == 'wenu': monov_tightMET="-A recoil tightMET 'pt_2(met_pt,met_phi,LepGood1_pt,LepGood1_phi)>250' "
    elif options.region == 'gjets': monov_tightMET="-A recoil tightMET 'pt_2(met_pt,met_phi,GammaGood1_pt,GammaGood1_phi)>250' "
    else: monov_tightMET = ' '

    print "==> Yields for category: ",options.category
    if options.category != '': cat_cut = monov_ak8jetAcc+monov_ak8jetT2T1+monov_ak8jetMpruned+monov_tightMET if options.category=='monov' else monoj_cut
    else: cat_cut = ''

    if options.region not in cuts: raise RuntimeError, "Region "+options.region+" not in the foreseen ones: "+cuts

    command = 'python ' + runy + cuts[options.region] + fev + ' --sp TTbarDM -X trigger -X metfilters ' + cat_cut
    if options.dryrun: print command
    else: os.system(command)
