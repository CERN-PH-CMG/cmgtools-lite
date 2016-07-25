import cPickle, re, optparse, os, os.path

def filterWithFilter(files, runFilter):
    ret = []
    pat = (r".*/store/data/\w+/\w+/\w+/PromptReco-v\d+/000/(\d\d\d)/(\d\d\d)/\w+/\w+-\w+-\w+-\w+-\w+.root.*")
    for fname in files:
        m = re.match(pat, fname)
        if not m: raise RuntimeError, "File %s does not match the PromptReco path specification" % fname
        run = int(m.group(1)+m.group(2))
        if runFilter(run): ret.append(fname)
    return ret

def filterWithRange(files, run_range):
    return filterWithFilter(files, lambda run : run_range[0] <= run and run <= run_range[1])
def filterWithCollection(files, runs):
    return filterWithFilter(files, lambda run : (run in runs))
def filterWithJSON(files, jsonfile):
    import json
    goodruns = map(int, json.load(open(jsonfile,'r')).keys())
    return filterWithCollection(files, goodruns)

def filterComponent(comp,verbose=0):
    nfiles = len(comp.files)
    if comp.run_range and comp.run_range[0] != -1 and comp.run_range[1] != -1: 
        comp.files = filterWithRange(comp.files, comp.run_range)
        if verbose > 2 or ((len(comp.files) != nfiles) and verbose > 1):
            print "Component %s reduced from %d files to %d files by run range %s" % (comp.name, nfiles, len(comp.files), comp.run_range)
    if comp.json:
        comp.files = filterWithJSON(comp.files, comp.json)
        if verbose > 2 or ((len(comp.files) != nfiles) and verbose > 1):
            print "Component %s reduced from %d files to %d files by JSON %s" % (comp.name, nfiles, len(comp.files), comp.json)
    if verbose == 2 or (verbose == 1 and len(comp.files) != nfiles):
        print "Component %s reduced from %d files to %d files" % (comp.name, nfiles, len(comp.files))
    return comp

def filterPickled(filename,json=None,run_range=None,verbose=1):
    original_filename = filename
    if os.path.isdir(filename):
        if os.path.exists(filename+"/config.pck"):
            filename += "/config.pck"
    if not os.path.exists(filename):
        raise RuntimeError, "Filename '%s' does not exist" % filename
    if not os.path.exists(filename+".sav"):
        if verbose >= 2: print "Making backup in %s.sav" % filename
        os.system("cp %s %s.sav" % (filename, filename))
    fin = open(filename+".sav")
    comp = cPickle.load(fin)
    fin.close()
    if verbose: print "Loaded %s (%s) - %d files." % (filename, comp.name, len(comp.files))
    if json: 
        if verbose >= 2:
           print "Overriding json from %s to %s" % (comp.json, json)
        comp.json = json
    if run_range: 
        if verbose >= 2:
            print "Overriding run_range from %s to %s" % (comp.run_range, run_range)
        comp.run_range = run_range
    comp = filterComponent(comp,options.verbose)
    fout = open(filename, 'w')
    cPickle.dump(comp,fout)
    fout.close()
    if len(comp.files) == 0:
        os.system("mv -v %s %s.empty" % (original_filename, original_filename))

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-v", dest="verbose", type="int", default=1, help="verbosity (default = 1)")
    parser.add_option("-j", "--json", dest="json", type="string", default=None, help="JSON to apply (overriding the one in the component)")
    parser.add_option("-r", "--run-range", dest="run_range", type="int", nargs=2, default=None, help="JSON to apply (overriding the one in the component)")
    (options, args) = parser.parse_args()
    for a in args:
        filterPickled(a, json=options.json, run_range=options.run_range, verbose = options.verbose)
