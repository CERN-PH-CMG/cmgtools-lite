#!/bin/env python                                                                                                                                                                                          
# usage: ./mergeCardComponents.py shapes.root combcard.txt -b Wm_el cards/helicity/card_bin*.card.txt

import ROOT
import sys,os,re

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] shapes.root combinedcard.txt cards/card*.txt")
parser.add_option("-m","--merge-root", dest="mergeRoot", default=False, action="store_true", help="Merge the root files with the inputs also")
parser.add_option("-b","--bin", dest="bin", default="ch1", type="string", help="name of the bin")
parser.add_option("-c","--constrain-rates", dest="constrainRateParams", type="string", default="0,1,2", help="add constraints on the rate parameters of (comma-separated list of) rapidity bins. Give only the left ones (e.g. 1 will constrain 1 with n-1 ")
(options, args) = parser.parse_args()

outfile=args[0]
cardfile=args[1]
files=args[2:]

if options.mergeRoot:
    for f in files:
        dir = os.path.dirname(f)
        with open(f) as file:
            for l in file.readlines():
                if re.match("shapes.*",l):
                    rootfile = dir+"/"+l.split()[3]
                if re.match("bin.*",l):
                    bin = l.split()[1]
                if re.match("process\s+",l) and '1' not in l:
                    processes = l.split()[1:]
        print "rootfile = ",rootfile
        print "bin = ",bin
        print "processes = ",processes
        tf = ROOT.TFile.Open(rootfile)
        of=ROOT.TFile("tmp_"+bin+".root","recreate")
        # remove the duplicates also
        plots = {}
        for e in tf.GetListOfKeys() :
            name=e.GetName()
            obj=e.ReadObj()
            for p in processes:
                if p in name:
                    newprocname = p+"_"+bin if ('Wm' in p or 'Wm' in p) else p
                    newname = name.replace(p,newprocname)
                    if newname not in plots:
                        plots[newname] = obj.Clone(newname)
                        print "replacing old %s with %s" % (name,newname)
                        plots[newname].Write()
     
        of.Close()
    os.system("hadd -f %s tmp_*root" % outfile)

    
combineCmd="combineCards.py "
for f in files:
    basename = os.path.basename(f).split(".")[0]
    binname = basename if ("Wp_" in basename or "Wm_" in basename) else "other"
    combineCmd += " %s=%s " % (binname,f)
combineCmd += " > tmpcard.txt"
os.system(combineCmd)

combinedCard = open(cardfile,'w')
combinedCard.write("imax 1\n")
combinedCard.write("jmax *\n")
combinedCard.write("kmax *\n")
combinedCard.write('##----------------------------------\n') 
realprocesses = [] # array to preserve the sorting
with open("tmpcard.txt") as file:    
    nmatchbin=0
    nmatchprocess=0
    for l in file.readlines():
        if re.match("shapes.*other",l):
            variables = l.split()[4:]
            combinedCard.write("shapes *  *  %s %s\n" % (outfile," ".join(variables)))
            combinedCard.write('##----------------------------------\n')
        if re.match("bin",l) and nmatchbin==0: 
            nmatchbin=1
            combinedCard.write('bin   %s\n' % options.bin) 
            bins = l.split()[1:]
        if re.match("observation",l): 
            yields = l.split()[1:]
            observations = dict(zip(bins,yields))
            combinedCard.write('observation %s\n' % observations['other'])
            combinedCard.write('##----------------------------------\n')
        if re.match("bin",l) and nmatchbin==1:
            pseudobins = l.split()[1:]
        if re.match("process",l):
            if nmatchprocess==0:
                pseudoprocesses = l.split()[1:]
                klen = 7
                kpatt = " %%%ds "  % klen
                for i in xrange(len(pseudobins)):
                    realprocesses.append(pseudoprocesses[i]+"_"+pseudobins[i] if ('Wm' in pseudobins[i] or 'Wp' in pseudobins[i]) else pseudoprocesses[i])
                combinedCard.write('bin            %s \n' % ' '.join([kpatt % options.bin for p in pseudoprocesses]))
                combinedCard.write('process        %s \n' % ' '.join([kpatt % p for p in realprocesses]))
                combinedCard.write('process        %s \n' % ' '.join([kpatt % str(i+1) for i in xrange(len(pseudobins))]))
            nmatchprocess += 1
        if nmatchprocess==2: 
            nmatchprocess +=1
        elif nmatchprocess>2: combinedCard.write(l)

os.system("rm tmpcard.txt")
if options.mergeRoot: 
    print "merged inputs in ",outfile
    os.system("rm tmp_*root")

print "merged datacard in ",cardfile

if options.constrainRateParams:
    signal_procs = filter(lambda x: re.match('Wp|Wm',x), realprocesses)
    signal_procs.sort(key=lambda x: int(x.split('_')[-1]))
    signal_L = filter(lambda x: re.match('.*left.*',x),signal_procs)
    signal_R = filter(lambda x: re.match('.*right.*',x),signal_procs)
    signal_0 = filter(lambda x: re.match('.*long.*',x),signal_procs)
    
    hel_to_constrain = [signal_L,signal_R]
    bins_to_constrain = options.constrainRateParams.split(',')
    for hel in hel_to_constrain:
        for i in xrange(len(hel)/2):
            pfx = '_'.join(hel[i].split('_')[:-1])
            sfx = (hel[i].split('_')[-1],hel[-i-1].split('_')[-1])
            param_range = '[0.95,1.05]' if sfx[0] in bins_to_constrain else '[0.80,1.20]'
            combinedCard.write('norm_%s_%s_%-5s   rateParam * %s_%-5s    1 %s\n' % (pfx,sfx[0],sfx[1],pfx,sfx[0],param_range))
            combinedCard.write('norm_%s_%s_%-5s   rateParam * %s_%-5s    1 %s\n' % (pfx,sfx[0],sfx[1],pfx,sfx[1],param_range))

    
