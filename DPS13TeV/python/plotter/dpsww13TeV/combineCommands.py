import ROOT, os, subprocess, sys, optparse
from array import array

def runAll():
    if not opts.onlyMuMu:
        cmd_combineCards = 'combineCards.py mumuplusplus=mumuplusplus.card.txt mumuminusminus=mumuminusminus.card.txt  elmuplusplus=elmuplusplus.card.txt elmuminusminus=elmuminusminus.card.txt'
        outcard_file = 'elmumumuAllCharges.card.txt'
    else:
        cmd_combineCards = 'combineCards.py mumuplusplus=mumuplusplus.card.txt mumuminusminus=mumuminusminus.card.txt '
        outcard_file = 'mumuAllCharges.card.txt'
    f = open(outcard_file, 'w')
    subprocess.call(cmd_combineCards.split(), stdout=f)

    additional_opt = ''
    if opts.scaleHL:
        print 'SCALING TO THE HL LHC LUMINOSITY!!!!!!'
        print '========================================================='
        with open(outcard_file,'a') as file:
            file.write('lumiscale rateParam * * 1\n')
            file.write('nuisance edit freeze lumiscale\n')
        file.close()
        lumi_scale = (3000./35.9)*1.15
        additional_opt += ' --setPhysicsModelParameters lumiscale={scale:.2f} '.format(scale=lumi_scale)

    
    r = 0.87/1.64
    
    print('RUNNING EXPECTED AND OBSERVED LIMIT')
    print('========================================')
    ## expected and observed limit
    if opts.runObs:
        cmd_limitObs = 'combine -M Asymptotic {card}'.format(card=outcard_file)+additional_opt
    else:
        cmd_limitObs = 'combine -M Asymptotic -t -1 {card}'.format(card=outcard_file)+additional_opt
    print('command: {cmd}'.format(cmd=cmd_limitObs))
    subprocess.call(cmd_limitObs.split())
    
    print('RUNNING EXPECTED SIGNIFICANCE')
    print('================================================')
    ## for the expected significance in the presence of signal
    cmd_significanceExp = 'combine -M ProfileLikelihood --signif -t -1 --expectSignal=1 {card}'.format(card=outcard_file)+additional_opt
    print('command: {cmd}'.format(cmd=cmd_significanceExp))
    subprocess.call(cmd_significanceExp.split())
    
    print('RUNNING EXPECTED SIGNIFICANCE FOR FACTORIZED APPROACH')
    print('================================================')
    ## for the expected significance in the presence of signal
    cmd_significanceExp = 'combine -M ProfileLikelihood --signif -t -1 --expectSignal={r} {card}'.format(r=r,card=outcard_file)+additional_opt
    print('command: {cmd}'.format(cmd=cmd_significanceExp))
    subprocess.call(cmd_significanceExp.split())
    
    print('RUNNING OBSERVED SIGNIFICANCE')
    print('================================================')
    ## for the expected significance in the presence of signal
    if opts.runObs:
        cmd_significanceObs = 'combine -M ProfileLikelihood --signif             --expectSignal=1 {card}'.format(card=outcard_file)+additional_opt
        print('command: {cmd}'.format(cmd=cmd_significanceObs))
        subprocess.call(cmd_significanceObs.split())
    
    print('RUNNING EXPECTED AND OBSERVED UNCERTAINTY ON THE SIGNAL STRENGTH')
    print('====================================================================')
    ## expected uncertainty on the signal strength
    cmd_sigUnc = 'combine -M MaxLikelihoodFit --justFit -t -1  --expectSignal=1 {card} --saveShapes --saveWithUncertainties '.format(card=outcard_file)+additional_opt ##--setPhysicsModelParameters lumiscale=1'
    ## observed uncertainty on the signal strength
    if opts.runObs:
        cmd_sigUnc = 'combine -M MaxLikelihoodFit --justFit --expectSignal=1 {card} --saveShapes --saveWithUncertainties '.format(card=outcard_file)+additional_opt ##--setPhysicsModelParameters lumiscale=1'
        subprocess.call(cmd_sigUnc.split())
        cmd_sigUnc2= 'combine -M MaxLikelihoodFit           --expectSignal=1 {card} --saveShapes --saveWithUncertainties '.format(card=outcard_file)+additional_opt ##--setPhysicsModelParameters lumiscale=1'
        print('command: {cmd}'.format(cmd=cmd_sigUnc2))
        subprocess.call(cmd_sigUnc2.split())
    
    print('RUNNING ANALYSIS OF THE PREFIT AND POSTFIT UNCERTAINTIES')
    print('====================================================================')
    ## do analysis of prefit and postfit uncertainty constraints
    cmd_pulls = 'python {base}/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py mlfit.root -a  -g pulls.root'.format(base=os.environ['CMSSW_BASE']) ## -f = "latex"
    print('command: {cmd}'.format(cmd=cmd_pulls))
    subprocess.call(cmd_pulls.split())

