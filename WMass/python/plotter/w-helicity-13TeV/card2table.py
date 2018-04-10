#!/usr/bin/env python
# USAGE: python w-helicity-13TeV/card2table.py Wel_plus_shapes.root

from math import *
import re
import os, os.path
from array import array

## safe batch mode
import sys
args = sys.argv[:]
sys.argv = ['-b']
import ROOT
sys.argv = args
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True

def formatProc(proc):
    x = proc.replace('x_','')
    x = x.replace('W_left','$W_L$')
    x = x.replace('W_right','$W_R$')
    if 'long' in proc: x = '$W_0$'
    x = x.replace('TauDecaysW','$W\\to\\tau\\nu$')
    x = x.replace('data_fakes','fakes')
    x = x.replace('data_obs','data')
    return x

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] shapes.root")
    (options, args) = parser.parse_args()

    shapes_f = args[0]
    tf = ROOT.TFile.Open(shapes_f)
    histos={}
    charge=None
    for e in tf.GetListOfKeys() :
        name=e.GetName()
        obj=e.ReadObj()
        if not charge and 'Wplus' in name: charge='plus'
        if not charge and 'Wminus' in name: charge='minus'
        if (not name.endswith('Down')) and (not name.endswith('Up')):
            histos[name] = obj
            histos[name].SetDirectory(None)
    tf.Close()

    # backgrounds
    bkgs = dict(filter(lambda (k,v): not re.match('.*(W{ch}_left|W{ch}_right).*'.format(ch=charge),k), histos.iteritems()))
    yields=dict((k,h.Integral()) for k,h in bkgs.iteritems())

    # W boson
    W_left = dict(filter(lambda (k,v): re.match('x_W%s_left'%charge,k),histos.iteritems()))
    W_right = dict(filter(lambda (k,v): re.match('x_W%s_right'%charge,k),histos.iteritems()))
    yields["W_left"] = sum(h.Integral() for k,h in W_left.iteritems())
    yields["W_right"] = sum(h.Integral() for k,h in W_right.iteritems())

    data = ["x_data_obs"]
    signal = ["W_left","W_right","x_W%s_long"%charge]
    others = [k for k,h in yields.iteritems() if not any(sp in k for sp in signal+data)]
    sorted_procs = signal+others+data
    print " & ".join(formatProc(p) for p in sorted_procs)," \\\\"
    print " & ".join("%.0f" % yields[p] for p in sorted_procs)," \\\\"
    print " ==> Total signal = %.0f M" % sum(y/1.e+6 for k,y in yields.iteritems() if any(sp in k for sp in signal))
    print " ==> Total bkg =  %.0f M" % sum(y/1.e+6 for k,y in yields.iteritems() if not any(sp in k for sp in signal+data))
