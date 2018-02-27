#ifndef PhysicsTools_HepMCCandAlgos_PDFWeightsHelper_h
#define PhysicsTools_HepMCCandAlgos_PDFWeightsHelper_h

#include <Eigen/Dense>

#include <iostream>

class PDFWeightsHelper {
  
public:
  
  PDFWeightsHelper();
  
  void Init(unsigned int nreplicas, unsigned int neigenvectors, const char *incsv);
  void DoMC2Hessian(double nomweight, const double *inweights, double *outweights);
  
  unsigned int neigenvectors() const { return transformation_.cols(); }
  
protected:
  
  Eigen::MatrixXd transformation_;  

};
#endif
