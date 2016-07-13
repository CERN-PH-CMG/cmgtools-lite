#!/usr/bin/env python
from math import *
import re, string
from CMGTools.TTHAnalysis.treeReAnalyzer import *

from optparse import OptionParser
import json

parser = OptionParser(usage="usage: %prog [options] rootfile [what] \nrun with --help to get list of options")
parser.add_option("-r", "--run-range",  dest="runrange", default=(0,99999999), type="float", nargs=2, help="Run range")
parser.add_option("-c", "--cut-file",  dest="cutfile", default=None, type="string", help="Cut file to apply")
parser.add_option("-C", "--cut",  dest="cut", default=None, type="string", help="Cut to apply")
parser.add_option("-T", "--type",  dest="type", default="zz", type="string", help="Type of events to print (for -f)")
parser.add_option("--jet-cleaning", dest="jetCleaning", default="candidate", help="Jet cleaning (candidate or event)")
parser.add_option("-F", "--fudge",   dest="fudge",  default=False, action="store_true",  help="print -999 for missing variables")
parser.add_option("-m", "--mc",     dest="ismc",  default=False, action="store_true",  help="print MC match info")
parser.add_option("-M", "--more",     dest="ismore",  default=False, action="store_true",  help="print more info")
parser.add_option("--mm", "--more-mc",     dest="moremc",  default=False, action="store_true",  help="print more MC match info")
parser.add_option("--tau", dest="tau",  default=False, action="store_true",  help="print Taus")
parser.add_option("-j", "--json",   dest="json",  default=None, type="string", help="JSON file to apply")
parser.add_option("-n", "--maxEvents",  dest="maxEvents", default=-1, type="int", help="Max events")
parser.add_option("-f", "--format",   dest="fmt",  default=None, type="string",  help="Print this format string")
parser.add_option("-t", "--tree",          dest="tree", default='tree', help="Pattern for tree name");
parser.add_option("-E", "--events", dest="events", default=[], action="append", help="Events to select")

(options, args) = parser.parse_args(); sys.argv = []

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

def findLepIndex(leps,pt,eta):
    for il,l in enumerate(leps):
        if abs(l.pt-pt)<1e-5 and abs(l.eta-eta)<1e-5:
            return il
    return -1
