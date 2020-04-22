#!/usr/bin/env python
import os
import sys
import numpy as np
import pandas as pd

from functools import partial

from ctcv_helper import print_table
from ctcv_helper import read_dataframe

## type 1

def xs_limit(ct, cv, df_xsecs, df_limits, limval='exp', att='tot'):
    """Multiply a limit by the cross section for cv=1.0, ct=ct/cv"""
    xsec = read_dataframe(round(ct / cv, 3), 1.0, df=df_xsecs, att=att)
    lim = read_dataframe(ct, cv, df=df_limits, att=limval)
    return float(xsec) * float(lim)


def xs_limit_ratio(ratio, df_xsecs, df_limits, limval='exp', att='tot'):
    # Take the cross section for cv=1.0, ct=ct/cv
    ratio = round(ratio, 3)
    xsec = read_dataframe(ratio, 1.0, df=df_xsecs, att=att)
    lim = getattr(df_limits.loc[df_limits.ratio.round(3)==ratio], limval)

    try:
        xs_lim = float(xsec) * float(lim)
    except TypeError as e:
        print ratio
        print xsec
        print lim
        raise e

    return xs_lim


def print_limits(df_limits, df_xsecs, att='tot'):
    print "----------------------------------------------------------------"
    print "   signal strength limits: "
    print " alpha  Ct/CV       CV=0.5           CV=1.0           CV=1.5"
    print "                  exp    (obs)    exp    (obs)    exp    (obs)"
    print_table([partial(read_dataframe, df=df_limits, att='exp'),
                 partial(read_dataframe, df=df_limits, att='obs')],
                linepat=" %6.3f (%6.3f)")

    print "----------------------------------------------------------------"
    print "   sigma x BR limits: "
    print " alpha  Ct/CV       CV=0.5           CV=1.0           CV=1.5"
    print "                  exp    (obs)    exp    (obs)    exp    (obs)"
    print_table([partial(xs_limit, df_xsecs=df_xsecs, df_limits=df_limits, limval='exp', att=att),
                 partial(xs_limit, df_xsecs=df_xsecs, df_limits=df_limits, limval='obs', att=att)],
                linepat=" %6.3f (%6.3f)")
    print "----------------------------------------------------------------"


def scale_limits(df_xs_limits, df_limits, df_xsecs, att='tot', scale_by_ratio=False):
    """Scale the limits in a dataframe by the cross sections in another"""
    for limval in ['twosigdown', 'onesigdown', 'exp', 'onesigup', 'twosigup', 'obs']:
        if not limval in df_limits.columns:
            continue

        if not scale_by_ratio:
            df_xs_limits[limval] = np.vectorize(partial(xs_limit,
                                                        df_xsecs=df_xsecs,
                                                        df_limits=df_limits,
                                                        limval=limval,
                                                        att=att))(df_limits.cf, df_limits.cv)
        if scale_by_ratio:
            df_xs_limits[limval] = np.vectorize(partial(xs_limit_ratio,
                                                        df_xsecs=df_xsecs,
                                                        df_limits=df_limits,
                                                        limval=limval,
                                                        att=att))(df_limits.ratio)


def process_limits(file_cv05, file_cv10, file_cv15,
                   outdir='xs_limits/',
                   scalings='xsecs/xsecs_tH_ttH_WWZZttbbgg_K6.csv',
                   printout=False,
                   att='tot'):
    # Read signal strength limits from csv files
    df_limits = pd.read_csv(file_cv05, sep=",", index_col=None)
    df_limits = df_limits.append(pd.read_csv(file_cv10, sep=",", index_col=None), ignore_index=True)
    df_limits = df_limits.append(pd.read_csv(file_cv15, sep=",", index_col=None), ignore_index=True)

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
    df_xs_limits.to_csv(os.path.join(outdir, "xs_limits.csv"))


if __name__ == '__main__':
    from optparse import OptionParser
    usage = """%prog limits.dat"""
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--outdir", dest="outdir",
                      type="string", default="xs_limits/")
    parser.add_option("--att", dest="att",
                      type="string", default="tot",
                      help="Which xsection to use ('tot' or 'hbb')")
    parser.add_option("--scalings", dest="scalings",
                      type="string", default="xsecs/xsecs_tH_ttH_WWZZttbbgg_K6.csv",
                      help="Which file to use for scalings")
    (options, args) = parser.parse_args()

    try:
        os.system('mkdir -p %s' % options.outdir)
    except ValueError:
        pass

    assert(all([os.path.exists(f) for f in args[:3]])), 'need 3 limit files (kV 0.5, 1.0, 1.5)'

    process_limits(args[0], args[1], args[2],
                   options.outdir,
                   printout=True,
                   scalings=options.scalings,
                   att=options.att)

    sys.exit(0)
