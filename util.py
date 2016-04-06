import subprocess
import os

def capture(cmd):
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, shell=True)
  return p.communicate()[0]

def captureErr(cmd):
  FNULL = open(os.devnull, 'w')
  p = subprocess.Popen(cmd, stdout=FNULL,  stderr=subprocess.PIPE, shell=True)
  return p.communicate()[1]
  
import subprocess

def run_cmd(cmd):
  return subprocess.call(cmd, shell=True)

import platform

def syshost():
# hostA = platform.node().split('.')
  hostlong = capture("hostname --long")
  hostA = hostlong.split('.')
  idx = 1 #Si changed this from 2 to 1
  if (len(hostA) < 2):
    idx = 0
# print hostA[idx]

  return hostA[idx]
