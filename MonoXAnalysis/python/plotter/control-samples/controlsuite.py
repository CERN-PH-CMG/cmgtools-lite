#!/usr/bin/env python

import sys, os
import re
from optparse import OptionParser

class PlotSet:
    def __init__(self,commands,weights,options):
        self._commands = commands
        self._weights = weights
        self._options = options

    def runAllVariables(self,subdet,r9,plotSel=None):
        # categorization
        if r9=="inclusive": r9_cut="" 
        else: r9_cut = " -A mass r9 'LepGood1_r9>0.94 && LepGood2_r9>0.94' " if r9=="high" else " -A mass r9 'LepGood1_r9<0.94 && LepGood2_r9<0.94' "

        pdir = "plots/Zel_ECAL_%s_r9_%s" % (subdet,r9)
        if subdet=="inclusive": eta_cut = ""
        else: eta_cut = " -A mass subdet 'abs(LepGood1_eta)<1.44 && abs(LepGood2_eta)<1.44' " if subdet=="barrel" else " -A mass subdet 'abs(LepGood1_eta)>1.57 && abs(LepGood2_eta)>1.57' "
      
        if plotSel!=None: plots=' --sP '+(' --sP '.join(plotSel))
        else: plots=''

        print "Using r9cut = ",r9_cut," and eta cut = ",eta_cut
        print "Printing the plots ",plots
      
        (runy,runp) = (self._commands[0],self._commands[1])
        (fev,sf) = (self._weights[0],self._weights[1])
        commands = []
        if options.yields: commands.append('python ' + runy + r9_cut + eta_cut + fev + sf + ' --sp DYJets ')
        if options.plot: commands.append('python ' + runp + r9_cut + eta_cut + fev + sf + ' --sp DYJets --pdir ' + pdir + ' --print=pdf,png ' + plots) 
        command = ' ; '.join(commands)
        if options.dryrun: print command
        else: os.system(command)


if __name__ == "__main__":
    usage="%prog mca.txt selection.txt plotfile.txt [options]"

    parser = OptionParser(usage=usage)
    parser.add_option("-y", "--yield", dest="yields", action="store_true", default=False, help='Make the yields')
    parser.add_option("-p", "--plot", dest="plot", action="store_true", default=False, help='Make only the plots')
    parser.add_option("-a", "--all", dest="allplots", action="store_true", default=False, help='Make all the plots, for EB and EE (not in R9 categories)')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')

    (options, args) = parser.parse_args()
    
    if len(args)<3: raise RuntimeError, 'Expecting at least three arguments'
    mca = args[0]
    selection = args[1]
    plotfile = args[2]

    T='/data1/emanuele/monox/TREES_2LEP_80X_V2/'

    lumi = '12.9' # fb-1
    weight = " -W 'vtxWeight' " #"-W 'vtxWeight*SF_trigmetnomu*SF_BTag*SF_NLO_QCD*SF_NLO_EWK' "
    coreopt = '-P '+T+' --s2v -j 6 -l ' + lumi + weight
    corey = 'mcAnalysis.py ' + coreopt + ' -G '
    corep = 'mcPlots.py ' + coreopt + ' -f --poisson --showRatio --maxRatioRange 0.7 1.3 --fixRatioRange --scaleSigToData '
    fev = ' -F mjvars/t \"'+T+'/friends/evVarFriend_{cname}.root\" '
    sf = '' #sf = ' --FM sf/t \"'+T+'/friends/sfFriend_{cname}.root\" '

    runy = corey + mca + ' ' + selection
    runp = corep + mca + ' ' + selection + ' ' + plotfile

    pset = PlotSet([runy,runp],[fev,sf],options)

    if options.allplots:
        for subdet in ['barrel','endcap']: pset.runAllVariables(subdet,'inclusive')
    else:
        print "only check mass variables..."
        massPlots = []
        infile = open(plotfile,'r')
        for line in infile:
            if re.match("\s*#.*", line) or len(line.strip())==0: continue
            plotName = line.split(":")[0]
            if 'mass' in plotName: massPlots.append(plotName)
        print "Will plot the variables: ",massPlots
        for subdet in ['barrel','endcap']: 
            for r9 in ['high','low']:
                pset.runAllVariables(subdet,r9,massPlots)
        
