#!/usr/bin/env python

import sys, os
import re
import fileinput
from optparse import OptionParser

class Analysis:
    def __init__(self,options,mcPlotsOptions=None):
    
        self.options = options
 
        TREEDIR='/data1/emanuele/monox/'
        anaOpts = []
        
        region = options.region
        if region in ['signal']: 
            T=TREEDIR+'TREES_MET_80X_V4'
            self.MCA='vbfdm/mca-80X-sync.txt'
        elif region in ['zmumu','wmunu']: 
            T=TREEDIR+'TREES_MET_80X_V4'
            self.MCA='vbfdm/mca-80X-muonCR.txt'
        elif region in ['zee','wenu']: 
            T=TREEDIR+'TREES_1LEP_80X_V4'
            self.MCA='vbfdm/mca-80X-electronCR.txt'
        elif region in ['gjets']: 
            T=TREEDIR+'TREES_1G_80X_V4'
            self.MCA='monojet/mca-80X-Gj.txt'        
     
        corey = 'mcAnalysis.py ' if len(options.pdir)==0 else 'mcPlots.py '
        coreopt = ' -P '+T+' --s2v -j 6 -l 24.47 -G'
        plotopt = ' -f --poisson --pdir ' + options.pdir
        if region != 'signal': plotopt += ' --showRatio --maxRatioRange 0.5 1.5 --fixRatioRange '
        anaOpts += [coreopt]
     
        if options.upToCut: anaOpts.append('-U '+options.upToCut)
     
        fev = ' -F mjvars/t \"'+T+'/friends/evVarFriend_{cname}.root\" '
        fsf = ' --FMC sf/t \"'+T+'/friends/sfFriend_{cname}.root\" '
        anaOpts += [fev, fsf]
        if options.synch == True: anaOpts += '-u'
        
        runy = ' '.join([corey,self.MCA,' '])
        cuts = {
            'signal': 'vbfdm/vbfdm.txt',
            'zmumu': 'vbfdm/zmumu.txt',
            'wmunu': 'vbfdm/wmunu.txt',
            'zee': 'vbfdm/zee.txt',
            'wenu': 'vbfdm/wenu.txt',
            'gjets': 'vbfdm/gjets.txt',
            }
        
        common_plotfile = "vbfdm/common_plots.txt"
        plotfile = re.split(".txt",cuts[region])[0]+"_plots.txt"
        with open('vbfdm/plots.txt','w') as fout:
            fin = fileinput.input([common_plotfile,plotfile])
            for line in fin:
                fout.write(line)
            fin.close()

        if options.pdir: 
            anaOpts += ['vbfdm/plots.txt', plotopt]
            if mcPlotsOptions!=None: anaOpts += mcPlotsOptions

        anaOptsString = ' '.join(anaOpts)
     
        if region not in cuts: raise RuntimeError, "Region "+region+" not in the foreseen ones: "+cuts
        weights = {
            'signal': ['puw','SF_trigmetnomu','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'zmumu' : ['puw','SF_trigmetnomu','SF_LepTightLoose','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'zee'   : ['puw','SF_LepTightLoose','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'wmunu' : ['puw','SF_trigmetnomu','SF_LepTight','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'wenu'  : ['puw','SF_LepTight','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'gjets' : ['puw','SF_BTag','SF_NLO_QCD','SF_NLO_EWK']
            }

        weightsString = " -W '" + "*".join(weights[region]) + "'"
     
        self.command = 'python ' + runy + cuts[region] + anaOptsString + weightsString + ' -X trigger -X metfilters '

    def runOne(self):
        if self.options.dryrun: print self.command
        else: os.system(self.command)


if __name__ == "__main__":
    usage="%prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--region", dest="region", default='signal', help='Find the yields for this phase space')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    parser.add_option("-s", "--synch", dest="synch", action="store_true", default=False, help='Do not apply any scale factor, bare yields')
    parser.add_option("-p", "--pdir", dest="pdir", type="string", default="", help='If given, make the plots and put them in the specified directory')
    parser.add_option("-U", "--up-to-cut",      dest="upToCut",   type="string", help="Run selection only up to the cut matched by this regexp, included.") 
    parser.add_option("--fullControlRegions", dest="fullControlRegions", action="store_true", default=False, help='Do not run only one mcAnalysis/mCPlots, do all the control regions')
    (options, args) = parser.parse_args()

    if options.fullControlRegions:

        sel_steps = {'v_presel':'btagveto', 'vbfjets':'vbfjets', 'full_sel':'deta2j'}
        exclude_plots = {'v_presel': ['jcentral_eta','jfwd_eta','detajj','detajj_fullsel','mjj','mjj_fullsel'],
                         'vbfjets': ['detajj_fullsel','mjj_fullsel','nvtx','rho'],
                         'full_sel': ['detajj','mjj','nvtx','rho']
                         }
        rebinFactor = {'v_presel':1, 'vbfjets':1, 'full_sel':4}
        
        #ctrl_regions = ['zmumu','wmunu']
        ctrl_regions = ['wenu'] 

        pdirbase = options.pdir
        for CR in ctrl_regions:
            options.region = CR
            options.upToCut = ''
            for s,v in sel_steps.iteritems():
                print "===> Making selection / plots for control region ",options.region," at selection step: ",s, "(cut =",v,")"
                options.upToCut = v
                options.pdir = pdirbase+"/"+CR+"CR/"+s
                mcpOpts = ['--xP '+','.join(exclude_plots[s]), '--rebin '+str(rebinFactor[s])]
                if CR!='wenu': mcpOpts += ['--xp QCD'] # too large uncertainty
                analysis = Analysis(options,mcpOpts)
                analysis.runOne()


    else: 
        mcpOpts = []
        if(options.region=='signal'): mcpOpts += ['--showIndivSigShapes','--xp data','--rebin 2']
        analysis = Analysis(options,mcpOpts)
        analysis.runOne()
        
