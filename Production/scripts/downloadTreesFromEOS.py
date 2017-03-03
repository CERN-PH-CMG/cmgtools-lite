#!/usr/bin/env python

import os
import CMGTools.Production.eostools as eostools
from optparse import OptionParser

if __name__ == "__main__":

	usage="""%prog [options] localdir [chunks]

# This script can be used to retrieve the flat trees stored on EOS during production, and linked in a .url file

"""

	parser = OptionParser(usage=usage)
	parser.add_option("-t", dest="treeproducername", type='string', default="myTreeProducer", help='Name of the tree producer module')
	parser.add_option("-T", dest="treename", type='string', default="tree.root", help='Name of the tree file')
	parser.add_option("-c", "--continue", dest="continueCopy", action="store_true", default=False, help='Continue downloading if a chunk failed and print a summary at the end')
	(options, args) = parser.parse_args()

	locdir = args[0]
	chunks = eostools.ls(locdir)

	print chunks

	if len(args)>1:
		chunks = [c for c in chunks if any([c.endswith('/'+d) for d in args[1:]])]

	print 'Will operate on the following chunks:',chunks

	tocopy = []
	failedDict = {}
	for d in chunks:
		f = '%s/%s/%s'%(d,options.treeproducername,options.treename)
		furl = '%s.url'%f
		if os.path.exists(f):
			print 'Chunk %s already contains tree root file %s, skipping'%(d,f)
			continue
		if not os.path.exists(furl):
			if (options.continueCopy):
				print 'Chunk %s does not contain url file %s' % (d, furl)
				failedDict[d] = furl
				continue
			else:
				raise RuntimeError,'Chunk %s does not contain url file %s'%(d,furl)
		with open(furl,'r') as _furl:
			rem = _furl.readline().replace('root://eoscms.cern.ch/','').replace('\n','')
			if not eostools.isFile(rem):
				raise RuntimeError,'Remote file %s not found'%rem
			eostools.xrdcp(rem,f)

	if (options.continueCopy and (len(failedDict.keys()) > 0)):
		print "="*100
		print "Summary of failed download attempts (%d in total):" % len(failedDict.keys())
		for d, furl in failedDict.iteritems():
			print 'Chunk %s does not contain url file %s' % (d, furl)
