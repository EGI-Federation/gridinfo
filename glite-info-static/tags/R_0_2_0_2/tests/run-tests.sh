#!/bin/sh

working_dir=$(pwd)
script=${working_dir}/../sbin/glite-info-static 
module_dir=${working_dir}
RETVAL=0

command="${script} -p ${module_dir} -m site -c my_site.cfg -i glue -t glue1"

echo -n "Tesing provinding output ... "
${command} | grep "objectClass: GlueSite"  >/dev/null
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAIL"
    RETVAL=1
fi

echo -n "Tesing single value substitution ... "
num=$(${command} | grep "GlueSiteOtherInfo" | wc -l )
if [ ${num} -eq 2 ]; then
    echo "OK"
else
    echo "FAIL"
    RETVAL=1
fi

echo -n "Tesing multi value substitution ... "
${command} | grep "GlueSiteUniqueID: cern.ch"  >/dev/null
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAIL"
    RETVAL=1
fi

if [ ${RETVAL} -eq 0 ]; then
    echo "Tests Passed!"
    exit 0
else
    echo "Tests Failed!"
    exit 1
fi