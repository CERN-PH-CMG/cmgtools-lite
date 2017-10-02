#!/usr/bin/env python
import os
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from CMGTools.MonoXAnalysis.postprocessing.framework.branchselection import BranchSelection
from CMGTools.MonoXAnalysis.postprocessing.framework.datamodel import InputTree
from CMGTools.MonoXAnalysis.postprocessing.framework.eventloop import eventLoop
from CMGTools.MonoXAnalysis.postprocessing.framework.output import FriendOutput, FullOutput
from CMGTools.MonoXAnalysis.postprocessing.framework.preskimming import preSkim

class PostProcessor :
    def __init__(self,outputDir,inputFiles,cut=None,branchsel=None,modules=[],compression="LZMA:9",friend=False,postfix=None,json=None,noOut=False,justcount=False):
	self.outputDir=outputDir
	self.inputFiles=inputFiles
	self.cut=cut
	self.modules=modules
	self.compression=compression
	self.postfix=postfix
	self.json=json
	self.noOut=noOut
	self.friend=friend
	self.justcount=justcount
 	self.branchsel = BranchSelection(branchsel) if branchsel else None 
    def run(self) :
    	if not self.noOut:
            outpostfix = self.postfix if self.postfix != None else ("_Friend" if self.friend else "_Skim")
            if self.compression != "none":
                ROOT.gInterpreter.ProcessLine("#include <Compression.h>")
                (algo, level) = self.compression.split(":")
                compressionLevel = int(level)
                if   algo == "LZMA": compressionAlgo  = ROOT.ROOT.kLZMA
                elif algo == "ZLIB": compressionAlgo  = ROOT.ROOT.kZLIB
                else: raise RuntimeError("Unsupported compression %s" % algo)
            else:
                compressionLevel = 0 
	    print "Will write selected trees to "+self.outputDir
            if not self.justcount:
                if not os.path.exists(self.outputDir):
                    os.system("mkdir -p "+self.outputDir)

	if self.noOut:
	    if len(self.modules) == 0: 
		raise RuntimeError("Running with --noout and no modules does nothing!")

	for m in self.modules: m.beginJob()

	fullClone = (len(self.modules) == 0)

	for fname in self.inputFiles:
	    # open input file
	    inFile = ROOT.TFile.Open(fname)

	    #get input tree
	    inTree = inFile.Get("tree")

	    # pre-skimming
	    elist,jsonFilter = preSkim(inTree, self.json, self.cut)
	    if self.justcount:
		print 'Would select %d entries from %s'%(elist.GetN() if elist else inTree.GetEntries(), fname)
		continue

	    if fullClone:
		# no need of a reader (no event loop), but set up the elist if available
		if elist: inTree.SetEntryList(elist)
	    else:
		# initialize reader
                if elist: inTree.SetEntryList(elist)
		inTree = InputTree(inTree, elist) 

	    # prepare output file
	    outFileName = os.path.join(self.outputDir, os.path.basename(fname).replace(".root",outpostfix+".root"))
	    outFile = ROOT.TFile.Open(outFileName, "RECREATE", "", compressionLevel)
	    if compressionLevel: outFile.SetCompressionAlgorithm(compressionAlgo)

	    # prepare output tree
	    if self.friend:
		outTree = FriendOutput(inFile, inTree, outFile)
	    else:
		outTree = FullOutput(inFile, inTree, outFile, branchSelection = self.branchsel, fullClone = fullClone, jsonFilter = jsonFilter)

	    # process events, if needed
	    if not fullClone:
		(nall, npass, time) = eventLoop(self.modules, inFile, outFile, inTree, outTree)
		print 'Processed %d entries from %s, selected %d entries' % (nall, fname, npass)
	    else:
		print 'Selected %d entries from %s' % (outTree.tree().GetEntries(), fname)

	    # now write the output
	    outTree.write()
	    outFile.Close()
	    print "Done %s" % outFileName

	for m in self.modules: m.endJob()
