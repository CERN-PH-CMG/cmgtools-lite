#!/bin/env python

# python w-helicity-13TeV/mergeCardComponentsDiffXsec.py -i cards/diffXsec_2018_05_24_diffXsec_GenPtEtaSigBin/ -b Wel -C plus -p CMS_We_flips -m

####################
###################
# TO BE UPDATED
##################
##################

import ROOT
import sys,os,re,json,copy

from mergeCardComponentsAbsY import mirrorShape
from make_diff_xsec_cards import getArrayParsingString


def get_ieta_ipt_from_process_name(name):
    tokens = name.split('_')
    for i,tkn in enumerate(tokens):
        #print "%d %s" % (i, tkn)                                                                                                                        
        if tkn == "ieta": ieta = int(tokens[i + 1])
        if tkn == "ipt":  ipt  = int(tokens[i + 1])
    return ieta,ipt

#from mergeCardComponentsAbsY import getXsecs    # for now it is reimplemented here
def getXsecs(processes, systs, etaPtBins, infile):  # in my case here, the histograms already have the cross section in pb, no need to divide by lumi

    # etaPtBins is a list of 4 things: Netabins, etabins, Nptbins,ptbins

    histo_file = ROOT.TFile(infile, 'READ')
    hists = []

    for process in processes:

        cen_name = 'gen_ptl1_etal1_W'+charge+'_el_'  # by mistake, I didn't write central after last _, while variations have the name of the systematic uncertainty
        cen_hist = histo_file.Get(cen_name)  # this is a TH2

        # process has the form: Wplus_el_ieta_3_ipt_0_Wplus_el_group_0, where the number after group is not relevant (does not coincide with absolute bin number)
        # as it can be the same for many processes
        # one should use ieta and ipt, which identifies the template bin (first index is 0, not 1)

        ieta,ipt = get_ieta_ipt_from_process_name(process)
        etabins = etaPtBins[1]
        ptbins = etaPtBins[3]
        etafirst = etabins[ieta]
        etalast  = etabins[ieta+1]
        ptfirst = ptbins[ipt]
        ptlast  = ptbins[ipt+1]

        # before searching the bin, sum epsilon to the y value being inspected
        # Root assigns the lower bin edge to the bin, while the upper bin edge is assigned to the adjacent bin. However, depending on the number y being used,
        # there can be a precision issue which might induce the selection of the wrong bin (since yfirst and yvalue are actually bin boundaries)
        # It seems odd, but I noticed that with the fake rate graphs (I was getting events migrating between adjacent eta bins)
        epsilon = 0.00001
        istart_eta = cen_hist.FindFixBin(etafirst + epsilon)
        iend_eta   = cen_hist.FindFixBin(etalast + epsilon)
        istart_pt  = cen_hist.FindFixBin(ptfirst + epsilon)
        iend_pt    = cen_hist.FindFixBin(ptlast + epsilon)

        ncen = cen_hist.Integral(istart_eta, iend_eta-1, istart_pt,iend_pt-1)

        tmp_hist = ROOT.TH1F('x_'+process,'x_'+process, 1, 0., 1.)
        ## normalize back to cross section
        tmp_hist.SetBinContent(1, ncen)

        hists.append(copy.deepcopy(tmp_hist))

        for sys in systs:

            upn = sys+'Up' if not 'pdf' in sys else sys
            dnn = sys+'Dn' if not 'pdf' in sys else sys

            sys_upname = 'gen_ptl1_etal1_W'+charge+'_el_'+upn
            sys_dnname = 'gen_ptl1_etal1_W'+charge+'_el_'+dnn

            sys_up_hist = histo_file.Get(sys_upname)
            sys_dn_hist = histo_file.Get(sys_dnname)

            nup = sys_up_hist.Integral(istart_eta, iend_eta-1, istart_pt,iend_pt-1)
            ndn = sys_dn_hist.Integral(istart_eta, iend_eta-1, istart_pt,iend_pt-1)

            if 'pdf' in sys:
                ndn = 2.*ncen-nup ## or ncen/nup?

            tmp_hist_up = ROOT.TH1F('x_'+process+'_'+sys+'Up','x_'+process+'_'+sys+'Up', 1, 0., 1.)
            tmp_hist_up.SetBinContent(1, nup)
            tmp_hist_dn = ROOT.TH1F('x_'+process+'_'+sys+'Down','x_'+process+'_'+sys+'Dn', 1, 0., 1.)
            tmp_hist_dn.SetBinContent(1, ndn)
            hists.append(copy.deepcopy(tmp_hist_up))
            hists.append(copy.deepcopy(tmp_hist_dn))

    hist_data = ROOT.TH1F('x_data_obs', 'x_data_obs', 1, 0., 1.)
    hist_data.SetBinContent(1, 1.)
    hists.append(copy.deepcopy(hist_data))

    return hists



