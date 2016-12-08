"""Efficiently draw multiple histograms with one loop over all events in a TTree

This script injects a MultiDraw method into TTree when it is imported.

Stolen from:
https://github.com/pwaller/minty/blob/master/minty/junk/MultiDraw.py
"""
import os

from ROOT import gROOT, gSystem, gDirectory, TObject, TTree, TObjArray, TTreeFormula,\
    TH1D, SetOwnership, TTreeFormulaManager


def MakeTObjArray(theList):
    """Turn a python iterable into a ROOT TObjArray"""

    result = TObjArray()
    result.SetOwner()

    # Make PyROOT give up ownership of the things that are being placed in the
    # TObjArary. They get deleted because of result.SetOwner()
    for item in theList:
        SetOwnership(item, False)
        result.Add(item)

    return result

import re


def MultiDraw(self, Formulae, CommonWeight="1"):
    """Draws many histograms in one loop over a tree.

        Instead of:
        MyTree.Draw( "nlcts >> a(100, -1, 1)", "weightA" )
        MyTree.Draw( "nlcts >> b(100, -1, 1)", "weightB" )

        Do:    
        MyTree.MultiDraw( ( "nlcts >> a(100, -1, 1)", "weightA" ),
                          ( "nlcts >> b(100, -1, 1)", "weightB" ) )

        This is significantly faster when there are many histograms to be drawn.
        The first parameter, CommonWeight, decides a weight given to all
        histograms.

        An arbitrary number of additional histograms may be specified. They can 
        either be specified with just a string containing the formula to be 
        drawn, the histogram name and bin configuration. 

        Alternatively it can be a tuple, with  said string, and an additional
        string specifying the weight to be applied to that histogram only.
    """

    if type(CommonWeight) == tuple:
        Formulae = (CommonWeight, ) + Formulae
        CommonWeight = "1"

    results, formulae, weights = [], [], []

    lastFormula, lastWeight = None, None

    # A weight common to everything being drawn
    CommonWeightFormula = TTreeFormula("CommonWeight", CommonWeight, self)
    CommonWeightFormula.SetQuickLoad(True)
    if not CommonWeightFormula.GetTree():
        raise RuntimeError("TTreeFormula didn't compile: " + CommonWeight)

    hists = {}

    for i, origFormula in enumerate(Formulae):
        # print "Have an origFormula", origFormula

        # Expand out origFormula and weight, otherwise just use weight of 1.
        if type(origFormula) == tuple:
            origFormula, weight = origFormula
        else:
            origFormula, weight = origFormula, "1"

        # print origFormula, weight

        # Pluck out histogram name and arguments
        match = re.match(r"^(.*?)\s*>>\s*(.*?)\s*\(\s*(.*?)\s*\)$", origFormula)
        if match:

            formula, name, arguments = match.groups()
            arguments = re.split(",\s*", arguments)

            bins, minX, maxX = arguments
            bins, minX, maxX = int(bins), float(minX), float(maxX)

            # Create histogram with name and arguments
            hist = TH1D(name, name, bins, minX, maxX)
            hist.Sumw2()
        else:
            # without arguments
            match = re.match(r"^(.*?)\s*>>\s*(.*?)\s*$", origFormula)
            if not match:
                raise RuntimeError("MultiDraw: Couldn't parse formula: '%s'" % origFormula)

            formula, name = match.groups()
            # print formula, name

            if name.startswith("+") and name[1:] in hists:
                # Drawing additionally into a histogram
                hist = hists[name[1:]]
            else:
                # name = name[1:] # JAN: ???
                hist = gDirectory.Get(name)
                if not hist:
                    raise RuntimeError("MultiDraw: Couldn't find histogram to fill '%s' in current directory." % name)

        if name not in hists:
            hists[name] = hist

        results.append(hist)

        # The following two 'if' clauses check that the next formula is different
        # to the previous one. If it is not, we add an ordinary TObject.
        # Then, the dynamic cast in MultiDraw.cxx fails, giving 'NULL', and
        # The previous value is used. This saves the recomputing of identical values

        if formula != lastFormula:
            f = TTreeFormula("formula%i" % i, formula, self)
            if not f.GetTree():
                raise RuntimeError("TTreeFormula didn't compile: " + formula)
            f.SetQuickLoad(True)
            formulae.append(f)
        else:
            formulae.append(TObject())

        if weight != lastWeight:
            f = TTreeFormula("weight%i" % i, weight, self)
            if not f.GetTree():
                raise RuntimeError("TTreeFormula didn't compile: " + formula)
            f.SetQuickLoad(True)
            weights.append(f)
        else:
            weights.append(TObject())

        lastFormula, lastWeight = formula, weight

    # Only compile MultiDraw once
    try:
        from ROOT import MultiDraw as _MultiDraw
    except ImportError:
        # gROOT.ProcessLine(".L %sMultiDraw.cxx+O" % "./")
        if "/sMultiDraw_cc.so" not in gSystem.GetLibraries(): 
            gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/MultiDraw.cc+" % os.environ['CMSSW_BASE']);
        from ROOT import MultiDraw as _MultiDraw

    # from time import time
    # start = time()

    # Ensure that formulae are told when tree changes
    fManager = TTreeFormulaManager()
    for formula in formulae + weights + [CommonWeightFormula, ]:
        if type(formula) == TTreeFormula:
            fManager.Add(formula)

    fManager.Sync()
    self.SetNotify(fManager)

    # Draw everything!
    _MultiDraw(self, CommonWeightFormula,
               MakeTObjArray(formulae),
               MakeTObjArray(weights),
               MakeTObjArray(results),
               len(Formulae))

    # print "Took %.2fs" % (time() - start), " "*20

    return results

TTree.MultiDraw = MultiDraw
