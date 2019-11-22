#!/bin/bash
#$2 is something like 2016/Top-tagged/
scp $1 `whoami`@server02.fynu.ucl.ac.be:~/public_html/ttH/plots_104X_v6/$2
