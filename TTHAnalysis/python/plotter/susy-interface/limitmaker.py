from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--perBin",  dest="perBin", action="store_true", default=False, help="Run every value of the bin separately.")

base = "python makeShapeCardsSusy.py {MCA} {CUTS} \"{EXPR}\" \"{BINS}\" {SYS} -o SR -P {T} --tree {TREENAME} {MCCS} {MACROS} --neg --s2v -f -j 4 -l {LUMI} --od {O} {FRIENDS} {PROCS} {FLAGS}"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker(base, args, options)

scenario = mm.getScenario()
sl = str(options.lumi)

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	
flags   = mm.collectFlags  ("flagsLimits")

for r in range(len(mm.regions)):
	mm.iterateRegion()

	procs   = mm.getProcs()	
	binnings = [mm.getVariable("bins","")] if not options.perBin else func.getAllBins(mm.getVariable("bins",""))
	
	for ib,b in enumerate(binnings):
	
		if options.perBin: 
			sl += "_"+b.replace(".","p")
			mm.useVar("bins", b)
	
		output = mm.outdir +"/"+ scenario +"/cards"+ sl.replace(".","p") +"/"+ mm.region.name
		func.mkdir(output)
	
		flags += " "+mm.getExprCut()
		
		mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("expr",""), mm.getVariable("bins",""), mm.getVariable("sysfile",""), mm.treedir, options.treename, mccs, macros, options.lumi, output, friends, procs, flags], mm.region.name)







