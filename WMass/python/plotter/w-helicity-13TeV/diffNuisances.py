#!/usr/bin/env python
import re
from sys import argv, stdout, stderr, exit
import datetime
from optparse import OptionParser
import HiggsAnalysis.CombinedLimit.calculate_pulls as CP 

# tool to compare fitted nuisance parameters to prefit values.
#
# Also used to check for potential problems in RooFit workspaces to be used with combine
# (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks)

# import ROOT with a fix to get batch mode (http://root.cern.ch/phpBB3/viewtopic.php?t=3198)
hasHelp = False
for X in ("-h", "-?", "--help"):
    if X in argv:
        hasHelp = True
        argv.remove(X)
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
argv.remove( '-b-' )
if hasHelp: argv.append("-h")

parser = OptionParser(usage="usage: %prog [options] in.root  \nrun with --help to get list of options")
parser.add_option("--vtol", "--val-tolerance", dest="vtol", default=0.30, type="float", help="Report nuisances whose value changes by more than this amount of sigmas")
parser.add_option("--stol", "--sig-tolerance", dest="stol", default=0.10, type="float", help="Report nuisances whose sigma changes by more than this amount")
parser.add_option("--vtol2", "--val-tolerance2", dest="vtol2", default=2.0, type="float", help="Report severely nuisances whose value changes by more than this amount of sigmas")
parser.add_option("--stol2", "--sig-tolerance2", dest="stol2", default=0.50, type="float", help="Report severely nuisances whose sigma changes by more than this amount")
parser.add_option("-a", "--all",      dest="show_all_parameters",    default=False,  action="store_true", help="Print all nuisances, even the ones which are unchanged w.r.t. pre-fit values.")
parser.add_option("-A", "--abs",      dest="absolute_values",    default=False,  action="store_true", help="Report also absolute values of nuisance values and errors, not only the ones normalized to the input sigma")
parser.add_option("-p", "--pois",      dest="pois",  default=None,   type="string",  help="Name of the nuisances to be fitted (comma separated list of regexps)")
parser.add_option("-f", "--format",   dest="format", default="text", type="string",  help="Output format ('text', 'latex', 'twiki'")
parser.add_option("-g", "--histogram", dest="plotfile", default=None, type="string", help="If true, plot the pulls of the nuisances to the given file.")
parser.add_option("", "--pullDef",  dest="pullDef", default="", type="string", help="Choose the definition of the pull, see python/calculate_pulls.py for options")

(options, args) = parser.parse_args()
if len(args) == 0:
    parser.print_usage()
    exit(1)

if options.pullDef!="" and options.pullDef not in CP.allowed_methods(): exit("Method %s not allowed, choose one of [%s]"%(options.pullDef,",".join(CP.allowed_methods())))


setUpString = "diffNuisances run on %s, at %s with the following options ... "%(args[0],datetime.datetime.utcnow())+str(options)

file = ROOT.TFile(args[0])
if file == None: raise RuntimeError, "Cannot open file %s" % args[0]
fit_s  = file.Get("fit_mdf")
if fit_s == None or fit_s.ClassName()   != "RooFitResult": raise RuntimeError, "File %s does not contain the output of the signal fit 'fit_mdf'"     % args[0]

isFlagged = {}

# maps from nuisance parameter name to the row to be printed in the table
table = {}

# get the initial/fitted parameters
fpi_s = fit_s.floatParsInit()
fpf_s = fit_s.floatParsFinal()
# get the ones to be plotted
#pars_all = list(fpi_s.at(i).GetName() for i in xrange(len(fpi_s)))
pars = list(fpi_s.at(i).GetName() for i in xrange(len(fpi_s))) 
if options.pois:
    poi_patts = options.pois.split(",")
    for ppatt in poi_patts:
        pars = filter(lambda x: re.match(ppatt,x),pars)

if any(re.match('pdf.*',x) for x in pars):
    pars = sorted(pars, key = lambda x: int(x.split('pdf')[-1]), reverse=False)

nuis_p_i=0
title = "pull" if options.pullDef else "#theta"

"""
def getGraph(hist,shift):

   gr = ROOT.TGraphAsymErrors()
   gr.SetName(hist.GetName())
   for i in range(hist.GetNbinsX()):
     x = hist.GetBinCenter(i+1)+shift
     y = hist.GetBinContent(i+1)
     e = hist.GetBinError(i+1)
     gr.SetPoint(i,x,y)
     gr.SetPointError(i,float(abs(shift))*0.8,e)
   return gr
"""

