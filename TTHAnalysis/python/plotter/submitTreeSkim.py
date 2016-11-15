## python
import sys, os
import tempfile

# Usage:
#./submit mca-Long.txt [rest]

if len(sys.argv) > 1:
    mcaF = sys.argv[1]
else:
    print "Usage:"
    print "./submit mca-Long.txt [rest]"
    exit(0)

# make unique name for jobslist
outdir = "skimmer/"
jobs = []
if not os.path.exists(outdir): os.system("mkdir -p "+outdir)

import time
itime = int(time.time())
jobListName = outdir+'jobList_%i.txt' %(itime)
jobList = open(jobListName,'w')
print 'Filling %s with job commands' % (jobListName)

with open(mcaF,"r") as mca:

    lines = [line for line in mca.readlines() if line[0] != "#" and len(line.split(":")) > 1]

    print "Found %i entries in file: %s" %(len(lines), mcaF)

    for line in lines:
        cline = line.replace("\n","")
        cline = cline.replace("\t","")
        cline = cline.replace(" ","")

        comp = cline.split(":")
        print 80*"#"
        print "Preparing job for", comp[1]

        tmpname = outdir + "mca_" + comp[1] + ".txt"
        #tmpname = tempfile.mkstemp("_"+comp[1]+".txt","mca_")[1]
        #tmpname = tmpname.replace("/tmp","~/tmp/skimmer/")
        #tmpname = tmpname.replace("/tmp","skimmer")
        #tmpMCA = tempfile.TemporaryFile(prefix="mca_"+comp[1])
        #tmpMCA.close()
        print "Storing mca in ", tmpname

        #tmpname = os.path.abspath(tmpname)

        # write line to temp mca
        tmpMCA = open(tmpname,"w")
        tmpMCA.write(line)
        tmpMCA.close()

        ######
        # submit job
        cmd = sys.argv

        # replace exe
        cmd[0] = "skimTrees.py"

        # replace MCA
        cmd[1] = tmpname
        cmds = " ".join(str(arg).replace("*","\*") for arg in cmd)

        jobList.write("python " + cmds + "\n")
        jobs.append(cmds)

# submit
#check log dir
logdir = outdir+'logs'
if not os.path.exists(logdir): os.system("mkdir -p "+logdir)

subCmd = 'qsub -t 1-%i -o %s nafbatch_runner.sh %s' %(len(jobs),logdir,jobListName)
print 'Going to submit', len(jobs), 'jobs with:', subCmd
os.system(subCmd)

exit(0)
# submit job array on list
subCmd = 'qsub -N %s -o %s  nafbatch_skimmer.sh %s' %("Skim_"+comp[1],logdir,cmds)
print 'Going to submit', subCmd
os.system(subCmd)

