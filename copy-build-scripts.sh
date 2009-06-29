#!/bin/sh

COMPONENTS="glue bdii"

for COMP in ${COMPONENTS}; do
    cp example/trunk/Makefile ${COMP}/trunk/
    cp example/trunk/debian/control ${COMP}/trunk/debian
    cp example/trunk/debian/rules ${COMP}/trunk/debian
    cp example/trunk/debian/compat ${COMP}/trunk/debian
done