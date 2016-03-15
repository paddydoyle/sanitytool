#!/bin/bash -l

#Luke Wilson
#Utility to determine if a user's environment is setup properly

BASEDIR=~build/apps/TACC-apps/env_check

VARIABLES="HOME WORK ARCHIVE ARCHIVER"
COMPILERS_INTEL="icc ifort mpif77 mpif90 mpicc mpicxx"
COMPILERS_AIX="xlc_r xlf90_r  mpxlf90_r mpcc_r mpCC_r"
COMPILERS_PATHSCALE="pathcc pathCC pathf90 pathf95"
LSF_UTILS="bsub showq lsuser bjobs bqueues ibrun"
SGE_UTILS="qsub qdel qstat qrsh qlogin"
LL_UTILS="llsubmit llcancel llclass llstatus llq llshowq"
TG_UTILS="cacl gx-request grid-proxy-init grid-proxy-info globusrun globus-job-run globus-job-submit globus-job-status"

#Parse command-line arguments
usage="Usage: env_check.sh [-noarchive] [-nojob] [-nohelp] [-basedir=<DIR>] [-? | -help]"
NOJOB=0
NOARCHIVE=0
for arg in "$@"
do
  case $arg in
    -nojob) NOJOB=1;;
    -noarchive) NOARCHIVE=1;;
    -basedir=*) BASEDIR=${arg:9};;
    -nohelp) NOHELP=1;;
    -?)	echo $usage
    	exit;;
    -help) echo $usage
           exit;;
  esac
done 

#Check system O/S
OS=`uname`
echo "Determining operating system...${OS}."

#Determine system scheduler
echo -n "Determining batch scheduler..."
if [ -e /opt/lsf ]; then
  SCHED="LSF"
  echo "LSF."
elif [ -e /usr/lpp/LoadL ]; then
  SCHED="LL"
  echo "LoadLeveler."
elif [ -e /opt/gridengine/bin ]; then
  SCHED="SGE"
  echo "SGE."
else
  echo "WARNING: No scheduler detected!"
fi


#Check to see what type of environment user has
TGUSER=0
echo -n "Checking user environment..."
if [ -e ~/.soft ]; then
  TGUSER=1
  echo "TG"
  if [ -e ~/.nosoft ]; then
    echo "WARNING: TG user has ~/.nosoft file."
  fi
else
  echo "UT"
fi

#Check the user's home quota
echo
quota
echo -n "Checking user quota..."
if quota | grep '*' > /dev/null 2>&1; then
  echo "ERROR: User is over quota."
  if ! [ -n "$NOHELP" ]; then
    echo "       Please remove files from your \$HOME directory."
  fi
  exit 1
else
  echo "ok."
fi

#Display user's project info
echo
if /usr/local/etc/atlogin 2>/dev/null | grep expired > $HOME/TACC_env_check_$$.prj; then
  echo "WARNING: The following projects have expired:"
  cat $HOME/TACC_env_check_$$.prj
  if ! [ -n "$NOHELP" ]; then
    echo
    echo "***Please use the TACC User Portal to request an allocation renewal."
    echo "   http://portal.tacc.utexas.edu/allocations"
  fi
fi
if /usr/local/etc/atlogin 2>/dev/null | grep overdrawn > $HOME/TACC_env_check_$$.prj; then
  echo "WARNING: The following projects are overdrawn:"
  cat $HOME/TACC_env_check_$$.prj
  if ! [ -n "$NOHELP" ]; then
    echo
    echo "***Please use the TACC User Portal to request an allocation increase."
    echo "   http://portal.tacc.utexas.edu/allocations"
  fi
fi
rm -f $HOME/TACC_env_check_$$.prj

#List the user's currently loaded modules
echo
module list 2>&1

#Display the user's $HOME and $WORK variabes
echo
echo "Checking standard variable values:"
for var in $VARIABLES; do
  echo -n "\$$var="
  eval echo \$"$var"
done

#Check to see if user was recently reaver'd
echo
echo "Checking for username \"`whoami`\" in /work/reaver:"
if ! ls /work/reaver 2>/dev/null | grep `whoami`; then
  echo "none."
fi

