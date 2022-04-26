#include "CMGTools/TTHAnalysis/interface/ONNXInterface.h"
#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"
#include<iostream> 


ONNXInterface::ONNXInterface(const std::string &modelFile, std::vector<std::vector<int64_t>> inputShapes, 
			     std::vector<std::string> inputNames, std::vector<std::string>  outputNames, bool debug):
  _modelFile(modelFile),
  _rt(modelFile),
  _inputShapes(inputShapes),
  _inputNames(inputNames),
  _outputNames(outputNames),
  _debug(debug)
{
    
}


ONNXInterface::~ONNXInterface()
{
}


cms::Ort::FloatArrays ONNXInterface::run(cms::Ort::FloatArrays input_values)
{

  
  return _rt.run(_inputNames, input_values, _inputShapes, _outputNames, 1);

}