def graphStyle(graph, mode):
    markerstyle = 20    if mode == 'obs' else 21          if mode == 'pyt' else 22
    color = ROOT.kBlack if mode == 'obs' else ROOT.kRed-4 if mode == 'pyt' else ROOT.kGreen+2
    style = 1 if mode == 'obs' else 2
    graph.SetMarkerStyle(markerstyle)
    graph.SetMarkerColor(color)
    graph.SetLineColor  (color)
    graph.SetLineWidth  (2)
    graph.SetLineStyle  (style)
    graph.SetMarkerSize(0.8)
    graph.GetXaxis().SetTitle('#sigma_{DPS} (pb)')
    graph.GetYaxis().SetTitle('-2 #Delta ln L')
    ##graph.GetYaxis().SetRangeUser(0.0, 1.5)
    ##graph.GetXaxis().SetRangeUser(0.0, 2.5)
    return graph


def getGraph(tree, mode = 'obs'):
    if mode == 'obs': xsec = 1.64
    if mode == 'pyt': xsec = 1.64
    if mode == 'fac': xsec = 1.64#0.87
    n = tree.Draw('2*deltaNLL:(r*{xs})'.format(xs=xsec), '', 'goff')
    vals = []
    minXsec = -999.
    for ev in tree:
        vals.append( [ev.r*xsec, (2.*ev.deltaNLL)] )
        if 2.*ev.deltaNLL == 0.:
            minXsec = ev.r*xsec
    vals = sorted(vals)
    graph = ROOT.TGraph(len(vals), array('d', [x[0] for x in vals]), array('d', [y[1] for y in vals]) )
    graph = graphStyle(graph, mode)
    graph_alt = ROOT.TGraph(len(vals), array('d', [y[1] for y in vals]), array('d', [x[0] for x in vals]) )
    err  = graph_alt.Eval(1.)
    return graph, minXsec


