from optparse import OptionParser
from lib import maker
from lib import functions as func

def collectProcesses(region):
	bkgs = " ".join(["-p "+b for b in region.bkgs])
	sigs = " ".join(["-p "+s for s in region.sigs])
	return sigs+" "+bkgs

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--perBin"     , dest="perBin", action="store_true", default=False, help="Run every value of the bin separately.")
parser.add_option("-f", "--final", dest="final" , action="store_true", default=False, help="Only total yield")

baseAll = "python mcAnalysis.py {MCA} {CUTS} -P {T} --neg --s2v --tree {TREENAME} {FINAL} -j 8 {MCCS} {MACROS} -l {LUMI} {FRIENDS} {PROCS} {FLAGS} >> {O}/{FILENAME}"
baseBin = "python mcPlots.py {MCA} {CUTS} {PLOTFILE} -P {T} --neg --s2v --tree {TREENAME} {FINAL} -j 4 {MCCS} {MACROS} -l {LUMI} --pdir {O} {FRIENDS} {PROCS} {PLOTS} {FLAGS} --perBin --print txt"
(options, args) = parser.parse_args()
mm = maker.Maker(baseAll, args, options)
if options.perBin: mm.reloadBase(baseBin)

scenario = mm.getScenario()
sl = str(options.lumi)

output = mm.outdir +"/"+ scenario +"/effs"+ sl.replace(".","p") +"/"+ mm.region.name
func.mkdir(output)

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	
flags   = mm.collectFlags  ("flagsEffs")

procs   = collectProcesses(mm.region)
final   = "-f" if options.final else ""

if options.perBin:
	mm.submit([mm.getVariable("mcafile"), mm.getVariable("cutfile"), mm.getVariable("plotfile"), mm.treedir, options.treename, final, mccs, macros, options.lumi, output, friends, procs, mm.getVariable("expr"), flags])
else:
	mm.submit([mm.getVariable("mcafile"), mm.getVariable("cutfile"), mm.treedir, options.treename, final, mccs, macros, options.lumi, friends, procs, flags, output, "effmap_%s_%s.txt"%(scenario,mm.region.name)])




