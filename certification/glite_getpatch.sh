#!/bin/bash
################################################################################
#                          gLite Get Patch Utility
#
# Automatic patch installation.
#
# Authors: Andrew Elwell (andrew.elwell@cern.ch)
#          David Horat (david.horat@cern.ch)
#
# Exit values:
#  0 - OK
#  1 - No patch number specified
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
  echo -e "\nThis program took $RUNTIME seconds to run"
  echo -e "ERROR $1: $2"
  exit $1
}

function usage {
    echo "Usage: `basename $0` -p patchnumber"
    echo "Automatic patch installation."
    echo
    echo "  -p: Specify the patch number to install."
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
while getopts "p:" option; do
  case ${option} in
      p)
        PATCH=${OPTARG}
      ;;
  esac
done
shift $(($OPTIND - 1))

# Fixed variables
VERSION='0.1'
STARTTIME=`date +%s`
RHVER=`cat /etc/redhat-release |  awk -F'release ' '{print $2}' | cut -c 1`

# Check for mandatory command line parameters
if [ ! $PATCH ]; then
  usage
  quit 1 'No patch number specified'
fi


################################################
# Main
################################################

case $RHVER in 
  4)
    SL="sl4"
    GLITE="3.1"
  ;;
  5)
    SL="sl5"
    GLITE="3.2"
  ;;
esac

echo "Generating repo for patch $PATCH"
cat << EOF >> /etc/yum.repos.d/patch$PATCH.repo
[patch$PATCH]
name=patch $PATCH
baseurl=http://grid-deployment.web.cern.ch/grid-deployment/glite/cert/$GLITE/patches/$PATCH/$SL/\$basearch/
enabled=1
EOF

yum -y install $PATCH

echo -e "\nPatch $PATCH installed `date +%F`" >> /etc/motd

# FIXME - we still need some way of working out if patch is a new metapackage type to add to /etc/glite-metapackages

# Bye messages and log
RUNTIME=$[`date +%s` - $STARTTIME]
echo -e "\n`basename $0` took $RUNTIME seconds to run"
echo -e "Patch $PATCH installed!"
exit 0

