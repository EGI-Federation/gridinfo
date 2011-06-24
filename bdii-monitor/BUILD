#!/usr/bin/make -f 
SCRATCH=${PWD}/scratch
CC  = /usr/bin/gcc
CFLAGS  = -Wall -O2 -g -DLDAP_DEPRECATED
LDFLAGS = -lldap
SRC = src

compile: 
	mkdir -p ${SCRATCH}
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRC)/check_bdii_entries.c -o ${SCRATCH}/check_bdii_entries
