import time
import itertools
import PhysicsTools.Heppy.loadlibs

import ROOT
from CMGTools.TTHAnalysis.treeReAnalyzer import *

###############
# MET filters
# Text files
###############


filterName = "/afs/cern.ch/user/k/kirschen/public/forSUSY/dummyFilterlist.txt" #to process 2016 data quickly...
#filterName = "/afs/desy.de/user/l/lobanov/public/SUSY/Run2/METfilters/Recent/Jan2016/skim/combine.txt"
#filterName = "/afs/desy.de/user/l/lobanov/public/SUSY/Run2/METfilters/SingleLepton_csc2015.txt"
#filterName = "/afs/desy.de/user/l/lobanov/public/SUSY/Run2/METfilters/JetHT_csc2015.txt"
#filterList = readList(filterName)
filterList = None

def readList(fname):
    evList = set()
    with open(fname,"r") as flist:
        for line in flist.readlines():
            if ":" not in line: continue
            sline = line.split(":")
            if len(sline) != 3: continue
            evList.add((int(sline[0]),int(sline[1]),int(sline[2])))


    print 80*"#"
    print "MET filters"
    print "Loaded %i events into CSC Filter list" %len(evList)
    print 80*"#"

    return evList

#print list(filterList)[:10]

class EventVars1L_filters:
    def __init__(self):
        self.branches = [
            'passFilters','passCSCFilterList',
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        if event.isData:
            global filterList
            if filterList == None: filterList = readList(filterName)

            # check MET text filter files
            if (event.run,event.lumi,event.evt) in filterList:
                #print "yes", event.run,event.lumi,event.evt
                ret['passCSCFilterList'] = False
            else:
                #print "no", event.run,event.ls,event.evt
                ret['passCSCFilterList'] = True

            # check filters present in event (not FastSim)
            if hasattr(event,"Flag_eeBadScFilter"):
                #for2016ICHEP https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#MiniAOD_8011_ICHEP_dataset
                ret['passFilters'] = event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and  event.Flag_goodVertices and event.Flag_eeBadScFilter and event.Flag_globalTightHalo2016Filter and event.Flag_badChargedHadronFilter and event.Flag_badMuonFilter
                #201574X:ret['passFilters'] = event.Flag_goodVertices and event.Flag_eeBadScFilter and event.Flag_HBHENoiseFilter_fix and event.Flag_HBHENoiseIsoFilter and ret['passCSCFilterList']
                #ret['passFilters'] = event.Flag_goodVertices and event.Flag_eeBadScFilter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter  and event.Flag_CSCTightHaloFilter and ret['passCSCFilterList']
            else:
                ret['passFilters'] = 1
        else:
            ret['passCSCFilterList'] = True
            ret['passFilters'] = True


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
