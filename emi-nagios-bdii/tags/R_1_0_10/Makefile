name= ${shell grep Name: *.spec | sed 's/^[^:]*: //' }
version= ${shell grep Version: *.spec | sed 's/^[^:]*: //' }
build=${shell pwd}/build

SCRATCH=${PWD}/build
CC  = /usr/bin/gcc
CFLAGS  = -Wall -O2 -g -DLDAP_DEPRECATED
LDFLAGS = -lldap
SRC = src
LOCATION=/usr/lib64/nagios/plugins/contrib/

compile: 
	mkdir -p ${SCRATCH}
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRC)/check_bdii_entries.c -o ${SCRATCH}/check_bdii_entries

install:
	mkdir -p $(prefix)$(LOCATION)
	install -m 0755 ${SCRATCH}/check_bdii_entries $(prefix)$(LOCATION)

sources: dist

dist:
	tar --gzip --exclude ".svn" --exclude ".svn" -cf ${name}-${version}.src.tgz *

prepare: dist
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp ${name}-${version}.src.tgz build/SOURCES 

srpm: prepare
	@rpmbuild -bs --define='_topdir ${build}' $(name).spec

rpm: prepare
	@rpmbuild -bb --define='_topdir ${build}' $(name).spec

deb: rpm
	fakeroot alien build/RPMS/noarch/${name}-${version}-1.noarch.rpm

clean:
	@rm -f *~ bin/*~ etc/*~ data/*~ ${name}-*.src.tgz
	@rm -rf build dist MANIFEST

.PHONY: dist srpm rpm sources clean 




