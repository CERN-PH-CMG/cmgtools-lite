import datetime, sys
from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--tmpdir" , dest="tmpdir" , type="string", default=None, help="Temporary output directory") 
parser.add_option("--gen"    , dest="gen"    , action="store_true", default=False, help="Use GenPart collection for splitting")
parser.add_option("--pdgId1" , dest="pdgId1" , type="int", default=None, help="PdgId of particle 1 when using --gen")
parser.add_option("--pdgId2" , dest="pdgId2" , type="int", default=None, help="PdgId of particle 2 when using --gen")
parser.add_option("--minmass", dest="minmass", type="int", default=100 , help="Minimum mass of particle 1 (for parallel splitting)")
parser.add_option("--maxmass", dest="maxmass", type="int", default=1200, help="Maximum mass of particle 1 (for parallel splitting)")
parser.add_option("--step"   , dest="step"   , type="int", default=None, help="Mass step of particle 1 (for parallel splitting)")
parser.add_option("--dm"     , dest="deltam" , type="int", default=None, help="Mass difference between particle 1 and 2 (for parallel splitting)") 

base = "python splitSMSTrees.py {O} {T} {GEN} {TMP} --tree {TREENAME} {MASS} {LSP}"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("splitmaker", base, args, options)

tmp = "--tmpdir "+options.tmpdir if options.tmpdir else ""
gen = "--gen" if options.gen else ""
if options.gen:
	gen += " --pdgId1 %d"%options.pdgId1 if options.pdgId1 else ""
	gen += " --pdgId2 %d"%options.pdgId2 if options.pdgId2 else ""

## split tree per mass (parallel splitting)
if options.minmass and options.maxmass and options.step:

	masses = [options.minmass + i*options.step for i in range((options.maxmass - options.minmass)/options.step+1)]
	for mass in masses:
		lsp = "--lsp "+str(mass-options.deltam) if options.deltam else ""
		mm.submit([mm.outdir, mm.treedir, gen, tmp, options.treename, "--mass "+str(mass), lsp],str(mass),False)
	mm.runJobs()
	mm.clearJobs()

## only one splitting job
else:
	mm.submit([mm.outdir, mm.treedir, gen, tmp, options.treename, "", ""])


