NAME= $(shell grep Name: *.spec | sed 's/^[^:]*:[^a-zA-Z]*//' )
VERSION= $(shell grep Version: *.spec | sed 's/^[^:]*:[^0-9]*//' )
RELEASE= $(shell grep Release: *.spec |cut -d"%" -f1 |sed 's/^[^:]*:[^0-9]*//')
build=$(shell pwd)/build
DATE=$(shell date "+%a, %d %b %Y %T %z")

default: 
	@echo "Nothing to do"

install:
	@echo installing ...
	@mkdir -p $(prefix)/var/lib/bdii/gip/provider/
	@mkdir -p $(prefix)/var/lib/bdii/gip/plugin/
	@install -m 0755 provider/glite-info-provider-* $(prefix)/var/lib/bdii/gip/provider/
	@install -m 0755 plugin/glite-info-plugin-* $(prefix)/var/lib/bdii/gip/plugin/

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