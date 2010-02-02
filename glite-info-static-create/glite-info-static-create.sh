#!/bin/bash
##############################################################################
# Copyright (c) Members of the EGEE Collaboration. 2010.
# See http://www.eu-egee.org/partners/ for details on the copyright
# holders.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at #
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################
#
# NAME :        glite-info-static-create
#
# DESCRIPTION : This script helps you create LDIF files.
#
# AUTHORS :     David.Horat@cern.ch
#               Laurence.Field@cern.ch
#
# WEB:          http://cern.ch/gridinfo
#
##############################################################################

# 1. Basic setup
`unalias -a` # Remove all aliases from this new shell
STARTTIME=`date +%s`
VERSION='0.1'
echo "Welcome to gLite Info Static Create v$VERSION"
if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--help" ]; then
  cat usage.txt
  exit 1
fi
module=$1
interface='wlcg'
templates='glue1 glue2'
shift
while [ $# -ne 0 ]; do
  case "$1" in
    -i)
      shift; interface=$1; shift;;
  esac
done

# 2. Source the config file
config_file=$module/$module.1.cfg
source $config_file

# 3. Check all needed variables are present using the interface
interface_file=$module/$module.$interface.ifc
source $interface_file
MANDATORY_VARS="$MANDATORY_SINGLEVALUED_VARS $MANDATORY_MULTIVALUED_VARS"
OPTIONAL_VARS="$OPTIONAL_SINGLEVALUED_VARS $OPTIONAL_MULTIVALUED_VARS"
MULTIVALUED_VARS="$MANDATORY_MULTIVALUED_VARS $OPTIONAL_MULTIVALUED_VARS"
SINGLEVALUED_VARS="$MANDATORY_SINGLEVALUED_VARS $OPTIONAL_SINGLEVALUED_VARS"
for var in $MANDATORY_VARS; do
  eval val=\$$var
  if [ "x$val" = "x" ]; then
    echo "ERROR: $var has no value. Check $config_file"
    echo "Mandatory values: $MANDATORY_VARS"
    echo "Optional values: $OPTIONAL_VARS"
    exit 1
  fi
done
for var in $OPTIONAL_VARS; do
  eval val=\$$var
  if [ "x$val" = "x" ]; then
    echo "WARNING: $var has no value. Fix it in $config_file"
  fi
done

# 4. Fill the templates so all variables are filled
for template in $templates; do
  cp $module/$module.$template.tpl output/$module.$template.ldif
  ldif_file=output/$module.$template.ldif
  # Substitue singlevalued attributes
  for var in $SINGLEVALUED_VARS; do
    eval val=\$$var
    if [ "x$val" = "x" ]; then
      sed -i "/$var/d" $ldif_file
    else
      sed -i "s|\$$var|$val|" $ldif_file
    fi
  done
  # Substitue mutivalued attributes
  for var in $MULTIVALUED_VARS; do
    eval multiple=\$$var
    if [ "x$multiple" = "x" ]; then
      sed -i "/\$$var/d" $ldif_file
    else
      # E.g.: GlueSiteLatitude: $SITE_LAT
      line=`sed -n "/$var/p" $ldif_file` # Select line
      # E.g.: GlueSiteLatitude: 
      line=${line%\$$var} # Strip the value from the original line
      output=''
      for val in $multiple; do
        if [ -z $output ]; then
          output="$val\n"
        else
          output=$output$line$val"\n"
        fi
      done
      output=${output%\\\n} # Remove trailing new line
      sed -i "s|\$$var|$output|" $ldif_file
    fi
  done
done

#5. Finalize
RUNTIME=$[`date +%s` - $STARTTIME]
echo "Finished! It took $RUNTIME seconds to run"