class BaseDumper(Module):
    def __init__(self,name,options=None,booker=None):
        Module.__init__(self,name,booker)
        self.options = options
    def preselect(self,ev):
        return True
    def makeVars(self,ev,zzkind="zz"):
        jets = Collection(ev,"Jet")
        ev.Jet1_pt_zs = jets[0].pt if len(jets) > 0 else -1.0
        ev.Jet2_pt_zs = jets[1].pt if len(jets) > 1 else -1.0
        if zzkind == "zzfast": 
            ev.category = -1
            ev.nJet30ZZ = ev.nJet30 
            return
        allleps = Collection(ev,"Lep","nLep") 
        zzs = Collection(ev,zzkind,"n"+zzkind)
        if len(zzs) == 0:
            ev.category = -1
            return
        zz = zzs[0]
        if self.options.jetCleaning == "candidate":
            myjetIndices = [ getattr(zz,"ij%d" % i) for i in xrange(1,10) ]
            ev.jetIndicesZZ = [ i for i in myjetIndices if i >= 0 ]
            jets = [ jets[i] for i in ev.jetIndicesZZ ]
            ev.nJet30ZZ = zz.nJet30 #len(jets)
            ev.Jet1_pt_zs = jets[0].pt if len(jets) > 0 else -1.0
            ev.Jet2_pt_zs = jets[1].pt if len(jets) > 1 else -1.0
        elif self.options.jetCleaning == "event":
            ev.jetIndicesZZ = range(ev.nJet30)
            ev.nJet30ZZ = ev.nJet30 
        ils = [ findLepIndex(allleps, zz.z1_l1_pt, zz.z1_l1_eta),
                findLepIndex(allleps, zz.z1_l2_pt, zz.z1_l2_eta),
                findLepIndex(allleps, zz.z2_l1_pt, zz.z2_l1_eta),
                findLepIndex(allleps, zz.z2_l2_pt, zz.z2_l2_eta) ]
        lepsS = []
        for i,l in enumerate(allleps):
            if i in ils: 
                lepsS.append(l)
            elif l.tightId and l.relIsoAfterFSR < 0.35 and l.sip3d < 4:
                lepsS.append(l)
        ev.nLepSel = len(lepsS)
        ev.mjj = (jets[0].p4()+jets[1].p4()).M() if len(jets) >= 2 else 0
        ev.Djet = 0.18*abs(jets[0].eta-jets[1].eta) + 1.92e-04*ev.mjj if len(jets) >= 2 else 0
        ev.nB = sum([(j.btagCSV > 0.89 and j.pt > 30) for j in jets]) if len(jets) else 0
        jets40c = [ j for j in jets if j.pt > 40 and abs(j.eta) < 2.4 ]
        ev.nJet40c = len(jets40c)
        ev.vhjjTags = 0; ev.mjj40c = 0
        if len(jets40c) >= 2:
            for i1,j1 in enumerate(jets40c[:-1]):
                for j2 in jets40c[i1+1:]:
                   mjj40c = (j1.p4()+j2.p4()).M()
                   if 60 < mjj40c and mjj40c < 120:
                        ev.vhjjTags += 1
                        if abs(mjj40c - 90) < abs(ev.mjj40c - 90):
                            ev.mjj40c = mjj40c
        if ev.nLepSel == 4 and ev.nJet30 >= 2 and ev.nB <= 1 and ev.Djet > 0.5:
          ev.category = 2
        elif ev.nLepSel == 4 and ev.nJet40c >= 2 and (60 < ev.mjj40c and ev.mjj40c < 120) and zz.pt > zz.mass:
          ev.category = 4
        elif ev.nLepSel == 4 and ev.nJet30ZZ == 2 and ev.nB == 2:
          ev.category = 4
        elif ev.nLepSel >= 5 and ev.nJet30ZZ <= 2 and ev.nB == 0:
          ev.category = 3
        elif ev.nJet30ZZ >= 3 and ev.nB >= 1:
          ev.category = 5
        elif ev.nLepSel >= 5:
          ev.category = 5
        elif ev.nJet30ZZ >= 1:
          ev.category = 1
        else:
          ev.category = 0
    def analyze(self,ev):
        if self.options.events and ( (ev.run, ev.lumi, ev.evt) not in self.options.events ):
            return False
        try:
            if options.type != "asis": self.makeVars(ev,zzkind=options.type)
        except:
            raise
            pass
        if self.options.fmt: 
            print string.Formatter().vformat(options.fmt.replace("\\t","\t"),[],ev)
            return True
        leps = Collection(ev,"Lep","nLep") 
        jets = Collection(ev,"Jet")
        print "run %6d lumi %4d event %11d (id: %d:%d:%d) " % (ev.run, ev.lumi, ev.evt, ev.run, ev.lumi, ev.evt)
        for i,l in enumerate(leps):
            print "    lepton %d: id %+2d pt %5.1f eta %+4.2f phi %+4.2f   tightId %d relIso %5.3f sip3d %5.2f dxy %+4.3f dz %+4.3f bdt %+6.4f lostHits %1d fsr %1d/%1d" % (
                    i+1, l.pdgId,l.pt,l.eta,l.phi, l.tightId, l.relIsoAfterFSR, l.sip3d, l.dxy, l.dz, l.mvaIdSpring16, l.lostHits, l.hasFSR, l.hasOwnFSR),
            if self.options.ismc:
                print "   mcMatch id %+4d, any %+2d" % (l.mcMatchId, l.mcMatchAny),
            if abs(l.pdgId) == 13:
                print "   pog loose %d trkHighPt %d stations %d, layers %d, pixels %d, glb %d" % (l.muIdLoose, l.muIdTrkHighPt, l.nStations, l.trackerLayers, l.pixelLayers, l.globalTrackChi2>0),
            if abs(l.pdgId) == 11:
                print "   etaSc %+6.4f spring15 bdt %+6.4f" % (l.etaSc, l.mvaIdSpring15),
            print ""
            if self.options.ismore:
                print "\t\t iso 04 ch %5.2f nh %5.2f ph %5.2f pu %5.2f rho %5.2f ea %4.3f preFSR %5.3f" % ( l.chargedHadIso04, l.neutralHadIso04, l.photonIso04, l.puChargedHadIso04, l.rho, l.EffectiveArea04, l.relIso04 )
                print "\t\t iso 03 ch %5.2f nh %5.2f ph %5.2f pu %5.2f rho %5.2f ea %4.3f preFSR %5.3f" % ( l.chargedHadIso03, l.neutralHadIso03, l.photonIso03, l.puChargedHadIso03, l.rho, l.EffectiveArea03, l.relIso03 )
                if self.options.ismc:
                    print "\t\t promptLep %d promptTau %d promptPho %d anyPho %d" % (l.mcPrompt, l.mcPromptTau, l.mcPromptGamma, l.mcGamma)
        for i,j in enumerate(jets):
            print "    jet %d:  pt %5.1f uncorrected pt %5.1f eta %+4.2f phi %+4.2f  btag %4.3f qgl %.3f " % (i+1, j.pt, j.rawPt, j.eta, j.phi, min(1.,max(0.,j.btagCSV)), j.qgl),
            if self.options.ismc:
                print "  mcMatch %2d mcFlavour %2d mcPt %5.1f" % (j.mcMatchId, j.hadronFlavour, j.mcPt),
            print ""
        fsr = Collection(ev, "FSR")
        for i,g in enumerate(fsr):
            print "    photon %d: pt %5.1f eta %+4.2f phi %+4.2f reliso% 7.3f (ch %5.1f nh %5.1f ph %5.1f pu %5.1f), closest lepton id %+2d pt %5.1f eta %+4.2f phi %+4.2f dr %.4f dr/et2 %.4f" % (i+1, 
                        g.pt, g.eta, g.phi, g.relIso, g.chargedHadIso, g.neutralHadIso, g.photonIso, g.puChargedHadIso, g.closestLepton_pdgId, g.closestLepton_pt, g.closestLepton_eta, g.closestLepton_phi, g.closestLeptonDR, g.closestLeptonDR/(g.pt*g.pt))

        for type in "zz", "zz2P2F", "zz3P1F", "zzSS", "zzRelII":
            zzs = Collection(ev,type)
            self.makeVars(ev,zzkind=type)
            if len(zzs):
                print "    four-lepton candidates of type %s" % type
            for izz,zz in enumerate(zzs):
                ils = [ findLepIndex(leps, zz.z1_l1_pt, zz.z1_l1_eta),
                        findLepIndex(leps, zz.z1_l2_pt, zz.z1_l2_eta),
                        findLepIndex(leps, zz.z2_l1_pt, zz.z2_l1_eta),
                        findLepIndex(leps, zz.z2_l2_pt, zz.z2_l2_eta) ]
                ifsr11 = findLepIndex(fsr, zz.z1_l1_pho_pt, zz.z1_l1_pho_eta) if zz.z1_l1_hasFSR else -1
                ifsr12 = findLepIndex(fsr, zz.z1_l2_pho_pt, zz.z1_l2_pho_eta) if zz.z1_l2_hasFSR else -1
                ifsr21 = findLepIndex(fsr, zz.z2_l1_pho_pt, zz.z2_l1_pho_eta) if zz.z2_l1_hasFSR else -1
                ifsr22 = findLepIndex(fsr, zz.z2_l2_pho_pt, zz.z2_l2_pho_eta) if zz.z2_l2_hasFSR else -1
                print "      candidate %1d: leptons %d %d %d %d, mass %6.3f mz1 %6.3f mz2 %6.3f , Z1 FSR %d %d Z2 FSR %d %d " % (
                        izz, ils[0]+1,ils[1]+1,ils[2]+1,ils[3]+1, zz.mass, zz.z1_mass, zz.z2_mass, ifsr11+1, ifsr12+1, ifsr21+1, ifsr22+1 )
                print "                   jets:", " ".join(str(i+1) for i in ev.jetIndicesZZ)
                print "                   m12 %6.3f  m13 %6.3f  m14 %6.3f  m23 %6.3f  m24 %6.3f  m34 %6.3f" % (
                         zz.mll_12, zz.mll_13, zz.mll_14, zz.mll_23, zz.mll_24, zz.mll_34)
                print "                   D_bkg^kin %.3f D_bkg %.3f D_gg %.3f D_0- %.3f D_HJJ^VBF %.3f " % (
                          zz.D_bkg_kin, zz.D_bkg, zz.D_gg, zz.D_0m, zz.Dkin_HJJ_VBF)
                print "                   pt4l %6.1f mjj %6.1f Djet %.3f nLepSel %d nJet30 %d nB %d nJet40c %d, mjj40c %6.1f: category %d" % (
                          zz.pt, ev.mjj, ev.Djet, ev.nLepSel, ev.nJet30ZZ, ev.nB, ev.nJet40c, ev.mjj40c, ev.category)
        print "    met %6.2f (phi %+4.2f)" % (ev.met_pt, ev.met_phi)
        print "    vertices %d" % (ev.nVert)
        print "    HLT: ", " ".join([t for t in "DoubleMu DoubleEl MuEG TripleEl TripleMu DoubleMuEl DoubleElMu SingleEl SingleMu Signal".split() if getattr(ev,"HLT_"+t)])
        print ""

cut = None
if options.cut:
    cut = options.cut
if options.events:
    rles = []
    for ids in options.events:
        for i in ids.split(","):
            (r,l,e) = map(int, i.strip().split(":"))
            rles.append((r,l,e))
    options.events = rles
file = ROOT.TFile.Open(args[0])
tree = file.Get(options.tree)
tree.vectorTree = False
dumper = BaseDumper("dump", options)
el = EventLoop([dumper])
el.loop(tree,options.maxEvents,cut=cut)

