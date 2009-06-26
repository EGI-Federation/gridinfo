#!/usr/bin/make -f

metadata=config
name:=$(shell grep NAME ${metadata} | sed 's/^[^:]*: //' )
version:=$(shell grep VERSION ${metadata} | sed 's/^[^:]*: //' )
release:=$(shell grep RELEASE ${metadata} | sed 's/^[^:]*: //' )
prefix:=$(shell grep PREFIX ${metadata} | sed 's/^[^:]*: //' )
packager:=$(shell grep PACKAGER ${metadata} | sed 's/^[^:]*: //' )
description:=$(shell grep DESCRIPTION ${metadata} | sed 's/^[^:]*: //' )
group:=$(shell grep GROUP ${metadata} | sed 's/^[^:]*: //' )
topdir:=$(shell rpm --eval %_topdir 2>/dev/null || echo ${pwd}/build )
debian=${topdir}/BUILD/${name}-${version}/DEBIAN

.PHONY: 

all: 

install: 
	@mkdir -p ${prefix}etc/ldap/schema/
	@install -m 0755 etc/ldap/schema/*.schema  ${prefix}etc/ldap/schema/

clean:
	@rm -f *~ *.deb
	@rm -rf scratch
dist:
	@mkdir -p  ${topdir}/SOURCES/
	@tar --gzip --exclude ".svn" --exclude "scratch" --exclude "*.deb" \
	-cf ${topdir}/SOURCES/${name}-${version}.src.tgz *

rpm: dist
	@mkdir -p  ${topdir}/RPMS/noarch
	@mkdir -p  ${topdir}/SRPMS/
	@mkdir -p  ${topdir}/SPECS/
	@mkdir -p  ${topdir}/BUILD/
	@rpmbuild -ba --define="_topdir ${topdir}" ${name}.spec

deb: dist
	@mkdir -p ${debian}
	@tar -zxf ${topdir}/SOURCES/${name}-${version}.src.tgz -C ${topdir}/BUILD/${name}-${version} 
	@rm -f ${topdir}/BUILD/${name}-${version}/config 
	@rm -f ${topdir}/BUILD/${name}-${version}/Makefile 
	@rm -f ${topdir}/BUILD/${name}-${version}/*.spec 
	@rm -f ${topdir}/BUILD/${name}-${version}/INSTALLED_FILES
	@sed -i "s/Package:.*/Package: ${name}/" ${debian}/control
	@sed -i "s/Version:.*/Version: ${version}/" ${debian}/control
	@sed -i "s/Maintainer:.*/Maintainer: ${packager}/" ${debian}/control
	@sed -i "s/Description:.*/Description: ${description}/" ${debian}/control
	@sed -i "s/Section:.*/Section: ${group}/" ${debian}/control

	@dpkg -ba ${topdir}/BUILD/${name}-${version} ${name}-${version}.deb