#!/usr/bin/env python

import os, glob
import CMGTools.Production.eostools as eostools
from optparse import OptionParser

if __name__ == "__main__":

	usage="""%prog [options] localdir remoteEOSdir

# This script can be used to archive the flat trees produced by a module to EOS.
#
# If the trees are in mybasedir/TREE_PRODUCTION_XYZ/myTreeProducer/tree.root,
# you should navigate to mybasedir and execute from there:
# archiveTreesOnEOS.py -t myTreeProducer TREE_PRODUCTION_XYZ /eos/cms/store/user/myusername/mytreesdirectory
#
# The friend tree files of the format mybasedir/TREE_PRODUCTION_XYZ/somename/*evVarFriend* are also archived.
# See the options for customization of the file name format.
#
# This script will not erase the local trees, but you will be provided with the commands to do so.
# Be sure that the copy was successful before doing so! The checksums of local and remote files are compared to help you.

"""

	parser = OptionParser(usage=usage)
	parser.add_option("-t", dest="treeproducername", type='string', default="myTreeProducer", help='Name of the tree producer module')
	parser.add_option("-f", dest="friendtreestring", type='string', default="evVarFriend", help='String identifying friend trees (must be contained in the root file name)')
	parser.add_option("-T", dest="treename", type='string', default="tree.root", help='Name of the tree file')
	parser.add_option("--dset", dest="dset", type='string', default=None, help='Name of the dataset to process')
	parser.add_option("--al", "--allowSymlinks", dest="allowSymlinks", action='store_true', default=False, help='Allow symlinks')
        parser.add_option("-P","--permissive", dest="permissive", action="store_true", default=False, help="Skip files or directories that don't contain trees, without raising an error")
        parser.add_option("-F","--force", dest="force", action="store_true", default=False, help="Skip files or directories that don't contain trees, without raising an error")
	(options, args) = parser.parse_args()
	if len(args)<2: raise RuntimeError, 'Expecting at least two arguments'
	
	locdir = args[0]
	remdir = os.path.join(args[1], os.path.basename(locdir))
	
	
	if not eostools.isEOS(remdir): raise RuntimeError, 'Remote directory should be on EOS.'
	if (not eostools.fileExists(locdir)) or eostools.isFile(locdir): 
	    raise RuntimeError, 'The local directory that should contain the trees does not exist.'

# check removed to allow for top-up of tree productions
#	if eostools.fileExists('%s/%s' % (remdir,locdir)):
#	    raise RuntimeError, 'The remote EOS directory where the trees should be archived already exists.'
	
	alldsets = [ p for p in glob.glob(locdir+"/*") if os.path.isdir(p) ]
        if not options.allowSymlinks: 
            symlinks = [ d for d in alldsets if os.path.islink(d) ]
            if symlinks: 
                print "The following directories are symlinks and will not be considered (run with --allowSymlinks to include them): ", ", ".join(map(os.path.basename,symlinks))
                alldsets = [ d for d in alldsets if not os.path.islink(d) ]
	dsets = [d for d in alldsets if [ fname for fname in glob.glob(d+"/*") if options.friendtreestring in fname]==[] ]
	if options.dset: dsets = [d for d in dsets if options.dset in d]
	friends = [d for d in alldsets if d not in dsets]
	if options.dset: friends = [d for d in friends if options.dset in d]
	
	tocopy = []
	for d in dsets:
	    if os.path.isfile(d): 
                if options.permissive:
                    print 'WARNING: File %s found in local directory --> will be skipped' % d
                    continue
                raise RuntimeError, 'File %s found in local directory (use --permissive to skip it)' % d
	    if not os.path.exists('%s/%s'%(d,options.treeproducername)): 
                if options.permissive:
                    print 'WARNING: Tree producer sub-directory %s/%s not found --> will skip directory %s' % (d,options.treeproducername,d)
                    continue
                raise RuntimeError, 'Tree producer sub-directory %s/%s not found (use --permissive to skip it).' % (d,options.treeproducername)
	    fname = d+'/'+options.treeproducername+'/'+options.treename
	    if not os.path.isfile(fname): raise RuntimeError, 'Tree file %s not found (or it is not a file).' % fname
	    tocopy.append( (fname,'%s/%s_%s_%s'%(remdir,os.path.basename(d),options.treeproducername,options.treename)) )
	for d in friends:
	    allfriends = glob.glob(d+"/*")
	    for f in allfriends:
	        if (options.friendtreestring not in f) or (not os.path.isfile(f)):
	            raise RuntimeError, 'Unknown file in friend directory.'
	        tocopy.append( (f,'%s/%s_%s'%(remdir,os.path.basename(d),f.split('/')[-1])) )
	for task in tocopy:
	    if os.path.exists(task[0]+".url"): 
                if options.force:
         	    print "WARNING: .url file already exists for %s, but forcing a new transfer" % task[0]
                else:
                    raise RuntimeError, '.url file already exists for %s (use --force to force a new archival)' % task[0]
	print 'Will create EOS directory %s and copy the following files:\n'%remdir
	for task in tocopy: print '%s -> %s' % task
	
	print '\nDo you agree? [y/N]\n'
	if raw_input()!='y':
	    print 'Aborting'
	    exit()
	
	eostools.mkdir(remdir)
	if not eostools.fileExists(remdir): raise RuntimeError, 'Impossible to create remote directory.'
	for task in tocopy:
	    eostools.xrdcp(task[0],task[1])
	    fcmd = open(task[0]+".url","w")
	    fcmd.write("root://eoscms.cern.ch/%s\n" % task[1])
	    fcmd.close()
	print 'Copied %.2f GB to EOS\n' % eostools.eosDirSize(remdir)

	print 'Verifying checksums:\n'
	problem = False
	for task in tocopy:
		lcheck = eostools.fileChecksum(task[0])
		rcheck = eostools.fileChecksum(task[1])
		ok = (lcheck==rcheck)
		print task[0],lcheck,rcheck,('OK' if ok else 'ERROR')
		if not ok: problem = True
	if problem:
		raise RuntimeError, 'CHECKSUM ERROR DETECTED !!!'
	else:
		print '\nALL CHECKSUMS OK\n'
		print '\nIf you want, you can rename the local root files to force usage of the remote EOS copy for testing:\n'
		for task in tocopy: print 'mv -n %s %s.transferred'%(task[0],task[0])
		print '\nIf the testing is successful, you can delete the local root files:\n'
		for task in tocopy: print 'rm -v %s.transferred'%task[0]
