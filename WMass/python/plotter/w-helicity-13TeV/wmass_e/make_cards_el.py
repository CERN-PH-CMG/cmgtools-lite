import os
from datetime import datetime

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option("-d", "--dry-run", dest="dryRun",   action="store_true", default=False, help="Do not run the job, only print the command");
parser.add_option("-s", "--suffix", dest="suffix", type="string", default=None, help="Append a suffix to the default outputdir (helicity_<date>)");
parser.add_option("-q", "--queue", dest="queue", type="string", default="cmscaf1nd", help="Select the queue to use");
parser.add_option("--pdf-syst", dest="addPdfSyst", action="store_true", default=False, help="Add PDF systematics to the signal (need incl_sig directive in the MCA file)");
(options, args) = parser.parse_args()

PROG="w-helicity-13TeV/make_helicity_cards.py"
BASECONFIG="w-helicity-13TeV/wmass_e"
MCA=BASECONFIG+'/mca-80X-wenu-helicity.txt'
CUTFILE=BASECONFIG+'/wenu_80X.txt'
SYSTFILE=BASECONFIG+'/systsEnv.txt'
TREEPATH="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY"
QUEUE=str(options.queue)
VAR="\"ptElFull(LepGood1_calPt,LepGood1_eta):LepGood1_eta\""
#BINNING="\"48,-2.5,2.5,20,30.,50.\""
#BINNING="\"24,-2.5,2.5,20,30.,50.\""
BINNING="\"[-2.5,-2.25,-2.0,-1.8,-1.566,-1.4442,-1.3,-1.2,-1.1,-1.0,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4442,1.566,1.8,2.0,2.25,2.5]*[30,31,32,33,34,35,36,37,38,39,40,41,42,45]\""
WEIGHTSTRING=" \'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)\' "
OUTDIR="helicity_%s" % datetime.now().strftime("%Y_%m_%d")
if options.suffix: OUTDIR += ("_%s" % options.suffix)

components=[" -s "," -b "]

for c in components:
    cmd="python " + " ".join([PROG,MCA,CUTFILE,VAR,BINNING,SYSTFILE,OUTDIR]) + \
        (" --long-bkg -W %s " % WEIGHTSTRING) + (" -P %s " % TREEPATH) + (" -q %s " % QUEUE) + c
    if options.dryRun: cmd += '  --dry-run '
    if options.addPdfSyst: cmd += '  --pdf-syst '
    os.system(cmd)
