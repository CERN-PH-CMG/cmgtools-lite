# usage:  python w-helicity-13TeV/hadd_wy.py <input_folder> [options]
#
# first argument is list of folders with distributions for no or nominal selection
# See examples below

# example usage: python w-helicity-13TeV/hadd_wy.py plots/gen_eff_tightCharge_chargeMatch/ -c pfmt -l -o eff_tightCharge_chargeMatch  

# script developed to work passing a folder containing other folders like the following:
#
# [mciprian@pccmsrm29 plotter]$ ls plots/gen/
# wgen_fullsel_minus         wgen_fullsel_pfmt30_plus   wgen_fullsel_pfmt40_plus   wgen_fullsel_pfmt50_plus  wgen_nosel_minus
# wgen_fullsel_pfmt30_minus  wgen_fullsel_pfmt40_minus  wgen_fullsel_pfmt50_minus  wgen_fullsel_plus         wgen_nosel_plus
# [mciprian@pccmsrm29 plotter]$ python w-helicity-13TeV/hadd_wy.py plots/gen/ -c pfmt
#
# it will create root files containing histograms with no selection and with any of the other selections (no pfmt or pfmtXX in this case).
# For the example above, it will create 4 files, one for nominal and one for each of the 3 pfmt selections
#
# It works also in you have only nosel and nominal selection (4 folders), which is the default.
#
# In general we use NLO samples, but we could also use LO (for example, for systematics). 
# In this case the convention is that the last folder must end with '_LO'
# In that case, the histograms will also be named with '_LO' at the end of their original names, and will be put in the same output file as the others.
# This requires passing option -l, otherwise the script complains becasue it sees more than 4 folders 
# (if you have exactly 4 folders and all are named with _LO the script still works).
# The rest works in the same way (if you have additional selections and so on)
#
# Note: the script should still work if all the fullsel folders have some cut tag in their name, like in the following:
#
# [mciprian@pccmsrm29 plotter]$ ls plots/gen_eff_tightCharge/     
# wgen_fullsel_pfmt40_minus     wgen_fullsel_pfmt40_plus     wgen_nosel_minus     wgen_nosel_plus
# wgen_fullsel_pfmt40_minus_LO  wgen_fullsel_pfmt40_plus_LO  wgen_nosel_minus_LO  wgen_nosel_plus_LO
#
# In this case, you may not specify the cut with -c <cut_name_ID> option, and the files will be treated as usual, but you need -l

import sys, os
import ROOT, datetime, array
import re

from optparse import OptionParser
parser = OptionParser(usage='python %prog <input_folder> [options] ')
parser.add_option('-x','--x-var', dest='xvar', default='wy', type='string', help='Name of variable in the x axis, as should appear inside the input root files (default is wy)')
parser.add_option('-c','--cut-name', dest='cutName', default='', type='string', help='name of cut. It is a tag that should be present in some folders')
parser.add_option('-o','--outdir', dest='outdir', default='./', type='string', help='Output folder (default is current one)')
parser.add_option('-s','--skip', dest='skip', default='', type='string', help='Match to skip (if a file has this string in its name it will be skipped)')
parser.add_option('-e','--endtag', dest='endtag', default='', type='string', help='Match identifying a specific folder. This tag should be found at the end of the name (general case of option -l for LO samples)')
parser.add_option('-l','--LO', dest="hasLO", action="store_true", default=False, help="Specify if there are folders for LO samples (they must end with '_LO')")
parser.add_option(     '--TH2',dest="hasTH2", action="store_true", default=False, help="Specify if there are TH2 inside root file (default is TH1)")
parser.add_option(     '--no-helicity',dest="has_no_helicity", action="store_true", default=False, help="Specify that the helicity is not part of the histogram name (in case you only separate by charge)")

