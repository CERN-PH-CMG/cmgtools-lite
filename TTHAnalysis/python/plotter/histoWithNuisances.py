#!/usr/bin/env python
from math import sqrt,hypot
from copy import copy
import ROOT

class HistoWithNuisances:
    def __init__(self,histo_central,reset=False):
        self.nominal = histo_central.Clone(histo_central.GetName())
        self.variations = {}
        if reset:
            self.nominal.Reset()
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        return getattr(self.nominal,name)
    def Clone(self,newname):
        h = HistoWithNuisances(self.nominal.Clone(newname))
        for v,p in self.variations.iteritems():
            h.variations[v]=map(lambda x:x.Clone(), p)
        return h
    def Reset(self):
        self.nominal.Reset()
        self.variations = {}
    def printVariations(self):
        print 'central:',self.GetName(),self.Integral()
        for (x,(v1,v2)) in self.variations.iteritems():
            print x,v1.Integral() if v1 else '-',v2.Integral() if v2 else '-'
    def Scale(self,x):
        self.nominal.Scale(x)
        for v,p in self.variations.iteritems(): map(lambda h: h.Scale(x), p)
    def raw(self):
        return self.nominal
    def sumSystUncertainties(self,toadd=None):
        # in each bin, this does max/min of (central,up,down) of each variation and then sums in quadrature upward and downward shifts
        if not toadd: toadd = list(self.variations.keys())
        if "TH" not in self.ClassName(): raise RuntimeError, 'Cannot compute systematic uncertainty for scatter plot'
        hempty = self.raw().Clone(''); hempty.Reset();
        hvars={}
        for var in toadd:
            hvarup = hempty.Clone('')
            hvardn = hempty.Clone('')
            if 'TH1' in self.ClassName():
                for b in xrange(1,self.GetNbinsX()+1):
                    hvarup.SetBinContent(b,max(self.GetBinContent(b),self.variations[var][0].GetBinContent(b),self.variations[var][1].GetBinContent(b))-self.GetBinContent(b))
                    hvardn.SetBinContent(b,self.GetBinContent(b)-min(self.GetBinContent(b),self.variations[var][0].GetBinContent(b),self.variations[var][1].GetBinContent(b)))
            elif 'TH2' in self.ClassName():
                for b1 in xrange(1,self.GetNbinsX()+1):
                    for b2 in xrange(1,self.GetNbinsY()+1):
                        hvarup.SetBinContent(b1,b2,max(self.GetBinContent(b1,b2),self.variations[var][0].GetBinContent(b1,b2),self.variations[var][1].GetBinContent(b1,b2))-self.GetBinContent(b1,b2))
                        hvardn.SetBinContent(b1,b2,self.GetBinContent(b1,b2)-min(self.GetBinContent(b1,b2),self.variations[var][0].GetBinContent(b1,b2),self.variations[var][1].GetBinContent(b1,b2)))
            hvars[var]=[hvarup,hvardn]
        htotup = hempty.Clone(self.GetName()+'_systUp')
        htotdn = hempty.Clone(self.GetName()+'_systDn')
        if 'TH1' in self.ClassName():
            for b in xrange(1,self.GetNbinsX()+1):
                htotup.SetBinContent(b,self.GetBinContent(b)+sqrt(sum(map(lambda x: (hvars[x][0].GetBinContent(b))**2, hvars))))
                htotdn.SetBinContent(b,self.GetBinContent(b)-sqrt(sum(map(lambda x: (hvars[x][1].GetBinContent(b))**2, hvars))))
        elif 'TH2' in self.ClassName():
            for b1 in xrange(1,self.GetNbinsX()+1):
                for b2 in xrange(1,self.GetNbinsY()+1):
                    htotup.SetBinContent(b1,b2,self.GetBinContent(b1,b2)+sqrt(sum(map(lambda x: (hvars[x][0].GetBinContent(b1,b2))**2, hvars))))
                    htotdn.SetBinContent(b1,b2,self.GetBinContent(b1,b2)-sqrt(sum(map(lambda x: (hvars[x][1].GetBinContent(b1,b2))**2, hvars))))
        return [htotup,htotdn]
    def graphAsymmTotalErrors(self,toadd=None,relative=False):
        h = self.raw()
        hup, hdn = self.sumSystUncertainties(toadd)
        xaxis = h.GetXaxis()
        points = []; errors = []
        for i in xrange(h.GetNbinsX()):
            N = h.GetBinContent(i+1);
            dN = h.GetBinError(i+1)
            if N == 0 and dN == 0: continue
            x = xaxis.GetBinCenter(i+1);
            EYlow = hypot(N-min(N,hup.GetBinContent(i+1),hdn.GetBinContent(i+1)),dN)
            EYhigh = hypot(max(N,hup.GetBinContent(i+1),hdn.GetBinContent(i+1))-N,dN)
            EXhigh, EXlow = (xaxis.GetBinUpEdge(i+1)-x, x-xaxis.GetBinLowEdge(i+1))
            if relative:
                errors.append( (EXlow,EXhigh,EYlow/N,EYhigh/N) )
                points.append( (x,1) )
            else:
                errors.append( (EXlow,EXhigh,EYlow,EYhigh) )
                points.append( (x,N) )
        ret = ROOT.TGraphAsymmErrors(len(points))
        ret.SetName(h.GetName()+"_errors")
        for i,((x,y),(EXlow,EXhigh,EYlow,EYhigh)) in enumerate(zip(points,errors)):
            ret.SetPoint(i, x, y)
            ret.SetPointError(i, EXlow,EXhigh,EYlow,EYhigh)
        return ret

    def getVariation(self,alternate):
        return self.variations[alternate]
    def getVariationList(self):
        return self.variations.keys()
    def addVariation(self,name,sign,histo_varied):
        idx = 0 if sign=='up' else 1
        if name not in self.variations: self.variations[name] = [None,None]
        self.variations[name][idx] = histo_varied.Clone('')
    def __iadd__(self,x):
        vars1 = self.variations # writing on self.variations
        vars2 = copy(x.variations)
        for var in set(vars1.keys()+vars2.keys()):
            if var not in vars1: vars1[var] = [self.nominal.Clone(''),self.nominal.Clone('')]
            if var not in vars2: vars2[var] = [x.nominal,x.nominal]
        def adder(v1,v2):
            if "TGraph" in v1.ClassName():
                other = ROOT.TList()
                other.Add(v2)
                v1.Merge(other)
            else:
                v1.Add(v2)
        adder(self.nominal,x.nominal)
        for var in set(vars1.keys()+vars2.keys()):
            for idx in xrange(2): adder(vars1[var][idx],vars2[var][idx])
        return self
    def __add__(self,x):
        h = self.Clone(self.GetName())
        h+=x
        return h

def mergePlots(name,plots):
    one = plots[0].Clone(name)
    for p in plots[1:]:
        one+=p
    return one
