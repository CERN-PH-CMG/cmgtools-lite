#ifndef CMGTools_TTHAnalysis_CollectionSkimmer_h
#define CMGTools_TTHAnalysis_CollectionSkimmer_h
/** CollectionSkimmer
    C++ utility to quickly copy data from one collection to another skimming the list of elements 
*/

#include <memory>
#include <string>
#include <vector>
#include <cassert>
class TTree;
#include <Rtypes.h>
#include <TTreeReaderArray.h>

class CollectionSkimmer {
    public:
        template<typename T1, typename T2> class CopyVar {
            public:
                CopyVar(const std::string &collName, const std::string &varName, TTreeReaderArray<T1> *src=0) :
                      collName_(collName), varName_(varName), in_(src) {}
                const std::string & collName() { return collName_; }
                const std::string & varName() { return varName_; }
                void setSrc(TTreeReaderArray<T1> *src) { in_ = src; }
                void copy(int ifrom, int ito) { out_[ito] = (*in_)[ifrom]; } 
                void branch(TTree *tree, unsigned int maxEntries) ; 
            private:
                std::string collName_, varName_;
                TTreeReaderArray<T1> *in_;
                std::unique_ptr<T2[]> out_;
        };
        typedef CopyVar<float,Float_t> CopyFloat;
        typedef CopyVar<int,Int_t> CopyInt;

        CollectionSkimmer(const std::string &outName) : outName_(outName), hasBranched_(false) {}
        CollectionSkimmer(const CollectionSkimmer &other) = delete;
        CollectionSkimmer &operator=(const CollectionSkimmer &other) = delete;

        /// to be called first to register the branches, and possibly re-called if the treeReaderArrays are remade
        void copyFloat(const std::string &varname, TTreeReaderArray<Float_t> * src = nullptr) ; 
        void copyInt(const std::string &varname, TTreeReaderArray<Int_t> * src = nullptr) ;

        /// to be called once on the tree, after a first call to copyFloat and copyInt
        void makeBranches(TTree *tree, unsigned int maxEntries) ;

        //---- to be called on each event for copying ----
        /// clear the output collection
        void clear() { nOut_ = 0; }

        /// push back entry iSrc from input collection to output collection
        void push_back(unsigned int iSrc) {
            for (auto & c : copyFloats_) c.copy(iSrc, nOut_);
            for (auto & c : copyInts_) c.copy(iSrc, nOut_);
            nOut_++;
        }
        /// push back all entries in iSrcs
        void push_back(const std::vector<int> &iSrcs) {
            for (int i : iSrcs) push_back(i);
        }

        /// resize output collection to a fixed size
        void resize(unsigned int size) { nOut_ = size; }

        /// copy from iSrc into iTo (must be iTo < size())
        void copy(unsigned int iSrc, unsigned int iTo) {
            assert(unsigned(nOut_) > iTo);
            for (auto & c : copyFloats_) c.copy(iSrc, iTo);
            for (auto & c : copyInts_) c.copy(iSrc, iTo);
        }

        /// number of selected output objects
        unsigned int size() const { return nOut_; }

    private:
        std::string outName_;
        Int_t nOut_;
        std::vector<CopyFloat> copyFloats_;
        std::vector<CopyInt> copyInts_;
        bool hasBranched_;

        template<typename CopyVarVectorT, typename SrcT>
        void _copyVar(const std::string &varname, SrcT * src, CopyVarVectorT &copyVars) ; 
        void _checkNoBranchesYet() ;
};

#endif
