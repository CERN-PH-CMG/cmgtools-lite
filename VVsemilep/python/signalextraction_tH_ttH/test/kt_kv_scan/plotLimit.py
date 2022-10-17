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

import seaborn as sns
sns.set(style="ticks")
sns.set_context("poster")

from process_limits import scale_limits
from process_limits import xs_limit, xs_limit_ratio
from process_limits import print_limits

## type 1

def setUpMPL():
    mpl.rcParams['text.latex.preamble'] = [
           r'\usepackage{helvet}',    # set the normal font here
           r'\usepackage{sansmath}',  # load up the sansmath so that math -> helvet
           r'\sansmath'               # <- tricky! -- gotta actually tell tex to use!
           r'\DeclareSymbolFont{Greekletters}{OT1}{iwona}{m}{n}'
           r'\DeclareMathSymbol{\Delta}{\mathord}{Greekletters}{"01}'
    ]
    mpl.rc('text', usetex=True)

    plt.rcParams["figure.figsize"] = [10.0, 9.0]


def readConfig(configfile, options=None):
    options = options or {}

    with open(configfile, 'read') as cfile:
        try:
            return json.load(cfile)
        except Exception, e:
            print "Failed to load config from %s" % configfile
            raise e

    return None


def process_limits(csv_files,
                   outdir='xs_limits/',
                   scalings='xsecs/xsecs_tH_ttH_WWZZttbbgg_K6.csv',
                   printout=False,
                   writeout=False,
                   att='tot'):
    # Read signal strength limits from csv files
    assert(len(csv_files) == 3), "provide exactly 3 csv files with r limits"
    if not ('0p5' in csv_files[0] and
            '1p0' in csv_files[1] and
            '1p5' in csv_files[2]):
        print "WARNING, wrong order for csv files? %s" % csv_files
    df_limits = pd.read_csv(csv_files[0], sep=",", index_col=None)
    df_limits = df_limits.append(pd.read_csv(csv_files[1], sep=",", index_col=None), ignore_index=True)
    df_limits = df_limits.append(pd.read_csv(csv_files[2], sep=",", index_col=None), ignore_index=True)

    # Read the cross sections from csv files
    print "...reading scalings from %s" % scalings
    df_xsecs = pd.read_csv(scalings, sep=",", index_col=None)

    if printout:
        print_limits(df_limits, df_xsecs, att)

    df_xs_limits = pd.DataFrame()
    df_xs_limits['alpha'] = np.sign(df_limits.cf*df_limits.cv)*df_limits.cf**2/(df_limits.cf**2+df_limits.cv**2)
    df_xs_limits['alpha'] = df_xs_limits.alpha.round(4)
    df_xs_limits['ratio'] = df_limits.cf/df_limits.cv
    df_xs_limits['ratio'] = df_xs_limits.ratio.round(3)

    # Use our xs_limit function to store the limits
    scale_limits(df_xs_limits, df_limits, df_xsecs, att=att)

    # Remove the duplicate entries, sort, reset the index, and write to csv
    df_xs_limits.drop_duplicates(subset='ratio', inplace=True)
    df_xs_limits.sort_values(by='ratio', inplace=True)
    df_xs_limits.index = range(1,len(df_xs_limits)+1)

    if writeout:
        df_xs_limits.to_csv(os.path.join(outdir, "xs_limits.csv"))
    return df_xs_limits

def process(df, scalings=None, att='tot', scale_by_ratio=False):
    # Scale with a cross section?
    if scalings:
        print "...scaling limits with cross section (%s) from %s" % (att, scalings)
        df_xsecs = pd.read_csv(scalings, sep=",", index_col=0)
        scale_limits(df, df, df_xsecs, att=att, scale_by_ratio=scale_by_ratio)

    # Add in ratio and alpha columns if they're not there
    if not 'ratio' in df.columns:
        try:
            df['ratio'] = df.cf/df.cv
            df['ratio'] = df.ratio.round(3)
        except AttributeError:
            print "Failed to build ratio column in dataframe... check input file"

    return df

