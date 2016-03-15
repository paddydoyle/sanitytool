from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture,syshost

class Schedulers(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def description(self):
    return "Check scheduler commands"

  def error(self):
    print(self.error_message)

  def execute(self):
      host=syshost()
      if host=="stampede":
        commands=["sbatch","squeue","scancel"]
      elif host=="ls4":
        commands=["qsub","qstat","qdel"]
      else:
        return True

      Flag=True

      for command1 in commands:
        typecmd="type %s" %command1 
        output=capture(typecmd)
        if "not found" in output:
          Flag=False
	  self.error_message+="        ERROR: Scheduler command \"%s\" is not available now!\n" %command1
      return Flag     

  def help(self):
      print("        Please check your $PATH again, scheduler commands are missing.\n")

  def name(self):
      return "Check scheduler commands"

