name= ${shell grep Name: *.spec | sed 's/^[^:]*: //' }
version= ${shell grep Version: *.spec | sed 's/^[^:]*: //' }
build=${shell pwd}/build
sources: dist
	cp dist/${name}-${version}.tar.gz .

dist:
	python setup.py sdist
	tar -zxvf dist/${name}-${version}.tar.gz 
	tar -zcvf ${name}-${version}.tar.gz ${name}-${version} 
	mv ${name}-${version}.tar.gz dist
	rm -rf ${name}-${version} 

prepare: dist
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp dist/${name}-${version}.tar.gz build/SOURCES 

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




