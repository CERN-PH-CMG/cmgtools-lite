{
    gSystem->Load("libFWCoreFWLite");
    // TFile h("/eos/cms/store/mc/RunIISummer16MiniAODv2/DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/60000/BA7F98C8-5AD6-E611-A066-FA163EA7BEB3.root");
    //TFile h("root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v2/70000/5A56C70D-9029-E711-907D-002590DE3A92.root");
    TFile h("5A56C70D-9029-E711-907D-002590DE3A92.root");
    
    fwlite::Run run(&h);
    
    edm::Handle<LHERunInfoProduct> r;
    run.getByLabel<LHERunInfoProduct>(edm::InputTag("externalLHEProducer"), r);
    
    LHERunInfoProduct myLHERunInfoProduct = *(r.product());
    
     //typedef std::vector<LHERunInfoProduct::Comment>::const_iterator headers_const_iterator;
    
    //for (headers_const_iterator iter=myLHERunInfoProduct.comments_begin(); iter!=myLHERunInfoProduct.comments_end(); iter++){
    
     typedef std::vector<LHERunInfoProduct::Header>::const_iterator headers_const_iterator;
    for (headers_const_iterator iter=myLHERunInfoProduct.headers_begin(); iter!=myLHERunInfoProduct.headers_end(); iter++){
      std::cout << iter->tag() << std::endl;
      std::vector<std::string> lines = iter->lines();
      for (unsigned int iLine = 0; iLine<lines.size(); iLine++) {
       std::cout << lines.at(iLine);
      }
    }
}
