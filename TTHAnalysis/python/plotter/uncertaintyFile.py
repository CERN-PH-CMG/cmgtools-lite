#!/usr/bin/env python
from math import *
import re
import os, os.path
from array import array
from copy import *

from CMGTools.TTHAnalysis.plotter.fakeRate import *

class Uncertainty:
    def __init__(self,name,procmatch,binmatch,unc_type,more_args=None,extra=None,options=None):
        self.name = name
        self._procpattern = procmatch
        self._binpattern = binmatch
        self._procmatch = re.compile(procmatch+'$')
        self._binmatch = re.compile(binmatch+'$')
        self.unc_type = unc_type
        self.args = list(more_args) if more_args else []
        self.extra = dict(extra) if extra else {}
        self.fakerate = [FakeRate(''),FakeRate('')]
        self.fakerate[0]._weight = '1'
        self.fakerate[1]._weight = '1'
        self.removeFR = None
        self.trivialFunc=[None,None]
        self.normUnc=[None,None]
        self._postProcess = None
        self._nontrivialSelectionChange = False
        self.prepFR()

    def prepFR(self):

        if self.unc_type=='templateAsymm':
            if 'FakeRates' in self.extra:
                self._nontrivialSelectionChange = True
                for idx in xrange(2):
                    self.fakerate[idx] = FakeRate(self.extra['FakeRates'][idx],loadFilesNow=False)
            if 'AddWeights' in self.extra:
                for idx in xrange(2):
                    self.fakerate[idx]._weight = '(%s)*(%s)'%(self.fakerate[idx]._weight,self.extra['AddWeights'][idx])
            if 'FakeRates' not in self.extra and 'AddWeights' not in self.extra:
                raise RuntimeError("templateAsym requires at least one of FakeRates=['fname1'\\,'fname2'] or AddWeights=['expr1'\\,'expr2']")
        elif self.unc_type=='templateSymm':
            self.fakerate[1] = None
            self.trivialFunc[1] = 'symmetrize_up_to_dn'
            if 'FakeRate' in self.extra:
                self._nontrivialSelectionChange = True
                self.fakerate[0] = FakeRate(self.extra['FakeRate'],loadFilesNow=False)
            if 'AddWeight' in self.extra:
                self.fakerate[0]._weight = '(%s)*(%s)'%(self.fakerate[0]._weight,self.extra['AddWeight'])
            if 'FakeRate' not in self.extra and 'AddWeight' not in self.extra:
                raise RuntimeError("templateAsym requires at least one of FakeRate='fname' or AddWeight='expr'")
        elif self.unc_type=='normAsymm':
            if len(self.args) != 2:
                raise RuntimeError("normAsymm requires two arguments: low and high")
            self.fakerate = [None,None]
            self.trivialFunc = ['apply_norm_up','apply_norm_dn']
            for idx in xrange(2):
                self.normUnc[idx] = float(self.args[1-idx])
        elif self.unc_type=='normSymm':
            if len(self.args) != 1:
                raise RuntimeError("normAsymm requires one argument")
            self.fakerate = [None,None]
            self.trivialFunc = ['apply_norm_up','apply_norm_dn']
            self.normUnc[0] = float(self.args[0])
            self.normUnc[1] = 1.0/self.normUnc[0]
        elif self.unc_type=='none':
            pass
        else: raise RuntimeError, 'Uncertainty type "%s" not recognised' % self.unc_type
        if 'RemoveFakeRate' in self.extra:
            self._nontrivialSelectionChange = True
            self.removeFR = self.extra['RemoveFakeRate']
        if 'Normalize' in self.extra:
            self._postProcess = "Normalize"
        if 'DoesNotChangeEventSelection' in self.extra and self.extra['DoesNotChangeEventSelection']:
            self._nontrivialSelectionChange = False
    def isDummy(self):
        return  self.unc_type == 'none'
    def isTrivial(self,sign):
        return (self.getFR(sign)==None)
    def changesSelection(self,sign):
        if self.isTrivial(sign): return False
        return self._nontrivialSelectionChange
    def getTrivial(self,sign,results):
        idx = 0 if sign=='up' else 1
        if self.getFR(sign) or (self.trivialFunc[idx]==None): raise RuntimeError
        return getattr(self,self.trivialFunc[idx])(results)
    def postProcess(self,central,up,down):
        if self._postProcess == None:
            return
        if self._postProcess == "Normalize":
            h0 = central.Integral()
            if h0 != 0:
                if up.Integral(): 
                    up.Scale(h0/up.Integral())
                else:             
                    for b in xrange(1,up.GetNbinsX()+1): up.SetBinContent(b, central.GetBinContent(b))
                if down.Integral(): 
                    down.Scale(h0/down.Integral())
                else:             
                    for b in xrange(1,up.GetNbinsX()+1): up.SetBinContent(b, central.GetBinContent(b))
            else:
                up.Scale(0); down.Scale(0);
    def isNorm(self):
        return (self.normUnc!=[None,None])

    def symmetrize_up_to_dn(self,results):
        central, up, down = results
        h = central.Clone('');
        h.Multiply(h)
        h.Divide(up)
        return h
    def apply_norm_up(self,results):
        return self.apply_norm('up',results)
    def apply_norm_dn(self,results):
        return self.apply_norm('dn',results)
    def apply_norm(self,sign,results):
        central, up, down = results
        h = central.Clone('')
        h.Scale(self.normUnc[0] if sign=='up' else self.normUnc[1])
        return h

    def procpattern(self):
        return self._procpattern
    def binpattern(self):
        return self._binpattern
    def procmatch(self):
        return self._procmatch
    def binmatch(self):
        return self._binmatch
    def unc_type(self):
        return self.unc_type
    def getFR(self,sign):
        FR = self.fakerate[0 if sign=='up' else 1]
        if FR: FR.loadFiles()
        return FR
    def getFRToRemove(self):
        return self.removeFR
    def __str__(self):
        return ' : '.join([self.name,self._procmatch.pattern,self._binmatch.pattern,self.unc_type])+'\n'

