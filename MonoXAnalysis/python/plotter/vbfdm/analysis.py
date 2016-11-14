#!/usr/bin/env python

import sys, os
import re
import fileinput
import ROOT as rt
from optparse import OptionParser
from CMGTools.MonoXAnalysis.plotter.monojet.prepareRFactors import RFactorMaker

class Analysis:
    def __init__(self,options,mcPlotsOptions=None):
    
        self.options = options
 
        TREEDIR='/data1/emanuele/monox/'
        anaOpts = []
        
        region = options.region
        self.region = region
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

        self.anaOpts = anaOpts

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

        self.cuts = cuts[region] 
        self.extraopt = ' -X trigger '
        self.command = 'python ' + runy + cuts[region] + anaOptsString + weightsString + self.extraopt

    def runOne(self):
        if self.options.dryrun: print self.command
        else: os.system(self.command)

    def runOneSyst(self,var,process,outputdir):

        coresyst = 'mcSystematics.py '
        runsyst = ' '.join([coresyst,self.MCA,' '])

        anaOpts = self.anaOpts
        anaOpts += ['-f','-p '+process,'-o '+outputdir,'--sP '+var]
        anaOptsString = ' '.join(anaOpts)

        systs = {
            'signal' : 'vbfdm/syst_SR.txt', # to be replaced
            'zmumu' : 'vbfdm/syst_ZM.txt',
            'zee' : 'vbfdm/syst_ZE.txt',
            'wmunu' : 'vbfdm/syst_WM.txt',
            'wenu' : 'vbfdm/syst_WE.txt'
            }

        anaOptsString = ' '.join(anaOpts)
        command = 'python ' + runsyst + self.cuts + anaOptsString + ' ' + systs[self.region] + self.extraopt 

        if self.options.dryrun: print command
        else: os.system(command)
        

