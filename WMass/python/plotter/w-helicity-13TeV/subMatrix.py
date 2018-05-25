import ROOT, os, datetime, re, operator, math
ROOT.gROOT.SetBatch(True)

## ===================================================================
## USAGE:
## needs as infile a toys.root with limit tree from toys
## takes a comma separated list of regular expressions as input via --params
## if no output directory is given, it will just plot the smaller correlation matrix
## if output directory is given, it will save it there as pdf and png

## example:
## python w-helicity-13TeV/subMatrix.py toys.root --params alph,muR,muF,.*Ybin.*2,pdf12,pdf56,pdf42 --outdir <output_directory>
## examples of common regexps:
## NORMs: 'norm_.*'
## PDFs: range [1,20]: '^pdf([1-9]|1[0-9])|20$'
## ===================================================================


def niceName(name):

    if '_Ybin_' in name:
        nn  = '#mu: ' if '_mu_' in name else 'el: '
        nn += 'W+ ' if 'plus' in name else 'W- '
        nn += 'left ' if 'left' in name else 'right '
        nn += name.split('_')[-1]

        if 'eff_unc' in name:
            nn = '#epsilon_{unc}^{'+nn+'}'
        return nn
        
    else:
        return name
        

if __name__ == "__main__":

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetPaintTextFormat('.3f')

    date = datetime.date.today().isoformat()

    from optparse import OptionParser
    parser = OptionParser(usage='%prog workspace.root toys.root [options] ')
    parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='outdput directory to save the matrix')
    parser.add_option('-p','--params', dest='params', default='', type='string', help='parameters for which you want to show the correlation matrix. comma separated list of regexps')
    parser.add_option(     '--suffix', dest='suffix', default='', type='string', help='suffix for the correlation matrix')
    (options, args) = parser.parse_args()

    if len(args)<2: raise RuntimeError, "Need at least workspace.root toys.root to run. Exiting."

    if options.outdir:
        ROOT.gROOT.SetBatch()
        if not os.path.isdir(options.outdir):
            os.system('mkdir -p {od}'.format(od=options.outdir))
        os.system('cp {pf} {od}'.format(pf='/afs/cern.ch/user/g/gpetrucc/php/index.php',od=options.outdir))

    pois_regexps = list(options.params.split(','))
    print "Filtering POIs with the following regex: ",pois_regexps

    ### GET LIST OF PARAMETERS AND INITIAL VALUES FROM THE WORKSPACE
    wsfile = ROOT.TFile(args[0], 'read')
    rws = wsfile.Get('w')
    pars = ROOT.RooArgList(rws.allVars())
    params = list(pars.at(i).GetName() for i in xrange(len(pars)))
    params = filter(lambda x: not x.endswith('_In'),params)
    params = filter(lambda x: any([re.match(rgx,x) for rgx in pois_regexps]),params)
    
    print "filtered params = ",params

    toysfile = ROOT.TFile(args[1], 'read')
    toys = toysfile.Get('limit')
    
    fitvals = {}
    fiterrs = {}
    floatParams = []
    for p in params:
        bname = 'trackedParam_{par}'.format(par=p)
        if toys.GetBranch(bname) == None:
            # print "WARING! Branch for variable ",p," not tracked in the toys!"
            continue
        floatParams.append(p)
        central_val = pars.find(p).getVal()
        residual_thr = central_val*1E-03 if central_val!=0 else 1E-03 # to remove bad fits with BGSF2
        toys.Draw('{branch}>>h_{par}'.format(branch=bname,par=p),'abs({branch}-{central})>{thr}'.format(branch=bname,central=central_val,thr=residual_thr))
        h = ROOT.gROOT.FindObject('h_{par}'.format(par=p)).Clone()
        fitvals[p] = h.GetMean()
        fiterrs[p] = h.GetRMS()
        print "Par: ",p,":\tInitial = ",central_val,"\tFit = ",fitvals[p]," +/- ",fiterrs[p]

    print "===> Build covariance matrix from this set of params: ",floatParams

    cov = {}
    for i in xrange(len(floatParams)):
        for j in xrange(i,len(floatParams)):
            x=floatParams[i]; y=floatParams[j]
            bnamex='trackedParam_'+x; bnamey='trackedParam_'+y
            if toys.GetBranch(bnamex)==None or toys.GetBranch(bnamey)==None:
                continue
            print "Build covariance element: [",x,",",y,"]"
            central_val_x = pars.find(x).getVal(); central_val_y = pars.find(y).getVal()

            ### this gof criteria may screw up the corr matrix
            residual_x = 'abs({bnamex}-{cx})'.format(bnamex=bnamex,cx=central_val_x); residual_y = 'abs({bnamey}-{cy})'.format(bnamey=bnamey,cy=central_val_y);
            residual_thr_x = central_val_x*1E-02 if central_val_x!=0 else 1E-02; residual_thr_y = central_val_y*1E-02 if central_val_y!=0 else 1E-02
            residual_uthr_x = central_val_x*0.1 if central_val_x!=0 else 3; residual_uthr_y = central_val_y*0.1 if central_val_y!=0 else 3
            gof = '{resx}>{cutx} && {resy}>{cuty} && {resx}<{ucutx} && {resy}<{ucuty}'.format(cutx=residual_thr_x,resx=residual_x,cuty=residual_thr_y,resy=residual_y,ucutx=residual_uthr_x,ucuty=residual_uthr_y)
            var = '({x}-{x0})*({y}-{y0})'.format(x='trackedParam_'+x,x0=fitvals[x],y='trackedParam_'+y,y0=fitvals[y])
            toys.Draw('{var}>>h_{x}_{y}'.format(var=var,x=x,y=y),gof)
            h = ROOT.gROOT.FindObject('h_{x}_{y}'.format(x=x,y=y)).Clone()
            cov[(x,y)] = h.GetMean()
    for i in xrange(len(floatParams)):
        for j in xrange(i):
            x=floatParams[i]; y=floatParams[j]
            cov[(x,y)]=cov[(y,x)]

    corr = {}
    for x in floatParams:
        for y in floatParams:
            corr[(x,y)] = cov[(x,y)]/math.sqrt(cov[(x,x)])/math.sqrt(cov[(y,y)])
            # print x," - ",y," => cov = ",cov[(x,y)],"; sigma(x) = ",math.sqrt(cov[(x,x)]),"; sigma(y) = ",math.sqrt(cov[(y,y)])

    ## sort the floatParams. alphabetically, except for pdfs, which are sorted by number
    floatParams = sorted(floatParams, key= lambda x: int(x.split('_')[-1]) if 'norm' in x and '_Ybin_' in x else 0)
    floatParams = sorted(floatParams, key= lambda x: int(x.replace('pdf','')) if 'pdf' in x else 0)
            
    print "sorted params = ",floatParams

    c = ROOT.TCanvas("c","",1200,800)
    c.SetGridx()
    c.SetGridy()
    ROOT.gStyle.SetPalette(55)
    ROOT.gStyle.SetNumberContours(200); # default is 20 (values on palette go from -1 to 1)

    c.SetLeftMargin(0.09)
    c.SetRightMargin(0.11)
    c.SetBottomMargin(0.15)

    ## make the new, smaller TH2F correlation matrix
    nbins = len(floatParams)
    th2_sub = ROOT.TH2F('sub_corr_matrix', 'small correlation matrix', nbins, 0., nbins, nbins, 0., nbins)
    th2_sub.GetXaxis().SetTickLength(0.)
    th2_sub.GetYaxis().SetTickLength(0.)
    
    ## pretty nested loop. enumerate the tuples
    for i,x in enumerate(floatParams):
        for j,y in enumerate(floatParams):
            ## set it into the new sub-matrix
            th2_sub.SetBinContent(i+1, j+1, corr[(x,y)])
            ## set the labels correctly
            new_x = niceName(x)
            new_y = niceName(y)
            th2_sub.GetXaxis().SetBinLabel(i+1, new_x)
            th2_sub.GetYaxis().SetBinLabel(j+1, new_y)

    th2_sub.GetZaxis().SetRangeUser(-1, 1)
    if len(params)<30: th2_sub.Draw('colz text')
    else: th2_sub.Draw('colz')

    if options.outdir:
        for i in ['pdf', 'png']:
            suff = '' if not options.suffix else '_'+options.suffix
            c.SaveAs(options.outdir+'/smallCorrelation{suff}.{i}'.format(suff=suff,i=i))
        os.system('cp {pf} {od}'.format(pf='/afs/cern.ch/user/g/gpetrucc/php/index.php',od=options.outdir))

