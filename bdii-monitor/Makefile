name= ${shell grep Name: *.spec | sed 's/^[^:]*: //' }
version= ${shell grep Version: *.spec | sed 's/^[^:]*: //' }
build=${shell pwd}/build

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
	@rm -f *~ bin/*~ etc/*~ data/*~   
	@rm -rf build dist MANIFEST

.PHONY: dist srpm rpm sources clean 




