NAME=${shell grep ^Name *.spec | cut -d ":" -f 2 | sed 's/^[^a-zA-Z0-9]*//'}
VERSION=${shell grep ^Version *.spec | cut -d ":" -f 2 | sed 's/^[^a-zA-Z0-9]*//'}
PWD=$(shell pwd)
SCRATCH=${PWD}/scratch
topdir:=$(shell rpm --eval %_topdir 2>/dev/null || ${SCRATCH} )
prefix=""

default: 
	@echo "Nothing to do"

install:
	mkdir -p ${prefix}
	cp -r etc ${prefix}
clean:
	rm -f *~ 
	rm -rf ${SCRATCH}

sdist:
	@mkdir -p  ${SCRATCH}/SOURCES/
	tar --gzip --exclude ".svn" --exclude "scratch" -cf ${SCRATCH}/${NAME}-${VERSION}.src.tgz *

rpm: sdist
	mkdir -p ${topdir}/BUILD
	mkdir -p ${topdir}/RPMS
	mkdir -p ${topdir}/SRPMS
	mkdir -p ${topdir}/SOURCES
	mkdir -p ${topdir}/SPECS
	cp ${SCRATCH}/${NAME}-${VERSION}.src.tgz ${topdir}/SOURCES
	rpmbuild --define "_topdir ${topdir}" -ba ${NAME}.spec
