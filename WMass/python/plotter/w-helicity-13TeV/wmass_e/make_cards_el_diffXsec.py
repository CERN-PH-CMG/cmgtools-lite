import os
from datetime import datetime

# python w-helicity-13TeV/wmass_e/make_cards_el_diffXsec.py -q cmscaf1nd --groupSignalBy 10 --syst -d

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option("-d", "--dry-run", dest="dryRun",   action="store_true", default=False, help="Do not run the job, only print the command");
parser.add_option("-f", "--force", dest="force",   action="store_true", default=False, help="Force running without question below (useful only when using PDF systematics)");
parser.add_option("-s", "--suffix", dest="suffix", type="string", default=None, help="Append a suffix to the default outputdir (helicity_<date>)");
parser.add_option("-q", "--queue", dest="queue", type="string", default="cmscaf1nd", help="Select the queue to use");
parser.add_option("-r", "--run", dest="run", type="string", default="sb", help="Which components to run: s for signal, b for backgrounds or sb for both");
parser.add_option("--syst", dest="addSyst", action="store_true", default=False, help="Add PDF and QCD scale systematics to the signal (need incl_sig directive in the MCA file)");
#### options for differential xsec
#parser.add_option("-x", "--x-sec", dest="xsec",   action="store_true", default=False, help="Do differential cross-section");
parser.add_option(      "--xsec-sigcard-binned", dest="xsec_sigcard_binned",   action="store_true", default=False, help="When doing differential cross-section, will make 1 signal card for each 2D template bin (default is False because the number of cards easily gets huge)");
parser.add_option("--groupSignalBy", dest="groupSignalBy", type="int", default='0', help="Group signal bins in bunches of N (pass N as argument). Default is 0, meaning \
not using this option. This option will reduce the number of chunk datacard for signal,but jobs will last for longer");
(options, args) = parser.parse_args()

if options.xsec_sigcard_binned and options.addSyst and not options.force:
    print ""
    print "You are trying to run the differential cross-section measurement making a signal template/card for each bin of the 2D templates."
    print "In addition, you are trying to add PDF and QCD scale systematics (60 variations for PDF)"
    print "This is a huge number of outputs, are you sure you want to proceed? [y/N]\n"
    if raw_input()!='y':
        print 'Aborting'
        exit()

BASECONFIG="w-helicity-13TeV/wmass_e"
PROG="w-helicity-13TeV/make_diff_xsec_cards.py"
MCA=BASECONFIG+'/mca-80X-wenu-xsec.txt'
outdirbase = "diffXsec"
#BINNING="\"[-2.5,-2.3,-2.1,-1.9,-1.7,-1.566,-1.4442,-1.2,-1.0,-0.8,-0.6,-0.4,0.2,0,0.2,0.4,0.6,0.8,1.0,1.2,1.4442,1.566,1.7,1.9,2.1,2.3,2.5]*[30,33,36,39,42,45]\""
#BINNING="\"[-2.5,-2.3,-2.1,-1.9,-1.7,-1.566,-1.4442,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1.0,1.2,1.4442,1.566,1.7,1.9,2.1,2.3,2.5]*[30,33,36,39,42,45]\""
#BINNING="\"[-2.5,-1.566,-1.4442,0,1.4442,1.566,2.5]*[30,35,40,45]\""
BINNING="\"[-2.5,-2.3,-2.1,-1.9,-1.7,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.7,1.9,2.1,2.3,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]\""
CUTFILE=BASECONFIG+'/wenu_80X.txt'
SYSTFILE=BASECONFIG+'/systsEnv.txt'
TREEPATH="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
QUEUE=str(options.queue)
VAR="\"ptElFull(LepGood1_calPt,LepGood1_eta):LepGood1_eta\""
WEIGHTSTRING=" \'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)\' "
LUMI=30.9

OUTDIR="%s_%s" % (outdirbase,datetime.now().strftime("%Y_%m_%d"))
if options.groupSignalBy: OUTDIR += ("_group%s" % str(options.groupSignalBy))
if options.suffix: OUTDIR += ("_%s" % options.suffix)

components=[] 
if "s" in options.run:
    components.append(" -s ")
if "b" in options.run:
    components.append(" -b ")

### 
# create the mca for signal bins: it is needed only if you want to group signal bins, because you have to use option -p of mcAnalysis to select them as different processes
print " Creating signal MCA file: {base}/mca-includes/mca-80X-wenu-sigInclCharge_binned_eta_pt.txt".format(base=BASECONFIG)
makeMCAcommand="python w-helicity-13TeV/printBinnnedSignalMCA.py -o %s/mca-includes/ -n mca-80X-wenu-sigInclCharge_binned_eta_pt.txt -b %s -x 'GenLepDressed_eta[0]' -y 'GenLepDressed_pt[0]' -c el " % (BASECONFIG,BINNING)
os.system(makeMCAcommand)

for c in components:
    cmd="python " + " ".join([PROG,MCA,CUTFILE,VAR,BINNING,SYSTFILE,OUTDIR]) + \
        (" -W %s " % WEIGHTSTRING) + (" -P %s " % TREEPATH) + (" -q %s " % QUEUE) + c + \
        (" -l %f " % LUMI)
    if options.xsec_sigcard_binned: cmd += '  --xsec-sigcard-binned '
    if options.groupSignalBy: cmd += '  --groupSignalBy %d ' % options.groupSignalBy
    if options.dryRun: cmd += '  --dry-run '
    if options.addSyst: cmd += '  --pdf-syst --qcd-syst '
    os.system(cmd)
