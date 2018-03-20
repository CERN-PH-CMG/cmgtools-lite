#!/bin/env python

# usage: ./mergeCardComponents.py -b Wmu -m --long-lnN 1.10 -C minus,plus -i ../cards/helicity_xxxxx/
# fit scaling by eff: ./mergeCardComponents.py -b Wel -m -C minus,plus -i ../cards/helicity_xxxxx/ --longToTotal 0.5 --sf mc_reco_eff.root --absolute

import ROOT
import sys,os,re

def mirrorShape(nominal,alternate,newname,alternateShapeOnly=False):
    alternate.SetName("%sUp" % newname)
    if alternateShapeOnly:
        alternate.Scale(nominal.Integral()/alternate.Integral())
    mirror = nominal.Clone("%sDown" % newname)
    for b in xrange(1,nominal.GetNbinsX()+1):
        y0 = nominal.GetBinContent(b)
        yA = alternate.GetBinContent(b)
        yM = y0
        if (y0 > 0 and yA > 0):
            yM = y0*y0/yA
        elif yA == 0:
            yM = 2*y0
        mirror.SetBinContent(b, yM)
    if alternateShapeOnly:
        # keep same normalization
        mirror.Scale(nominal.Integral()/mirror.Integral())
    else:
        # mirror normalization
        mnorm = (nominal.Integral()**2)/alternate.Integral()
        mirror.Scale(mnorm/alternate.Integral())
    return (alternate,mirror)


from optparse import OptionParser
parser = OptionParser(usage='%prog [options] cards/card*.txt')
parser.add_option('-m','--merge-root', dest='mergeRoot', default=False, action='store_true', help='Merge the root files with the inputs also')
parser.add_option('-i','--input', dest='inputdir', default='', type='string', help='input directory with all the cards inside')
parser.add_option('-b','--bin', dest='bin', default='ch1', type='string', help='name of the bin')
parser.add_option('-C','--charge', dest='charge', default='plus,minus', type='string', help='process given charge. default is both')
parser.add_option('-c','--constrain-rates', dest='constrainRateParams', type='string', default='0,1,2', help='add constraints on the rate parameters of (comma-separated list of) rapidity bins. Give only the left ones (e.g. 1 will constrain 1 with n-1 ')
parser.add_option(     '--fix-YBins', dest='fixYBins', type='string', default='', help='add here replacement of default rate-fixing. with format plusR=10,11,12;plusL=11,12;minusR=10,11,12;minusL=10,11 ')
parser.add_option('-p','--POIs', dest='POIsToMinos', type='string', default=None, help='Decide which are the nuiscances for which to run MINOS (a.k.a. POIs). Default is all non fixed YBins. With format poi1,poi2 ')
parser.add_option('-l','--long-lnN', dest='longLnN', type='float', default=None, help='add a common lnN constraint to all longitudinal components')
parser.add_option(     '--absolute', dest='absoluteRates', default=False, action='store_true', help='Fit for absolute rates, not scale factors')
parser.add_option(     '--longToTotal', dest='longToTotal', type='float', default=None, help='Apply a constraint on the Wlong/Wtot rate. Implies fitting for absolute rates')
parser.add_option(     '--sf'    , dest='scaleFile'    , default='', type='string', help='path of file with the scaling/unfolding')
(options, args) = parser.parse_args()

from symmetrizeMatrixAbsY import getScales

charges = options.charge.split(',')


