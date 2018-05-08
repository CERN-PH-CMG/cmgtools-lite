import ROOT, os, datetime, re, operator


## ===================================================================
## USAGE:
## needs as infile a multidimfit.root result
## takes a comma separated list of regular expressions as input via --params
## if no output directory is given, it will just plot the smaller correlation matrix
## if output directory is given, it will save it there as pdf and png

## example:
## python w-helicity-13TeV/subMatrix.py --infile <multidimfit.root> --params alph,muR,muF,.*Ybin.*2,pdf12,pdf56,pdf42 --outdir <output_directory>
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
    parser = OptionParser(usage='%prog [options] ')
    parser.add_option('-i','--infile', dest='infile', default='', type='string', help='file with fitresult')
    parser.add_option('-o','--outdir', dest='outdir', default='', type='string', help='outdput directory to save the matrix')
    parser.add_option('-p','--params', dest='params', default='', type='string', help='parameters for which you want to show the correlation matrix. comma separated list of regexps')
    parser.add_option(     '--suffix', dest='suffix', default='', type='string', help='suffix for the correlation matrix')
    (options, args) = parser.parse_args()

    if options.outdir:
        ROOT.gROOT.SetBatch()
        if not os.path.isdir(options.outdir):
            os.system('mkdir -p {od}'.format(od=options.outdir))
        os.system('cp {pf} {od}'.format(pf='/afs/cern.ch/user/g/gpetrucc/php/index.php',od=options.outdir))

    infile = ROOT.TFile(options.infile, 'read')

    fitresult = infile.Get('fit_mdf')

    h2_corr = fitresult.correlationHist()

    c = ROOT.TCanvas("c","",1200,800)
    c.SetGridx()
    c.SetGridy()
    ROOT.gStyle.SetPalette(55)
    ROOT.gStyle.SetNumberContours(200); # default is 20 (values on palette go from -1 to 1)

    c.SetLeftMargin(0.09)
    c.SetRightMargin(0.11)
    c.SetBottomMargin(0.15)

    ## use a list here, because dicts are unordered
    binlabels = []
    pois_regexps = list(options.params.split(','))

    ## loop on all bin labels and store the name and index if it 
    ## fits any of the specified regexps

    for i in range(1,h2_corr.GetXaxis().GetNbins()+1):
        tmp_label = h2_corr.GetXaxis().GetBinLabel(i)
        for poi in pois_regexps:
            if re.match(poi, tmp_label): 
                ## x and y bin labels are different, so we need both
                ## append a tuple of (label, x-index, y-index) to the list
                binlabels.append( (tmp_label, i, h2_corr.GetNbinsX()+1-i) )

    ## sort the binlabels. alphabetically, except for pdfs, which are sorted by number
    binlabels = sorted(binlabels, key= lambda x: int(x[0].split('_')[-1]) if 'norm' in x[0] and '_Ybin_' in x[0] else 0)
    binlabels = sorted(binlabels, key= lambda x: int(x[0].replace('pdf','')) if 'pdf' in x[0] else 0)
        

    ## make the new, smaller TH2F correlation matrix
    nbins = len(binlabels)
    th2_sub = ROOT.TH2F('sub_corr_matrix', 'small correlation matrix', nbins, 0., nbins, nbins, 0., nbins)
    th2_sub.GetXaxis().SetTickLength(0.)
    th2_sub.GetYaxis().SetTickLength(0.)
    
    ## pretty nested loop. enumerate the tuples
    for i,(k1,vx1, vy1) in enumerate(binlabels):
        for j,(k2,vx2,vy2) in enumerate(binlabels):

            ## get the correct content from original histogram
            tmp_cont = h2_corr.GetBinContent(vx1, vy2)
            ## set it into the new sub-matrix
            th2_sub.SetBinContent(i+1, j+1, tmp_cont)
            ## set the labels correctly
            new_k1 = niceName(k1)
            new_k2 = niceName(k2)
            th2_sub.GetXaxis().SetBinLabel(i+1, new_k1)
            th2_sub.GetYaxis().SetBinLabel(j+1, new_k2)

    th2_sub.GetZaxis().SetRangeUser(-1, 1)
    th2_sub.Draw('colz text')

    if options.outdir:
        for i in ['pdf', 'png']:
            suff = '' if not options.suffix else '_'+options.suffix
            c.SaveAs(options.outdir+'/smallCorrelation{suff}.{i}'.format(suff=suff,i=i))
        os.system('cp {pf} {od}'.format(pf='/afs/cern.ch/user/g/gpetrucc/php/index.php',od=options.outdir))

