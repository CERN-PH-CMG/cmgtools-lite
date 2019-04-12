#!/usr/bin/env python
from math import sqrt,hypot,log,exp
from copy import copy
from array import array
import ROOT

def _cloneNoDir(hist,name=''):
    ret = hist.Clone(name)
    ret.SetDirectory(None)
    return ret

def _projectionXNoDir(hist2d,name,y1,y2):
    nx = hist2d.GetNbinsX()
    ax = hist2d.GetXaxis()
    xbins = array('f',[(ax.GetBinLowEdge(b+1) if b < nx else ax.GetBinUpEdge(b)) for b in xrange(0,nx+1)])
    proj = ROOT.TH1D(name,name,nx,xbins); proj.SetDirectory(None)
    proj.GetXaxis().SetTitle(ax.GetTitle()) # in case
    ys = range(y1,y2+1)
    for ix in xrange(1,nx+1):
        proj.SetBinContent(ix, sum(hist2d.GetBinContent(ix,y) for y in ys))
        proj.SetBinError(ix, sqrt(sum(hist2d.GetBinError(ix,y)**2 for y in ys)))
    return proj

def cropNegativeBins(histo):
            if "TH1" in histo.ClassName():
                for b in xrange(0,histo.GetNbinsX()+2):
                    if histo.GetBinContent(b) < 0: histo.SetBinContent(b, 0.0)
            elif "TH2" in histo.ClassName():
                for bx in xrange(0,histo.GetNbinsX()+2):
                    for by in xrange(0,histo.GetNbinsY()+2):
                        if histo.GetBinContent(bx,by) < 0: histo.SetBinContent(bx,by, 0.0)
            elif "TH3" in histo.ClassName():
                for bx in xrange(0,histo.GetNbinsX()+2):
                    for by in xrange(0,histo.GetNbinsY()+2):
                        for bz in xrange(0,histo.GetNbinsZ()+2):
                            if histo.GetBinContent(bx,by,bz) < 0: histo.SetBinContent(bx,by,bz, 0.0)

def _isNullHistogram(h):
    if h.Integral() != 0: return False
    if "TH1" in h.ClassName():
        for b in xrange(0,h.GetNbinsX()+2):
            if h.GetBinContent(b) != 0: return False
        return True
    elif "TH2" in h.ClassName():
        for bx in xrange(1,h.GetNbinsX()+1):
            for by in xrange(1,h.GetNbinsY()+1):
                if h.GetBinContent(bx,by) != 0: return False
        return True
    elif "TH3" in h.ClassName():
        for bx in xrange(1,h.GetNbinsX()+1):
          for by in xrange(1,h.GetNbinsY()+1):
            for bz in xrange(1,h.GetNbinsZ()+1):
               if h.GetBinContent(bx,by,bz) != 0: return False
        return True
    elif "TGraph" in h.ClassName():
        return (h.GetN() == 0)
    return False

class RooFitContext:
    def __init__(self,workspace):
        self.workspace = workspace
        self._import = getattr(workspace,'import')
        self.xvar = None
        self._rebin = False
    def prepareXVar(self,histo,density,name="x"):
        if "TH1" not in histo.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        self.xname = name
        self._histo = _cloneNoDir(histo, "_template_"); 
        if density: 
            self._rebin   = True
            self._density = True
        else:
            self._density = False
            axis = histo.GetXaxis()
            w0 = axis.GetBinWidth(1)
            for b in xrange(2,histo.GetNbinsX()):
                if axis.GetBinWidth(b) != w0:
                    self._rebin = True
                    break
        if self._rebin:
            self.xvar   = ROOT.RooRealVar(name,name, 0.0, histo.GetNbinsX())
            self._xdummy = ROOT.TH1F(name,name, histo.GetNbinsX(), 0.0, histo.GetNbinsX())
        else:
            self.xvar = ROOT.RooRealVar(name,name, axis.GetXmin(), axis.GetXmax())
        self.xvar.setBins(histo.GetNbinsX())
    def hist2roofit(self,histo):
        """If needed, transform input histogram produced by ROOT via Draw to deal with non-uniform binning, so that it can be used in RooFit without worries
           Input histogram is not modified"""
        if not self._rebin: return histo
        if "TH1" not in histo.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        ret = _cloneNoDir(self._xdummy, histo.GetName()+"_rebin")
        for b in xrange(1,histo.GetNbinsX()):
            scale = histo.GetXaxis().GetBinWidth(b) if self._density else 1.0
            ret.SetBinContent(b, scale * histo.GetBinContent(b))
        return ret
    def roofit2hist(self,histo,norm,target=None,add=False):
        """Transform input histogram produced by RooFit via createHistogram to undo what hist2roofit did, and set normalization
           Input histogram may be modified. Output may be the same object as input (but modified), or a new object."""
        if add and not target: raise RuntimeError("roofit2hist: can't set add without target")
        if histo.Integral(): 
            histo.Scale(norm/histo.Integral())
        if self._rebin or target != None:
            if "TH1" not in histo.ClassName(): raise RuntimeError("Unsupported for non-TH1")
            if target == None:
                target = _cloneNoDir(self._histo, histo.GetName())
            for b in xrange(1,histo.GetNbinsX()+1):
                scale = 1.0/histo.GetXaxis().GetBinWidth(b) if self._density else 1.0
                if add: target.SetBinContent(b, scale * histo.GetBinContent(b) + target.GetBinContent(b))
                else:   target.SetBinContent(b, scale * histo.GetBinContent(b))
            histo = target
        return histo
    def roopdf2hist(self,name,pdf,normobj,target=None,add=False):
        """Create a new histogram from a pdf, and normalize it according to a given RooAbsReal.
           If a target histogram is provided, write the output into it with SetBinContent."""
        if normobj.getVal() == 0:
            if target != None:
                target.Reset()
                return target
            pdf.Print("t");
            normobj.Print("t");
            raise RuntimeError("zero norm for %s, pdf %s, name %s" % (normobj.GetName(), pdf.GetName(), name))
        if ROOT.gROOT.FindObject(name): ROOT.gROOT.FindObject(name).Delete()
        if ROOT.gROOT.FindObject(name+"__"+self.xvar.GetName()): ROOT.gROOT.FindObject(name+"__"+self.xvar.GetName()).Delete()
        histo = pdf.createHistogram(name, self.xvar)
        histo.SetDirectory(None)
        return self.roofit2hist(histo,normobj.getVal(),target=target,add=add)
    def imp(self,obj,*args):    
        self._import(obj,*args)
        if hasattr(self.workspace,'nodelete'):
            self.workspace.nodelete.append(obj)
    def factory(self,expr,neverDelete=True):
        x = self.workspace.factory(expr)
        if neverDelete and hasattr(self.workspace,'nodelete'):
            self.workspace.nodelete.append(x)
        return x
        
