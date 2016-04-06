from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture

class Compilers(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def name(self):
      return "Check compilers"

  def description(self):
    return "Check compilers:"

  def error(self):
     print("\033[1;31m%s\033[0m" %(self.error_message))

  def help(self):
      print("\tPlease check your $PATH again, compilers are missing.\n",
            "\tIf you unload the compilers on purpose, please ignore this test.\n")
  
  def execute(self):
      compilers=["gcc","g++","gfortran","icc","icpc","ifort","mpicc","mpicxx","mpif90"]
      
      Flag=True

      for compiler1 in compilers:
        typecmd="type %s" %compiler1 
        output=capture(typecmd)
#       print(output)
        if "not found" in output:
          Flag=False
	  self.error_message+="\tError: Compiler %s is not available at this time!\n" %compiler1
      return Flag     
