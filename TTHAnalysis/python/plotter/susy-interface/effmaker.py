from optparse import OptionParser
from lib import maker
from lib import functions as func

parser = OptionParser(usage="%prog cfg regions treedir outdir [options]")
parser = maker.addMakerOptions(parser)
parser.add_option("--perBin"     , dest="perBin", type="string", default=None, help="Run every value of the bin separately.")
parser.add_option("-n", "--num", dest="num", action="store_true", default=False, help="Only total yield")

dimensions to vary
* numerator
* denominator / additional cuts
* processes
* signals
* xvar (binning)

run these variations in two dimensions
* group by cut     -> for every num / den variation vary the sig/processes
* group by process -> for every sig / proc variation vary the num/den
* both dimensions done in a third dimension: xvar

--xvars
--dens
--nums
--sigs
--procs

output = mm.outdir +"/"+ scenario +"/effs"+ sl.replace(".","p") +"/"+ mm.region.name +"/"+ xvar +"/"+ procs per cut

base = "python mcEfficiencies.py {MCA} {CUTS} {NUMS} {XVARS} -P {T} --neg --s2v --tree {TREENAME} {GROUPING} -j 4 --cmsprel '{LSPAM}' --legendWidth 0.20 --legendFontSize 0.035 --showRatio --ratioRange 0.0 1.99 --ytitle '{NAME}' --legend=TR {MCCS} {MACROS} -l {LUMI} -o {O} --sp {SIG} --sP {NUM} --sP {XVAR} {FRIENDS} {PROCS} {FLAGS}"
(options, args) = parser.parse_args()
options = maker.splitLists(options)
mm      = maker.Maker(baseAll, args, options)

scenario = mm.getScenario()
sl = str(options.lumi)

output = mm.outdir +"/"+ scenario +"/effs"+ sl.replace(".","p") +"/"+ mm.region.name
func.mkdir(output)

friends = mm.collectFriends()	
mccs    = mm.collectMCCs   ()
macros  = mm.collectMacros ()	
flags   = mm.collectFlags  ("flagsEffs")

for r in range(len(mm.regions)):
	mm.iterateRegion()

	procs   = mm.getProcs()
	final   = "-f" if options.final else ""

## logical things
compare cuts for given process
compare processes for given cut

ingredients
* group by (grouping = cut (then no -f) or process)
* --sP numerator
* --sP xvar
* --sp signal
	
	mm.submit([mm.getVariable("mcafile"), mm.getVariable("cutfile"), mm.treedir, options.treename, final, mccs, macros, options.lumi, friends, procs, flags, output, "effmap_%s_%s.txt"%(scenario,mm.region.name)])





num = "mvaM"
sig = "TT_red"
out = "/afs/cern.ch/user/c/cheidegg/www/heppy/2016-06-06_ewkfakerates_AJ40_" + num
tree = "/mnt/t3nfs01/data01/shome/cheidegg/o/2016-06-02_ewktrees76X_1LL/"

dens = [
        #["ra7FO", "-A pt den ''"],
        ["CBloose" , "-A ^pt den '(abs(LepGood_pdgId) == 11 && mvaDenEl) || (abs(LepGood_pdgId) == 13 && mvaDenMu)'"],
       ]

base = "python mcEfficiencies.py susy-multilepton/ewk_fakerate/mca_ewkino.txt susy-multilepton/ewk_fakerate/cuts_ewkino.txt susy-multilepton/ewk_fakerate/nums_ewkino.txt susy-multilepton/ewk_fakerate/xvars_ewkino.txt -P {TREE} --mcc susy-multilepton/ewk_fakerate/mcc_ewkino.txt --s2v --tree treeProducerSusyMultilepton --legend=TR --showRatio --ratioRange 0.0 1.99 --ytitle 'Fake Rate' -j 8 --groupBy cut -o {OUT} -p {PROC} --sp {SIG} {DEN} {BIN} --sP {NUM} --sP {VAR}"

baseAll = "python mcAnalysis.py {MCA} {CUTS} -P {T} --neg --s2v --tree {TREENAME} {FINAL} -j 8 {MCCS} {MACROS} -l {LUMI} {FRIENDS} {PROCS} {FLAGS} >> {O}/{FILENAME}"




pathStruct = "{out}_{den}/{flavor}/{what}/{flavor}_{what}_{den}_{bin}.root"

etaEl = [
         ["eta_00_08", "-A ^pt eta 'abs(LepGood_eta) < 0.8'"],
         ["eta_08_15", "-A ^pt eta 'abs(LepGood_eta) >= 0.8   && abs(LepGood_eta) < 1.479'"],
         ["eta_15_25", "-A ^pt eta 'abs(LepGood_eta) >= 1.479 && abs(LepGood_eta) < 2.5'"  ],
        ]

etaMu = [
         ["eta_00_12", "-A ^pt eta 'abs(LepGood_eta) < 1.2'"],
         ["eta_12_21", "-A ^pt eta 'abs(LepGood_eta) >= 1.2 && abs(LepGood_eta) < 2.1'"],
         ["eta_21_24", "-A ^pt eta 'abs(LepGood_eta) >= 2.1 && abs(LepGood_eta) < 2.4'"],
        ]

ptLep = [
         ["pt_10_15", "-A ^pt ptBin 'if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) >= 10 && if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) < 15'"],
         ["pt_15_25", "-A ^pt ptBin 'if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) >= 15 && if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) < 25'"],
         ["pt_25_35", "-A ^pt ptBin 'if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) >= 25 && if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) < 35'"],
         ["pt_35_50", "-A ^pt ptBin 'if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) >= 35 && if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) < 50'"],
         ["pt_50_70", "-A ^pt ptBin 'if3(mvaWpM,LepGood_pt,0.7*LepGood_pt/LepGood_jetPtRatiov2) >= 50'"                   ],
        ]

procEl = [
          #"TT_red,QCDEl_red",
          "TT_red,TT_bjets,QCDEl_red,QCDEl_bjets"
         ]

procMu = [
          #"TT_red,QCDMu_red",
          "TT_red,TT_bjets,QCDMu_red,QCDMu_bjets"
         ]

flav = [
        #name, cut, list containing pt binning, list containing eta binning, xvar for pt, xvar for eta
        ["el", "-I mu", "procEl", "ptLep", "etaEl", "conePtVarCB", "etaElVar"],
        ["mu", ""     , "procMu", "ptLep", "etaMu", "conePtVarCB", "etaMuVar"]
       ]


for den in dens:
	for what in ["pt", "eta"]:
		for f in flav:
			for proc in globals()[f[2]]: 
				binning = globals()[f[3]]; var = f[6]
				if what == "eta": binning = globals()[f[4]]; var = f[5]
				for bin in binning:
					path = pathStruct.format(out=out, den=den[0], flavor=f[0], what=what, bin=bin[0])
					full = base.format(TREE=tree, OUT=path, PROC=proc, SIG=sig, DEN=den[1], BIN=bin[1], NUM=num, VAR=var)
