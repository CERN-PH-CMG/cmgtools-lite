import ROOT, os, sys, re, array, math, json

class util:


    def solvePol2(self, a,b,c):
    
        # calculate the discriminant
        d = (b**2) - (4*a*c)
    
        if not a or d < 0:
            return (0,0,0)
        
        # find two solutions
        sol1 = (-b-math.sqrt(d))/(2*a)
        sol2 = (-b+math.sqrt(d))/(2*a)
    
        bestfit = -1.*b/(2.*a)
    
        return (bestfit, sol1, sol2)
    
    def graphStyle(self, graph):
        graph.SetMarkerStyle(20)
        graph.SetMarkerColor(ROOT.kOrange+7)
        graph.SetLineWidth  (2)
        graph.SetMarkerSize(1.0)
        graph.GetYaxis().SetTitle('-2 #Delta ln L')
        graph.GetYaxis().SetRangeUser(-0.01, 4.0)
    
    
    def getGraph(self, infile, par, norm, treename='limit'):
        f = ROOT.TFile(infile,'read')
        tree = f.Get(treename)
        vals = []
        normval = norm if norm else 1.
        for ev in tree:
            vals.append( [getattr(ev, par)/normval, 2.*ev.deltaNLL] )
        vals = sorted(vals)
        graph = ROOT.TGraph(len(vals), array.array('d', [x[0] for x in vals]), array.array('d', [y[1] for y in vals]) )
        self.graphStyle(graph)
        graph.GetXaxis().SetTitle(par)
        graph.SetTitle('scan for '+par)
        return graph

    def getErrorFromGraph(self, graph):
        graph.Fit('pol2')
        tmp_fit = graph.GetFunction('pol2')
        (best, sol1, sol2) = self.solvePol2(tmp_fit.GetParameter(2), tmp_fit.GetParameter(1), tmp_fit.GetParameter(0)-1)
        return (best, sol1, sol2)

    def getRebinned(self, ybins, charge, infile, ip):
        histo_file = ROOT.TFile(infile, 'READ')
    
        pstr = 'central' if not ip else 'pdf{ip}'.format(ip=ip)
    
        histos = {}
        for pol in ['left','right','long']:
            cp = '{ch}_{pol}'.format(ch=charge,pol=pol if not pol == 'long' else 'right')
    
            keys = histo_file.GetListOfKeys()
            for k in keys:
                if 'w{ch}'.format(ch=charge) in k.GetName() and pol in k.GetName() and pstr in k.GetName():
                    name = k.GetName()
            histo = histo_file.Get(name)# 'w{ch}_wy_W{ch}_{pol}'.format(ch=charge, pol=pol))
            conts = []
            for iv, val in enumerate(ybins[cp][:-1]):
                err = ROOT.Double()
                istart = histo.FindBin(val)
                iend   = histo.FindBin(ybins[cp][iv+1])
                val = histo.IntegralAndError(istart, iend-1, err) ## do not include next bin
                conts.append(float(int(val)))
            histos[pol] = conts
        histo_file.Close()
        return histos

    def getXSecFromShapes(self, ybins, charge, infile, channel, ip):
        values = {}
        if not infile:
            for pol in ['left','right']: #,'long']: 
                cp = '{ch}_{pol}'.format(ch=charge,pol=pol if not pol == 'long' else 'right')
                xsecs = []
                for iv in xrange(len(ybins[cp][:-1])):
                    xsecs.append(0.)
                values[pol] = xsecs
            return values

        histo_file = ROOT.TFile(infile, 'READ')
    
        pstr = '' if not ip else '_pdf{ip}Up'.format(ip=ip)
    
        for pol in ['left','right']: #,'long']
            cp = '{ch}_{pol}'.format(ch=charge,pol=pol if not pol == 'long' else 'right')
            xsecs = []
            for iv, val in enumerate(ybins[cp][:-1]):
                name = 'x_W{ch}_{pol}_W{ch}_{pol}_{channel}_Ybin_{iy}{suffix}'.format(ch=charge,pol=pol,channel=channel,iy=iv,ip=ip,suffix=pstr)
                histo = histo_file.Get(name)
                val = histo.Integral()
                xsecs.append(float(val))
            values[pol] = xsecs
        histo_file.Close()
        return values

    def getParametersFromWS(self, ws, regexp):

        ## get all the nuisance parameters from the workspace
        pars = ws.allVars()
        pars = ROOT.RooArgList(pars)
        ## this has to be a loop over a range... doesn't work otherwise
        parameters = []
        all_parameters = []
        pois_regexps = list(regexp.split(','))
        ## get the parameters to scan from the list of allVars and match them
        ## to the given regexp
        for i in range(len(pars)):
            tmp_name = pars[i].GetName()
            if '_In' in tmp_name: ## those are the input parameters
                continue
            if tmp_name in ['CMS_th1x', 'r']: ## don't want those
                continue
            all_parameters.append(tmp_name)
            for poi in pois_regexps:
                if re.match(poi, tmp_name):
                    parameters.append(pars[i].GetName())

        return parameters

    def translateWStoTF(self, pname):
        if not 'r_' in pname:
            return pname
     
        if 'Wplus' in pname or 'Wminus' in pname:
            pnew = pname.replace('r_','')
            pnew = pnew.split('_')
            pnew.insert(-2, 'mu' )#if 'Wmu' in options.tensorflow else 'el')
            pnew = '_'.join(pnew)
            return pnew
     
        return -1


    def getFromToys(self, infile):
        _dict = {}
        
        f = ROOT.TFile(infile, 'read')
        tree = f.Get('fitresults')
        lok  = tree.GetListOfLeaves()
        
        for p in lok:
            if '_err'   in p.GetName(): continue
            if '_minos' in p.GetName(): continue
            if '_gen'   in p.GetName(): continue
            if '_In'    in p.GetName(): continue
            
            tmp_hist = ROOT.TH1F(p.GetName(),p.GetName(), 100000, -5000., 5000.)
            tree.Draw(p.GetName()+'>>'+p.GetName())
            mean = tmp_hist.GetMean()
            err  = tmp_hist.GetRMS()
            _dict[p.GetName()] = (mean, mean+err, mean-err)
     
        return _dict

    def getHistosFromToys(self, infile):
        _dict = {}
        
        f = ROOT.TFile(infile, 'read')
        tree = f.Get('fitresults')
        lok  = tree.GetListOfLeaves()
        
        for p in lok:
            if '_err'   in p.GetName(): continue
            if '_minos' in p.GetName(): continue
            if '_gen'   in p.GetName(): continue
            if '_In'    in p.GetName(): continue
            
            tmp_hist = ROOT.TH1F(p.GetName(),p.GetName(), 100, -3., 3.)
            tree.Draw(p.GetName()+'>>'+p.GetName())
            mean = tmp_hist.GetMean()
            err  = tmp_hist.GetRMS()
            tmp_hist.SetDirectory(None)
            _dict[p.GetName()] = (mean, mean+err, mean-err, tmp_hist)
     
        return _dict


    def getExprFromToys(self, name, expression, infile):
        f = ROOT.TFile(infile, 'read')
        tree = f.Get('fitresults')        
        tmp_hist = ROOT.TH1F(name,name, 100000, -100., 5000.)
        tree.Draw(expression+'>>'+name)
        mean = tmp_hist.GetMean()
        err  = tmp_hist.GetRMS()
        return (mean, mean+err, mean-err)


    def getNormalizedXsecFromToys(self, ybins, charge, pol, channel, iy, infile, absYmax=6.0):
        cp = '{ch}_{pol}'.format(ch=charge,pol=pol)
        ybins_expr = []
        for iv, val in enumerate(ybins[cp][:-1]):
            if abs(val)<absYmax:
                ybins_expr.append('W{charge}_{pol}_W{charge}_{pol}_{ch}_Ybin_{iy}_pmaskedexp'.format(charge=charge,pol=pol,ch=channel,iy=iv))
        num = 'W{charge}_{pol}_W{charge}_{pol}_{ch}_Ybin_{iy}_pmaskedexp'.format(charge=charge,pol=pol,ch=channel,iy=iy)
        den = '('+'+'.join(ybins_expr)+')'        
        ret = self.getExprFromToys(charge+pol+channel+str(iy),'{num}/{den}'.format(num=num,den=den),infile)
        return ret

    def getFromScans(self, indir):
        _dict = {}
        
        for sd in os.listdir(indir):
     
            if 'jobs' in sd: continue
     
            par = self.translateWStoTF(sd) ## parameter name different than in TF
            f = ROOT.TFile(indir+'/'+sd+'/scan_'+sd+'.root', 'read')
            tree = f.Get('fitresults')
     
            vals = []
            for ev in tree:
                vals.append( [getattr(ev, par), 2.*ev.nllval  ] )
            vals = sorted(vals)
            lvals = vals[:len(vals)/2]
            rvals = vals[len(vals)/2:]
     
            graph = ROOT.TGraph(len(vals), array.array('d', [x[1] for x in vals]), array.array('d', [y[0] for y in vals]) )
     
            best = graph.Eval(0.)
            lgraph = ROOT.TGraph(len(lvals), array.array('d', [x[1] for x in lvals]), array.array('d', [y[0] for y in lvals]) )
            rgraph = ROOT.TGraph(len(rvals), array.array('d', [x[1] for x in rvals]), array.array('d', [y[0] for y in rvals]) )
            sol1  = lgraph.Eval(1.)
            sol2  = rgraph.Eval(1.)
     
            _dict[par] = (best, sol1, sol2)
     
        return _dict


    def effSigma(self, histo):
        xaxis = histo.GetXaxis()
        nb = xaxis.GetNbins()
        xmin = xaxis.GetXmin()
        ave = histo.GetMean()
        rms = histo.GetRMS()
        total=histo.Integral()
        if total < 100: 
            print "effsigma: Too few entries to compute it: ", total
            return 0.
        ierr=0
        ismin=999
        rlim=0.683*total
        bwid = xaxis.GetBinWidth(1)
        nrms=int(rms/bwid)
        if nrms > nb/10: nrms=int(nb/10) # Could be tuned...
        widmin=9999999.
        for iscan in xrange(-nrms,nrms+1): # // Scan window centre 
            ibm=int((ave-xmin)/bwid)+1+iscan
            x=(ibm-0.5)*bwid+xmin
            xj=x; xk=x;
            jbm=ibm; kbm=ibm;
            bin=histo.GetBinContent(ibm)
            total=bin
            for j in xrange(1,nb):
                if jbm < nb:
                    jbm += 1
                    xj += bwid
                    bin=histo.GetBinContent(jbm)
                    total += bin
                    if total > rlim: break
                else: ierr=1
                if kbm > 0:
                    kbm -= 1
                    xk -= bwid
                    bin=histo.GetBinContent(kbm)
                    total+=bin
                if total > rlim: break
                else: ierr=1
            dxf=(total-rlim)*bwid/bin
            wid=(xj-xk+bwid-dxf)*0.5
            if wid < widmin:
                widmin=wid
                ismin=iscan
        if ismin == nrms or ismin == -nrms: ierr=3
        if ierr != 0: print "effsigma: Error of type ", ierr
        return widmin
