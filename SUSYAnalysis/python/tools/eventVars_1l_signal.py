from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator

# import gluino xsec table
xsecGlu = {} # dict for xsecs
xsecFile = "../python/tools/glu_xsecs_13TeV.txt"

cntsSusy = {} # dict for signal counts
C_ISRweightsSusy = {}
#cntFile = "../python/tools/t1ttt_scan_counts.txt"
cntFile = "../python/tools/scans/counts_T1tttt_2016.txt"
ISRweightFile = "../python/tools/scans/ISRnormWeights_T1tttt2016.txt"

def loadSUSYparams():

    global xsecGlu
    global cntsSusy
    global C_ISRweightsSusy

    print 80*"#"
    print "Loading SUSY parameters"

    with open(xsecFile,"r") as xfile:
        lines = xfile.readlines()
        print 'Found %i lines in %s' %(len(lines),xsecFile)
        for line in lines:
            if line[0] == '#': continue
            (mGo,xsec,err) = line.split()
            #print 'Importet', mGo, xsec, err, 'from', line
            xsecGlu[int(mGo)] = (float(xsec),float(err))

        print 'Filled %i items to dict' % (len(xsecGlu))
        #print sorted(xsecGlu.keys())

    with open(cntFile,"r") as cfile:
        lines = cfile.readlines()
        print 'Found %i lines in %s' %(len(lines),cntFile)

        for line in lines:
            if line[0] == '#': continue
            else:
                (mGo,mLSP,tot,totW,cnt,wgt) = line.split()
                #print 'Importet', mGo, mLSP, cnt, 'from', line
                #cntsSusy[(int(mGo),int(mLSP))] = (int(tot),int(cnt),float(wgt))
                cntsSusy[(int(mGo),int(mLSP))] = (float(totW),int(cnt),float(wgt))

        print 'Filled %i items to dict' % (len(cntsSusy))
        print "Finished signal parameter load"

    with open(ISRweightFile,"r") as cfile:
        lines = cfile.readlines()
        print 'Found %i lines in %s' %(len(lines),ISRweightFile)

        for line in lines:
            if line[0] == '#': continue
            else:
                (mGo,mLSP,C_ISRweight,C_ISRweight_up,C_ISRweight_down) = line.split()
                #print 'Importet', mGo, mLSP, cnt, 'from', line
                #cntsSusy[(int(mGo),int(mLSP))] = (int(tot),int(cnt),float(wgt))
                C_ISRweightsSusy[(int(mGo),int(mLSP))] = (C_ISRweight,C_ISRweight_up,C_ISRweight_down)

        print 'Filled ISR weights %i items to dict' % (len(C_ISRweightsSusy))

    return 1

#### LHE Weights #####
lheDict = {}
pckname = "../python/tools/scans/LHEweights.pck"

maxLHEidx = 10

def loadLHE():

    print "Loading mean LHE weights"

    global lheDict

    import cPickle as pickle
    lheDict = pickle.load(open( pckname, "rb" ))
    #print lheDict.keys()

