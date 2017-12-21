#!/usr/bin/env python
from math import sqrt,hypot
from copy import copy
import ROOT

class RooFitContext:
    def __init__(self,workspace):
        self.workspace = workspace
        self.xvar = None
        self._rebin = False
    def prepareXVar(self,histo,density,name="x"):
        self.xname = name
        self._histo = histo.Clone("_template_"); 
        self._histo.SetDirectory(None)
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
        ret = self._xdummy.Clone(histo.GetName()+"_rebin")
        for b in xrange(1,histo.GetNbinsX()):
            scale = histo.GetXaxis().GetBinWidth(b) if self._density else 1.0
            ret.SetBinContent(b, scale * histo.GetBinContent(b))
        return ret
    def roofit2hist(self,histo,norm,target=None):
        """Transform input histogram produced by RooFit via createHistogram to undo what hist2roofit did, and set normalization
           Input histogram may be modified. Output may be the same object as input (but modified), or a new object."""
        if histo.Integral(): 
            histo.Scale(norm/histo.Integral())
        if self._rebin or target != None:
            if target == None:
                target = self._histo.Clone(histo.GetName())
            for b in xrange(1,histo.GetNbinsX()+1):
                scale = 1.0/histo.GetXaxis().GetBinWidth(b) if self._density else 1.0
                target.SetBinContent(b, scale * histo.GetBinContent(b))
            histo = target
        return histo
    def roopdf2hist(self,name,pdf,normobj,target=None):
        """Create a new histogram from a pdf, and normalize it according to a given RooAbsReal.
           If a target histogram is provided, write the output into it with SetBinContent."""
        histo = pdf.createHistogram(name, self.xvar)
        histo.SetDirectory(None)
        return self.roofit2hist(histo,normobj.getVal(),target=target)
            
        
        
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
    def _throwPostFit(self,ntoys):
        obs = ROOT.RooArgSet(self.params).snapshot()
        dtoy = ROOT.RooDataSet("postFitToys","",obs)
        print "Throwing %d toys of %d nuisances" % (ntoys, obs.getSize())
        for i in xrange(ntoys):
            obs.assignValueOnly(self.fitResult.randomizePars())
            dtoy.add(obs)
        self._postFitToys = dtoy