if __name__ == "__main__":
    usage="%prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--region", dest="region", default='signal', help='Find the yields for this phase space')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    parser.add_option("-s", "--synch", dest="synch", action="store_true", default=False, help='Do not apply any scale factor, bare yields')
    parser.add_option("-p", "--pdir", dest="pdir", type="string", default="", help='If given, make the plots and put them in the specified directory')
    parser.add_option("-U", "--up-to-cut",      dest="upToCut",   type="string", help="Run selection only up to the cut matched by this regexp, included.") 
    parser.add_option("--fullControlRegions", dest="fullControlRegions", action="store_true", default=False, help='Do not run only one mcAnalysis/mCPlots, do all the control regions')
    parser.add_option("--propSystToVar", dest="propSystToVar", type="string", default="", help='Make the templates for a given variable, nominal and systematic alternatives')
    parser.add_option("--tF","--transferFactor", dest="transferFactor",  type="string", default="", help='Make the transfer factors from control regions to signal region. Take the templates for the specified variable.')
    (options, args) = parser.parse_args()

    sel_steps = {'v_presel':'btagveto', 'vbfjets':'vbfjets', 'full_sel':'deta2j'}
    exclude_plots = {'v_presel': ['jcentral_eta','jfwd_eta','detajj','detajj_fullsel','mjj','mjj_fullsel'],
                     'vbfjets': ['mjj_fullsel','nvtx','rho'],
                     'full_sel': ['detajj','mjj','nvtx','rho']
                     }
    rebinFactor = {'v_presel':1, 'vbfjets':1, 'full_sel':4}
    ctrl_regions = ['zmumu','wmunu','zee','wenu']

    if options.fullControlRegions:
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

    # eg.:  vbfdm/analysis.py --propSystToVar detajj_fullsel
    elif len(options.propSystToVar)>0:
        pdirbase = options.pdir if options.pdir else "templates"
        if not os.path.exists(pdirbase): os.mkdir(pdirbase)
        processesToProp = {
            'signal': ['ZNuNu','W'],
            'zmumu' : ['ZLL','EWKZLL'],
            'zee' : ['ZLL','EWKZLL'],
            'wmunu' : ['W','EWKW'],
            'wenu' : ['W','EWKW']
            }
        sel_step = sel_steps['vbfjets']
        all_regions = ['signal'] + ctrl_regions
        for reg in all_regions:
            options.region = reg
            options.upToCut = sel_step
            options.pdir = pdirbase
            mcpOpts = ['--rebin '+str(rebinFactor[sel_step])]
            procs = ','.join(processesToProp[reg])
            print "# propagating systematics to processes ",procs, " in the region ",reg
            analysis = Analysis(options,mcpOpts)
            myout = pdirbase+"/templates_"+options.propSystToVar+'_'+reg+'.root'
            analysis.runOneSyst(options.propSystToVar,procs,myout)


    # eg:  vbfdm/analysis.py --tF detajj_fullsel -p templates
    elif len(options.transferFactor)>0:

        # list of transfer factors to do, with files with input templates
        TFs = {
            #    key                num    den    numfile  denfile
            'Znunu_from_Zmumu' : ['ZNuNu','ZLL','signal','zmumu'],
            'Znunu_from_Zee'   : ['ZNuNu','ZLL','signal','zee'],
            'W_from_Wmumu' : ['W','W','signal','wmunu'],
            'W_from_Wenu' : ['W','W','signal','wenu'],
            'Z_from_Wlnu' : ['ZNuNu','W','signal','signal']
            }

        for k,tf in TFs.iteritems():
            num_proc=tf[0]; den_proc=tf[1]
            file_prefix = options.pdir if options.pdir else 'templates'
            file_prefix += ('/templates_'+options.transferFactor+'_')
            num_file=file_prefix+tf[2]+'.root'; den_file=file_prefix+tf[3]+'.root'
            num_sel='SR'; den_sel='CR' if k!='Z_from_Wlnu' else 'SR'

            print "# computing transfer factor: ",k, " reading ", num_sel, " histos from ",num_file," and ",den_sel, " histos from ",den_file
    
            systsUpL   = ['lepID_up']
            systsDownL = ['lepID_down']
         
            systsUpG   = ['QCD_renScaleUp', 'QCD_facScaleUp', 'QCD_pdfUp', 'EWK_up']
            systsDownG = ['QCD_renScaleDown', 'QCD_facScaleDown', 'QCD_pdfDown', 'EWK_down']
         
            titles = {'ZLL':'R_{Z(#mu#mu)}',
                      'W':'R_{W(#mu#mu)}'}
         
            systs={}
         
            if den_proc=='ZLL' or den_proc=='W':
                systs[(den_proc,'CR','up')]=systsUpL
                systs[(den_proc,'CR','down')]=systsDownL
            elif den_proc=='GJetsHT':
                systs[(den_proc,'CR','up')]=systsUpG
                systs[(den_proc,'CR','down')]=systsDownG
            else:
                print "ERROR! Numerator processes can be only ZLL or W or GJetsHT"
                exit()
         
            if num_proc=='ZNuNu':
                systs[(num_proc,'SR','up')]=[]
                systs[(num_proc,'SR','down')]=[]
                if den_proc=='ZLL': title = 'R_{Z}'
                elif den_proc=='W': title = 'R_{Z/W}'
                elif den_proc=='GJetsHT': title = 'R_{#gamma}'
                else: exit()
            elif num_proc=='W':
                systs[(num_proc,'SR','up')]=[]
                systs[(num_proc,'SR','down')]=[]
                if den_proc=='W': title = 'R_{W}'
                else:
                    print "Num is ",num_proc," so only W is allowed as denominator"
                    exit()
            else:
                print "ERROR! Numerator processes can be only ZNuNu or W"
                exit()
         
         
            outname = options.pdir+"/rfactors_"+num_proc+num_sel+"_Over_"+tf[3]+den_sel+".root"
            outfile = rt.TFile(outname,"RECREATE")
         
            rfm = RFactorMaker(options.transferFactor,num_file,den_file,num_proc,den_proc,systs)
            hists = rfm.computeFullError(outfile)
            rfac_full = rfm.computeRFactors(hists,outfile,"full")
            hists_statonly = {}
            hists_statonly[(num_proc,'SR')] = rfm.hists_nominal[(num_proc,'SR','nominal')]
            hists_statonly[(den_proc,'CR')] = rfm.hists_nominal[(den_proc,'CR','nominal')]
            rfac_statonly = rfm.computeRFactors(hists_statonly,outfile,"stat")
            name = outname.replace(".root","")
            lumi = 24.47
            rfm.makePlot(rfac_statonly,rfac_full,name,lumi,title,[])
         
            outfile.Close()

    else: 
        mcpOpts = []
        if(options.region=='signal'): mcpOpts += ['--showIndivSigShapes','--xp data,QCD','--rebin 2']
        analysis = Analysis(options,mcpOpts)
        analysis.runOne()
