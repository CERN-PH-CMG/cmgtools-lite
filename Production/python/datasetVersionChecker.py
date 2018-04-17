from CMGTools.Production.dataset import _dasPopen
import re

class DatasetVersionChecker:
    def __init__(self):
        pass
    def checkComp(self,comp,verbose=False):
        dataset = comp.dataset
        return self.check(dataset,verbose=verbose)
    def check(self,dataset,verbose=False):
        pattern = re.compile(r"(/[^/]+/[^/]+)-v(\d+)(/[A-Z\-]+)$")
        m = re.match(pattern, dataset)
        if not m: raise RuntimeError, "Sorry, dataset %r is not conformant with our expectations" % dataset
        dwild = "%s-v*%s" % (m.group(1), m.group(3))
        currversion = int(m.group(2))
        dbs='dasgoclient --query="dataset dataset=%s status=VALID" --limit 999'%(dwild,)
        dbsOut = _dasPopen(dbs, verbose=False)
        versions  = []
        for line in dbsOut:
            mline = re.match(pattern, line.strip())
            if not mline: continue
            versions.append(int(mline.group(2))) 
        versions  = list(sorted(set(versions)))
        if verbose: print "%s: current version %d, all versions %s, match %s" % (
            dataset, currversion, versions, "OK" if ( currversion == max(versions) ) else "FAIL") 
        return currversion == max(versions)

       
