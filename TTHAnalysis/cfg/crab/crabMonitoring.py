import os,sys,subprocess

def crabMonitoring(initProxy=False):

    if initProxy:
        os.system("voms-proxy-init --voms cms --valid 168:00")

    totPath=str(os.environ["PWD"])
    path=str(os.environ["CMSSW_BASE"])
    cmssw=path.split("/")[-1]
    path=path[:-(1+len(cmssw))]
    
    #writing the cronjob script
    cronFile=open(path+'/cronJob.sh','w')
    
    cronFile.write("#!/bin/bash\n\n")

    cronFile.write("source /afs/cern.ch/sw/lcg/external/gcc/4.7/x86_64-slc6/setup.sh\n")
    cronFile.write("export SCRAM_ARCH=slc6_amd64_gcc491\n")
    cronFile.write("export CMS_PATH=/afs/cern.ch/cms\n") 
    cronFile.write("source $CMS_PATH/cmsset_default.sh\n")

    cronFile.write("cd "+path+"\n\n")
    cronFile.write("source /cvmfs/cms.cern.ch/crab3/crab.sh\n")
    cronFile.write("if [ -f $PWD/ProdTool/scripts/setEnvVar.sh ];then\nsource $PWD/ProdTool/scripts/setEnvVar.sh $release $PWD\nfi\n")
    cronFile.write("cd "+totPath+"\n\n")
    cronFile.write("eval `scramv1 runtime -sh`\n\n")
    cronFile.write("python crabAutoTool.py\n")

    cronFile.close()

    pipe = subprocess.Popen("hostname", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    host, err = pipe.communicate()
   
    cronTxt=open(totPath+'/crontab.txt','w')
    cronTxt.write("00	00,04,08,12,16,20     *	*	*	"+host.split("\n")[0]+"	"+path+"/cronJob.sh\n")
    cronTxt.close()

    os.system("acrontab < crontab.txt")

if len(sys.argv) > 1:
    crabMonitoring( bool(sys.argv[1]) )
else:
    crabMonitoring()
