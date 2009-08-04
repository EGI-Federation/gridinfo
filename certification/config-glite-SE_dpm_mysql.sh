#!/bin/bash
################################################################################
#                      SE DPM MySQL Configuration Script
#
# Automatic script for SE DPM MySQL Configuration.
#
# Authors: David Horat (david.horat@cern.ch)
#
# Exit values:
#  0 - OK
#  1 - Could not restart MySQL
#  2 - Could not create tables
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
VERSION='0.1'
STARTTIME=`date +%s`
SITEINFODEFFILE='/etc/yaim/site-info.def'
HOST=`hostname`


################################################
# Main
################################################

# Welcome
echo "Automatic script for SE DPM MySQL Configuration v$VERSION"

# Start MySQL
echo "INFO: Starting MySQL"
/etc/init.d/mysqld restart
if [ $? -ne 0 ]; then
  quit 1 "Could not restart MySQL."
fi

# Create tables into MySQL
echo "INFO: Creating tables"
mysql -u root < /opt/lcg/share/DPM/create_dpns_tables_mysql.sql
if [ $? -ne 0 ]; then
  quit 2 "Could not create tables."
fi

# Alter site-info.def file with DPM specific parameters
echo "INFO: Altering $SITEINFODEFFILE"
sed -i 's/DPM_HOST="lxb7608v1.$MY_DOMAIN"/DPM_HOST="'$HOST'"/' $SITEINFODEFFILE
sed -i 's,DPM_FILESYSTEMS="$DPM_HOST:/storage lxb7608v2.$MY_DOMAIN:/path2 lxfsrd0502.$MY_DOMAIN:/storage",DPM_FILESYSTEMS="$DPM_HOST:/storage",' $SITEINFODEFFILE

# Bye messages and log
RUNTIME=$[`date +%s` - $STARTTIME]
echo -e "\n`basename $0` took $RUNTIME seconds to run"
echo -e "OK!"
exit 0
