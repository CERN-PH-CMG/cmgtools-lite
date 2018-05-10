#!/bin/env python 

import ROOT
import sys,os,re

if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser(usage='%prog [options] shapes.root newcard.txt')
    parser.add_option('--sp', dest='selectProcesses', type="string", default=[], action="append", help="Processes to consider (comma-separated list of regexp, can specify multiple ones)");
    (options, args) = parser.parse_args()

    binname = 'test_bin'

    procsAndRates = {}
    shapes_f = ROOT.TFile.Open(args[0])
    for e in shapes_f.GetListOfKeys() :
        name=e.GetName()
        obj=e.ReadObj()
        if (not name.endswith('Up') and not name.endswith('Down')):
            pname = '_'.join(name.split('_')[1:])
            procsAndRates[pname] = obj.Integral()
    shapes_f.Close()

    wantProcs = {}
    for pname,rate in procsAndRates.iteritems():
        for p1 in options.selectProcesses:
            for p in p1.split(","):
                if re.match(p+"$", pname): wantProcs[pname] = rate
    procs = wantProcs.keys()

    asimov_rate = sum([r for p,r in wantProcs.iteritems()])

    datacard = open(args[1],'w')
    datacard.write("shapes *        * {shapes_file} x_$PROCESS x_$PROCESS_$SYSTEMATIC\n".format(shapes_file=args[0]))
    datacard.write("bin "+binname+"\n")
    datacard.write("observation {obs}\n".format(obs=asimov_rate))
    datacard.write("##----------------------------------\n")
    klen = max([7, len(binname)]+[len(p) for p in procs])
    kpatt = " %%%ds "  % klen
    fpatt = " %%%d.%df " % (klen,3)
    datacard.write("##----------------------------------\n")
    datacard.write('bin             '+(" ".join([kpatt % binname  for p in procs]))+"\n")
    datacard.write('process         '+(" ".join([kpatt % p        for p in procs]))+"\n")
    datacard.write('process         '+(" ".join([kpatt % str(iproc+1) for iproc,p in enumerate(procs)]))+"\n")
    datacard.write('rate            '+(" ".join([fpatt % wantProcs[p] for p in procs]))+"\n")
    datacard.write('##----------------------------------\n')
    datacard.write('lumi lnN        '+(" ".join([kpatt % ('-' if 'data' in p else '1.026') for p in procs]))+"\n")
    
    print "Written card to ",args[1],"\n"
