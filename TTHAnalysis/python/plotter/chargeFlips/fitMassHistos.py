#!/usr/bin/env python
import sys, os, pickle, math
import os.path as osp
import ROOT

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def getErr(m1, m2, e1, e2):
    err = math.pow(e1/m1,2) + math.pow(e2/m2,2)
    if m1==0: return 1.
    return (m1/m2)*math.sqrt(err)

def getRatio(m1, m2, e1, e2):
    try:
        return m1/m2, getErr(m1,m2,e1,e2)
    except ZeroDivisionError:
        return 0.0, 1.0

def shushRooFit():
    "Make RooFit shut up"
    msgSI = ROOT.RooMsgService.instance()
    msgSI.setSilentMode(True)
    for s in [0,1]:
        for t in ['Eval',
                  'NumIntegration',
                  'DataHandling',
                  'ObjectHandling',
                  'Minimization',
                  'Fitting',
                  'Plotting',
                  'InputArguments',
                  'Caching']:
            msgSI.getStream(s).removeTopic(getattr(ROOT.RooFit,t))

def putPHPIndex(odir):
    LOC = '/afs/cern.ch/user/s/stiegerb/www/ttH/index.php'
    try:
        os.symlink(LOC, os.path.join(odir,'index.php'))
    except OSError, e:
        if e.errno == 17:  # 'File exists'
            pass

def shapeCBBreitWigner(ws):
    ws.factory("RooBreitWigner::bw(mass, mZ0[91.188], gammaZ0[2.4952])")
    ws.factory("RooCBShape::cb_pdf(mass, cbb[0.07, -3.00, 3.0]," # bias
                                        "cbw[1.00,  0.00, 5.0]," # width
                                        "cba[1.20,  0.03, 4.0]," # alpha
                                        "cbn[5])")               # power

    ws.factory("RooFFTConvPdf::sig(mass, bw, cb_pdf)")

def shapeExpBackgr(ws):
    ws.factory("RooExponential::bg(mass,tau[-0.05,-40.,-0.01])")

def shapeRooCMSShape(ws):
    ws.factory("RooCMSShape::bg(mass, alpha[40.,20.,160.], "
                                     "beta[ 0.050, 0., 2.0], "
                                     "gamma[0.020, 0., 0.1], "
                                     "peak[91.2])")

def getNSignalEvents(histo, dofit=True, odir='massfits/'):
    if not dofit:
        # Return cut&count values
        binlo = histo.GetXaxis().FindBin(81.)
        binhi = histo.GetXaxis().FindBin(101.)
        err = ROOT.Double(0.0)
        nev = histo.IntegralAndError(binlo,binhi,err)
        return nev,err

    os.system('mkdir -p %s'%odir)

    ROOT.gROOT.SetBatch(1)
    shushRooFit()

    ws = ROOT.RooWorkspace()
    mass = ws.factory('mass[70,110]')
    data = ROOT.RooDataHist(histo.GetName(),
                            histo.GetTitle(),
                            ROOT.RooArgList(mass),
                            histo)
    getattr(ws,'import')(data)

    # Define the pdfs:
    shapeCBBreitWigner(ws)
    shapeRooCMSShape(ws)
    # shapeExpBackgr(ws)

    # Define the fit model:
    nev = histo.Integral()
    nsig  = ws.factory('nsig[%.1f,%.1f,%.0f]'%(0.9*nev,0.2*nev,1.5*nev))
    nbkg  = ws.factory('nbkg[%.1f,0,%.0f]'%(0.1*nev,1.5*nev))
    shape = ws.factory('SUM::model(nsig*sig, nbkg*bg)')
    getattr(ws,'import')(shape)

    # Do the fit
    fitResult = shape.fitTo(data, ROOT.RooFit.Save())

    # Plot the result
    canv = ROOT.TCanvas('canv_%s'%histo.GetName(),'canvas', 800, 800)
    frame = mass.frame()
    data.plotOn(frame)
    shape.plotOn(frame,
               ROOT.RooFit.Name('total'),
               ROOT.RooFit.ProjWData(data),
               ROOT.RooFit.LineColor(ROOT.kBlue),
               ROOT.RooFit.LineWidth(2),
               ROOT.RooFit.MoveToBack())
    shape.plotOn(frame,
               ROOT.RooFit.Name('bkg'),
               ROOT.RooFit.ProjWData(data),
               ROOT.RooFit.Components('*bg*'),
               ROOT.RooFit.FillColor(ROOT.kGray),
               ROOT.RooFit.LineColor(ROOT.kGray),
               ROOT.RooFit.LineWidth(1),
               ROOT.RooFit.DrawOption('f'),
               ROOT.RooFit.FillStyle(1001),
               ROOT.RooFit.MoveToBack())
    frame.Draw()

    tlat = ROOT.TLatex()
    tlat.SetTextFont(83)
    tlat.SetNDC(1)
    tlat.SetTextSize(22)
    fitparms = ['cbb', 'cbw', 'cba', 'beta', 'gamma', 'alpha']
    for v in fitparms:
        val = ws.var(v).getVal()
        # if abs(val - ws.var(v).getMax()) < 1e-5:
        #     print ('########## %s is hitting maximum: %f (%f)' %
        #                   (v, val, ws.var(v).getMax()))
        # if abs(val - ws.var(v).getMin()) < 1e-5:
        #     print ('########## %s is hitting minimum: %f (%f)' %
        #                   (v, val, ws.var(v).getMin()))

        tlat.DrawLatex(0.14, 0.80-0.03*fitparms.index(v), '%-5s: %6.3f' % (v, val))
    tlat.DrawLatex(0.14, 0.86, 'Nsig : %8.1f' % (nsig.getVal()))
    tlat.DrawLatex(0.14, 0.83, 'Nbkg : %8.1f' % (nbkg.getVal()))


    canv.SaveAs(osp.join(odir,"massfit_%s.pdf"%(histo.GetName())))
    canv.SaveAs(osp.join(odir,"massfit_%s.png"%(histo.GetName())))
    if 'www' in odir: putPHPIndex(odir)

    return nsig.getVal(), nsig.getError(), nbkg.getVal(), nbkg.getError()

