def convertSignal(filein,fileout):
    f = open(filein)
    ff=open(fileout,'w')

    ff.write("from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator\n")
    ff.write("kreator = ComponentCreator()\n")  
    ff.write('signalSamples=[] \n')
    for line in f:
        prefix = line.split('/')[1]
        mass = prefix.split('M-')[1].split('_')[0]
        name=prefix.split('M-')[0]+mass 
        ff.write('{name}=kreator.makeMCComponent("{name}", "{sample}", "CMS", ".*root",1.0)\n'.format(name=name,sample=line.split('\n')[0]))
        ff.write('signalSamples.append({name})\n'.format(name=name))
    f.close()
    ff.close()



def convertSignalWithWidth(filein,fileout):
    f = open(filein)
    ff=open(fileout,'w')

    ff.write("from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator\n")
    ff.write("kreator = ComponentCreator()\n")  
    ff.write('signalSamples=[] \n')
    for line in f:
        prefix = line.split('/')[1]
        mass = prefix.split('W-')[1].split('_')[0]
        name=prefix.split('W-')[0]+mass 
        name=name.replace('-','_')
        ff.write('{name}=kreator.makeMCComponent("{name}", "{sample}", "CMS", ".*root",1.0)\n'.format(name=name,sample=line.split('\n')[0]))
        ff.write('signalSamples.append({name})\n'.format(name=name))
    f.close()
    ff.close()


def convertBackground(filein,fileout):
    f = open(filein)
    ff=open(fileout,'w')

    ff.write("from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator\n")
    ff.write("kreator = ComponentCreator()\n")  
    ff.write('backgroundSamples=[] \n')
    for line in f:
        items= line.split(' ')
        ff.write('{name}=kreator.makeMCComponent("{name}", "{sample}", "CMS", ".*root",{sigma})\n'.format(name=items[0],sample=items[1],sigma=items[2].split('\n')[0]))
        ff.write('backgroundSamples.append({name})\n'.format(name=items[0]))
    f.close()
    ff.close()
