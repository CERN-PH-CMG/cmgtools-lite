import numpy as np
import pandas as pd
from itertools import product
cvs = [0.5, 1.0, 1.5]
cts = [-3, -2, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0.0,
       0.25, 0.50, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]
points = points = sorted(list(product(cvs, cts)))

def alpha(ct,cv):
    """Calculate ct^2/(ct^2+cv^2) * sign(ct/cv)"""
    return float(np.sign(ct/cv)*ct**2/((ct**2+cv**2)))

alphas = sorted(list(set([alpha(ct,cv) for cv,ct in points ] )))
ratios = sorted(list(set([ct/cv for cv,ct in points])))
apoints = {alpha(ct,cv) : [(v,t) for v,t in points if alpha(t,v) == alpha(ct,cv)] for cv,ct in points}

def print_table(funcs, linepat=" %5.4f (%5.4f) "):
    """
    Print a table of rows corresponding to unique alpha/ratio values and
    columns corresponding to different cv values.
    `funcs` are callables taking two argument (ct, cv) and returning floats.
    `linepat` is a string format taking as many numbers as funcs are defined
    """
    filler = len(linepat % tuple([1.0 for _ in range(len(funcs))]))
    for a,r in zip(alphas,ratios):
        line = "%6.3f %6.3f: " % (a,r)
        for cv in cvs:
            if cv in [v for v,t in apoints[a]]:
                ct = [t for v,t in apoints[a] if v == cv]
                assert(len(ct) == 1)
                ct = ct[0]
                vals = tuple([f(ct,cv) for f in funcs])
                try:
                    line += linepat % vals
                except TypeError:
                    print "Error parsing line: %s" % repr(vals)
            else:
                line += filler*" "
        print line


def read_dataframe(ct, cv, df=None, att=None):
    """
    Read out an attribute from a dataframe at given ct, cv value
    Use with functools.partial to create a function of ct and cv
    to give to print_table
    """
    result = None
    try:
        result = df.loc[df.cv==cv].loc[df.ct.round(3)==ct].get(att)
    except AttributeError:
        # Some call it cf instead of ct
        result = df.loc[df.cv==cv].loc[df.cf.round(3)==ct].get(att)
    return result

def read_dataframe_ratio(ct, cv, df=None, att1=None, att2=None):
    """
    Read out two attributes from a dataframe at given ct, cv value
    Use with functools.partial to create a function of ct and cv
    to give to print_table
    Return the ratio of the two atts
    """
    return read_dataframe(ct,cv,df=df,att=att1)/read_dataframe(ct,cv,df=df,att=att2)