if __name__ == "__main__":
    

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options]')
    parser.add_option('-m','--merge-root', dest='mergeRoot', default=False, action='store_true', help='Merge the root files with the inputs also')
    parser.add_option('-i','--input', dest='inputdir', default='', type='string', help='input directory with all the cards inside')
    parser.add_option('-b','--bin', dest='bin', default='ch1', type='string', help='name of the bin')
    parser.add_option('-C','--charge', dest='charge', default='plus,minus', type='string', help='process given charge. default is both')
    # fixYBins not used here
    parser.add_option(     '--fix-YBins', dest='fixYBins', type='string', default='plusR=99;plusL=99;minusR=99;minusL=99', help='add here replacement of default rate-fixing. with format plusR=10,11,12;plusL=11,12;minusR=10,11,12;minusL=10,11 ')
    parser.add_option('-p','--POIs', dest='POIsToMinos', type='string', default=None, help='Decide which are the nuiscances for which to run MINOS (a.k.a. POIs). Default is all non fixed YBins. With format poi1,poi2 ')
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
    Wcharge = ["Wplus","Wminus"]
        
    for charge in charges:
    
        outfile  = os.path.join(options.inputdir,options.bin+'_{ch}_shapes.root'.format(ch=charge))
        cardfile = os.path.join(options.inputdir,options.bin+'_{ch}_card.txt'   .format(ch=charge))
    
        ## prepare the relevant files. only the datacards and the correct charge
        files = ( f for f in os.listdir(options.inputdir) if f.endswith('.card.txt') )
        files = ( f for f in files if charge in f and not re.match('.*_pdf.*|.*_muR.*|.*_muF.*|.*alphaS.*|.*wptSlope.*',f) )
        files = sorted(files, key = lambda x: int(x.rstrip('.card.txt').split('_')[-1]) if not any(bkg in x for bkg in ['bkg','Z_']) else -1) ## ugly but works
        files = list( ( os.path.join(options.inputdir, f) for f in files ) )
        
    
        tmpfiles = []
        for ifile,f in enumerate(files):
            basename = os.path.basename(f).split('.')[0]
            dirf = os.path.dirname(f)
            bin = ''
            isEmpty = False
            with open(f) as thisfile:
                for l in thisfile.readlines():
                    if re.match('shapes.*',l):
                        rootfile = dirf+'/'+l.split()[3]
                    if re.match('bin.*',l):
                        if len(l.split()) < 2: continue ## skip the second bin line if empty
                        bin = l.split()[1]
                        binn = int(bin.split('_')[-1]) if 'group_' in bin else -1
                    rootfiles_syst = filter(lambda x: re.match('{base}_sig_(pdf\d+|muR\S+|muF\S+|alphaS\S+|wptSlope\S+)\.input\.root'.format(base=basename),x), os.listdir(options.inputdir))
                    if ifile==0:
                        rootfiles_syst += filter(lambda x: re.match('Z_{channel}_{charge}_dy_(pdf\d+|muR\S+|muF\S+|alphaS\S+\S+)\.input\.root'.format(channel=channel,charge=charge),x), os.listdir(options.inputdir))
                    rootfiles_syst = [dirf+'/'+x for x in rootfiles_syst]
                    rootfiles_syst.sort()
                    if re.match('process\s+',l): 
                        if len(l.split()) > 1 and all(n.isdigit() for n in l.split()[1:]) : continue
                        processes = l.split()[1:]
 
            if options.mergeRoot:
                print 'processing bin: {bin}'.format(bin=bin)
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
                        if name.endswith('data_obs') and 'data' not in basename: continue
                        if (not re.match('Wplus|Wminus',os.path.basename(f))) and 'data_obs' in name: obj.Clone().Write()
                        for p in processes:
                            if p in name:
                                newprocname = p+'_'+bin if re.match('Wplus|Wminus',p) else p
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
        pdfsyst = {k:v for k,v in theosyst.iteritems() if 'pdf' in k}
        qcdsyst = {k:v for k,v in theosyst.iteritems() if 'muR' in k or 'muF' in k}
        alssyst = {k:v for k,v in theosyst.iteritems() if 'alphaS' in k }
        wptsyst = {k:v for k,v in theosyst.iteritems() if 'wptSlope' in k}
        sortedpdfkeys = sorted(pdfsyst.keys(),key= lambda x: int(x.strip('pdf')))
        sortednonpdfkeys = sorted([x for x in theosyst.keys() if "pdf" not in x]) 
        sortedsystkeys = sortedpdfkeys + sortednonpdfkeys
        if len(theosyst): print "Found a bunch of theoretical systematics: ",sortedsystkeys
        else: print "You are running w/o theory systematics. Lucky you!"

        combineCmd="combineCards.py "
        for f in files:
            basename = os.path.basename(f).split(".")[0]
            binn = int(basename.split('_')[-1]) if 'group_' in basename else -999
            binname = ''
            if re.match('Wplus|Wminus',basename): binname=basename
            elif re.match('Z.*{charge}'.format(charge=charge),basename): binname='Z'
            else: binname='other'
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
        with open(tmpcard) as file_tmpcard:    
            nmatchbin=0
            nmatchprocess=0
            rateWritten=False
            for l in file_tmpcard.readlines():
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
                            # as it was implemented, I think this is always equal to pseudoprocesses[i], because there is no charge in pseudobins
                            # pseudobins is the number of the bin ( <= 0 for signal, > 0 for backgrounds) 
                            realprocesses.append(pseudoprocesses[i]+"_"+pseudobins[i] if any(x in pseudobins[i] for x in Wcharge) else pseudoprocesses[i])
                        combinedCard.write('bin            %s \n' % ' '.join([kpatt % options.bin for p in pseudoprocesses]))
                        combinedCard.write('process        %s \n' % ' '.join([kpatt % p for p in realprocesses]))
                        # going to write the number for the process: negative or 0 for signal, positive for the rest
                        procBin = {}
                        ibkg = 1
                        isig = 0
                        for p in realprocesses:
                            if any(wcharge in p for wcharge in Wcharge):
                                procBin[p] = isig
                                isig += -1 
                            else:
                                procBin[p] = ibkg
                                ibkg += 1
                        #combinedCard.write('process        %s \n' % ' '.join([kpatt % str(i+1) for i in xrange(len(pseudobins))]))
                        combinedCard.write('process        %s \n' % ' '.join([kpatt % procBin[p] for p in realprocesses]))
                    nmatchprocess += 1
                if re.match("rate",l):
                    klen = 7
                    kpatt = " %%%ds "  % klen
                    combinedCard.write('rate        %s \n' % ' '.join([kpatt % "-1" for p in realprocesses]))
                    rateWritten=True
                if nmatchprocess>=2 and rateWritten and not re.match("rate",l):  # when evaluating rate line above, here l is still that one!
                    # copy all the rest after rate from the temporary card
                    combinedCard.write(l)
            # now luminosity uncertainty and CMS_W, in case  they are not in systfile 
            # lumipar = "{0:.3f}".format(1.0 + options.lumiLnN) #"1.026"  # 2.6% 
            # Wxsec   = "{0:.3f}".format(1.0 + options.wLnN)    #"1.038"  # 3.8%
            # combinedCard.write(('%-23s lnN' % "CMS_lumi_13TeV") + ' '.join([kpatt % ("-" if "data" in key else lumipar) for key in realprocesses]) + "\n")
            # not needed because it will be measured
            #combinedCard.write(('%-23s lnN' % "CMS_W") + ' '.join([kpatt % (Wxsec if any(x in key for x in Wcharge) else "-"    ) for key in realprocesses]) + "\n")


        os.system('rm {tmpcard}'.format(tmpcard=tmpcard))
        
        if options.scaleFile: options.absoluteRates = True
        
        kpatt = " %7s "
    
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
    
        combinedCard.close()

        combinedCard = open(cardfile,'a')
        POIs = []; fixedPOIs = []; allPOIs = []
        # following two lines currently not used anywhere
        signal_procs = filter(lambda x: re.match('Wplus|Wminus',x), realprocesses)
        signal_procs.sort(key=lambda x: int(x.split('_')[-1]))
        

        ## add the PDF systematics                                                         
        #for sys,procs in theosyst.iteritems():
        for sys in sortedsystkeys:
            # there should be 2 occurrences of the same proc in procs (Up/Down). This check should be useless if all the syst jobs are DONE                      
            procs = theosyst[sys]
            combinedCard.write('%-15s   shape %s\n' % (sys,(" ".join(['1.0' if p in procs and procs.count(p)==2 else '  -  ' for p,r in ProcsAndRates]))) )
        if len(sortedsystkeys):
            combinedCard.write('\npdfs group = '+' '.join([sys for sys in sortedpdfkeys])+'\n')
            combinedCard.write('\nscales group = '+' '.join([sys for sys,procs in qcdsyst.iteritems()])+'\n')
            combinedCard.write('\nalphaS group = '+' '.join([sys for sys,procs in alssyst.iteritems()])+'\n')
            combinedCard.write('\nwpt group = '+' '.join([sys for sys,procs in wptsyst.iteritems()])+'\n')

        combinedCard.close()


        ## here we make a second datacard that will be masked. which for every process                                               
        ## has a 1-bin histogram with the cross section for every nuisance parameter and                                             
        ## every signal process inside                                                                                               

        ## first make a list of all the signal processes
        tmp_sigprocs = [p for p in realprocesses if 'Wminus' in p or 'Wplus' in p]

        # get eta pt binning
        etaPtBinningFile = options.inputdir + "/binningPtEta.txt"
        with open(etaPtBinningFile) as f:
            content = f.readlines()
        for x in content:
            etaPtBinning = str(x).strip() #if not str(x).startswith("#")                          
        etabinning = etaPtBinning.split('*')[0]    # this is like [a,b,c,...], and is of type string. We nedd to get an array                     
        ptbinning  = etaPtBinning.split('*')[1]
        etabinning = getArrayParsingString(etabinning,makeFloat=True)
        ptbinning  = getArrayParsingString(ptbinning,makeFloat=True)
        binning = [len(etabinning)-1, etabinning, len(ptbinning)-1, ptbinning]
 
        ## xsecfilename                                                                                                                                                    
        hists = getXsecs(tmp_sigprocs,
                         [i for i in sortedsystkeys if not 'wpt' in i],
                         binning,
                         #35.9 if channel == 'mu' else 30.9,  # no need to pas a luminosity, histograms in xsection_genEtaPt.root are already divided by it (xsec in pb)
                         '/afs/cern.ch/user/m/mciprian/public/whelicity_stuff/xsection_genEtaPt.root' ## hard coded for now
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
        ###tmp_xsec_dc.write('process  {s}\n'.format(s=' '.join([str(i+1)  for i in range(len(tmp_sigprocs))]))) 
        tmp_xsec_dc.write('process  {s}\n'.format(s=' '.join([str(procBin[pname])  for pname in tmp_sigprocs])))
        tmp_xsec_dc.write('rate     {s}\n'.format(s=' '.join('-1' for i in range(len(tmp_sigprocs)))))
        tmp_xsec_dc.write('# --------------------------------------------------------------\n')

        # for sys,procs in theosyst.iteritems():          
        for sys in sortedsystkeys:
            if 'wpt' in sys: continue
            # there should be 2 occurrences of the same proc in procs (Up/Down). This check should be useless if all the syst jobs are DONE                      
            tmp_xsec_dc.write('%-15s   shape %s\n' % (sys,(" ".join(['1.0' if p in tmp_sigprocs  else '  -  ' for p in tmp_sigprocs]))) )
        tmp_xsec_dc.close()

        ## end of all the xsec construction of datacard and making the file                                                               


        quit()

########################################
## I arrived until here
########################################
# Following part must be readapted
########################################


        if options.absoluteRates:
            ProcsAndRatesUnity = []
            for (p,r) in ProcsAndRates:
                ProcsAndRatesUnity.append((p,'1') if ('left' in p or 'right' in p or 'long' in p) else (p,r))
    
            combinedCardNew = open(cardfile+"_new",'w')
            combinedCard = open(cardfile,'r')
            for l in combinedCard.readlines():
                if re.match("rate\s+",l):
                    combinedCardNew.write('rate            %s \n' % ' '.join([kpatt % r for (p,r) in ProcsAndRatesUnity])+'\n')
                else: combinedCardNew.write(l)
            Wlong = [(p,r) for (p,r) in ProcsAndRates if re.match('W.*long',p)]
            WLeftOrRight = [(p,r) for (p,r) in ProcsAndRates if ('left' in p or 'right' in p)]
            if options.scaleFile:
                eff_long = 1./getScales([ybins['left'][0],ybins['left'][-1]], charge, 'long', options.scaleFile)[0] # just take the eff on the total Y acceptance (should be 0,6)
                eff_left = 1./getScales([ybins[pol][0],ybins[pol][-1]], charge, 'left', options.scaleFile)[0]
                eff_right = 1./getScales([ybins[pol][0],ybins[pol][-1]], charge, 'right', options.scaleFile)[0]
                normWLong = sum([float(r) for (p,r) in Wlong])/eff_long # there should be only 1 Wlong/charge
                normWLeft = sum([float(r) for (p,r) in WLeftOrRight if 'left' in p])/eff_left
                normWRight = sum([float(r) for (p,r) in WLeftOrRight if 'right' in p])/eff_right
                normWLeftOrRight = normWLeft + normWRight
                combinedCardNew.write("eff_{nc}   rateParam * {n}    {eff:.5f} [{dn:.5f},{up:.5f}]\n".format(nc=Wlong[0][0].replace('_long','_%s_long' % channel),n=Wlong[0][0],
                                                                                                             eff=eff_long,dn=(1-1E-04)*eff_long,up=(1+1E-04)*eff_long))
                ## write the long yield here
                nl = normWLong; tc = tightConstraint
                combinedCardNew.write("norm_{n} rateParam * {n} {r:15.1f} [{dn:.1f},{up:.1f}]\n".format(n=Wlong[0][0],r=nl,dn=(1-tc)*nl,up=(1+tc)*nl))
                POIs.append('norm_{n}'.format(n=Wlong[0][0].replace('_long','_%s_long' % channel))) # at this stage, norm POIs have still the channel inside
    
            ## if we do not scale gen-reco, then we go back to before...
            else:
                normWLong = sum([float(r) for (p,r) in Wlong]) # there should be only 1 Wlong/charge
                normWLeftOrRight = sum([float(r) for (p,r) in WLeftOrRight])
                combinedCardNew.write("norm_%-50s   rateParam * %-5s  %15.1f [%.0f,%.0f]\n" % (Wlong[0][0],Wlong[0][0],normWLong,(1-tightConstraint)*normWLong,(1+tightConstraint)*normWLong))
    
            ## make an efficiency nuisance group
            combinedCardNew.write('\nefficiencies group = '+' '.join([p.replace('norm','eff') for p in POIs])+'\n\n' )
            ## make a group for the fixed rate parameters.
            print 'adding a nuisance group for the fixed rateParams'
            if len(fixedPOIs): combinedCardNew.write('\nfixedY group = {fixed} '.format(fixed=' '.join(i.strip() for i in fixedPOIs)))
            combinedCardNew.write('\nallY group = {all} \n'.format(all=' '.join(i.strip().replace('_%s_'%options.bin,'_') for i in allPOIs)))
            combinedCardNew.close() ## for some reason this is really necessary
            os.system("mv {cardfile}_new {cardfile}".format(cardfile=cardfile))

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
        
            combinedCard = open(cardfile,'a+')
            ## add the PDF systematics 
            for sys,procs in theosyst.iteritems():
                # there should be 2 occurrences of the same proc in procs (Up/Down). This check should be useless if all the syst jobs are DONE
                combinedCard.write('%-15s   shape %s\n' % (sys,(" ".join([kpatt % '1.0' if p in procs and procs.count(p)==2 else '  -  ' for p,r in ProcsAndRates]))) )
            combinedCard.write('\npdfs group = '+' '.join([sys for sys in sortedpdfkeys])+'\n')
            combinedCard.write('\nscales group = '+' '.join([sys for sys,procs in qcdsyst.iteritems()])+'\n')
            combinedCard.write('\nalphaS group = '+' '.join([sys for sys,procs in alssyst.iteritems()])+'\n')
            combinedCard.write('\nwpt group = '+' '.join([sys for sys,procs in wptsyst.iteritems()])+'\n')

            ## now assign a uniform luminosity uncertainty to all the MC processes
            combinedCard.write('\nCMS_lumi_13TeV   lnN %s\n' % (" ".join([kpatt % '-' if 'data' in p else '%.3f'%(1+options.lumiLnN) for p,r in ProcsAndRates])) )
            combinedCard.write('CMS_W   lnN %s\n' % (" ".join([kpatt % '%.3f' % (1+options.wLnN) if (p=='TauDecaysW' or re.match('W{charge}'.format(charge=charge),p)) else '-' for p,r in ProcsAndRates])) )
            combinedCard.close() 

        print "merged datacard in ",cardfile
        
        ws = cardfile.replace('_card.txt', '_ws.root')
        if options.absoluteRates:
            txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal --X-no-check-norm '.format(cf=cardfile, ws=ws)
            combineCmd = 'combine {ws} -M MultiDimFit    -t -1 --expectSignal=1 -m 999 --saveFitResult --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1       --redefineSignalPOIs {pois}            --floatOtherPOIs=0 --freezeNuisanceGroups efficiencies,fixedY{pdfs}{scales}{alphas} -v 9'.format(ws=ws, pois=','.join(minosPOIs), pdfs=(',pdfs' if len(pdfsyst) else ''), scales=(',scales' if len(qcdsyst) else ''),alphas=(',alphaS' if len(alssyst) else ''))
        else: 
            signals = ['W{charge}_{pol}_W{charge}_{pol}_{channel}_Ybin_{yb}'.format(charge=charge,pol=pol,channel=channel,yb=yb) for pol in ['left','right'] for yb in xrange(len(ybins[pol])) ]
            signals += ['W{charge}_long'.format(charge=charge)]
            multisig = ' '.join(["--PO 'map=.*/{proc}$:r_{proc}[1,0,10]'".format(proc=proc) for proc in signals])
            txt2wsCmd = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal --X-no-check-norm -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose {pos}'.format(cf=cardfile, ws=ws, pos=multisig)
            combineCmd = 'combine {ws} -M MultiDimFit    -t -1 -m 999 --saveFitResult --keepFailures --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1       --redefineSignalPOIs {pois} --floatOtherPOIs=0 -v 9'.format(ws=ws, pois=','.join(['r_'+p for p in signals]))
        print txt2wsCmd
        os.system(txt2wsCmd)
        print combineCmd
    # end of loop over charges

    datacards = [os.path.abspath(options.inputdir)+"/"+options.bin+'_{ch}_card.txt'.format(ch=charge) for charge in ['plus','minus']]
    if sum([os.path.exists(card) for card in datacards])==2:
        print "Cards for W+ and W- done. Combining them now..."
        combinedCard = os.path.abspath(options.inputdir)+"/"+options.bin+'_card.txt'
        combineCards = 'combineCards.py '+' '.join(['{bin}_{ch}={bin}_{ch}_card.txt'.format(bin=options.bin,ch=charge) for charge in ['plus','minus']])+' > '+combinedCard
        print "combining W+ and W- with: ",combineCards
        # go into the input dir to issue the combine command w/o paths not to screw up the paths of the shapes in the cards
        os.system('cd {inputdir}; {cmd}; cd -'.format(inputdir=os.path.abspath(options.inputdir),cmd=combineCards))
      
        ws = combinedCard.replace('_card.txt', '_ws.root')
        t2w = 'text2workspace.py {cf} -o {ws} --X-allow-no-signal --X-no-check-norm '.format(cf=combinedCard, ws=ws)
        print "combined t2w command: ",t2w
        os.system(t2w)
        combineCmdTwoCharges = 'combine {ws} -M MultiDimFit    -t -1 --expectSignal=1 -m 999 --saveFitResult --cminInitialHesse 1 --cminFinalHesse 1 --cminPreFit 1       --redefineSignalPOIs {pois}            --floatOtherPOIs=0 --freezeNuisanceGroups efficiencies,fixedY{pdfs}{scales} -v 9'.format(ws=ws, pois=','.join(minosPOIs), pdfs=(',pdfs' if len(pdfsyst) else ''), scales=(',scales' if len(qcdsyst) else ''))
        print combineCmdTwoCharges
        print "DONE. ENJOY FITTING !"