# Also make histograms for pull distributions:
hist_fit_s  = ROOT.TH1F("fit_s"   ,"S+B fit Nuisances   ;;%s "%title,len(pars),0,len(pars))
hist_prefit = ROOT.TH1F("prefit_nuisancs","Prefit Nuisances    ;;%s "%title,len(pars),0,len(pars))
# Store also the *asymmetric* uncertainties

gr_fit_s    = ROOT.TGraphAsymmErrors(); gr_fit_s.SetTitle("fit_b_s")


# loop over all fitted parameters
for name in pars:

    nuis_s = fpf_s.find(name)
    nuis_p = fpi_s.find(name)

    # keeps information to be printed about the nuisance parameter
    row = []

    flag = False;
    mean_p, sigma_p, sigma_pu, sigma_pd = 0,0,0,0

    if nuis_p == None:
        # nuisance parameter NOT present in the prefit result
        if not options.absolute_values: continue
        row += [ "[%.2f, %.2f]" % (nuis_s.getMin(), nuis_s.getMax()) ]

    else:
        # get best-fit value and uncertainty at prefit for this 
        # nuisance parameter
 	if nuis_p.getErrorLo()==0 : nuis_p.setErrorLo(nuis_p.getErrorHi())
        mean_p, sigma_p, sigma_pu,sigma_pd = (nuis_p.getVal(), nuis_p.getError(),nuis_p.getErrorHi(),nuis_p.getErrorLo())

	if not sigma_p > 0: sigma_p = (nuis_p.getMax()-nuis_p.getMin())/2
	nuisIsSymm = abs(abs(nuis_p.getErrorLo())-abs(nuis_p.getErrorHi()))<0.01 or nuis_p.getErrorLo() == 0
        if options.absolute_values: 
		if nuisIsSymm : row += [ "%.6f +/- %.6f" % (nuis_p.getVal(), nuis_p.getError()) ]
		else: row += [ "%.6f +%.6f %.6f" % (nuis_p.getVal(), nuis_p.getErrorHi(), nuis_p.getErrorLo()) ]

    for fit_name, nuis_x in [('s',nuis_s)]:
        if nuis_x == None:
            row += [ " n/a " ]
        else:
	    nuisIsSymm = abs(abs(nuis_x.getErrorLo())-abs(nuis_x.getErrorHi()))<0.01 or nuis_x.getErrorLo() == 0
            if nuisIsSymm : row += [ "%+.2f +/- %.2f" % (nuis_x.getVal(), nuis_x.getError()) ]
	    else: row += [ "%+.2f +%.2f %.2f" % (nuis_x.getVal(), nuis_x.getErrorHi(), nuis_x.getErrorLo()) ]
 	    if nuis_x.getErrorLo()==0 : nuis_x.setErrorLo(nuis_x.getErrorHi())
            if nuis_p != None:
	        if options.plotfile: 
                  nuis_p_i+=1
	          if fit_name=='s': # fit name 'b' is not there when running MultiDimFit
		    if options.pullDef and nuis_p!=None:
		      nx,ned,neu = CP.returnPullAsym(options.pullDef,nuis_x.getVal(),mean_p,nuis_x.getErrorHi(),sigma_pu,abs(nuis_x.getErrorLo()),abs(sigma_pd))
		      gr_fit_s.SetPoint(nuis_p_i-1,nuis_p_i-0.5-0.1,nx)
		      gr_fit_s.SetPointError(nuis_p_i-1,0,0,ned,neu)
		    else:
		      gr_fit_s.SetPoint(nuis_p_i-1,nuis_p_i-0.5-0.1,nuis_x.getVal())
		      gr_fit_s.SetPointError(nuis_p_i-1,0,0,abs(nuis_x.getErrorLo()),nuis_x.getErrorHi())
	      	    hist_fit_s.SetBinContent(nuis_p_i,nuis_x.getVal())
	      	    hist_fit_s.SetBinError(nuis_p_i,nuis_x.getError())
	      	    hist_fit_s.GetXaxis().SetBinLabel(nuis_p_i,name)
	      	    gr_fit_s.GetXaxis().SetBinLabel(nuis_p_i,name)
		  hist_prefit.SetBinContent(nuis_p_i,mean_p)
		  hist_prefit.SetBinError(nuis_p_i,sigma_p)
	      	  hist_prefit.GetXaxis().SetBinLabel(nuis_p_i,name)

                if sigma_p>0: 

                        # calculate the difference of the nuisance parameter
                        # w.r.t to the prefit value in terms of the uncertainty
                        # on the prefit value
			valShift = (nuis_x.getVal() - mean_p)/sigma_p

                        # ratio of the nuisance parameter's uncertainty
                        # w.r.t the prefit uncertainty
                	sigShift = nuis_x.getError()/sigma_p

		else :
			#print "No definition for prefit uncertainty %s. Printing absolute shifts"%(nuis_p.GetName())
			valShift = (nuis_x.getVal() - mean_p)
                	sigShift = nuis_x.getError()
                if options.absolute_values:
                    row[-1] += " (%+4.2fsig, %4.2f)" % (valShift, sigShift)
                else:
                    row[-1] = " %+4.2f, %4.2f" % (valShift, sigShift)

                if (abs(valShift) > options.vtol2 or abs(sigShift-1) > options.stol2):

                    # severely report this nuisance:
                    # 
                    # the best fit moved by more than 2.0 sigma or the uncertainty (sigma)
                    # changed by more than 50% (default thresholds) w.r.t the prefit values

                    isFlagged[(name,fit_name)] = 2

                    flag = True

                elif (abs(valShift) > options.vtol  or abs(sigShift-1) > options.stol):

                    # report this nuisance:
                    # 
                    # the best fit moved by more than 0.3 sigma or the uncertainty (sigma)
                    # changed by more than 10% (default thresholds) w.r.t the prefit values

                    if options.show_all_parameters: isFlagged[(name,fit_name)] = 1

                    flag = True

                elif options.show_all_parameters:
                    flag = True

    # end of loop over s and b

    row += [ "%+4.2f"  % fit_s.globalCorr(name) ]
    if flag or options.show_all_parameters: table[name] = row

