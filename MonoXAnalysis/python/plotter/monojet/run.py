#!/usr/bin/env python

import sys, os
import re
from optparse import OptionParser

if __name__ == "__main__":
    usage="%prog [options] categories"

    parser = OptionParser(usage=usage)
    parser.add_option("-y", "--yields", dest="yields", action="store_true", default=False, help='Run the yields and save them to a file')
    parser.add_option("-p", "--plots", dest="plots", action="store_true", default=False, help='Run the plots and save them to afs')
    parser.add_option("-d", "--dry-run", dest="dryrun", action="store_true", default=False, help='Do not run the commands, just print them')
    (options, args) = parser.parse_args()
    if len(args) < 1: raise RuntimeError, "Expect a listy of categories as input"
    categories=args
    
    print 'Running for the categories ', args
    
    bashopts = ''
    if options.dryrun: bashopts='-y '
    else: bashopts='-e -y '

    CRs=['zmm','zee','wmn','wen','gj']
    
    for c in categories:
        print "--> Category ",c
        for r in CRs:
            commands=[]
            if options.yields==True and options.plots==True:
                commands.append('./monojet/monojet.sh -e -y -c '+c+' '+r)
                commands.append('./monojet/monojet.sh -e -p -c '+c+' '+r)
            else:
                if options.yields==True:
                    commands.append('./monojet/monojet.sh -e -y -c '+c+' '+r)
                if options.plots==True:
                    commands.append('./monojet/monojet.sh -e -p -c '+c+' '+r)
            for exe in commands:
                if options.dryrun: exe = re.sub(" -e","",exe)
                print '\tExecuting command',exe
                os.system(exe)