class PostFitSetup:
    def __init__(self,params=None,constraints=None,fitResult=None,throwPreFitToys=0,throwPostFitToys=0):
        self.params    = (params if params != None else (fitResult.floatParsFinal() if fitResult else None))
        self.constraints = constraints
        self.fitResult = fitResult
        self._preFitToys = None
        self._postFitToys = None
        if throwPreFitToys:
            if params == None or constraints == None: 
                raise RuntimeError("Can't throw pre-fit toys without nuisances and constraint terms")
            self._throwPreFit(throwPreFitToys)
        if throwPostFitToys:
            if fitResult == None: 
                raise RuntimeError("Can't throw pre-fit toys without nuisances and constraint terms")
            if params != None:
                self._checkParamsForPostFit()
            self._throwPostFit(throwPostFitToys)
    def postFitToys(self,ntoys_min=500):
        if self._postFitToys == None or self._postFitToys.numEntries() < ntoys_min:
            self._throwPostFit(ntoys_min)
        return self._postFitToys
    def preFitToys(self,ntoys_min=500):
        if self._preFitToys == None or self._preFitToys.numEntries() < ntoys_min:
            self._throwPreFit(ntoys_min)
        return self._preFitToys
    def _throwPostFit(self,ntoys):
        obs = ROOT.RooArgSet(self.params).snapshot()
        dtoy = ROOT.RooDataSet("postFitToys","",obs)
        #print "Throwing %d toys of %d nuisances" % (ntoys, obs.getSize())
        #timer = ROOT.TStopwatch()
        for i in xrange(ntoys):
            obs.assignValueOnly(self.fitResult.randomizePars())
            dtoy.add(obs)
        #print "Thrown %d toys of %d nuisances in %.3f s" % (ntoys, obs.getSize(), timer.RealTime())
        self._postFitToys = dtoy
    def _throwPreFit(self,ntoys):
        if self.params == None: raise RuntimeError("Can't throw pre-fit toys without nuisances")
        obs = ROOT.RooArgSet(self.params).snapshot()
        dtoy = ROOT.RooDataSet("preFitToys","",obs)
        print "Throwing %d pre-fit toys of %d nuisances" % (ntoys, obs.getSize())
        #obs.Print("")
        #timer = ROOT.TStopwatch()
        for i in xrange(ntoys):
            it = obs.fwdIterator()
            for i in xrange(obs.getSize()):
                it.next().setVal(ROOT.gRandom.Gaus())
            dtoy.add(obs)
        #print "Thrown %d pre-fit toys of %d nuisances in %.3f s" % (ntoys, obs.getSize(), timer.RealTime())
        self._preFitToys = dtoy
    def makeFitLog(self):
        if not self.fitResult: return []
        log = [ "FIT RESULT (status = %d, covQual %d, edm %g)" % (self.fitResult.status(), self.fitResult.covQual(), self.fitResult.edm()), [] ]
        init  = self.fitResult.floatParsInit()
        final = self.fitResult.floatParsFinal()
        names = [ init.at(i).GetName() for i in xrange(init.getSize()) ]
        maxlen = max(max(map(len,names)),15)
        nfmt  = "%%-%ds" % maxlen
        log.append( (nfmt+"     %-10s      %-10s +- %-10s      [ %-10s , %-10s ]") % ("Parameter", " PreFit", " PostFit", "   Err", "   Min", "   Max") )
        log.append( (nfmt+"     %-10s      %-10s----%-10s      --%-10s---%-10s--") % ("-"*maxlen, "-"*10, "-"*10, "-"*10, "-"*10, "-"*10) )
        for n in sorted(names):
            pre, post = init.find(n), final.find(n)
            log.append( (nfmt+"     %10.4f     %10.4f +- %10.4f      [ %10.4f , %10.4f ]") % (
                            n, pre.getVal(), post.getVal(), post.getError(), pre.getMin(), pre.getMax() ) )
        return log
        