#end of loop over all fitted parameters

#----------
# print the results
#----------

#print details
print setUpString
print 

fmtstring = "%-40s     %15s  %10s"
highlight = "*%s*"
morelight = "!%s!"
pmsub, sigsub = None, None
if options.format == 'text':
    if options.absolute_values:
        fmtstring = "%-40s     %15s    %30s  %10s"
        print fmtstring % ('name', 'pre fit', 's+b fit', 'rho')
    else:
        print fmtstring % ('name', 's+b fit', 'rho')
elif options.format == 'latex':
    pmsub  = (r"(\S+) \+/- (\S+)", r"$\1 \\pm \2$")
    sigsub = ("sig", r"$\\sigma$")
    highlight = "\\textbf{%s}"
    morelight = "{{\\color{red}\\textbf{%s}}}"
    if options.absolute_values:
        fmtstring = "%-40s &  %15s & %30s & %6s \\\\"
        print "\\begin{tabular}{|l|r|r|r|} \\hline ";
        print (fmtstring % ('name', 'pre fit', '$s+b$ fit', r'$\rho(\theta, \mu)$')), " \\hline"
    else:
        fmtstring = "%-40s & %15s & %6s \\\\"
        print "\\begin{tabular}{|l|r|r|} \\hline ";
        #what = r"$(x_\text{out} - x_\text{in})/\sigma_{\text{in}}$, $\sigma_{\text{out}}/\sigma_{\text{in}}$"
        what = r"\Delta x/\sigma_{\text{in}}$, $\sigma_{\text{out}}/\sigma_{\text{in}}$"
        print  fmtstring % ('', '$s+b$ fit', '')
        print (fmtstring % ('name', what, r'$\rho(\theta, \mu)$')), " \\hline"
elif options.format == 'html':
    pmsub  = (r"(\S+) \+/- (\S+)", r"\1 &plusmn; \2")
    sigsub = ("sig", r"&sigma;")
    highlight = "<b>%s</b>"
    morelight = "<strong>%s</strong>"
    print """
<html><head><title>Comparison of nuisances</title>
<style type="text/css">
    td, th { border-bottom: 1px solid black; padding: 1px 1em; }
    td { font-family: 'Consolas', 'Courier New', courier, monospace; }
    strong { color: red; font-weight: bolder; }
</style>
</head><body style="font-family: 'Verdana', sans-serif; font-size: 10pt;"><h1>Comparison of nuisances</h1>
<table>
"""
    if options.absolute_values:
        print "<tr><th>nuisance</th><th>pre fit</th><th>signal fit</th><th>correlation</th></tr>"
        fmtstring = "<tr><td><tt>%-40s</tt> </td><td> %-15s </td><td> %-30s </td><td> %-15s </td></tr>"
    else:
        what = "&Delta;x/&sigma;<sub>in</sub>, &sigma;<sub>out</sub>/&sigma;<sub>in</sub>";
        print "<tr><th>nuisance</th><th>signal fit<br/>%s</th><th>&rho;(&mu;, &theta;)</tr>" % (what,what)
        fmtstring = "<tr><td><tt>%-40s</tt> </td><td> %-15s </td><td> %-15s </td></tr>"

