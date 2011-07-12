package=glite-info-plugin-fcr

.PHONY: configure install clean rpm

all: configure

install: 
	@echo installing ...
	@mkdir -p $(prefix)/opt/glite/libexec
	@mkdir -p $(prefix)/var/cache/fcr
#	@mkdir -p $(prefix)/etc/cron.hourly
	@install -m 0755 src/glite-info-plugin-fcr $(prefix)/opt/glite/libexec
#	@install -m 0755 etc/cron.hourly/generate-fcr-exclude-file $(prefix)/etc/cron.hourly/

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

