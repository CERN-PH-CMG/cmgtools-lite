import os
import pprint
import pickle
import shutil

def haddPck(file, odir, idirs):
    '''add pck files in directories idirs to a directory outdir.
    All dirs in idirs must have the same subdirectory structure.
    Each pickle file will be opened, and the corresponding objects added to a destination pickle in odir.
    '''
    sum = None
    for dir in idirs:
        fileName = file.replace( idirs[0], dir )
        pckfile = open(fileName)
        try:
            obj = pickle.load(pckfile)
        except:
            print "Error loading pckfile "+fileName
            raise
        if sum is None:
            sum = obj
        else:
            try:
                sum += obj
            except TypeError:
                # += not implemented, nevermind
                pass
                
    oFileName = file.replace( idirs[0], odir )
    pckfile = open(oFileName, 'w')
    pickle.dump(sum, pckfile)
    txtFileName = oFileName.replace('.pck','.txt')
    txtFile = open(txtFileName, 'w')
    txtFile.write( str(sum) )
    txtFile.write( '\n' )
    txtFile.close()
    

def hadd(file, odir, idirs):
    if file.endswith('.pck'):
        try:
            haddPck( file, odir, idirs)
        except ImportError:
            pass
        return
    elif not file.endswith('.root'):
        return
    haddCmd = ['hadd']
    haddCmd.append( file.replace( idirs[0], odir ) )
    for dir in idirs:
        haddCmd.append( file.replace( idirs[0], dir ) )
    # import pdb; pdb.set_trace()
    cmd = ' '.join(haddCmd)
    print cmd
    os.system(cmd)


def haddRec(odir, idirs):
    print 'adding', idirs
    print 'to', odir 

    cmd = ' '.join( ['mkdir', odir])
    # import pdb; pdb.set_trace()
    # os.system( cmd )
    try:
        os.mkdir( odir )
    except OSError:
        print 
        print 'ERROR: directory in the way. Maybe you ran hadd already in this directory? Remove it and try again'
        print 
        raise
    for root,dirs,files in os.walk( idirs[0] ):
        # print root, dirs, files
        for dir in dirs:
            dir = '/'.join([root, dir])
            dir = dir.replace(idirs[0], odir)
            cmd = 'mkdir ' + dir 
            # print cmd
            # os.system(cmd)
            os.mkdir(dir)
        for file in files:
            hadd('/'.join([root, file]), odir, idirs)


def haddChunks(idir, removeDestDir, cleanUp=False, ignoreDirs=None, maxSize=None):

    chunks = {}
    compsToSpare = set()
    if ignoreDirs == None: ignoreDirs = set()

    for file in sorted(os.listdir(idir)):
        filepath = '/'.join( [idir, file] )
        # print filepath
        if os.path.isdir(filepath):
            compdir = file
            try:
                prefix,num = compdir.rsplit('_Chunk',1)
            except ValueError:
                # ok, not a chunk
                continue
            #print prefix, num
            if compdir in ignoreDirs:
                ignoreDirs.remove(compdir)
                compsToSpare.add(prefix)
                continue
            chunks.setdefault( prefix, list() ).append(filepath)
    if len(chunks)==0:
        print 'warning: no chunk found.'
        return
    if cleanUp:
        chunkDir = 'Chunks'
        if os.path.isdir('Chunks'):
            shutil.rmtree(chunkDir)
        os.mkdir(chunkDir)
    for comp, cchunks in chunks.iteritems():
        odir = '/'.join( [idir, comp] )
        tasks = [ (odir,cchunks) ]
        if maxSize:
            threshold = maxSize*(1024.**3)
            #print odir, cchunks
            running = [ dict(files=[], size=0.) ]
            for ch in cchunks:
                size = sum(sum(os.path.getsize(os.path.join(p,f)) for f in fs) for p,d,fs in os.walk(ch))
                if running[-1]['size'] + size > threshold:
                    running.append(dict(files=[], size=0.))
                running[-1]['files'].append(ch)
                running[-1]['size'] += size
            if len(running) > 1:
                tasks = []
                for i,task in enumerate(running):
                    tasks.append( ("%s_part%d" % (odir,i+1), task['files'][:]) )
                    print "Part %s: %d files, %.3f Gb" % (tasks[-1][0], len(task['files']), task['size']/(1024.**3))
            else:
                print "Entire chunk %.3f Gb, below threshold" % (running[-1]['size']/(1024.**3))
        for odir, cchunks in tasks:
            #print odir, cchunks
            if removeDestDir:
                if os.path.isdir( odir ):
                    shutil.rmtree(odir)
            haddRec(odir, cchunks)
            if cleanUp and (comp not in compsToSpare):
                for chunk in cchunks:
                    shutil.move(chunk, chunkDir)




        
if __name__ == '__main__':
    import sys
    args = sys.argv
    # odir = args[1]
    # idirs = args[2:]
    # haddRec(odir, idirs)
    haddChunks(sys.argv[1])
