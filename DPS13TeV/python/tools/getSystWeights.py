from DataFormats.FWLite import Handle, Runs
import ROOT
import sys

lheruninfo=Handle('LHERunInfoProduct')
runs=Runs(sys.argv[1])
for r in runs:
    r.getByLabel('externalLHEProducer',lheruninfo)
    #r.getByLabel('source',lheruninfo)
    it=lheruninfo.product().headers_begin()
    while it!=lheruninfo.product().headers_end():
        lines=it.lines()
        allowPrint=False
        wgtCtr=0
        for i in xrange(0,lines.size()):
            linestr=lines.at(i)
            if '<weightgroup' in linestr : allowPrint=True
            if '</weightgroup' in linestr : allowPrint=False
            if not allowPrint : continue
            if 'weightgroup' in linestr :
                print '*'*50
                print linestr
                print '*'*50
            else:
                if not 'weight' in linestr : continue
                print wgtCtr,linestr
                wgtCtr+=1
        it.next()
