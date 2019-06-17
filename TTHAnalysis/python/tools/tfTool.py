import os, ROOT

class TFTool:
    def __init__(self, name, pb, vars, classes):
        self.name = name
        self.pb   = pb
        self.vars = vars
        self.classes = classes

        # set tensorflow interface
        variables_ = ROOT.vector('string')()
        classes_   = ROOT.vector('string')()
        for var in self.vars    : variables_.push_back( var ) 
        for cla in self.classes : classes_.push_back(cla)
        self.worker = ROOT.TensorFlowInterface(pb, variables_, classes_)
        self.outbranches = [ '%s_%s'%(x,self.name) for x in self.classes]
        

    def __call__(self, ev):
        inp = ROOT.std.map('string','double')()
        ret = {} 
        for key, var in self.vars.iteritems():
            inp[key] = var(ev) 
        res = self.worker(inp)
        for cla in self.classes: 
            ret['%s_%s'%(self.name,cla)] = res[cla]
        
        return ret

            
