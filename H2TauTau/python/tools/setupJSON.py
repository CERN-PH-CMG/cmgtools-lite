from CMGTools.H2TauTau.skims.applyJSON_cff import applyJSON
from CMGTools.RootTools.json.jsonPick import jsonPick
from CMGTools.H2TauTau.officialJSONS import jsonMap

def setupJSON( process ):
    print 'setting up JSON:'

    fileName = process.source.fileNames[0]
    json = jsonPick( fileName, jsonMap )
    print json
    applyJSON(process, json )
    return json
