NAME= $(shell grep Name: *.spec | sed 's/^[^:]*:[^a-zA-Z]*//' )
VERSION= $(shell grep Version: *.spec | sed 's/^[^:]*:[^0-9]*//' )
RELEASE= $(shell grep Release: *.spec |cut -d"%" -f1 |sed 's/^[^:]*:[^0-9]*//')
build=$(shell pwd)/build
DATE=$(shell date "+%a, %d %b %Y %T %z")

default: 
	@echo "Nothing to do"

install:
	@echo installing ...
	@mkdir -p $(prefix)/opt/glite/libexec/
	@mkdir -p $(prefix)/opt/glite/etc/
	@mkdir -p $(prefix)/opt/glite/doc/
	@install -m 0755 src/glite-info-service $(prefix)/opt/glite/libexec
	@install -m 0755 src/glite-info-service-* $(prefix)/opt/glite/libexec
	@install -m 0755 src/glite-info-glue2-* $(prefix)/opt/glite/libexec
	@install -m 0644 etc/*.template $(prefix)/opt/glite/etc
	@install -m 0644 etc/*.test.ldif $(prefix)/opt/glite/etc
	@install -m 0644 doc/README $(prefix)/opt/glite/doc
	@install -m 0644 doc/README-GLUE2 $(prefix)/opt/glite/doc

dist:
	@mkdir -p  $(build)/$(NAME)-$(VERSION)/
	rsync -HaS --exclude ".svn" --exclude "$(build)" * $(build)/$(NAME)-$(VERSION)/
	cd $(build); tar --gzip -cf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION)/; cd -

sources: dist
	cp $(build)/$(NAME)-$(VERSION).tar.gz .

deb: dist
	cd $(build)/$(NAME)-$(VERSION); dpkg-buildpackage -us -uc; cd -

prepare: dist
	@mkdir -p  $(build)/RPMS/noarch
	@mkdir -p  $(build)/SRPMS/
	@mkdir -p  $(build)/SPECS/
	@mkdir -p  $(build)/SOURCES/
	@mkdir -p  $(build)/BUILD/
	cp $(build)/$(NAME)-$(VERSION).tar.gz $(build)/SOURCES 

srpm: prepare
	@rpmbuild -bs --define='_topdir ${build}' $(NAME).spec

rpm: srpm
	@rpmbuild --rebuild  --define='_topdir ${build} ' $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE).src.rpm

clean:
	rm -f *~ $(NAME)-$(VERSION).tar.gz
	rm -rf $(build)

.PHONY: dist srpm rpm sources clean 
