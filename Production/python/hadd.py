import os
import pickle
import shutil
import subprocess
from collections import defaultdict

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


def hadd(file, odir, idirs, appx=''):
    MAX_ARG_STRLEN = 131072
    if file.endswith('.pck'):
        try:
            haddPck( file, odir, idirs)
        except ImportError:
            pass
        return
    elif not file.endswith('.root'):
        return
    haddCmd = ['hadd']
    haddCmd.append(file.replace(idirs[0], odir).replace('.root', appx+'.root'))
    for dir in idirs:
        haddCmd.append( file.replace( idirs[0], dir ) )
    # import pdb; pdb.set_trace()
    cmd = ' '.join(haddCmd)
    print cmd
    if len(cmd) > MAX_ARG_STRLEN:
        print 'Command longer than maximum unix string length; dividing into 2'
        hadd(file, odir, idirs[:len(idirs)/2], '1')
        hadd(file.replace(idirs[0], idirs[len(idirs)/2]), odir, idirs[len(idirs)/2:], '2')
        haddCmd = ['hadd']
        haddCmd.append(file.replace(idirs[0], odir).replace('.root', appx+'.root'))
        haddCmd.append(file.replace(idirs[0], odir).replace('.root', '1.root'))
        haddCmd.append(file.replace(idirs[0], odir).replace('.root', '2.root'))
        cmd = ' '.join(haddCmd)
        print 'Running merge cmd:', cmd
        os.system(cmd)
    else:
        os.system(cmd)


def haddRec(odir, idirs):
    print 'adding', idirs
    print 'to', odir

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
            # cmd = 'mkdir ' + dir 
            # print cmd
            # os.system(cmd)
            os.mkdir(dir)
        for file in files:
            hadd('/'.join([root, file]), odir, idirs)

def haddNano(odir, idirs, firstTime=True):
    print 'adding', idirs
    print 'to', odir

    if os.path.exists(odir):
        raise RuntimeError("Error, %s exists already." % odir)
    elif os.path.dirname(odir):
        if not os.path.isdir(os.path.dirname(odir)): 
            os.makedirs(os.path.dirname(odir))

    if firstTime:
        files = []
        for chunk in idirs:
            if os.path.isdir(chunk):
                found = False
                for fname in os.listdir(chunk):
                    if fname.endswith(".root") and os.path.isfile(os.path.join(chunk, fname)):
                        files.append(os.path.join(chunk, fname))
                        found = True
                if not found: 
                    raise RuntimeError("Error, chunk %s doesn't contain any root file" % chunk)
            elif chunk.endswith(".root"):
                files.append(chunk)
    else:
        files = idirs[:]

    if len(files) == 0:
        raise RuntimeError("Error, no files for target %s" % odir)
    elif len(files) > 200:
        newlist = []; sublist = []
        for f in files:
            sublist.append(f)
            if len(sublist) == 200:
                haddNano(odir+"_sub%d" % len(newlist), sublist, firstTime=False)
                newlist.append(odir+"_sub%d.root" % len(newlist))
                sublist = []
        if sublist:
            haddNano(odir+"_sub%d" % len(newlist), sublist, firstTime=False)
            newlist.append(odir+"_sub%d.root" % len(newlist))
        haddNano(odir, newlist, firstTime=False)
        return

    try:
        if len(files) == 1:
            shutil.move(files[0], odir+".root")
        else:
            subprocess.call(["haddnano.py", odir+".root" ] + files)
    except OSError:
        print 
        print 'ERROR: directory in the way. Maybe you ran hadd already in this directory? Remove it and try again'
        print 
        raise

def haddChunks(idir, removeDestDir, cleanUp=False, ignoreDirs=None, maxSize=None, nanoAOD=False):

    chunks = {}
    compsToSpare = set()
    if ignoreDirs == None: ignoreDirs = set()

    for file in sorted(os.listdir(idir)):
        filepath = '/'.join( [idir, file] )
        isdir = os.path.isdir(filepath)
        # print filepath
        if isdir or (nanoAOD and filepath.endswith(".root")):
            compdir = file if isdir else file.rstrip(".root")
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
                if nanoAOD and os.path.isfile(ch+".root"):
                    size = os.path.getsize(ch+".root")
                else:
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
                if nanoAOD and os.path.isfile(odir + ".root"):
                    os.unlink(odir + ".root")
                elif os.path.isdir( odir ):
                    shutil.rmtree(odir)
            if nanoAOD:
                haddNano(odir, cchunks)
            else:
                haddRec(odir, cchunks)
            if cleanUp and (comp not in compsToSpare):
                for chunk in cchunks:
                    if nanoAOD and not os.path.exists(chunk): continue
                    shutil.move(chunk, chunkDir)




        
if __name__ == '__main__':
    import sys
    args = sys.argv
    # odir = args[1]
    # idirs = args[2:]
    # haddRec(odir, idirs)
    haddChunks(sys.argv[1])
