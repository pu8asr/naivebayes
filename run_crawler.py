#!/usr/local/bin/pypy

"""
Wrapper to ensure that a crawler script does not run for too long Usage:
    run_crawler.py <crawler-script> <crawler-args>
    
"""

import sys
import subprocess
import time

cmd = ' '.join(sys.argv[1:])
p = subprocess.Popen(cmd, shell=True)
sys.exit(0)
while True:
    time.sleep(60)
    retcode = p.poll()
    if retcode == None:
        p.kill()
        p = subprocess.Popen(cmd, shell=True)
        continue
    break
