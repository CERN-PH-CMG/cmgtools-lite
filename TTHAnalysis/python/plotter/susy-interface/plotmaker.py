from optparse import OptionParser
from lib import maker
from lib import functions as func

def collectMakes(region, make):
	available = ["data", "sigs", "bkgs", "mix"]
	mix       = ["all", "both"]
	if not make in available and not make in mix: return []
	if make in mix:
		if make=="all" : return available
		if make=="both": return ["sigs", "bkgs"]
	if make in available: return [make]
	return []

def collectPlots(region, plotsname):
	available = [k for k,v in region.plots.iteritems()]
	if len(available)==0 or (plotsname!="all" and not plotsname in available): return []
	if plotsname=="all": return available
	return [plotsname]

def collectPPlots(region, plotsname):
	if not plotsname in region.plots.keys(): return ""
	return " ".join("--sP "+v for v in region.plots[plotsname])

def collectProcesses(mm, make):
	if len(mm.options.procs)>0: 
		procs = " ".join(["-p "+b for b in mm.getProcs()])
		add = ""
		if make=="sigs" or make=="mix": add="--showIndivSigs --noStackSig "
		if make=="sigs": add="--empytStack -p dummy "+add
		return add + procs
	bkgs = " ".join(["-p "+b for b in mm.getBkgs()])
	sigs = " ".join(["-p "+s for s in mm.getSigs()])
	if make=="data": return "-p data "+bkgs
	if make=="mix" : return "--showIndivSigs --noStackSig "+sigs+" "+bkgs
	if make=="sigs": return "--emptyStack -p dummy --showIndivSigs --noStackSig "+sigs
	if make=="bkgs": return bkgs
	return ""
	
parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--make",  dest="make",   type="string", default="data", help="Give info what to plot, either 'data' (data vs bkg), 'bkg' (for bkg only), 'sig' (for signal only), 'mix' (for bkg and signal together), 'both' (for running once 'sig' and once 'bkg')");
parser.add_option("--plots",  dest="plots",   type="string", default="all", help="Give the name of the plot collection you want to run");
parser.add_option("--lspam", dest="lspam", type="string", default="Preliminary", help="Left-spam for CMS_lumi in mcPlots, either Preliminary, Simulation, Internal or nothing")
parser.add_option("--noRatio", dest="ratio", action="store_false", default=True, help="Do NOT plot the ratio (i.e. give flag --showRatio)")

base = "python mcPlots.py {MCA} {CUTS} {PLOTFILE} -P {T} --neg --s2v --tree {TREENAME} -f --cmsprel '{LSPAM}' --legendWidth 0.20 --legendFontSize 0.035 {MCCS} {MACROS} {RATIO} -l {LUMI} --pdir {O} {FRIENDS} {PROCS} {PLOTS} {FLAGS} --showMCError"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("plotmaker", base, args, options)

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	

for r in range(len(mm.regions)):
	mm.iterateRegion()

	flags   = mm.collectFlags  ("flagsPlots")
	ratio   = "--showRatio" if options.ratio else ""
	
	makes    = collectMakes(mm.region, options.make)
	plots    = collectPlots(mm.region, options.plots)
	scenario = mm.getScenario()
	
	for p in plots:
		for m in makes:
			output = mm.outdir +"/"+ scenario +"/"+ p +"/"+ mm.region.name +"/"+ m
			func.mkdir(output)
	
			procs   = collectProcesses(mm       , m)
			pplots  = collectPPlots   (mm.region, p)
	
			mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("plotfile",""), mm.treedir, options.treename, options.lspam, mccs, macros, ratio, options.lumi, output, friends, procs, pplots, flags],mm.region.name+"_"+p+"_"+m,False)
mm.runJobs()
mm.clearJobs()