def doMassFits(infile, options):
    tf = ROOT.TFile.Open(infile, "READ")
    result = {} # histkey -> (nSig, nSigE)
    allhistos = [tf.Get(k.GetName()) for k in tf.GetListOfKeys()]
    print " Doing fits for %d histos" % len(allhistos)
    for histo in allhistos:
        try:
            print ("...processing %-75s" % ("%s with %d entries" %
                      (histo.GetName(), histo.GetEntries()))),

            nSig, nSigE, nBkg, nBkgE  = getNSignalEvents(histo,
                                           dofit=True if not options.cutNCount else False,
                                           odir=options.outDir)

            print " %s done: S: %.2f +- %.2f, B: %.2f +- %.2f %s" % (bcolors.OKGREEN,
                                           nSig, nSigE, nBkg, nBkgE, bcolors.ENDC)
            result[histo.GetName()] = (nSig, nSigE, nBkg, nBkgE)

        except ReferenceError:
            print " WARNING: Problem with %s, continuing without" % histo.GetName()
            continue

    return result

def parseCatFromHistName(name):
    import re
    regm = re.match((r'(data|DY)\_l1Pt\_([\.\d]+)\_l1Eta\_([\.\d]+)\_'
                     r'l2Pt\_([\.\d]+)\_l2Eta\_([\.\d]+)\_(SS|OS)'), name)
    try:
        proc, pt1, eta1, pt2, eta2, charge = regm.groups()
        return proc, float(pt1), float(eta1), float(pt2), float(eta2), charge
    except AttributeError:
        return None

def main(args, options):
    try:
        if not osp.exists(args[0]):
            print "Input file does not exists: %s" % args[0]
            sys.exit(-1)
    except IndexError:
        parser.print_usage()
        sys.exit(-1)

    # Do the fits and collect results
    cachefilename = "fitresults.pck"
    if not osp.isfile(cachefilename):
        fitresults = doMassFits(args[0], options)
        print "ALL DONE"

        with open(cachefilename, 'w') as cachefile:
            pickle.dump(fitresults, cachefile, pickle.HIGHEST_PROTOCOL)
            print ('>>> Wrote fit results to cache (%s)' %
                                                        cachefilename)
    else:
        with open(cachefilename, 'r') as cachefile:
            fitresults = pickle.load(cachefile)
            print ('>>> Read fit results from cache (%s)' %
                                                        cachefilename)

    # Remove non-parsable histos
    fitresults = {k:v for k,v in fitresults.iteritems() if parseCatFromHistName(k)}

    # Parse categories and bins from the histogram names
    parsedresults = {parseCatFromHistName(k):v for k,v in fitresults.iteritems()}
    ptbins  = sorted(list(set([float(p) for _,p1,_,p2,_,_ in parsedresults.keys() for p in (p1,p2)])))
    etabins = sorted(list(set([float(e) for _,_,e1,_,e2,_ in parsedresults.keys() for e in (e1,e2)])))

    categories = sorted(list(set([(p1,e1,p2,e2) for _,p1,e1,p2,e2,_ in parsedresults.keys()])))

    print "Found %d categories:" %len(categories)
    for proc in ['data', 'DY']:
        print 'assembling equations for %s' % proc
        eqfilename = 'equations_%s.dat' % proc
        with open(eqfilename, 'w') as eqfile:
            for p1,e1,p2,e2 in categories:
                nss, nsse, _, _ = parsedresults[(proc, p1, e1, p2, e2, 'SS')]
                nos, nose, _, _ = parsedresults[(proc, p1, e1, p2, e2, 'OS')]
                ratio, ratioerr = getRatio(nss, nos, nsse, nose)
                line = ('%2.0f, %5.3f, %2.0f, %5.3f: NSS/NOS '
                        '(%8.2f+-%6.2f)/(%11.2f+-%7.2f) = (%.6f+-%.6f)' %
                          (p1, e1, p2, e2, nss, nsse, nos, nose, ratio, ratioerr))
                print line
                eqfile.write("%d %d %d %d %.6f %.6f\n" % (ptbins.index(p1), etabins.index(e1),
                                                          ptbins.index(p2), etabins.index(e2),
                                                          ratio, ratioerr))
                # eqfile.write("%2.0f %5.3f %2.0f %5.3f %.5f %.5f\n" % (p1, e1, p2, e2, ratio, ratioerr))

        print "Wrote system of equations to %s" % eqfilename

    return 0

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """%prog [options] meecathistos.root

    Read a root file with histograms of ee invariant masses for
    same-sign (SS) and opposite-sign (OS) pairs, for data and MC.
    Fit each of them to extract the number of signal events.

    Finally, do a chi2 minimization of the system of equations to 
    get the charge misid probability in a number of pt and eta bins.
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--outDir", default="mass_fits/",
                      action="store", type="string", dest="outDir",
                      help=("Output directory for charge misid plots "
                            "[default: %default/]"))
    parser.add_option('-c', '--cutNCount', dest='cutNCount',
                      action="store_true",
                      help='Do cut & count instead of fitting mass shape')
    # parser.add_option('-j', '--jobs', dest='jobs', action="store",
    #                   type='int', default=1,
    #                   help=('Number of jobs to run in parallel '
    #                     '[default: single]'))
    (options, args) = parser.parse_args()

    sys.exit(main(args, options))
