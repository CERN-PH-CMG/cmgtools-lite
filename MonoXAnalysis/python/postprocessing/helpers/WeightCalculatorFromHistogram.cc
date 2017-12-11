#ifndef CMGAnalysis_NanoAODTools_WeightCalculatorFromHistogram_h
#define CMGAnalysis_NanoAODTools_WeightCalculatorFromHistogram_h

#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <TH1.h>

class WeightCalculatorFromHistogram {
 public:
  // get the weight from the bin content of the histogram (has to be set with set histogram
  WeightCalculatorFromHistogram(bool verbose=false) : verbose_(verbose) {}
  // get the weight from the bin content of the passed histogram
  WeightCalculatorFromHistogram(TH1 *histogram, bool verbose=false) : histogram_(histogram), verbose_(verbose) {}
  // get the weight from the bin content of the ratio hist/targethist
  WeightCalculatorFromHistogram(TH1 *hist, TH1* targethist, bool norm=true, bool fixLargeWeights=true, bool verbose=false);
  ~WeightCalculatorFromHistogram() {}

  void setHistogram(TH1 *histogram) { histogram_ = histogram; }

  float getWeight(float x, float y=0) const;
  float getWeightErr(float x, float y=0) const;
  
 private:
  std::vector<float> loadVals(TH1 *hist, bool norm=true);
  TH1* ratio(TH1 *hist, TH1* targethist, bool fixLargeWgts);
  void fixLargeWeights(std::vector<float> &weights, float maxshift=0.0025,float hardmax=3);
  float checkIntegral(std::vector<float> wgt1, std::vector<float> wgt2);

  TH1* histogram_ = nullptr;
  std::vector<float> refvals_,targetvals_;
  bool verbose_;
  bool norm_;
};

WeightCalculatorFromHistogram::WeightCalculatorFromHistogram(TH1 *hist, TH1* targethist, bool norm, bool fixLargeWeights, bool verbose) {
  norm_ = norm;
  verbose_ = verbose;
  if(hist->GetNcells()!=targethist->GetNcells()) {
    std::cout << "ERROR! Numerator and denominator histograms have different number of bins!" << std::endl;
    histogram_=0;
  } else {
    for(int i=0; i<(int)hist->GetNcells(); ++i) {
      refvals_.push_back(hist->GetBinContent(i));
      targetvals_.push_back(targethist->GetBinContent(i));
    }
    histogram_ = ratio(hist,targethist,fixLargeWeights);
  }
}

float WeightCalculatorFromHistogram::getWeight(float x, float y) const {
  if(histogram_==NULL) {
    std::cout << "ERROR! The weights input histogram is not loaded. Returning weight 0!" << std::endl;
    return 0.;
  }
  if(!histogram_->InheritsFrom("TH2")) {
    int bin = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    return histogram_->GetBinContent(bin);
  } else {
    int binx = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    int biny = std::max(1, std::min(histogram_->GetNbinsY(), histogram_->GetYaxis()->FindBin(y)));
    return histogram_->GetBinContent(binx,biny);
  }
}

float WeightCalculatorFromHistogram::getWeightErr(float x, float y) const {
  if(histogram_==NULL) {
    std::cout << "ERROR! The weights input histogram is not loaded. Returning weight error 1!" << std::endl;
    return 1.;
  }
  if(!histogram_->InheritsFrom("TH2")) {
    int bin = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    return histogram_->GetBinError(bin);
  } else {
    int binx = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(x)));
    int biny = std::max(1, std::min(histogram_->GetNbinsX(), histogram_->GetXaxis()->FindBin(y)));
    return histogram_->GetBinError(binx,biny);
  }
}

std::vector<float> WeightCalculatorFromHistogram::loadVals(TH1 *hist, bool norm) {
  int nbins=hist->GetNcells();
  std::vector<float> vals;
  for(int i=0; i<nbins; ++i) {
    double bc=hist->GetBinContent(i);
    double val = (i>0 && bc==0 && hist->GetBinContent(i-1)>0 && hist->GetBinContent(i+1)>0) ? 0.5*(hist->GetBinContent(i-1)+hist->GetBinContent(i+1)) : bc;
    vals.push_back(std::max(bc,0.));
  }
  if(verbose_) std::cout << "Normalization of " << hist->GetName() << ": " << hist->Integral() << std::endl;
  if(norm) {
    float scale = 1.0/hist->Integral();
    for(int i=0; i<nbins; ++i) vals[i] *= scale;
  }
  return vals;
}

TH1* WeightCalculatorFromHistogram::ratio(TH1 *hist, TH1* targethist, bool fixLargeWgts) {
  TH1 *ret = (TH1*)hist->Clone("hweights");
  ret->SetDirectory(0);

  std::vector<float> vals = loadVals(hist,norm_);
  std::vector<float> targetvals = loadVals(targethist,norm_);
  std::vector<float> weights;
  int nbins = vals.size();
  if(verbose_) std::cout << "Weights for variable " << hist->GetName() << " with a number of bins equal to " << nbins << ":" << std::endl;
  for(int i=0; i<nbins; ++i) {
    if(norm_ && fixLargeWgts) {
      if(targetvals[i]<1e-3) targetvals[i]=0.;
      if(vals[i]<1e-3) vals[i]=0.;
    }
    float weight = vals[i] !=0 ? targetvals[i]/vals[i] : 1.;
    if(verbose_) std::cout <<  std::setprecision(4) << weight << " ";
    weights.push_back(weight);
  }
  if(verbose_) std::cout << "." << std::endl;
  if(fixLargeWgts) fixLargeWeights(weights);
  if(verbose_) std::cout << "Final weights: " << std::endl;
  for(int i=0; i<(int)weights.size(); ++i) {
    ret->SetBinContent(i,weights[i]);
    if(verbose_) std::cout << std::setprecision(4) << weights[i] << " ";
  }
  if(verbose_) std::cout << "." << std::endl;
  return ret;
}

float WeightCalculatorFromHistogram::checkIntegral(std::vector<float> wgt1, std::vector<float> wgt2) {
  float myint=0;
  float refint=0;
  for(int i=0; i<(int)wgt1.size(); ++i) {
    myint += wgt1[i]*refvals_[i];
    refint += wgt2[i]*refvals_[i];
  }
  return (myint-refint)/refint;
}

void WeightCalculatorFromHistogram::fixLargeWeights(std::vector<float> &weights, float maxshift,float hardmax) {
  float maxw = std::min(*(std::max_element(weights.begin(),weights.end())),float(5.));
  std::vector<float> cropped(weights); //start with the default weights before cropping
  while (maxw > hardmax) {
    for(int i=0; i<(int)weights.size(); ++i) cropped[i]=std::min(maxw,weights[i]);
    float shift = checkIntegral(cropped,weights);
    if(verbose_) std::cout << "For maximum weight " << maxw << ": integral relative change: " << shift << std::endl;
    if(fabs(shift) > maxshift) break;
    maxw *= 0.95;
  }
  maxw /= 0.95;
  for(int i=0; i<(int)weights.size(); ++i) cropped[i] = std::min(maxw,weights[i]);
  float normshift = checkIntegral(cropped,weights);
  for(int i=0; i<(int)weights.size(); ++i) weights[i] = cropped[i]*(1-normshift);
}

#endif