names = table.keys()
names.sort()
highlighters = { 1:highlight, 2:morelight };
for n in names:
    v = table[n]
    if options.format == "latex": n = n.replace(r"_", r"\_")
    if pmsub  != None: v = [ re.sub(pmsub[0],  pmsub[1],  i) for i in v ]
    if sigsub != None: v = [ re.sub(sigsub[0], sigsub[1], i) for i in v ]
    if (n,'s') in isFlagged: v[-2] = highlighters[isFlagged[(n,'s')]] % v[-2]
    if options.absolute_values:
       print fmtstring % (n, v[0], v[1], v[2])
    else:
       print fmtstring % (n, v[0], v[1])

if options.format == "latex":
    print " \\hline\n\end{tabular}"
elif options.format == "html":
    print "</table></body></html>"


if options.plotfile:
    import ROOT
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    fout = ROOT.TFile(options.plotfile,"RECREATE")

    canvas_nuis = ROOT.TCanvas("nuisances", "nuisances", 900, 600)
    hist_fit_e_s = hist_fit_s.Clone("errors_s")
    #gr_fit_s = getGraph(hist_fit_s,-0.1)
    gr_fit_s.SetLineColor(ROOT.kRed)
    gr_fit_s.SetMarkerColor(ROOT.kRed)
    gr_fit_s.SetMarkerStyle(20)
    gr_fit_s.SetMarkerSize(1.0)
    gr_fit_s.SetLineWidth(2)
    hist_prefit.SetLineWidth(2)
    hist_prefit.SetTitle("")
    hist_prefit.SetLineColor(ROOT.kBlack)
    hist_prefit.SetFillColor(ROOT.kGray)
    hist_prefit.LabelsOption("v");
    hist_prefit.SetMaximum(3)
    hist_prefit.SetMinimum(-3)
    hist_prefit.Draw("E2")
    hist_prefit.Draw("histsame")
    gr_fit_s.Draw("EPsame")
    canvas_nuis.SetGridx()
    canvas_nuis.RedrawAxis()
    canvas_nuis.RedrawAxis('g')
    leg=ROOT.TLegend(0.6,0.7,0.89,0.89)
    leg.SetFillColor(0)
    leg.SetTextFont(42)
    leg.AddEntry(hist_prefit,"Prefit","FL")
    leg.AddEntry(gr_fit_s,"S+B fit"   ,"EPL")
    leg.Draw()
    fout.WriteTObject(canvas_nuis)
    for ext in ['png', 'pdf']:
        canvas_nuis.SaveAs("nuisances.%s" % ext)
    canvas_pferrs = ROOT.TCanvas("post_fit_errs", "post_fit_errs", 900, 600)
    for b in range(1,hist_fit_e_s.GetNbinsX()+1): 
      hist_fit_e_s.SetBinContent(b,hist_fit_s.GetBinError(b)/hist_prefit.GetBinError(b))
      hist_fit_e_s.SetBinError(b,0)
    hist_fit_e_s.SetFillColor(ROOT.kRed)
    hist_fit_e_s.SetBarWidth(0.4)
    hist_fit_e_s.GetYaxis().SetTitle("#sigma_{#theta}/(#sigma_{#theta} prefit)")
    hist_fit_e_s.SetTitle("Nuisance Parameter Uncertainty Reduction")
    hist_fit_e_s.LabelsOption("v");
    hist_fit_e_s.SetMaximum(1.5)
    hist_fit_e_s.SetMinimum(0)
    hist_fit_e_s.Draw("bar")
    leg_rat=ROOT.TLegend(0.6,0.7,0.89,0.89)
    leg_rat.SetFillColor(0)
    leg_rat.SetTextFont(42)
    leg_rat.AddEntry(hist_fit_e_s,"S+B fit"   ,"F")
    leg_rat.Draw()
    line_one = ROOT.TLine(0,1,hist_fit_e_s.GetXaxis().GetXmax(),1)
    line_one.SetLineColor(1); line_one.SetLineStyle(2); line_one.SetLineWidth(2)
    line_one.Draw()
    canvas_pferrs.RedrawAxis()
    for ext in ['png', 'pdf']:
        canvas_pferrs.SaveAs("pferrs.%s" % ext)

    fout.WriteTObject(canvas_pferrs)

   