class UncertaintyFile:
    def __init__(self,txtfileOrUncertainty,options=None):
        if type(txtfileOrUncertainty) == list:
            self._uncertainty = deepcopy(txtfileOrUncertainty[:])
        elif isinstance(txtfileOrUncertainty,UncertaintyFile):
            self._uncertainty = deepcopy(txtfileOrUncertainty.uncertainty())
        else:
            self._uncertainty = []
            file = open(txtfileOrUncertainty, "r")
            if not file: raise RuntimeError, "Cannot open "+txtfileOrUncertainty+"\n"
            for line in file:
              try:
                line = line.strip()
                if len(line) == 0 or line[0] == '#': continue
                line = re.sub(r"(?<!\\)#.*","",line)  ## regexp black magic: match a # only if not preceded by a \!
                line = line.replace(r"\#","#")        ## and now we just unescape the remaining #'s
                while line[-1] == "\\":
                    line = line[:-1] + " " + file.next().strip()
                    line = re.sub(r"(?<!\\)#.*","",line)  ## regexp black magic: match a # only if not preceded by a \!
                    line = line.replace(r"\#","#")        ## and now we just unescape the remaining #'s
                extra = {}
                if ";" in line:
                    (line,more) = line.split(";")[:2]
                    more = more.replace("\\,",";")
                    for setting in [f.strip().replace(";",",") for f in more.split(',')]:
                        if "=" in setting: 
                            (key,val) = [f.strip() for f in setting.split("=",1)]
                            extra[key] = eval(val)
                        else: extra[setting] = True
                field = [f.strip() for f in line.split(':')]
                if options and getattr(options,'uncertaintiesToExclude',[]):
                    skipme = True
                    for p0 in options.uncertaintiesToExclude:
                        for p in p0.split(","):
                            if re.match(p+"$", field[0]): skipMe = True
                    if skipme: continue
                (name, procmatch, binmatch, unc_type) = field[:4]
                more_args = field[4:]
                self._uncertainty.append(Uncertainty(name,procmatch,binmatch,unc_type,more_args,extra))

              except ValueError, e:
                print "Error parsing cut line [%s]" % line.strip()
                raise 
    def __str__(self):
        newstring = ""
        for u in self._uncertainty:
            newstring += u.__str__()
        return newstring[:-1]
    def uncertainty(self):
        return self._uncertainty[:]
    def add(self,uncertainty):
        if uncertainty.name in [u.name for u in self._uncertainty]: raise RuntimeError, 'Uncertainty with name %s is already present' % uncertainty.name
        self._uncertainty.append(uncertainty)