class HistoWithNuisances:
    def __init__(self,histo_central,reset=False):
        if isinstance(histo_central, HistoWithNuisances): raise RuntimeError, "Created with HWN instead of THn or TGraph"
        self.central = _cloneNoDir(histo_central, histo_central.GetName())
        self.nominal = self.central # pre-fit state
        self.variations = {}
        if reset:
            self.nominal.Reset()
        self._rooFit  = None
        self._postFit = None
        self._usePostFit = True
    def __getstate__(self):
        """Needed to pickle"""
        ret = { 'name':self.central.GetName(), 'central':self.central, 'nominal':None }
        if self.nominal != self.central:
            ret['nominal'] = self.nominal; 
        variations = []
        for (x,(v1,v2)) in self.variations.iteritems():
            variations.append((x,(v1,v2)))
        ret['variations'] = variations
        return ret
    def __setstate__(self,state):
        """Needed to un-pickle"""
        self.central = _cloneNoDir(state['central'], state['name'])
        self.nominal = _cloneNoDir(state['nominal'], state['name']+"_nominal") if (state['nominal'] != None) else self.central
        self.variations = dict()
        for (x,(v1,v2)) in state['variations']:
            v1c = _cloneNoDir(v1, "%s_%s_up"   % (self.central.GetName(),x))
            v2c = _cloneNoDir(v2, "%s_%s_down" % (self.central.GetName(),x))
            self.variations[x] = (v1c, v2c)
        self._rooFit  = None
        self._postFit = None
        self._usePostFit = True
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        return getattr(self.nominal if self._usePostFit else self.central, name)
    def isSimple(self):
        if len(self.variations) != 0: return False
        if self.nominal != self.central: return False
        if self._rooFit or self._postFit: return False
        return True
    def isZero(self):
        if not _isNullHistogram(self.central): 
            return False
        for v,p in self.variations.iteritems():
            for h in p:
                if not _isNullHistogram(h): return False
        return True
    def Clone(self,newname):
        h = HistoWithNuisances(_cloneNoDir(self.central, newname))
        for v,p in self.variations.iteritems():
            h.variations[v] = map(lambda x: _cloneNoDir(x,x.GetName()), p)
        if self.nominal == self.central:
            h.nominal = h.central
        else:
            h.nominal = _cloneNoDir(self.nominal, newname)
        if self._rooFit: h.setupRooFit(self._rooFit["context"])
        h._postFit = self._postFit
        h._usePostFit = self._usePostFit
        return h
    def Reset(self):
        self.central.Reset()
        self.nominal.Reset()
        self.variations = {}
        self._dropPdfAndNorm()
    def printVariations(self):
        print 'central:',self.GetName(),self.Integral()
        for (x,(v1,v2)) in self.variations.iteritems():
            print x,v1.Integral() if v1 else '-',v2.Integral() if v2 else '-'
    def Scale(self,x):
        if self._rooFit and 'norm' in self._rooFit:
            self._rooFit['norm'].setNominalValue(self.central.Integral() * x)
        self.central.Scale(x)
        if self.nominal != self.central: self.nominal.Scale(x)
        for v,p in self.variations.iteritems(): map(lambda h: h.Scale(x), p)
    def addRooFitScaleFactor(self,roofunc):
        if not self._rooFit: raise RuntimeError, "Component was not roofitized before"
        if "norm" not in self._rooFit: self._makePdfAndNorm()
        self._rooFit["norm"].addOtherFactor(roofunc)
        self._rooFit["scaleFactors"][roofunc.GetName()] = roofunc
    def rooFitScaleFactors(self):
        if self._rooFit:
            if "scaleFactors" in self._rooFit: 
                return self._rooFit["scaleFactors"]
        return {}
    def raw(self):
        return self.nominal if self._usePostFit else self.central
    def sumSystUncertainties(self,toadd=None):
        """in each bin, this does max/min of (central,up,down) of each variation and then sums in quadrature upward and downward shifts"""
        if toadd == []: return [self.nominal,self.nominal]
        if self._postFit and self._usePostFit and toadd != None: raise RuntimeError, "Selection of nuisances yet implemented for post-fit"
        if toadd == None: toadd = list(self.variations.keys())
        if "TH" not in self.ClassName(): raise RuntimeError, 'Cannot compute systematic uncertainty for scatter plot'
        hempty = _cloneNoDir(self.central); hempty.Reset()
        htotup = _cloneNoDir(hempty, self.GetName()+'_systUp')
        htotdn = _cloneNoDir(hempty, self.GetName()+'_systDn')
        if self._postFit and self._usePostFit:
            if "pdf" not in self._rooFit: self._makePdfAndNorm()
            toys = self._postFit.postFitToys()
            if "TH1" not in self.nominal.ClassName(): raise RuntimeError("Unsupported for non-TH1")
            nom_bins = [ self.nominal.GetBinContent(b) for b in xrange(1,self.nominal.GetNbinsX()+1) ]
            sumw2s   = [ 0. for x in nom_bins ]
            #vals     = [ [] for x in nom_bins ]
            wvars    = self._rooFit["workspace"].allVars()
            pdf, norm = self._rooFit["pdf"], self._rooFit["norm"]
            roofit = self._rooFit["context"]
            #timer = ROOT.TStopwatch()
            for i in xrange(toys.numEntries()):
                wvars.assignValueOnly(toys.get(i))
                roofit.roopdf2hist("_toy", pdf, norm, target=hempty)
                for ib,x0 in enumerate(nom_bins):
                    #vals[ib].append(hempty.GetBinContent(ib+1))
                    sumw2s[ib] += (hempty.GetBinContent(ib+1)-x0)**2
            #print "Used %d post-fit toys to make histograms in %.3f s" % (toys.numEntries(), timer.RealTime())
            #print "postfit plot of %s" % (self.central.GetName())
            for ib,(x0,xw2) in enumerate(zip(nom_bins,sumw2s)):
                #print "   bin %2d: %9.3f +- %6.3f" % (ib+1, x0, sqrt(xw2/toys.numEntries()))
                htotup.SetBinContent(ib+1,       x0 + sqrt(xw2/toys.numEntries()))
                htotdn.SetBinContent(ib+1, max(0,x0 - sqrt(xw2/toys.numEntries())))
        else:
            hvars={}
            # compute up envelope and down envelope for all variations
            for var in toadd:
                hvarup = _cloneNoDir(hempty)
                hvardn = _cloneNoDir(hempty)
                hup, hdn = self.variations[var][0], self.variations[var][1]
                if 'TH1' in self.ClassName():
                    for b in xrange(1,self.GetNbinsX()+1):
                        hvarup.SetBinContent(b,max(self.GetBinContent(b),hup.GetBinContent(b),hdn.GetBinContent(b))-self.GetBinContent(b))
                        hvardn.SetBinContent(b,self.GetBinContent(b)-min(self.GetBinContent(b),hup.GetBinContent(b),hdn.GetBinContent(b)))
                elif 'TH2' in self.ClassName():
                    for b1 in xrange(1,self.GetNbinsX()+1):
                        for b2 in xrange(1,self.GetNbinsY()+1):
                            hvarup.SetBinContent(b1,b2,max(self.GetBinContent(b1,b2),hup.GetBinContent(b1,b2),hdn.GetBinContent(b1,b2))-self.GetBinContent(b1,b2))
                            hvardn.SetBinContent(b1,b2,self.GetBinContent(b1,b2)-min(self.GetBinContent(b1,b2),hup.GetBinContent(b1,b2),hdn.GetBinContent(b1,b2)))
                hvars[var]=[hvarup,hvardn]
            # sum in quadrature all the up envelopes and down envelopes
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
    def integralSystError(self,toadd=None,relative=False,symmetrize=True,cropAtZero=True):
        """Compute the systematic-only uncertainty on the integral. Does not add the MC statistics."""
        if "TH" not in self.ClassName(): raise RuntimeError, 'Cannot compute systematic uncertainty for scatter plot'
        i0 = self.raw().Integral()
        if relative and i0 == 0: return 0 if symmetrize else (0,0)
        if self._postFit and self._usePostFit: 
            if toadd == None and symmetrize==True:
                if "norm" not in self._rooFit: self._makePdfAndNorm()
                toys = self._postFit.postFitToys()
                wvars = self._rooFit["workspace"].allVars()
                norm  = self._rooFit["norm"]
                nominal, sumw2 = norm.getVal(), 0.0
                for i in xrange(toys.numEntries()):
                    wvars.assignValueOnly(toys.get(i))
                    sumw2 += (norm.getVal()-nominal)**2
                wvars.assignValueOnly(self._postFit.fitResult.floatParsFinal()) # recover central values
                #print "postfit norm of %-40s: %8.2f +- %5.2f (%.3f)" % (self.central.GetName(), nominal, sqrt(sumw2/toys.numEntries()), sqrt(sumw2/toys.numEntries())/nominal)
                return sqrt(sumw2/toys.numEntries())
            else:
                raise RuntimeError("Not implemented yet")
        else:
            if toadd == None: toadd = list(self.variations.keys())
            iup2, idown2 = 0., 0.
            for var in toadd:
                shifts = [self.variations[var][i].Integral()-i0 for i in (0,1)]
                iup2   += max(0, max(shifts))**2
                idown2 += max(0,-min(shifts))**2
            iup, idown = sqrt(iup2), sqrt(idown2)
        if cropAtZero: idown = min(idown,i0)
        if relative:
            iup /= i0; idown /= i0
        return sqrt(0.5*(iup**2+idown**2)) if symmetrize else (-idown,iup)
    def graphAsymmTotalErrors(self,toadd=None,relative=False):
        if "TH1" not in self.central.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        h = self.raw()
        hup, hdn = self.sumSystUncertainties(toadd)
        xaxis = h.GetXaxis()
        points = []; errors = []
        for i in xrange(h.GetNbinsX()):
            N = h.GetBinContent(i+1);
            dN = h.GetBinError(i+1) if len(self.variations) == 0 else 0 #FIXME
            if N == 0 and (dN == 0 or relative): continue
            x = xaxis.GetBinCenter(i+1);
            EYlow = hypot(N-hdn.GetBinContent(i+1),dN)
            EYhigh = hypot(hup.GetBinContent(i+1)-N,dN)
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
    def cropNegativeBins(self, allVariations=True):
        cropNegativeBins(self.nominal)
        if allVariations:
            cropNegativeBins(self.central)
            for hs in self.variations.itervalues():
                for h in hs: cropNegativeBins(h)
    def getCentral(self):
        return self.central
    def getVariation(self,alternate):
        return self.variations[alternate]
    def hasVariation(self,alternate):
        return (alternate in self.variations)
    def hasVariations(self):
        return bool(self.variations) 
    def getVariationList(self):
        return self.variations.keys()
    def addVariation(self,name,sign,histo_varied, clone=True):
        idx = 0 if sign=='up' else 1
        if name not in self.variations: self.variations[name] = [None,None]
        self.variations[name][idx] = _cloneNoDir(histo_varied) if clone else histo_varied
        # invalidate caches
        if self._rooFit or self._postFit:
            print "WARNING: adding a variantion on an object that already has roofit/postfit info"
            self._rooFit  = None
            self._postFit = None
    def addBinByBin(self, namePattern="{name}_bbb_{bin}", ycutoff=1e-3, relcutoff=1e-2, verbose=False, norm=False, conservativePruning=False):
        if "TH1" not in self.central.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        ref = self.central
        ytot = ref.Integral()
        if (ytot == 0): return 
        for b in xrange(1,ref.GetNbinsX()+1):
            y, e = ref.GetBinContent(b), ref.GetBinError(b)
            if y <= 0 or e < 0: continue
            if conservativePruning: # conservative adaptive pruning that was used in makeShapeCards in the past
                if e < 0.1*sqrt(y+0.04): continue 
            else:
                if y/ytot < ycutoff: continue
                if e/y    < relcutoff: continue
                if e < 0.2*sqrt(y+1): continue
            if verbose: 
                print "\tbin %3d: yield %9.1f +- %9.1f (rel %.5f), rel err. %.4f, poisson %.1f" % (b, y, e, y/ytot, e/y if y else 1, sqrt(y+1))
            hi = _cloneNoDir(ref)
            lo = _cloneNoDir(ref)
            hi.SetBinContent(b, y+e)
            lo.SetBinContent(b, y*y/(y+e))
            if norm:
                hi.Scale(ytot/hi.Integral())
                lo.Scale(ytot/lo.Integral())
            nuis = namePattern.format(name=self.central.GetName(), bin=b)
            self.variations[nuis] = [ hi, lo ] 
            self.central.SetBinError(b, 0) # otherwise it's double-counted in the plots
        if self._rooFit or self._postFit:
            print "WARNING: addBinByBinn on an object that already has roofit/postfit info"
            self._rooFit  = None
            self._postFit = None
    def isShapeVariation(self,name,tolerance=1e-5,debug=False):
        """return true if the specified variation alters the shape of the histogram.
           this is tested by checking if the ratio between non-empty bins of the 
           nominal and varied histogram are identical within the tolerance"""
        if "TH1" not in self.central.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        h0 = self.central
        for h in self.variations[name]:
            ratio = None 
            for b in xrange(1,h0.GetNbinsX()+1):
                y0 = h0.GetBinContent(b)
                y  =  h.GetBinContent(b)
                if debug: 
                    print "  bin %3d  nominal %9.4f  varied %9.4f   ratio %8.5f   diff %8.5f" % (
                                b, y0, y, (y/y0 if y0 else 1), y/y0-ratio if (ratio != None and y0 != 0) else 0)
                if (y0 == 0):
                    if (y != 0): return True
                elif y == 0: 
                    return True
                else:
                    if ratio is None:
                        ratio = y/y0
                    else:
                        if abs(y/y0 - ratio) > tolerance: 
                            return True
        return False
    def regularizeVariation(self, var, minUnweightedEvents=12, minRatio=0.2, quiet=False, debug=False, binname="<unknown bin>"):
        if "TH1" not in self.central.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        if var not in self.variations: return
        h = self.central
        (hup,hdown) = self.variations[var]
        s0,su,sd = 0,0,0
        s02,su2,sd2 = 0,0,0
        reg_xy, reg_nx = [], 0
        xscale = 1.0/float(h.GetNbinsX())
        for ib in xrange(h.GetNbinsX()):
            y0,yu,yd = h.GetBinContent(ib+1),hup.GetBinContent(ib+1),hdown.GetBinContent(ib+1) 
            if y0 == 0 and yu == 0 and yd == 0: continue
            e0,eu,ed = h.GetBinError(ib+1),hup.GetBinError(ib+1),hdown.GetBinError(ib+1) 
            if y0: 
                if yu > minRatio*y0: reg_xy.append((ib*xscale, log(yu/y0), max(e0,eu)/y0))
                if yd > minRatio*y0: reg_xy.append((ib*xscale, log(y0/yd), max(e0,ed)/y0))
                if yu > minRatio*y0 or yd > minRatio*y0: reg_nx += 1
            s0 += y0; su += yu; sd += yd
            s02 += e0**2; su2 += eu**2; sd2 += ed**2
        if debug: print "Template for %s %s %s effective unweighted events: %9.2f" % (binname, h.GetName(), var, s0**2/s02)
        if (s0**2/s02) < minUnweightedEvents and len(reg_xy) > 0:
            #print "     data points for regularization: %d (%d independent x values) " % (len(reg_xy), reg_nx)
            s1, sx, sy, sxx, sxy = 0,0,0,0,0
            for rx, ry, dry in reg_xy:
                #print "          %8.4f    %8.4f +- %8.4f" % (rx, ry, dry)
                w = 1.0/dry**2
                s1  += w
                sx  += w * rx
                sy  += w * ry
                sxy += w * rx*ry
                sxx += w * rx*rx
            det = sxx*s1 - sx**2
            if reg_nx > 1 and det != 0:
                alpha = (sxx * sy - sx * sxy)/det 
                beta  = (-sx * sy + s1 * sxy)/det 
            else:
                alpha = sy/s1
                beta  = 0
            #print "     -> alpha %+8.4f   beta %+8.4f    kappa = exp(alpha) = %6.3f " % (alpha, beta, exp(alpha))
            spu, spd = 0,0
            for ib in xrange(h.GetNbinsX()):
                y0,yu,yd = h.GetBinContent(ib+1),hup.GetBinContent(ib+1),hdown.GetBinContent(ib+1) 
                e0,eu,ed = h.GetBinError(ib+1),hup.GetBinError(ib+1),hdown.GetBinError(ib+1) 
                pu = y0 * exp(alpha + beta*ib*xscale)
                pd = y0 / exp(alpha + beta*ib*xscale)
                hup.SetBinContent(ib+1, pu); hdown.SetBinContent(ib+1, pd)
                if y0 == 0 and yu == 0 and yd == 0: continue
                if debug: print "     bin %2d    nominal  %7.3f +- %7.3f     up:  %7.3f +- %6.3f -> %7.3f (%+5.2fs)   down: %7.3f +- %6.3f -> %7.3f (%+5.2fs)      dup: %6.3f (%6.3f) -> %6.3f (%6.3f)    ddown: %6.3f (%6.3f) -> %6.3f (%6.3f) " % (
                                ib+1, y0,e0,  
                                yu,eu, pu, min(max( (pu-yu)/(max(e0,eu) if e0 else 1e-5),  -9.99),+9.99),
                                yd,ed, pd, min(max( (pd-yd)/(max(e0,ed) if e0 else 1e-5),  -9.99),+9.99),
                                (yu-y0),  min(abs(yu/y0 if y0 else 99.999),99.999),  (pu-y0),  min(abs(pu/y0 if y0 else 99.999),99.999),  
                                (yd-y0),  min(abs(yd/y0 if y0 else 99.999),99.999),  (pd-y0),  min(abs(pd/y0 if y0 else 99.999),99.999))
                spu += pu; spd += pd
            if debug: print "         total nominal  %7.3f +- %7.3f     up:  %7.3f +- %6.3f -> %7.3f (%+5.2fs)   down: %7.3f +- %6.3f -> %7.3f (%+5.2fs)      dup: %6.3f (%6.3f) -> %6.3f (%6.3f)    ddown: %6.3f (%6.3f) -> %6.3f (%6.3f) " % (
                                s0,sqrt(s02),  
                                su,sqrt(su2), spu, min(max( (su-spu)/(sqrt(max(s02,su2)) if s02 else 1e-5),  -9.99),+9.99),
                                sd,sqrt(sd2), spd, min(max( (sd-spd)/(sqrt(max(s02,sd2)) if s02 else 1e-5),  -9.99),+9.99),
                                (su-s0),  min(abs(su/s0 if s0 else 99.999),99.999),  (spu-s0),  min(abs(spu/s0 if s0 else 99.999),99.999),  
                                (sd-s0),  min(abs(sd/s0 if s0 else 99.999),99.999),  (spd-s0),  min(abs(spd/s0 if s0 else 99.999),99.999))
            elif not quiet: print "Info: template %s %s %s effective unweighted events %.2f was regularized. kup = %.2f, kdown = %.2f" % (binname, h.GetName(), var, s0**2/s02, spu/s0 if s0 else 999, spd/s0 if s0 else 999)


    def rooFitPdfAndNorm(self,roofitContext=None):
        if self._rooFit:
            if roofitContext != None and self._rooFit['context'] != roofitContext:
                print "I have to regenerate the RooFit setup as it has changed."
                self._rooFit = None
                self._postFit = None
        if not self._rooFit:
            if not roofitContext: raise RuntimeError("Must provide a valid RooFitContext to create objects")
            self.setupRooFit(roofitContext)
        if "pdf" not in self._rooFit:
            self._makePdfAndNorm()
        return ( self._rooFit["pdf"], self._rooFit["norm"] )
    def setPostFitInfo(self,postFitSetup,applyIt):
        if self._rooFit == None:
            raise RuntimeError, "Can't setPostFitInfo if you don't have a valid roofit setup"
        self._postFit = postFitSetup
        if applyIt: self._doPostFit()
        else:       self._doPreFit()
    def _doPreFit(self):
        self._usePostFit = False
        self.nominal = self.central
        if self._rooFit and self._postFit and self._postFit.fitResult:
            self._rooFit["workspace"].allVars().assignValueOnly(self._postFit.fitResult.floatParsInit())
    def _doPostFit(self):
        self._usePostFit = True
        roofit = self._rooFit["context"]
        roofit.workspace.allVars().assignValueOnly(self._postFit.fitResult.floatParsFinal())
        self.nominal = _cloneNoDir(self.central, "%s_postfit" % self.central.GetName())
        if self.central.Integral() == 0: return
        if "pdf" not in self._rooFit: self._makePdfAndNorm()
        if self._rooFit["norm"].getVal() == 0:
            self.nominal.Reset()
        else:
            roofit.roopdf2hist("_toy", self._rooFit["pdf"], self._rooFit["norm"], target=self.nominal)
        # FIXME this should be improved
        if "TH1" not in self.central.ClassName(): raise RuntimeError("Unsupported for non-TH1")
        for b in xrange(1,self.central.GetNbinsX()+1):
            if self.central.GetBinContent(b) == 0: continue
            self.nominal.SetBinError(b, self.nominal.GetBinContent(b) * self.central.GetBinError(b)/self.central.GetBinContent(b))
    def setupRooFit(self,roofitContext):
        if self._rooFit: 
            if self._rooFit["context"] == roofitContext:
                return
            print "WARNING, discarding already existing RooFit context"
        self._rooFit = { "context":roofitContext, "workspace":roofitContext.workspace }
    def _makePdfAndNorm(self):
        self.cropNegativeBins() # can't do with this
        roofitContext = self._rooFit["context"]
        templates = ROOT.TList()
        nuisances = ROOT.RooArgList()
        templates.Add(roofitContext.hist2roofit(self.central))
        norm0 = self.central.Integral()
        normfactor = ROOT.ProcessNormalization("%s_norm" % self.central.GetName(), "", norm0)
        for var,(hup,hdown) in self.variations.iteritems():
            nuis = roofitContext.workspace.var(var)
            if not nuis: raise RuntimeError("ERROR: can't find nuisance %s needed to parameterize %s" % var, self.central.GetName())
            if self.isShapeVariation(var):
                nuisances.add(nuis)
                templates.Add(roofitContext.hist2roofit(hup))
                templates.Add(roofitContext.hist2roofit(hdown))
            if norm0==0: raise RuntimeError, '%s has zero central normalization'%self.central.GetName()
            if abs(hup.Integral()/norm0-1)>1e-5 or abs(hdown.Integral()/norm0-1)>1e-5:
                kup   = min(max(0.1, hup.Integral()/norm0),   10) # sanitze
                kdown = min(max(0.1, hdown.Integral()/norm0), 10) # sanitze
                normfactor.addAsymmLogNormal(kdown, kup, nuis) 
        pdf = ROOT.FastVerticalInterpHistPdf2("%s_pdf" % self.nominal.GetName(),     "", roofitContext.xvar, templates, nuisances, 1., 1)
        self._rooFit["norm"] = normfactor
        self._rooFit["pdf"] = pdf
        self._rooFit["nuisances"] = nuisances
        self._rooFit["templates"] = templates
        self._rooFit["scaleFactors"] = {}
    def _dropPdfAndNorm(self):
        if self._rooFit:
            for k in "norm", "pdf", "nuisances", "templates", "scaleFactors":
                if k in self._rooFit: del self._rooFit[k]
    def _canAdd(self,x):
        if isinstance(x,SumWithNuisances): return False
        return set(self.rooFitScaleFactors().keys()) == set(x.rooFitScaleFactors().keys())
    def __iadd__(self,x):
        if not self._canAdd(x):
            return SumWithNuisances(self.central.GetName(), [self, x])
        if x.isZero(): return self 
        vars1 = self.variations # writing on self.variations
        vars2 = copy(x.variations)
        for var in set(vars1.keys()+vars2.keys()):
            if var not in vars1: 
                vars1[var] = [_cloneNoDir(self.central),_cloneNoDir(self.central)]
            if var not in vars2: vars2[var] = [x.central,x.central]
        def adder(v1,v2):
            if "TGraph" in v1.ClassName():
                other = ROOT.TList()
                other.Add(v2)
                v1.Merge(other)
            else:
                v1.Add(v2)
        adder(self.central,x.central)
        if self.central != self.nominal:
            adder(self.nominal,x.nominal)
        elif x.central != x.nominal:
            self.nominal = _cloneNoDir(self.central,self.central.GetName())
            adder(self.nominal,x.nominal)
        for var in set(vars1.keys()+vars2.keys()):
            for idx in xrange(2): adder(vars1[var][idx],vars2[var][idx])
        if self._rooFit and "pdf" in self._rooFit and x._rooFit:
            print "Would be good to be able to add roofit objects"
        self._dropPdfAndNorm()
        return self
    def __add__(self,x):
        if not self._canAdd(x):
            return SumWithNuisances(self.central.GetName(), [self, x])
        h = self.Clone(self.GetName())
        h+=x
        return h
    def Add(self,other,scaleFactor=None):
        if scaleFactor is None:
            self += other
        elif self.isSimple() and other.isSimple():
            self.central.Add(other.central, scaleFactor)
        else:
            scaledCopy = other.Clone("tmp")
            scaledCopy.Scale(scaleFactor)
            self += scaledCopy
    def projectionX(self,name,iy1,iy2):
        h = HistoWithNuisances(_projectionXNoDir(self.central,name,iy1,iy2))
        h.central.SetDirectory(None)
        for v,p in self.variations.iteritems():
            h.variations[v] = (_projectionXNoDir(p[0], "%s_%s_up"   % (name,v), iy1,iy2),
                               _projectionXNoDir(p[1], "%s_%s_down" % (name,v), iy1,iy2))
            for hi in h.variations[v]: hi.SetDirectory(None)
        if self.nominal == self.central:
            h.nominal = h.central
        else:
            h.nominal = _projectionXNoDir(self.nominal, name+"_nominal", iy1,iy2)
            h.nominal.SetDirectory(None)
        if self._rooFit: h.setupRooFit(self._rooFit["context"])
        h._postFit = self._postFit
        h._usePostFit = self._usePostFit
        return h
    def writeToFile(self,tfile,writeVariations=True,takeOwnership=True):
        tfile.WriteTObject(self.nominal, self.nominal.GetName())
        for key,vals in self.variations.iteritems():
            tfile.WriteTObject(vals[0], self.GetName()+"_"+key+"Up")
            tfile.WriteTObject(vals[1], self.GetName()+"_"+key+"Down")
        if self.central != self.nominal:
            tfile.WriteTObject(self.central, self.central.GetName())
        if takeOwnership:
            if self.nominal.InheritsFrom("TH1"): 
                self.nominal.SetDirectory(tfile) 
                for vals in self.variations.itervalues():
                    for v in vals: v.SetDirectory(tfile) 
                if self.central != self.nominal:
                    self.central.SetDirectory(tfile) 

