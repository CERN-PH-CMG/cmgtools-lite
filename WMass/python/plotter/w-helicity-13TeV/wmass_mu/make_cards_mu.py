import os
from datetime import datetime

from optparse import OptionParser
parser = OptionParser(usage='%prog [options]')
parser.add_option('-d', '--dry-run', dest='dryRun',   action='store_true', default=False, help='Do not run the job, only print the command');
parser.add_option('-s', '--suffix', dest='suffix', type='string', default=None, help='Append a suffix to the default outputdir (helicity_<date>)');
parser.add_option("--syst", dest="addSyst", action="store_true", default=False, help="Add PDF systematics to the signal (need incl_sig directive in the MCA file)");
parser.add_option("--long-bkg", dest="longBkg",    action="store_true", default=True, help="Treat the longitudinal polarization as one background template.");
(options, args) = parser.parse_args()

PROG         = 'w-helicity-13TeV/make_helicity_cards.py'
BASECONFIG   = 'w-helicity-13TeV/wmass_mu'
MCA          = BASECONFIG+'/mca-wmu-helicity.txt'
CUTFILE      = BASECONFIG+'/cuts_wmu.txt'
SYSTFILE     = BASECONFIG+'/systsEnv.txt'
#TREEPATH     = '/eos/user/m/mdunser/w-helicity-13TeV/trees/trees_all_skims/'
TREEPATH     = '/eos/user/m/mdunser/w-helicity-13TeV/trees/TREES_latest_1muskim/'
QUEUE        = '8nh'
VAR          = '\'LepGood1_pt:LepGood1_eta\''

## variable binning in eta
binsEta = list(i*0.1 for i in range(1,11)) + list(1.+0.15*i for i in range(1,11))
negstring = '['+','.join(reversed(  list(str(-1.*i) for i in binsEta) ))
posstring =     ','.join(           list(str(    i) for i in binsEta) )+']'
etabinning= negstring+',0.,'+posstring

## variable binning in pt
ptbinning = '['+','.join(str(i) for i in range(25,46))+']'

##BINNING      = '\'32,-2.4,2.4,20,25.,45.\''
BINNING      = '\''+etabinning+'*'+ptbinning+'\''
WEIGHTSTRING = ' \'puw2016_nTrueInt_36fb(nTrueInt)*LepGood_effSF[0]\' '
#WEIGHTSTRING = ' \'puWeight \' '#*LepGood_effSF[0]\' '
#WEIGHTSTRING = ' \'1. \' '#*LepGood_effSF[0]\' '
OUTDIR       = 'helicity_%s' % datetime.now().strftime('%Y_%m_%d')
if options.suffix: OUTDIR += ('_%s' % options.suffix)

components=[' -s ',' -b ']
#components=[' -b ']

for c in components:
    cmd='python ' + ' '.join([PROG,MCA,CUTFILE,VAR,BINNING,SYSTFILE,OUTDIR,'-C mu']) + \
        (' -W %s ' % WEIGHTSTRING) + (' -P %s ' % TREEPATH) + (' -q %s ' % QUEUE) + c
    if options.dryRun: cmd += '  --dry-run '
    if options.addSyst: cmd += '  --pdf-syst --qcd-syst '
    if options.longBkg: cmd += ' --long-bkg '
    os.system(cmd)
