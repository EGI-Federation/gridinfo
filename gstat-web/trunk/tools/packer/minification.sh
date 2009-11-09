#!/bin/bash

################################################################################
#                               Minification                                   #
#                                                                              #
# This script minificates javascript and css files in the objective directory  #
# and all its subdirectories recursively to reduce their size.                 #
#                                                                              #
# Usage:                                                                       #
# ./minification.sh [directory]                                                #
#                                                                              #
# Exit values:                                                                 #
#  0 - all OK                                                                  #
#  1 - No parameters. Displaying usage info                                    #
#  3 - Source directory not found                                              #
#                                                                              #
# Author: David Horat (david.horat@gmail.com)                                  #
################################################################################

# Functions
function quit {
  RUNTIME=$[`date +%s` - $STARTTIME]
  echo "Runtime: $RUNTIME seconds"
  echo "ERROR $1: $2"
  exit $1
}

# Basic info
`unalias -a` # Remove all aliases from this new shell
PATH='/usr/local/bin:/usr/bin:/bin'
VERSION='0.3'
STARTTIME=`date +%s`

# Welcome message
echo "Welcome to Minification v$VERSION by David Horat"
date

# Display usage info
if [ ! $# -eq  1 ]; then
  echo 'Usage:'
  echo './minification.sh [directory]'
fi

# Check if source directory exists
if [ ! -d $1 ]; then
  quit 3 "$1 source directory not found"
fi
SRC=${1%/}

# Save original directory size
ORIGSIZE=`du -s -b $SRC |awk '{print $1}'`
echo "Original directory size: $ORIGSIZE"

# Minification process
echo -n "Minification process started..."
for File in `find $SRC -iname *.js`; do
  php pack.php $File -esp > $File
done
echo -n "......"
# No CSS minification at the moment
#find $SRC -iname *.css -exec java -jar $YUIJAR --type css -o {} {} \;
echo "end!"

# Final directory size and statistics
FINALSIZE=`du -s -b $SRC |awk '{print $1}'`
echo "Final directory size: $FINALSIZE"
DIFSIZE=$[$ORIGSIZE - $FINALSIZE]
echo "Difference: $DIFSIZE"
PERSIZE=$[$DIFSIZE * 100 / $ORIGSIZE]
echo "Improved overall: $PERSIZE%"

# Bye messages
RUNTIME=$[`date +%s` - $STARTTIME]
echo "Runtime: $RUNTIME seconds"
echo "Finished!"
