#!/bin/env python                                                                                                                                                                                          

# usage: ./mergeCardComponents.py -b Wmu -m --long-lnN 1.10 -C minus,plus -i ../cards/helicity_xxxxx/
# fit scaling by eff: ./mergeCardComponents.py -b Wel -m -C minus,plus -i ../cards/helicity_xxxxx/ --longToTotal 0.5 --sf mc_reco_eff.root --absolute

import ROOT
import sys,os,re

from optparse import OptionParser
parser = OptionParser(usage='%prog [options] cards/card*.txt')
parser.add_option(     '--Ybins' , dest='Ybins' , default='-6.0,-3.25,-2.75,-2.5,-2.25,-2.0,-1.75,-1.5,-1.25,-1.0,-0.75,-0.5,-0.25,0.,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.25,6.0', type='string', help='binning in Y')
parser.add_option('-m','--merge-root', dest='mergeRoot', default=False, action='store_true', help='Merge the root files with the inputs also')
parser.add_option('-i','--input', dest='inputdir', default='', type='string', help='input directory with all the cards inside')
parser.add_option('-b','--bin', dest='bin', default='ch1', type='string', help='name of the bin')
parser.add_option('-C','--charge', dest='charge', default='plus,minus', type='string', help='process given charge. default is both')
parser.add_option('-c','--constrain-rates', dest='constrainRateParams', type='string', default='0,1,2', help='add constraints on the rate parameters of (comma-separated list of) rapidity bins. Give only the left ones (e.g. 1 will constrain 1 with n-1 ')
parser.add_option('-l','--long-lnN', dest='longLnN', type='float', default=None, help='add a common lnN constraint to all longitudinal components')
parser.add_option(     '--absolute', dest='absoluteRates', default=False, action='store_true', help='Fit for absolute rates, not scale factors')
parser.add_option(     '--longToTotal', dest='longToTotal', type='float', default=None, help='Apply a constraint on the Wlong/Wtot rate. Implies fitting for absolute rates')
parser.add_option(     '--sf'    , dest='scaleFile'    , default='', type='string', help='path of file with the scaling/unfolding')
(options, args) = parser.parse_args()

from symmetrizeMatrix import getScales

charges = options.charge.split(',')

