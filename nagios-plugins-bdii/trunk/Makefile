NAME= $(shell grep Name: *.spec | sed 's/^[^:]*:[^a-zA-Z]*//' )
VERSION= $(shell grep Version: *.spec | sed 's/^[^:]*:[^0-9]*//' )
RELEASE= $(shell grep Release: *.spec |cut -d"%" -f1 |sed 's/^[^:]*:[^0-9]*//')
build=$(shell pwd)/build
DATE=$(shell date "+%a, %d %b %Y %T %z")
dist=$(shell rpm --eval '%dist' | sed 's/%dist/.el5/')

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
	tar --gzip --exclude ".svn" --exclude ".svn" -cf ${NAME}-${VERSION}.tar.gz *

prepare: dist
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp ${NAME}-${VERSION}.tar.gz build/SOURCES 

srpm: prepare
	@rpmbuild -bs --define="dist ${dist}" --define='_topdir ${build}' $(NAME).spec

rpm: srpm
	@rpmbuild --rebuild  --define='_topdir ${build} ' $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)${dist}.src.rpm

deb: rpm
	fakeroot alien build/RPMS/noarch/${NAME}-${VERSION}-1.noarch.rpm

clean:
	@rm -f *~ bin/*~ etc/*~ data/*~ ${NAME}-*.tar.gz
	@rm -rf build dist MANIFEST

.PHONY: dist srpm rpm sources clean 




