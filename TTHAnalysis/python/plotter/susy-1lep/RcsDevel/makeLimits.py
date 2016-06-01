#!/usr/bin/env python
import os, glob, sys

SMS = "T1tttt"

from ROOT import *
def combineCards(f , s ):
    try:            
        os.stat('combinedCards') 
    except:
        os.mkdir('combinedCards')

    cmd = 'combineCards.py ' + f + '/LT*txt > ' + f.replace(s,'combinedCards') +'/' + s + '.txt'
    print cmd
    os.system(cmd)

    return 1
def runCards(f , s):
    cmd = 'combine -M Asymptotic ../' + f + ' -n ' + s
    print cmd
    os.system(cmd)
    return 1

def createJobs(f , s, jobs):
    cmd = 'combine -M Asymptotic ../' + f + ' -n ' + s + '\n'
    print cmd
    jobs.write(cmd)
    return 1

def submitJobs(jobList, nchunks):
    print 'Reading joblist'
    jobListName = jobList
    subCmd = 'qsub -t 1-%s -o logs ../../nafbatch_runner_limits.sh %s' %(nchunks,jobListName)
    print 'Going to submit', nchunks, 'jobs with', subCmd
    os.system(subCmd)

    return 1
if __name__ == "__main__":

    ## remove '-b' option
    if '-b' in sys.argv:
        sys.argv.remove('-b')
        _batchMode = True

    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)

    ## Create Yield Storage
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
    os.chdir(pattern)
    dirList = glob.glob(SMS+'*')
    samples = [x[x.find('/')+1:] for x in dirList]    
    if 1==1:

        print samples
        for (f,s) in zip(dirList,samples):
            combineCards(f,s)
    
    if 1==1:
        fileList = glob.glob('combinedCards/*')
        print fileList
        try:            
            os.stat('limitOutput') 
        except:
            os.mkdir('limitOutput')

        chunks =0
        os.chdir('limitOutput')
        jobList = 'joblist_limits.txt'
        jobs = open(jobList, 'w') 
        print fileList
        for f in fileList:
            s = f[f.find('/')+1:f.find('.txt')]
            createJobs(f,s,jobs)
            chunks = chunks+1
#            runCards(f,s)
        submitJobs(jobList, chunks)
        jobs.close()
        


    
