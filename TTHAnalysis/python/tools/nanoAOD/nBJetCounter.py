from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

class nBJetCounter( Module ):
    def __init__(self,label,bTagLabel,jetSel,WPs=["Loose","Medium","Tight"],years=[2016,2017,2018]):
        self._label = label
        self._bTagLabel = bTagLabel
        self._jetCut = jetSel
        self._WPs = WPs
        self._ops = {}
        for y in years:
            if bTagLabel == "btagDeepB":
                self._ops[y] = [ _btagWPs["DeepCSV_%d_%s" %(y,W[0])][1] for W in WPs ]
            elif bTagLabel == "btagDeepFlavB":
                self._ops[y] = [ _btagWPs["DeepFlav_%d_%s"%(y,W[0])][1] for W in WPs ]
            else:
                raise RuntimeError("B-tagger %s not supported for year %y" % (bTagLabel,y))
        #self._n = 0
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for W in self._WPs:
            self.out.branch("nBJet%s%s" % (self._label, W), "I")
    def analyze(self, event):
        #self._n += 1
        jetvals = [ getattr(j, self._bTagLabel) for j in Collection(event, 'Jet') if self._jetCut(j) ]
        for (W,cut) in zip(self._WPs,self._ops[event.year]):
            self.out.fillBranch("nBJet%s%s" % (self._label, W), sum([(v > cut) for v in jetvals]))
        #if self._n < 20:
        #    print "New event: (year: %d) " % event.year
        #    for j in Collection(event, 'Jet'):
        #        print "  jet pt %6.1f  eta %+5.2f  id %2d  sel %1d    btag %+.4f" % (j.pt, j.eta, j.jetId, int(self._jetCut(j)),  getattr(j, self._bTagLabel))
        #    print "All btags of selected jets: ", jetvals
        #    print "WPs for this year: ", self._ops[event.year]
        #    for (W,cut) in zip(self._WPs,self._ops[event.year]):
        #        print "nBJet%s%s: %2d" % (self._label, W, sum([(v > cut) for v in jetvals]))
        #    print "" 
        return True