def readHistoWithNuisances(tfile, name, variations, mayBeMissing=False):
    central = tfile.Get(name)
    if not central: 
        if mayBeMissing: return None
        raise RuntimeError("Missing %s in %s" % (name, tfile.GetName()))
    ret = HistoWithNuisances(central)
    for var in variations:
        for sign in ("Up", "Down"):
            hvar = tfile.Get(name+"_"+var+sign)
            if not hvar: raise RuntimeError("Missing %s in %s" % (name+"_"+var+sign, tfile.GetName()))
            ret.addVariation(var, sign.lower(), hvar)
    return ret

class SumWithNuisances(HistoWithNuisances):
    def __init__(self,name,histos):
        for h in histos:
            if (not isinstance(h,HistoWithNuisances)) or isinstance(h,SumWithNuisances):
                raise RuntimeError("Can't add %s" % h)
        hsel = [ h for h in histos if h._rooFit ]
        if len(hsel) == 0: raise RuntimeError("Need at least one histogram with roofit to sum")
        hsel += [ h for h in histos if not h._rooFit ]
        # set up histos and variations
        self.central = _cloneNoDir(hsel[0].getCentral(), name)
        self.central.Reset()
        self.variations = {} 
        self._histos = []
        # set up roofit
        roofit = hsel[0]._rooFit["context"]
        self._rooFit = { "context":roofit, "workspace":roofit.workspace }
        self._norms = ROOT.RooArgList()
        self._pdfs  = ROOT.RooArgList()
        self._nuisances = ROOT.RooArgSet()
        self._usePostFit = False # for now, will be reset later
        self._postFit    = None # for now, will be reset later
        self._nodeletes  = []
        # make the sum
        for h in hsel: self._iadd(h)
        # set up post-fit if needed
        hpostfits = [ h for h in histos if h._rooFit and h._postFit ]
        if hpostfits:
            self._postFit = hpostfits[0]._postFit
            self._usePostFit = hpostfits[0]._usePostFit
        self._makeNominal()
    def _makeNominal(self):
        if self._usePostFit: 
            #self._doPostFit()
            self.nominal = _cloneNoDir(self._histos[0].nominal, "%s_postfit" % self.central.GetName())
            for h in self._histos[1:]:
                self.nominal.Add(h.nominal)
        else: 
            self.nominal = self.central
    ## HistoWithNuisance API that we cannot support
    def __getstate__(self): raise RuntimeError("Not supported")
    def __setstate__(self,state): raise RuntimeError("Not supported")
    def printVariations(self): raise RuntimeError("Not supported")
    def Scale(self,x): raise RuntimeError("Not supported")
    def addRooFitScaleFactor(self,roofunc):  raise RuntimeError("Not supported")
    def rooFitScaleFactors(self): raise RuntimeError("Not supported")
    def getVariation(self,alternate): raise RuntimeError("Not supported")
    def addVariation(self,name,sign,histo_varied, clone=True):  raise RuntimeError("Not supported")
    def addBinByBin(self, namePattern="{name}_bbb_{bin}", ycutoff=1e-3, relcutoff=1e-2, verbose=False, norm=False):  raise RuntimeError("Not supported")
    ## HistoWithNuisance API that we could support but we don't
    def Reset(self): raise RuntimeError("Not supported")
    def Clone(self,newname): raise RuntimeError("Not supported")
    def writeToFile(self,tfile,writeVariations=True): raise RuntimeError("Not implemented")
    ## HistoWithNuisance API that we implement differently: variation names
    def hasVariations(self):
        return bool(self.variations) 
    def getVariationList(self):
        return self.variations.keys()
    ## HistoWithNuisance API that we implement differently: rootfit 
    def setPostFitInfo(self,postFitSetup,applyIt):
        if self._rooFit == None:
            raise RuntimeError, "Can't setPostFitInfo if you don't have a valid roofit setup"
        self._postFit = postFitSetup
        if applyIt: self._doPostFit()
        else:       self._doPreFit()
    def setupRooFit(self,roofitContext): 
        if roofitContext != self._rooFit['context']: 
            raise RuntimeError("Not supported")
    def _makePdfAndNorm(self): 
        name = self.central.GetName()
        self._rooFit["pdf"] = ROOT.RooAddPdf(name+"_pdf", name, self._pdfs, self._norms)
        self._rooFit["norm"] = ROOT.RooAddition(name+"_norm", name, self._norms)
    ## HistoWithNuisance API that we implement differently: adding
    def _canAdd(self,x): 
        return True
    def _iadd(self,other):
        hi = other._histos if isinstance(other,SumWithNuisances) else [other]
        for h in hi:
            #if h.isZero(): continue
            self.central.Add(h.getCentral())
            for v in h.getVariationList():
                self.variations[v] = True
            (hpdf,hnorm) = h.rooFitPdfAndNorm(self._rooFit["context"])
            self._pdfs.add(hpdf)
            self._norms.add(hnorm)
            self._nodeletes.append((hpdf,hnorm))
            self._nuisances.add(h._rooFit["nuisances"])
            self._histos.append(h)
    def __iadd__(self,other):
        self._iadd(other)
        self._dropPdfAndNorm()
        self._makeNominal()
        return self
    def __add__(self,x):
        raise RuntimeError("Not supported")
    def Add(self,other,scaleFactor=None): 
        if isinstance(other,HistoWithNuisances) and not isinstance(other,SumWithNuisances):
            if scaleFactor != None:
                other = other.Clone(other.GetName())
                other.Scale(scaleFactor)
            self += other
        else:
            raise RuntimeError("Not supported")
    ## HistoWithNuisance API that we implement differently: uncertainties
    def sumSystUncertainties(self,toadd=None):
        if toadd == []: return [self.nominal,self.nominal]
        if toadd != None: raise RuntimeError("Not implemented")
        hempty = _cloneNoDir(self.central); hempty.Reset(); 
        htotup = _cloneNoDir(hempty, self.nominal.GetName()+'_systUp')
        htotdn = _cloneNoDir(hempty, self.nominal.GetName()+'_systDn')
        if not self._postFit:
            self._postFit = PostFitSetup(params = self._nuisances)
        toys = self._postFit.postFitToys() if self._usePostFit else self._postFit.preFitToys()
        nom_bins = [ self.nominal.GetBinContent(b) for b in xrange(1,self.nominal.GetNbinsX()+1) ]
        sumw2s   = [ 0. for x in nom_bins ]
        wvars    = self._rooFit["workspace"].allVars()
        snap = wvars.snapshot()
        roofit = self._rooFit["context"]
        for i in xrange(toys.numEntries()):
            wvars.assignValueOnly(toys.get(i))
            # calling createHistogram on the RooAddPdf seems to have not understood but bad side-effects.
            # calling it on the individual components and adding them up works, so doing that for now
            hempty.Reset()
            for isub in xrange(self._norms.getSize()):
                spdf  = self._pdfs.at(isub)
                snorm = self._norms.at(isub)
                roofit.roopdf2hist("_toy", spdf, snorm, target=hempty, add=True)
            for ib,x0 in enumerate(nom_bins):
                sumw2s[ib] += (hempty.GetBinContent(ib+1)-x0)**2
        for ib,(x0,xw2) in enumerate(zip(nom_bins,sumw2s)):
            htotup.SetBinContent(ib+1,       x0 + sqrt(xw2/toys.numEntries()))
            htotdn.SetBinContent(ib+1, max(0,x0 - sqrt(xw2/toys.numEntries())))
        wvars.assignValueOnly(snap)
        return [htotup,htotdn]
    def integralSystError(self,toadd=None,relative=False,symmetrize=True,cropAtZero=True):
        i0 = self.raw().Integral()
        if relative and i0 == 0: return 0 if symmetrize else (0,0)
        if toadd == []: return 0 if symmetrize else (0,0)
        if toadd != None or symmetrize != None: raise RuntimeError("Not implemented")
        if "pdf" not in self._rooFit: self._makePdfAndNorm()
        if not self._postFit:
            self._postFit = PostFitSetup(params = self._nuisances)
        toys = self._postFit.postFitToys() if self._usePostFit else self._postFit.preFitToys()
        norm  = self._rooFit["norm"]
        nominal, sumw2 = norm.getVal(), 0.0
        wvars    = self._rooFit["workspace"].allVars()
        snap = wvars.snapshot()
        for i in xrange(toys.numEntries()):
            wvars.assignValueOnly(toys.get(i))
            sumw2 += (norm.getVal()-nominal)**2
        wvars.assignValueOnly(snap)
        #print "postfit swn norm of %-40s: %8.2f +- %5.2f (%.3f)" % (self.central.GetName(), nominal, sqrt(sumw2/toys.numEntries()), sqrt(sumw2/toys.numEntries())/nominal)
        return sqrt(sumw2/toys.numEntries())

