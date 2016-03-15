from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture,syshost
from datetime import *

class Allocation(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def description(self):
    return "Check my allocation balance:"

  def error(self):
    print(self.error_message)

  def execute(self):
      userid=capture("whoami").rstrip()
###   userid="jkatzene"      #Fake test 
      
      host=syshost()
      if (host=="stampede" or host=="maverick"):
        TACC_ACC_DIR="/usr/local/etc/"
      elif host=="ls4":
        TACC_ACC_DIR="/sge_common/default/acct/map/"
      else:
        return True 

      proj_map=TACC_ACC_DIR+"project.map"
      projuser_map=TACC_ACC_DIR+"projectuser.map"
      projbalance_map=TACC_ACC_DIR+"projectbalance.map"
      usage_map=TACC_ACC_DIR+"usage.map"
 
#     grepcmd="grep %s %s" %(userid,projuser_map)
      grepcmd="""awk -v user=%s '$1 == user {print $0}' %s """ %(userid,projuser_map)
#      print(grepcmd)
      myprojects=capture(grepcmd).split()
#      print(myprojects)
      if len(myprojects) < 2:
	self.error_message+="        ERROR: "+"No valid allocation\n"
        return False
      
      Flag=False

      for proj in myprojects[1:]:
        grepcmd="grep %s %s" %(proj,proj_map)
#        print(grepcmd)
	proj_name_all=capture(grepcmd).split()
#	print(proj_name_all)
	if proj_name_all:
          proj_name=proj_name_all[0]
#         grepcmd="grep %s %s" %(proj_name,usage_map)
          grepcmd="awk -F: '{ if ($1==\"%s\") print}' %s" %(proj_name,usage_map)
#          print(grepcmd)
#          print(capture(grepcmd))
          usage_report=capture(grepcmd).split(":")
	  if len(usage_report) < 6:
	    print("        WARNING: Valid allocation detected.")
            continue
          exp_date=usage_report[3].split("-")
          exp_date_f=date(int(exp_date[0]), int(exp_date[1]), int(exp_date[2]))
          today = date.today()

          cur_bal=float(usage_report[6])
        # print("        My project '%s'; balance %s." %(proj_name,cur_bal))
	  if exp_date_f < date.today():
	    print("        WARNING: One of your project '%s' has expired." %proj_name[0])
          elif cur_bal < 0:
	    print("        WARNING: One of your project '%s' has negative balance %s." %(proj_name,cur_bal))
          else:
            Flag=True
      
      if Flag: 
	return True
      else:  
        self.error_message+="        ERROR: All your allocations are invalid"
      return Flag     

  def help(self):
      print("        Please renew your allocations.\n")

  def name(self):
    return "Check allocation balance"
