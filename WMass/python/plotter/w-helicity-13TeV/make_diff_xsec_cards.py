#!/usr/bin/env python
from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np
# import some parameters from wmass_parameters.py, they are also used by other scripts
from wmass_parameters import *

# work only if make_helicity_cards.py has a __main__, otherwise it copies everything (not good, it copies also the body)
# from make_helicity_cards import getMcaIncl
# from make_helicity_cards import writePdfSystsToMCA
# from make_helicity_cards import writeQCDScaleSystsToMCA
# from make_helicity_cards import writePdfSystsToSystFile
# from make_helicity_cards import submitBatch


def intermediateBinning(diff):

    n25 = int(diff/0.25)

    rest = diff - n25*0.25

    if any([np.isclose(rest,0.2), np.isclose(rest,0.15)]):
        bins = [rest]
        bins += [0.25 for i in range(n25)]
    elif rest < 0.15:
        bins = [0.25 for i in range(n25-1)] + [0.25+rest]

    return bins

## infile should be the reco/gen efficiency file of the electrons
def makeYWBinning(infile, cutoff=5000):
    
    histo_file = ROOT.TFile(infile, 'READ')
    
    yw_binning = {}
    
    for ch in ['plus', 'minus']:
        for pol in ['left', 'right']:
            cp = '{ch}_{pol}'.format(ch=ch,pol=pol)
            yw_binning[cp] = [i*0.15 for i in range(11)]
            hname = 'w{ch}_abswy_reco_W{ch}_{pol}'.format(ch=ch,pol=pol)
            histo = histo_file.Get(hname)
            nlast = 0.
            for ibin in reversed(range(1,histo.GetNbinsX()+1)):
                if not nlast > cutoff:
                    nlast += histo.GetBinContent(ibin)
                else:
                    ilast = ibin
                    ylast = histo.GetXaxis().GetBinUpEdge(ilast)
                    diffTo1p5 = ylast - 1.5
                    intermediate_binning = intermediateBinning(diffTo1p5)
                    for i in intermediate_binning:
                        yw_binning[cp] += [yw_binning[cp][-1]+i]
                    yw_binning[cp] += [histo.GetXaxis().GetXmax()]
                    yw_binning[cp] = [float('{n:.2f}'.format(n=n)) for n in yw_binning[cp] ]
                    break
    
    return yw_binning

NPDFSYSTS=60 # Hessian variations of NNPDF 3.0
pdfsysts=[] # array containing the PDFs signal variations
qcdsysts=[] # array containing the QCD scale signal variations

def getMcaIncl(mcafile,incl_mca='incl_sig'):
    incl_file=''
    mcaf = open(mcafile,'r')
    for l in mcaf.readlines():
        if re.match("\s*#.*", l): continue
        tokens = [t.strip() for t in l.split(':')]
        if len(tokens)<2: continue
        if tokens[0]==incl_mca and "+" in tokens[1]:
            options_str = [t.strip() for t in (l.split(';')[1]).split(',')]
            for o in options_str:
                if "IncludeMca" in o: 
                    incl_file = o.split('=')[1]
            break
    return incl_file

def writePdfSystsToMCA(mcafile,odir,vec_weight="hessWgt",syst="pdf",incl_mca='incl_sig',append=False):
    open("%s/systEnv-dummy.txt" % odir, 'a').close()
    incl_file=getMcaIncl(mcafile,incl_mca)
    if len(incl_file)==0: 
        print "Warning! '%s' include directive not found. Not adding pdf systematics samples to MCA file" % incl_mca
        return
    if append:
        filename = "%s/mca_systs.txt" % odir
        if not os.path.exists(filename): os.system('cp {mca_orig} {mca_syst}'.format(mca_orig=mcafile,mca_syst=filename))
    for i in range(1,NPDFSYSTS+1):
        postfix = "_{proc}_{syst}{idx}".format(proc=incl_mca.split('_')[1],syst=syst,idx=i)
        mcafile_syst = open(filename, 'a') if append else open("%s/mca%s.txt" % (odir,postfix), "w")
        mcafile_syst.write(incl_mca+postfix+'   : + ; IncludeMca='+incl_file+', AddWeight="'+vec_weight+str(i)+'", PostFix="'+postfix+'" \n')
        pdfsysts.append(postfix)
    print "written ",syst," systematics relative to ",incl_mca

