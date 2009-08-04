#!/bin/bash
################################################################################
#                          gLite Node Setup
#
# Automatic setup script for node installation of the gLite Middleware.
#
# Authors: Andrew Elwell (andrew.elwell@cern.ch)
#          David Horat (david.horat@cern.ch)
#
# Exit values:
#  0 - OK
#  1 - You must input all mandatory parameters
#  2 - Unknown architecture
#  3 - yum failed to update the system
#  4 - Input files do not exist
#  5 - Problem installing Java from the CERN-only repo
#  6 - Problem installing BitFace in SL5
#  7 - Problem starting AFS in SL5
#  8 - Problem checking out latest YAIMGEN version from $YAIMGENREPO
#  9 - yaimgen failed. Check the logs in $YAIMGEN/yaimgen.out
# 10 - Patch #$PATCHNUMBER installation failed
# 11 - Could not copy site-info.def from $SITEINFODEFURL
# 12 - YAIM failed trying to configure $YAIMNODE
# 13 - Tests based on the script $TESTFILE FAILED
# 14 - Test script $TESTFILE does not exist
# 15 - Configuration script $CONFIGSCRIPT FAILED
# 16 - Configuration script $CONFIGSCRIPT does not exist
#
################################################################################

# A healthy bash shell starts from scratch :)
`unalias -a`

################################################
# Functions
################################################

# Give run time in seconds, error message and exit
function quit {
  RUNTIME=$[`date +%s` - $STARTTIME]
  echo
  echo "This program took $RUNTIME seconds to run"
  if [ $pass ]; then
    echo "The generated password for your services is: $pass"
  fi
  echo "ERROR $1: $2"
  echo "IT'S BUSINESS TIME!"
  exit $1
}

# Write the MOTD file based on current parameters. 
function writeMOTD {
  MOTD='/etc/motd'
  echo 'Writing Message Of The Day (MOTD)'
  echo --------------------------------- > $MOTD

  case $ARCH in
    i*86)
      echo "INFO: Arch:       32 Bit" >> $MOTD
    ;;

    x86_64)
      echo "INFO: Arch:       64 Bit" >> $MOTD
    ;;

   *)
      echo "ERROR - Unknown Architecture ($ARCH)"
      quit 2 'Unknown architecture'
    ;;
  esac

  case $RHVER in
   4)
      echo "INFO: Base:       SL(C)4" >> $MOTD
   ;;
   5)
      echo "INFO: Base:       SL(C)5" >> $MOTD
   ;;
  esac

  echo "INFO: REPO:       $REPO" >> $MOTD
  echo "INFO: Middleware: $MWARE" >> $MOTD
  echo "INFO: Hostname:   $HOSTNAME" >> $MOTD
  echo "MOTD brought to you by gLite Node Setup v$VERSION" >> $MOTD
}

# Display usage of this script
function usage {
    echo "Usage: `basename $0` -r repo -m mware [-p number] [-c file] [-y node] [-t file]"
    echo "Automatic setup script for node installation of the gLite Middleware."
    echo
    echo "  -r: Repository type. Can be prod or cert."
    echo "  -m: Middleware node. E.g. glite-BDII, glite-LFC_mysql"
    echo "      More for gLite 3.1: https://twiki.cern.ch/twiki/bin/view/LCG/GenericInstallGuide310"
    echo "      More for gLite 3.2: https://twiki.cern.ch/twiki/bin/view/LCG/GenericInstallGuide320"
    echo "  -p: Patch number to install before YAIM configuration"
    echo "      More: https://savannah.cern.ch/"
    echo "  -c: Run a configuration script before running YAIM"
    echo "  -y: Run YAIM specifying the node type. E.g. glite-BDII_top"
    echo "      More: https://twiki.cern.ch/twiki/bin/view/LCG/YaimGuide400"
    echo "  -t: Run automatic tests based on the yaim node"
    echo "      E.g.: test-glite-BDII_top.sh"
    echo
    echo "Example: `basename $0` -r prod -m glite-BDII -p 3114 -y glite-BDII_top -t test_glite-BDII_top.sh"
    echo
    echo "Report bugs to ... DO IT YOURSELF! :)"
}


################################################
# Parameters and initialization
################################################

# Check for expected args
if [ $# -eq 0 ]; then
  usage
  exit
fi

# Parse command line arguments
while getopts "r:m:p:c:y:t:" option; do
  case ${option} in
      r)
        REPO=${OPTARG}
      ;;
      m)
        MWARE=${OPTARG}
      ;;
      p)
        PATCHNUMBER=${OPTARG}
      ;;
      c)
        CONFIGSCRIPT=${OPTARG}
      ;;
      y)
        YAIMNODE=${OPTARG}
      ;;
      t)
        TESTFILE=${OPTARG}
      ;;
  esac
done
shift $(($OPTIND - 1))