def mergePlots(name,plots):
    # check for mergeability
    one = plots[0]
    if isinstance(one, HistoWithNuisances):
        if any(p for p in plots[1:] if not one._canAdd(p)):
            return SumWithNuisances(name,plots)
    one = one.Clone(name)
    if isinstance(one, HistoWithNuisances):
        for p in plots[1:]: one+=p
    elif isinstance(one, ROOT.TH1):
        for p in plots[1:]: one.Add(p)
    elif isinstance(one, ROOT.TGraph):
        others = ROOT.TList()
        for p in plots[1:]: others.Add(p)
        one.Merge(others)
    else: # try blindly and hope it works
        for p in plots[1:]: one+=p
    return one

def listAllNuisances(histWithNuisanceMap):
    return set().union(*(h.getVariationList() for (k,h) in histWithNuisanceMap.iteritems() if k != "data" and h.Integral() >= 0))

def addMyPOIs(context, histoWithNuisanceMap, mca):
    pois = set()
    for p in mca.listBackgrounds(allProcs=True) + mca.listSignals(allProcs=True):
        if p not in histoWithNuisanceMap: continue
        if histoWithNuisanceMap[p].Integral() <= 0: continue
        (pdf,norm) = histoWithNuisanceMap[p].rooFitPdfAndNorm()
        if mca.getProcessOption(p,'FreeFloat',False):
            normTermName = mca.getProcessOption(p,'PegNormToProcess',p)
            print "%s scale as %s" % (p, normTermName)
            poi = context.factory('r_%s[1,%g,%g]' % (normTermName, 0.0, 5))
            norm.addOtherFactor(poi)
            pois.add('r_%s' % normTermName)
    return pois
 