def writeQCDScaleSystsToMCA(mcafile,odir,syst="qcd",incl_mca='incl_sig',scales=[],append=False):
    open("%s/systEnv-dummy.txt" % odir, 'a').close()
    incl_file=getMcaIncl(mcafile,incl_mca)
    if len(incl_file)==0: 
        print "Warning! '%s' include directive not found. Not adding QCD scale systematics!"
        return
    if append:
        filename = "%s/mca_systs.txt" % odir
        if not os.path.exists(filename): os.system('cp {mca_orig} {mca_syst}'.format(mca_orig=mcafile,mca_syst=filename))    
    for scale in scales:
        for idir in ['Up','Dn']:
            postfix = "_{proc}_{syst}{idir}".format(proc=incl_mca.split('_')[1],syst=scale,idir=idir)
            mcafile_syst = open(filename, 'a') if append else open("%s/mca%s.txt" % (odir,postfix), "w")
            if not scale == "wptSlope": ## alphaS and qcd scales are treated equally here. but they are different from the w-pT slope
                mcafile_syst.write(incl_mca+postfix+'   : + ; IncludeMca='+incl_file+', AddWeight="qcd_'+scale+idir+'", PostFix="'+postfix+'" \n')
            else:
                sign  =  1 if idir == 'Dn' else -1
                asign = -1 if idir == 'Dn' else  1
                offset = 0.05; slope = 0.005;
                fstring = "wpt_slope_weight(genw_pt\,{off:.3f}\,{slo:.3f})".format(off=1.+asign*offset, slo=sign*slope)
                mcafile_syst.write(incl_mca+postfix+'   : + ; IncludeMca='+incl_file+', AddWeight="'+fstring+'", PostFix="'+postfix+'" \n')
            qcdsysts.append(postfix)
    print "written ",syst," systematics relative to ",incl_mca

def writePdfSystsToSystFile(filename,sample="W.*",syst="CMS_W_pdf"):
    SYSTFILEALL=('.').join(filename.split('.')[:-1])+"-all.txt"
    copyfile(filename,SYSTFILEALL)
    systfile=open(SYSTFILEALL,"a")
    for i in range(NPDFSYSTS/2):
        systfile.write(syst+str(i+1)+"  : "+sample+" : .* : pdf"+str(i+1)+" : templates\n")
    print "written pdf syst configuration to ",SYSTFILEALL
    return SYSTFILEALL


def submitBatch(dcname,outdir,mkShCardsCmd,options):
    srcfile=outdir+"/jobs/"+dcname+".sh"
    logfile=outdir+"/jobs/"+dcname+".log"
    srcfile_op = open(srcfile,"w")
    srcfile_op.write("#! /bin/sh\n")
    srcfile_op.write("ulimit -c 0 -S\n")
    srcfile_op.write("ulimit -c 0 -H\n")
    srcfile_op.write("cd {cmssw};\neval $(scramv1 runtime -sh);\ncd {dir};\n".format( 
            dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE']))
    srcfile_op.write(mkShCardsCmd)
    os.system("chmod a+x "+srcfile)
    cmd = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}\n".format(
        queue=options.queue, dir=os.getcwd(), logfile=logfile, srcfile=srcfile)
    if options.dryRun: print cmd
    else: os.system(cmd)

