#include <TFile.h>
#include <TH1.h>
#include <TF1.h>
#include <TString.h>
#include <TRandom.h>
#include <TMath.h>
#include <assert.h>

class MEtSys {
  
 public:
  MEtSys(TString fileName);
  ~MEtSys(){};

  void ShiftMEt(float metPx,
		float metPy,
		float genVPx, 
		float genVPy,
		float visVPx,
		float visVPy,
		int njets,
		int bkgdType,
		int sysType,
		float sysShift,
		float & metShiftPx,
		float & metShiftPy);

  void ShiftResponseMet(float metPx,
			float metPy,
			float genVPx, 
			float genVPy,
			float visVPx,
			float visVPy,
			int njets,
			int bkgdType,
			float sysShift,
			float & metShiftPx,
			float & metShiftPy);

  
  void ShiftResolutionMet(float metPx,
			  float metPy,
			  float genVPx, 
			  float genVPy,
			  float visVPx,
			  float visVPy,
			  int njets,
			  int bkgdType,
			  float sysShift,
			  float & metShiftPx,
			  float & metShiftPy);

  enum BkgdType{EWK=0, TOP=1};
  enum SysType{Response=0, Resolution=1};

 private:

  void ComputeHadRecoilFromMet(float metX,
			       float metY,
			       float genVPx, 
			       float genVPy,
			       float visVPx,
			       float visVPy,
			       float & Hparal,
			       float & Hperp);


  void ComputeMetFromHadRecoil(float Hparal,
			       float Hperp,
			       float genVPx, 
			       float genVPy,
			       float visVPx,
			       float visVPy,
			       float & metX,
			       float & metY);
  
  
  int nBkgdTypes;
  int nJetBins;
  TH1D * responseHist[2][5];


};
