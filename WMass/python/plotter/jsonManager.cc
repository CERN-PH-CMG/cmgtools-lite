#include <stdio.h>
#include <stdlib.h>
#include <cstdlib> //as stdlib.h
#include <cstdio>
#include <cmath>
#include <iostream>
#include <fstream>
#include <sstream>      // std::istringstream ; to read array of numbers from a line in a file
#include <string>
#include <vector>
#include <map>
#include <utility>      // std::pair
#include <iomanip> //for input/output manipulators

//ROOT header files   
#include <TROOT.h>

using namespace std;

std::map< UInt_t, std::vector< std::pair<UInt_t,UInt_t> > > theJsonMap;
static string formattedJson = "myFormat_LSforPath_HLT_Ele27_WPTight_Gsf.json";

//==========================================================

std::map< UInt_t, std::vector< std::pair<UInt_t,UInt_t> > > makeMapFromJson(const string myJsonFile = "") {

  // format is 
  // run: [ls1,ls2] [ls3,ls4] [...]  note that spaces are important
  // given a json, this format can be obtained with myFormatJson.py
  string run;
  string lumiBlocks;
  std::map< UInt_t, std::vector< std::pair<UInt_t,UInt_t> > > runsAndLumiBlocks;

  // following works only if you are in the CMSSW_BASE area where you have CMGTools/WMass/...         
  char* cmsswPath;
  cmsswPath = getenv ("CMSSW_BASE");
  if (cmsswPath == NULL) {
    cout << "Error in makeMapFromJson(): environment variable CMSSW_BASE not found. Exit" << endl;
    exit(EXIT_FAILURE);
  }

  string jsonFile = Form("%s/src/CMGTools/WMass/python/plotter/%s",cmsswPath,myJsonFile.c_str());

  ifstream inputFile(jsonFile.c_str());

  //cout << "Printing content of " << myJsonFile << endl;

  if (inputFile.is_open()) {


    while (inputFile >> run) {

      // read line without first object that was put in run (the space separates objects in the line)
      getline(inputFile, lumiBlocks);  

      run.assign(run,0,6); // run has 6 digits
      //cout << run << " --> ";

      vector< pair<UInt_t,UInt_t> > blocks;
      stringstream ss(lumiBlocks);     
      string block;

      while (ss >> block) {

    	//cout << block << " ";

    	size_t pos = block.find(",");
    	UInt_t LSin, LSfin;
    	string num1, num2;
    	// we have block = "[a,b]" where a and b are integers. We want to get a and b
    	num1.assign(block,1,pos);
    	num2.assign(block,pos+1,block.size()-1);
    	LSin  = (UInt_t) std::stoi(num1);
    	LSfin = (UInt_t) std::stoi(num2);
    	// cout << "LSin,LSfin = " << LSin << "," << LSfin << endl;
    	blocks.push_back(std::make_pair(LSin,LSfin));

      }

      //runsAndLumiBlocks[run] = blocks;
      //cout << endl;
      runsAndLumiBlocks.insert ( std::pair< UInt_t, std::vector< std::pair<UInt_t,UInt_t > > >((UInt_t) stoi(run), blocks) );
      //      runsAndLumiBlocks.at(stoi(run)) = blocks;

    }

    /////////////////////////
    // check that it works
    // cout << "printing map ..." << endl;
    // for (std::map<UInt_t, vector< pair<UInt_t,UInt_t> > >::iterator it = runsAndLumiBlocks.begin(); it != runsAndLumiBlocks.end(); ++it) {
    //   cout << it->first << " --> "; 
    //   for (UUInt_t i = 0; i < it->second.size(); i++) {
    // 	cout << "[" << it->second.at(i).first << "," << it->second.at(i).second << "]  ";
    //   } 
    //   cout << endl;
    // }
    // cout << endl;
    ///////////////////////////

  } else {
    
    cout << "Error in makeMapFromJson(): could not open file " << jsonFile << endl;
    exit(EXIT_FAILURE);

  }

  return runsAndLumiBlocks;

}

//==========================================================


Bool_t isGoodRunLS(Bool_t isData, UInt_t run, UInt_t lumis) {
  
  // for MC thsi fucntion always return true
  if (not isData) return true;

  // I should make it load the json somewhere else, something like loading the FR file
  if (theJsonMap.empty()) theJsonMap = makeMapFromJson(formattedJson);

  // if (theJsonMap.empty()) {
  //   cout << "Warning in isGoodRunLS(): mymap is empty. Returning false, but please check what's happening!" << endl;
  //   return false;
  // }

  if ( theJsonMap.find(run) == theJsonMap.end() ) return false; // run not found

  Bool_t LSfound = false;

  for (UInt_t i = 0; i < theJsonMap.at(run).size() && !LSfound; ++i) {
    
    // evaluate second value, skip if lumis is bigger (block does not contain it)
    if (lumis >= theJsonMap.at(run).at(i).second) continue;  
    // if arrive here, check lower boundary
    if (lumis >= theJsonMap.at(run).at(i).first ) LSfound = true;

  }

  return LSfound;
    
}

//==========================================================
