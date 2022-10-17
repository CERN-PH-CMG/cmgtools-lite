from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as NanoAODCollection 

from CMGTools.TTHAnalysis.treeReAnalyzer import Collection as CMGCollection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput


class ObjTagger(Module):
    def __init__(self,label,coll,sel,sizelimit=10,linkColl='', linkVar=''):
        self.label = "" if (label in ["",None]) else (label)
        self.coll = coll
        self.sel = sel
        self.sizelimit = sizelimit
        self.linkColl  = linkColl
        self.linkVar   = linkVar

    def listBranches(self):
        biglist = [ ("n"+self.coll,"I"), ("n"+self.coll+"_"+self.label, "I"), (self.coll+"_"+self.label,"I",100,"n"+self.coll) ]
        return biglist
    def __call__(self,event):
        return self.runIt(event,CMGCollection)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, [ ("n"+self.coll,"I"), ("n"+self.coll+"_"+self.label, "I"), (self.coll+"_"+self.label,"I",100,"n"+self.coll) ])
    def analyze(self, event):
        writeOutput(self, self.runIt(event,NanoAODCollection))
        return True

    def runIt(self, event, Collection):
        try :
            assert (getattr(event,"n"+self.coll) <= self.sizelimit)
        except AssertionError:
            print 'ERROR in ObjTagger: branch size limit is '+str(self.sizelimit)+' while n'+self.coll+'=='+str(getattr(event,"n"+self.coll))
            raise
        objs  = [l for l in Collection(event,self.coll,"n"+self.coll)]
        linked= [g for g in Collection(event,self.linkColl, "n"+self.linkColl)] if self.linkColl != "" else []
        ret = {"n"+self.coll : getattr(event,"n"+self.coll) }
        ret["n"+self.coll+"_"+self.label]=0
        ret[self.coll+"_"+self.label]=[0] * getattr(event,"n"+self.coll)
        for i,ob in enumerate(objs):
            ispassing = True
            for selector in self.sel:
                if self.linkColl == "":
                    if not selector(ob):
                        ispassing = False
                        break
                else:
                    if not selector(ob,linked[getattr(ob,self.linkVar)]):
                        ispassing = False
                        break
            if ispassing:
                ret["n"+self.coll+"_"+self.label] += 1
                ret[self.coll+"_"+self.label][i] = 1
        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    tree.vectorTree = True
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf1 = ObjTagger("LepPt25","LepGood",[lambda ob : ob.pt >= 25])
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf1(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)

        
