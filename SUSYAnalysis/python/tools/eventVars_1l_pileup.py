from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

# mc to data pu weight
def getPUdict(fname, puHistName = "puRatio"):
    puDict = {}

    puFile = ROOT.TFile(fname,"READ")
    hPUw = puFile.Get(puHistName)

    if not hPUw:
        print "PU hist not found!"
        exit(0)

    for ibin in range(1,hPUw.GetNbinsX()):

        #npv = hPUw.GetXaxis().GetBinLowEdge(ibin)
        npv = int(hPUw.GetXaxis().GetBinCenter(ibin))
        rat = hPUw.GetBinContent(ibin)

        puDict[npv] = rat

    puFile.Close()

    return puDict

# pu histo file name
#puFileName_norm = "../python/tools/pileup/pu_ratio_80mb.root"
#puFileName_up = "../python/tools/pileup/pu_ratio_84mb.root"
#puFileName_down = "../python/tools/pileup/pu_ratio_76mb.root"

'''
puFileName_up = "../python/tools/pileup/pu_ratio_74mb.root"
puFileName_norm = "../python/tools/pileup/pu_ratio_70mb.root"
puFileName_down = "../python/tools/pileup/pu_ratio_66mb.root"
'''

puFileName_up = "../python/tools/pileup/pu_ratio_72p45mb.root"
puFileName_norm = "../python/tools/pileup/pu_ratio_69mb.root"
puFileName_down = "../python/tools/pileup/pu_ratio_65p55mb.root"

puNorm =  getPUdict(puFileName_norm)
puUp =  getPUdict(puFileName_up)
puDown =  getPUdict(puFileName_down)

print 80*"#"
print "Loaded PU weights!"
#print puNorm

class EventVars1L_pileup:
    def __init__(self):
        self.branches = [
            'nVtx', 'nTrueInt',
            'puRatio','puRatio_up','puRatio_down'
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        if not event.isData:

            ret['nVtx'] = event.nVert

            nTrueInt = event.nTrueInt
            ret['nTrueInt'] = nTrueInt

            if nTrueInt in puNorm:
                ret['puRatio'] = puNorm[nTrueInt]
                ret['puRatio_up'] = puUp[nTrueInt]
                ret['puRatio_down'] = puDown[nTrueInt]
            else:
                ret['puRatio'] = 0
                ret['puRatio_up'] = 0
                ret['puRatio_down'] = 0
        else:
            ret['puRatio'] = 1
            ret['puRatio_up'] = 1
            ret['puRatio_down'] = 1


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
