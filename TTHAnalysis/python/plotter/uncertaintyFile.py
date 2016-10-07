#!/usr/bin/env python
from math import *
import re
import os, os.path
from array import array
from copy import *

from CMGTools.TTHAnalysis.plotter.fakeRate import *

class Uncertainty:
    def __init__(self,name,procmatch,binmatch,unc_type,extra_args={}):
        self.name = name
        self.procmatch = procmatch
        self.binmatch = binmatch
        self.unc_type = unc_type
        self.extra_args = extra_args
        self.fakerate = [FakeRate(''),FakeRate('')]
        self.fakerate[0]._weight = '1'
        self.fakerate[1]._weight = '1'
        self.prepFR()

    def prepFR(self):

        if self.unc_type=='templateAsymm':
            for idx in xrange(2):
                if 'FakeRate' in self.extra_args[idx]:
                    self.fakerate[idx] = FakeRate(self.extra_args[idx]['FakeRate'])
                if 'AddWeight' in self.extra_args[idx]:
                    self.fakerate[idx]._weight = '(%s)*(%s)'%(self.fakerate[idx]._weight,self.extra_args[idx]['AddWeight'])

        elif self.unc_type=='templateSymm':
            self.fakerate[1] = None
            idx=0
            if 'FakeRate' in self.extra_args[idx]:
                self.fakerate[idx] = FakeRate(self.extra_args[idx]['FakeRate'])
            if 'AddWeight' in self.extra_args[idx]:
                self.fakerate[idx]._weight = '(%s)*(%s)'%(self.fakerate[idx]._weight,self.extra_args[idx]['AddWeight'])
            
        else: raise RuntimeError, 'Uncertainty type not recognised'
            
    def isTrivial(self,sign):
        return (self.getFR(sign)==None)
    def procmatch(self):
        return self.procmatch
    def binmatch(self):
        return self.binmatch
    def unc_type(self):
        return self.unc_type
    def getFR(self,sign):
        if sign=='up': return self.fakerate[0]
        elif sign=='dn': return self.fakerate[1]
        else: raise RuntimeError
    def __str__(self):
        return ' : '.join([self.name,self.procmatch.pattern,self.binmatch.pattern,self.unc_type])+'\n'

class UncertaintyFile:
    def __init__(self,txtfileOrUncertainty):
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
                field = [f.strip() for f in line.split(':')]
                (name, procmatch, binmatch, unc_type) = field[:4]
                procmatch = re.compile(procmatch+'$')
                binmatch = re.compile(binmatch+'$')

                def getSettings(_this_f):
                    extra = {}
                    for setting in [f.replace(';',',').strip() for f in _this_f.replace('\\,',';').split(',')]:
                        if "=" in setting:
                            (key,val) = [f.strip() for f in setting.split("=")]
                            extra[key] = eval(val)
                        else: extra[setting] = True
                    return extra
                self._uncertainty.append(Uncertainty(name,procmatch,binmatch,unc_type,[getSettings(_f) for _f in field[4:]]))

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
