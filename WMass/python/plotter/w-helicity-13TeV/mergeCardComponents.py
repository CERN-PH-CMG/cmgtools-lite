#!/bin/env python                                                                                                                                                                                          

# usage: ./mergeCardComponents.py -b Wmu -m --long-lnN 1.10 -C minus,plus -i ../cards/helicity_xxxxx/

import ROOT
import sys,os,re

from optparse import OptionParser
parser = OptionParser(usage='%prog [options] cards/card*.txt')
parser.add_option('-m','--merge-root', dest='mergeRoot', default=False, action='store_true', help='Merge the root files with the inputs also')
parser.add_option('-i','--input', dest='inputdir', default='', type='string', help='input directory with all the cards inside')
parser.add_option('-b','--bin', dest='bin', default='ch1', type='string', help='name of the bin')
parser.add_option('-C','--charge', dest='charge', default='plus,minus', type='string', help='process given charge. default is both')
parser.add_option('-c','--constrain-rates', dest='constrainRateParams', type='string', default='0,1,2', help='add constraints on the rate parameters of (comma-separated list of) rapidity bins. Give only the left ones (e.g. 1 will constrain 1 with n-1 ')
parser.add_option('-l','--long-lnN', dest='longLnN', type='float', default=None, help='add a common lnN constraint to all longitudinal components')
(options, args) = parser.parse_args()

charges = options.charge.split(',')

