#!/usr/bin/env python                                                                                                                                                                                              
import sys, os
import numpy as np
import ROOT  as r
import pickle
from tabulate import tabulate
sys.path.append(os.environ['CMSSW_BASE']+ '/CMGTools/python/plotter/ttH-modules/')
from signalExtractionHarvestingConfigs import regionMappingFortables
from signalExtractionHarvesting        import readNominalAndToys, stackByMapping, tableToNumbers, buildRms, makeTable

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--reloadToys', dest='reloadToys',action='store_true',default=False)
parser.add_option('--redoStack', dest='redoStack',action='store_true',default=False)
parser.add_option('--fittype', dest='fittype',type="string",default="fit_s")
parser.add_option('--fitdiagnostics', dest='fitdiagnostics',type="string",default="/nfs/fanae/user/sscruz/Combine/CMSSW_10_2_13/src/postfit_tests/fitDiagnostics_shapes_combine_combo_ttHmultilep_cminDefaultMinimizerStrategy0robustHesse_MINIMIZER_analytic_fixXtrg.root")
parser.add_option('--toys', dest='toys',type="string",default="/nfs/fanae/user/sscruz/Combine/CMSSW_10_2_13/src/postfit_tests/toys/toys_{fit}{toy}.root")
parser.add_option('--region', dest='region',default=[], action='append')

(options, args) = parser.parse_args()

if options.redoStack:
    results,data=readNominalAndToys(options.fitdiagnostics, options.toys,fit=options.fittype,readFromPickle=(not options.reloadToys))
else:
    results=None; data=None

results,data=stackByMapping( results, data, regionMappingFortables, 'stack_paper', readFromPickle=(not options.redoStack))
tableToNumbers( results, data, regionMappingFortables)
buildRms( results, data, regionMappingFortables)
if not len(options.region):
    for cat in regionMappingFortables:
        options.region.append(cat)
makeTable(options.region, results, data)


