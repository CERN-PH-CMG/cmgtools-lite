#!/usr/bin/env python
# python w-helicity-13TeV/DatacardsChecker.py -c cards/helicity_2018_03_06_testpdf el

import os.path
import sys,ROOT,os
ROOT.gROOT.SetBatch(True)

class CardsChecker:
    def __init__(self, card_dir, options):
        self.card_dir = card_dir
        self.options = options
        self.datacards = {}
        self.cardinputs = {}
        self.pycmd = {}
        for f in os.listdir(card_dir+'/jobs/'):
            if not f.endswith('.sh'): 
                continue
            key = f.replace('.sh','')
            tmp_f = open(card_dir+'/jobs/'+f, 'r')
            lines = tmp_f.readlines()
            self.headerlines =[i for i in lines if not 'python ' in i]
            pycmds =[i for i in lines if 'python ' in i]
            for cmd in pycmds:
                tmp_name = cmd.split(' -o ')[1].split()[0]
                f_txt = tmp_name+'.card.txt'
                f_root = tmp_name+'.input.root'
                self.datacards[tmp_name] = f_txt
                self.cardinputs[tmp_name] = f_root
                self.pycmd[tmp_name] = cmd
        print '## Expecting {n} cards and rootfiles'.format(n=len(self.datacards))

    def makeResubFile(self, key):
        resubdir = self.card_dir+'/jobs/resub/'
        os.system('mkdir -p '+resubdir)
        tmp_file_name = resubdir+'/'+key+'_resub.sh'
        tmp_file = open(tmp_file_name,'w')
        
        for i in self.headerlines:
            tmp_file.write(i)
        tmp_file.write(self.pycmd[key])
        return tmp_file_name


    def checkCards(self):
        resubcmds = {}
        for key,dc in self.datacards.iteritems():
            if not os.path.exists(self.card_dir+'/'+dc): 
                if self.options.verbose>1: print '# datacard ',dc,' is not present in ',self.card_dir
                resubfile = self.makeResubFile(key)
                os.system('chmod u+x '+os.path.abspath(resubfile))
                resubcmds[key] = 'bsub -q {queue} -o {log} {srcfile}'.format(
                    queue=self.options.queue, log=os.path.abspath(resubfile.replace('.sh','.log')), srcfile=os.path.abspath(resubfile))

        for key,f in self.cardinputs.iteritems():
            f_ok = True
            if not os.path.exists(self.card_dir+'/'+f): 
                if self.options.verbose>1: print '# input root file ',f,' is not present in ',self.card_dir
                f_ok = False
            elif os.path.getsize(self.card_dir+'/'+f) < 1000.:
                print '# WARNING found a input root file below 1kB:', self.card_dir+'/'+f
                f_ok = False
            else: 
                if self.options.checkZombies:
                    tfile = ROOT.TFile.Open(self.card_dir+'/'+f)
                    if not tfile or tfile.IsZombie():
                        if self.options.verbose>1: print '# ',f, ' is Zombie'
                        f_ok = False
                    if len(tfile.GetListOfKeys()) < 0:
                        if self.options.verbose>1: print '# WARNING',f, ' has no keys inside!!'
                        f_ok = False

            if not f_ok: 
                resubfile = self.makeResubFile(key)
                os.system('chmod u+x '+os.path.abspath(resubfile))
                resubcmds[key] = 'bsub -q {queue} -o {log} {srcfile}'.format(
                    queue=self.options.queue, log=os.path.abspath(resubfile.replace('.sh','.log')), srcfile=os.path.abspath(resubfile))
        return resubcmds

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage='%prog dir channel (el,mu) [nRapBins] [nPdfBins]')
    parser.add_option('-c', '--check-cards', dest='checkCards', default=False, action='store_true', help='Check if there are all the datacards and ROOT files');
    parser.add_option('-z', '--check-zombies', dest='checkZombies', default=False, action='store_true', help='Check if all the ROOT files are sane');
    parser.add_option('-q', '--queue', dest='queue', type='string', default='1nd', help='choose the queue to submit batch jobs (default is 8nh)');
    parser.add_option('-v', '--verbose', dest='verbose', default=0, type=int, help='Degree of verbosity (0=default prints only the resubmit commands)');
    (options, args) = parser.parse_args()

    if options.checkCards:
        carddir = args[0]
        if len(args)<1: print 'needed inputs: datacards_dir '; quit()
        cc = CardsChecker(carddir, options)
        result = cc.checkCards()
        if len(result)==0: print 'All cards are GOOD.'
        else: 
            keys = result.keys()
            keys.sort()
            for k in keys: print result[k]
            print '## in total have to resubmit {n} jobs'.format(n=len(result))

