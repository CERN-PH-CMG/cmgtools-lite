from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import itertools,re

class objectSelection():
    def __init__(self):
        self.num=0
        self.ptThr=0
        self.xtra=""
        self.pid=""
        self.cut=""
        self.select=""
        self.invPtThr=False
        self.checkMass=False
        self.OS=False
        self.SS=False
        self.mMin=-1
        self.mMax=1000000
        self.invMassSel=False

    def setFlags(self):
        #print " pt trheshold =======>>> ",self.ptThr
        if self.cut!="":
            self.objSel= eval("lambda "+self.pid+": "+self.cut)

        tmpL=self.xtra
        if "!pt" in self.xtra:
            self.invPtThr=True
            tmpL=tmpL.replace("!pt","")
        if "os" in self.xtra:
            self.OS=True
            tmpL=tmpL.replace("os","")
        if "ss" in self.xtra:
            self.SS=True
            tmpL=tmpL.replace("ss","")
        if "M" in self.xtra:
            self.checkMass=True
            if "!M" in self.xtra:
                self.invMassSel=True
            
            scansel1B=re.compile(r"M(\d+)([<>])")
            scansel2B=re.compile(r"M(\d+)[-](\d+)")
            test=re.compile(r"")
            r1=re.match(scansel1B, tmpL)
            r2=re.match(scansel2B, tmpL)
            if r1:
                if r1.group(2)=="<":
                    self.mMax=float(r1.group(1))
                if r1.group(2)==">":
                    self.mMin=float(r1.group(1))
            if r2:
                self.mMin=float(r2.group(1))
                self.mMax=float(r2.group(2))

            #print "===>> mass sel :", self.mMin, self.mMax, self.invMassSel

class ttHLepSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(ttHLepSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
      
        self.collections=cfg_ana.collections if hasattr(cfg_ana, "collections") else {}
        self.selections= cfg_ana.selections if hasattr(cfg_ana, "selections") else []
        self.objectSels=[]
        for selection in self.selections:
            psel=self.parseSelection(selection)
            self.objectSels.append(psel)

            


    def declareHandles(self):
        super(ttHLepSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(ttHLepSkimmer,self).beginLoop(setup)
        self.counters.addCounter('events')
        count = self.counters.counter('events')
        count.register('all events')
        count.register('vetoed events')
        count.register('accepted events')

    def process(self, event):
        self.readCollections( event.input )
        self.counters.counter('events').inc('all events')

        collections={}
        for col in self.collections.keys():
            collections[col]=getattr(event, self.collections[col])

        ret=False
        if len(self.selections)==0 or len(self.collections)==0:
            ret=True
        selCnt={}
        for k,sel in enumerate(self.objectSels):
            nObjTypes=len(sel.keys())
            for objType in sel.keys():
                #print "---------------------------------- ",objType, sel[objType].num, len(collections[objType])
                cntObj=sel[objType].num
                hasEnoughObj=False                
                for obj in collections[objType]:
                    selected=self.selectObject(obj, collections[objType], sel[objType])
                    if selected:
                        cntObj-=1
                        #print "======>>> ",objType, cntObj
                        if cntObj<=0:
                          
                            hasEnoughObj=True
                            break

                if hasEnoughObj:
                    nObjTypes-=1

            if nObjTypes==0: #one full selection checked
                ret=True
                break
        
        #print "selected? ", ret
        if ret: self.counters.counter('events').inc('accepted events')
        return ret



    def parseSelection(self, selection):

        sel=selection.replace("_"," ")
        objects=sel.split()
        ret={}
        for obj in objects:
            #print obj
            scanline=re.compile(r"(\d+)(\D+)(\d+)$")
            scanlineXtra=re.compile(r"(\d+)(\D+)(\d+)([^()0-9]{1}[^()]+)$")
            scanlineId=re.compile(r"(\d+)(\D+)(\d+)(\(.+\))$")
            scanlineXtraId=re.compile(r"(\d+)(\D+)(\d+)([^()0-9]{1}.+)(\(.+\))$")
            m = re.match(scanline, obj) 
            mXtra = re.match(scanlineXtra, obj) 
            mId = re.match(scanlineId, obj) 
            mXtraId = re.match(scanlineXtraId, obj) 
            os=objectSelection()
            pid=""
            #print m, mXtra, mId, mXtraId
            if m:
                os.num=int(m.group(1))
                os.pid=m.group(2)
                os.ptThr=float(m.group(3))
                os.xtra=""
                os.cut=""
                #print "<<>> ", m.group(1), m.group(2), m.group(3)
            if mXtra:
                os.num=int(mXtra.group(1))
                os.pid=mXtra.group(2)
                os.ptThr=float(mXtra.group(3))
                os.xtra=mXtra.group(4)
                os.cut=""
                #print "<<=>> ", mXtra.group(1), mXtra.group(2), mXtra.group(3),mXtra.group(4)
            if mId:
                os.num=int(mId.group(1))
                os.pid=mId.group(2)
                os.ptThr=float(mId.group(3))
                os.xtra=""
                os.cut=mId.group(4)
            if mXtraId:
                os.num=int(mXtraId.group(1))
                os.pid=mXtraId.group(2)
                os.ptThr=float(mXtraId.group(3))
                os.xtra=mXtraId.group(4)
                os.cut=mXtraId.group(5)
                #print "===>> ", mXtraId.group(1), mXtraId.group(2), mXtraId.group(3),mXtraId.group(4),mXtraId.group(5)


            #print  " ----->>> ", os.xtra," // ", os.ptThr," // ", os.cut
            os.setFlags()
            ret[os.pid]=os

        return ret


    
    def selectObject(self, obj, colObj, sel):
        #print obj.p4().pt(), obj.charge(), sel.invPtThr, sel.ptThr, sel.OS, sel.SS, sel.invMassSel
        passPtCut = (obj.pt()>sel.ptThr) if not sel.invPtThr else (obj.pt()<sel.ptThr)
        if not passPtCut: 
            return False
        if hasattr(sel, "objSel"):
            if not sel.objSel(obj): 
                return False
        if not sel.checkMass and not sel.OS and not sel.SS:
            return True
        passCharge=False
        passMass=False
        for obj2 in colObj:
            if obj==obj2:
                continue
            passPtCut=(obj2.pt()>sel.ptThr) if not sel.invPtThr else (obj2.pt()<sel.ptThr)
            if not passPtCut: 
                continue
            if hasattr(sel, "objSel"):
                if not sel.objSel(obj): 
                    continue
            #print "combination ", obj.pt()," <> ", obj2.pt(), (obj.pt()>sel.ptThr), (obj.pt()<sel.ptThr), (obj2.pt()>float(sel.ptThr)), (obj2.pt()<float(sel.ptThr))
            if sel.OS and obj.charge()!=obj2.charge(): 
                passCharge=True
            if sel.SS and obj.charge()==obj2.charge(): 
                passCharge=True
            if not sel.OS and not sel.SS:
                passCharge=True
            
            if not sel.checkMass:
                passMass=True
            else:
                mass=(obj.p4()+obj2.p4()).M()
                if not sel.invMassSel and mass>=sel.mMin and mass<sel.mMax:
                    passMass=True
                if sel.invMassSel and (mass<sel.mMin or mass>sel.mMax):
                    passMass=True

            #print " charge ", passCharge, passMass
            if passCharge and passMass:
                return True

        return False
