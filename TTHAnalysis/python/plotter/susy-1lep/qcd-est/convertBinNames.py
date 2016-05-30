#!/usr/bin/env python

'''
Macro to convert code bin names (ST1) to readable names (200 < ST < 250)
'''

import os
import sys
import glob

nameDict = {}

# ST bin names
nameDict['ST0'] = "$[200,250]$"
nameDict['ST1'] = "$[250,350]$"
nameDict['ST2'] = "$[350,450]$"
nameDict['ST3'] = "$[450,600]$"
nameDict['ST4'] = "$>$600"

# HT bin names
nameDict['HT0'] = "500 $<$ \\HT $<$ 750"
nameDict['HT1'] = "750 $<$ \\HT $<$ 1250"
nameDict['HT2'] = "\\HT $>$ 1250"

# Nj bins
nameDict['34j'] = "\\njet = 3,5"
nameDict['45j'] = "\\njet = 4,5"
nameDict['68j'] = "\\njet = 6-8"

def convLine(line):

    # exceptions
    if 'label' in line: return line

    cline = line

    for key in nameDict.keys():
        if key in line:
            #print 'Converting', key, nameDict[key]
            cline = line.replace(key,nameDict[key])

    return cline

def convert(tfile):

    for line in tfile.readlines():
        print convLine(line),

    return 1

if __name__ == "__main__":


    if len(sys.argv) > 1:
        txtName = sys.argv[1]
    else:
        txtName = "test.tex"

    if len(sys.argv) > 2:
        pfmt = sys.argv[2]
    else:
        pfmt = "text"

    print 'Going to convert', txtName

    with open(txtName) as tfile:
        convert(tfile)

    print 'Done'
