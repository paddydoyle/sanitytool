from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture,syshost

class Quota(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def name(self):
    return "Check quota for $HOME and $WORK spaces:"

  def description(self):
    return "Check quota for $HOME and $WORK spaces:"

  def error(self):
     print("\033[1;31m%s\033[0m" %(self.error_message))

  def help(self):
      print("\tPlease remove unnecessary files to clean your spaces.\n")

  def execute(self):
      userid=capture("whoami").rstrip()
      host=syshost()
     
      if (host=="stampede" or host=="ls5"):
        spaces=["/home1","/work"]
      elif host=="ls4":
	spaces=["/home1","/work"]
      elif (host=="maverick"):
	spaces=["/home","/work"]
      else:
        return True

      Flag=True

      for space in spaces:
        if ( (host=="ls4" and space=="/home1") or (host=="maverick" and space=="/home") or (host=="ls5" and space=="/home1")):
          quotacmd="quota"
          rawinfo=capture(quotacmd).split("\n")
	  if len(rawinfo)<3:
            return False
          quotainfo=rawinfo[-2].split()     
##	  print(quotainfo[0],quotainfo[2],quotainfo[3],quotainfo[5])          
##        print(quotainfo)
	  if len(quotainfo) <6:
            self.error_message+="\tError: "+"No valid quota report\n"
            return False
          if float(quotainfo[0]) >= float(quotainfo[2])*0.95 :
            Flag=False
            self.error_message+="\tError: You are over/close to the disk limit under %s.\n" %space
          if float(quotainfo[3]) >= float(quotainfo[5])*0.95 :
            Flag=False
            self.error_message+="\tError: You are over/close to the inode limit under %s.\n" %space

        else:
          lfscmd="lfs quota -u %s %s" %(userid,space)
        ##  print(lfscmd)
	  quotainfo=capture(lfscmd).split("\n")[2].split()
	  quotainfo[5]=quotainfo[5].strip("*")
	  quotainfo[1]=quotainfo[1].strip("*")
##	  print(quotainfo[1], quotainfo[3], quotainfo[5], quotainfo[7]
##	  print(quotainfo)
	  if len(quotainfo) <8:
	    self.error_message+="\tError: "+"No valid quota report\n"
            return False
	
	  if float(quotainfo[1]) >= float(quotainfo[3])*0.95 :
            Flag=False
	    self.error_message+="\tError: You are over/close to the disk limit under %s.\n" %space   
          if float(quotainfo[5]) >= float(quotainfo[7])*0.95 :	
            Flag=False
            self.error_message+="\tError: Your are over/close to the inode limit under %s.\n" %space 
          
      return Flag     