class EventVars1L_signal:
    def __init__(self):
        self.branches = [
            ### Masses and Xsec
            'mGo','mLSP','susyXsec',
            'susyNgen','totalNgen','susyWgen',
            'nISR','nISRweight','nISRweightsyst_up', 'nISRweightsyst_down',
            ## LHE Scale Weights
            #("nScaleWgt","I"),("ScaleWgt","I",10,"nScaleWgt")
            ("ScaleWgt","F",maxLHEidx,maxLHEidx)
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        if not event.isData and "T1tttt" in self.sample:

            global xsecGlu
            global cntsSusy
            global C_ISRweightsSusy 

            if len(xsecGlu) == 0: loadSUSYparams()

            ## MASS POINT
            mGo = 0
            mLSP = 0

            # Gluino Mass
            if hasattr(event,'GenSusyMGluino'): mGo = event.GenSusyMGluino

            # LSP Mass
            if hasattr(event,'GenSusyMNeutralino'): mLSP = event.GenSusyMNeutralino
            # set LSP mass of 1 to zero
            if mLSP == 1: mLSP = 0;

            # save masses
            ret['mGo'] = mGo; ret['mLSP'] = mLSP

            # SUSY Xsec
            if mGo in xsecGlu:
                ret['susyXsec'] = xsecGlu[mGo][0]
                #ret['susyXsecErr'] = xsecGlu[mGo][1]
            elif mGo > 0:
                print 'Xsec not found for mGo', mGo

            # Number of generated events
            #ret['totalNgen'] = cntTotal
            nISR = 0
            if hasattr(event,'nIsr'): nISR = event.nIsr
            nISRforWeights = int(nISR)
            if nISR > 6:
                nISRforWeights = 6

            ret['nISR'] = int(nISR)
            ISRweights = { 0: 1, 1 : 0.882, 2 : 0.792, 3 : 0.702, 4 : 0.648, 5 : 0.601, 6 : 0.515}
            ISRweightssyst = { 0: 0.0, 1 : 0.059, 2 : 0.104, 3 : 0.149, 4 : 0.176, 5 : 0.199, 6 : 0.242}

            C_ISR = float(C_ISRweightsSusy[(mGo,mLSP)][0])
            C_ISR_up = float(C_ISRweightsSusy[(mGo,mLSP)][1])
            C_ISR_down = float(C_ISRweightsSusy[(mGo,mLSP)][2])



            nISRweight = C_ISR * ISRweights[nISRforWeights]
            nISRweightsyst_up =  C_ISR_up * (ISRweights[nISRforWeights]+ISRweightssyst[nISRforWeights])
            nISRweightsyst_down =  C_ISR_down * (ISRweights[nISRforWeights]-ISRweightssyst[nISRforWeights])

            ret['nISRweight'] = nISRweight
            ret['nISRweightsyst_up'] = nISRweightsyst_up 
            ret['nISRweightsyst_down'] = nISRweightsyst_down
            #print nISR, nISRweight, nISRweightsyst_up, nISRweightsyst_down
            ###Get ISR stuff

            ##############
            if (mGo,mLSP) in cntsSusy:
                #ret['totalNgen'] = cntsSusy[(mGo,mLSP)][0] # merged scan: 93743963
                if "Scan" in self.sample: ret['totalNgen'] = 93743963
                else: ret['totalNgen'] = cntsSusy[(mGo,mLSP)][0]
                ret['susyNgen'] = cntsSusy[(mGo,mLSP)][1]
                ret['susyWgen'] = cntsSusy[(mGo,mLSP)][2]
            else:
                ret['totalNgen'] = 1
                ret['susyNgen'] = 1
                ret['susyWgen'] = 1

            #print "don't to LHE stuff"
            #### LHE Weights (for Scale uncert) #####
            ## Scale uncertainty
            ## https://indico.cern.ch/event/459797/contribution/2/attachments/1181555/1710844/mcaod-Nov4-2015.pdf
            ## Standard prescription: Compute the envelope of your
            ## observable for weight indices 1,2,3,4,6,8 (index 0 corresponds
            ## to nominal scale, indices 5 and 7 correspond to "unphysical"
            ## anti-correlated variations)

            noLHEstuff = True
            if noLHEstuff:
                return ret
            global lheDict

            if len(lheDict) == 0: loadLHE()
            print "1", lheDict.keys()

            # initialize dummy list
            scaleWgts = [1 for i in range(0,maxLHEidx)]
            # average weights
            meanWgts  = [1 for i in range(0,maxLHEidx)]

            print self.sample
            print "2", lheDict.keys()

            sampkey = self.sample

            if sampkey not in lheDict:# and "mGo" in sampkey:
                # search for gluino mass in keys
                for point in lheDict.keys():
                    if str(mGo) in point: sampkey = point; break
            print sampkey

            if sampkey in lheDict:
                meanWgts = lheDict[sampkey]

                lheWgts = [w for w in Collection(event,"LHEweight","nLHEweight")]

                scaleWgts = []
                for i in range(0,maxLHEidx):

                    #print lheWgts[i].wgt,lheWgts[0].wgt,meanWgts[i]
                    wgt = lheWgts[i].wgt/lheWgts[0].wgt/meanWgts[i]
                    #wgt = meanWgts[i]
                    #print wgt
                    scaleWgts.append(wgt)

                print scaleWgts
            else: print "No mean scale weights found for", sampkey
            ret['ScaleWgt'] = scaleWgts
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
