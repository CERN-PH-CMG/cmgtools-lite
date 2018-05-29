from CMGTools.VVResonances.analyzers.VVBuilder import *


class TTBuilder(VVBuilder):
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TTBuilder,self).__init__(cfg_ana, cfg_comp, looperName)


    def makeJJ(self,event,fatJets,leptons):
        output=[]

        if len(fatJets)<2:
            return output

        topJets=sorted(fatJets,key=lambda x: abs(x.mass()-174.0))


        TT=Pair(topJets[0],topJets[1])
        if abs(TT.leg1.eta()-TT.leg2.eta())>1.3:
            return output

        #topology of the event (other stuff on top of tt)
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Tight')  ,leptons,0.3,[TT.leg1,TT.leg2],0.8)
        self.topology(TT,satteliteJets,leptons)

        if self.cfg_comp.isMC:
            self.substructureGEN(TT.leg2,event)
            self.substructureGEN(TT.leg1,event)


        output.append(TT)



        return output


    def makeJWb(self,event,fatJets,leptons):
        output=[]

        if len(fatJets)<2:
            return output


        top=min(fatJets,key=lambda x: abs(x.mass()-174.0))
        W=None
        WM=1000.0
        for j in fatJets:
            if deltaR(j.eta(),j.phi(),top.eta(),top.phi())>0.8:
                residual = abs(j.substructure.softDropJet.mass()-80.0)
                if residual<WM:
                    WM=residual
                    W=j

        if W==None:
            return output
        otherJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Tight')  ,leptons,0.3,[top,W],0.8)

        if len(otherJets)==0:
            return output

        #make all combos
        Wbs=[]
        for j in otherJets:
            Wbs.append(Pair(W,j))
        #The one closest to top mass
        bestWb = min(Wbs,key=lambda x:abs(x.mass()-174.0))

        #best fat jet other

        TT=Pair(bestWb,top)
        if abs(TT.leg1.eta()-TT.leg2.eta())>1.3:
            return output

        #topology of the event (other stuff on top of tt)
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Tight')  ,leptons+[TT.leg1.leg2],0.3,[TT.leg1.leg1,TT.leg2],0.8)
        self.topology(TT,satteliteJets,leptons)

        if self.cfg_comp.isMC:
            self.substructureGEN(TT.leg2,event)
            self.substructureGEN(TT.leg1.leg1,event)

        output.append(TT)
        return output



    def makeWbWb(self,event,wJets,leptons):
        output=[]
        if len(wJets)<2:
            return output

        otherJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Tight')  ,leptons,0.3,[wJets[0],wJets[1]],0.8)

        if len(otherJets)<2:
            return output

        #make all super combos
        Wbs=[]
        for w in [wJets[0],wJets[1]]:
            for j in otherJets:
                Wbs.append(Pair(w,j))

        #power of python
        TTs=[]
        for t1,t2 in itertools.combinations(Wbs,2):
            #remove overlap
            if deltaR(t1.leg1.eta(),t1.leg1.phi(),t2.leg1.eta(),t2.leg1.phi())<0.8:
                continue
            if deltaR(t1.leg2.eta(),t1.leg2.phi(),t2.leg2.eta(),t2.leg2.phi())<0.4:
                continue

            TTs.append(Pair(t1,t2))



        if len(TTs)==0:
            return output
        #The one closest to SUM(top mass)
        TT = min(TTs,key=lambda x:abs(x.leg1.mass()-174.0)+abs(x.leg2.mass()-174.0))

        #topology of the event (other stuff on top of tt)
        satteliteJets = self.selectJets(event.jets,lambda x: x.pt()>30.0  and x.jetID('POG_PFID_Tight')  ,leptons+[TT.leg1.leg2,TT.leg2.leg2],0.3,[TT.leg1.leg1,TT.leg2.leg1],0.8)
        self.topology(TT,satteliteJets,leptons)


        if self.cfg_comp.isMC:
            self.substructureGEN(TT.leg2.leg1,event)
            self.substructureGEN(TT.leg1.leg1,event)



        output.append(TT)
        return output





    def process(self, event):
        self.readCollections( event.input )
        #first create a set of four vectors to recluster jets later
        event.LVs = ROOT.std.vector("math::XYZTLorentzVector")()
        #load packed candidatyes
        cands = self.handles['packed'].product()

        #if use PUPPI weigh them or lese just pass through
        if self.doPUPPI:
            for c in cands:
                if c.pt()>13000 or c.pt()==float('Inf'):
                    continue;
                if c.puppiWeight()>0:
                    event.LVs.push_back(c.p4()*c.puppiWeight())
        else:
           for c in cands:
                if c.pt()>13000 or c.pt()==float('Inf'):
                    continue;
                event.LVs.push_back(c.p4())

        #if MC create the stable particles for Gen Jet reco and substructure
        if self.cfg_comp.isMC:
            event.genParticleLVs =ROOT.std.vector("math::XYZTLorentzVector")()
            for p in event.genParticles:
                if p.status()==1 and not (p.pdgId() in [12,14,16]):
                    event.genParticleLVs.push_back(p.p4())

        #Precategorize here

        leptons= filter(lambda x: (abs(x.pdgId())==11 and x.heepID) or (abs(x.pdgId())==13 and x.highPtIDIso ),event.selectedLeptons)
        fatJetsPre=self.selectJets(event.jetsAK8,lambda x: x.pt()>200.0 and abs(x.eta())<2.4 and x.jetID('POG_PFID_Tight')  ,leptons,1.0)



        #precalculate substructure for all fat jets
        fatJets=[]
        for fat in fatJetsPre:
            self.substructure(fat,event)
            if hasattr(fat,'substructure'):
                fatJets.append(fat)


        TT=self.makeJJ(event,fatJets,leptons)
        WbT=self.makeJWb(event,fatJets,leptons)
        WbWb=self.makeWbWb(event,fatJets,leptons)

        setattr(event,'TT'+self.cfg_ana.suffix,TT)
        setattr(event,'WbT'+self.cfg_ana.suffix,WbT)
        setattr(event,'WbWb'+self.cfg_ana.suffix,WbWb)
