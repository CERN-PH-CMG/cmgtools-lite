#!/usr/bin/env python
import os
import re
import sys
import json
import numpy as np
import pandas as pd

from functools import partial
from collections import namedtuple
from scipy.interpolate import splev, splrep

import matplotlib.pyplot as plt
import matplotlib as mpl

#import seaborn as sns
#sns.set(style="ticks")
#sns.set_context("poster")

from process_limits import scale_limits
from plotLimit import readConfig
from plotLimit import setUpMPL

## type 1

def process(inputfile, xaxis, added=None):
    df = pd.read_csv(inputfile, sep=",", index_col=None)

    # Drop failed fit results
    #df.dropna(subset=['dnll'], inplace=True)

    # Calculate relative NLL
    if not 'dnll'in df.columns:
        df['dnll'] = 2*(df.nllr1 - df.nllr0)
    else:
        df['dnll'] = -2*df.dnll

    # Add in ratio column if it's not there
    if not 'ratio' in df.columns:
        try:
            df['ratio'] = df.cf/df.cv
            df['ratio'] = df[xaxis].round(3)
        except AttributeError:
            print "Failed to build ratio column in dataframe... check input file"

    # Drop duplicates for equal ratios
    df.drop_duplicates(subset='cf', inplace=True)
    df.sort_values(by="cf", inplace=True) # Xanda FIXME
    df.index = range(1,len(df)+1)
    print df#["rescalecv",  "rescalect", "dnll"]
    
    # Add interpolating points?
    if added:
        df = addInterpolatingPoints(df, added, xaxis, npoints=3)
    
    # Shift dnll up by lowest value
    dnllmin = np.min(df.dnll)
    idxmin = df.dnll.idxmin()
    assert(df.loc[idxmin].dnll == dnllmin), "inconsistent minimum?"
    print '... shifting dnll values by %5.3f (at %4.2f) for %s' % (np.abs(dnllmin), df.loc[idxmin][xaxis], inputfile)
    df['dnll'] = df.dnll + np.abs(dnllmin)

    return df


def addInterpolatingPoints(dframe, filename, xaxis,npoints=3):
    """
    Add additional, interpolating points. dframe should contain the original points
    FIXME: - Take only ONE file and do it automatically
           - Need to pass a list of predefined ratio values
    """
    print "Adding interpolating points from", filename
    files  = {v:os.path.basename(f) for v,f in zip(dframe[xaxis], dframe.fname)}

    def addvalues(x, y, nvals=1):
        return [np.round(v, 4) for v in list(np.linspace(x,y, nvals+2))[1:-1]]

    added_values = {} # new ratio value -> (file1, weight1), (file2, weight2)
    for x,y in zip(list(dframe[xaxis])[:-1], list(dframe[xaxis])[1:]):
        to_add = addvalues(x, y, npoints)
        weights = [float(n)/(npoints+1) for n in range(npoints, 0, -1)]

        for val, weight in zip(to_add, weights):
            added_values[val] = ((files[x], weight), (files[y], 1.0-weight))

    df = pd.read_csv(filename)
    df['fname'] = df.fname.apply(os.path.basename)
    df.sort_values(by="rescalect", inplace=True)
    df.index = range(1,len(df)+1)
    df['dnll'] = 2*(df.nllr1 - df.nllr0)

    def get_dll(ratio, fname, dframe=df, att='dnll'):
        return float(dframe.loc[dframe.fname==fname].loc[dframe[xaxis]==ratio][att])

    df_added = pd.DataFrame(sorted(added_values.keys()), columns=['ratio'])
    df_added['file1']   = [added_values[k][0][0] for k in df_added[xaxis]]
    df_added['weight1'] = [added_values[k][0][1] for k in df_added[xaxis]]
    df_added['file2']   = [added_values[k][1][0] for k in df_added[xaxis]]
    df_added['weight2'] = [added_values[k][1][1] for k in df_added[xaxis]]

    df_added['dnll1'] = np.vectorize(partial(get_dll, dframe=df, att='dnll'))(df_added[xaxis], df_added.file1)
    df_added['dnll2'] = np.vectorize(partial(get_dll, dframe=df, att='dnll'))(df_added[xaxis], df_added.file2)
    df_added['dnll'] = df_added.weight1*df_added.dnll1 + df_added.weight2*df_added.dnll2
    df_added['bfr1'] = np.vectorize(partial(get_dll, dframe=df, att='bestfitr'))(df_added[xaxis], df_added.file1)
    df_added['bfr2'] = np.vectorize(partial(get_dll, dframe=df, att='bestfitr'))(df_added[xaxis], df_added.file2)
    df_added['bestfitr'] = df_added.weight1*df_added.bfr1 + df_added.weight2*df_added.bfr2

    # Drop temporary columns
    df_added = df_added.drop(columns=['file1', 'weight1', 'file2', 'weight2', 'dnll1', 'dnll2', 'bfr1', 'bfr2'])

    dframe = dframe.append(df_added)
    dframe.sort_values(by='ratio', inplace=True)
    dframe.index = range(1,len(dframe)+1)

    return dframe


