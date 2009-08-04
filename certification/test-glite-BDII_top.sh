#!/bin/bash
################################################################################
#                        Top Level BDII Test Script
#
# Automatic script for Top BDII testing.
#
# Authors: David Horat (david.horat@cern.ch)
#
# Exit values:
#  0 - OK
#  1 - Problem checking out the basic tests from the Product Team
#  2 - Problems running BDII basic tests from the Product Team
#  3 - Problem checking out top level BDII tests from the Product Team
#  4 - Problems running the test-bdii-top script
#  5 - Problems running the test-bdii-chain script
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
  echo "ERROR $1: $2"
  exit $1
}


################################################
# Parameters and initialization
################################################

# Fixed variables
VERSION='0.3'
STARTTIME=`date +%s`


################################################
# Main
################################################

# Welcome message and write the MOTD
echo "Top BDII Test Script v$VERSION"

# Checkout latest basic tests from the Product Team
echo "INFO: Downloading basic tests from the Product Team..."
svn co http://svnweb.cern.ch/guest/gridinfo/bdii/trunk/tests
if [ $? -ne 0 ]; then
  quit 1 "Problem checking out the basic tests from the Product Team."
fi

# Running basic tests from the Product Team
echo "INFO: Running basic tests from the Product Team..."
cd tests
./test-bdii
if [ $? -ne 0 ]; then
  quit 2 "Problems running BDII basic tests from the Product Team."
fi
cd -

# Checkout latest top level BDII tests from the Product Team
echo "INFO: Downloading top level BDII tests from the Product Team..."
svn co http://svnweb.cern.ch/guest/gridinfo/tests/trunk
if [ $? -ne 0 ]; then
  quit 3 "Problem checking out top level BDII tests from the Product Team."
fi

# Running top level BDII tests from the Product Team
echo "INFO: Running top level BDII tests from the Product Team..."
cd trunk
./test-bdii-top
if [ $? -ne 0 ]; then
  quit 4 "Problems running the test-bdii-top script."
fi
./test-bdii-chain
if [ $? -ne 0 ]; then
  quit 5 "Problems running the test-bdii-chain script."
fi
cd -

# Bye messages and log
RUNTIME=$[`date +%s` - $STARTTIME]
echo -e "\n`basename $0` took $RUNTIME seconds to run"
echo -e "OK!"
exit 0
