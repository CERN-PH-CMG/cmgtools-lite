from CMGTools.TTHAnalysis.treeReAnalyzer import *
import ROOT
import itertools
import PhysicsTools.Heppy.loadlibs
import math

### SF ROOT files
### Full SIM ###
eleSFname = "../python/tools/SFs/eleSF.root"
eleHname = "CBTight_MiniIso0p1_ACDV"
muSFname = "../python/tools/SFs/muonSF.root"
muHname = "MediumID_MiniIso0p2_IP3D_ACDV"

hEleSF = 0
hMuSF = 0

# Load SFs
tf = ROOT.TFile(eleSFname,"READ")
hEleSF = tf.Get(eleHname).Clone()
hEleSF.SetDirectory(0)
tf.Close()
if not hEleSF:
    print "Could not load ele SF"
    exit(0)

tf = ROOT.TFile(muSFname,"READ")
hMuSF = tf.Get(muHname).Clone()
hMuSF.SetDirectory(0)
tf.Close()
if not hMuSF:
    print "Could not load mu SF"
    exit(0)

### Full SIM ###
eleSFname = "../python/tools/SFs/sf_el_tightCB_mini01.root"
eleHname = "histo3D"
muSFname = "../python/tools/SFs/sf_mu_mediumID_mini02.root"
muHname = "histo3D"

hEleSF_FS = 0
hMuSF_FS = 0

# Load SFs
tf = ROOT.TFile(eleSFname,"READ")
hEleSF_FS = tf.Get(eleHname).Clone()
hEleSF_FS.SetDirectory(0)
tf.Close()
if not hEleSF_FS:
    print "Could not load ele SF_FS"
    exit(0)

tf = ROOT.TFile(muSFname,"READ")
hMuSF_FS = tf.Get(muHname).Clone()
hMuSF_FS.SetDirectory(0)
tf.Close()
if not hMuSF_FS:
    print "Could not load mu SF_FS"
    exit(0)


def getLepSF(lep, nPU = 1, sample = "FullSim"):

    lepPt = lep.pt#lep.p4().Et()
    lepEta = abs(lep.eta)

    if(abs(lep.pdgId) == 13): hSF = hMuSF; hSFfs = hMuSF_FS
    elif(abs(lep.pdgId) == 11): hSF = hEleSF; hSFfs = hEleSF_FS
    else: return 1,0

    # fit pt to hist
    #print hSF, hSFfs
    maxPt = hSF.GetXaxis().GetXmax()
    if lepPt > maxPt: lepPt = maxPt-0.1

    bin = hSF.FindBin(lepPt,lepEta)
    lepSF = hSF.GetBinContent(bin)
    lepSFerr = hSF.GetBinError(bin)

    if sample == "FastSim":
        maxPtfs = hSFfs.GetXaxis().GetXmax()
        if lepPt > maxPtfs: lepPt = maxPtfs-0.1

        bin = hSFfs.FindBin(lepPt,lepEta, nPU)
        lepSF *= hSFfs.GetBinContent(bin)
        lepSFerr = math.hypot(lepSFerr,hSFfs.GetBinError(bin))

    #print lep, hSF, lepPt, lepEta, bin, lepSF
    if lepSF == 0:
        print "zero SF found!"
        print lepPt, lepEta, bin, lepSF, lepSFerr
        return 1,0

    return lepSF,lepSFerr

class EventVars1L_leptonSF:
    def __init__(self):
        self.branches = [ "lepSF","lepSFerr","lepSFunc" ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        if event.isData: return ret

        sample = self.sample
        if "T1ttt" in sample: sample = "FastSim"
        else: sample = "FullSim"

        ret['lepSF'] = 1; ret['lepSFerr'] = 0; ret['lepSFunc'] = 0.5

        # get some collections from initial tree
        leps = [l for l in Collection(event,"LepGood","nLepGood")]; nlep = len(leps)
        #jets = [j for j in Collection(event,"Jet","nJet")]; njet = len(jets)

        ####################################
        # import output from previous step #
        #base = keyvals
        ####################################
        if len(base.keys()) < 1: return ret # do nothing if base is empty

        # get selected leptons
        tightLeps = []
        tightLepsIdx = base['tightLepsIdx']
        tightLeps = [leps[idx] for idx in tightLepsIdx]
        nTightLeps = len(tightLeps)

        if nTightLeps == 0: return ret
        else:
            nVtx = event.nTrueInt

            # take SF for leading lepton
            lep = tightLeps[0]
            lepSF,lepSFerr = getLepSF(lep, nVtx, sample)
            ret['lepSF'] = lepSF
            ret['lepSFerr'] = lepSFerr

        # return branches
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