# new function
def getArrayParsingString(inputString, verbose=False, makeFloat=False):
    # convert string [a,b,c,...] to list of a b c ...
    tmp = inputString.replace('[','').replace(']','')
    tmp = tmp.split(',')
    if verbose:
        print "Input:",inputString
        print "Output:",tmp
    if makeFloat:
        ret = [float(x) for x in tmp]
    else:
        ret = tmp
    return ret

# new function
def getGlobalBin(ix, iy, nbinsX, binFrom0=True):
    # ix goes from 0 to nbinsX-1, like the value returned by "for ix in xrange(nbinsX)"
    # same is expected for iy
    # If this is the case, global bin starts from 0
    #However, if binFrom0=False, it is expected that the bins start from 1 (like those of a TH1) and the globalbin that is returned will start from 1 as well
    return (ix + iy * nbinsX)

def getXYBinsFromGlobalBin(globalbin, nbinsX, binFrom0=True):
    # global bin goes from 0 to nbinX*nbinsY-1 
    # returned x(y) is a number from 0 to nbinsX(Y) -1
    # however, if that is not the convention, then binFrom0 must be set to False: this manages the case where the global bin starts from 1 and the returned ix and iy will start from 1 as well
    tmp = globalbin if binFrom0 else (globalbin-1)
    iy = int(tmp/nbinsX)
    ix = tmp % nbinsX
    if not binFrom0:
        ix = ix + 1
        iy = iy + 1
    return ix,iy