def plotNLLScans(cfg, outdir='plots/', tag='', nosplines=False, smoothing=0.0):
    for entry in cfg['entries']:
        filename = entry['csv_file']
        print ("reading: ", filename )
        if 'inputdir' in cfg:
            filename = os.path.join(cfg['inputdir'], entry['csv_file'])
        #entry['df'] = process(filename)
        xaxis = cfg["xaxis"]
        x_axis_label = cfg['x_axis_label']
        #entry['df'] = process(filename, xaxis, added=entry.get('csv_file_interp'))
        entry['df'] = process(filename, xaxis,added=None)
    fig, ax = plt.subplots(1)

    x = sorted(list(set(cfg['entries'][0]['df'][xaxis].values.tolist())))
    x2 = np.linspace(-3, 3 ,100000) # Evaluate spline at more points

    for entry in cfg['entries']:
        df = entry['df']
        print (df.loc[df[xaxis]<=cfg['xmax']].loc[df[xaxis]>=-cfg['xmax']].dnll)
        if nosplines:
            ax.plot(df.loc[df[xaxis]<=cfg['xmax']].loc[df[xaxis]>=-cfg['xmax']][xaxis],
                    df.loc[df[xaxis]<=cfg['xmax']].loc[df[xaxis]>=-cfg['xmax']].dnll,
                    lw=entry['line_width'], c=entry['color'], ls=entry['line_style'])
        else:
            spline = splev(x2, splrep(df[xaxis], df.dnll, s=cfg.get('smoothing', 1.0), k=3))
            ax.plot(x2, spline, ls=entry['line_style'], lw=entry['line_width'], color=entry['color'],zorder=0)
        ax.scatter(df.loc[df[xaxis]<=cfg['xmax']].loc[df[xaxis]>=-cfg['xmax']][xaxis],
                   df.loc[df[xaxis]<=cfg['xmax']].loc[df[xaxis]>=-cfg['xmax']].dnll,
                marker=entry['marker_style'], s=30, c=entry['color'], lw=entry['line_width'])

    # Configure axes
    ax.get_xaxis().set_tick_params(which='both', direction='in')
    if cfg['xmax'] == 1 :
        ax.get_xaxis().set_major_locator(mpl.ticker.MultipleLocator(0.1))
        ax.get_xaxis().set_minor_locator(mpl.ticker.MultipleLocator(0.010))
        ax.set_xlim(0.0, cfg['xmax'])
    else :
        ax.get_xaxis().set_major_locator(mpl.ticker.MultipleLocator(1.0))
        ax.get_xaxis().set_minor_locator(mpl.ticker.MultipleLocator(0.10))
        ax.set_xlim(-cfg['xmax'], cfg['xmax'])

    ax.axhline(1.0, lw=0.5, ls='--', color='gray')
    ax.axhline(4.0, lw=0.5, ls='--', color='gray')
    ax.axhline(9.0, lw=0.5, ls='--', color='gray')
    ax.axhline(16.0, lw=0.5, ls='--', color='gray')
    ax.axhline(25.0, lw=0.5, ls='--', color='gray')
    plt.text(cfg['xmax'] + 0.02*cfg['xmax'], 1.0-0.2, "1$\\sigma$", fontsize=14, color='gray')
    plt.text(cfg['xmax'] + 0.02*cfg['xmax'], 4.0-0.2, "2$\\sigma$", fontsize=14, color='gray')
    plt.text(cfg['xmax'] + 0.02*cfg['xmax'], 9.0-0.2, "3$\\sigma$", fontsize=14, color='gray')
    plt.text(cfg['xmax'] + 0.02*cfg['xmax'], 16.0-0.2, "4$\\sigma$", fontsize=14, color='gray')
    plt.text(cfg['xmax'] + 0.02*cfg['xmax'], 25.0-0.2, "5$\\sigma$", fontsize=14, color='gray')

    ## Draw 95% C.L. line:
    # ax.axhline(3.84, lw=0.5, ls='-.', color='gray')
    # plt.text(-cfg['xmax'] + 0.02*cfg['xmax'], 3.84-0.2, "95\\% C.L.", fontsize=14, color='gray')

    ax.set_ylim(0., cfg['ymax'])
    ax.set_yscale("linear", nonposy='clip')
    ax.get_yaxis().set_tick_params(which='both', direction='in')
    ax.get_yaxis().set_major_locator(mpl.ticker.MultipleLocator(cfg['y_major_ticks']))
    ax.get_yaxis().set_minor_locator(mpl.ticker.MultipleLocator(cfg['y_minor_ticks']))

    # Set axis labels
    ax.set_xlabel(x_axis_label , fontsize=24, labelpad=20)
    ax.set_ylabel(cfg['y_axis_label'], fontsize=24, labelpad=20)

    def print_text(x, y, text, fontsize=24, addbackground=True, bgalpha=0.8):
        if addbackground:
            ptext = plt.text(x, y, text, fontsize=fontsize, transform=ax.transAxes, backgroundcolor='white')
            ptext.set_bbox(dict(alpha=bgalpha, color='white'))
        else:
            ptext = plt.text(x, y, text, fontsize=fontsize, transform=ax.transAxes)

    # Print stuff
    print_text(0.03, 1.02, cfg["header_left"], 28, addbackground=False)
    print_text(0.65, 1.02, cfg["header_right"], addbackground=False)
    print_text(0.06, 0.92, cfg["tag1"], bgalpha=cfg["text_bg_alpha"])
    print_text(0.06, 0.86, cfg["tag2"], bgalpha=cfg["text_bg_alpha"])
    print_text(0.06, 0.78, cfg["tag3"], bgalpha=cfg["text_bg_alpha"])

    # Cosmetics
    import matplotlib.patches as mpatches
    legentries = []
    for entry in cfg['entries']:
        legentries.append(mpl.lines.Line2D([], [],
                          color=entry['color'], linestyle=entry['line_style'],
                          label=entry['label'], marker=entry['marker_style'], markersize=14, markerfacecolor=entry['color'], c=entry['color'], linewidth=2))

    # Legend
    legend = plt.legend(handles=legentries, fontsize=18, loc='upper right',
                        frameon=True, framealpha=cfg["text_bg_alpha"])
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_linewidth(0)

    # Save to pdf/png
    outfile = os.path.join(outdir, cfg['name'])
    # outfile = os.path.join(outdir, os.path.splitext(os.path.basename(cfg['entries'][0]['csv_file']))[0])
    if tag:
        outfile += '_%s' % tag
    plt.savefig("%s.pdf"%outfile, bbox_inches='tight')
    plt.savefig("%s.png"%outfile, bbox_inches='tight', dpi=300)
    print "...saved plot in %s.pdf" % outfile

    return 0

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """%prog config.json"""
    parser = OptionParser(usage=usage)
    parser.add_option("-o","--outdir", dest="outdir",
                      type="string", default="plots/")
    parser.add_option("-t","--tag", dest="tag",
                      type="string", default="")
    parser.add_option("--nosplines", dest="nosplines",
                      action="store_true", default=False)
    parser.add_option("--defaultOptions", dest="defaultOptions",
                      type="string", default="cards/defaults_nllscan.json",
                      help="Config file for default options")

    parser.add_option("--inputdir", dest="inputdir",
                      type="string", default=None,
                      help="Take csv files from this input directory (override config file)")
    parser.add_option("-n", "--name", dest="name",
                      type="string", default=None,
                      help="Output name (override config file)")
    parser.add_option("--header_left", dest="header_left",
                      type="string", default=None,
                      help="Header left (override config file)")

    parser.add_option("--ymax", dest="ymax", type='float',
                      default=None, help="Y axis maximum")
    parser.add_option("--xmax", dest="xmax", type='float',
                      default=None, help="X axis maximum/minimum")
    parser.add_option("--y_major_ticks", dest="y_major_ticks", type='float',
                      default=None, help="Major ticks on y axis")
    parser.add_option("--y_minor_ticks", dest="y_minor_ticks", type='float',
                      default=None, help="Minor ticks on y axis")
    parser.add_option("--smoothing", dest="smoothing", type='float',
                      default=None, help="Smoothing for splines")
    (options, args) = parser.parse_args()

    try:
        os.system('mkdir -p %s' % options.outdir)
    except ValueError:
        pass

    setUpMPL()
    
    for ifile in args:
        print ("ifile =", ifile)
        if not os.path.exists(ifile):
            print "Ignoring %s" % ifile
            continue

        plotConfig = readConfig(options.defaultOptions, options=options)
        plotConfig.update(readConfig(ifile))

        # Do fixes here
        for attr in ['xmax', 'ymax', 'y_major_ticks', 'y_minor_ticks', 'smoothing']:
            if getattr(options, attr, None) is not None:
                plotConfig[attr] = float(getattr(options, attr, plotConfig[attr]))
        for attr in ['inputdir', 'name', 'header_left']:
            if getattr(options, attr, None) is not None:
                plotConfig[attr] = str(getattr(options, attr, plotConfig[attr]))
        print(plotConfig)
        plotNLLScans(plotConfig, outdir=options.outdir, tag=options.tag, nosplines=options.nosplines)

    sys.exit(0)
