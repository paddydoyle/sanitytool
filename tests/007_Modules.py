from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture,captureErr
import os,sys

class Modules(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def description(self):
    return "Check Module environment"

  def error(self):
    print(self.error_message)

  def execute(self):
      Flag=True
      
      modcmd="tests/bash_module_test.bash"
      output=capture(modcmd)
      if "not found" in output:
	self.error_message+="        ERROR: Module is not defined."
        return False
      
      modcmd="tests/csh_module_test.csh"
      output=capture(modcmd)     
      if not output:
        self.error_message+="        ERROR: Module is not defined."
        return False

      unknown = "**UNKNOWN**"
      value = os.environ.get('LMOD_CMD',unknown)
      if (value == unknown):
	  self.error_message+="        ERROR: Module is not defined."
          return False             

      lmodcmd=os.environ['LMOD_CMD']
      mlcmd=lmodcmd + " python list"
      output=captureErr(mlcmd).split()
      module_need=["TACC"]
      for mod1 in module_need:
	if mod1 not in output:
	  self.error_message+="        ERROR: Module \"%s\" is not loaded.\n" %mod1
	  Flag=False
      
      return Flag
	
  def help(self):
      print("        Please check your module environment.\n")

  def name(self):
      return "Check Module Environment"