# Parameters
YAIMGEN='/root/yaimgen'
YAIMGENREPO='http://svnweb.cern.ch/guest/yaimgen/yaimgen2/tags/rel-0_1/'
BITFACE='ca_BitFace-0.4-5.noarch.rpm'
SITEINFODEFURL='http://horat.web.cern.ch/horat/glite/site-info.def'
SITEINFODEFFILE='/etc/yaim/site-info.def'

# Fixed variables
VERSION='0.4'
HOST=`hostname`
ARCH=`uname -p`
RHVER=`cat /etc/redhat-release |  awk -F'release ' '{print $2}' | cut -c 1`
STARTTIME=`date +%s`

# Check for mandatory command line parameters
if [ ! $REPO -o ! $MWARE ]; then
  usage
  quit 1 'You must input all mandatory parameters'
fi


################################################
# Main
################################################

# Welcome message and write the MOTD
echo "Welcome to gLite Node Setup v$VERSION"
date
# YAIM IS ALSO WRITING A MOTD, SO MAYBE WE SHOULD GET THIS OUT
#writeMOTD

# Check input files and print debug information
echo "Command line parameters:"
echo "   REPO      = $REPO"
echo "   MWARE     = $MWARE"
if [ $CONFIGSCRIPT ]; then
  if [ ! -f $CONFIGSCRIPT ]; then
    quit 4 "$CONFIGSCRIPT file does not exist"
  fi
  echo "   CONFIG    = $CONFIGSCRIPT"
fi
if [ $YAIMNODE ]; then
  echo "   YAIMNODE  = $YAIMNODE"
fi
if [ $PATCHNUMBER ]; then
  echo "   PATCH     = $PATCHNUMBER"
fi
if [ $TESTFILE ]; then
  if [ ! -f $TESTFILE ]; then
    quit 4 "$TESTFILE file does not exist"
  fi
  echo "   TEST FILE = $TESTFILE"
fi

# YAIM STILL NEEDS AN AFS TOKEN!
echo "AFS token still needed by YAIMGEN"
kinit horat
if [ $? -ne 0 ]; then
  echo 'Wrong password'
  exit 100
fi
aklog

# Append $MWARE to metapakage list so tests can pick it up later
echo $MWARE >> /etc/glite-metapackages
# Add warning about keeping metapackage list up to date.
echo -e "\nIf you add any extra metapackages by hand, be sure to append the"
echo -e "details to /etc/glite-metapackages so the testsuite picks them up\n"

# get RPM to show $arch
echo "%_query_all_fmt   %%{name}-%%{version}-%%{release}.%%{arch}" >> /root/.rpmmacros

# Update the system
yum -y update
if [ $? -ne 0 ]; then
  quit 3 "yum failed to update the system."
fi
TEMPRUNTIME=$[`date +%s` - $STARTTIME]
echo -e "\n yum update took $TEMPRUNTIME seconds to run"
echo "INFO: ${MWARE}_${ARCH} ($REPO)"

