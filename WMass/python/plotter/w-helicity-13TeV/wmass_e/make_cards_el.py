import os
from datetime import datetime

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option("-d", "--dry-run", dest="dryRun",   action="store_true", default=False, help="Do not run the job, only print the command");
parser.add_option("-s", "--suffix", dest="suffix", type="string", default=None, help="Append a suffix to the default outputdir (helicity_<date>)");
parser.add_option("-q", "--queue", dest="queue", type="string", default="cmscaf1nd", help="Select the queue to use");
parser.add_option("--syst", dest="addSyst", action="store_true", default=False, help="Add PDF and QCD scale systematics to the signal (need incl_sig directive in the MCA file)");
#### options for differential xsec
parser.add_option("-x", "--x-sec", dest="xsec",   action="store_true", default=False, help="Do differential cross-section");
parser.add_option(      "--xsec-sigcard-binned", dest="xsec_sigcard_binned",   action="store_true", default=False, help="When doing differential cross-section, will make 1 signal card for each 2D template bin (default is False because the number of cards easily gets huge)");
parser.add_option("--groupSignalBy", dest="groupSignalBy", type="int", default='0', help="Group signal bins in bunches of N (pass N as argument). Default is 0, meaning \
not using this option. This option will reduce the number of chunk datacard for signal,but jobs will last for longer");
(options, args) = parser.parse_args()

if options.xsec and options.xsec_sigcard_binned and options.addSyst:
    print "You are trying to run the differential cross-section measurement making a signal template/card for each bin of the 2D templates."
    print "In addition, you are trying to add PDF and QCD scale systematics (60 variations for PDF)"
    print "This is a huge number of outputs, are you sure you want to proceed?[ y/N]\n"
    if raw_input()!='y':
        print 'Aborting'
        exit()

BASECONFIG="w-helicity-13TeV/wmass_e"
PROG="w-helicity-13TeV/make_helicity_cards.py"  # overriden below if options.xsec = True
MCA=BASECONFIG+'/mca-80X-wenu-helicity.txt'     # overriden below if options.xsec = True
CUTFILE=BASECONFIG+'/wenu_80X.txt'
SYSTFILE=BASECONFIG+'/systsEnv.txt'
TREEPATH="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
QUEUE=str(options.queue)
VAR="\"ptElFull(LepGood1_calPt,LepGood1_eta):LepGood1_eta\""
#BINNING="\"48,-2.5,2.5,20,30.,50.\""
#BINNING="\"24,-2.5,2.5,20,30.,50.\""
BINNING="\"[-2.5,-2.25,-2.0,-1.8,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.8,2.0,2.25,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]\""   # overriden below if options.xsec = True
WEIGHTSTRING=" \'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)\' "

outdirbase = "helicity" 

if options.xsec:
    PROG="w-helicity-13TeV/make_diff_xsec_cards.py"
    MCA=BASECONFIG+'/mca-80X-wenu-xsec.txt'
    outdirbase = "diffXsec"
    BINNING="\"[-2.5,-2.2,-1.9,-1.566,-1.4442,-1.2,-0.9,-0.6,-0.3,0,0.3,0.6,0.9,1.2,1.4442,1.566,1.9,2.2,2.5]*[30,33,36,39,42,45]\""

OUTDIR="%s_%s" % (outdirbase,datetime.now().strftime("%Y_%m_%d"))
if options.suffix: OUTDIR += ("_%s" % options.suffix)


components=[" -s "," -b "]
longBackGroundOption = "" if options.xsec else "--long-bkg"  # for xsec we are not separating the helicities component at the moment, so this option is useless

for c in components:
    cmd="python " + " ".join([PROG,MCA,CUTFILE,VAR,BINNING,SYSTFILE,OUTDIR]) + \
        (" %s -W %s " % (longBackGroundOption,WEIGHTSTRING)) + (" -P %s " % TREEPATH) + (" -q %s " % QUEUE) + c
    if options.xsec:
        if options.xsec_sigcard_binned: cmd += '  --xsec-sigcard-binned '
        if options.groupSignalBy: cmd += '  --groupSignalBy %d ' % options.groupSignalBy
    if options.dryRun: cmd += '  --dry-run '
    if options.addSyst: cmd += '  --pdf-syst --qcd-syst '
    os.system(cmd)
