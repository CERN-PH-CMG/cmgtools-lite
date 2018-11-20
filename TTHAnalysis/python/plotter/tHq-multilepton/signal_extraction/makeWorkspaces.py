#!/usr/bin/env python
import os
import sys
import time
import shlex
import multiprocessing
from subprocess import Popen, PIPE


def makeWorkspace(card, outname, options, verbose=False):
    starttime = time.time()
    cmd = "text2workspace.py"
    cmd += " %s" % options
    cmd += " -o %s" % outname
    cmd += " %s" % card

    if verbose: 
        print 40*'-'
        print cmd
        print 40*'-'

    try:
        p = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
        comboutput = p.communicate()[0]
    except OSError:
        print "text2workspace.py not known. Try this: cd /afs/cern.ch/user/s/stiegerb/combine/ ; cmsenv ; cd -"
        comboutput = None

    elapsed = time.time() - starttime
    if os.path.isfile(outname):
        return " %-30s \033[92mDone\033[0m in %.2f min" % (card, elapsed/60.)
    else:
        return " %-30s \033[91mFailed\033[0m in %.2f min" % (card, elapsed/60.)


if __name__ == '__main__':
    from optparse import OptionParser
    usage = """
    %prog [options] card1.txt card2.txt
    %prog [options] card_*.txt

    Call text2workspace.py on a bunch of cards.

    Note that you need to have 'combine' in your path. Try:
    cd /afs/cern.ch/user/s/stiegerb/combine/ ; cmsenv ; cd -
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-b","--baseModel", dest="baseModel", type="string",
                      default="HiggsAnalysis.CombinedLimit.LHCHCGModels",
                      help="Base model to use, e.g. 'HiggsAnalysis.CombinedLimit.LHCHCGModels'")
    parser.add_option("-m","--model", dest="model", type="string", default="K7",
                      help="Specific model to use, e.g. 'K7'")
    parser.add_option("-t","--tag", dest="tag", type="string", default="",
                      help="Some additional tag to add to output files")
    parser.add_option("-v","--verbose", dest="verbose", action='store_true',
                      help="Print the combine command that is run")
    parser.add_option("-j","--jobs", dest="jobs", type="int", default=1,
                      help="Number of jobs to run in parallel")
    (options, args) = parser.parse_args()

    pool = multiprocessing.Pool(processes=options.jobs)

    futures = []
    starttime = time.time()
    print 'Using model %s:\033[1m%s \033[0m' % (options.baseModel, options.model)
    for card in args:
        if not (os.path.isfile(card) and card.endswith('.txt')):
            print "... ignoring", card
            continue

        copts = "-P %s:%s -m 125" % (options.baseModel, options.model)

        trunk = os.path.basename(card).replace('.card.txt', '')
        outname = "ws_%s_%s" % (trunk, options.model)
        if options.tag:
            outname += '_%s' % options.tag
        outname += '.card.root'

        future = pool.apply_async(makeWorkspace, (card,
                                                  outname,
                                                  copts,
                                                  options.verbose))
        futures.append((card, future))

    for n, (card, future) in enumerate(futures):
        printout = future.get()
        print "%s (%d/%d)" % (printout, n, len(futures))

    print " \033[1m \033[92mAll Done\033[0m in %.2f min" % ((time.time()-starttime)/60.)