for charge in charges:

    outfile  = os.path.join(options.inputdir,options.bin+'_{ch}_shapes.root'.format(ch=charge))
    cardfile = os.path.join(options.inputdir,options.bin+'_{ch}_card.txt'   .format(ch=charge))

    ## prepare the relevant files. only the datacards and the correct charge
    files = ( f for f in os.listdir(options.inputdir) if f.endswith('.card.txt') )
    files = ( f for f in files if charge in f and 'pdf' not in f )
    files = sorted(files, key = lambda x: int(x.rstrip('.card.txt').split('_')[-1]) if not 'bkg'in x else -1) ## ugly but works
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

    fixedYBins = {'plusR' : [n,n-1,n-2],
                  'plusL' : [n],
                  'minusR': [n,n-1,n-2],
                  'minusL': [n],
                 }
    
    if options.fixYBins:
        splitted = options.fixYBins.split(';')
        for comp in splitted:
            chhel = comp.split('=')[0]
            bins  = comp.split('=')[1]
            fixedYBins[chhel] = list(int(i) for i in bins.split(','))
            ## this doesn't work here anymore if not fixedYBins[chhel][0] == 0:
            ## this doesn't work here anymore     raise RuntimeError, "Your fixed bins should start at 0!!"
            ## this doesn't work here anymore if not max(fixedYBins[chhel]) == len(fixedYBins[chhel])-1:
            ## this doesn't work here anymore     raise RuntimeError, "This list does not seem to be continuous. Fix!"
    print fixedYBins


    ybinfile = open(os.path.join(options.inputdir, 'binningYW.txt'),'r')
    ybinline = ybinfile.readlines()[0]
    ybins = list(float(i) for i in ybinline.split())
    ybinfile.close()
    #ybins = list(float(i) for i in options.Ybins.split(','))
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
                basename = os.path.basename(f).split('.')[0]
                rootfiles_syst = filter(lambda x: re.match('{base}_(pdf\d+)\.input\.root'.format(base=basename),x), os.listdir(options.inputdir))
                rootfiles_syst = [dir+'/'+x for x in rootfiles_syst]
                rootfiles_syst.sort()
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
                nominals = {}
                for irf,rf in enumerate([rootfile]+rootfiles_syst):
                    print '\twith nominal/systematic file: ',rf
                    tf = ROOT.TFile.Open(rf)
                    tmpfile = os.path.join(options.inputdir,'tmp_{bin}_sys{sys}.root'.format(bin=bin,sys=irf))
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
                                if irf==0:
                                    if newname not in plots:
                                        plots[newname] = obj.Clone(newname)
                                        nominals[newname] = obj.Clone(newname+"0")
                                        nominals[newname].SetDirectory(None)
                                        #print 'replacing old %s with %s' % (name,newname)
                                        plots[newname].Write()
                                else:
                                    tokens = newname.split("_"); pfx = '_'.join(tokens[:-1]); pdf = tokens[-1]
                                    ipdf = int(pdf.split('pdf')[-1])
                                    newname = "{pfx}_pdf{ipdf}".format(pfx=pfx,ipdf=ipdf)
                                    (alternate,mirror) = mirrorShape(nominals[pfx],obj,newname)
                                    for alt in [alternate,mirror]:
                                        if alt.GetName() not in plots:
                                            plots[alt.GetName()] = alt.Clone()
                                            plots[alt.GetName()].Write()
                    of.Close()
    if len(empty_bins):
        print 'found a bunch of empty bins:', empty_bins
    if options.mergeRoot:
        haddcmd = 'hadd -f {of} {tmpfiles}'.format(of=outfile, tmpfiles=' '.join(tmpfiles) )
        #print 'would run this now: ', haddcmd
        #sys.exit()
        os.system(haddcmd)
        os.system('rm {rm}'.format(rm=' '.join(tmpfiles)))

    print "Now trying to get info on PDF uncertainties..."
    pdfsyst = {}
    tf = ROOT.TFile.Open(outfile)
    for e in tf.GetListOfKeys() :
        name=e.GetName()
        if 'pdf' in name:
            if name.endswith("Up"): name = re.sub('Up$','',name)
            if name.endswith("Down"): name = re.sub('Down$','',name)
            syst = name.split('_')[-1]
            binWsyst = '_'.join(name.split('_')[1:-1])
            if syst not in pdfsyst: pdfsyst[syst] = [binWsyst]
            else: pdfsyst[syst].append(binWsyst)
    if len(pdfsyst): print "Found a bunch of PDF sysematics: ",pdfsyst.keys()
    else: print "You are running w/o PDF systematics. Lucky you!"

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

    efficiencies = {}; efferrors = {}
    if options.scaleFile:
        for pol in ['left','right','long']: 
            efficiencies[pol] = [1./x for x in getScales(ybins, charge, pol, os.path.abspath(options.scaleFile))]
            efferrors   [pol] = [   x for x in getScales(ybins, charge, pol, os.path.abspath(options.scaleFile), returnError=True)] ## these errors are relative to the effs

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
        looseConstraint = tightConstraint
        for hel in hel_to_constrain:
            for iy,helbin in enumerate(hel):
                pol = helbin.split('_')[1]
                index_procs = procs.index(helbin)
                lns = ' - '.join('' for i in range(index_procs+1))
                lns += ' {effunc:.4f} '.format(effunc=1.+efferrors[pol][iy])
                lns += ' - '.join('' for i in range(len(procs) - index_procs))
                combinedCard.write('eff_unc_{hb}    lnN {lns}\n'.format(hb=helbin,lns=lns))
        for hel in hel_to_constrain:
            for iy,helbin in enumerate(hel):
                sfx = str(iy)
                pol = helbin.split('_')[1]
                rateNuis = tightConstraint if iy in bins_to_constrain else looseConstraint
                normPOI = 'norm_{n}'.format(n=helbin)

                ## if we fit absolute rates, we need to get them from the process and plug them in below
                if options.absoluteRates:

                    ## if we want to fit with the efficiency gen-reco, we need to add one efficiency parameter
                    if options.scaleFile:
                        tmp_eff = efficiencies[pol][iy]
                        combinedCard.write('eff_{n}    rateParam * {n} \t {eff:.5f} [{dn:.5f},{up:.5f}]\n'.format(n=helbin,eff=tmp_eff,dn=(1-1E-04)*tmp_eff,up=(1+1E-04)*tmp_eff))
                        expRate0 = float(ProcsAndRatesDict[helbin])/tmp_eff
                        param_range_0 = '{r:15.1f} [{dn:.1f},{up:.1f}]'.format(r=expRate0,dn=(1-rateNuis)*expRate0,up=(1+rateNuis)*expRate0)
                        combinedCard.write('norm_{n}  rateParam * {n} \t {pr}\n'.format(n=helbin,pr=param_range_0))

                    ## if we do not want to fit the gen-level thing, we want to just put the absolute reco rates here
                    else:
                        expRate0 = float(ProcsAndRatesDict[helbin])
                        param_range_0 = '{r:15.1f} [{dn:.1f},{up:.1f}]'.format(r=expRate0,dn=(1-rateNuis)*expRate0,up=(1+rateNuis)*expRate0)
                        combinedCard.write('norm_{n}  rateParam * {n} \t {pr}\n'.format(n=helbin,pr=param_range_0))

                ## if not fitting full rates, we do the relative rateParams close to 1.
                else:
                    param_range_0 = '1. [{dn:.2f},{up:.2f}]'.format(dn=1-rateNuis,up=1+rateNuis)
                    param_range_1 = param_range_0
                    combinedCard.write('norm_{n}   rateParam * {n}    {pr}\n'.format(n=helbin,pr=param_range_0))
                POIs.append(normPOI)

        ## not sure this below will still work with absY, but for now i don't care (marc)
        if not longBKG and not options.longLnN:
            for i in xrange(len(signal_0)):
                sfx = signal_0[i].split('_')[-1]
                param_range = '[0.95,1.05]' if sfx in bins_to_constrain else '[0.95,1.05]'
                combinedCard.write('norm_%-5s   rateParam * %-5s    1 %s\n' % (signal_0[i],signal_0[i],param_range))
                POIs.append('norm_%s' % signal_0[i])
    
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
                combinedCardNew.write("eff_{n}   rateParam * {n}    {eff:.5f} [{dn:.5f},{up:.5f}]\n".format(n=Wlong[0][0],eff=eff_long,dn=(1-1E-04)*eff_long,up=(1+1E-04)*eff_long))

                ## i have no idea what happens after here in this if block...
                if options.longToTotal:
                    r0overLR = normWLong/normWLeftOrRight
                    combinedCardNew.write("norm_%-50s    rateParam * %-5s    %15.1f [%.0f,%.0f]\n" % (Wlong[0][0],Wlong[0][0],normWLeftOrRight,(1-options.longToTotal)*normWLeftOrRight,(1+options.longToTotal)*normWLeftOrRight))
                    wLongNormString = "ratio_%-5s   rateParam * %-5s   2*(%s)*%.3f %s\n" \
                        % (Wlong[0][0],Wlong[0][0],'+'.join(['@%d'%i for i in xrange(len(POIs))]),r0overLR,','.join([p for p in POIs]))
                    combinedCardNew.write(wLongNormString)

                ## if we do not constrain the long to the total, we should write the long yield here
                else:
                    nl = normWLong; tc = tightConstraint
                    combinedCardNew.write("norm_{n} rateParam * {n} {r:15.1f} [{dn:.1f},{up:.1f}]\n".format(n=Wlong[0][0],r=nl,dn=(1-tc)*nl,up=(1+tc)*nl))
                    POIs.append('norm_{n}'.format(n=Wlong[0][0]))

            ## if we do not scale gen-reco, then we go back to before...
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

            ## make an efficiency nuisance group
            combinedCardNew.write('\nefficiencies group = eff_'+Wlong[0][0]+' '+' '.join([p.replace('norm','eff') for p in POIs])+'\n\n' )

            ## add the PDF systematics 
            for sys,procs in pdfsyst.iteritems():
                # there should be 2 occurrences of the same proc in procs (Up/Down). This check should be useless if all the syst jobs are DONE
                combinedCardNew.write('%-15s   shape %s\n' % (sys,(" ".join([kpatt % '1.0' if p in procs and procs.count(p)==2 else '  -  ' for p,r in ProcsAndRates]))) )
            combinedCardNew.write('\npdfs group = '+' '.join([sys for sys,procs in pdfsyst.iteritems()])+'\n')

            combinedCardNew.close() ## for some reason this is really necessary
            os.system("mv {cardfile}_new {cardfile}".format(cardfile=cardfile))

    
    ## remove all the POIs that we want to fix
    fixedPOIs = []
    for poi in POIs:
        if 'right' in poi and any('Ybin_'+str(i) in poi for i in fixedYBins[charge+'R']):
            fixedPOIs.append(poi)
        if 'left'  in poi and any('Ybin_'+str(i) in poi for i in fixedYBins[charge+'L']):
            fixedPOIs.append(poi)
    floatPOIs = list(poi for poi in POIs if not poi in fixedPOIs)
    allPOIs = fixedPOIs+floatPOIs

    ## define the combine POIs, i.e. the subset on which to run MINOS
    minosPOIs = allPOIs if not options.POIsToMinos else options.POIsToMinos.split(',')

    ## make a group for the fixed rate parameters. just append it to the file.
    print 'adding a nuisance group for the fixed rateParams'
    with open(cardfile,'a+') as finalCardfile:
        finalCardfile.write('\nfixedY group = {fixed} '.format(fixed=' '.join(i.strip() for i in fixedPOIs)))
        finalCardfile.write('\nfixedMcErr group = {fixed} '.format(fixed=' '.join(i.strip().replace('norm','eff_unc') for i in fixedPOIs))) # not used in the command, but may be useful to stabilize the fit
        finalCardfile.write('\n\n## end of file')
    #finalCardfile.close()

    print "merged datacard in ",cardfile
    
    #ws = "%s_ws.root" % options.bin
    ws = cardfile.replace('_card.txt', '_ws.root')
    txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal --X-no-check-norm '.format(cf=cardfile, ws=ws)
    print txt2wsCmd
    os.system(txt2wsCmd)
        
    combineCmd = 'combine {ws} -M MultiDimFit    -t -1 --expectSignal=1 -m 999 --saveFitResult --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1       --redefineSignalPOIs {pois}            --floatOtherPOIs=0 --freezeNuisanceGroups efficiencies,fixedY{pdfs} -v 9'.format(ws=ws, pois=','.join(minosPOIs), pdfs=(',pdfs' if len(pdfsyst) else ''))
    print combineCmd