for charge in charges:

    outfile  = os.path.join(options.inputdir,options.bin+'_{ch}_shapes.root'.format(ch=charge))
    cardfile = os.path.join(options.inputdir,options.bin+'_{ch}_card.txt'   .format(ch=charge))

    ## prepare the relevant files. only the datacards and the correct charge
    files = ( f for f in os.listdir(options.inputdir) if f.endswith('.card.txt') )
    files = ( f for f in files if charge in f )
    files = sorted(files, key = lambda x: int(x.rstrip('.card.txt').split('_')[-1]) if not 'bkg' in x else -1) ## ugly but works
    files = list( ( os.path.join(options.inputdir, f) for f in files ) )
    
    existing_bins = []
    empty_bins = []

    ## look for the maximum ybin bin number
    nbins = 0
    print "FILES = ",files
    for f in files:
        if 'Ybin_' in f:
            n = int(f[f.find('Ybin_')+5 : f.find('.card')])
            if n>nbins: nbins=n
            if n not in existing_bins: existing_bins.append(n)
    print 'found {n} bins of rapidity'.format(n=nbins+1)

    ybins = list(float(i) for i in options.Ybins.split(','))
    for b in xrange(len(ybins)-1):
        if b not in existing_bins: 
            if b not in empty_bins:
                empty_bins.append(b)
                empty_bins.append(nbins+1-b)            

    longBKG = False
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
                    if not ('left' in l and 'right' in l):
                        if not binn in empty_bins: 
                            if binn >= 0:
                                empty_bins.append(binn)
                                empty_bins.append(nbins-binn)
                        isEmpty = True
                    processes = l.split()[1:]
                if re.match('process\s+W.*long',l) and 'bkg' in f:
                    print "===> W long is treated as a background"
                    longBKG = True
        if options.mergeRoot:
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
                            if longBKG and re.match('(Wplus_long|Wminus_long)',p): newprocname = p
                            newname = name.replace(p,newprocname)
                            if newname not in plots:
                                plots[newname] = obj.Clone(newname)
                                #print 'replacing old %s with %s' % (name,newname)
                                plots[newname].Write()
         
                of.Close()
    if len(empty_bins):
        print 'found a bunch of empty bins:', empty_bins
    if options.mergeRoot:
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
                        realprocesses.append(pseudoprocesses[i]+"_"+pseudobins[i] if ('Wminus' in pseudobins[i] or 'Wplus' in pseudobins[i]) else pseudoprocesses[i])
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
    
    if options.longToTotal or options.scaleFile: options.absoluteRates = True
    
    kpatt = " %7s "
    if options.longLnN and not options.longToTotal:
        combinedCard.write('norm_long_'+options.bin+'       lnN    ' + ' '.join([kpatt % (options.longLnN if 'long' in x else '-') for x in realprocesses])+'\n')

    combinedCard = open(cardfile,'r')
    procs = []
    rates = []
    for l in combinedCard.readlines():
        if re.match("process\s+",l) and not re.match("process\s+\d",l): # my regexp qualities are bad... 
            procs = (l.rstrip().split())[1:]
        if re.match("rate\s+",l):
            rates = (l.rstrip().split())[1:]
        if len(procs) and len(rates): break
    ProcsAndRates = zip(procs,rates)
    ProcsAndRatesDict = dict(zip(procs,rates))

    efficiencies = {}
    if options.scaleFile:
        for pol in ['left','right','long']: 
            efficiencies[pol] = [1./x for x in getScales(ybins, charge, pol, options.scaleFile)]

    combinedCard = open(cardfile,'a')
    POIs = []
    if options.constrainRateParams:
        signal_procs = filter(lambda x: re.match('Wplus|Wminus',x), realprocesses)
        if longBKG: signal_procs = filter(lambda x: re.match('(?!Wplus_long|Wminus_long)',x), signal_procs)
        signal_procs.sort(key=lambda x: int(x.split('_')[-1]))
        signal_L = filter(lambda x: re.match('.*left.*',x),signal_procs)
        signal_R = filter(lambda x: re.match('.*right.*',x),signal_procs)
        signal_0 = filter(lambda x: re.match('.*long.*',x),signal_procs)
        
        hel_to_constrain = [signal_L,signal_R]
        bins_to_constrain = options.constrainRateParams.split(',')
        tightConstraint = 0.05
        looseConstraint = 0.20
        for hel in hel_to_constrain:
            for i in xrange(len(hel)/2):
                pfx = '_'.join(hel[i].split('_')[:-1])
                sfx = (hel[i].split('_')[-1],hel[-i-1].split('_')[-1])
                pol = pfx.split('_')[1]
                rateNuis = tightConstraint if sfx[0] in bins_to_constrain else looseConstraint
                normPOI = 'norm_%s_%s_%s' % (pfx,sfx[0],sfx[1])
                if options.absoluteRates:
                    if options.scaleFile:
                        effPar = normPOI.replace('norm','eff')
                        ybin_0 = int(sfx[0].split('_')[-1])
                        ybin_1 = int(sfx[1].split('_')[-1])
                        combinedCard.write('%-5s   rateParam * %s_%-5s %.4f [%.4f,%.4f]\n' % (effPar,pfx,sfx[0],efficiencies[pol][ybin_0],(1-1E-04)*efficiencies[pol][ybin_0],(1+1E-04)*efficiencies[pol][ybin_0]))
                        combinedCard.write('%-5s   rateParam * %s_%-5s %.4f [%.4f,%.4f]\n' % (effPar,pfx,sfx[1],efficiencies[pol][ybin_1],(1-1E-04)*efficiencies[pol][ybin_1],(1+1E-04)*efficiencies[pol][ybin_1]))
                        expRate0 = float(ProcsAndRatesDict[pfx+'_'+sfx[0]])/efficiencies[pol][ybin_0]
                        expRate1 = float(ProcsAndRatesDict[pfx+'_'+sfx[1]])/efficiencies[pol][ybin_1]
                        param_range_0 = '%15.1f [%.0f,%.0f]' % (expRate0,(1-rateNuis)*expRate0,(1+rateNuis)*expRate0)
                        param_range_1 = '%15.1f [%.0f,%.0f]' % (expRate1,(1-rateNuis)*expRate1,(1+rateNuis)*expRate1)
                        combinedCard.write('%-5s   rateParam * %s_%-5s %s\n' % (normPOI,pfx,sfx[0],param_range_0))
                        combinedCard.write('%-5s   rateParam * %s_%-5s %s\n' % (normPOI,pfx,sfx[1],param_range_1))
                    else:
                        expRate0 = float(ProcsAndRatesDict[pfx+'_'+sfx[0]])
                        expRate1 = float(ProcsAndRatesDict[pfx+'_'+sfx[1]])
                        param_range_0 = '%15.1f [%.0f,%.0f]' % (expRate0,(1-rateNuis)*expRate0,(1+rateNuis)*expRate0)
                        param_range_1 = '%15.1f [%.0f,%.0f]' % (expRate1,(1-rateNuis)*expRate1,(1+rateNuis)*expRate1)
                        combinedCard.write('%-5s   rateParam * %s_%-5s    %s\n' % (normPOI,pfx,sfx[0],param_range_0))
                        combinedCard.write('%-5s   rateParam * %s_%-5s    %s\n' % (normPOI,pfx,sfx[1],param_range_1))
                else:
                    param_range_0 = '1 [%.2f,%.2f]' % (1-rateNuis,1+rateNuis)
                    param_range_1 = param_range_0
                    combinedCard.write('%-5s   rateParam * %s_%-5s    %s\n' % (normPOI,pfx,sfx[0],param_range_0))
                    combinedCard.write('%-5s   rateParam * %s_%-5s    %s\n' % (normPOI,pfx,sfx[1],param_range_1))
                POIs.append(normPOI)
        if not longBKG and not options.longLnN:
            for i in xrange(len(signal_0)/2):
                sfx = signal_0[i].split('_')[-1]
                param_range = '[0.95,1.05]' if sfx in bins_to_constrain else '[0.80,1.20]'
                combinedCard.write('norm_%-5s   rateParam * %-5s    1 %s\n' % (signal_0[i],signal_0[i],param_range))
                combinedCard.write('norm_%-5s   rateParam * %-5s    1 %s\n' % (signal_0[-1-i],signal_0[-1-i],param_range))
                POIs.append('norm_%s' % signal_0[i])
                POIs.append('norm_%s' % signal_0[-1-i])
    
        if options.absoluteRates:
            combinedCard = open(cardfile,'r')
            procs = []
            rates = []
            for l in combinedCard.readlines():
                if re.match("process\s+",l) and not re.match("process\s+\d",l): # my regexp qualities are bad... 
                    procs = (l.rstrip().split())[1:]
                if re.match("rate\s+",l):
                    rates = (l.rstrip().split())[1:]
                if len(procs) and len(rates): break
            ProcsAndRates = zip(procs,rates)

            combinedCard = open(cardfile,'r')
            ProcsAndRatesUnity = []
            for (p,r) in ProcsAndRates:
                ProcsAndRatesUnity.append((p,'1') if ('left' in p or 'right' in p or 'long' in p) else (p,r))

            combinedCardNew = open(cardfile+"_new",'w')
            for l in combinedCard.readlines():
                if re.match("rate\s+",l):
                    combinedCardNew.write('rate            %s \n' % ' '.join([kpatt % r for (p,r) in ProcsAndRatesUnity])+'\n')
                else: combinedCardNew.write(l)
            Wlong = [(p,r) for (p,r) in ProcsAndRates if re.match('W.*long',p)]
            WLeftOrRight = [(p,r) for (p,r) in ProcsAndRates if ('left' in p or 'right' in p)]
            if options.scaleFile:
                eff_long = 1./getScales([ybins[0],ybins[-1]], charge, 'long', options.scaleFile)[0]
                eff_left = 1./getScales([ybins[0],ybins[-1]], charge, 'left', options.scaleFile)[0]
                eff_right = 1./getScales([ybins[0],ybins[-1]], charge, 'right', options.scaleFile)[0]
                normWLong = sum([float(r) for (p,r) in Wlong])/eff_long # there should be only 1 Wlong/charge
                normWLeft = sum([float(r) for (p,r) in WLeftOrRight if 'left' in p])/eff_left
                normWRight = sum([float(r) for (p,r) in WLeftOrRight if 'right' in p])/eff_right
                normWLeftOrRight = normWLeft + normWRight
                combinedCardNew.write("eff_%-50s   rateParam * %-5s    %.4f [%.4f,%.4f]\n" % (Wlong[0][0],Wlong[0][0],eff_long,(1-1E-04)*eff_long,(1+1E-04)*eff_long))
                if options.longToTotal:
                    r0overLR = normWLong/normWLeftOrRight
                    combinedCardNew.write("norm_%-50s    rateParam * %-5s    %15.1f [%.0f,%.0f]\n" % (Wlong[0][0],Wlong[0][0],normWLeftOrRight,(1-options.longToTotal)*normWLeftOrRight,(1+options.longToTotal)*normWLeftOrRight))
                    wLongNormString = "ratio_%-5s   rateParam * %-5s   2*(%s)*%.3f %s\n" \
                        % (Wlong[0][0],Wlong[0][0],'+'.join(['@%d'%i for i in xrange(len(POIs))]),r0overLR,','.join([p for p in POIs]))
                    combinedCardNew.write(wLongNormString)
                else:
                    combinedCardNew.write("norm_%-50s    rateParam * %-5s    %15.1f [%.0f,%.0f]\n" % (Wlong[0][0],Wlong[0][0],normWLong,(1-tightConstraint)*normWLong,(1+tightConstraint)*normWLong))                    
            else:
                normWLong = sum([float(r) for (p,r) in Wlong]) # there should be only 1 Wlong/charge
                normWLeftOrRight = sum([float(r) for (p,r) in WLeftOrRight])
                if options.longToTotal:
                    r0overLR = normWLong/normWLeftOrRight
                    combinedCardNew.write("norm_%-50s   rateParam * %-5s  %15.1f [%.0f,%.0f]\n" % (Wlong[0][0],Wlong[0][0],normWLeftOrRight,(1-options.longToTotal)*normWLeftOrRight,(1+options.longToTotal)*normWLeftOrRight))
                    wLongNormString = "ratio_%-5s   rateParam * %-5s   2*(%s)*%.3f %s\n" \
                        % (Wlong[0][0],Wlong[0][0],'+'.join(['@%d'%i for i in xrange(len(POIs))]),r0overLR,','.join([p for p in POIs]))
                    combinedCardNew.write(wLongNormString)
                else:
                    combinedCardNew.write("norm_%-50s   rateParam * %-5s  %15.1f [%.0f,%.0f]\n" % (Wlong[0][0],Wlong[0][0],normWLong,(1-tightConstraint)*normWLong,(1+tightConstraint)*normWLong))                    
            combinedCardNew.write("efficiencies group = %s" % 'eff_'+Wlong[0][0]+' '+' '.join([p.replace('norm','eff') for p in POIs]) )

            os.system("mv {cardfile}_new {cardfile}".format(cardfile=cardfile))

    print "merged datacard in ",cardfile
    
    #ws = "%s_ws.root" % options.bin
    ws = cardfile.replace('_card.txt', '_ws.root')
    txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal '.format(cf=cardfile, ws=ws)
    if options.longToTotal: txt2wsCmd += "  --X-no-check-norm"
    print txt2wsCmd
    
    #print 'combine {ws} -M FitDiagnostics -t -1 --expectSignal=1 -m 999 --saveShapes --saveWithUncertainties --redefineSignalPOIs {pois} --skipBOnlyFit -v 9'.format(ws=ws,pois=','.join(POIs))
    print 'combine {ws} -M MultiDimFit    -t -1 --expectSignal=1 -m 999 --saveFitResult --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1 --redefineSignalPOIs {pois} -P {floatPOIs} --floatOtherPOIs=0 -v 9'.format(ws=ws, pois=','.join(POIs), floatPOIs=' -P '.join(POIs))
