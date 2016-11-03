import ROOT

class CollectionSkimmer:
    def __init__(self, outName, srcColl, ints=[], floats=[], maxSize=100):
        """Read from a collection called srcColl (eg. 'Jet'), write out to a collection called outName (e.g. 'CleanJet')
           Clone the variables specified in the ints and floats list (e.g. 'mcMatchId', 'pt', ...)
           maxSize fixes the maximum allowed number of entries in the output."""
        self._maxSize = maxSize
        self._ints   = ints
        self._floats = floats
        self._impl = ROOT.CollectionSkimmer(outName)
        self._iprefix = srcColl + "_"
        for i in ints: self._impl.copyInt(i)
        for f in floats: self._impl.copyFloat(f)
        self._ttreereaderversion = -1
    def initInputTree(self,tree):
        """To be called to initialize the input tree. 
           initEvent also takes care of re-calling it if needed"""
        for i in self._ints:   self._impl.copyInt(i, tree.arrayReader(self._iprefix+i))
        for f in self._floats: self._impl.copyFloat(f, tree.arrayReader(self._iprefix+f))
        self._ttreereaderversion = tree._ttreereaderversion
    def initOutputTree(self,outpytree):
        """To be called once when defining the output PyTree, to declare the branches"""
        self._impl.makeBranches(outpytree.tree, self._maxSize)
    def initEvent(self,event):
        """To be called at the beginning of every event.
           Returns true if the underlying TTreeReader has changed"""
        self._impl.clear()
        if self._ttreereaderversion != event._tree._ttreereaderversion:
            self.initInputTree(event._tree)
            return True
        return False
    def cppImpl(self):
        """Get the C++ CollectionSkimmer instance, to pass to possible C++ worker code"""
        return self._impl
    def clear(self): 
        """Clear the list of output objects (note: initEvent does it already)"""
        self._impl.clear()
    def push_back(self,iSrc): 
        """Select one object (if passing an int) or many objects (if passing std::vector<int>) for output"""
        self._impl.push_back(iSrc)
    def push_back_all(self,iSrcList): 
        """Select a python list of objects for output"""
        for iSrc in iSrcList:
            self._impl.push_back(iSrc)
    def resize(self,newSize): 
        """Fix the size of the output collection (to be called before with copy() or [] for out-of-order filling)"""
        self._impl.reSize(newSize)
    def copy(self,iSrc,iTo):
        """Copy input object of index iSrc into output iTo (you must have called resize with a suitable size before)"""
        self._impl.copy(iSrc,iTo)
    def __setitem__(self,iTo,iSrc):
        """Set output at the specified index iTo to be a copy of the input at iSrc (note that the order is reversed wrt copy())"""
        self._impl.copy(iSrc,iTo)
    def size(self):
        """Return the number of selected items in this event"""
        return self._impl.size()
    def __len__(self):
        """Return the number of selected items in this event"""
        return self._impl.size()
