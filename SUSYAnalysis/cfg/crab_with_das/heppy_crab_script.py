#!/usr/bin/env python
import os
import PhysicsTools.HeppyCore.framework.config as cfg
#cfg.Analyzer.nosubdir=True
cfg.Analyzer.nosubdir=False

import PSet
import sys
import re
print "ARGV:",sys.argv
JobNumber=sys.argv[1]
datasetname = None
for arg in sys.argv[2:]:
     fields = arg.split("=")
     if len(fields)==2 and fields[0].lower()=="datasetname":
          datasetname = fields[1]
          break
if datasetname==None:
     print "Missing datasetname argument"
     sys.exit(1)

print "Loading dataset with name ",datasetname
import pickle
comp = pickle.load(open("sample_"+datasetname+".pkl","rb"))

crabFiles=PSet.process.source.fileNames
print crabFiles
firstInput = crabFiles[0]
print "--------------- using edmFileUtil to convert PFN to LFN -------------------------"
for i in xrange(0,len(crabFiles)) :
     pfn=os.popen("edmFileUtil -d %s"%(crabFiles[i])).read() 
     pfn=re.sub("\n","",pfn)
     print crabFiles[i],"->",pfn
     crabFiles[i]=pfn
     #crabFiles[i]="root://xrootd-cms.infn.it:1194/"+crabFiles[i]


import imp
handle = open("heppy_config.py", 'r')
cfo = imp.load_source("heppy_config", "heppy_config.py", handle)

#config = cfo.config
cfg = cfo.cfg
seq = cfo.sequence
pre = cfo.preprocessor
handle.close()

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
print "creating config with ",[comp],seq
config = cfg.Config(components=[comp],sequence=seq,preprocessor=pre,services=[],events_class=Events)

#replace files with crab ones
config.components[0].files=crabFiles

print crabFiles

#
# transfer lumisToProcess parameter to heppy config, if present
#
if hasattr(PSet.process.source,"lumisToProcess"):
     print "Found CRAB lumi mask: ",PSet.process.source.lumisToProcess.value()
     from FWCore.PythonUtilities.LumiList import LumiList
     compList = { }
     for sub in PSet.process.source.lumisToProcess:
          for r in sub.split(","):
               a = r.split("-")
               assert len(a)==1 or len(a)==2
               b = [ ]
               for x in a:
                    c = x.split(":")
                    assert len(c)==2
                    for d in c:
                         assert d.isdigit()
                    b.append([int(c[0]),int(c[1])])
               if len(a)==1:
                    compList.setdefault(b[0][0],[]).append([b[0][1],b[0][1]])
               else:
                    assert b[0][0]==b[1][0]
                    compList.setdefault(b[0][0],[]).append([b[0][1],b[1][1]])
     lumiList = LumiList(compactList=compList)
     lumiList.writeJSON("heppy_json.txt")
     if hasattr(config.components[0],"json"):
          print "Old heppy json = ",config.components[0].json
     config.components[0].json = "heppy_json.txt"
     print "Setting heppy json"
     os.system("cat heppy_json.txt")


from PhysicsTools.HeppyCore.framework.looper import Looper
looper = Looper( 'Output', config, nPrint = 1)
looper.loop()
looper.write()

print PSet.process.output.fileName
os.system("ls -lR")
os.rename("Output/treeProducerSusySingleLepton/tree.root", "tree.root")
os.system("ls -lR")

# print in crab log file the content of the job log files, so one can see it from 'crab getlog'
print "-"*25
print "printing output txt files"
os.system('for i in Output/*/*.txt; do echo $i; cat $i; echo "---------"; done')
# pack job log files to be sent to output site
os.system("tar czf output.log.tgz Output/")

import ROOT
f=ROOT.TFile.Open('tree.root')
entries=f.Get('tree').GetEntries()
print "Entries = ",entries

fwkreport='''<FrameworkJobReport>
<ReadBranches>
</ReadBranches>
<PerformanceReport>
  <PerformanceSummary Metric="StorageStatistics">
    <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
    <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
    <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
    <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
    <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
    <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
  </PerformanceSummary>
</PerformanceReport>

<GeneratorInfo>
</GeneratorInfo>

<InputFile>
<LFN>%s</LFN>
<PFN></PFN>
<Catalog></Catalog>
<InputType>primaryFiles</InputType>
<ModuleLabel>source</ModuleLabel>
<GUID></GUID>
<InputSourceClass>PoolSource</InputSourceClass>
<EventsRead>1</EventsRead>

</InputFile>

<File>
<LFN></LFN>
<PFN>tree.root</PFN>
<Catalog></Catalog>
<ModuleLabel>HEPPY</ModuleLabel>
<GUID></GUID>
<OutputModuleClass>PoolOutputModule</OutputModuleClass>
<TotalEvents>%s</TotalEvents>
<BranchHash>dc90308e392b2fa1e0eff46acbfa24bc</BranchHash>
</File>

</FrameworkJobReport>''' % (firstInput,entries)

print fwkreport

f1=open('./FrameworkJobReport.xml', 'w+')
f1.write(fwkreport)
f1.close()

