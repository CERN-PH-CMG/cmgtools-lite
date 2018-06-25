import sys, os
import ROOT, datetime, array
import re

from make_diff_xsec_cards import getArrayParsingString

# usage 
# create an MCA with many signal processes for different cuts
#
# python w-helicity-13TeV/printMCAforXsec.py -o w-helicity-13TeV/wmass_e/mca-includes/ -n mca-80X-wenu-sigInclCharge_binned_eta_pt.txt -c el
#
# for option -b, I have to implement using constant width binning, with format like the histogram creator for mcPlots.py

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option('-o','--outdir', dest='outdir',   default='w-helicity-13TeV/wmass_e/mca-includes/', type='string', help='Output folder')
parser.add_option('-n','--name', dest='mcaName',   default='mca-80X-wenu-sigInclCharge_gen_eta_pt_4xsec.txt', type='string', help='Name of output mca file')
parser.add_option('-c','--channel', dest='channel',   default='el', type='string', help='Channel (el or mu)')
# parser.add_option('-x','--xvar', dest='xvar',   default='GenLepDressed_eta[0]', type='string', help='Name of variable in x axis of the template')
# parser.add_option('-y','--yvar', dest='yvar',   default='GenLepDressed_pt[0]', type='string', help='Name of variable in y axis of the template')
# parser.add_option(     '--xbin', dest='xbin',   default='500,-5.0,5.0', type='string', help='Inputs to define template x axis binning: format is nbins,min,max')
# parser.add_option(     '--ybin', dest='ybin',   default='180,10,100', type='string', help='Inputs to define template y axis binning: format is nbins,min,max')
(options, args) = parser.parse_args() 

outdir = options.outdir
if not outdir.endswith('/'):
    outdir += '/'
    
if not os.path.exists(outdir): 
    os.mkdirs(outdir)

print "Writing file %s%s " % (outdir,options.mcaName)
mcafile = open(outdir+options.mcaName,'w')

genDecayId = 12 if options.channel == "el" else 14

charges = [ "plus", "minus"]
flav=options.channel

scaleVars = ['muR','muF',"muRmuF", "alphaS"]
syst_suffix = []
for x in scaleVars:
    syst_suffix.append("%sUp" % x)
    syst_suffix.append("%sDn" % x)
#pdf
for i in range(60):
    syst_suffix.append("pdf%d" % int(i+1))

#labels = ["lep scale Up", "lep scale Dn"]  
#syst_label = dict(zip(syst_suffix, labels))
all_syst_suffix = [""]  # "" is for nominal
all_syst_suffix.extend(syst_suffix)

for syst in all_syst_suffix:

    for charge in charges:

        if syst == "":
            print "Writing charge ",charge
            mcafile.write("## CHARGE %s\n" % charge)
            label = " Label=\"W%s\"" % ("+" if charge == "plus" else "-")
        else:
            print "Writing syst '%s' for charge %s" % (syst,charge)
            mcafile.write("## CHARGE %s   SYST %s \n" % (charge, syst))
            label = " Label=\"W%s %s\"" % ("+" if charge == "plus" else "-", syst)

        chargeSignCut = ">" if charge == "plus" else "<"

        fullcut = "genw_decayId == " + str(genDecayId) 
        fullcut = fullcut + " && genw_charge" + chargeSignCut + "0"
        # fullcut = fullcut + " && LepGood1_mcMatchId*LepGood1_charge!=-24 "  # this is a reco cut, avoid it!!
        
        line = "W{ch}_{fl}_{syst} : WJetsToLNu_NLO* : 3.*20508.9 : {cut}".format(ch=charge,fl=flav,cut=fullcut,syst=syst if syst != "" else "central")
        line += " ; FillColor=ROOT.kRed+2 , {lab} ".format(lab=label)
        if syst != "": 
            if not "pdf" in syst:
                wgt = "qcd_%s" % syst
            else:
                wgt = "hessWgt%d" % int(str(syst[3:]))   # syst is pdf1, pdf2, ...: get the integer number to build the weight
            line += ", AddWeight=\"{wgt}\"".format(wgt=wgt)

        mcafile.write(line+"\n")

    mcafile.write("\n")

mcafile.close()


#Wplus   : WJetsToLNu_NLO* : 3.*20508.9   : genw_decayId == 12 && genw_charge>0 && LepGood1_mcMatchId*LepGood1_charge!=-24 ; FillColor=ROOT.kRed+2 , Label="W+"
#Wminus  : WJetsToLNu_NLO* : 3.*20508.9   : genw_decayId == 12 && genw_charge<0 && LepGood1_mcMatchId*LepGood1_charge!=-24 ; FillColor=ROOT.kRed+2 , Label="W-"