def addExternalDefaultPOI(context,histoWithNuisanceMap,mca,poiName):
    if context.workspace.var(poiName):
        return
    poi = context.workspace.factory("%s[1]" % poiName); context.workspace.nodelete.append(poi)
    poi.setConstant(False)
    poi.removeRange()
    for p in mca.listSignals(allProcs=True):
        if p not in histoWithNuisanceMap: continue
        h = histoWithNuisanceMap[p]
        if h.Integral() > 0:
            h.addRooFitScaleFactor(poi)

def addExternalPhysicsModelPOIs(context,histoWithNuisanceMap,mca,processPegs):
    pois  = set(v for (p,v) in processPegs)
    done = True
    for p in pois:
        if p in ("0","1"): continue
        if not context.workspace.var(p):
            done = False; break
    if done: return
    for poiName in pois:
        if poiName in ("1","0"): continue
        poi = context.workspace.factory("%s[1]" % poiName); context.workspace.nodelete.append(poi)
        poi.removeRange()
        poi.setConstant(False)
    for p in mca.listSignals(allProcs=True)+mca.listBackgrounds(allProcs=True):
        if p not in histoWithNuisanceMap: continue
        h = histoWithNuisanceMap[p]
        if h.Integral() <= 0: continue
        poi = mca.getProcessOption(p,'PegNormToProcess',None)
        if poi == None or poi == "1":
            continue
        elif poi == "0":
            h.Scale(0);
        else:
            h.addRooFitScaleFactor(context.workspace.var(poi))

 
