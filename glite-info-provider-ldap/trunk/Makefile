prefix=/opt/glite
package=glite-info-provider-ldap

.PHONY: configure install clean rpm

all: configure

install: 
	@echo installing ...
	@mkdir -p $(prefix)/libexec/
	@install -m 0755 src/glite-info-provider-ldap $(prefix)/libexec

clean:
	rm -f *~ 
	rm -rf rpmbuild 

rpm:
	@mkdir -p  rpmbuild/RPMS/noarch
	@mkdir -p  rpmbuild/SRPMS/
	@mkdir -p  rpmbuild/SPECS/
	@mkdir -p  rpmbuild/SOURCES/
	@mkdir -p  rpmbuild/BUILD/
	@tar --gzip -cf rpmbuild/SOURCES/${package}.src.tgz *
	@rpmbuild -ba ${package}.spec

