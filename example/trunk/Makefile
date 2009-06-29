include CONFIG
PWD=$(shell pwd)
control=scratch/${NAME}-${VERSION}/debian/control
SCRATCH=${PWD}/scratch

default: 
	@echo "Nothing to do"

clean:
	rm -f *~
	rm -rf ${SCRATCH}

sdist:
	@mkdir -p  ${SCRATCH}/SOURCES/
	tar --gzip --exclude ".svn" --exclude "scratch" -cf ${SCRATCH}/SOURCES/${NAME}-${VERSION}.src.tgz *

deb: sdist
	@mkdir -p ${SCRATCH}/${NAME}-${VERSION}/
	tar -zx -C ${SCRATCH}/${NAME}-${VERSION}/ -f \
	${SCRATCH}/SOURCES/${NAME}-${VERSION}.src.tgz
	rm -f ${SCRATCH}/${NAME}-${VERSION}/Makefile
	@sed -i "s/Package:.*/Package: ${NAME}/" ${control}
	@sed -i "s/Source:.*/Source: ${NAME}/" ${control}
	@sed -i "s/Version:.*/Version: ${VERSION}/" ${control}
	@sed -i "s/Maintainer:.*/Maintainer: ${PACKAGER}/" ${control}
	@sed -i "s/Description:.*/Description: ${DESCRIPTION}/" ${control}
	@sed -i "s/Section:.*/Section: ${GROUP}/" ${control}
	cd ${SCRATCH}/${NAME}-${VERSION}; dpkg-buildpackage -us -uc; cd ${PWD}

rpm: sdist
	mkdir -p ${SCRATCH}/BUILD
	mkdir -p ${SCRATCH}/RPMS
	mkdir -p ${SCRATCH}/SRPMS
	mkdir -p ${SCRATCH}/SOURCES
	mkdir -p ${SCRATCH}/SPECS
	rpmbuild --define "_topdir ${SCRATCH}" -ba ${NAME}.spec
