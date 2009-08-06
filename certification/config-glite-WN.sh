#!/bin/bash

`unalias -a`
SITEINFODEFFILE='/etc/yaim/site-info.def'
WNLISTDIR='/etc/yaim'
WNLISTFILE="$WNLISTDIR/wn-list.conf"
HOST=`hostname`


################################################
# Main
################################################

# Welcome
echo "Automatic script for gLite WN Configuration"

# Create WN-List for YAIM
echo "INFO: Creating $WNLISTFILE"
mkdir -p $WNLISTDIR
echo $HOST > $WNLISTFILE

# Alter site-info.def file with DPM specific parameters
echo "INFO: Altering $SITEINFODEFFILE"
sed -i 's,WN_LIST=/afs/cern.ch/project/gd/yaim-server/cert-TB-config/site-TB/wn-list.conf,WN_LIST='$WNLISTFILE',' $SITEINFODEFFILE

# Exit
exit 0
