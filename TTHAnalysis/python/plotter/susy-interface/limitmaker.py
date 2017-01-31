import os
from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--perBin"  ,  dest="perBin"  , action="store_true", default=False, help="Run every value of the bin separately.")
parser.add_option("--finalize",  dest="finalize", action="store_true", default=False, help="After running, tidy up output directory like scanmaker")

base = "python makeShapeCardsSusy.py {MCA} {CUTS} \"{EXPR}\" \"{BINS}\" {SYS} -o SR -P {T} --tree {TREENAME} {MCCS} {MACROS} --neg --s2v -f -l {LUMI} --od {O} {FRIENDS} {PROCS} {FLAGS}"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker("limitmaker", base, args, options)

sl = str(options.lumi)

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	
outDirs = []

for r in range(len(mm.regions)):
	mm.iterateRegion()

	scenario = mm.getScenario()
	flags    = mm.collectFlags  ("flagsLimits")
	procs    = " ".join(["-p "+b for b in mm.getProcs()])
	binnings = [mm.getVariable("bins","")] if not options.perBin else func.getAllBins(mm.getVariable("bins",""))
	
	for ib,b in enumerate(binnings):
	
		if options.perBin: 
			sl += "_"+b.replace(".","p")
			mm.useVar("bins", b)
	
		output = mm.outdir +"/"+ scenario +"/"+ mm.region.name + "/"+ sl.replace(".","p") +"fb"
		outDirs.append(output)
		func.mkdir(output)
	
		flags += " "+mm.getExprCut()
		
		mm.submit([mm.getVariable("mcafile",""), mm.getVariable("cutfile",""), mm.getVariable("expr",""), mm.getVariable("bins",""), mm.getVariable("sysfile",""), mm.treedir, options.treename, mccs, macros, options.lumi, output, friends, procs, flags], mm.region.name, False)

mm.runJobs()
mm.clearJobs()

if options.finalize:
	for output in outDirs:
		for d in os.listdir(output):
			path = output +"/"+d
			if d in ["index.php", "common"]: continue
			if not os.path.exists(path+"/SR.card.txt"): continue
			model = "_".join(d.split("_")[:-2])
			mp    = "_".join(d.split("_")[-2:])
			if not os.path.isdir(output+"/"+model): os.system("mkdir -p "+output+"/"+model+"/mps")
			os.system("mkdir -p "+output+"/"+model+"/mps/"+mp+"/common")
			os.system("mv "+path+" "+output+"/"+model+"/mps/"+mp+"/sig_"+d)
			os.system("cp "+output+"/common/SR.input.root "+output+"/"+model+"/mps/"+mp+"/common")
	

