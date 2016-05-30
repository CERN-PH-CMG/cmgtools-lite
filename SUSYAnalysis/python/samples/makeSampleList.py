#!/usr/bin/env python
# command to make list
# das_client --query="dataset=/SMS-T1tttt_mGluino-*TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM" --key /afs/desy.de/user/l/lobanov/.globus/cms.proxy  --cert /afs/desy.de/user/l/lobanov/.globus/cms.proxy --limit 50

listfile = "das_list_t1tttt.txt"

oldPath = "_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-FastAsympt25ns_74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"

compLine = "%s = kreator.makeMCComponent(\"%s\",\"%s\",\"CMS\",\".*root\")"

samps = []

with open(listfile,"r") as flist:

    lines = [line for line in flist.readlines() if "#" not in line]

    for line in lines:
        #print line
        line = line.replace("\n","")

        samp = line.replace(oldPath,"")
        samp = samp.replace("/SMS-","")
        samp = samp.replace("-","_")
        samp = samp.replace("Gluino","Go")

        samps.append(samp)
        #print samp
        print compLine %(samp,samp,line)

print samps