class HistoWithNuisances:
    def __init__(self,histo_central,reset=False):
        if isinstance(histo_central, HistoWithNuisances): raise RuntimeError, "Created with HWN instead of THn or TGraph"
        self.central = histo_central.Clone(histo_central.GetName())
        self.central.SetDirectory(None)
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
        self.central = state['central'].Clone(state['name'])
        self.nominal = state['nominal'].Clone(state['name']+"_nominal") if (state['nominal'] != None) else self.central
        self.central.SetDirectory(None)
        self.nominal.SetDirectory(None)
        self.variations = dict()
        for (x,(v1,v2)) in state['variations']:
            v1c = v1.Clone("%s_%s_up"   % (self.central.GetName(),x)); v1c.SetDirectory(None)
            v2c = v2.Clone("%s_%s_down" % (self.central.GetName(),x)); v2c.SetDirectory(None)
            self.variations[x] = (v1c, v2c)
        self._rooFit  = None
        self._postFit = None
        self._usePostFit = True
    def __getattr__(self,name):
        if name in self.__dict__: return self.__dict__[name]
        return getattr(self.nominal if self._usePostFit else self.central, name)
    def Clone(self,newname):
        h = HistoWithNuisances(self.central)
        self.central.SetName(newname)
        for v,p in self.variations.iteritems():
            h.variations[v]=map(lambda x:x.Clone(), p)
            for hi in h.variations[v]: hi.SetDirectory(None)
        if self.nominal == self.central:
            h.nominal = h.central
        else:
            h.nominal = self.nominal.Clone(newname)
            h.nominal.SetDirectory(None)
        if self._rooFit: h.setupRooFit(self._rooFit["context"])
        h._postFit = self._postFit
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
    def raw(self):
        return self.nominal if self._usePostFit else self.central
    def sumSystUncertainties(self,toadd=None):
        """in each bin, this does max/min of (central,up,down) of each variation and then sums in quadrature upward and downward shifts"""
        if toadd == []: return [self.nominal,self.nominal]
        if self._postFit and self._usePostFit and toadd != None: raise RuntimeError, "Selection of nuisances yet implemented for post-fit"
        if toadd == None: toadd = list(self.variations.keys())
        if "TH" not in self.ClassName(): raise RuntimeError, 'Cannot compute systematic uncertainty for scatter plot'
        hempty = self.central.Clone(''); hempty.Reset();
        htotup = hempty.Clone(self.GetName()+'_systUp')
        htotdn = hempty.Clone(self.GetName()+'_systDn')
        if self._postFit and self._usePostFit:
            if "pdf" not in self._rooFit: self._makePdfAndNorm()
            toys = self._postFit.postFitToys()
            nom_bins = [ self.nominal.GetBinContent(b) for b in xrange(1,self.nominal.GetNbinsX()+1) ]
            sumw2s   = [ 0. for x in nom_bins ]
            #vals     = [ [] for x in nom_bins ]
            wvars    = self._rooFit["workspace"].allVars()
            pdf, norm = self._rooFit["pdf"], self._rooFit["norm"]
            roofit = self._rooFit["context"]
            for i in xrange(toys.numEntries()):
                wvars.assignValueOnly(toys.get(i))
                roofit.roopdf2hist("", pdf, norm, target=hempty)
                for ib,x0 in enumerate(nom_bins):
                    #vals[ib].append(hempty.GetBinContent(ib+1))
                    sumw2s[ib] += (hempty.GetBinContent(ib+1)-x0)**2
            for ib,(x0,xw2) in enumerate(zip(nom_bins,sumw2s)):
                htotup.SetBinContent(ib+1,       x0 + sqrt(xw2/toys.numEntries()))
                htotdn.SetBinContent(ib+1, max(0,x0 - sqrt(xw2/toys.numEntries())))
        else:
            hvars={}
            # compute up envelope and down envelope for all variations
            for var in toadd:
                hvarup = hempty.Clone('')
                hvardn = hempty.Clone('')
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
        if relative and i0 == 0: return (0,0) if symmetrize else 0
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
        h = self.raw()
        hup, hdn = self.sumSystUncertainties(toadd)
        xaxis = h.GetXaxis()
        points = []; errors = []
        for i in xrange(h.GetNbinsX()):
            N = h.GetBinContent(i+1);
            dN = h.GetBinError(i+1)
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

    def getCentral(self):
        return self.central
    def getVariation(self,alternate):
        return self.variations[alternate]
    def hasVariations(self):
        return bool(self.variations) 
    def getVariationList(self):
        return self.variations.keys()
    def addVariation(self,name,sign,histo_varied):
        idx = 0 if sign=='up' else 1
        if name not in self.variations: self.variations[name] = [None,None]
        self.variations[name][idx] = histo_varied.Clone('')
        self.variations[name][idx].SetDirectory(None)
        # invalidate caches
        if self._rooFit or self._postFit:
            print "WARNING: adding a variantion on an object that already has roofit/postfit info"
            self._rooFit  = None
            self._postFit = None
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
        if self._rooFit and self._postFit:
            self._rooFit["workspace"].allVars().assignValueOnly(self._postFit.fitResult.floatParsInit())
    def _doPostFit(self):
        self._usePostFit = True
        roofit = self._rooFit["context"]
        roofit.workspace.allVars().assignValueOnly(self._postFit.fitResult.floatParsFinal())
        self.nominal = self.central.Clone("%s_postfit" % self.central.GetName())
        if self.central.Integral() == 0: return
        if "pdf" not in self._rooFit: self._makePdfAndNorm()
        roofit.roopdf2hist("", self._rooFit["pdf"], self._rooFit["norm"], target=self.nominal)
        # FIXME this should be improved
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
        roofitContext = self._rooFit["context"]
        templates = ROOT.TList()
        nuisances = ROOT.RooArgList()
        templates.Add(roofitContext.hist2roofit(self.central))
        norm0 = self.central.Integral()
        normfactor = ROOT.ProcessNormalization("%s_norm" % self.central.GetName(), "", norm0)
        for var,(hup,hdown) in self.variations.iteritems():
            nuis = roofitContext.workspace.var(var)
            if not nuis: raise RuntimeError("ERROR: can't find nuisance %s needed to parameterize %s" % var, self.central.GetName())
            nuisances.add(nuis)
            templates.Add(roofitContext.hist2roofit(hup))
            templates.Add(roofitContext.hist2roofit(hdown))
            normfactor.addAsymmLogNormal(hdown.Integral()/norm0, hup.Integral()/norm0, nuis) 
        pdf = ROOT.FastVerticalInterpHistPdf2("%s_pdf" % self.nominal.GetName(),     "", roofitContext.xvar, templates, nuisances, 1., 1)
        self._rooFit["norm"] = normfactor
        self._rooFit["pdf"] = pdf
        self._rooFit["nuisances"] = nuisances
        self._rooFit["templates"] = templates
    def _dropPdfAndNorm(self):
        if self._rooFit:
            for k in "norm", "pdf", "nuisances", "templates":
                if k in self._rooFit: del self._rooFit[k]
    def __iadd__(self,x):
        vars1 = self.variations # writing on self.variations
        vars2 = copy(x.variations)
        for var in set(vars1.keys()+vars2.keys()):
            if var not in vars1: vars1[var] = [self.central.Clone(''),self.central.Clone('')]
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
            self.nominal = self.central.Clone(self.central.GetName())
            adder(self.nominal,x.nominal)
        for var in set(vars1.keys()+vars2.keys()):
            for idx in xrange(2): adder(vars1[var][idx],vars2[var][idx])
        if self._rooFit and "pdf" in self._rooFit and x._rooFit:
            print "Would be good to be able to add roofit objects"
        self._dropPdfAndNorm()
        return self
    def __add__(self,x):
        h = self.Clone(self.GetName())
        h+=x
        return h
    def writeToFile(self,tfile,writeVariations=True):
        tfile.WriteTObject(self.nominal, self.nominal.GetName())
        for key,vals in self.variations.iteritems():
            tfile.WriteTObject(vals[0], self.GetName()+"_"+key+"Up")
            tfile.WriteTObject(vals[1], self.GetName()+"_"+key+"Down")
        if self.central != self.nominal:
            tfile.WriteTObject(self.central, self.central.GetName())
        if self.nominal.InheritsFrom("TH1"): 
            self.nominal.SetDirectory(tfile) 
            for vals in self.variations.itervalues():
                for v in vals: v.SetDirectory(tfile) 
            if self.central != self.nominal:
                self.central.SetDirectory(tfile) 

def mergePlots(name,plots):
    one = plots[0].Clone(name)
    for p in plots[1:]:
        one+=p
    return one

def listAllNuisances(histWithNuisanceMap):
    return set().union(*(h.getVariationList() for (k,h) in histWithNuisanceMap.iteritems() if k != "data" and h.Integral() >= 0))

def addDefaultPOI(context,histoWithNuisanceMap,mca,poiName):
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

def addPhysicsModelPOIs(context,histoWithNuisanceMap,mca,processPegs):
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

 
def roofitizeReport(histoWithNuisanceMap, workspace=None, xvarName="x", density=False):
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
    # setup the context
    if workspace == None:
        workspace = ROOT.RooWorkspace("w","w"); workspace.nodelete = []
        for nuis in listAllNuisances(histoWithNuisanceMap):
            workspace.nodelete.append(workspace.factory("%s[0,-7,7]" % nuis))
    roofit = RooFitContext(workspace) 
    # create the x variable
    roofit.prepareXVar(h0, density, name=xvarName)
    # now roofitise all objects
    for k,h in histoWithNuisanceMap.iteritems():
        if k != "data": 
            h.setupRooFit(roofit)
    # and return the context
    return roofit
    
