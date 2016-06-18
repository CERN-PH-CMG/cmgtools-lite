#!/usr/bin/env python
from math import *
import re, string
from CMGTools.TTHAnalysis.treeReAnalyzer import *
from CMGTools.TTHAnalysis.plotter.tree2yield import CutsFile, scalarToVector

from optparse import OptionParser
import json

parser = OptionParser(usage="usage: %prog [options] rootfile [what] \nrun with --help to get list of options")
parser.add_option("-r", "--run-range",  dest="runrange", default=(0,99999999), type="float", nargs=2, help="Run range")
parser.add_option("-c", "--cut-file",  dest="cutfile", default=None, type="string", help="Cut file to apply")
parser.add_option("-C", "--cut",  dest="cut", default=None, type="string", help="Cut to apply")
parser.add_option("-T", "--type",  dest="type", default=None, type="string", help="Type of events to select")
parser.add_option("-F", "--fudge",   dest="fudge",  default=False, action="store_true",  help="print -999 for missing variables")
parser.add_option("-m", "--mc",     dest="ismc",  default=False, action="store_true",  help="print MC match info")
parser.add_option("--mm", "--more-mc",     dest="moremc",  default=False, action="store_true",  help="print more MC match info")
parser.add_option("-j", "--json",   dest="json",  default=None, type="string", help="JSON file to apply")
parser.add_option("-n", "--maxEvents",  dest="maxEvents", default=-1, type="int", help="Max events")
parser.add_option("-f", "--format",   dest="fmt",  default=None, type="string",  help="Print this format string")
parser.add_option("-t", "--tree",          dest="tree", default='tree', help="Pattern for tree name");
parser.add_option("-E", "--events", dest="events", default=[], action="append", help="Events to select")

### CUT-file options
parser.add_option("-S", "--start-at-cut",   dest="startCut",   type="string", help="Run selection starting at the cut matched by this regexp, included.") 
parser.add_option("-U", "--up-to-cut",      dest="upToCut",   type="string", help="Run selection only up to the cut matched by this regexp, included.") 
parser.add_option("-X", "--exclude-cut", dest="cutsToExclude", action="append", default=[], help="Cuts to exclude (regexp matching cut name), can specify multiple times.") 
parser.add_option("-I", "--invert-cut",  dest="cutsToInvert",  action="append", default=[], help="Cuts to invert (regexp matching cut name), can specify multiple times.") 
parser.add_option("-R", "--replace-cut", dest="cutsToReplace", action="append", default=[], nargs=3, help="Cuts to invert (regexp of old cut name, new name, new cut); can specify multiple times.") 
parser.add_option("-A", "--add-cut",     dest="cutsToAdd",     action="append", default=[], nargs=3, help="Cuts to insert (regexp of cut name after which this cut should go, new name, new cut); can specify multiple times.") 
parser.add_option("--enable-cut", dest="cutsToEnable", action="append", default=[], help="Cuts to enable if they were disabled in the cut file (regexp matching cut name), can specify multiple times.") 
parser.add_option("--s2v", "--scalar2vector",     dest="doS2V",    action="store_true", default=False, help="Do scalar to vector conversion") 
 
(options, args) = parser.parse_args()

if options.cut and options.cutfile: raise RuntimeError, "You can't specify both a cut and a cutfile"

jsonmap = {}
if options.json:
    J = json.load(open(options.json, 'r'))
    for r,l in J.iteritems():
        jsonmap[long(r)] = l
    stderr.write("Loaded JSON %s with %d runs\n" % (options.json, len(jsonmap)))

def testJson(ev):
    try:
        lumilist = jsonmap[ev.run]
        for (start,end) in lumilist:
            if start <= ev.lumi and ev.lumi <= end:
                return True
        return False
    except KeyError:
        return False