if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] mc.txt cuts.txt var bins systs.txt outdir ")
    parser.add_option("-q", "--queue",    dest="queue",     type="string", default=None, help="Run jobs on lxbatch instead of locally");
    parser.add_option("--dry-run", dest="dryRun",    action="store_true", default=False, help="Do not run the job, only print the command");
    parser.add_option("-s", "--signal-cards",  dest="signalCards",  action="store_true", default=False, help="Make the signal part of the datacards");
    parser.add_option("-b", "--bkgdata-cards", dest="bkgdataCards", action="store_true", default=False, help="Make the background and data part of the datacards");
    parser.add_option("-W", "--weight", dest="weightExpr", default="1", help="Event weight expression (default 1)");
    parser.add_option("-P", "--path", dest="path", type="string",default=None, help="Path to directory with input trees and pickle files");
    parser.add_option("-C", "--channel", dest="channel", type="string", default='el', help="Channel. either 'el' or 'mu'");
    parser.add_option("--groupSignalBy", dest="groupSignalBy", type="int", default='0', help="Group signal bins in bunches of N (pass N as argument). Default is 0, meaning not using this option. This option will reduce the number of chunk datacard for signal,but jobs will last for longer");
    parser.add_option("--not-unroll2D", dest="notUnroll2D", action="store_true", default=False, help="Do not unroll the TH2Ds in TH1Ds needed for combine (to make 2D plots)");
    parser.add_option("--pdf-syst", dest="addPdfSyst", action="store_true", default=False, help="Add PDF systematics to the signal (need incl_sig directive in the MCA file)");
    parser.add_option("--qcd-syst", dest="addQCDSyst", action="store_true", default=False, help="Add QCD scale systematics to the signal (need incl_sig directive in the MCA file)");
    parser.add_option("--xsec-sigcard-binned", dest="xsec_sigcard_binned",   action="store_true", default=False, help="When doing differential cross-section, will make 1 signal card for each 2D template bin (default is False because the number of cards easily gets huge)");
    (options, args) = parser.parse_args()

    if len(sys.argv) < 6:
        parser.print_usage()
        quit()


    FASTTEST=''
    #FASTTEST='--max-entries 1000 '
    T=options.path
    print "\n"
    print "Used trees from: ",T
    J=2
    MCA = args[0]
    CUTFILE = args[1]
    fitvar = args[2]
    binning = args[3]
    SYSTFILE = args[4]

    if not os.path.exists("cards/"):
        os.makedirs("cards/")
    outdir="cards/"+args[5]

    if not os.path.exists(outdir): 
        os.makedirs(outdir)
    if options.queue and not os.path.exists(outdir+"/jobs"): 
        os.mkdir(outdir+"/jobs")
        os.mkdir(outdir+"/mca")

    # copy some cfg for bookkeeping
    os.system("cp %s %s" % (CUTFILE, outdir))
    os.system("cp %s %s" % (MCA, outdir))

    ## save template binning (eta on X, pt on y axis)
    ptEta_binfile = open(outdir+'/binningPtEta.txt','w')
    ptEta_binfile.write("#Template binning: eta-pt on x-y axis\n")
    ptEta_binfile.write(binning)
    ptEta_binfile.write('\n')
    ptEta_binfile.close()
    
    if options.addPdfSyst:
        # write the additional systematic samples in the MCA file
        writePdfSystsToMCA(MCA,outdir+"/mca") # on W + jets 
        writePdfSystsToMCA(MCA,outdir+"/mca",incl_mca='incl_dy') # on DY + jets
        # write the complete systematics file (this was needed when trying to run all systs in one job)
        # SYSTFILEALL = writePdfSystsToSystFile(SYSTFILE)
    if options.addQCDSyst:
        scales = ['muR','muF',"muRmuF", "alphaS"]
        writeQCDScaleSystsToMCA(MCA,outdir+"/mca",scales=scales+["wptSlope"])
        writeQCDScaleSystsToMCA(MCA,outdir+"/mca",scales=scales,incl_mca='incl_dy')

    ARGS=" ".join([MCA,CUTFILE,"'"+fitvar+"' "+"'"+binning+"'",SYSTFILE])
    BASECONFIG=os.path.dirname(MCA)
    if options.queue:
        ARGS = ARGS.replace(BASECONFIG,os.getcwd()+"/"+BASECONFIG)
    OPTIONS=" -P "+T+" --s2v -j "+str(J)+" -l "+str(luminosity)+" -f --obj tree "+FASTTEST
    if not os.path.exists(outdir): os.makedirs(outdir)
    OPTIONS+=" -F Friends '{P}/friends/tree_Friend_{cname}.root' "
    if not options.notUnroll2D:
        OPTIONS+=" --2d-binning-function unroll2Dto1D "

    if options.queue:
        import os, sys
        basecmd = "bsub -q {queue} {dir}/lxbatch_runner.sh {dir} {cmssw} python {self}".format(
                    queue = options.queue, dir = os.getcwd(), cmssw = os.environ['CMSSW_BASE'], self=sys.argv[0]
                )

    etabinning=binning.split('*')[0]    # this is like [a,b,c,...], and is of type string. We nedd to get an array
    ptbinning=binning.split('*')[1]
    etabinning = getArrayParsingString(etabinning)
    ptbinning = getArrayParsingString(ptbinning)
    #ptVarCutEl="ptElFull(LepGood1_calPt,LepGood1_eta)"
    #ptVarCutMu="LepGood1_pt"
    ptVarCut = "GenLepDressed_pt[0]" #  ptVarCutEl if (options.channel == "el") else ptVarCutMu
    etaVarCut = "GenLepDressed_eta[0]" #"LepGood1_eta"
    nptbins = len(ptbinning)-1
    netabins = len(etabinning)-1
    nBinsInTemplate = (netabins)*(nptbins)

    ngroup = 0
    if options.groupSignalBy:
        ngroup = int(options.groupSignalBy)
        # below, subtract 1 because nBinsInTemplate starts from 1 (but should start from 0 for this logic)
        # then add 1 because xrange excludes the last index
        loopBins = int((nBinsInTemplate-1)/ngroup)+1 
    elif options.xsec_sigcard_binned:
        loopBins = nBinsInTemplate
    else:
        loopBins = 1

    ## previous lines were meant to distinguish the case where the signal template is made all at once (a single TH2) or dividing into each bin
    ## The latter requires just one job and create one datacard and one shape.root file, but then I need a way to allow each bin
    ## of the TH2 to float independently of the other (with some constraints), a kind of bin-by-uncertainty
    ## The former treat all bins as the rapidity bin in the helicity fit, but the number of bins here can be huge (let alone the PDf variations ...)
    ## Another way is to make signal cards grouping bins in bunches with some criteria
    ## this is enabled by option.groupSignalBy
    ## In this case, I set loopBins so to loop from 0 to int(nBinsInTemplate/ngroup) 

    POSCUT=" -A alwaystrue positive 'LepGood1_charge>0' "
    NEGCUT=" -A alwaystrue negative 'LepGood1_charge<0' "

    if options.signalCards:

        print "MAKING SIGNAL PART: "

        for ibin in xrange(loopBins):

            wsyst = ['']+[x for x in pdfsysts+qcdsysts if 'sig' in x]
            for ivar,var in enumerate(wsyst):
                for charge in ['plus','minus']:
                    antich = 'plus' if charge == 'minus' else 'minus'
                    if ivar==0: 
                        IARGS = ARGS
                    else: 
                        IARGS = ARGS.replace(MCA,"{outdir}/mca/mca{syst}.txt".format(outdir=outdir,syst=var))
                        IARGS = IARGS.replace(SYSTFILE,"{outdir}/mca/systEnv-dummy.txt".format(outdir=outdir))
                        print "Running the systematic: ",var
                    if not os.path.exists(outdir): os.makedirs(outdir)
                    if options.queue and not os.path.exists(outdir+"/jobs"): os.mkdir(outdir+"/jobs")
                    syst = '' if ivar==0 else var

                    xpsel=' --xp "W{antich}.*,Flips,Z,Top,DiBosons,TauDecaysW,data.*" --asimov '.format(antich=antich)      
                    ycut = POSCUT if charge=='plus' else NEGCUT

                    if options.groupSignalBy != "":
                        # if we are here, loopBins is not the number of bins in 2D template
                        # rather, it is the number of groups with ngroup bins each (+1 because xrange will exclude the last number)
                        # to get the ieta,ipt we must obtain again the real globalbin number
                        selectedSigProcess = ' -p '
                        for n in xrange(ngroup):
                            tmpGlobalBin = n + ibin * ngroup
                            ieta,ipt = getXYBinsFromGlobalBin(tmpGlobalBin,netabins)
                            selectedSigProcess += 'W{charge}_{channel}_ieta_{ieta}_ipt_{ipt}.*,'.format(charge=charge, channel=options.channel,
                                                                                                              ieta=ieta,ipt=ipt,syst=syst)
                        if selectedSigProcess.endswith(','):
                            selectedSigProcess = selectedSigProcess[:-1]
                        selectedSigProcess += " "
                        xpsel = selectedSigProcess + xpsel
                        dcname = "W{charge}_{channel}_group_{gr}{syst}".format(charge=charge, channel=options.channel,gr=ibin,syst=syst)

                    elif options.xsec_sigcard_binned:
                        ieta,ipt = getXYBinsFromGlobalBin(ibin,netabins)
                        print "Making card for %s<=pt<%s, %s<=eta<%s and signal process with charge %s " % (ptbinning[ipt],ptbinning[ipt+1],
                                                                                                            etabinning[ieta],etabinning[ieta+1],
                                                                                                            charge)
                        ptcut=" -A alwaystrue pt%d '%s>=%s && %s<%s' " % (ipt,ptVarCut,ptbinning[ipt],ptVarCut,ptbinning[ipt+1])
                        etacut=" -A alwaystrue eta%d '%s>=%s && %s<%s' " % (ieta,etaVarCut,etabinning[ieta],etaVarCut,etabinning[ieta+1])
                        ycut += (ptcut + etacut)
                        ##dcname = "W{charge}_{channel}_ieta_{ieta}_ipt_{ipt}{syst}".format(charge=charge, channel=options.channel,ieta=ieta,ipt=ipt,syst=syst)
                        ## keep same logic as before for the datacard name
                        dcname = "W{charge}_{channel}_group_{gr}{syst}".format(charge=charge,channel=options.channel,gr=ibin,syst=syst)
                    else:
                        dcname = "W{charge}_{channel}_group_{gr}{syst}".format(charge=charge, channel=options.channel,gr=ibin,syst=syst)

                    BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + ycut
                    if options.queue:
                        mkShCardsCmd = "python {dir}/makeShapeCards.py {args} \n".format(dir = os.getcwd(), args = IARGS+" "+BIN_OPTS)
                        submitBatch(dcname,outdir,mkShCardsCmd,options)
                    else:
                        cmd = "python makeShapeCards.py "+IARGS+" "+BIN_OPTS
                        if options.dryRun: print cmd
                        else:
                            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                            out, err = p.communicate() 
                            result = out.split('\n')
                            for lin in result:
                                if not lin.startswith('#'):
                                    print(lin)


    if options.bkgdataCards:
        print "MAKING BKG and DATA PART:\n"
        for charge in ['plus','minus']:
            xpsel=' --xp "W.*" ' 
            if len(pdfsysts+qcdsysts)>1: # 1 is the nominal 
                xpsel+=' --xp "Z" '
            chargecut = POSCUT if charge=='plus' else NEGCUT
            dcname = "bkg_and_data_{channel}_{charge}".format(channel=options.channel, charge=charge)
            BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + chargecut
            if options.queue:
                mkShCardsCmd = "python {dir}/makeShapeCards.py {args} \n".format(dir = os.getcwd(), args = ARGS+" "+BIN_OPTS)
                submitBatch(dcname,outdir,mkShCardsCmd,options)
            else:
                cmd = "python makeShapeCards.py "+ARGS+" "+BIN_OPTS
                if options.dryRun: print cmd
                else:
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    out, err = p.communicate() 
                    result = out.split('\n')
                    for lin in result:
                        if not lin.startswith('#'):
                            print(lin)

    if options.bkgdataCards and len(pdfsysts+qcdsysts)>1:
        dysyst = ['']+[x for x in pdfsysts+qcdsysts if 'dy' in x]
        for ivar,var in enumerate(dysyst):
            for charge in ['plus','minus']:
                antich = 'plus' if charge == 'minus' else 'minus'
                if ivar==0: 
                    IARGS = ARGS
                else: 
                    IARGS = ARGS.replace(MCA,"{outdir}/mca/mca{syst}.txt".format(outdir=outdir,syst=var))
                    IARGS = IARGS.replace(SYSTFILE,"{outdir}/mca/systEnv-dummy.txt".format(outdir=outdir))
                    print "Running the DY with systematic: ",var
                print "Making card for DY process with charge ", charge
                chcut = POSCUT if charge=='plus' else NEGCUT
                xpsel=' --xp "[^Z]*" --asimov '
                syst = '' if ivar==0 else var
                dcname = "Z_{channel}_{charge}{syst}".format(channel=options.channel, charge=charge,syst=syst)
                BIN_OPTS=OPTIONS + " -W '" + options.weightExpr + "'" + " -o "+dcname+" --od "+outdir + xpsel + chcut
                if options.queue:
                    mkShCardsCmd = "python {dir}/makeShapeCards.py {args} \n".format(dir = os.getcwd(), args = IARGS+" "+BIN_OPTS)
                    submitBatch(dcname,outdir,mkShCardsCmd,options)
                else:
                    cmd = "python makeShapeCards.py "+IARGS+" "+BIN_OPTS
                    if options.dryRun: print cmd
                    else:
                        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                        out, err = p.communicate() 
                        result = out.split('\n')
                        for lin in result:
                            if not lin.startswith('#'):
                                print(lin)
