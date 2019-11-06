import re
import os

import ROOT
if "/smearer_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/smearer.cc+" % os.environ['CMSSW_BASE']);
if "/mcCorrections_cc.so" not in ROOT.gSystem.GetLibraries(): 
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/TTHAnalysis/python/plotter/mcCorrections.cc+" % os.environ['CMSSW_BASE']);

class SimpleCorrection:
    def __init__(self,find,replace,procMatch=None,componentMatch=None,onlyForCuts=False,alsoData=False, year=None):
        self._find    = re.compile(find)
        self._replace = replace
        self._procMatch = re.compile(procMatch) if procMatch else None
        self._componentMatch = re.compile(componentMatch) if componentMatch else None
        self._onlyForCuts = onlyForCuts
        self.alsoData = alsoData
        self.year = year
    def __call__(self,expr,process,component,iscut,isdata, year):
        if isdata and not self.alsoData: return expr
        if self.year and self.year != int(year): return expr
        if self._procMatch and not re.match(self._procMatch, process): return expr
        if self._componentMatch and not re.match(self._componentMatch, component   ): return expr
        if self._onlyForCuts and not iscut: return expr
        return re.sub(self._find, self._replace, expr)

class MCCorrections:
    def __init__(self,file):
        self._file = file
        self._corrections = []
        infile = open(file,'r')
        for line in infile:
            if re.match("\s*#.*", line): continue
            while line.strip()[-1] == "\\":
                line = line.strip()[:-1] + infile.next()
            line = re.sub("#.*","",line)
            extra = {}
            if ";" in line:
                (line,more) = line.split(";")[:2]
                for setting in [f.replace(';',',').strip() for f in more.replace(r'\,',';').split(',')]:
                    if "=" in setting: 
                        (key,val) = [f.strip() for f in setting.split("=")]
                        extra[key] = eval(val)
                    else: extra[setting] = True
            field = [f.strip() for f in line.split(':')]
            if len(field) <= 1: continue
            self._corrections.append( SimpleCorrection(field[0], field[1], 
                                    procMatch=(extra['Process'] if 'Process' in extra else None),
                                    componentMatch=(extra['Component'] if 'Component' in extra else None),
                                    onlyForCuts=('OnlyForCuts' in extra),
                                    alsoData=('AlsoData' in extra), 
                                    year=(extra['year'] if 'year' in extra else None)) )
    def __call__(self,expr,process,component,iscut,isdata,year):
        ret = expr
        for c in self._corrections:
            ret = c(ret,process,component,iscut,isdata, year)
        return ret
    def __str__(self): 
        return "MCCorrections('%s')" % self._file
    def __repr__(self): 
        return "MCCorrections('%s')" % self._file

def printcorrections(myglob):
    print 'summary of MC corrections'
    print myglob
    def myprint(x):
        print '%s -> %s   --- data=%s'%(x._find.pattern,x._replace,x.alsoData)
    for c in myglob:
        if isinstance(c,MCCorrections):
            print str(c)
            print len(c._corrections)
            for corr in c._corrections:
                myprint(corr)
        elif isinstance(c,SimpleCorrection):
            myprint(c)
        else: raise RuntimeError, "Unknown object in corrections list"
    
_corrections = []; _corrections_init = []
def loadMCCorrections(options):
    if options not in _corrections_init:
        _corrections_init.append(options)
        for file in options.mcCorrs:
            _corrections.append( MCCorrections(file) )

def globalMCCorrections():
    return _corrections