def plotLimits(cfg, outdir='plots/', tag=''):
    print "...reading observed limits from %s" % str(cfg['observed']['csv_files'])
    print "...reading cross sections from %s" % (cfg['xsecs'])

    # Fill dataframes
    df_obs = None
    if 'observed' in cfg:
        if 'csv_files' in cfg['observed']:
            files = [os.path.join(cfg['inputdir'], f) for f in cfg['observed']['csv_files']]
            df_obs = process_limits(files, scalings=cfg['xsecs'], att=cfg['xsec_att'])
        else:
            df_obs = pd.read_csv(cfg['observed']['csv_file'], sep=',', index_col=0)
            # FIXME Scale with xsec?
        df_obs = process(df_obs)
    
    df_exp = None
    if 'csv_files' in cfg['expected']:
        files = [os.path.join(cfg['inputdir'], f) for f in cfg['expected']['csv_files']]
        df_exp = process_limits(files, scalings=cfg['xsecs'], att=cfg['xsec_att'])
    else:
        df_exp = pd.read_csv(os.path.join(cfg['inputdir'], cfg['expected']['csv_file']))
        if cfg['expected'].get('scaling_file'):
            df_exp = process(df_exp, scalings=cfg['expected']['scaling_file'],
                                     att=cfg['expected'].get('scaling_att', 'tot'),
                                     scale_by_ratio=True)
        else:
            df_exp = process(df_exp)

    fig, ax = plt.subplots(1)

    # Configure axes
    ax.get_xaxis().set_tick_params(which='both', direction='in')
    ax.get_xaxis().set_major_locator(mpl.ticker.MultipleLocator(1.0))
    ax.get_xaxis().set_minor_locator(mpl.ticker.MultipleLocator(0.25))
    ax.set_xlim(-cfg['xmax'], cfg['xmax'])

    ax.set_ylim(0., cfg['ymax'])
    ax.set_yscale("linear", nonposy='clip')
    ax.get_yaxis().set_tick_params(which='both', direction='in')
    ax.get_yaxis().set_major_locator(mpl.ticker.MultipleLocator(cfg['y_major_ticks']))
    ax.get_yaxis().set_minor_locator(mpl.ticker.MultipleLocator(cfg['y_minor_ticks']))

    x = sorted(list(set(df_exp.ratio.values.tolist())))
    x2 = np.linspace(-6, 6, 100) # Evaluate spline at more points

    spline_twosigdown = splev(x2, splrep(x, df_exp.twosigdown, s=cfg['expected'].get('smoothing2s', 0.0)))
    spline_onesigdown = splev(x2, splrep(x, df_exp.onesigdown, s=cfg['expected'].get('smoothing1s', 0.0)))
    spline_exp        = splev(x2, splrep(x, df_exp.exp,        s=cfg['expected'].get('smoothing', 0.0)))
    spline_onesigup   = splev(x2, splrep(x, df_exp.onesigup,   s=cfg['expected'].get('smoothing1s', 0.0)))
    spline_twosigup   = splev(x2, splrep(x, df_exp.twosigup,   s=cfg['expected'].get('smoothing2s', 0.0)))

    # Plot limits with sigma error bands
    ax.plot(x2, spline_exp, "--", lw=2, color='black',zorder=4)
    ax.fill_between(x2, spline_onesigdown, spline_onesigup,   
                    facecolor=cfg['expected']['col1s'], alpha=0.8, zorder=0)
    ax.fill_between(x2, spline_twosigdown, spline_onesigdown, 
                    facecolor=cfg['expected']['col2s'], alpha=0.8, zorder=0)
    ax.fill_between(x2, spline_twosigup,   spline_onesigup,   
                    facecolor=cfg['expected']['col2s'], alpha=0.8, zorder=0)

    if df_obs is not None:
        ax.plot(df_obs.loc[df_obs.ratio<=cfg['xmax']].loc[df_obs.ratio>=-cfg['xmax']].ratio,
                df_obs.loc[df_obs.ratio<=cfg['xmax']].loc[df_obs.ratio>=-cfg['xmax']].obs,
                lw=2.0, c='black')
        ax.scatter(df_obs.loc[df_obs.ratio<=cfg['xmax']].loc[df_obs.ratio>=-cfg['xmax']].ratio,
                   df_obs.loc[df_obs.ratio<=cfg['xmax']].loc[df_obs.ratio>=-cfg['xmax']].obs,
                   marker='o', s=30, c='black', lw=2)

    # Cross section lines
    for entry in cfg['xsec_lines']:
        df = pd.read_csv(entry['csv_file'], sep=",", index_col=None)
        spl = splev(x2, splrep(x, df.loc[df.cv==1.0][entry['att']], s=entry['smoothing']))
        ax.plot(x2, spl, lw=entry['lw'], label='dummy', color=entry.get('color', 'black'),
                            linestyle=entry['ls'])


    # Set axis labels
    ax.set_xlabel(cfg['x_axis_label'], fontsize=24, labelpad=20)
    ax.set_ylabel(cfg['y_axis_label'], fontsize=24, labelpad=20)

    def print_text(x, y, text, fontsize=24, addbackground=True, bgalpha=0.8):
        if addbackground:
            ptext = plt.text(x, y, text, fontsize=fontsize, transform=ax.transAxes,
                                         backgroundcolor='white')
            ptext.set_bbox(dict(alpha=bgalpha, color='white'))
        else:
            ptext = plt.text(x, y, text, fontsize=fontsize, transform=ax.transAxes)

    # Print stuff
    print_text(0.03, 1.02, cfg["header_left"], 28, addbackground=False)
    print_text(0.65, 1.02, cfg["header_right"], addbackground=False)
    print_text(0.06, 0.92, cfg["tag1"], bgalpha=cfg["text_bg_alpha"])
    print_text(0.06, 0.86, cfg["tag2"], bgalpha=cfg["text_bg_alpha"])
    print_text(0.06, 0.78, cfg["tag3"], bgalpha=cfg["text_bg_alpha"])
    if "tag4" in cfg:
        print_text(0.06, 0.70, cfg["tag4"], bgalpha=cfg["text_bg_alpha"])


    # Cosmetics
    import matplotlib.patches as mpatches
    twosigpatch = mpatches.Patch(color=cfg['expected']['col2s'], label=r'$\pm2$ Standard Deviations')
    onesigpatch = mpatches.Patch(color=cfg['expected']['col1s'], label=r'$\pm1$ Standard Deviations')
    obsline = mpl.lines.Line2D([], [], color='black', linestyle='-',
                               label=r'Observed limit ($\sigma\times\mathrm{BR}$)', marker='.',
                               markersize=14, linewidth=2)
    explabel = r'Expected limit ($\sigma\times\mathrm{BR}$)'
    expline = mpl.lines.Line2D([], [], color='black', linestyle='--', label=explabel, linewidth=2.0)


    # Legend
    xsec_legentries = []
    for entry in cfg['xsec_lines']:
        xsec_legentries.append(mpl.lines.Line2D([], [], color=entry.get('color', 'black'),
                                                lw=entry.get('lw', 1.0),
                                                linestyle=entry.get('ls', '-'),
                                                label=entry['label']))

    legentries = [expline, onesigpatch, twosigpatch]
    if df_obs is not None:
        legentries.insert(0, obsline)
    legentries.extend(xsec_legentries)

    legend = plt.legend(handles=legentries, fontsize=18, frameon=True, loc='upper right', framealpha=1.0)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_linewidth(0)

    # Save to pdf/png
    outfile = os.path.join(outdir, cfg['name'])
    plt.savefig("%s.pdf"%outfile, bbox_inches='tight')
    plt.savefig("%s.png"%outfile, bbox_inches='tight', dpi=300)
    print "...saved plots in %s.pdf/.png" % outfile

    return 0

