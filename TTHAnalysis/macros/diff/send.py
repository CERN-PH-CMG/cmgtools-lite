import os

from optparse import OptionParser
parser = OptionParser(usage="%prog [options]")
# common options, independent of the flavour chosen
parser.add_option('--secureCopy',  dest='secureCopy', action='store_true', help='Friend tree with the needed information')
parser.add_option('--server',      dest='server',  type='string', help='Server')
parser.add_option('--outdir',      dest='outdir', type='string', help='Output dir')
parser.add_option('-f', '--force', dest='force', action='store_true', help='Override dictionary')
(options, args) = parser.parse_args()

userdict = {
    'helfaham' : [True, 'server02.fynu.ucl.ac.be', '~/public_html/ttH/temp_for_preapproval//2lss_ee_v6_2016_top_tagged'],
    'pvischia' : [True, 'server02.fynu.ucl.ac.be', '~/public_html/ttH/blahtemp'],
    # feel free to add users and servers based on your cluster configuration. Use 'False' instead of 'True' if you need cp instead of scp, and leave the server empty,
    # 'usernossh' : [False, '', '~/where_to_put/'],
} 

user = os.environ['USER']

secureCopy, server, outdir = userdict[user] if ( user in userdict.keys() and not options.force) else [options.secureCopy, options.server, options.outdir] 


cmd = '{copycommand} *.png {serverstring}{outdir}/'.format(copycommand='scp' if secureCopy else 'cp', serverstring='{user}@{server}:'.format(user=user,server=server) if secureCopy else '', outdir=outdir)


# I only print to screen, so that if you run you get a display of the command, and to execute it simply run by redirecting to a shell: python send.py | sh
print(cmd)
