#!/bin/env python

# usage: ./mergeCardComponents.py -b Wmu -C minus,plus -i ../cards/helicity_xxxxx/
# fit scaling by eff: ./mergeCardComponentsAbsY.py [-m] -b Wel -C minus,plus -i cards/ --sf eff_el_PFMT40.root 

import ROOT
import sys,os,re,json, copy

def getXsecs(processes, systs, ybins, lumi, infile):
    histo_file = ROOT.TFile(infile, 'READ')

    hists = []

    for process in processes:
        pol = 'left' if 'left' in process else 'right' if 'right' in process else 'long'

        cen_name = 'w'+charge+'_wy_central_W' +charge+'_'+pol
        cen_hist = histo_file.Get(cen_name)

        ybinnumber = int(process.split('_')[-1])
        yfirst = ybins[pol][ybinnumber]
        ylast  = ybins[pol][ybinnumber+1]

        # before searching the bin, sum epsilon to the y value being inspected
        # Root assigns the lower bin edge to the bin, while the upper bin edge is assigned to the adjacent bin. However, depending on the number y being used,
        # there can be a precision issue which might induce the selection of the wrong bin (since yfirst and yvalue are actually bin boundaries)
        # It seems odd, but I noticed that with the fake rate graphs (I was getting events migrating between adjacent eta bins)
        epsilon = 0.00001
        istart = cen_hist.FindBin(yfirst + epsilon)
        iend   = cen_hist.FindBin(ylast + epsilon)

        ncen = cen_hist .Integral(istart, iend-1)

        tmp_hist = ROOT.TH1F('x_'+process,'x_'+process, 1, 0., 1.)
        ## normalize back to cross section
        tmp_hist.SetBinContent(1, ncen/lumi)

        hists.append(copy.deepcopy(tmp_hist))

        for sys in systs:

            upn = sys+'Up' if not 'pdf' in sys else sys
            dnn = sys+'Dn' if not 'pdf' in sys else sys

            sys_upname = 'w'+charge+'_wy_'+upn+'_W'+charge+'_'+pol
            sys_dnname = 'w'+charge+'_wy_'+dnn+'_W'+charge+'_'+pol

            sys_up_hist = histo_file.Get(sys_upname)
            sys_dn_hist = histo_file.Get(sys_dnname)

            nup = sys_up_hist .Integral(istart, iend-1)
            ndn = sys_dn_hist .Integral(istart, iend-1)

            if 'pdf' in sys:
                ndn = 2.*ncen-nup ## or ncen/nup?

            tmp_hist_up = ROOT.TH1F('x_'+process+'_'+sys+'Up','x_'+process+'_'+sys+'Up', 1, 0., 1.)
            tmp_hist_up.SetBinContent(1, nup/lumi)
            tmp_hist_dn = ROOT.TH1F('x_'+process+'_'+sys+'Down','x_'+process+'_'+sys+'Dn', 1, 0., 1.)
            tmp_hist_dn.SetBinContent(1, ndn/lumi)
            hists.append(copy.deepcopy(tmp_hist_up))
            hists.append(copy.deepcopy(tmp_hist_dn))

    hist_data = ROOT.TH1F('x_data_obs', 'x_data_obs', 1, 0., 1.)
    hist_data.SetBinContent(1, 1.)
    hists.append(copy.deepcopy(hist_data))

    return hists


def mirrorShape(nominal,alternate,newname,alternateShapeOnly=False):
    alternate.SetName("%sUp" % newname)
    if alternateShapeOnly:
        alternate.Scale(nominal.Integral()/alternate.Integral())
    mirror = nominal.Clone("%sDown" % newname)
    for b in xrange(1,nominal.GetNbinsX()+1):
        y0 = nominal.GetBinContent(b)
        yA = alternate.GetBinContent(b)
        yM = y0
        if yA != 0:
            yM = y0*y0/yA
        elif yA == 0:
            yM = 0
        mirror.SetBinContent(b, yM)
    if alternateShapeOnly:
        # keep same normalization
        mirror.Scale(nominal.Integral()/mirror.Integral())
    return (alternate,mirror)

