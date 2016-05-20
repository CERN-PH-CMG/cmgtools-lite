#!/usr/bin/env python
import sys, os, pickle
import os.path as osp

def checkIsData(dirname):
    with open(osp.join(dirname,'config.pck'), 'r') as cfile:
        config = pickle.load(cfile)
        try:
            return config.isData
        except AttributeError:
            return None

def getNEvents(dirname):
    with open(osp.join(dirname,
                       'skimAnalyzerCount',
                       'SkimReport.pck'), 'r') as cfile:
        report = pickle.load(cfile)
        return dict(report)['All Events']

def getXSec(dirname):
    with open(osp.join(dirname,'config.pck'), 'r') as cfile:
        config = pickle.load(cfile)
        try:
            return config.xSection
        except AttributeError:
            return None


if __name__ == '__main__':
    from optparse import OptionParser
    usage = """
    Collect xsec and number of processed events from config.pck and
    skimAnalyzerCount/SkimReport.pck files in all subdirectories of
    the first argument. Store them as a dictionary of
       subdirname -> xsec/nevs
    in a cachefile (.xsecweights.pck by default). If cachefile exists,
    extend the entries or check for conflict.

    Ignore everything that goes wrong, replace by new value in case
    there is a conflict. If it's data, set the weight to 1.

    xsecs are read in [pb] and scaled to [fb] such that the resulting
    weight has to be multiplied by the integrated luminosity in fb^-1.

    %prog [options] treeDir

    """
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--cachefile", default=".xsecweights.pck",
                      action="store", dest="cachefile",
                      help=("Cache for xsec weights [default: %default]"))
    (options, args) = parser.parse_args()

    try:
        with open(options.cachefile, 'r') as cachefile:
            xsecweights = pickle.load(cachefile)
            print ('>>> Read xsecweights from cache (%s)' % options.cachefile)
    except IOError:
        xsecweights = {}

    for procdir in os.listdir(args[0]):
        try:
            nevs = getNEvents(  osp.join(args[0],procdir))
            xsec = getXSec(     osp.join(args[0],procdir))
            try:
                newweight = 1000*float(xsec)/float(nevs)
                oldweight = xsecweights.setdefault(procdir,newweight)
                if not oldweight == newweight:
                    print '...replacing %-36s'% procdir,
                    print 'old:', oldweight,
                    print 'new:', newweight, '(%f/%d)'%(xsec,nevs)
                    xsecweights[procdir] = newweight
                else:
                    print '...adding %-36s' % procdir,
                    print '  ', newweight, '(%f/%d)'%(xsec,nevs)
            except TypeError:
                if checkIsData( osp.join(args[0],procdir)):
                    xsecweights[procdir] = 1.0
        except IOError: pass

    with open(options.cachefile, 'w') as cachefile:
        pickle.dump(xsecweights, cachefile, pickle.HIGHEST_PROTOCOL)
        print ('>>> Wrote xsecweights to cache (%s)' % options.cachefile)
