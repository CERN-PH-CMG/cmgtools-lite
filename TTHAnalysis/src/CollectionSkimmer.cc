#include "CMGTools/TTHAnalysis/interface/CollectionSkimmer.h"
#include <TTree.h>
#include <TTreeReaderArray.h>

template<typename T1, typename T2>
void CollectionSkimmer::CopyVar<T1,T2>::branch(TTree *tree, unsigned int maxLength) 
{
    out_.reset(new T2[maxLength]);
    std::string typecode = "?";
    if      (typeid(T2) == typeid(int))   typecode = "I";
    else if (typeid(T2) == typeid(float)) typecode = "F";
    else throw std::logic_error("Unsupported type");
    tree->Branch( (collName_ + "_" + varName_).c_str(),
                  out_.get(),
                  (collName_ + "_" + varName_ + "[n" + collName_ + "]/" + typecode).c_str() );
}

void 
CollectionSkimmer::makeBranches(TTree *tree, unsigned int maxEntries) {
    tree->Branch(("n"+outName_).c_str(), &nOut_, ("n"+outName_+"/I").c_str());
    for (auto & c : copyFloats_) c.branch(tree, maxEntries);
    for (auto & c : copyInts_) c.branch(tree, maxEntries);
    hasBranched_ = true;
}

void CollectionSkimmer::copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src) 
{ 
    _copyVar(varname, src, copyFloats_);
}

void CollectionSkimmer::copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src) 
{
    _copyVar(varname, src, copyInts_);
}

template<typename CopyVarVectorT, typename SrcT>
void CollectionSkimmer::_copyVar(const std::string &varname, SrcT * src, CopyVarVectorT &copyVars) 
{ 
    bool found = false;
    for (auto &c : copyVars) {
        if (c.varName() == varname) {
            c.setSrc(src);
            found = true;
            break;
        }
    }
    if (!found) {
        _checkNoBranchesYet();
        copyVars.emplace_back(outName_, varname);
    }
}

void CollectionSkimmer::_checkNoBranchesYet() 
{
    if (hasBranched_) throw std::logic_error("Error, can't add a new variable after having set the output tree\n");
}


