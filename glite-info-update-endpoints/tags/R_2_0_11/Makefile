NAME= $(shell grep Name: *.spec | sed 's/^[^:]*:[^a-zA-Z]*//' )
VERSION= $(shell grep Version: *.spec | sed 's/^[^:]*:[^0-9]*//' )
RELEASE= $(shell grep Release: *.spec |cut -d"%" -f1 |sed 's/^[^:]*:[^0-9]*//')
build=$(shell pwd)/build
DATE=$(shell date "+%a, %d %b %Y %T %z")
dist=$(shell rpm --eval '%dist' | sed 's/%dist/.el5/')

default: 
	@echo "Nothing to do"

install:
	@echo installing ...
	@mkdir -p ${prefix}/etc/glite
	@mkdir -p ${prefix}/etc/cron.hourly
	@mkdir -p ${prefix}/usr/bin/
	@mkdir -p ${prefix}/var/log/glite
	@mkdir -p ${prefix}/var/cache/glite/glite-info-update-endpoints
	@mkdir -p $(prefix)/usr/share/doc/glite-info-update-endpoints
	@install -m 0644 etc/glite-info-update-endpoints.conf ${prefix}/etc/glite/
	@install -m 0755 bin/glite-info-update-endpoints ${prefix}/usr/bin/
	@install -m 0755 etc/cron.hourly/glite-info-update-endpoints ${prefix}/etc/cron.hourly/
	@install -m 0644 doc/README $(prefix)/usr/share/doc/glite-info-update-endpoints

dist:
	@mkdir -p  $(build)/$(NAME)-$(VERSION)/
	rsync -HaS --exclude ".svn" --exclude "$(build)" * $(build)/$(NAME)-$(VERSION)/
	cd $(build); tar --gzip -cf $(NAME)-$(VERSION).src.tgz $(NAME)-$(VERSION)/; cd -

sources: dist
	cp $(build)/$(NAME)-$(VERSION).src.tgz .

deb: dist
	cd $(build)/$(NAME)-$(VERSION); dpkg-buildpackage -us -uc; cd -

prepare: dist
	@mkdir -p  $(build)/RPMS/noarch
	@mkdir -p  $(build)/SRPMS/
	@mkdir -p  $(build)/SPECS/
	@mkdir -p  $(build)/SOURCES/
	@mkdir -p  $(build)/BUILD/
	cp $(build)/$(NAME)-$(VERSION).src.tgz $(build)/SOURCES 

srpm: prepare
	@rpmbuild -bs --define="dist ${dist}" --define='_topdir ${build}' $(NAME).spec 

rpm: srpm
	@rpmbuild --rebuild  --define='_topdir ${build} ' $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)${dist}.src.rpm 

clean:
	rm -f *~ $(NAME)-$(VERSION).src.tgz
	rm -rf $(build)

.PHONY: dist srpm rpm sources clean 
