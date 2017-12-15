from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

import PhysicsTools.HeppyCore.framework.config as cfg

class TriggerFilterMatch(object):
    def __init__(self, leg1_names, leg2_names, match_both_legs=True, triggers=None):
        self.leg1_names = leg1_names
        self.leg2_names = leg2_names
        # If true, requires both legs to be matched (if there are names)
        self.match_both_legs = match_both_legs
        # If set, will only attach this to passed trigger names; other,
        # TriggerAnalyzer will figure it out
        self.triggers = [] if triggers is None else triggers
    def __str__(self):
        return 'TriggerFilterMatch: leg1_names={leg1_names}, leg2_names={leg2_names}, match_both_legs={match_both_legs}'.format(leg1_names=self.leg1_names, leg2_names=self.leg2_names,
            match_both_legs=self.match_both_legs)

class TriggerInfo(object):
    def __init__(self, name, index, fired=True, prescale=1.):
        self.name = name
        self.index = index
        self.fired = fired
        self.prescale = prescale

        self.leg1_objs = []
        self.leg1_names = []
        self.leg2_objs = []
        self.leg2_names = []
        self.match_both = True
        self.match_infos = set()

    def __str__(self):
        return 'TriggerInfo: name={name}, fired={fired}, n_objects={n_o}'.format(
            name=self.name, fired=self.fired, n_o=len(self.match_infos))

