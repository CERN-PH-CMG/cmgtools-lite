#!/usr/bin/env python
import sys, os, pickle, re
import os.path as osp

xsections = None
def fillXSecsFromSamplesFile(filename):
    global xsections
    if not xsections:
        xsections = {}

    print "Filling cross sections from %s" % filename

    pattern = re.compile(r'.*?makeMCComponent\s*\(\s*\"([\w]*?)\"')
    with open(filename, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line.startswith('#'): continue

            # Remove trailing comments:
            if '#' in line:
                line = line[:line.find('#')].strip()

            match = pattern.match(line)
            if not match: continue
            sample_name = match.group(1)

            # Get the cross section
            xsec_string = line.rsplit(',',1)[1][:-1].strip()
            if re.match(r'[A-Za-z]', xsec_string):
                raise RuntimeError('Warning: invalid xsec_string: %s' % xsec_string)

            try:
                xsec = float(eval(xsec_string))
            except SyntaxError:
                raise RuntimeError("Error: unable to parse xsection string: %s, from line %s" % (xsec_string, line))
            # Check if we already know about this sample and the values are different
            if xsections.get(sample_name, xsec) != xsec:
                print 'Warning: ambiguous cross section for %s in %s' % (sample, filename)

            xsections[sample_name] = xsec

def checkIsData(dirname):
    with open(osp.join(dirname,'config.pck'), 'r') as cfile:
        config = pickle.load(cfile)
        try:
            return config.isData
        except AttributeError:
            return None

def getXSecFromConfig(dirname):
    with open(osp.join(dirname,'config.pck'), 'r') as cfile:
        config = pickle.load(cfile)
        try:
            return config.xSection
        except AttributeError:
            if config.isData:
                return None
            else: raise

def getNEvents(dirname):
    with open(osp.join(dirname,
                       'skimAnalyzerCount',
                       'SkimReport.pck'), 'r') as cfile:
        report = pickle.load(cfile)
        return dict(report)['All Events']

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
    parser.add_option("--samplesfile",
                      default=osp.join(os.environ.get('CMSSW_BASE',''),
                                       'src/CMGTools/RootTools/python/samples',
                                       'samples_13TeV_RunIISummer16MiniAODv2.py'),
                      action="store", dest="samplesfile",
                      help=("Cache for xsec weights [default: %default]"))
    (options, args) = parser.parse_args()

    try:
        with open(options.cachefile, 'r') as cachefile:
            xsecweights = pickle.load(cachefile)
            print ('>>> Read xsecweights from cache (%s)' % options.cachefile)
    except IOError:
        xsecweights = {}

    fillXSecsFromSamplesFile(options.samplesfile)

    notfound = []
    for procdir in os.listdir(args[0]):
        # try:
        nevs = getNEvents(osp.join(args[0],procdir))
        xsec = xsections.get(procdir, None)
        if xsec == None:
            try:
                xsec = getXSecFromConfig(osp.join(args[0],procdir))
            except IOError: pass
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
            if not procdir in xsections and '2016' in procdir:
                xsecweights[procdir] = 1.0
        # except IOError: pass

        if not procdir in xsecweights:
            notfound.append(procdir)

    if notfound:
        print "No weights found for %d samples:" % len(notfound), notfound

    with open(options.cachefile, 'w') as cachefile:
        pickle.dump(xsecweights, cachefile, pickle.HIGHEST_PROTOCOL)
        print ('>>> Wrote xsecweights to cache (%s)' % options.cachefile)
