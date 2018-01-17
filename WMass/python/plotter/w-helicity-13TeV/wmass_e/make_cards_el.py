import os
from datetime import datetime

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
parser.add_option("-d", "--dry-run", dest="dryRun",   action="store_true", default=False, help="Do not run the job, only print the command");
parser.add_option("-s", "--suffix", dest="suffix", type="string", default=None, help="Append a suffix to the default outputdir (helicity_<date>)");
(options, args) = parser.parse_args()

PROG="w-helicity-13TeV/make_helicity_cards.py"
BASECONFIG="w-helicity-13TeV/wmass_e"
MCA=BASECONFIG+'/mca-80X-wenu-helicity.txt'
CUTFILE=BASECONFIG+'/wenu.txt'
SYSTFILE=BASECONFIG+'/systsEnv.txt'
TREEPATH="/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V3"
QUEUE="cmscaf1nd"
VAR="\"ptElFull(LepGood1_calPt,LepGood1_eta):LepGood1_eta\""
BINNING="\"34,-2.5,2.5,13,30.,50.\""
#BINNING="\"24,-2.5,2.5,20,30.,50.\""
WEIGHTSTRING=" \'puw2016_nTrueInt_36fb(nTrueInt)*trgSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta,2)*leptonSF_We(LepGood1_pdgId,LepGood1_pt,LepGood1_eta)\' "
OUTDIR="helicity_%s" % datetime.now().strftime("%Y_%m_%d")
if options.suffix: OUTDIR += ("_%s" % options.suffix)

components=[" -s "," -b "]

for c in components:
    cmd="python " + " ".join([PROG,MCA,CUTFILE,VAR,BINNING,SYSTFILE,OUTDIR]) + \
        (" -W %s " % WEIGHTSTRING) + (" -P %s " % TREEPATH) + (" -q %s " % QUEUE) + c
    if options.dryRun: cmd += '  --dry-run '
    os.system(cmd)
