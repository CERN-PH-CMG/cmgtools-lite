#include "CMGTools/TTHAnalysis/interface/CollectionSkimmer.h"
#include <TTree.h>
#include <TTreeReaderArray.h>
#include <iostream>

template<typename T1, typename T2>
void CollectionSkimmer::CopyVar<T1,T2>::branch(TTree *tree, unsigned int maxLength) 
{
    out_.reset(new T2[maxLength]);
    std::string typecode = "?";
    if      (typeid(T2) == typeid(int))   typecode = "I";
    else if (typeid(T2) == typeid(float)) typecode = "F";
    else throw std::logic_error("Unsupported type");
    maxEntries_ = maxLength;
    branch_ = tree->Branch( (collName_ + "_" + varName_).c_str(),
                             out_.get(),
                             (collName_ + "_" + varName_ + "[n" + collName_ + "]/" + typecode).c_str() );
}

template<typename T1, typename T2>
void CollectionSkimmer::CopyVar<T1,T2>::ensureSize(unsigned int n) 
{
    if (n > maxEntries_) {
        maxEntries_ = std::max<unsigned>(n, 2*maxEntries_);
        out_.reset(new T2[maxEntries_]);
        branch_->SetAddress(out_.get());
    }
} 
void 
CollectionSkimmer::makeBranches(TTree *tree, unsigned int maxEntries, bool padSelectedIndicesCollection, int padSelectedIndicesCollectionWith) {
    maxEntries_ = maxEntries;
    padSelectedIndicesCollection_ = padSelectedIndicesCollection;
    padSelectedIndicesCollectionWith_ = padSelectedIndicesCollectionWith;
    if (saveTagForAll_) {
      iTagOut_.reset(new int[maxEntries]);
      tree->Branch(("n"+collName_).c_str(), &nIn_, ("n"+collName_+"/I").c_str());
      branchTag_ = tree->Branch((collName_+"_is"+outName_).c_str(), iTagOut_.get(), (collName_+"_is"+outName_+"[n"+collName_+"]/I").c_str());
    }
    tree->Branch(("n"+outName_).c_str(), &nOut_, ("n"+outName_+"/I").c_str());
    if (saveSelectedIndices_) {
      iOut_.reset(new int[maxEntries]);
      if (padSelectedIndicesCollection_) {
          branch_ = tree->Branch(("i"+outName_).c_str(), iOut_.get(), ("i"+outName_+"[" + std::to_string(maxEntries) + "]/I").c_str());
      } else {
          branch_ = tree->Branch(("i"+outName_).c_str(), iOut_.get(), ("i"+outName_+"[n" + outName_ + "]/I").c_str());
      }
    }
    for (auto & c : copyFloats_) c.branch(tree, maxEntries);
    for (auto & c : copyInts_) c.branch(tree, maxEntries);
    hasBranched_ = true;
}

void CollectionSkimmer::ensureSize(unsigned int n) {
    if (n > maxEntries_) {
        maxEntries_ = std::max<unsigned>(n, 2*maxEntries_);
        if (saveSelectedIndices_) {
            iOut_.reset(new int[maxEntries_]);
            branch_->SetAddress(iOut_.get());
        }
        if (saveTagForAll_) {
            iTagOut_.reset(new int[maxEntries_]);
            branchTag_->SetAddress(iTagOut_.get());
        }
        for (auto & c : copyFloats_) c.ensureSize(n);
        for (auto & c : copyInts_) c.ensureSize(n);
    }
}

void CollectionSkimmer::declareCopyFloat(const std::string &varname) 
{ 
    _copyVar(varname, (TTreeReaderArray<Float_t>*)nullptr, copyFloats_);
}

void CollectionSkimmer::declareCopyInt(const std::string &varname) 
{
    _copyVar(varname, (TTreeReaderArray<Int_t>*)nullptr, copyInts_);
}

void CollectionSkimmer::copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src) 
{ 
    if (!src) { std::cout << "ERROR: CollectionSkimmer(" << collName_ << " -> " << outName_ << "): asked to copy float " << varname << " from null reader" << std::endl; }
    _copyVar(varname, src, copyFloats_);
}

void CollectionSkimmer::copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src) 
{
    if (!src) { std::cout << "ERROR: CollectionSkimmer(" << collName_ << " -> " << outName_ << "): asked to copy int " << varname << " from null reader" << std::endl; }
    _copyVar(varname, src, copyInts_);
}

void CollectionSkimmer::srcCount(TTreeReaderValue<Int_t> * src)
{
  if (!src) { std::cout << "ERROR: CollectionSkimmer(" << collName_ << " -> " << outName_ << "): null counter reader<int>" << std::endl; }
  srcCount_signed_ = src;
  assert(srcCount_unsigned_ == nullptr);
}

void CollectionSkimmer::srcCount(TTreeReaderValue<UInt_t> * src)
{
  if (!src) { std::cout << "ERROR: CollectionSkimmer(" << collName_ << " -> " << outName_ << "): null counter reader<UInt_t>" << std::endl; }
  srcCount_unsigned_ = src;
  assert(srcCount_signed_ == nullptr);
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


