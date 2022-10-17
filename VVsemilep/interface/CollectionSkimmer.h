#ifndef CMGTools_TTHAnalysis_CollectionSkimmer_h
#define CMGTools_TTHAnalysis_CollectionSkimmer_h
/** CollectionSkimmer
    C++ utility to quickly copy data from one collection to another skimming the list of elements 
*/

#include <memory>
#include <string>
#include <vector>
#include <cassert>
#include <algorithm>
#include <iostream>
class TTree;
#include <Rtypes.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

class CollectionSkimmer {
    public:
        template<typename T1, typename T2> class CopyVar {
            public:
                CopyVar(const std::string &collName, const std::string &varName, TTreeReaderArray<T1> *src=0) :
                      collName_(collName), varName_(varName), in_(src), branch_(NULL) {}
                const std::string & collName() { return collName_; }
                const std::string & varName() { return varName_; }
                void setSrc(TTreeReaderArray<T1> *src) { 
                    if (!src) { std::cout << "ERROR: CollectionSkimmer::CopyVar(" << collName_ << "," << varName_ << ")::setSrc: asked to copy from null reader" << std::endl; }
                    in_ = src; 
                }
                void copy(int ifrom, int ito) { out_[ito] = (*in_)[ifrom]; } 
                void branch(TTree *tree, unsigned int maxEntries) ; 
                void ensureSize(unsigned int n);
            private:
                std::string collName_, varName_;
                TTreeReaderArray<T1> *in_;
                std::unique_ptr<T2[]> out_;
                unsigned int maxEntries_;
                TBranch *branch_;
        };
        typedef CopyVar<float,Float_t> CopyFloat;
        typedef CopyVar<int,Int_t> CopyInt;
	typedef CopyVar<unsigned char, UChar_t> CopyUChar;

        CollectionSkimmer(const std::string &outName, const std::string &collName, bool saveSelectedIndices = false, bool saveTagForAll = false) : outName_(outName), collName_(collName), hasBranched_(false), srcCount_signed_(NULL), srcCount_unsigned_(NULL), saveSelectedIndices_(saveSelectedIndices), saveTagForAll_(saveTagForAll), maxEntries_(0), branch_(NULL), branchTag_(NULL) {}
        CollectionSkimmer(const CollectionSkimmer &other) = delete;
        CollectionSkimmer &operator=(const CollectionSkimmer &other) = delete;

        /// to be called first to register the branches, and possibly re-called if the treeReaderArrays are remade
        void declareCopyFloat(const std::string &varname) ; 
        void declareCopyInt(const std::string &varname) ;
	void declareCopyUChar(const std::string &varname) ;
        void copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src = nullptr) ; 
        void copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src = nullptr) ;
	void copyUChar(const std::string &varname, TTreeReaderArray<UChar_t> * src = nullptr) ;
	void srcCount(TTreeReaderValue<Int_t> * src);
	void srcCount(TTreeReaderValue<UInt_t> * src);

        /// to be called once on the tree, after a first call to copyFloat and copyInt
        void makeBranches(TTree *tree, unsigned int maxEntries, bool padSelectedIndicesCollection = false, int padSelectedIndicesCollectionWith = -1) ;

        unsigned int count() {
            if (srcCount_signed_ == nullptr && srcCount_unsigned_ == nullptr) {
                std::cout << "ERROR: CollectionSkimmer(" << collName_ << " -> " << outName_ << ")::count: both counters are null." << std::endl; 
            }
            assert (srcCount_signed_ != nullptr || srcCount_unsigned_!= nullptr); // pointer to srcCount TTreeReaderValue must be set
            return srcCount_signed_ ? ** srcCount_signed_ : int(**srcCount_unsigned_);
        }
        void ensureSize(unsigned int n);

        //---- to be called on each event for copying ----
        /// clear the output collection
        void clear() {
	  nOut_ = 0;
	  nIn_ = 0;
	  ensureSize(count());
	  if (saveSelectedIndices_) {
	    std::fill_n(iOut_.get(),maxEntries_,padSelectedIndicesCollectionWith_);
	  }
	  if (saveTagForAll_){
	    nIn_ = count();
	    std::fill_n(iTagOut_.get(),nIn_,0);
	  }
	}

        /// push back entry iSrc from input collection to output collection
        void push_back(unsigned int iSrc) {
	  assert(iSrc < count());
	  ensureSize(iSrc);
	  for (auto & c : copyFloats_) c.copy(iSrc, nOut_);
	  for (auto & c : copyInts_) c.copy(iSrc, nOut_);
	  for (auto & c : copyUChars_) c.copy(iSrc, nOut_);
	  if (saveSelectedIndices_) iOut_[nOut_] = iSrc;
	  if (saveTagForAll_) iTagOut_[iSrc] = 1;
	  nOut_++;
        }
        /// push back all entries in iSrcs
        void push_back(const std::vector<int> &iSrcs) {
            for (int i : iSrcs) push_back(i);
        }

        /// resize output collection to a fixed size
        void resize(unsigned int size) { ensureSize(size); nOut_ = size; }

        /// copy from iSrc into iTo (must be iTo < size())
        void copy(unsigned int iSrc, unsigned int iTo) {
            assert(unsigned(nOut_) > iTo);
            if (saveSelectedIndices_) iOut_[iTo] = iSrc;
	    iTagOut_[iSrc] = true; // careful if using with saveTagForAll_, do not overwrite with copy
            for (auto & c : copyFloats_) c.copy(iSrc, iTo);
            for (auto & c : copyInts_) c.copy(iSrc, iTo);
	    for (auto & c : copyUChars_) c.copy(iSrc, iTo);
        }

        /// number of selected output objects
        unsigned int size() const { return nOut_; }

    private:
        std::string outName_;
        std::string collName_;
        Int_t nOut_;
        bool hasBranched_;
        std::unique_ptr<int[]> iOut_;
        TTreeReaderValue<Int_t> *srcCount_signed_;
        TTreeReaderValue<UInt_t> *srcCount_unsigned_;
        std::vector<CopyFloat> copyFloats_;
        std::vector<CopyInt> copyInts_;
	std::vector<CopyUChar> copyUChars_;
	bool saveSelectedIndices_;
	bool padSelectedIndicesCollection_;
	int padSelectedIndicesCollectionWith_;
	bool saveTagForAll_;
	Int_t nIn_;
        std::unique_ptr<int[]> iTagOut_;
	unsigned int maxEntries_;
	TBranch *branch_, *branchTag_;

        template<typename CopyVarVectorT, typename SrcT>
        void _copyVar(const std::string &varname, SrcT * src, CopyVarVectorT &copyVars) ; 
        void _checkNoBranchesYet() ;
};

#endif
