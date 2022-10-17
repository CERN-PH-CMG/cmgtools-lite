from CMGTools.TTHAnalysis.treeReAnalyzer import *
import math

class VertexWeightFriend:
    def __init__(self,myfile,targetfile,myhist="pileup",targethist="pileup",name="vtxWeight",verbose=False,vtx_coll_to_reweight="nVert",autoPU=False):
        self.name = name
        self.verbose = verbose
        self.autoPU = autoPU
        self.files = [None,None]
        self.files[1] = ROOT.TFile.Open(targetfile)
        self.targetvals, self.numnorm, self.targetbounds = self.load(self.files[1].Get(targethist))
        if not self.autoPU:
            self.files[0] = ROOT.TFile.Open(myfile)
            self.myvals, self.dennorm, self.mybounds = self.load(self.files[0].Get(myhist))
            if self.mybounds!=self.targetbounds or len(self.myvals)!=len(self.targetvals): raise RuntimeError, 'Source and target histogram have different ranges or binnings'
        self.vtxCollectionInEvent = vtx_coll_to_reweight
        self.warned = False
    def init(self,tree):
        if self.autoPU:
            print 'Auto-determining pileup profile from source file, using %s as the variable to reweight...'%self.vtxCollectionInEvent
            tree.Draw("%s >> autoPUhist(%d,%f,%f)"%(self.vtxCollectionInEvent,len(self.targetvals),self.targetbounds[0],self.targetbounds[1]))
            self.myvals, self.dennorm, self.mybounds = self.load(ROOT.gDirectory.Get('autoPUhist'))
        def w2(t,m):
            if t == 0: return (0 if m else 1)
            return (t/m if m else 1)
        self.weights = [ w2(t,m) for (m,t) in zip(self.myvals,self.targetvals) ]
        if self.verbose:
            print "Raw weights for vertex multiplicity up to %d; max %.3f, min %.3f, avg %.3f" % (
                len(self.weights), max(self.weights), min(self.weights), sum(self.weights)/len(self.weights) )
            print self.weights
        self.fixLargeWeights()
        if self.verbose:
            print "Initialized weights for vertex multiplicity up to %d; max %.3f, min %.3f, avg %.3f" % (
                len(self.weights), max(self.weights), min(self.weights), sum(self.weights)/len(self.weights) )
            print self.weights
    def fixLargeWeights(self,maxshift=0.0025,hardmax=3):
        def checkIntegral(weights):
            myint  = sum(a*b for (a,b) in zip(weights,     self.myvals)) 
            refint = sum(a*b for (a,b) in zip(self.weights,self.myvals)) 
            return (myint-refint)/refint
        maxw = min(max(self.weights),5)
        while maxw > hardmax:
            cropped = [ min(maxw,w) for w in self.weights ]
            check = checkIntegral(cropped)
            if self.verbose:
                print "For maximum weight %.3f: integral match: %.5f" % (maxw, check)
            if abs(check) > maxshift:
                break
            maxw *= 0.9
        maxw /= 0.9
        cropped = [ min(maxw,w) for w in self.weights ]
        normshift = checkIntegral(cropped)
        recalibrated = [ c*(1-normshift) for c in cropped ]
        if self.verbose:
            print "Cropped weights up to maximum %d. Normalization shift %.5f, corrected overall to %g" % (maxw,normshift,checkIntegral(recalibrated))
        self.weights = recalibrated
    def load(self,hist,norm=True):
        vals = [ hist.GetBinContent(i) for i in xrange(1,hist.GetNbinsX()+1) ]
        for i in xrange(1,len(vals)-1):
            if vals[i] == 0 and vals[i-1] > 0 and vals[i+1] > 0:
                vals[i] = 0.5*(vals[i-1]+vals[i+1])
        if self.verbose:
            print "Normalization of ",hist.GetName(),": ",sum(vals)
        if norm: 
            scale = 1.0/sum(vals)
            vals = [ v*scale for v in vals ]
        return vals, (1.0/scale if norm else 1), (hist.GetXaxis().GetXmin(),hist.GetXaxis().GetXmax())
    def listBranches(self):
        return [ (self.name,'F') ]
    def __call__(self,event):
        if hasattr(event,self.vtxCollectionInEvent):
            _nvtx = getattr(event,self.vtxCollectionInEvent)
            if math.isinf(_nvtx) or math.isnan(_nvtx) or _nvtx < 0:
                print 'WARNING: crazy value of input reweigthing variable found (%f), returning weight = 1'%_nvtx
                weight = 1
            else:
                nvtx = int(_nvtx)
                weight = self.weights[nvtx] if nvtx < len(self.weights) else 1
            return { self.name: weight }
        else:
            if not self.warned:
                print "WARNING! Variable ",self.vtxCollectionInEvent," is missing in the tree. Setting the weight to 1."
                self.warned = True
            return { self.name: 1 }
    def printPUWCode(self,name):
        privname = name
        pubname  = name[1:]
        print ""
        print "float %s[%d] = { %s };" % (privname, len(self.weights), ", ".join(map(str,self.weights)))
        print "float %s(int nVert) { return %s[std::min(nVert,%d)] * (%s/%s); } " % (pubname, privname, len(self.weights)-1, self.numnorm, self.dennorm);
        print ""
if __name__ == '__main__':
    from sys import argv
    class Tester(Module):
        def __init__(self, name, nvtx=False):
            Module.__init__(self,name,None)
            if nvtx:
                self.mc  = VertexWeightFriend(myfile=argv[2],targetfile=argv[2],myhist="nvtx_background",targethist="nvtx_data",verbose=True)
            else:
                self.mc  = VertexWeightFriend(myfile=None,targetfile=argv[2],myhist=None,targethist="pileup",vtx_coll_to_reweight="nTrueInt",verbose=True,autoPU=True)
        def init(self,tree):
            self.mc.init(tree)
        def analyze(self,ev):
            ret = self.mc(ev)
            print ev.nVert, ret.values()[0]
    import os.path
    if os.path.exists(argv[1]):
        test = Tester("tester")
        el = EventLoop([ test ])
        file = ROOT.TFile(argv[1])
        tree = file.Get("tree")
        tree.vectorTree = True
        el.loop([tree], maxEvents = 10 if len(argv) < 4 else int(argv[3]))
    elif argv[1].startswith("_puw"):
        test = Tester("tester",nvtx=True)
        test.mc.init(None)
        test.mc.printPUWCode(argv[1]) 
