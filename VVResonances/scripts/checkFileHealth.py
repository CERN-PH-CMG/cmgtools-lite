import ROOT
import os
import fnmatch
import sys

def main():

    baseDir = sys.argv[1]
    print "Checking files in", baseDir
    fileCounter = 0

    for root, dirnames, filenames in os.walk(baseDir):
        for filename in fnmatch.filter(filenames, '*.root'):
            fileCounter += 1
            fullPath = os.path.join(root, filename)
            rootFile = ROOT.TFile(fullPath)
            if (rootFile.IsZombie()):
                print fullPath, "is broken."
            elif (rootFile.TestBit(ROOT.TFile.kRecovered)):
                print fullPath, "has been recovered."
    print "Checked %d files" % fileCounter

if __name__ == '__main__':
    main()
