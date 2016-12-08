// MultiDraw.cxx:
// Draws many histograms in one loop over a tree. 
// A little bit like a TTree::Draw which can make many histograms

#include <TTree.h>
#include <TH1F.h>
#include <TTreeFormula.h>
#include <TStopwatch.h>

#include <iostream>
using std::cout;
using std::endl;

void MultiDraw( TTree *inTree, TTreeFormula *commonWeightFormula, TObjArray *Formulae, TObjArray *Weights, TObjArray *Hists, UInt_t ListLen )
{
    Long64_t i = 0, NumEvents = inTree->GetEntries();
    
    // Get an Element from an array
    #define EL( type, array, index ) dynamic_cast<type *>( array->At( index ) )
    
    Double_t Value = 0, Weight = 0, commonWeight = 0, 
             treeWeight = inTree->GetWeight();
    Int_t TreeNumber = -1;

    TStopwatch s;
    
    for ( i = 0; i < NumEvents; i++ )
    {
        // Display progress every 20000 events
        if ( i % 20000 == 0 )
        {
            cout.precision( 2 );
            
            double nTodo  = NumEvents - i, perSecond = 20000 / s.RealTime();
            Int_t seconds = (Int_t)(nTodo / perSecond), minutes = (Int_t)(seconds / 60.);
            seconds -= (Int_t)(minutes*60.);
            
            // cout << "Done " << (double(i) / ( double(NumEvents)) * 100.0f) << "% ";
            // if ( minutes ) cout << minutes << " minutes ";
            // cout << seconds << " seconds remain.                            \r";
            
            // cout.flush();
            s.Start();
        }
        
        if ( TreeNumber != inTree->GetTreeNumber() )
        {
            treeWeight = inTree->GetWeight();
            TreeNumber = inTree->GetTreeNumber();
        }
        
        inTree->LoadTree( inTree->GetEntryNumber( i ) );
        
        commonWeight = commonWeightFormula->EvalInstance();
        
        // Skip events with 0 weight
        if ( !commonWeight ) 
            continue;
        
        commonWeight *= treeWeight;
        
        for ( UInt_t j = 0; j < ListLen; j++ )
        {
            // If the Value or the Weight is the same as the previous, then it can be re-used.
            // In which case, this element fails to dynamic_cast to a formula, and evaluates to NULL
            if ( EL( TTreeFormula, Formulae, j ) )
                Value = EL( TTreeFormula, Formulae, j )->EvalInstance();
            
            if ( EL( TTreeFormula, Weights,  j ) )
                Weight = EL( TTreeFormula, Weights, j )->EvalInstance() * commonWeight;
        
            if ( Weight )
                EL( TH1F, Hists, j )->Fill( Value, Weight );
        }
    }
}
