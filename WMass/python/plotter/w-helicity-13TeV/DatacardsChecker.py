#!/usr/bin/env python
# python w-helicity-13TeV/DatacardsChecker.py -c cards/helicity_2018_03_06_testpdf el

import os.path
import sys,ROOT,os
ROOT.gROOT.SetBatch(True)

class CardsChecker:
    def __init__(self, card_dir, channel, nRapBins, nPdfBins, options):
        self.card_dir = card_dir
        self.options = options
        self.datacards = {}
        self.cardinputs = {}
        for charge in ["plus","minus"]:
            for r in xrange(nRapBins):
                for ipdf in xrange(1,nPdfBins+1):
                    key = "W{charge}_{channel}_Ybin_{bin}_pdf{eigen}".format(charge=charge,channel=channel,bin=r,eigen=ipdf)
                    f_txt = key+".card.txt" 
                    f_root = key+".input.root"
                    self.datacards[key] = f_txt
                    self.cardinputs[key] = f_root

    def checkCards(self):
        resubcmds = {}
        for key,dc in self.datacards.iteritems():
            if not os.path.exists(self.card_dir+"/"+dc): 
                if self.options.verbose>1: print "# datacard ",dc," is not present in ",self.card_dir
                resubcmds[key] = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}".format(
                    queue=self.options.queue, dir="/".join([os.getcwd(),self.card_dir,"jobs"]), logfile=key+"_resub.log", srcfile=key+".sh")
        for key,f in self.cardinputs.iteritems():
            f_ok = True
            if not os.path.exists(self.card_dir+"/"+f): 
                if self.options.verbose>1: print "# input root file ",f," is not present in ",self.card_dir
                f_ok = False
            else: 
                if self.options.checkZombies:
                    tfile = ROOT.TFile.Open(self.card_dir+"/"+f)
                    if not tfile or tfile.IsZombie():
                        if self.options.verbose>1: print "# ",f, " is Zombie"
                        f_ok = False
            if not f_ok: 
                resubcmds[key] = "bsub -q {queue} -o {dir}/{logfile} {dir}/{srcfile}".format(
                    queue=self.options.queue, dir="/".join([os.getcwd(),self.card_dir,"jobs"]), logfile=key+"_resub.log", srcfile=key+".sh")
        return resubcmds

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog dir channel (el,mu) [nRapBins] [nPdfBins]")
    parser.add_option("-c", "--check-cards", dest="checkCards", default=False, action="store_true", help="Check if there are all the datacards and ROOT files");
    parser.add_option("-z", "--check-zombies", dest="checkZombies", default=False, action="store_true", help="Check if all the ROOT files are sane");
    parser.add_option("-q", "--queue", dest="queue", type="string", default="2nd", help="choose the queue to submit batch jobs (default is 8nh)");
    parser.add_option("-v", "--verbose", dest="verbose", default=0, type=int, help="Degree of verbosity (0=default prints only the resubmit commands)");
    (options, args) = parser.parse_args()

    if options.checkCards:
        if len(args)<2: print "needed inputs: datacards_dir channel "; quit()
        if args[1] not in ["el","mu"]: print "channel must be either 'mu' or 'el'"; quit()
        nRapBins = args[2] if len(args)>2 else 13
        nPdfBins = args[3] if len(args)>3 else 60
        cc = CardsChecker(args[0],args[1], nRapBins, nPdfBins, options)
        result = cc.checkCards()
        if len(result)==0: print "All cards are GOOD."
        else: 
            keys = result.keys()
            keys.sort()
            for k in keys: print result[k]

