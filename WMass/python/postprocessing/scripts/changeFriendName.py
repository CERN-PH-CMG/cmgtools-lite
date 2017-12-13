#!/usr/bin/env python
import os, sys
from glob import glob

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] inputDir oldPrefix newPrefix")
    parser.add_option("-p", "--pretend", dest="pretend",   action="store_true", default=False, help="Don't run anything");

    (options, args) = parser.parse_args()

if len(args)<3:
    parser.print_help()
    sys.exit(1)

(inputdir,oldPfx,newPfx)=sys.argv[1:4]
print "Changing prefix of files from inputdir %s, from %s_ to %s_" % (inputdir,oldPfx,newPfx)

for f in glob(inputdir+"/*"):
    tokens=f.split(oldPfx)
    name=tokens[1]
    command = "mv %s %s" % (f,inputdir+"/"+newPfx+name)
    print command
    if not options.pretend: os.system(command)
