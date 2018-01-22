import os,sys,math,re


def readFile(fname):

    ifile=open(fname,'r')
    lines=ifile.read().splitlines()
    return lines


def checkTune(sample, newSamples):
    
    tune=re.compile(r"(\S+)_Tune(\S+)_(.+)/")
    st=re.match(tune,sample)
    tuneSamples=[]
    #print sample, st
    if st:
        #print "==================", st.group(1), st.group(3)
        for ns in newSamples:
            #print ns, (st.group(1)+"_Tune" in ns), (st.group(3) in ns)
            if st.group(1)+"_Tune" in ns and st.group(3) in ns:
                tuneSamples.append(ns)

    #print tuneSamples
    return tuneSamples


def matchSample(line, newSamples):

    olds=re.compile(r".+/(\S+/)(\S+)/MINIAODSIM.+")
    s=re.match(olds,line)
    if s:
        sample=s.group(1)
        ext= ''
        if 'ext' in s.group(2):
            exts=re.compile(r".+(ext[0-9])")
            se=re.match(exts,s.group(2))
            if se:
                ext=se.group(1)

        goodSamples=[s for s in newSamples if ((sample in s) and ((ext in s) if ext!='' else ('ext' not in s) ) )]
        if len(goodSamples)==0:
            tuneSamples=checkTune(sample, newSamples)
            #print "-->> ", tuneSamples
            goodSamples=[s for s in tuneSamples if (len(tuneSamples)==1 or ((ext in s) if ext!='' else ('ext' not in s) ) ) ]
            #print ">>", goodSamples

        #print line, goodSamples
        if len(goodSamples)>1:
            for gs in goodSamples:
                if 'backup' in gs:
                    goodSamples.remove(gs)
        if len(goodSamples)>1:
            version=re.compile(r".+v([0-9])/MINIAODSIM")
            goodIdx=-1
            vMax=-1
            for idx,gs in enumerate(goodSamples):
                vs=re.match(version,gs)
                if vs:
                    if vMax<int(vs.group(1)):
                        goodIdx=idx
                        vMax=int(vs.group(1))
            for idx,gs in enumerate(goodSamples):
                if idx!=goodIdx:
                    goodSamples.remove(gs)

        if len(goodSamples)==0:
            return False, []
        else:
            return True, goodSamples
    else:
        return False, []

def replaceSample(line, sample):

    olds=re.compile(r".+(/\S+/\S+/MINIAODSIM).+")
    s=re.match(olds,line)
    #print s
    if s:
        updatedLine=re.sub(r'/\S+/\S+/MINIAODSIM',sample,line)
    else:
        updatedLine=line


    #print line
    #print '->', updatedLine

    return updatedLine



def findSamples(newSampleFile, samples, newFile):
    
    linesSample=readFile(samples)
    linesNewS=readFile(newSampleFile)

    comments=[]
    uncomments=[]
    for idx,line in enumerate(linesSample):
        dec, samples=matchSample(line, linesNewS)
        #print dec ,"-->", samples
        if dec and len(samples)>1:
            print "--->>>", line
            print "===>>>", samples
        elif not dec and 'MINIAODSIM' in line and line[0]!="#":
            #print line
            linesSample[idx]="#"+linesSample[idx]
            comm=re.compile(r"#(\S+).+=")
            sc=re.match(comm,linesSample[idx])
            if sc:
                comments.append(sc.group(1))
        elif dec and len(samples)==1:
            linesSample[idx]=replaceSample(line, samples[0])
            comm=re.compile(r"(\S+) .+")
            sc=re.match(comm,linesSample[idx])
            if sc:
                uncomments.append(sc.group(1))
        
    #turn on/off the components in the arrays
    for idx,line in enumerate(linesSample):
        if 'MINIAODSIM' in line or 'mcSamples' in line: continue
        for com in comments:
            if com in line and line[0]!="#":
                linesSample[idx]="#"+linesSample[idx]
        for ucom in uncomments:
            if com in line and line[0]=="#":
                linesSample[idx]=linesSample[idx][1:]


    ofile=open(newFile,'w')
    for line in linesSample:
        ofile.write(line+'\n')


if __name__ == "__main__":

    import os, itertools
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] OLDFILE NEWFILE PRODID")
    parser.add_option("-s", "--samples", dest="newSamples",  type="string", default="", help="new sample file");
    (options, args) = parser.parse_args()
    
    if options.newSamples=="":
        os.system('das_client.py --query="dataset dataset=/*/'+args[2]+'*/MINIAODSIM" --limit 0 > tmpNewSamples') 
        newSamples="tmpNewSamples"
    else:
        newSamples=options.newSamples
    oldFile=args[0]
    newFile=args[1]

    findSamples(newSamples, oldFile, newFile)
    