def roofitizeReport(histoWithNuisanceMap, workspace=None, xvarName="x", density=False, context=None):
    # sanity check all inputs, and get one representative histogram
    h0 = None
    for k,h in histoWithNuisanceMap.iteritems():
        if k == "data": continue
        if not isinstance(h, HistoWithNuisances):
            raise RuntimeError("element %s (%s, %s) is not a HistoWithNuisances" % (h, h.GetName() if h else "<nil>"))
        if not str(h.raw().ClassName()).startswith("TH1"): 
            raise RuntimeError("element %s (%s, %s) is not a TH1" % (h, h.GetName() if h else "<nil>", h.ClassName() if h else "<nil>"))
        if h.Integral() <= 0: continue
        if h0 == None: h0 = h
    if h0 == None: raise RuntimeError("Empty report")
    roofit = context
    if context != None:
        if workspace != None and workspace != context.workspace: 
            raise RuntimeError("Mismatch between workspaces")
        workspace = context.workspace
    else:
        # setup the context
        if workspace == None:
            workspace = ROOT.RooWorkspace("w","w")
        if not hasattr(workspace,'nodelete'):
            workspace.nodelete = []
        roofit = RooFitContext(workspace) 
    if not roofit.xvar:
        # create the x variable
        roofit.prepareXVar(h0, density, name=xvarName)
    for nuis in listAllNuisances(histoWithNuisanceMap):
        if not workspace.arg(nuis):
            roofit.factory("%s[0,-7,7]" % nuis)
    # now roofitise all objects
    for k,h in histoWithNuisanceMap.iteritems():
        if k != "data": 
            h.setupRooFit(roofit)
    # and return the context
    return roofit
    
