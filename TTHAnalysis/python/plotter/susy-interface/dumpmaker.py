from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)

base = "python mcDump.py --dumpFile .fdump.txt {MCA} {CUTS} {FMT} -P {T} --s2v --tree {TREENAME} -j 4 {MCCS} {MACROS} {FRIENDS} {PROCS} {FLAGS} &&  sort -n -k1 -k2 -k3 .fdump.txt > {O}/dump_{TAG}.txt && rm .fdump.txt"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("dumpmaker", base, args, options)

friends  = mm.collectFriends()	
mccs     = mm.collectMCCs   ()
macros   = mm.collectMacros ()	

for r in range(len(mm.regions)):
	mm.iterateRegion()
	
	fmt = "'{run:1d} {lumi:9d} {evt:12d}\\t"+mm.getVariable("fmt","").replace("\\\\t","\\t")+"'"
	scenario = mm.getScenario   ()
	flags    = mm.collectFlags  ("flagDumps", False)
	procs    = mm.getProcs()

	for p in procs:
	
		output = mm.outdir +"/"+ scenario +"/dumps/"+ mm.region.name
		func.mkdir(output)
		
		tag = p.replace(".*.","").replace(".*", "").replace("*.","").rstrip("_")
		
		mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), fmt, mm.treedir, options.treename, mccs, macros, friends, "-p "+p, flags, output, tag],mm.region.name,False)

mm.runJobs()
mm.clearJobs()
