import os, subprocess, sys

ERAs = [
    ('Run2015B',      (251162, 252126)),
    ('Run2015C_50ns', (254833, 254833)),
    ('Run2015C_25ns', (253888, 254914)),
    ('Run2015D',      (256629, 260627)),
]
PDs = { 
   'DoubleMuon' : { 'pd': '/{PD}/{ERA}-16Dec2015-v{VNUM}/MINIAOD', 'vnums':{} },
   'DoubleEG' : { 'pd': '/{PD}/{ERA}-16Dec2015-v{VNUM}/MINIAOD', 'vnums':{'Run2015D':'2'} },
   'MuonEG' : { 'pd': '/{PD}/{ERA}-16Dec2015-v{VNUM}/MINIAOD', 'vnums':{} },
   'SingleMuon' : { 'pd': '/{PD}/{ERA}-16Dec2015-v{VNUM}/MINIAOD', 'vnums':{} },
   'SingleElectron' : { 'pd': '/{PD}/{ERA}-16Dec2015-v{VNUM}/MINIAOD', 'vnums':{} },
}

evlist = open(sys.argv[1])
rls = []
rles = []
filesbypdera = {}
for rle in evlist:
    (run,lumi,event) = map(int, rle.split(":"))
    if (run,lumi,event) in rles: continue
    rles.append((run,lumi,event))
    if (run,lumi) in rls: continue
    rls.append((run,lumi))
    for (ename,(rmin,rmax)) in ERAs:
        if rmin <= run and run <= rmax:
            for pd,attrs in PDs.iteritems():
                if (ename,pd) not in filesbypdera: filesbypdera[(ename,pd)] = []
                vnum = '1'
                if ename in attrs['vnums']: vnum = attrs['vnums'][ename]
                dataset = attrs['pd'].format(ERA=ename,VNUM=vnum,PD=pd)
                out = subprocess.check_output(['das_client.py', '--query', 'file dataset={DATASET} run={RUN} lumi={LUMI}'.format(
                        DATASET=dataset, RUN=run, LUMI=lumi, PD=pd, ERA=ename)])
                for token in out.split():
                    if '.root' in token: filesbypdera[(ename,pd)].append(token)
            break
for (ename,pd),files in filesbypdera.iteritems():
    cfg = """
import FWCore.ParameterSet.Config as cms
process = cms.Process('cmsMerge')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(), 
    lumisToProcess = cms.untracked.VLuminosityBlockRange(),
    eventsToProcess = cms.untracked.VEventRange(),
)
process.source.fileNames = [ {FILES} ]
process.source.lumisToProcess = [ {LUMIS} ]
process.source.eventsToProcess = [ {EVENTS} ]
process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('{OUT}') )
process.end = cms.EndPath(process.out)
""".format(
    FILES=", ".join(map(repr, files)),
    LUMIS=", ".join("'%d:%d'" % rl for rl in rls),
    EVENTS=", ".join("'%d:%d:%d'" % rle for rle in rles),
    OUT="picked_%s_%s.root" % (pd,ename)
)
    stream = open("pick_%s_%s.py" % (pd,ename), 'w')
    stream.write(cfg)
    print "Wrote to pick_%s_%s.py" % (pd,ename)
#for PD in Double{EG,Muon} MuonEG; do grep $PD files | sort | uniq | ~/pl/cmsMerge.pl --out=$PD-Run2015D_SR.root | cat - select | tee slurp_$PD-Run2015D_SR.py; done
#cat events.txt | awk 'BEGIN{ORS=""; print "process.source.eventsToProcess = cms.untracked.VEventRange(["; ORS=", ";} {print "\""$1"\""; }  END{ORS=""; print "])\n"; }' | tee select
#cut -d: -f1-2  events.txt | sort | uniq  | awk 'BEGIN{ORS=""; print "process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange(["; ORS=", ";} {print "\""$1"\""; }  END{ORS=""; print "])\n"; }'  | tee -a select
#for PD in Double{Muon,EG} MuonEG; do v=1; [[ "$PD" == "DoubleEG" ]] && v=2; cat events.txt  | awk -F: "{ print \"dasql \\\"file dataset=/$PD/Run2015D-16Dec2015-v$v/MINIAOD run=\"\$1\" lumi=\"\$2\"\\\" | grep root \"  } " | tee fetch.$PD; done


