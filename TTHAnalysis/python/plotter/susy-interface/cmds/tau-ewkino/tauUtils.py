import os
import subprocess

"""
"""
def command(cmd, pretend):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]

        newCmd = 'python {cmd}'.format(cmd=p.split('python')[1])
        if pretend:
                print newCmd
        else:
                os.system(newCmd)
                
        print "Done."
"""
"""
