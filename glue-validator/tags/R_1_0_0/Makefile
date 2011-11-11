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
	cp dist/${NAME}-${VERSION}.tar.gz .

dist:
	python setup.py sdist
	tar -zxvf dist/${NAME}-${VERSION}.tar.gz 
	tar -zcvf ${NAME}-${VERSION}.tar.gz ${NAME}-${VERSION} 
	mv ${NAME}-${VERSION}.tar.gz dist/${NAME}-${VERSION}.tar.gz
	rm -rf ${NAME}-${VERSION} 

prepare: dist
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp dist/${NAME}-${VERSION}.tar.gz build/SOURCES 

srpm: prepare
	@rpmbuild -bs --define="dist ${dist}" --define='_topdir ${build}' $(NAME).spec 

rpm: srpm
	@rpmbuild --rebuild  --define='_topdir ${build} ' $(build)/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)${dist}.src.rpm 

deb: rpm
	fakeroot alien build/RPMS/noarch/${NAME}-${VERSION}-1.noarch.rpm

clean:
	@rm -f *~ bin/*~ etc/*~ data/*~   
	@rm -rf build dist MANIFEST

.PHONY: dist srpm rpm sources clean 