# Lets clean up /etc/yum.repos.d
rm -f /etc/yum.repos.d/*.sh

# Give the option to snarf CERN packaged goodies (disabled by default)
SLCVER=slc$RHVER\X
cat << EOF > /etc/yum.repos.d/CERN-only.repo
[CERN-only]
name=SLC cernonly packages
baseurl=http://linuxsoft.cern.ch/onlycern/$SLCVER/\$basearch/yum/cernonly
enabled=0
protect=1
EOF

# Make concrete installation depending on platform
case $RHVER in
	4)
    # Install Java from CERN-only
    yum -y --enablerepo CERN-only install java-1.5.0-sun java-1.5.0-sun-devel
    if [ $? -ne 0 ]; then
      quit 5 'Problem installing Java from the CERN-only repo in SL4.'
    fi
  ;;

  5)
    echo "Downloading lcg-CA and DAG repo files"
    cd /etc/yum.repos.d/
    wget http://grid-deployment.web.cern.ch/grid-deployment/glite/repos/3.2/dag.repo
    wget http://grid-deployment.web.cern.ch/grid-deployment/glite/repos/3.2/lcg-CA.repo
    cd -
    
    echo "Disabling DAG repo because it conflicts when doing a yum update"
    cd /etc/yum.repos.d/
    sed 's/enabled=1/enabled=0/g' dag.rep > dag.rep.bak
    cp -u dag.rep.bak dag.rep
    cd -

    if [ $REPO == "prod" ] ; then
      echo "Downloading production repository"
	    cd /etc/yum.repos.d/
	    wget http://grid-deployment.web.cern.ch/grid-deployment/glite/repos/3.2/$MWARE.repo
	    cd - 
    fi

    echo "Installing ca_BitFace"
    rpm -Uvh http://grid-deployment.web.cern.ch/grid-deployment/glite/cert/3.1/internal/sl4/x86_64/RPMS.cert-updates/$BITFACE
    if [ $? -ne 0 ]; then
      quit 6 'Problem installing BitFace in SL5.'
    fi

    # Tidy up installed crap on vnode
    yum -y erase java-gcj-compat subversion xdelta
    yum -y install rsync man lcg-CA subversion

    # AFS 
    service afs start
    if [ $? -ne 0 ]; then
      quit 7 'Problem starting AFS in SL5.'
    fi
  ;;
esac

##### COMMON TO ALL

# Install Grid Security Certificates
# This should be done already in the machine (Ricardo in next version)
mkdir -p /etc/grid-security/
cp /opt/certs/$HOST/* /etc/grid-security/

# Blow away old yaimgen and get the SVN version
rm -rf yaimgen
svn co $YAIMGENREPO $YAIMGEN
if [ $? -ne 0 ]; then
  quit 8 "Problem checking out latest YAIMGEN version from $YAIMGENREPO."
fi

# HACK: yaimgen.conf is SL5 - we need to change for SL4
if [ $RHVER = 4 ] ; then
	sed -i 's/YG_GLITEVERSION="3.2"/YG_GLITEVERSION="3.1"/' $YAIMGEN/yaimgen.conf
	sed -i 's/YG_SLTAG=sl5/YG_SLTAG=sl4/' $YAIMGEN/yaimgen.conf
	sed -i 's/export YG_DEFAULTS_REPOS="lcg-CA dag"/export YG_DEFAULTS_REPOS="dag jpackage lcg-CA"/' $YAIMGEN/yaimgen.conf
	sed -i 's/export YG_DEFAULTS_PACKAGES="lcg-CA"/export YG_DEFAULTS_PACKAGES="dag jpackage lcg-CA"/' $YAIMGEN/yaimgen.conf
fi

# Prepare YAIMGEN input file
cat > $YAIMGEN/yaimgen.in << EOF
YG_REPO="$REPO"
YG_TARGETS="$MWARE"
YG_CERT_INST="no"
EOF

# Run YAIMGEN
cd $YAIMGEN
./yaimgen.sh preconfigure yaimgen.in
if [ $? -ne 0 ]; then
  quit 9 "yaimgen failed. Check the logs in $YAIMGEN/yaimgen.out"
fi
cd -

# Download a site-info.def for YAIM or keep the existing one
if [ ! -f $SITEINFODEFFILE ]; then
  rm -f $SITEINFODEFFILE
else
  mkdir -p /etc/yaim/
fi
cd /etc/yaim/
wget -nv $SITEINFODEFURL
if [ $? -ne 0 ]; then
  quit 11 "Could not retrieve site-info.def from $SITEINFODEFURL"
fi
pass=$RANDOM-$RANDOM
sed -i 's/{{PLACEHOLDER}}/'$pass'/' site-info.def
sed -i 's/{{HOST}}/'$HOST'/' site-info.def
echo "$file copied from $SITEINFODEFURL"
cd -

# Patch installation
if [ $PATCHNUMBER ]; then
  ./glite_getpatch.sh -p $PATCHNUMBER
  if [ $? -ne 0 ]; then
    quit 10 "Patch #$PATCHNUMBER installation failed"
  fi
fi

# Configuration script
if [ $CONFIGSCRIPT ]; then
  if [ -f $CONFIGSCRIPT ]; then
    chmod +x $CONFIGSCRIPT
    ./$CONFIGSCRIPT
    if [ $? -ne 0 ]; then
      quit 15 "Configuration script $CONFIGSCRIPT FAILED"
    fi
  else
    quit 16 "Configuration script $CONFIGSCRIPT does not exist"
  fi
fi

# YAIM configuration
if [ $YAIMNODE ]; then
  echo "Running YAIM ..."
  /opt/glite/yaim/bin/yaim -c -s /etc/yaim/site-info.def -n $YAIMNODE
  if [ $? -ne 0 ]; then
    quit 12 "YAIM failed trying to configure $YAIMNODE"
  fi
else
  echo -e "\nNOW RUN YAIM:"
  echo "/opt/glite/yaim/bin/yaim -c -s /etc/yaim/site-info.def -n [NODE TYPE]"
  echo "eg: /opt/glite/yaim/bin/yaim -c -s /etc/yaim/site-info.def -n glite-BDII_top"
  echo "Your current middleware node is: $MWARE"
fi

# Testing
if [ $TESTFILE ]; then
  if [ -f $TESTFILE ]; then
    chmod +x $TESTFILE
    ./$TESTFILE
    if [ $? -ne 0 ]; then
      quit 13 "Tests based on the script $TESTFILE FAILED"
    fi
  else
    quit 14 "Test script $TESTFILE does not exist."
  fi
fi

# Information on how to create a user if it is needed
echo -e "\nIf you need to create a user, run:"
echo 'groupadd -g 2648 gr'
echo 'useradd -g 2648 -d /afs/cern.ch/user/[FIRSTLETTER]/[USER] -u 29625 [USER]'

# Bye messages and log
RUNTIME=$[`date +%s` - $STARTTIME]
echo -e "\n`basename $0` took $RUNTIME seconds to run"
if [ $pass ]; then
  echo "The generated password for your services is: $pass"
fi
echo 'OK!'
exit 0
