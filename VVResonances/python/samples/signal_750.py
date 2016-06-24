from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
signalSamples750=[] 

XToaaTobbtautau_10 = kreator.makeMCComponentFromEOS('XToaaTobbtautau_10', '/mh10/bbtautau/miniAOD/', '/store/cmst3/group/exovv/tosi/13TeV/Radion_X2hh/narrow_MX750/%s',".*root",1) 
signalSamples750.append(XToaaTobbtautau_10) 

XToaaTo4tau_10 = kreator.makeMCComponentFromEOS('XToaaTo4tau_10', '/mh10/tautautautau/miniAOD/', '/store/cmst3/group/exovv/tosi/13TeV/Radion_X2hh/narrow_MX750/%s',".*root",1) 
signalSamples750.append(XToaaTo4tau_10) 


