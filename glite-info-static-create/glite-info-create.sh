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

# 0. Functions
function print_help() {
  cat << EOF >&2
Usage:
  glite-info-create.sh -m <module> [-i <iface>] [-t <template>] [-c <config>]
       
Parameters:
  <module>    The module you are using. E.g.: site
  <iface>     The interface you want to use. E.g.: glue, wlcg (default)
  <template>  The template you want to use. E.g.: glue1, glue2
  <config>    The config file location if outside from the module directory

Examples:
       glite-info-create.sh -m site
       glite-info-create.sh -m site -i glue -t glue2 -c /etc/bdii/site.cfg

Web site: http://cern.ch/gridinfo
EOF
}

# 1. Basic setup
`unalias -a` # Remove all aliases from this new shell
STARTTIME=`date +%s`
VERSION='0.2'
echo "Welcome to gLite Info Static Create v$VERSION"
if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--help" ]; then
  print_help
  exit 1
fi

# 2. Set default values and parse command line arguments
interface='wlcg'
templates='glue1 glue2'
while getopts ":m:i:t:c:" opt; do
  case $opt in
    i) interface=$OPTARG;;
    t) templates=$OPTARG;;
    c) config_file=$OPTARG;;
    m) module=$OPTARG;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1;;
    :) echo "Option -$OPTARG requires an argument." >&2; exit 1;;
  esac
done

if [ -z $module ]; then
  print_help; 
  echo "ERROR: Parameter -m <module> is mandatory"; 
  exit 1;
fi
if [ -z $config_file ]; then config_file=$module/$module.1.cfg; fi

# 3. Source the config file
if [ ! -f $config_file ]; then
  echo "ERROR: $config_file is not a valid config file"
  exit 1
fi
source $config_file

# 4. Check all needed variables are present using the interface
interface_file=$module/$module.$interface.ifc
if [ ! -f $interface_file ]; then
  echo "ERROR: $interface_file is not a valid interface file"
  exit 1
fi
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

# 5. Fill the templates so all variables are filled
for template in $templates; do
  template_file=output/$module.$template.ldif
  if [ ! -f $template_file ]; then
    echo "ERROR: $template_file is not a valid template file"
    exit 1
  fi
  ldif_file=output/$module.$template.ldif
  if [ ! -f $ldif_file ]; then
    echo "WARNING: $ldif_file already exists. It will be overwritten."
    exit 1
  fi
  cp $template_file $ldif_file
  # Substitute singlevalued attributes
  for var in $SINGLEVALUED_VARS; do
    eval val=\$$var
    if [ "x$val" = "x" ]; then
      sed -i "/$var/d" $ldif_file
    else
      sed -i "s|\$$var|$val|" $ldif_file
    fi
  done
  # Substitute mutivalued attributes
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

#6. Finalize
RUNTIME=$[`date +%s` - $STARTTIME]
echo "Finished! It took $RUNTIME seconds to run"
