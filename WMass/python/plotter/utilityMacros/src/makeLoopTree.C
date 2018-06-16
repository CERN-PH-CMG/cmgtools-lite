#include "TSystem.h"
#include "TROOT.h"

#include <iostream>
#include <string>
#include <cstdlib> //as stdlib.h                    
#include <cstdio>

#include "../interface/utility.h"

using namespace std;

void makeLoopTree() {

  // load source codes with ++, so that they are always compiled (you never know ...)

  string cmssw_base = getEnvVariable("CMSSW_BASE");
  cout << "CMSSW_BASE = " << cmssw_base << endl;
 
  cout << "Loading functions.cc" << endl;
  gROOT->ProcessLine(Form(".L %s/src/CMGTools/WMass/python/plotter/functions.cc++",cmssw_base.c_str())); 
  cout << "Loading functionsWMass.cc" << endl;
  gROOT->ProcessLine(Form(".L %s/src/CMGTools/WMass/python/plotter/w-helicity-13TeV/functionsWMass.cc++",cmssw_base.c_str()));
  cout << "Loading loopNtuplesSkeleton.cc" << endl;
  gROOT->ProcessLine(".L loopNtuplesSkeleton.C++");

  string command = "loopNtuplesSkeleton(\"/eos/cms/store/group/dpg_ecal/comm_ecal/localreco/TREES_1LEP_80X_V3_WENUSKIM_V5_TINY/\",\"./\",\"wmass_varhists.root\")";
  cout << "Executing " << command << endl;
  gROOT->ProcessLine(command.c_str());
  cout << endl;                                          
  cout << "===========================" << endl;                    
  cout << " THE END!" << endl;                          
  cout << "===========================" << endl;         



}
