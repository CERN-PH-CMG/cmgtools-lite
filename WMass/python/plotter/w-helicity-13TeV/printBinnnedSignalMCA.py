import sys, os
import ROOT, datetime, array
import re

from make_diff_xsec_cards import getArrayParsingString

# usage 
# create an MCA with many signal processes for different cuts
#
# python printBinnnedSignalMCA.py -o w-helicity-13TeV/wmass_e/mca-includes/ -n mca-80X-wenu-sigInclCharge_binned_eta_pt.txt -b "[x1,x2,x3,...]*[y1,y2,y3,...]" -x GenLepDressed_eta[0] -y GenLepDressed_pt[0] -c el
#
# for option -b, I have to implement using constant width binning, with format like the histogram creator for mcPlots.py

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option('-o','--outdir', dest='outdir',   default='w-helicity-13TeV/wmass_e/mca-includes/', type='string', help='Output folder')
parser.add_option('-n','--name', dest='mcaName',   default='mca-80X-wenu-sigInclCharge_binned_eta_pt.txt', type='string', help='Name of output mca file')
parser.add_option('-c','--channel', dest='channel',   default='el', type='string', help='Channel (el or mu)')
parser.add_option('-x','--xvar', dest='xvar',   default='LepGood1_eta', type='string', help='Name of variable in x axis of the template')
parser.add_option('-y','--yvar', dest='yvar',   default='ptElFull(LepGood1_calPt,LepGood1_eta)', type='string', help='Name of variable in y axis of the template')
parser.add_option('-b','--binning', dest='binning', default='[-2.5,-2.1,-1.566,-1.4442,-1.0,-0.5,0,0.5,1.0,1.4442,1.566,2.1,2.5]*[30,33,36,39,42,45]', type='string', help='Binning (use same format as for histogram definition for mcPlots.py (to be implemented correctly)')
(options, args) = parser.parse_args()

outdir = options.outdir
if not outdir.endswith('/'):
    outdir += '/'
    
if not os.path.exists(outdir): 
    os.mkdirs(outdir)

print "Writing file %s%s " % (outdir,options.mcaName)
mcafile = open(outdir+options.mcaName,'w')
mcafile.write("## Binning\n")
mcafile.write("## %s\n\n" % options.binning)

binning = options.binning
genDecayId = 12 if options.channel == "el" else 14

if options.binning:
    etabinning=binning.split('*')[0]    # this is like [a,b,c,...], and is of type string. We nedd to get an array                                                          
    ptbinning=binning.split('*')[1]
    etabinning = getArrayParsingString(etabinning)
    ptbinning = getArrayParsingString(ptbinning)
    ptVarCut = options.yvar
    etaVarCut = options.xvar
    nptbins = len(ptbinning)-1
    netabins = len(etabinning)-1
else:
    nptbins = 1
    netabins = 1

charges = [ "plus", "minus"]
flav=options.channel


syst_suffix = ["_elescale_Up", "_elescale_Dn"] 
labels = ["lep scale Up", "lep scale Dn"]  
syst_label = dict(zip(syst_suffix, labels))
all_syst_suffix = [""]  # "" is for nominal
all_syst_suffix.extend(syst_suffix)

for syst in all_syst_suffix:

    for charge in charges:

        if syst == "":
            print "Writing charge ",charge
            mcafile.write("## CHARGE %s\n\n" % charge)
            label = " Label=\"W%s\"" % "+" if charge == "plus" else "-"
        else:
            print "Writing syst '%s' for charge %s" % (syst,charge)
            mcafile.write("## CHARGE %s   SYST %s \n\n" % (charge, syst))
            label = " Label=\"W%s %s\"" % ("+" if charge == "plus" else "-", syst_label[syst])

        chargeSignCut = ">" if charge == "plus" else "<"

        for ipt in xrange(nptbins):
            for ieta in xrange(netabins):

                etacut = "%s>=%s && %s<%s" % (etaVarCut,etabinning[ieta],etaVarCut,etabinning[ieta+1])
                ptcut = "%s>=%s && %s<%s" % (ptVarCut,ptbinning[ipt],ptVarCut,ptbinning[ipt+1])
                fullcut = etacut + " && " + ptcut
                fullcut = fullcut + " && genw_decayId == " + str(genDecayId) 
                fullcut = fullcut + " && genw_charge" + chargeSignCut + "0"
                fullcut = fullcut + " && LepGood1_mcMatchId*LepGood1_charge!=-24 "

                line = "W{ch}_{fl}_ieta_{ieta}_ipt_{ipt}{syst} : WJetsToLNu_NLO* : 3.*20508.9 : {cut} ; FillColor=ROOT.kRed+2 , {lab} ".format(ch=charge,fl=flav,
                                                                                                                                               ieta=ieta,ipt=ipt,
                                                                                                                                               cut=fullcut,lab=label,
                                                                                                                                               syst=syst)
                if syst != "": line += ", SkipMe=True"
                mcafile.write(line+"\n")


        mcafile.write("\n\n")



mcafile.close()


#Wplus   : WJetsToLNu_NLO* : 3.*20508.9   : genw_decayId == 12 && genw_charge>0 && LepGood1_mcMatchId*LepGood1_charge!=-24 ; FillColor=ROOT.kRed+2 , Label="W+"
#Wminus  : WJetsToLNu_NLO* : 3.*20508.9   : genw_decayId == 12 && genw_charge<0 && LepGood1_mcMatchId*LepGood1_charge!=-24 ; FillColor=ROOT.kRed+2 , Label="W-"
