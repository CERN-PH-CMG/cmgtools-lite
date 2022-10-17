from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
import ROOT as r 

class CPmva2lss(Module):
    def __init__(self):

        # number of input variables
        self.jetVariables=6
        self.scalarVariables=9
        self.maxJets=13

        # setup input shape
        inputShapes=r.vector('std::vector<int64_t>')()
        inputShape = r.vector('int64_t')(); 
        inputShape.push_back(1);
        inputShape.push_back(self.maxJets);
        inputShape.push_back(self.jetVariables+self.scalarVariables);
        inputShapes.push_back(inputShape)

        # input names
        inputNames=r.vector('std::string')()
        inputNames.push_back('input_1:0')

        # output names 
        outputNames=r.vector('std::string')()
        outputNames.push_back('Identity:0')

        #... and now the worker
        self.worker=r.ONNXInterface('/t3home/sesanche/ABCnet/abcnet2.1/model.onnx', inputShapes, inputNames, outputNames)

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('score','F')
    def analyze(self, event):
        
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"JetSel_Recl")]
        gen  = [g for g in Collection(event,"GenPart")]

        vars=[]
        
        if len(leps)>=2: 

            for j in jets[:self.maxJets]: 
                if jets.index(j) in [int(event.BDThttTT_eventReco_iJetSel1), int(event.BDThttTT_eventReco_iJetSel2), int(event.BDThttTT_eventReco_iJetSel3)]:
                    setattr(j, 'fromHadTop', True)
                else:
                    setattr(j, 'fromHadTop', False)

                # comprobar si njet25 esta acotada por arriba
                # comprobar el orden de las variables
                vars.extend([ 
                    j.eta, j.phi, j.pt, j.mass, 
                    j.btagDeepFlavB > (0.3093, 0.3033, 0.2770)[event.year-2016], j.fromHadTop,
                    leps[0].pt, leps[0].eta, leps[0].phi,
                    leps[1].pt, leps[1].eta, leps[1].phi,
                    event.nJet25_Recl, event.MET_pt, event.MET_phi]
                        )
            while len(vars)<13*(6+9):
                vars.extend([ 
                    0,0,0,0,
                    0,0,
                    leps[0].pt, leps[0].eta, leps[0].phi,
                    leps[1].pt, leps[1].eta, leps[1].phi,
                    event.nJet25_Recl, event.MET_pt, event.MET_phi]
                )
                
        else:
            vars = self.maxJets*(self.scalarVariables+self.jetVariables)*[0] # all zeros as dummy values

        if len(vars) != self.maxJets*(self.scalarVariables+self.jetVariables):
            raise RuntimeError("Wrong input dimension")
            
        input_values=r.vector('std::vector<float>')()
        input_value =r.vector('float')()
        for var in vars:
            input_value.push_back(var)
        input_values.push_back(input_value)
        result= self.worker.run(input_values)
        self.out.fillBranch('score',result[0][0])

        return True
            
