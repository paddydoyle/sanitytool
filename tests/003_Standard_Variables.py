from __future__ import print_function
from TestBase   import TestBase 
from util       import run_cmd, capture, syshost
import os

class Standard_Variables(TestBase): 
  
  #Keep the error message and print it when necessary
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def description(self):
    return "Report Standard Variables, and check file system availability:"

  def help(self):
    pass

  def error(self):
    print(self.error_message)
    exit

  def execute(self):
    # Different variable are necessary on different machines.
    standardVarT = {
      'stampede' : [ "HOME", "WORK", "STOCKYARD", "SCRATCH" ],
      'ls4'      : [ "HOME", "WORK", "SCRATCH" ],
      'maverick' : [ "HOME", "WORK", "STOCKYARD" ],
      }

    host = syshost()
    if host in standardVarT.keys():
      varA = standardVarT.get(host, standardVarT[host])
    else:
      self.error_message+="Not a known host."
      result = False
      return
 
    if not varA:
	return True

    result = True
    unknown = "**UNKNOWN**"

    for var in varA:
      value = os.environ.get(var,unknown)
      if (value == unknown):
	temp_string="        ERROR: Your $"+var+" is not defined.\n"
	self.error_message+=temp_string
        result = False
      elif( os.path.exists(value) ):
        pass
      else:
	temp_string="        ERROR: Your $" + var + " space(" + value + ") is not accessible at this time!\n"
	self.error_message+=temp_string
        result=False 	

#   fake test, ignore in the practical runs
#   mypath="/home/01225/siliu/no_exist_dir/"
#   if (os.path.exists(mypath) ):
#	print("my path exists")
#   else:
#	print("my path does not exist")
	
    return result

  def name(self):
    return "Standard Variables"
