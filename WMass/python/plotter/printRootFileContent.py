#!/usr/bin/env python  

from shutil import copyfile
import re, sys, os, os.path, subprocess, json, ROOT
import numpy as np

from optparse import OptionParser
parser = OptionParser(usage="%prog [options] infile.root")
(options, args) = parser.parse_args()

if len(sys.argv) < 1:
    parser.print_usage()
    quit()

tf = ROOT.TFile.Open(args[0],"READ")

print "Class name"
for k in tf.GetListOfKeys() :
    name=k.GetName()
    obj=k.ReadObj()
    print "%s %s" % (obj.ClassName(), name)
print "There were %d keys" % tf.GetNkeys()

    


