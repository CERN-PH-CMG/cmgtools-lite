+
+from CMGTools.TTHAnalysis.tools.nanoAOD.higgsDecayFinder import higgsDecayFinder
+higgsDecay = lambda : higgsDecayFinder()
+
+from CMGTools.TTHAnalysis.tools.nanoAOD.mcMatcher import MCmatcher
+mcMatcher = lambda  : MCmatcher( 'LepGood','GenPart' )
+
+from CMGTools.TTHAnalysis.tools.nanoAOD.mvaVariables import MVAVariables
+mvaVars = lambda : MVAVariables()
+
+#lepmvaSeq = [ lepJetBTagDeepFlav, lepJetNDauChargedMVASel, mcMatcher , mvaVars]