for charge in charges:

    outfile  = os.path.join(options.inputdir,options.bin+'_{ch}_shapes.root'.format(ch=charge))
    cardfile = os.path.join(options.inputdir,options.bin+'_{ch}_card.txt'   .format(ch=charge))

    ## prepare the relevant files. only the datacards and the correct charge
    files = ( f for f in os.listdir(options.inputdir) if f.endswith('.card.txt') )
    files = ( f for f in files if charge in f )
    files = sorted(files, key = lambda x: int(x.rstrip('.card.txt').split('_')[-1]) if not 'bkg' in x else -1) ## ugly but works
    files = list( ( os.path.join(options.inputdir, f) for f in files ) )
    
    ## look for the maximum ybin bin number
    nbins = 0
    for f in files:
        if 'Ybin_' in f:
            n = int(f[f.find('Ybin_')+5 : f.find('.card')])
            if n>nbins: nbins=n
    print 'found {n} bins of rapidity'.format(n=nbins+1)
    
    empty_bins = []
    
    if options.mergeRoot:
        tmpfiles = []
        for f in files:
            dir = os.path.dirname(f)
            bin = ''
            isEmpty = False
            with open(f) as file:
                for l in file.readlines():
                    if re.match('shapes.*',l):
                        rootfile = dir+'/'+l.split()[3]
                    if re.match('bin.*',l):
                        if len(l.split()) < 2: continue ## skip the second bin line if empty
                        bin = l.split()[1]
                        binn = int(bin.split('_')[-1]) if 'Ybin_' in bin else -1
                    #if re.match('process\s+',l) and '1' not in l:
                    if re.match('process\s+',l): 
                        if len(l.split()) > 1 and all(n.isdigit() for n in l.split()[1:]) : continue
                        if not ('left' in l and 'right' in l and 'long' in l):
                            if not binn in empty_bins: 
                                if binn >= 0:
                                    empty_bins.append(binn)
                                    empty_bins.append(nbins-binn)
                            isEmpty = True
                        processes = l.split()[1:]
            if not binn in empty_bins:
                print 'processing bin = ',bin
                tf = ROOT.TFile.Open(rootfile)
                tmpfile = os.path.join(options.inputdir,'tmp_'+bin+'.root')
                of=ROOT.TFile(tmpfile,'recreate')
                tmpfiles.append(tmpfile)
                # remove the duplicates also
                plots = {}
                for e in tf.GetListOfKeys() :
                    name=e.GetName()
                    obj=e.ReadObj()
                    if (not re.match('Wplus|Wminus',os.path.basename(f))) and 'data_obs' in name: obj.Clone().Write()
                    for p in processes:
                        if p in name:
                            newprocname = p+'_'+bin if re.match('Wplus|Wminus',p) else p
                            newname = name.replace(p,newprocname)
                            if newname not in plots:
                                plots[newname] = obj.Clone(newname)
                                #print 'replacing old %s with %s' % (name,newname)
                                plots[newname].Write()
         
                of.Close()
        if len(empty_bins):
            print 'found a bunch of empty bins:', empty_bins
        haddcmd = 'hadd -f {of} {tmpfiles}'.format(of=outfile, tmpfiles=' '.join(tmpfiles) )
        #print 'would run this now: ', haddcmd
        #sys.exit()
        os.system(haddcmd)
        os.system('rm {rm}'.format(rm=' '.join(tmpfiles)))
    
        
    combineCmd="combineCards.py "
    for f in files:
        basename = os.path.basename(f).split(".")[0]
        binn = int(basename.split('_')[-1]) if 'Ybin_' in basename else 999
        binname = basename if re.match('Wplus|Wminus',basename) else "other"
        if not binn in empty_bins:
            combineCmd += " %s=%s " % (binname,f)
    tmpcard = os.path.join(options.inputdir,'tmpcard.txt')
    combineCmd += ' > {tmpcard}'.format(tmpcard=tmpcard)
    #sys.exit()
    os.system(combineCmd)
    
    combinedCard = open(cardfile,'w')
    combinedCard.write("imax 1\n")
    combinedCard.write("jmax *\n")
    combinedCard.write("kmax *\n")
    combinedCard.write('##----------------------------------\n') 
    realprocesses = [] # array to preserve the sorting
    with open(tmpcard) as file:    
        nmatchbin=0
        nmatchprocess=0
        for l in file.readlines():
            if re.match("shapes.*other",l):
                variables = l.split()[4:]
                combinedCard.write("shapes *  *  %s %s\n" % (os.path.abspath(outfile)," ".join(variables)))
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
    
    os.system('rm {tmpcard}'.format(tmpcard=tmpcard))
    ## already done if options.mergeRoot: 
    ## already done     print "merged inputs in ",outfile
    ## already done     os.system("rm tmp_*root")
    
    
    if options.longLnN:
        kpatt = " %7s "
        combinedCard.write('norm_long_'+options.bin+'       lnN    ' + ' '.join([kpatt % (options.longLnN if 'long' in x else '-') for x in realprocesses])+'\n')
    
    POIs = []
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
                POIs.append('norm_%s_%s_%s' % (pfx,sfx[0],sfx[1]))
        if not options.longLnN:
            for i in xrange(len(signal_0)/2):
                sfx = signal_0[i].split('_')[-1]
                param_range = '[0.95,1.05]' if sfx in bins_to_constrain else '[0.80,1.20]'
                combinedCard.write('norm_%-5s   rateParam * %-5s    1 %s\n' % (signal_0[i],signal_0[i],param_range))
                combinedCard.write('norm_%-5s   rateParam * %-5s    1 %s\n' % (signal_0[-1-i],signal_0[-1-i],param_range))
                POIs.append('norm_%s' % signal_0[i])
                POIs.append('norm_%s' % signal_0[-1-i])
    
    print "merged datacard in ",cardfile
    
    #ws = "%s_ws.root" % options.bin
    ws = cardfile.replace('_card.txt', '_ws.root')
    txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal '.format(cf=cardfile, ws=ws)
    print txt2wsCmd
    
    print 'combine {ws} -M FitDiagnostics -t -1 --expectSignal=1 -m 999 --saveShapes --saveWithUncertainties --redefineSignalPOIs {pois}'.format(ws=ws,pois=','.join(POIs))
    print 'combine {ws} -M MultiDimFit    -t -1 --expectSignal=1 -m 999 --saveFitResult                      --redefineSignalPOIs {pois}'.format(ws=ws, pois=','.join(POIs))
