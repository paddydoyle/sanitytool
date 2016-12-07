from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture,syshost
import getpass

class Block_User(TestBase):
 
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def name(self):
    return "Check user's queue accessibility"

  def description(self):
    return "Check user's queue accessibility (Stampede Only):"

  def error(self):
     print("\033[1;31m%s\033[0m" %(self.error_message))

  def help(self):
      print("\tYou are blocked by the system administratots, please contact TACC for help.\n")

  def execute(self):
    host = syshost()
    if host!="stampede":
      return True

    userid=getpass.getuser()
    
    grepcmd1="""awk '/ALL = /,/ALL = /' /etc/slurm/tacc_filter_options | awk '{print substr($0,7,length($0)-7)}' | awk -v user=%s 'BEGIN {FS=" !!"}; {for (i=1; i<=NF; i++) if($i == user) {print $0}}'""" %userid      
#    print(grepcmd1)
    myrecord1=capture(grepcmd1).split('\n')
#    print(myrecord1)
    
    grepcmd2="""awk '($1=="largemem")' /etc/slurm/tacc_filter_options | awk '{gsub(/ /, "", $0);print substr($0,12, length($0)-12)}' |  awk -v user=%s 'BEGIN {FS="!!"}; {for (i=1; i<=NF; i++) if ($i == user) {print $0}}'""" %userid
#    print(grepcmd2)
    myrecord2=capture(grepcmd2).split('\n')
#    print(myrecord2)	

    grepcmd3="""awk '($1=="normal-mic" || $1=="normal-2mic")' /etc/slurm/tacc_filter_options | awk '{gsub(/ /, "", $0); print substr($0,14, length($0)-14)}' |  awk -v user=%s 'BEGIN {FS="!!"}; {for (i=1; i<=NF; i++) if ($i == user) {print $0}}'""" %userid
#    print(grepcmd3)
    myrecord3=capture(grepcmd3).split('\n')
#    print(myrecord3)
    
    myrecord=myrecord1 + myrecord2 + myrecord3
#    print(myrecord) 
   
    for ss in myrecord1:
	if ss and not ss.strip().startswith('#'):
		self.error_message+="\tError: You are blocked from general submission.\n"
		return False
    for ss in myrecord2:
        if ss and not ss.strip().startswith('#'):
                self.error_message+="\tError: You are blocked from largemem queue submission.\n"
                return False

    for ss in myrecord3:
        if ss and not ss.strip().startswith('#'):
                self.error_message+="\tError: You are blocked from mic queue submission.\n"
                return False
    
    return True
