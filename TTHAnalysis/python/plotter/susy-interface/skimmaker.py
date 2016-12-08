import datetime, sys
from optparse import OptionParser
from lib import maker
from lib import functions as func

def makeDummyMCA(m, samples, allSamples):
	path = m.tmpdir+"/"+func.timestamp(False)+".txt"
	s = samples if len(samples)>0 and not allSamples else m.getAllSamples(allSamples)
	f = open(path,"w")
	for p in s:
		f.write(p +" : "+ p + ": 1.0")
	f.close()
	return path

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--json"   , dest="json"   , type="string", default=None, help="Regexp of the JSON file you want to use to skim your tree")
parser.add_option("--samples", dest="samples", type="string", action="append", default=[], help="Only use these samples in the skimming and ignore procs, bkgs and sigs")
parser.add_option("--allSamples", dest="allSamples", action="store_true", default=False, help="Skim all samples in the MCA")

base = "python skimTrees.py {MCA} {CUTS} {O} -P {T} --tree {TREENAME} {MCCS} {MACROS} {FRIENDS} {JSON}"
baseFriends = "python skimFTrees.py {T} {F} {O}" 

(options, args) = parser.parse_args()
options         = maker.splitLists(options)
options.samples = func.splitList(options.samples)
mm              = maker.Maker("skimmaker", base, args, options)

## skim main tree
friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	

for r in range(len(mm.regions)):
	mm.iterateRegion()
	mm.reloadBase(base)

	mca     = makeDummyMCA(mm, options.samples, options.allSamples)
	
	output = mm.outdir
	func.mkdir(output)
	json = options.json if options.json else ""
	
	base = "python skimTrees.py {MCA} {CUTS} {O} -P {T} --tree {TREENAME} -j 4 {MCCS} {MACROS} {FRIENDS} {JSON}"
	mm.submit([mca, mm.getVariable("cutfile",""), output, mm.treedir, options.treename, mccs, macros, friends, json],"main",True)

	## skim friend trees
	mm.reloadBase(baseFriends)
	fs, fm = mm.getFriendLocations()
	
	for i,f in enumerate(fs):
	
		#output = mm.outdir+"/"+fm[i]
		func.mkdir(output)
	
		mm.submit([mm.outdir, f, mm.outdir],"friend_"+f,False)
	mm.runJobs()
	mm.clearJobs()