def makeScans(n = 100):

    if opts.recalculateLimits:
        txt2ws = 'text2workspace.py elmumumuAllCharges.card.txt'
        subprocess.call(txt2ws.split())
        r = 0.87/1.64

        cmd_scanObs  = 'combine -M MultiDimFit elmumumuAllCharges.card.root --algo=grid --points={n} --setPhysicsModelParameterRanges r=0.,2.                          -m 120'.format(n=n)
        cmd_scanExp1 = 'combine -M MultiDimFit elmumumuAllCharges.card.root --algo=grid --points={n} --setPhysicsModelParameterRanges r=0.,2. -t -1 --expectSignal=1   -m 119'.format(n=n)
        cmd_scanExp2 = 'combine -M MultiDimFit elmumumuAllCharges.card.root --algo=grid --points={n} --setPhysicsModelParameterRanges r=0.,2. -t -1 --expectSignal={r} -m 118'.format(n=n, r=r)
        
        subprocess.call(cmd_scanObs .split())
        subprocess.call(cmd_scanExp1.split())
        subprocess.call(cmd_scanExp2.split())

    f_obs = ROOT.TFile('higgsCombineTest.MultiDimFit.mH120.root', 'READ'); l_obs = f_obs.Get('limit')
    f_ex1 = ROOT.TFile('higgsCombineTest.MultiDimFit.mH119.root', 'READ'); l_ex1 = f_ex1.Get('limit')
    f_ex2 = ROOT.TFile('higgsCombineTest.MultiDimFit.mH118.root', 'READ'); l_ex2 = f_ex2.Get('limit')
    
    (g_obs, xsec_obs) = getGraph(l_obs, 'obs')
    (g_ex1, xsec_ex1) = getGraph(l_ex1, 'pyt')
    (g_ex2, xsec_ex2) = getGraph(l_ex2, 'fac')

    canv = ROOT.TCanvas('foo', 'bar', 600, 600)
    canv.cd()
    xmax = 2.5
    dummy = ROOT.TH1F('foo', 'Likelihood scan of #sigma_{DPS}', 100, 0., xmax)
    dummy.GetYaxis().SetRangeUser(0., 4.5)
    dummy.GetXaxis().SetTitle(g_obs.GetXaxis().GetTitle())
    dummy.GetYaxis().SetTitle(g_obs.GetYaxis().GetTitle())
    dummy.GetXaxis().SetRangeUser(0., xmax)
    dummy.GetYaxis().SetNdivisions(505)
    dummy.GetXaxis().SetNdivisions(510)
    dummy.GetYaxis().SetTitleOffset(1.2)

    ROOT.gStyle.SetOptStat(0)
    dummy.Draw('AXIS')

    mg = ROOT.TMultiGraph()
    mg.Add(g_obs)
    mg.Add(g_ex1)
    mg.Add(g_ex2)
    mg.Draw('l')
    #mg.GetYaxis().SetRangeUser(0., 4.5)
    #mg.GetXaxis().SetTitle(g_obs.GetXaxis().GetTitle())
    #mg.GetYaxis().SetTitle(g_obs.GetYaxis().GetTitle())
    #mg.GetXaxis().SetRangeUser(0., xmax)
    #mg.GetYaxis().SetNdivisions(505)
    #mg.GetXaxis().SetNdivisions(510)
    #mg.GetYaxis().SetTitleOffset(1.2)


    line = ROOT.TLine()
    line.SetLineStyle(7)
    line.SetLineWidth(2)
    line.SetLineColor(ROOT.kGray+2)
    line.DrawLine(0., 1., xmax, 1.)
    line.SetLineStyle(4)
    line.SetLineColor(ROOT.kGray+1)
    line.DrawLine(0., 3.84, xmax, 3.84)

    leg = ROOT.TLegend(0.5, 0.5, 0.85, 0.70)
    leg.SetTextSize(0.03)
    leg.AddEntry(g_obs, 'observed'           , 'l')
    leg.AddEntry(g_ex1, 'expected pythia8'   , 'l')
    leg.AddEntry(g_ex2, '#splitline{expected factorized}{(#sigma_{eff} = 20.7 mb)}', 'l')
    leg.SetLineColor(ROOT.kWhite)
    leg.Draw('same')

    lat = ROOT.TLatex()
    lat.SetNDC()
    lat.SetTextAlign(31)
    lat.SetTextSize(0.025)
    lat.SetTextColor(ROOT.kGray+2)
    lat.DrawLatex(0.87, 0.28, '1 #sigma')
    lat.SetTextColor(ROOT.kGray+1)
    lat.DrawLatex(0.87, 0.79, '95% CL')
    lat.SetTextColor(ROOT.kBlack)
    lat.SetTextSize(0.04)
    lat.DrawLatex(0.68, 0.92, 'Likelihood scan of #sigma_{DPS}')

    tarr = ROOT.TArrow(0.43, 0.25, 0.43, 0.15, 0.03, ">")
    #tarr.SetNDC()
    tarr.SetLineWidth(2)
    lat.SetTextAlign(22)
    lat.SetTextFont(42)
    lat.SetTextSize(0.031)
    arry1, arry2 = -0.35, -0.05 #0.12, 0.30
    laty = 0.02

    tarr.SetLineColor(ROOT.kBlack)
    tarr.DrawArrow(xsec_obs, arry1, xsec_obs, arry2)
    lat .DrawLatex(0.45, laty, '{obs:.2f}'.format(obs=xsec_obs))

    tarr.SetLineColor(ROOT.kRed-4)
    lat .SetTextColor(ROOT.kRed-4)
    tarr.DrawArrow(xsec_ex1, arry1, xsec_ex1, arry2)
    lat .DrawLatex(0.62, laty, '{obs:.2f}'.format(obs=xsec_ex1))

    tarr.SetLineColor(ROOT.kGreen+2)
    lat .SetTextColor(ROOT.kGreen+2)
    tarr.DrawArrow(xsec_ex2, arry1, xsec_ex2, arry2)
    lat .DrawLatex(0.38, laty, '{obs:.2f}'.format(obs=xsec_ex2))
    

    ## canv.SaveAs('/afs/cern.ch/user/m/mdunser/www/private/dps-ww-2017/results/2017-03-01-unblinded_35p9invfb/likelihood_scan.pdf')
    ## canv.SaveAs('/afs/cern.ch/user/m/mdunser/www/private/dps-ww-2017/results/2017-03-01-unblinded_35p9invfb/likelihood_scan.png')
    canv.SaveAs('/afs/cern.ch/user/m/mdunser/www/private/dps-ww-2017/results/2017-06-26-flipsNuisance_correlated_newLumiUnc_final/likelihood_scan.pdf')
    canv.SaveAs('/afs/cern.ch/user/m/mdunser/www/private/dps-ww-2017/results/2017-06-26-flipsNuisance_correlated_newLumiUnc_final/likelihood_scan.png')


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--makeScans', '--scans',  action='store_true', dest='makeScans'        , default=False, help='make likelihood scans')
    parser.add_option('--runAll'   , '--all'  ,  action='store_true', dest='runAll'           , default=False, help='run all combine commands. including combineCards')
    parser.add_option('--mumu'     ,             action='store_true', dest='onlyMuMu'         , default=False, help='run the combination for only mumu')
    parser.add_option('--recalc'   ,             action='store_true', dest='recalculateLimits', default=False, help='recalculate the limits for the likelihood scan')
    parser.add_option('--scaleHL'  ,             action='store_true', dest='scaleHL'          , default=False, help='scale to the HL LHC lumi of 3000 fb-1')
    parser.add_option('--runObserved',           action='store_true', dest='runObs'           , default=False, help='run also the observed limit and significances')
    global opts
    (opts, args) = parser.parse_args()


    if opts.makeScans:
        makeScans()
    if opts.runAll:
        runAll()
