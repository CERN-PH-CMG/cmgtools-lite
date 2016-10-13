import ROOT

class CollectionSkimmer:
    def __init__(self, outName, srcColl, ints=[], floats=[], maxSize=100):
        self._maxSize = maxSize
        self._ints   = ints
        self._floats = floats
        self._impl = ROOT.CollectionSkimmer(outName)
        self._iprefix = srcColl + "_"
        for i in ints: self._impl.copyInt(i)
        for f in floats: self._impl.copyFloat(f)
        self._ttreereaderversion = -1
    def initInputTree(self,tree):
        for i in self._ints:   self._impl.copyInt(i, tree.arrayReader(self._iprefix+i))
        for f in self._floats: self._impl.copyFloat(f, tree.arrayReader(self._iprefix+f))
        self._ttreereaderversion = tree._ttreereaderversion
    def initOutputTree(self,outpytree):
        self._impl.makeBranches(outpytree.tree, self._maxSize)
    def initEvent(self,event):
        self._impl.clear()
        if self._ttreereaderversion != event._tree._ttreereaderversion:
            self.initInputTree(event._tree)
            return True
        return False
    def cppImpl(self):
        return self._impl
    def clear(self): 
        self._impl.clear()
    def push_back(self,iSrc): 
        self._impl.push_back(iSrc)
    def push_back_all(self,iSrcList): 
        for iSrc in iSrcList:
            self._impl.push_back(iSrc)
    def resize(self,newSize): 
        self._impl.reSize(newSize)
    def copy(self,iSrc,iTo):
        self._impl.copy(iSrc,iTo)
    def __setitem__(self,iTo,iSrc):
        self._impl.copy(iSrc,iTo)
    def size(self):
        return self._impl.size()
    def __len__(self):
        return self._impl.size()
