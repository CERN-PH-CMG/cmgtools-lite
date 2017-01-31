import tauUtils
import string

"""
"""
        # Regions:
    # 
    # C:         3lC         SR-42            OSSF + 1tau
    # D:         3lD         SR-56            e mu tau
    # E:         3lE         SR-70            SS + 1 tau
    # F:         3lF         SR-80            A: OSSF, F: e/mu + 1tau
    # I:         3lI         SR-96            3l + 1tau

regions = {
    'C': ['3lC', 'SR-42', 'OSSF + 1tau'             ], 
    'D': ['3lD', 'SR-56', 'e mu tau'                ],
    'E': ['3lE', 'SR-70', 'SS + 1 tau'              ],
    'F': ['3lF', 'SR-80', 'A: OSSF, F: e/mu + 1tau' ],
    'I': ['4lI', 'SR-96', '3l + 1tau'               ]
    }

"""
"""



import optparse
# Command line options
usage = 'usage: %prog [--newData]'
parser = optparse.OptionParser(usage)
parser.add_option('-i', '--input',          dest='inputDir',       help='input directory',        default='/pool/ciencias/HeppyTrees/RA7/estructura/trees_8011_July5_allscans/',           type='string')
parser.add_option('-o', '--output',         dest='outputDir',      help='output directory',       default='~/www/susyRA7/',           type='string')
parser.add_option('-a', '--action',         dest='action',         help='which action to perform', default='tauopt', type='string')
parser.add_option('-s', '--subaction',      dest='subaction',      help='which subAction to perform', default='', type='string')
parser.add_option('-p', '--pretend',        dest='pretend',        help='only print commands out', action='store_true')

(opt, args) = parser.parse_args()

inputDir  = opt.inputDir
outputDir = opt.outputDir
action    = opt.action
subaction = opt.subaction
pretend   = opt.pretend
blind = '--flags "-X blinding"'


if(action=='generalplots'):
        cmd = 'python susy-interface/plotmaker.py 3l 3lA {inputDir} {outputDir} -l 12.9 --make data --plots br -o SR {blind} --pretend'.format(inputDir=inputDir,outputDir=outputDir,blind=blind)
        command(cmd, pretend)

elif(action=='tauopt'):
        
        mca='susy-ewkino/3l/taus/mca_taus.txt'
        
        
        for region in regions:
                if subaction and (region != subaction):
                        continue
                cmd = 'python susy-interface/plotmaker.py 3l {region} {inputDir} {outputDir} --mca {mca} -l 12.9 --make data --plots br -o {sr} {blind} --pretend'.format(region=regions[region][0],inputDir=inputDir,outputDir=outputDir,mca=mca,blind=blind,sr=regions[region][1])
                command(cmd,pretend)
        

print 'Everything is done now'
