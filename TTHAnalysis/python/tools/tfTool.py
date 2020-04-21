import os, ROOT

class TFTool:
    def __init__(self, name, pb, vars, classes, varorder):
        self.name = name
        self.pb   = pb
        self.vars = vars
        self.classes = classes
        self.varorder= varorder
        self.debug   = False

        # set tensorflow interface
        variables_ = ROOT.vector('string')()
        classes_   = ROOT.vector('string')()
        for var in self.varorder: variables_.push_back( var ) 
        for cla in self.classes : classes_.push_back(cla)
        self.worker = ROOT.TensorFlowInterface(pb, variables_, classes_)
        self.outbranches = [ '%s_%s'%(x,self.name) for x in self.classes]
        

    def __call__(self, ev):
        inp = ROOT.std.map('string','double')()
        ret = {} 
        for key in self.varorder:
            var = self.vars[key]
            if self.debug: print key, var(ev) 
            inp[key] = var(ev) 
        res = self.worker(inp)
        for cla in self.classes: 
            if self.debug: print cla, res[cla]
            ret['%s_%s'%(self.name,cla)] = res[cla]
        
        return ret

            
