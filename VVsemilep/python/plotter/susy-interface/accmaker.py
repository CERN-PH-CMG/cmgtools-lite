from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--perBin"     , dest="perBin", type="string", default=None, help="Run every value of the bin separately.")
parser.add_option("-f", "--final", dest="final" , action="store_true", default=False, help="Only total yield")
parser.add_option("--fom",         dest="fom"   , type="string", default=None, help="Figure of merit (S/B, S/sqrB, S/sqrSB)")

baseAll = "python mcAnalysis.py {MCA} {CUTS} -P {T} --neg --s2v --tree {TREENAME} {FINAL} {MCCS} {MACROS} -l {LUMI} {FRIENDS} {PROCS} {FLAGS} {FOM} >> {O}/{FILENAME}"
baseBin = "python mcPlots.py {MCA} {CUTS} {PLOTFILE} -P {T} --neg --s2v --tree {TREENAME} {FINAL} {MCCS} {MACROS} -l {LUMI} --pdir {O} {FRIENDS} {PROCS} {PLOTS} {FLAGS} --perBin --print txt"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("accmaker", baseAll, args, options)
if options.perBin: mm.reloadBase(baseBin)

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	
sl = str(options.lumi)

for r in range(len(mm.regions)):
	mm.iterateRegion()

	output = mm.outdir +"/"+ scenario +"/accs"+ sl.replace(".","p") +"/"+ mm.region.name
	func.mkdir(output)
	
	scenario = mm.getScenario()
	flags    = mm.collectFlags  ("flagsAccs")
	
	procs   = mm.collectProcs()
	final   = "-f" if options.final else ""
	fom     = options.fom if options.fom else ""
	
	if options.perBin:
		mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("plotfile",""), mm.treedir, options.treename, final, mccs, macros, options.lumi, output, friends, procs, options.perBin, flags],mm.region.name,False)
	else:
		mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.treedir, options.treename, final, mccs, macros, options.lumi, friends, procs, flags, fom, output, "accmap_%s_%s.txt"%(scenario,mm.region.name)],mm.region.name,False)

mm.runJobs()
mm.clearJobs()



