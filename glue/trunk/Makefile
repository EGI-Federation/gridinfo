metadata=config
name:=$(shell grep NAME ${metadata} | sed 's/^[^:]*: //' )
version:=$(shell grep VERSION ${metadata} | sed 's/^[^:]*: //' )
release:=$(shell grep RELEASE ${metadata} | sed 's/^[^:]*: //' )
prefix:=$(shell grep PREFIX ${metadata} | sed 's/^[^:]*: //' )
topdir:=$(shell rpm --eval %_topdir 2>/dev/null || echo ${pwd}/build )

.PHONY: 

all: 

install: 
	@mkdir -p ${prefix}etc/ldap/schema/
	@install -m 0755 etc/ldap/schema/*.schema  ${prefix}etc/ldap/schema/

clean:
	rm -f *~ 
	rm -rf build
dist:
	@mkdir -p  ${topdir}/SOURCES/
	@tar --gzip -cf ${topdir}/SOURCES/${name}-${version}.src.tgz *

rpm: dist
	@mkdir -p  ${topdir}/RPMS/noarch
	@mkdir -p  ${topdir}/SRPMS/
	@mkdir -p  ${topdir}/SPECS/
	@mkdir -p  ${topdir}/BUILD/
	@rpmbuild -ba --define="_topdir ${topdir}" ${name}.spec