if __name__ == "__main__":
    

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] cards/card*.txt')
    parser.add_option('-m','--merge-root', dest='mergeRoot', default=False, action='store_true', help='Merge the root files with the inputs also')
    parser.add_option('-i','--input', dest='inputdir', default='', type='string', help='input directory with all the cards inside')
    parser.add_option('-b','--bin', dest='bin', default='ch1', type='string', help='name of the bin')
    parser.add_option('-C','--charge', dest='charge', default='plus,minus', type='string', help='process given charge. default is both')
    parser.add_option(     '--fix-YBins', dest='fixYBins', type='string', default='plusR=99;plusL=99;minusR=99;minusL=99', help='add here replacement of default rate-fixing. with format plusR=10,11,12;plusL=11,12;minusR=10,11,12;minusL=10,11 ')
    parser.add_option('-p','--POIs', dest='POIsToMinos', type='string', default=None, help='Decide which are the nuiscances for which to run MINOS (a.k.a. POIs). Default is all non fixed YBins. With format poi1,poi2 ')
    parser.add_option('--fp', '--freezePOIs'    , dest='freezePOIs'    , action='store_true'               , help='run tensorflow with --freezePOIs (for the pdf only fit)');
    parser.add_option('-l','--long-lnN', dest='longLnN', type='float', default=None, help='add a common lnN constraint to all longitudinal components')
    parser.add_option(     '--sf'    , dest='scaleFile'    , default='', type='string', help='path of file with the scaling/unfolding')
    parser.add_option(     '--lumiLnN'    , dest='lumiLnN'    , default=0.026, type='float', help='Log-uniform constraint to be added to all the fixed MC processes')
    parser.add_option(     '--wXsecLnN'   , dest='wLnN'       , default=0.038, type='float', help='Log-normal constraint to be added to all the fixed W processes')
    parser.add_option(     '--pdf-shape-only'   , dest='pdfShapeOnly' , default=False, action='store_true', help='Normalize the mirroring of the pdfs to central rate.')
    parser.add_option('-M','--minimizer'   , dest='minimizer' , type='string', default='GSLMultiMinMod', help='Minimizer to be used for the fit')
    parser.add_option(     '--comb'   , dest='combineCharges' , default=False, action='store_true', help='Combine W+ and W-, if single cards are done')
    (options, args) = parser.parse_args()
    
    from symmetrizeMatrixAbsY import getScales
    
    charges = options.charge.split(',')
    channel = 'mu' if 'mu' in options.bin else 'el'
    
    ## look for the maximum ybin bin number in each charge/helicity state
    binningFile = open(options.inputdir+'/binningYW.txt')
    binningYW = eval(binningFile.read())
    nbins = {}
    for i,j in binningYW.items():
        nbins[i] = len(j)-1
       
    ## we have the last bin constructed in a way that it has ~5k events.
    fixedYBins = {'plusR' : [nbins['plus_right' ]],
                  'plusL' : [nbins['plus_left'  ]],
                  'minusR': [nbins['minus_right']],
                  'minusL': [nbins['minus_left' ]],
                 }
    
    if options.fixYBins:
        splitted = options.fixYBins.split(';')
        for comp in splitted:
            chhel = comp.split('=')[0]
            bins  = comp.split('=')[1]
            fixedYBins[chhel] = list(int(i) for i in bins.split(','))
    print 'I WILL FIX THESE BINS IN THE FIT:'
    print fixedYBins
    print '---------------------------------'
    
    
    for charge in charges:
    
        outfile  = os.path.join(options.inputdir,options.bin+'_{ch}_shapes.root'.format(ch=charge))
        cardfile = os.path.join(options.inputdir,options.bin+'_{ch}_card.txt'   .format(ch=charge))
    
        ## prepare the relevant files. only the datacards and the correct charge
        files = ( f for f in os.listdir(options.inputdir) if f.endswith('.card.txt') )
        files = ( f for f in files if charge in f and not re.match('.*_pdf.*|.*_muR.*|.*_muF.*|.*alphaS.*|.*wptSlope.*',f) )
        files = sorted(files, key = lambda x: int(x.rstrip('.card.txt').split('_')[-1]) if not any(bkg in x for bkg in ['bkg','Z_']) else -1) ## ugly but works
        files = list( ( os.path.join(options.inputdir, f) for f in files ) )
        
        existing_bins = {'left': [], 'right': [], 'long': []}
        empty_bins = {'left': [], 'right': [], 'long': []}
    
    
        ybins = {}
        for pol in ['left','right','long']:
            cp = '{ch}_{pol}'.format(ch=charge,pol=pol)
            ybins[pol] = binningYW[cp]

            ## for b in xrange(len(ybins[pol])-1):
            ##     if b not in existing_bins[pol]:
            ##         if b not in empty_bins[pol]:
            ##             empty_bins[pol].append(b)
            ##             empty_bins[pol].append(nbins[cp]+1-b)
    
        longBKG = False
        tmpfiles = []
        for ifile,f in enumerate(files):
            basename = os.path.basename(f).split('.')[0]
            if basename.startswith('W{charge}'.format(charge=charge)): pol=basename.split('_')[1]
            else: pol='none' # bkg and data
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
                    rootfiles_syst = filter(lambda x: re.match('{base}_sig_(pdf\d+|muR\S+|muF\S+|alphaS\S+|wptSlope\S+)\.input\.root'.format(base=basename),x), os.listdir(options.inputdir))
                    if ifile==0:
                        rootfiles_syst += filter(lambda x: re.match('Z_{channel}_{charge}_dy_(pdf\d+|muR\S+|muF\S+|alphaS\S+\S+)\.input\.root'.format(channel=channel,charge=charge),x), os.listdir(options.inputdir))
                    rootfiles_syst = [dir+'/'+x for x in rootfiles_syst]
                    rootfiles_syst.sort()
                    if re.match('process\s+',l): 
                        if len(l.split()) > 1 and all(n.isdigit() for n in l.split()[1:]) : continue
                        if not pol in l:
                            if pol!='none' and binn not in empty_bins[pol]: 
                                if binn >= 0:
                                    empty_bins[pol].append(binn)
                                    empty_bins[pol].append(nbins[charge+'_'+pol]-binn)
                            isEmpty = True
                        processes = l.split()[1:]
                    if re.match('process\s+W.*long',l) and 'bkg' in f:
                        print "===> W long is treated as a background"
                        longBKG = True
            if options.mergeRoot:
                if pol=='none' or binn not in empty_bins[pol]:
                    print 'processing bin: {bin} for polarization: {pol}'.format(bin=bin,pol=pol)
                    nominals = {}
                    for irf,rf in enumerate([rootfile]+rootfiles_syst):
                        print '\twith nominal/systematic file: ',rf
                        tf = ROOT.TFile.Open(rf)
                        tmpfile = os.path.join(options.inputdir,'tmp_{pol}_{bin}_sys{sys}.root'.format(pol=pol,bin=bin,sys=irf))
                        of=ROOT.TFile(tmpfile,'recreate')
                        tmpfiles.append(tmpfile)
                        # remove the duplicates also
                        plots = {}
                        for e in tf.GetListOfKeys() :
                            name=e.GetName()
                            obj=e.ReadObj()
                            if name.endswith('data_obs') and 'data' not in basename: continue
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
                                        if 'pdf' in newname: # these changes by default shape and normalization. Each variation should be symmetrized wrt nominal
                                            tokens = newname.split("_"); pfx = '_'.join(tokens[:-2]); pdf = tokens[-1]
                                            ipdf = int(pdf.split('pdf')[-1])
                                            newname = "{pfx}_pdf{ipdf}".format(pfx=pfx,ipdf=ipdf)
                                            (alternate,mirror) = mirrorShape(nominals[pfx],obj,newname,options.pdfShapeOnly)
                                            for alt in [alternate,mirror]:
                                                if alt.GetName() not in plots:
                                                    plots[alt.GetName()] = alt.Clone()
                                                    plots[alt.GetName()].Write()
                                        elif re.match('.*_muR.*|.*_muF.*|.*alphaS.*|.*wptSlope.*',newname): # these changes by default shape and normalization
                                            tokens = newname.split("_"); pfx = '_'.join(tokens[:-2]); syst = tokens[-1].replace('Dn','Down')
                                            newname = "{pfx}_{syst}".format(pfx=pfx,syst=syst)
                                            if 'wptSlope' in newname: # this needs to be scaled not to change normalization
                                                obj.Scale(nominals[pfx].Integral()/obj.Integral())
                                            if newname not in plots:
                                                plots[newname] = obj.Clone(newname)
                                                plots[newname].Write()
                        of.Close()
        if any(len(empty_bins[pol]) for pol in ['left','right']):
            print 'found a bunch of empty bins:', empty_bins
        if options.mergeRoot:
            haddcmd = 'hadd -f {of} {indir}/tmp_*.root'.format(of=outfile, indir=options.inputdir )
            #print 'would run this now: ', haddcmd
            #sys.exit()
            os.system(haddcmd)
            os.system('rm {indir}/tmp_*.root'.format(indir=options.inputdir))
        
        print "Now trying to get info on theory uncertainties..."
        theosyst = {}
        tf = ROOT.TFile.Open(outfile)
        for e in tf.GetListOfKeys() :
            name=e.GetName()
            if re.match('.*_pdf.*|.*_muR.*|.*_muF.*|.*alphaS.*|.*wptSlope.*',name):
                if name.endswith("Up"): name = re.sub('Up$','',name)
                if name.endswith("Down"): name = re.sub('Down$','',name)
                syst = name.split('_')[-1]
                binWsyst = '_'.join(name.split('_')[1:-1])
                if syst not in theosyst: theosyst[syst] = [binWsyst]
                else: theosyst[syst].append(binWsyst)
        if len(theosyst): print "Found a bunch of theoretical sysematics: ",theosyst.keys()
        else: print "You are running w/o theory systematics. Lucky you!"
        pdfsyst = {k:v for k,v in theosyst.iteritems() if 'pdf' in k}
        qcdsyst = {k:v for k,v in theosyst.iteritems() if 'muR' in k or 'muF' in k}
        alssyst = {k:v for k,v in theosyst.iteritems() if 'alphaS' in k }
        wptsyst = {k:v for k,v in theosyst.iteritems() if 'wptSlope' in k}
    
        combineCmd="combineCards.py "
        for f in files:
            basename = os.path.basename(f).split(".")[0]
            binn = int(basename.split('_')[-1]) if 'Ybin_' in basename else 999
            binname = ''
            if re.match('Wplus|Wminus',basename): binname=basename
            elif re.match('Z.*{charge}'.format(charge=charge),basename): binname='Z'
            else: binname='other'
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
                        #combinedCard.write('process        %s \n' % ' '.join([kpatt % p for p in realprocesses]))
                        ## marc combinedCard.write('process        %s \n' % ' '.join([kpatt % str(i+1) for i in xrange(len(pseudobins))]))
                        procids = []; procnames = []
                        pos = 1; neg =  0;
                        for i,proc in enumerate(realprocesses):
                            if 'Ybin' in proc:
                                procnames.append(proc)
                                procids.append( str(neg)); neg -= 1
                            else:
                                procnames.append(proc)
                                procids.append( str(pos)); pos += 1
                        processNameLine = 'process        '
                        processIDLine   = 'process        '
                        for i,pid in enumerate(procids):
                            processNameLine += '       '+procnames[i]
                            processIDLine   += '       '+pid
                        processNameLine += ' \n'
                        processIDLine   += ' \n'
                        combinedCard.write(processNameLine)
                        combinedCard.write(processIDLine  )
    
                    nmatchprocess += 1
                if nmatchprocess==2: 
                    nmatchprocess +=1
                elif nmatchprocess>2: combinedCard.write(l)
        
        os.system('rm {tmpcard}'.format(tmpcard=tmpcard))
        
        kpatt = " %7s "
        if options.longLnN:
            combinedCard.write('norm_long_'+options.bin+'       lnN    ' + ' '.join([kpatt % (options.longLnN if 'long' in x else '-') for x in realprocesses])+'\n')
    
        combinedCard = open(cardfile,'r')
        procs = []
        rates = []
        for l in combinedCard.readlines():
            ##if re.match("process\s+",l) and not re.match("process\s+\d",l): # my regexp qualities are bad... 
            if 'process' in l and 'Ybin' in l:
                procs = (l.rstrip().split())[1:]
            if re.match("rate\s+",l):
                rates = (l.rstrip().split())[1:]
            if len(procs) and len(rates): break
        ProcsAndRates = zip(procs,rates)
        ProcsAndRatesDict = dict(zip(procs,rates))
    
        efficiencies    = {}; efferrors    = {}
        efficiencies_LO = {}; efferrors_LO = {}
        if options.scaleFile:
            for pol in ['left','right']: 
                efficiencies   [pol] = [1./x for x in getScales(ybins[pol], charge, pol, os.path.abspath(options.scaleFile))]
                efferrors      [pol] = [   x for x in getScales(ybins[pol], charge, pol, os.path.abspath(options.scaleFile), returnError=True)] ## these errors are relative to the effs
                efficiencies_LO[pol] = [1./x for x in getScales(ybins[pol], charge, pol, os.path.abspath(options.scaleFile), doNLO=False)]
                efferrors_LO   [pol] = [   x for x in getScales(ybins[pol], charge, pol, os.path.abspath(options.scaleFile), doNLO=False, returnError=True)]
        combinedCard.close()

        combinedCard = open(cardfile,'a')
        POIs = []; fixedPOIs = []; allPOIs = []
        signal_procs = filter(lambda x: re.match('Wplus|Wminus',x), realprocesses)
        if longBKG: signal_procs = filter(lambda x: re.match('(?!Wplus_long|Wminus_long)',x), signal_procs)
        signal_procs.sort(key=lambda x: int(x.split('_')[-1]))
        signal_L = filter(lambda x: re.match('.*left.*',x),signal_procs)
        signal_R = filter(lambda x: re.match('.*right.*',x),signal_procs)
        signal_0 = filter(lambda x: re.match('.*long.*',x),signal_procs)
        
        hel_to_constrain = [signal_L,signal_R]
        tightConstraint = 0.50
        for hel in hel_to_constrain:
            for iy,helbin in enumerate(hel):
                pol = helbin.split('_')[1]
                index_procs = procs.index(helbin)
                if options.scaleFile:
                    lns = ' - '.join('' for i in range(index_procs+1))
                    lns += ' {effunc:.4f} '.format(effunc=1.+efferrors[pol][iy])
                    lns += ' - '.join('' for i in range(len(procs) - index_procs))
                    combinedCard.write('eff_unc_{hb}    lnN {lns}\n'.format(hb=helbin,lns=lns))
        for hel in hel_to_constrain:
            for iy,helbin in enumerate(hel):
                sfx = str(iy)
                pol = helbin.split('_')[1]
                rateNuis = tightConstraint
                normPOI = '{norm}_{n}'.format(norm='norm' if options.scaleFile else 'r', n=helbin)

                ## if we fit absolute rates, we need to get them from the process and plug them in below
                ## if we want to fit with the efficiency gen-reco, we need to add one efficiency parameter
                if options.scaleFile:
                    tmp_eff = efficiencies[pol][iy]
                    combinedCard.write('eff_{n}    rateParam * {n} \t {eff:.5f} [{dn:.5f},{up:.5f}]\n'.format(n=helbin,eff=tmp_eff,dn=(1-1E-04)*tmp_eff,up=(1+1E-04)*tmp_eff))
                    expRate0 = float(ProcsAndRatesDict[helbin])/tmp_eff
                    param_range_0 = '{r:15.1f} [{dn:.1f},{up:.1f}]'.format(r=expRate0,dn=(1-rateNuis)*expRate0,up=(1+rateNuis)*expRate0)
                    # remove the channel to allow ele/mu combination when fitting for GEN
                    helbin_nochan = helbin.replace('_{channel}_Ybin'.format(channel=channel),'_Ybin')
                    combinedCard.write('norm_{nc}  rateParam * {n} \t {pr}\n'.format(nc=helbin_nochan,n=helbin,pr=param_range_0))
                POIs.append(normPOI)
        combinedCard.close()

        ### Now write the final datacard
        combinedCardNew = open(cardfile+"_new",'w')
        combinedCard = open(cardfile,'r')

        ProcsAndRatesUnity = [] # used in case of scaling to GEN
        for (p,r) in ProcsAndRates:
            ProcsAndRatesUnity.append((p,'1') if ('left' in p or 'right' in p or 'long' in p) else (p,r))
        Wlong = [(p,r) for (p,r) in ProcsAndRates if re.match('W.*long',p)]
        WLeftOrRight = [(p,r) for (p,r) in ProcsAndRates if ('left' in p or 'right' in p)]

        for l in combinedCard.readlines():
            if re.match("rate\s+",l):
                if options.scaleFile: combinedCardNew.write('rate            %s \n' % ' '.join([kpatt % r for (p,r) in ProcsAndRatesUnity])+'\n')
                else: combinedCardNew.write('rate            %s \n' % ' '.join([kpatt % '-1' for (p,r) in ProcsAndRates])+'\n')
            else: combinedCardNew.write(l)
        if options.scaleFile:
            eff_long = 1./getScales([ybins['left'][0],ybins['left'][-1]], charge, 'long', options.scaleFile)[0] # just take the eff on the total Y acceptance (should be 0,6)
            eff_left = 1./getScales([ybins[pol][0],ybins[pol][-1]], charge, 'left', options.scaleFile)[0]
            eff_right = 1./getScales([ybins[pol][0],ybins[pol][-1]], charge, 'right', options.scaleFile)[0]
            normWLong = sum([float(r) for (p,r) in Wlong])/eff_long # there should be only 1 Wlong/charge
            normWLeft = sum([float(r) for (p,r) in WLeftOrRight if 'left' in p])/eff_left
            normWRight = sum([float(r) for (p,r) in WLeftOrRight if 'right' in p])/eff_right
            combinedCardNew.write("eff_{nc}   rateParam * {n}    {eff:.5f} [{dn:.5f},{up:.5f}]\n".format(nc=Wlong[0][0].replace('_long','_%s_long' % channel),n=Wlong[0][0],
                                                                                                         eff=eff_long,dn=(1-1E-04)*eff_long,up=(1+1E-04)*eff_long))
            ## write the long yield here
            nl = normWLong; tc = tightConstraint
            combinedCardNew.write("norm_{n} rateParam * {n} {r:15.1f} [{dn:.1f},{up:.1f}]\n".format(n=Wlong[0][0],r=nl,dn=(1-tc)*nl,up=(1+tc)*nl))
            POIs.append('norm_{n}'.format(n=Wlong[0][0].replace('_long','_%s_long' % channel))) # at this stage, norm POIs have still the channel inside
        else:
            pass
            # POIs.append('r_{n}'.format(n=Wlong[0][0].replace('_long','_%s_long' % channel)))
    
        if options.scaleFile: ## make an efficiency nuisance group
            combinedCardNew.write('\nefficiencies group = '+' '.join([p.replace('norm','eff') for p in POIs])+'\n\n' )

        ## remove all the POIs that we want to fix
        # remove the channel to allow ele/mu combination when fitting for GEN
        POIs = [poi.replace('_{channel}_'.format(channel=channel),'_') for poi in  POIs]
        for poi in POIs:
            if 'right' in poi and any('Ybin_'+str(i) in poi for i in fixedYBins[charge+'R']):
                fixedPOIs.append(poi)
            if 'left'  in poi and any('Ybin_'+str(i) in poi for i in fixedYBins[charge+'L']):
                fixedPOIs.append(poi)
        floatPOIs = list(poi for poi in POIs if not poi in fixedPOIs)
        allPOIs = fixedPOIs+floatPOIs
        ## define the combine POIs, i.e. the subset on which to run MINOS
        minosPOIs = allPOIs if not options.POIsToMinos else options.POIsToMinos.split(',')

        ## make a group for the fixed rate parameters. ## this is maybe obsolete, and restricted only to absolute rate fitting
        if options.scaleFile:
            print 'adding a nuisance group for the fixed rateParams'
            if len(fixedPOIs): combinedCardNew.write('\nfixedY group = {fixed} '.format(fixed=' '.join(i.strip() for i in fixedPOIs)))
            combinedCardNew.write('\nallY group = {all} \n'.format(all=' '.join([i for i in allPOIs])))
        combinedCardNew.close() ## for some reason this is really necessary
        os.system("mv {cardfile}_new {cardfile}".format(cardfile=cardfile))
        
        combinedCard = open(cardfile,'a+')
        ## add the PDF systematics 
        for sys,procs in theosyst.iteritems():
            # there should be 2 occurrences of the same proc in procs (Up/Down). This check should be useless if all the syst jobs are DONE
            combinedCard.write('%-15s   shape %s\n' % (sys,(" ".join(['1.0' if p in procs and procs.count(p)==2 else '  -  ' for p,r in ProcsAndRates]))) )
        combinedCard.write('\npdfs group = '+' '.join([sys for sys,procs in pdfsyst.iteritems()])+'\n')
        combinedCard.write('\nscales group = '+' '.join([sys for sys,procs in qcdsyst.iteritems()])+'\n')
        combinedCard.write('\nalphaS group = '+' '.join([sys for sys,procs in alssyst.iteritems()])+'\n')
        combinedCard.write('\nwpt group = '+' '.join([sys for sys,procs in wptsyst.iteritems()])+'\n')

        ## now assign a uniform luminosity uncertainty to all the MC processes
        # combinedCard.write('\nCMS_lumi_13TeV   lnN %s\n' % (" ".join(['-' if 'data' in p else '%.3f'%(1+options.lumiLnN) for p,r in ProcsAndRates])) )
        ## not needed as  far as we float all the Y bins
        # combinedCard.write('CMS_W   lnN %s\n' % (" ".join(['%.3f' % (1+options.wLnN) if (p=='TauDecaysW' or re.match('W{charge}'.format(charge=charge),p)) else '-' for p,r in ProcsAndRates])) )
        combinedCard.close() 

            
        ## here we make a second datacard that will be masked. which for every process
        ## has a 1-bin histogram with the cross section for every nuisance parameter and
        ## every signal process inside

        ## first make a list of all the signal processes. this excludes the long!!!!
        tmp_sigprocs = [p for p in realprocesses if 'Wminus' in p or 'Wplus' in p]
        ## long now signal tmp_sigprocs = [p for p in tmp_sigprocs if not 'long' in p]

        ## xsecfilname 
        hists = getXsecs(tmp_sigprocs, 
                         [i for i in theosyst.keys() if not 'wpt' in i],
                         ybins, 
                         36000., 
                         '/afs/cern.ch/work/m/mdunser/public/cmssw/w-helicity-13TeV/CMSSW_8_0_25/src/CMGTools/WMass/data/theory/theory_cross_sections.root' ## hard coded for now
                        )
        tmp_xsec_histfile_name = os.path.abspath(outfile.replace('_shapes','_shapes_xsec'))
        tmp_xsec_hists = ROOT.TFile(tmp_xsec_histfile_name, 'recreate')
        for hist in hists:
            hist.Write()
        tmp_xsec_hists.Close()

        tmp_xsec_dc_name = os.path.join(options.inputdir,options.bin+'_{ch}_xsec_card.txt'   .format(ch=charge))
        tmp_xsec_dc = open(tmp_xsec_dc_name, 'w')
        tmp_xsec_dc.write("imax 1\n")
        tmp_xsec_dc.write("jmax *\n")
        tmp_xsec_dc.write("kmax *\n")
        tmp_xsec_dc.write('##----------------------------------\n') 
        tmp_xsec_dc.write("shapes *  *  %s %s\n" % (tmp_xsec_histfile_name, 'x_$PROCESS x_$PROCESS_$SYSTEMATIC'))
        tmp_xsec_dc.write('##----------------------------------\n')
        tmp_xsec_dc.write('bin {b}\n'.format(b=options.bin))
        tmp_xsec_dc.write('observation -1\n') ## don't know if that will work...
        tmp_xsec_dc.write('bin      {s}\n'.format(s=' '.join(['{b}'.format(b=options.bin) for p in tmp_sigprocs])))
        tmp_xsec_dc.write('process  {s}\n'.format(s=' '.join([p for p in tmp_sigprocs])))
        ###tmp_xsec_dc.write('process  {s}\n'.format(s=' '.join(str(i+1)  for i in range(len(tmp_sigprocs)))))
        tmp_xsec_dc.write('process  {s}\n'.format(s=' '.join(procids[procnames.index(pname)]  for pname in tmp_sigprocs)))
        tmp_xsec_dc.write('rate     {s}\n'.format(s=' '.join('-1' for i in range(len(tmp_sigprocs)))))
        tmp_xsec_dc.write('# --------------------------------------------------------------\n')

        for sys,procs in theosyst.iteritems():
            if 'wpt' in sys: continue
            # there should be 2 occurrences of the same proc in procs (Up/Down). This check should be useless if all the syst jobs are DONE
            tmp_xsec_dc.write('%-15s   shape %s\n' % (sys,(" ".join(['1.0' if p in tmp_sigprocs  else '  -  ' for p in tmp_sigprocs]))) )

        tmp_xsec_dc.close()

        ## end of all the xsec construction of datacard and making the file

        ## command to make the workspace. should be done after combineCards.py!
        ## os.system('text2workspace.py --X-allow-no-signal -o {ws} {dc}'.format(ws=tmp_xsec_dc_name.replace('_card','_ws'), dc=tmp_xsec_dc_name))

        print "merged datacard in ",cardfile
        
        ws = cardfile.replace('_card.txt', '_ws.root')
        minimizerOpts = ' --cminDefaultMinimizerType '+options.minimizer
        if options.minimizer.startswith('GSLMultiMin'): # default is Mod version by Josh
            minimizerOpts += ' --cminDefaultMinimizerAlgo BFGS2 --cminDefaultMinimizerTolerance=0.001 --keepFailures '
        else: 
            minimizerOpts += ' --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1 '
        if options.scaleFile:
            txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal --X-no-check-norm '.format(cf=cardfile, ws=ws)
            combineCmd = 'combine {ws} -M MultiDimFit -t -1 -m 999 --saveFitResult {minOpts} --redefineSignalPOIs {pois} --floatOtherPOIs=0 --freezeNuisanceGroups efficiencies,fixedY{pdfs}{scales}{alphas} -v 9'.format(ws=ws, pois=','.join(minosPOIs), pdfs=(',pdfs' if len(pdfsyst) else ''), scales=(',scales' if len(qcdsyst) else ''),alphas=(',alphaS' if len(alssyst) else ''),minOpts=minimizerOpts)
        else: 
            signals = ['W{charge}_{pol}_W{charge}_{pol}_{channel}_Ybin_{yb}'.format(charge=charge,pol=pol,channel=channel,yb=yb) for pol in ['left','right'] for yb in xrange(len(ybins[pol])-1) ]
            signals += ['W{charge}_long'.format(charge=charge)]
            multisig      = ' '.join(["--PO 'map=.*/{proc}$:r_{proc_nochan}[1,0,10]'".format(proc=proc,proc_nochan=proc.replace('_{channel}_'.format(channel=channel),'_')) for proc in signals])

            cardfile_xsec = cardfile.replace('_card', '_card_withXsecMask')
            chname = options.bin+'_{ch}'.format(ch=charge)
            chname_xsec = chname+'_xsec'
            ccCmd = 'combineCards.py {oc}={odc} {xc}={xdc} > {out}'.format(oc=chname,odc=cardfile,xc=chname_xsec,xdc=tmp_xsec_dc_name,out=cardfile_xsec)

            newws = cardfile_xsec.replace('_card','_ws').replace('.txt','.root')

            txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-background --X-no-check-norm -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose {pos} --channel-masks '.format(cf=cardfile_xsec, ws=newws, pos=multisig)
            txt2wsCmd_noXsec = 'text2workspace.py {cf} -o {ws} --X-no-check-norm -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose {pos} '.format(cf=cardfile, ws=ws, pos=multisig)
            txt2tfCmd = 'text2tf.py --maskedChan {maskch} --X-allow-no-background {cf}'.format(maskch=chname_xsec,cf=cardfile_xsec)
            if options.freezePOIs:
                txt2tfCmd += ' --POIMode none '

            #combineCmd = 'combine {ws} -M MultiDimFit    -t -1 -m 999 --saveFitResult --keepFailures --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1       --redefineSignalPOIs {pois} --floatOtherPOIs=0 -v 9'.format(ws=ws, pois=','.join(['r_'+p for p in signals]))
            combineCmd = 'combine {ws} -M MultiDimFit -t -1 -m 999 --saveFitResult {minOpts} --redefineSignalPOIs {pois} -v 9 --setParameters mask_{xc}=1 '.format(ws=newws, pois=','.join(['r_'+p for p in signals]),minOpts=minimizerOpts, xc=chname_xsec)
        ## here running the combine cards command first
        print ccCmd
        os.system(ccCmd)
        ## then running the t2w command afterwards
        print txt2wsCmd
        print '-- will NOT run text2workspace -----------------------'
        #os.system(txt2wsCmd)
        print "NOT doing the noXsec workspace..."
        #os.system(txt2wsCmd_noXsec)
        print '-- will run text2tf ---------------------'
        os.system(txt2tfCmd)
        ## print out the command to run in combine
        print combineCmd
    # end of loop over charges

    datacards = [os.path.abspath(options.inputdir)+"/"+options.bin+'_{ch}_card.txt'.format(ch=charge) for charge in ['plus','minus']]
    if options.combineCharges and sum([os.path.exists(card) for card in datacards])==2:
        print "Cards for W+ and W- done. Combining them now..."
        combinedCard = os.path.abspath(options.inputdir)+"/"+options.bin+'_card.txt'
        combineCards = 'combineCards.py '+' '.join(['{bin}_{ch}={bin}_{ch}_card.txt'.format(bin=options.bin,ch=charge) for charge in ['plus','minus']])+' > '+combinedCard
        print "combining W+ and W- with: ",combineCards
        # go into the input dir to issue the combine command w/o paths not to screw up the paths of the shapes in the cards
        os.system('cd {inputdir}; {cmd}; cd -'.format(inputdir=os.path.abspath(options.inputdir),cmd=combineCards))
      
        ws = combinedCard.replace('_card.txt', '_ws.root')
        t2w = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal --X-no-check-norm '.format(cf=combinedCard, ws=ws)
        print "combined t2w command: ",t2w
        ## marc os.system(t2w)
        combineCmdTwoCharges = 'combine {ws} -M MultiDimFit    -t -1 --expectSignal=1 -m 999 --saveFitResult --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1       --redefineSignalPOIs {pois}            --floatOtherPOIs=0 --freezeNuisanceGroups efficiencies,fixedY{pdfs}{scales} -v 9'.format(ws=ws, pois=','.join(minosPOIs), pdfs=(',pdfs' if len(pdfsyst) else ''), scales=(',scales' if len(qcdsyst) else ''))
        print combineCmdTwoCharges
        print "DONE. ENJOY FITTING !"
