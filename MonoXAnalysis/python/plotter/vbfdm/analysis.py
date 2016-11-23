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
        if "HOSTNAME" in os.environ:  
            if os.environ["HOSTNAME"] == "pccmsrm29.cern.ch":
                TREEDIR='/u2/emanuele/'

        anaOpts = []
        
        region = options.region
        self.region = region
        if region in ['SR']: 
            T=TREEDIR+'TREES_MET_80X_V4'
            self.MCA='vbfdm/mca-80X-sync.txt'
        elif region in ['ZM','WM']: 
            T=TREEDIR+'TREES_MET_80X_V4'
            self.MCA='vbfdm/mca-80X-muonCR.txt'
        elif region in ['ZE','WE']: 
            T=TREEDIR+'TREES_1LEP_80X_V4'
            self.MCA='vbfdm/mca-80X-electronCR.txt'
        elif region in ['gjets']: 
            T=TREEDIR+'TREES_1G_80X_V4'
            self.MCA='monojet/mca-80X-Gj.txt'        
     
        corey = 'mcAnalysis.py ' if len(options.pdir)==0 else 'mcPlots.py '
        coreopt = ' -P '+T+' --s2v -j 6 -l 24.47 -G'
        plotopt = ' -f --poisson --pdir ' + options.pdir
        if region != 'SR': plotopt += ' --showRatio --maxRatioRange 0.5 1.5 --fixRatioRange '
        anaOpts += [coreopt]
     
        if options.upToCut: anaOpts.append('-U '+options.upToCut)
     
        fdir = {
            'SR': 'friends_SR',
            'ZM': 'friends_VM',
            'WM': 'friends_VM',
            'ZE': 'friends_VE',
            'WE': 'friends_VE',
            }
        fev = ' -F mjvars/t \"'+T+'/'+fdir[region]+'/evVarFriend_{cname}.root\" '
        fsf = ' --FMC sf/t \"'+T+'/friends/sfFriend_{cname}.root\" '
        anaOpts += [fev, fsf]
        if options.synch == True: anaOpts += ['-u']
        
        runy = ' '.join([corey,self.MCA,' '])
        cuts = {
            'SR': 'vbfdm/vbfdm.txt',
            'ZM': 'vbfdm/zmumu.txt',
            'WM': 'vbfdm/wmunu.txt',
            'ZE': 'vbfdm/zee.txt',
            'WE': 'vbfdm/wenu.txt',
            'gjets': 'vbfdm/gjets.txt',
            }
        
        common_plotfile = "vbfdm/common_plots_2D.txt" if options.twodim else "vbfdm/common_plots.txt"
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
            'SR': ['puw','SF_trigmetnomu','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'ZM' : ['puw','SF_trigmetnomu','SF_LepTightLoose','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'ZE'   : ['puw','SF_LepTightLoose','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'WM' : ['puw','SF_trigmetnomu','SF_LepTight','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
            'WE'  : ['puw','SF_LepTight','SF_BTag','SF_NLO_QCD','SF_NLO_EWK'],
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
            'SR' : 'vbfdm/syst_SR.txt', # to be replaced
            'ZM' : 'vbfdm/syst_ZM.txt',
            'ZE' : 'vbfdm/syst_ZE.txt',
            'WM' : 'vbfdm/syst_WM.txt',
            'WE' : 'vbfdm/syst_WE.txt'
            }

        anaOptsString = ' '.join(anaOpts)
        command = 'python ' + runsyst + self.cuts + anaOptsString + ' ' + systs[self.region] + self.extraopt 

        if self.options.dryrun: print command
        else: os.system(command)
        

if __name__ == "__main__":
    usage="%prog [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-r", "--region", dest="region", default='SR', help='Find the yields for this phase space')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    parser.add_option("-s", "--synch", dest="synch", action="store_true", default=False, help='Do not apply any scale factor, bare yields')
    parser.add_option("-p", "--pdir", dest="pdir", type="string", default="", help='If given, make the plots and put them in the specified directory')
    parser.add_option("--select-plot", "--sP", dest="plotselect", action="append", default=[], help="Select only these plots out of the full file")
    parser.add_option("-U", "--up-to-cut",      dest="upToCut",   type="string", help="Run selection only up to the cut matched by this regexp, included.")
    parser.add_option("--twodim", dest="twodim", action="store_true", help="run the two-dimensional analysis")
    parser.add_option("--fullControlRegions", dest="fullControlRegions", action="store_true", default=False, help='Do not run only one mcAnalysis/mCPlots, do all the control regions')
    parser.add_option("--propSystToVar", dest="propSystToVar", type="string", default="", help='Make the templates for a given variable, nominal and systematic alternatives')
    parser.add_option("--tF","--transferFactor", dest="transferFactor",  type="string", default="", help='Make the transfer factors from control regions to signal region. Take the templates for the specified variable.')
    (options, args) = parser.parse_args()

    #sel_steps = {'v_presel':'btagveto', 'vbfjets':'vbfjets', 'full_sel':'dphihmT'}
    #sel_steps = {'vbfjets':'vbfjets', 'full_sel':'dphihmT'}
    sel_steps = {'vbfjets':'vbfjets'}
    exclude_plots = {'v_presel': ['jcentral_eta','jfwd_eta','detajj','detajj_fullsel','mjj','mjj_fullsel'],
                     'vbfjets': ['jcentral_eta','jfwd_eta'],
                     'full_sel': ['detajj','mjj','nvtx','rho']
                     }
    rebinFactor = {'v_presel':1, 'vbfjets':1, 'full_sel':1}
    ctrl_regions = ['ZM','WM','ZE','WE','SR']

    if options.fullControlRegions:
        pdirbase = options.pdir
        for CR in ctrl_regions:
            options.region = CR
            options.upToCut = ''
            for s,v in sel_steps.iteritems():
                print "#===> Making selection / plots for control region ",options.region," at selection step: ",s, "(cut =",v,")"
                options.upToCut = v
                options.pdir = pdirbase+"/"+CR+("/" if CR=='SR' else "CR/")+s
                mcpOpts = ['--xP '+','.join(exclude_plots[s]), '--rebin '+str(rebinFactor[s])]
                if len(options.plotselect)>0: mcpOpts += ['--sP '+','.join(options.plotselect)]
                if CR!='WE': mcpOpts += ['--xp QCD'] # too large uncertainty
                if CR=='SR': mcpOpts += ['--showIndivSigShapes','--xp data,QCD','--rebin 2'] # blind data
                analysis = Analysis(options,mcpOpts)
                analysis.runOne()        

    # eg.:  vbfdm/analysis.py --propSystToVar detajj_fullsel
    elif len(options.propSystToVar)>0:
        pdirbase = options.pdir if options.pdir else "templates"
        processesToProp = {
            'SR': ['ZNuNu','W'],
            'ZM' : ['ZLL','EWKZLL'],
            'ZE' : ['ZLL','EWKZLL'],
            'WM' : ['W','EWKW'],
            'WE' : ['W','EWKW']
            }
        all_regions = ['SR'] + ctrl_regions
        for reg in all_regions:
            options.region = reg
            for s,v in sel_steps.iteritems():
                print "#===> Propagating systematics for control region ",options.region," at selection step: ",s, "(cut =",v,")"
                options.upToCut = s
                options.pdir = pdirbase + "/" + s
                mcpOpts = ['--rebin '+str(rebinFactor[s])]
                procs = ','.join(processesToProp[reg])
                print "# propagating systematics to processes ",procs, " in the region ",reg
                analysis = Analysis(options,mcpOpts)
                myout = pdirbase+"/"+s+"/templates_"+options.propSystToVar+'_'+reg+'.root'
                analysis.runOneSyst(options.propSystToVar,procs,myout)


    # eg:  vbfdm/analysis.py --tF detajj_fullsel
    elif len(options.transferFactor)>0:

        # list of transfer factors to do, with files with input templates
        TFs = {
            #    key                num    den    numfile  denfile
            'Znunu_from_Zmumu' : ['ZNuNu','ZLL','SR','ZM'],
            'Znunu_from_Zee'   : ['ZNuNu','ZLL','SR','ZE'],
            'W_from_Wmumu' : ['W','W','SR','WM'],
            'W_from_Wenu' : ['W','W','SR','WE'],
            'Z_from_Wlnu' : ['ZNuNu','W','SR','SR']
            }
        
        for s,v in sel_steps.iteritems():
            print "#===> Calculating transfer factors for variable ",options.transferFactor," at selection step: ",s, "(cut =",v,")"
            for k,tf in TFs.iteritems():
                num_proc=tf[0]; den_proc=tf[1]
                outdir = options.pdir if options.pdir else 'templates'
                file_prefix = outdir+('/'+s+'/templates_'+options.transferFactor+'_')
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
             
             
                outname = outdir+"/"+s+"/rfactors_"+options.transferFactor+"_"+num_proc+num_sel+"_Over_"+tf[3]+den_sel+".root"
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
        if(options.region=='SR'): mcpOpts += ['--showIndivSigShapes','--xp data,QCD','--rebin 2']
        analysis = Analysis(options,mcpOpts)
        analysis.runOne()