if __name__ == '__main__':
    from optparse import OptionParser
    usage = """%prog limits.dat"""
    parser = OptionParser(usage=usage)
    parser.add_option("-o","--outdir", dest="outdir",
                      type="string", default="plots/")
    parser.add_option("-t","--tag", dest="tag",
                      type="string", default="")
    parser.add_option("--defaultOptions", dest="defaultOptions",
                      type="string", default="defaults_limits.json",
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

    parser.add_option("--ymax", dest="ymax", type="float",
                      default=5.0, help="Y axis maximum")
    parser.add_option("--xmax", dest="xmax", type="float",
                      default=3.0, help="X axis maximum/minimum")
    parser.add_option("--y_major_ticks", dest="y_major_ticks", type="float",
                      default=0.5, help="Major ticks on y axis")
    parser.add_option("--y_minor_ticks", dest="y_minor_ticks", type="float",
                      default=-1.0, help="Minor ticks on y axis")
    (options, args) = parser.parse_args()
    if options.y_minor_ticks == -1.0:
        options.y_minor_ticks = options.y_major_ticks / 4.0

    try:
        os.system('mkdir -p %s' % options.outdir)
    except ValueError:
        pass

    setUpMPL()
    for ifile in args:
        if not os.path.exists(ifile):
            print "Ignoring %s" % ifile
            continue

        plotConfig = readConfig(options.defaultOptions, options=options)
        plotConfig.update(readConfig(ifile))

        # Do fixes here
        for attr in ['xmax', 'ymax', 'y_major_ticks', 'y_minor_ticks']:
            if getattr(options, attr, None) is not None:
                plotConfig[attr] = float(getattr(options, attr, plotConfig[attr]))
        for attr in ['inputdir', 'name', 'header_left']:
            if getattr(options, attr, None) is not None:
                plotConfig[attr] = str(getattr(options, attr, plotConfig[attr]))
        
        plotLimits(plotConfig, outdir=options.outdir, tag=options.tag)

    sys.exit(0)