#Check for proper SSH keys
echo
echo -n "Checking SSH keys..."
if ! grep -F "`cat ~/.ssh/id_rsa.pub`" ~/.ssh/authorized_keys >/dev/null 2>&1; then
  echo "ERROR: ~/.ssh/id_rsa.pub not found in ~/.ssh/authorized_keys."
  if ! [ -n "$NOHELP" ]; then
    echo -n "                           "
    echo "Please append the contents of ~/.ssh/id_rsa.pub to ~/.ssh/authorized_keys."
    echo -n "                           "
    echo "(Example: lonestar2$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys)"
  fi
  exit 1
else
  echo "ok."
fi

#Check user's ability to rsh to archive
if ! [ $NOARCHIVE -eq 1 ]; then
  echo
  if [ -n "$ARCHIVER" ]; then
    echo -n "Checking for rsh capability to $ARCHIVER..."
    if ! (rsh $ARCHIVER exit) >/dev/null 2>&1; then
      echo "ERROR: Unable to connect to $ARCHIVER."
      if ! [ -n "$NOHELP" ]; then
        echo "       Please contact TACC Consulting to resolve this problem."
	echo "       Be sure to include a copy of this output in your ticket submission."
	echo "       https://portal.tacc.utexas.edu/consulting.php"
      fi
      exit 1
    else
      echo "ok."
    fi
  else
    echo "WARNING: \$ARCHIVER variable not set...skipping archive check"
  fi
else
  echo
  echo "WARNING: \"-noarchive\" option provided...skipping archive check"
fi

#Check for the presence of compilers
echo
echo "Checking for compilers: "
case $SCHED in
  LSF) COMPILERS=$COMPILERS_INTEL;;
   LL) COMPILERS=$COMPILERS_AIX;;
  SGE) COMPILERS=$COMPILERS_PATHSCALE;;
esac
for compiler in $COMPILERS; do
  echo -n "$compiler..."
  if ! type $compiler >/dev/null 2>&1; then
    echo "ERROR: \"$compiler\" not found."
    exit 1
  else
    which $compiler
  fi
done

echo

#Check for the presence of LSF/SGE/LL tools/utilities
echo -n "Checking for "
case $SCHED in
    LSF) echo -n "LSF "
         UTILS=$LSF_UTILS;;
     LL) echo -n "LoadLeveler "
         UTILS=$LL_UTILS;;
    SGE) echo -n "SGE "
         UTILS=$SGE_UTILS;;
esac
echo "utilities:"
for utils in $UTILS; do
  echo -n "$utils..."
  if ! type $utils >/dev/null 2>&1; then
    echo "ERROR: \"$utils\" not found."
    exit 1
  else
    which $utils
  fi
done

#Check for standard TG utilities
if [ $TGUSER -eq 1 ]; then
  echo
  echo "Checking for TG utilities:"
  for tg in $TG_UTILS; do
    echo -n "$tg..."
    if ! type $tg >/dev/null 2>&1; then
      echo "ERROR: \"$tg\" not found."
      exit 1
    else
      which $tg
    fi
  done
fi

#Perform test job submission
echo
if ! [ $SCHED = "LL" ]; then
  if ! [ $NOJOB -eq 1 ]; then
    echo "Submitting test job to check scheduling..."
    case $SCHED in
      LSF) cmd="bsub < $BASEDIR/env_check.lsf 2>&1";;
       LL) cmd="llsubmit $BASEDIR/env_check.ll 2>&1";;
      SGE) cmd="qrsh -pe mpich 4 $BASEDIR/env_check.sge 2>&1";;
    esac
    if ! eval $cmd; then
      echo "ERROR: Unable to submit sample program"
      exit 1
    fi
    KILLIT=0
    if ! (grep ^ENV_CHECK $HOME/TACC_env_check.out | diff $BASEDIR/env_check.master -) >/dev/null 2>&1; then
      echo "ERROR: Sample program did not complete correctly"
      KILLIT=1
    fi
    if ! [ $KILLIT -eq 1 ]; then
      cat $HOME/TACC_env_check.out
      echo "ok."
    fi
    rm -f $HOME/TACC_env_check.out $HOME/env_check.sge.p*
    if [ $KILLIT -eq 1 ]; then
      exit 1
    fi
  else
    echo "WARNING: \"-nojob\" option provided...skipping sample job submission."
  fi
else
  echo "LoadLeveler scheduler detected...skipping sample job submission."
fi

echo
echo "Environment passes TACC Criteria"
