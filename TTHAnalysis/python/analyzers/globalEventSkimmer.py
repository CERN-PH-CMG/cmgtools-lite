from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import itertools,re

class objectSelection():
    def __init__(self):

        #string based
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
        self.maxObj=10000
        self.mMin=-1
        self.mMax=1000000
        self.invMassSel=False
        self.vetoDS=False

        #function based
        self.isFctSel=False
        self.selFunctions=[]


    def setFlags(self, compName):
        if self.cut!="":
            self.objSel= eval("lambda "+self.pid+": "+self.cut)

        if self.xtra=="":
            return

        options=self.xtra[1:-1].split(':')
        for opt in options:
            if opt=="!pt":
                self.invPtThr=True
            if opt=="os":
                self.OS=True
            if opt=="ss":
                self.SS=True
            if opt=="maxObj":
                scanMaxObj=re.compile(r"maxObj(\d+)")
                m=re.match(scanMaxObj, opt)
                if m:
                    self.maxObj=int(m.group(1))
            if opt[0]=="M" or opt[0:1]=="!M":
                self.checkMass=True
                if opt[0]=="!":
                    self.invMassSel=True
                scansel1B=re.compile(r"M(\d+)([<>])")
                scansel2B=re.compile(r"M(\d+)[-](\d+)")
                r1=re.match(scansel1B, opt)
                r2=re.match(scansel2B, opt)
                if r1:
                    if r1.group(2)=="<":
                        self.mMax=float(r1.group(1))
                    if r1.group(2)==">":
                        self.mMin=float(r1.group(1))
                if r2:
                    self.mMin=float(r2.group(1))
                    self.mMax=float(r2.group(2))
            if "DS" in opt:
                veto=True if opt[0]=="!" else False
                scanDS1=re.compile(r"\WDS_(\w+)")
                scanDS2=re.compile(r"\WDS (\w+)")
                m1=re.match(scanDS1, opt)
                m2=re.match(scanDS2, opt)
                DS=""
                if m1:
                    DS=str(m1.group(1))
                elif m2:
                    DS=str(m2.group(1))
                else:
                    DS=opt[2:] if opt[0]!="!" else opt[3:]
               
                if (DS==compName and veto) or (DS!=compName and not veto):
                    self.vetoDS=True

class globalEventSkimmer( Analyzer ):
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(globalEventSkimmer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.collections=cfg_ana.collections if hasattr(cfg_ana, "collections") else {}
        self.selections= cfg_ana.selections if hasattr(cfg_ana, "selections") else []
        self.objectSels=[]
        for selection in self.selections:
            if not isinstance(selection, basestring):
                psel=objectSelection()
                psel.isFctSel=True
                psel.selFunction=selection
                self.objectSels.append(psel)
                continue

            psel=self.parseSelection(selection, self.cfg_comp.name)
            self.objectSels.append(psel)


    def declareHandles(self):
        super(globalEventSkimmer, self).declareHandles()

    def beginLoop(self, setup):
        super(globalEventSkimmer,self).beginLoop(setup)
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
            if "met" in col: #self.collections[col]=="met":
                collections[col]=[getattr(event,self.collections[col])]
            else:
                collections[col]=getattr(event, self.collections[col])

        ret=False
        if len(self.selections)==0 or len(self.collections)==0:
            ret=True
        selCnt={}

        for sel in self.objectSels:
            
            #function based skim selection
            if not isinstance(sel,dict): 
                if sel.isFctSel:
                    valid=True
                    if sel.selFunction(event):
                        ret=True    
                    continue

            #string based skim selection
            nObjTypes=len(sel.keys())
            for s in sel.keys():
                objType=sel[s].pid
                if sel[s].vetoDS:
                    nObjTypes-=1
                    continue
                
                cntObj=sel[s].num
                cntMaxObj=sel[s].maxObj
                hasEnoughObj=False    
                tooMuchObj=False 
                for obj in collections[objType]:
                    selected=self.selectObject(obj, collections[objType], sel[s])
                    if selected:
                        cntObj-=1
                        cntMaxObj-=1
                        if cntObj<=0 :
                            hasEnoughObj=True
                            if cntMaxObj>1000:
                                break
                        if cntMaxObj<0:
                            tooMuchObj=True
                            break

                if hasEnoughObj:
                    nObjTypes-=1
                if tooMuchObj:
                    nObjTypes+=1
                    

            if nObjTypes==0: #one full selection checked
                ret=True
                break
        
        #print "selected? ", ret
        if ret: self.counters.counter('events').inc('accepted events')
        return ret



    def parseSelection(self, selection, compName):

        sel=selection
        scanopt=re.compile(r".+(\[.+\]).+")
        scansel=re.compile(r".+(\(.+\)).+")
        so=re.match(scanopt, sel)
        ss=re.match(scansel, sel)
        sel=sel.replace("_"," ")
        if so:
            sel=re.sub(r'\[.*?\]',so.group(1),sel)
        if ss:
            sel=re.sub('\(.*?\)',ss.group(1),sel)

        objects=sel.split()
        ret={}
        for obj in objects:
            scanline=re.compile(r"(\d+)(\D+)(\d+)$")
            scanlineXtra=re.compile(r"(\d+)(\D+)(\d+)(\[[^()0-9]{1}[^()]+\])$")
            scanlineId=re.compile(r"(\d+)(\D+)(\d+)(\(.+\))$")
            scanlineXtraId=re.compile(r"(\d+)(\D+)(\d+)(\[[^()0-9]{1}.+\])(\(.+\))$")
            m = re.match(scanline, obj) 
            mXtra = re.match(scanlineXtra, obj) 
            mId = re.match(scanlineId, obj) 
            mXtraId = re.match(scanlineXtraId, obj) 
            os=objectSelection()
            pid=""
            #print selection,"-->",m, mXtra, mId, mXtraId
            if m:
                os.num=int(m.group(1))
                os.pid=m.group(2)
                os.ptThr=float(m.group(3))
                os.xtra=""
                os.cut=""
            if mXtra:
                os.num=int(mXtra.group(1))
                os.pid=mXtra.group(2)
                os.ptThr=float(mXtra.group(3))
                os.xtra=mXtra.group(4)
                os.cut=""
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


            #print " ----->>> ",os.pid, "// ", os.xtra," // ", os.ptThr," // ", os.cut
            os.setFlags(compName)
            ret[obj]=os

        return ret


    
    def selectObject(self, obj, colObj, sel):

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

            if passCharge and passMass:
                return True

        return False