(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_usage()
    quit()

inputdir = args[0]

outdir = options.outdir
if not outdir.endswith("/"):
    outdir += "/" 

# varcut = "pfmt"
# if varcut != "":
#     noAdditionalCut = False
# else:
#     noAdditionalCut = True

xvar = options.xvar
xvarMatch = "_" + xvar + "_"

varcut = ""
noAdditionalCut = True
if options.cutName != '':
    varcut = options.cutName
    noAdditionalCut = False

skipMatch = False
match = ""
if options.skip != '':
    skipMatch = True
    match = options.skip

if options.hasTH2:
    baseClassName = "TH2"
else:
    baseClassName = "TH1"

#files = [ f for f in os.listdir(inputdir) if f.endswith('.root') ]
#files = list( [os.path.join(inputdir, f) for f in files] )
    
if not os.path.isdir(outdir):
    os.system('mkdir -p {od}'.format(od=outdir))

files = list()
for root, dirs, tmpfiles in os.walk(inputdir):
    for f in tmpfiles:
        if f.endswith(".root"):
            thisfile = os.path.join(root, f)
            print("Getting file --> %s " % str(thisfile))
            files.append(str(thisfile))

if options.hasLO:
    expectedFolders = 8
else:
    expectedFolders = 4

if options.endtag != '':
    expectedFolders = expectedFolders + 2  # 1 additional reco for each charge, but the logic could change if we add more endtags

#print "expectedFolders = " + str(expectedFolders)

if len(files) > expectedFolders and noAdditionalCut:
    print "==================================="
    print "WARNING: you have not specified any folder name tag, but I see more than %d folders (%d)" % (int(expectedFolders),len(files))
    if int(expectedFolders) == 4 and len(files) == 8:
        print "Did you want to include LO samples but forgot option --LO ?"
    print "I cannot manage this situation correctly, please check. Exit"
    print "==================================="
    quit()

# for f in files:
#     print f
# quit()

helicities = ["right", "left", "long"]

tmpplots = []
varcut_thr_list = set([])
for f in files:
    if skipMatch and match in f: 
        continue
    print "Opening file: ",f
    tf = ROOT.TFile.Open(f)
    for k in tf.GetListOfKeys() :
        name=k.GetName()
        obj=k.ReadObj()
        if xvarMatch in name and obj.InheritsFrom(baseClassName):
            if options.has_no_helicity or any(h in name for h in helicities):
                if options.hasTH2 and 'background' in name: continue
                if 'fullsel' in f:
                    tokens = name.split('_')
                    if varcut != "" and varcut in f:
                        print "=== Check ==="
                        regex = re.compile(varcut+'([0-9]*)')
                        varcut_thr = regex.findall(f)
                        if len(varcut_thr) and varcut_thr[0] != '':
                            # case pfmtXX with XX integer
                            #print "==> " + varcut_thr[0] 
                            varcut_thr_list.add(int(varcut_thr[0]))
                            newname = '_'.join( tokens[:2]+['reco_%s%d' % (varcut, int(varcut_thr[0]))]+tokens[2:] )                        
                        else:
                            # case pfmtSmearXX with XX integer
                            regex = re.compile(varcut+'([A-Za-z]*)')  # get Smear
                            suffix = regex.findall(f)
                            regex = re.compile(str(suffix[0])+'([0-9]*)')  # get XX
                            varcut_thr = regex.findall(f)
                            varcut_thr_list.add(int(varcut_thr[0]))
                            #print "==> " + suffix[0] + varcut_thr[0]
                            newname = '_'.join( tokens[:2]+['reco_%s%d' % (varcut, int(varcut_thr[0]))]+tokens[2:]+suffix )   
                    else: 
                        newname = '_'.join( tokens[:2]+['reco']+tokens[2:] )
                else:
                    newname = name
                lastFolder = os.path.basename(os.path.dirname(f))
                if lastFolder.endswith('_LO'):
                    newname = newname + '_LO'
                if options.endtag != '' and lastFolder.endswith(options.endtag):
                    newname = newname + '_' + options.endtag

                newh = obj.Clone(newname)
                newh.SetDirectory(None)
                tmpplots.append(newh)
        #tf.Close()

outputfile = outdir + 'mc_reco_eff.root'
mergedFile = ROOT.TFile.Open(outputfile,'recreate')
mergedFile.cd()

print "#####################"
print "File ", outputfile
for p in tmpplots:
    if noAdditionalCut or varcut not in p.GetName():
        print "Writing histo: ",p.GetName()
        p.Write()
mergedFile.Close()


if not noAdditionalCut:

    print ""    
    print "thresholds for " + varcut + " cut: ",varcut_thr_list
    for thr in varcut_thr_list:
        outputfile = outdir + 'mc_reco_%s%d_eff.root' % (varcut, thr) 
        mergedFile = ROOT.TFile.Open(outputfile,'recreate')
        mergedFile.cd()
        print "#####################"
        print "File ", outputfile
        for p in tmpplots:
            if 'reco' not in p.GetName() or (str(thr) in p.GetName() and varcut in p.GetName()):
                tmpNameNoCut = p.GetName().replace("%s%d_" % (varcut, thr),"")
                print "%s%d: Writing histo: %s (original name --> %s)" % (varcut, thr, tmpNameNoCut, p.GetName())
                p.Write(tmpNameNoCut)
        mergedFile.Close()
    
