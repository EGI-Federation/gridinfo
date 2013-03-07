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

sources: dist
	cp $(build)/$(NAME)-$(VERSION).tar.gz .

dist:
	mkdir -p  $(build)/$(NAME)-$(VERSION)/
	rsync -HaS --exclude .svn --exclude 'build*' * $(build)/$(NAME)-$(VERSION)/
	cd $(build); tar --gzip -cf $(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION)/; cd -

prepare: dist
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp build/${NAME}-${VERSION}.tar.gz build/SOURCES 

srpm: prepare
	@rpmbuild -bs --define="dist ${dist}" --define='_topdir ${build}' $(NAME).spec 

rpm: srpm
	@rpmbuild --rebuild  --define='_topdir ${build} ' --define="dist ${dist}" $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)${dist}.src.rpm 

deb: dist
	cd $(build)/$(NAME)-$(VERSION); dpkg-buildpackage -us -uc; cd -


clean:
	@rm -f *~ bin/*~ etc/*~ data/*~   
	@rm -rf build dist MANIFEST

.PHONY: dist srpm rpm sources deb clean 