class BaseDumper(Module):
    def __init__(self,name,options=None,booker=None):
        Module.__init__(self,name,booker)
        self.options = options
    def preselect(self,ev):
        if self.options.events and ( (ev.run, ev.lumi, ev.evt) not in self.options.events ):
            return False
        return True
    def analyze(self,ev):
        if self.options.events and ( (ev.run, ev.lumi, ev.evt) not in self.options.events ):
            return False
        if self.options.fmt: 
            print string.Formatter().vformat(options.fmt.replace("\\t","\t"),[],ev)
            return True
        print "run %6d lumi %4d event %11d : met %.1f ht %.1f central jets %d (CSV loose %d, CSV medium %d) leptons %d/%d taus %d/%d" % (
                ev.run, ev.lumi, ev.evt, ev.met_pt, ev.htJet20j, ev.nJet, ev.nBJetsLoose20, ev.nBJetsMedium20, ev.nLepGood, ev.nLepOther, ev.nTauGood, getattr(ev,'nTauOther',0))
        lepsg = Collection(ev,"LepGood","nLepGood") 
        lepsb = Collection(ev,"LepOther","nLepOther") 
        tausg = Collection(ev,"TauGood","nTauGood") 
        tausb = Collection(ev,"TauOther","nTauOther") if hasattr(ev, "nTauOther") else []
        jets = Collection(ev,"Jet","nJet") 
        ivfs = Collection(ev,"SV","nSV") 
        for i,(lt,l) in enumerate([("good",l) for l in lepsg] + [("bad ",l) for l in lepsb]):
            print "    lep %s %d: id %+2d pt %5.1f eta %+4.2f phi %+4.2f  id %d/% d  miniRelIso %6.3f sip3d %5.2f dxy %+4.3f dz %+4.3f  lostHits %d " % (
                    lt, i+1, l.pdgId,l.pt,l.eta,l.phi, l.looseIdOnly,l.tightId, l.miniRelIso, l.sip3d, l.dxy, l.dz, l.lostHits),
            if self.options.ismc:
                print "   mcMatch %8d/%d mcGamma %d" % (l.mcMatchId, l.mcMatchAny, l.mcPromptGamma),
            print ""
            #if abs(l.pdgId) == 11:
            #    print "   tightId %d mvaId %5.3f misHit %d conVeto %d tightCh %d mvaIdTrig %5.3f" % (l.tightId, l.mvaId, l.lostHits, l.convVeto, l.tightCharge, l.mvaIdTrig)
            #else:
            #    print "   tightId %d lostHits %2d tightCh %d" % (l.tightId, l.lostHits, l.tightCharge)
        for i,(lt,l) in enumerate([("good",l) for l in tausg] + [("bad ",l) for l in tausb]):
            print "    tau %s %d: id %+2d pt %5.1f eta %+4.2f phi %+4.2f   decModeId %d/%d idMVA %d idMVANew %d   dxy %+4.3f dz %+4.3f " % (
                    lt, i+1, l.pdgId,l.pt,l.eta,l.phi, l.idDecayMode, l.idDecayModeNewDMs, l.idMVA,l.idMVANewDM, l.dxy, l.dz),
            if self.options.ismc: print "   mcMatch %+3d" % l.mcMatchId,
            print ""
        for i,j in enumerate(jets):
            print "    jet %d:  pt %6.1f eta %+4.2f phi %+4.2f   btag %4.3f  dPhi(j,MET) %+4.2f MT(j,MET) %6.1f   raw pt %6.1f " % (
                     i+1, j.pt, j.eta, j.phi, min(1.,max(0.,j.btagCSV)), deltaPhi(j.phi,ev.met_phi), sqrt(2*j.pt*ev.met_pt*(1-cos(j.phi-ev.met_phi))), j.rawPt),
            if self.options.ismc:
                print "  mcMatch %8d/%d mcPt %5.1f" % (j.mcMatchId, j.hadronFlavour, j.mcPt),
            print ""
        for i,ivf in enumerate(ivfs):
            print "    IVF %d:  pt %5.1f eta %+4.2f phi %+4.2f  mass %4.1f  ntracks %1d  chi2/ndf %5.1f/%5.1f  cos(theta) % .3f  dxy %4.3f  ip3d %6.3f  sip2d %4.1f  sip3d %4.1f  jet pt %6.1f dR %.2f  dPhi(ivf,MET) %+4.2f  MT(ivf,MET)%6.1f   dR(ivf,ISR) %4.2f  MT(ivf,ISR) %6.1f " % (
                     i+1, ivf.pt, ivf.eta, ivf.phi, ivf.mass, ivf.ntracks, ivf.chi2, ivf.ndof, ivf.cosTheta, ivf.dxy, ivf.ip3d, ivf.dxy/ivf.edxy, ivf.sip3d,
                             ivf.jetPt, ivf.jetDR,
                             deltaPhi(ivf.phi,ev.met_phi), sqrt(2*ivf.pt*ev.met_pt*(1-cos(ivf.phi-ev.met_phi))),
                             deltaR(ivf.eta,ivf.phi,ev.ISRJet_eta,ev.ISRJet_phi) if ev.ISRJet_pt > 0 else 0, 
                             sqrt(2*ivf.pt*ev.ISRJet_pt*(1-cos(ivf.phi-ev.ISRJet_phi))) if ev.ISRJet_pt > 0 else 0),
            if self.options.ismc:
                print "  mcMatch %d/%d mcFlav %d/%d" % (ivf.mcMatchNTracks, ivf.mcMatchNTracksHF, ivf.mcFlavFirst,ivf.mcFlavHeaviest),
            print ""
        print "    met %6.2f (phi %+4.2f)  ht %.1f mht %6.2f" % (ev.met_pt, ev.met_phi, ev.htJet20j, ev.mhtJet20)
        print "    primary vertices %d (first is good? %s)" % (ev.nVert, ev.firstPVIsGood != 0)
        print ""
        print ""
        print ""

cut = None
if options.cutfile:
    cut = CutsFile(options.cutfile,options).allCuts()
elif options.cut:
    cut = options.cut
if options.doS2V:
    cut = scalarToVector(cut)
if options.events:
    rles = []
    for ids in options.events:
        for i in ids.split(","):
            (r,l,e) = map(int, i.strip().split(":"))
            rles.append((r,l,e))
    options.events = rles
 
file = ROOT.TFile.Open(args[0])
tree = file.Get(options.tree)
tree.vectorTree = True 
dumper = BaseDumper("dump", options)
el = EventLoop([dumper])
el.loop(tree,options.maxEvents,cut=cut)

