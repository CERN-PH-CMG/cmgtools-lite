import ROOT, os, sys, re, array, math

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
    
    def graphStyle(self, graph, style=20, color=ROOT.kOrange+7, size=1.0, titleY='-2 #Delta ln L', rangeY=(-0.01,4.0) ):
        graph.SetMarkerStyle(style)
        graph.SetMarkerColor(color)
        graph.SetLineWidth  (2)
        graph.SetMarkerSize(size)
        graph.GetYaxis().SetTitle(titleY)
        if rangeY:
            graph.GetYaxis().SetRangeUser(rangeY[0], rangeY[1])
    
    
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
        return histos

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