class TriggerAnalyzer(Analyzer):
    '''Access to trigger information, and trigger selection. The required
    trigger names need to be attached to the components.'''

    def declareHandles(self):
        super(TriggerAnalyzer, self).declareHandles()

        if hasattr(self.cfg_ana, 'triggerResultsHandle'):
            myhandle = self.cfg_ana.triggerResultsHandle
            self.handles['triggerResultsHLT'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'edm::TriggerResults'
                )
        else:    
            trig_proc_name = 'HLT2' if 'reHLT' in self.cfg_comp.dataset else 'HLT'
            self.handles['triggerResultsHLT'] = AutoHandle(
                ('TriggerResults', '', trig_proc_name),
                'edm::TriggerResults'
                )

        if hasattr(self.cfg_ana, 'triggerObjectsHandle'):
            myhandle = self.cfg_ana.triggerObjectsHandle
            self.handles['triggerObjects'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'std::vector<pat::TriggerObjectStandAlone>'
                )
        else:    
            self.handles['triggerObjects'] =  AutoHandle(
                'selectedPatTrigger',
                'std::vector<pat::TriggerObjectStandAlone>'
                )
 
        if hasattr(self.cfg_ana, 'triggerPrescalesHandle'):
            myhandle = self.cfg_ana.triggerPrescalesHandle
            self.handles['triggerPrescales'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'pat::PackedTriggerPrescales'
                )
        else:    
            self.handles['triggerPrescales'] =  AutoHandle(
                'patTrigger',
                'pat::PackedTriggerPrescales'
                )
 
    def beginLoop(self, setup):
        super(TriggerAnalyzer,self).beginLoop(setup)

        self.triggerList = self.cfg_comp.triggers
        self.triggerObjects = []
        self.extraTriggerObjects = []
        if hasattr(self.cfg_comp, 'triggerobjects'):
            self.triggerObjects = self.cfg_comp.triggerobjects
        if hasattr(self.cfg_ana, 'extraTrig'):
            self.extraTrig = self.cfg_ana.extraTrig
        else:
            self.extraTrig = []
        if hasattr(self.cfg_ana, 'extraTrigObj'):
            self.extraTriggerObjects = self.cfg_ana.extraTrigObj

        self.vetoTriggerList = None

        if hasattr(self.cfg_comp, 'vetoTriggers'):
            self.vetoTriggerList = self.cfg_comp.vetoTriggers
            
        self.counters.addCounter('Trigger')
        self.counters.counter('Trigger').register('All events')
        self.counters.counter('Trigger').register('HLT')

        for trigger in self.triggerList:
            self.counters.counter('Trigger').register(trigger)
            self.counters.counter('Trigger').register(trigger + 'prescaled')


    def process(self, event):
        self.readCollections(event.input)
        
        event.run = event.input.eventAuxiliary().id().run()
        event.lumi = event.input.eventAuxiliary().id().luminosityBlock()
        event.eventId = event.input.eventAuxiliary().id().event()

        triggerBits = self.handles['triggerResultsHLT'].product()
        names = event.input.object().triggerNames(triggerBits)

        preScales = self.handles['triggerPrescales'].product()

        self.counters.counter('Trigger').inc('All events')

        trigger_passed = False

        if not self.triggerList:
            return True

        trigger_infos = []
        triggers_fired = []
        
        for trigger_name in self.triggerList + self.extraTrig:
            index = names.triggerIndex(trigger_name)
            if index == len(triggerBits):
                continue
            prescale = preScales.getPrescaleForIndex(index)
            fired = triggerBits.accept(index)

            trigger_infos.append(TriggerInfo(trigger_name, index, fired, prescale))

            if fired and (prescale == 1 or self.cfg_ana.usePrescaled):
                if trigger_name in self.triggerList:
                    trigger_passed = True
                    self.counters.counter('Trigger').inc(trigger_name)            
                triggers_fired.append(trigger_name)
            elif fired:
                print 'WARNING: Trigger not passing because of prescale', trigger_name
                self.counters.counter('Trigger').inc(trigger_name + 'prescaled')

        if self.cfg_ana.requireTrigger:
            if not trigger_passed:
                return False
        
        if self.cfg_ana.addTriggerObjects:
            triggerObjects = self.handles['triggerObjects'].product()
            for to in triggerObjects:
                to.unpackPathNames(names)
                for info in trigger_infos:
                    if to.hasPathName(info.name):
                        for match_info in self.triggerObjects + self.extraTriggerObjects:
                            if match_info.triggers:
                                if not info.name in match_info.triggers:
                                    continue
                            if any(n in to.filterLabels() for n in match_info.leg1_names):
                                info.leg1_objs.append(to)
                                info.leg1_names.append([n for n in to.filterLabels() if n in match_info.leg1_names])
                                info.match_both = match_info.match_both_legs
                                info.match_infos.add(match_info)

                            if any(n in to.filterLabels() for n in match_info.leg2_names):
                                info.leg2_objs.append(to)
                                info.leg2_names.append([n for n in to.filterLabels() if n in match_info.leg2_names])
                                info.match_both = match_info.match_both_legs
                                info.match_infos.add(match_info)

            for info in trigger_infos:
                if not info.fired: 
                    break

                if len(info.match_infos) == 0:
                    print 'Warning in TriggerAnalyzer, did not find trigger matching information for trigger path', info.name

                if len(info.match_infos) > 1:
                    print 'Warning in TriggerAnalyzer, found several matching trigger matching information pieces for trigger path', info.name
                    for match_info in info.match_infos: 
                        print match_info

                for match_info in info.match_infos:
                    if info.fired:
                        if match_info.leg1_names and not info.leg1_objs:
                            print 'Warning in TriggerAnalyzer, matching info associated but no leg1 objects set', info.name, match_info
                        if match_info.leg2_names and not info.leg2_objs:
                            print 'Warning in TriggerAnalyzer, matching info associated but no leg2 objects set', info.name, match_info

                                                
        event.trigger_infos = trigger_infos

        if self.cfg_ana.verbose:
            print 'run %d, lumi %d,event %d' %(event.run, event.lumi, event.eventId) , 'Triggers_fired: ', triggers_fired  
        if hasattr(self.cfg_ana, 'saveFlag'):
            if self.cfg_ana.saveFlag:
                setattr(event, 'tag', False)    
                setattr(event, 'probe', False)
                for trig in self.triggerList:
                    if trig in triggers_fired:
                        setattr(event, 'tag', True)    
                        break
                for trig in self.extraTrig:
                    if trig in triggers_fired:
                        setattr(event, 'probe', True)
                        break

        self.counters.counter('Trigger').inc('HLT')
        return True

    def __str__(self):
        tmp = super(TriggerAnalyzer,self).__str__()
        triglist = str(self.triggerList)
        return '\n'.join([tmp, triglist])

setattr(TriggerAnalyzer, 'defaultConfig', 
    cfg.Analyzer(
        class_object=TriggerAnalyzer,
        requireTrigger=True,
        usePrescaled=False,
        addTriggerObjects=True,
        # vetoTriggers=[],
    )
)
