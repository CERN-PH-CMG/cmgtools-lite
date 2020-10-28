#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"
#include <string>


class ONNXInterface
{
 public: 
  ONNXInterface(const std::string &modelFile,std::vector<std::vector<int64_t>> inputShapes,  
		std::vector<std::string> inputNames, std::vector<std::string>  outputNames,
		bool debug=false);
  ~ONNXInterface();
  cms::Ort::FloatArrays run(cms::Ort::FloatArrays);

 protected:
  std::string _modelFile;
  cms::Ort::ONNXRuntime _rt  ;
  std::vector<std::vector<int64_t>> _inputShapes;
  std::vector<std::string> _inputNames;
  std::vector<std::string> _outputNames;
  bool _debug;

};
