#!/usr/bin/env python

import ROOT
import os, sys, re, optparse,pickle,shutil,json,random




parser = optparse.OptionParser()

parser.add_option("-q","--queue",dest="queue",help="Batch Queue",default='8nh')
parser.add_option("-t","--toyCard",dest="toyCard",help="Toy DataCard",default='')
parser.add_option("-N","--nToys",dest="toys",type=int,help="number of Toys",default=1000)
(options,args) = parser.parse_args()




for i in range(0,options.toys):
    f=open("submit_{i}.sh".format(i=i),'w')
    execScript = 'cd {cwd} \n'.format(cwd=os.getcwd())
    execScript += 'eval `scramv1 runtime -sh` \n'
    seed=int(201606+random.random()*10101982)
    execScript += "combine -m {mass} -M GenerateOnly --expectSignal=0 --bypassFrequentistFit -t 1 --saveToys  --seed {seed} {card}\n".format(mass=m,seed=seed,card=options.toyCard)
        execScript+='combine -t 1 -m {mass} --rMin=-10 --rMax=10 -M MaxLikelihoodFit  --toysFile=higgsCombineTest.GenerateOnly.mH{mass}.{seed}.root    --skipBOnlyFit -n Result_{i} {card}\n'.format(mass=m,seed=seed,i=i,card=args[0])
    f.write(execScript)
    f.close()
    os.system('chmod +x submit_{i}.sh'.format(i=i))

    if options.queue!="local":
        os.system('bsub -q {queue} submit_{i}.sh '.format(queue=options.queue,i=i))
    else:    
        os.system('sh submit_{i}.sh '.format(i=i))





