NAME= $(shell grep Name: *.spec | sed 's/^[^:]*:[^a-zA-Z]*//' )
VERSION= $(shell grep Version: *.spec | sed 's/^[^:]*:[^0-9]*//' )
RELEASE= $(shell grep Release: *.spec |cut -d"%" -f1 |sed 's/^[^:]*:[^0-9]*//')
build=$(shell pwd)/build
DATE=$(shell date "+%a, %d %b %Y %T %z")
dist=$(shell rpm --eval '%dist' | sed 's/%dist/.el5/')

CC  = /usr/bin/gcc
LDFLAGS = -lldap
SRC = src

compile: 
	mkdir -p ${build}
	$(CC) $(CFLAGS) $(LDFLAGS) $(SRC)/check_bdii_entries.c -o ${build}/check_bdii_entries

install:
	mkdir -p $(prefix)/usr/lib64/nagios/plugins/
	install -m 0755 ${build}/check_bdii_entries $(prefix)/usr/lib64/nagios/plugins/

sources: dist

dist:
	mkdir -p  $(build)/$(NAME)-$(VERSION)/
	rsync -HaS --exclude ".svn" --exclude "$(build)" * $(build)/$(NAME)-$(VERSION)/
	cd $(build); tar --gzip -cf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION)/; cd -

prepare: dist
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp $(build)/$(NAME)-$(VERSION).tar.gz $(build)/SOURCES

srpm: prepare
	rpmbuild -bs --define="dist ${dist}" --define='_topdir ${build}' $(NAME).spec

rpm: srpm
	rpmbuild --rebuild  --define='_topdir ${build} ' $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)${dist}.src.rpm

deb: rpm
	fakeroot alien build/RPMS/noarch/${NAME}-${VERSION}-1.noarch.rpm

clean:
	@rm -f *~ bin/*~ etc/*~ data/*~ ${NAME}-*.tar.gz
	@rm -rf build dist MANIFEST

.PHONY: dist srpm rpm sources clean 




