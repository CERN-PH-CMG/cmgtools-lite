import ROOT

class CollectionSkimmer:
    def __init__(self, outName, srcColl, ints=[], floats=[], uchars=[], maxSize=100, saveSelectedIndices=False, padSelectedIndicesWith=None, saveTagForAll=False):
        """Read from a collection called srcColl (eg. 'Jet'), write out to a collection called outName (e.g. 'CleanJet')
           Clone the variables specified in the ints and floats list (e.g. 'mcMatchId', 'pt', ...)
           maxSize fixes the maximum allowed number of entries in the output."""
        self._maxSize = maxSize
        self._ints   = ints
        self._uchars = uchars
        self._floats = floats
        self._saveSelectedIndices = saveSelectedIndices
        self._padSelectedIndicesWith = padSelectedIndicesWith
        self._saveTagForAll = saveTagForAll
        self._impl = ROOT.CollectionSkimmer(outName,srcColl,saveSelectedIndices,saveTagForAll)
        self._iprefix = srcColl + "_"
        for i in ints  : self._impl.declareCopyInt(i[0])   if type(i) == tuple else self._impl.declareCopyInt(i)  
        for f in floats: self._impl.declareCopyFloat(f[0]) if type(f) == tuple else self._impl.declareCopyFloat(f)
        for u in uchars: self._impl.declareCopyUChar(u[0]) if type(u) == tuple else self._impl.declareCopyUChar(u)
        self._ttreereaderversion = -1
    def initInputTree(self,tree):
        """To be called to initialize the input tree. 
           initEvent also takes care of re-calling it if needed"""
        #always read the size, to be sure of the capacity of the vectors
        self._impl.srcCount(tree.valueReader('n'+self._iprefix[:-1]))
        for i in self._ints:   self._impl.copyInt(i[0]  , tree.arrayReader(self._iprefix+i[1])) if type(i) == tuple else self._impl.copyInt(i, tree.arrayReader(self._iprefix+i))  
        for f in self._floats: self._impl.copyFloat(f[0], tree.arrayReader(self._iprefix+f[1])) if type(f) == tuple else self._impl.copyFloat(f, tree.arrayReader(self._iprefix+f))
        for u in self._uchars: self._impl.copyUChar(u[0], tree.arrayReader(self._iprefix+u[1])) if type(u) == tuple else self._impl.copyUChar(u, tree.arrayReader(self._iprefix+u))
        self._ttreereaderversion = tree._ttreereaderversion
    def initOutputTree(self,outpytree,bareTree=False):
        """To be called once when defining the output PyTree, to declare the branches"""
        self._impl.makeBranches(outpytree if bareTree else outpytree.tree, self._maxSize, (self._padSelectedIndicesWith!=None), self._padSelectedIndicesWith if (self._padSelectedIndicesWith!=None) else -1)
    def initEvent(self,event):
        """To be called at the beginning of every event.
           Returns true if the underlying TTreeReader has changed"""
        if self._ttreereaderversion != event._tree._ttreereaderversion:
            self.initInputTree(event._tree)
            self._impl.clear()
            return True
        else:
            self._impl.clear()
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
