import types
import ROOT

def initTree(tree):
    tree.entry = -1
    tree._ttreereader = ROOT.TTreeReader(tree)
    tree._ttreereader.SetEntry(0)
    tree._ttrvs = {}
    tree._ttras = {}
    tree._leafTypes = {}
    tree._ttreereaderversion = 1
    tree.arrayReader = types.MethodType(getArrayReader, tree)
    tree.valueReader = types.MethodType(getValueReader, tree)
    tree.readBranch = types.MethodType(readBranch, tree)

def getArrayReader(tree, branchName, isClean=False):
    """Make a reader for branch branchName containing a variable-length value array. 
       If you are sure nobody has yet read from the tree, you can set isClean to True and save some overhead."""
    if branchName not in tree._ttras:
       if not tree.GetBranch(branchName): raise RuntimeError, "Can't find branch '%s'" % branchName
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if not leaf.GetLen() == 0: raise RuntimeError, "Branch %s is not a variable-length value array" % branchName
       typ = _rootType2Python[leaf.GetTypeName()]
       tree._ttras[branchName] = _makeArrayReader(tree, typ, branchName, remakeAllFirst=not(isClean))
    return tree._ttras[branchName]

def getValueReader(tree, branchName, isClean=False):
    """Make a reader for branch branchName containing a single value. 
       If you are sure nobody has yet read from the tree, you can set isClean to True and save some overhead."""
    if branchName not in tree._ttrvs:
       if not tree.GetBranch(branchName): raise RuntimeError, "Can't find branch '%s'" % branchName
       leaf = tree.GetBranch(branchName).GetLeaf(branchName)
       if not leaf.GetLen() == 1: raise RuntimeError, "Branch %s is not a value" % branchName
       typ = _rootType2Python[leaf.GetTypeName()]
       tree._ttrvs[branchName] = _makeValueReader(tree, typ, branchName, remakeAllFirst=not(isClean))
    return tree._ttrvs[branchName]


def readBranch(tree, branchName):
    """Return the branch value if the branch is a value, and a TreeReaderArray if the branch is an array"""
    if branchName in tree._ttras: 
        return tree._ttras[branchName]
    elif branchName in tree._ttrvs: 
        return tree._ttrvs[branchName].Get()[0]
    else:
        branch = tree.GetBranch(branchName)
        if not branch: raise RuntimeError, "Unknown branch %s" % branchName
        leaf = branch.GetLeaf(branchName)
        if leaf.GetTypeName() not in _rootType2Python:
            raise RuntimeError, "Branch %s has unsupported type %s" % (branchName, leaf.GetTypeName())
        typ = _rootType2Python[leaf.GetTypeName()]
        if leaf.GetLen() == 1: 
            return _makeValueReader(tree, typ, branchName).Get()[0]
        else:
            return _makeArrayReader(tree, typ, branchName)
        

####### PRIVATE IMPLEMENTATION PART #######

_rootType2Python = { 'Int_t':int, 'Long_t':long, 'UInt_t':int, 'ULong_t':long,
                     'Float_t':float, 'Double_t':float }

def _makeArrayReader(tree, typ, nam, remakeAllFirst=True):
    if remakeAllFirst: _remakeAllReaders(tree) 
    ttra = ROOT.TTreeReaderArray(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttras[nam] = ttra;
    tree._ttreereader.SetEntry(tree.entry)
    return tree._ttras[nam]

def _makeValueReader(tree, typ, nam, remakeAllFirst=True):
    if remakeAllFirst: _remakeAllReaders(tree) 
    ttrv = ROOT.TTreeReaderValue(typ)(tree._ttreereader, nam)
    tree._leafTypes[nam] = typ
    tree._ttrvs[nam] = ttrv
    tree._ttreereader.SetEntry(tree.entry)
    return tree._ttrvs[nam]

def _remakeAllReaders(tree):
    _ttreereader = ROOT.TTreeReader(tree)
    _ttrvs = {}
    for k in tree._ttrvs.iterkeys():
        _ttrvs[k] = ROOT.TTreeReaderValue(tree._leafTypes[k])(_ttreereader,k)
    _ttras = {}
    for k in tree._ttras.iterkeys():
        _ttras[k] = ROOT.TTreeReaderArray(tree._leafTypes[k])(_ttreereader,k)
    tree._ttrvs = _ttrvs
    tree._ttras = _ttras
    tree._ttreereader = _ttreereader
    tree._ttreereaderversion += 1



