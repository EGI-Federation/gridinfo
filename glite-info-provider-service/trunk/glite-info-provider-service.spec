Name:           glite-info-provider-service
Version:        1.13.1
Release:        1%{?dist}
Summary:        The GLUE service information provider
License:        ASL 2.0
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/glite-info-provider-service/tags/R_1_13_1_1 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source:         %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Group: Development/Libraries
URL: https://tomtools.cern.ch/confluence/display/IS/ResourceBDII

%description
The GLUE service information provider

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir /etc/glite/info/service
%dir /usr/share/doc/glite-info-provider-service
/usr/bin/glite-info-glue2-service
/usr/bin/glite-info-glue2-endpoint
/usr/bin/glite-info-glue2-simple
/usr/bin/glite-info-glue2-multi
/usr/bin/glite-info-glue2-voms
/usr/bin/glite-info-service
/usr/bin/glite-info-service-glue2
/usr/bin/glite-info-service-glue2-beta
/usr/bin/glite-info-service-test
/usr/bin/glite-info-service-amga
/usr/bin/glite-info-service-argus
/usr/bin/glite-info-service-bdii
/usr/bin/glite-info-service-gridice
/usr/bin/glite-info-service-vobox
/usr/bin/glite-info-service-voms
/usr/bin/glite-info-service-voms-wrapper
/usr/bin/glite-info-service-voms-admin
/usr/bin/glite-info-service-myproxy
/usr/bin/glite-info-service-wmproxy
/usr/bin/glite-info-service-lbserver
/usr/bin/glite-info-service-frontier
/usr/bin/glite-info-service-squid
/usr/bin/glite-info-service-cream
/usr/bin/glite-info-service-dcache
/usr/bin/glite-info-service-dpm
/usr/bin/glite-info-service-rtepublisher
/usr/bin/glite-info-service-gatekeeper
/usr/bin/glite-info-service-status
/etc/glite/info/service/glite-info-glue2-amga.conf.template
/etc/glite/info/service/glite-info-glue2-argus-pap.conf.template
/etc/glite/info/service/glite-info-glue2-argus-pep.conf.template
/etc/glite/info/service/glite-info-glue2-argus-pdp.conf.template
/etc/glite/info/service/glite-info-glue2-bdii-site.conf.template
/etc/glite/info/service/glite-info-glue2-bdii-top.conf.template
/etc/glite/info/service/glite-info-glue2-lbserver.conf.template
/etc/glite/info/service/glite-info-glue2-rtepublisher.conf.template
/etc/glite/info/service/glite-info-glue2-vobox.conf.template
/etc/glite/info/service/glite-info-glue2-voms.conf.template
/etc/glite/info/service/glite-info-glue2-voms-admin.conf.template
/etc/glite/info/service/glite-info-glue2-frontier.conf.template
/etc/glite/info/service/glite-info-glue2-squid.conf.template
/etc/glite/info/service/glite-info-glue2-myproxy.conf.template
/etc/glite/info/service/glite-info-glue2-cemon.conf.template
/etc/glite/info/service/glite-info-glue2-wmproxy.conf.template
/etc/glite/info/service/glite-info-service-test.conf.template
/etc/glite/info/service/glite-info-service-amga.conf.template
/etc/glite/info/service/glite-info-service-argus-pap.conf.template
/etc/glite/info/service/glite-info-service-argus-pep.conf.template
/etc/glite/info/service/glite-info-service-argus-pdp.conf.template
/etc/glite/info/service/glite-info-service-bdii.conf.template
/etc/glite/info/service/glite-info-service-bdii-site.conf.template
/etc/glite/info/service/glite-info-service-bdii-top.conf.template
/etc/glite/info/service/glite-info-service-gridice.conf.template
/etc/glite/info/service/glite-info-service-gsirfio.conf.template
/etc/glite/info/service/glite-info-service-lbserver.conf.template
/etc/glite/info/service/glite-info-service-frontier.conf.template
/etc/glite/info/service/glite-info-service-squid.conf.template
/etc/glite/info/service/glite-info-service-cream.conf.template
/etc/glite/info/service/glite-info-service-cemon.conf.template
/etc/glite/info/service/glite-info-service-myproxy.conf.template
/etc/glite/info/service/glite-info-service-vobox.conf.template
/etc/glite/info/service/glite-info-service-voms.conf.template
/etc/glite/info/service/glite-info-service-voms-admin.conf.template
/etc/glite/info/service/glite-info-service-srm-dcache-v1.conf.template
/etc/glite/info/service/glite-info-service-srm-dcache-v2.conf.template
/etc/glite/info/service/glite-info-service-srm-dpm-v1.conf.template
/etc/glite/info/service/glite-info-service-srm-dpm-v2.conf.template
/etc/glite/info/service/glite-info-service-wmproxy.conf.template
/etc/glite/info/service/glite-info-service-rtepublisher.conf.template
/etc/glite/info/service/glite-info-service-gatekeeper.conf.template
/etc/glite/info/service/glite-info-glue2-test.conf.template
/etc/glite/info/service/glite-info-glue2-test2.conf.template
/etc/glite/info/service/glite-info-glue2-service-test.conf.template
/etc/glite/info/service/glite-info-glue2-service-argus.conf.template
/etc/glite/info/service/glue1.test.ldif
/etc/glite/info/service/glue1.test.ldif.prev
/etc/glite/info/service/glue2.test.ldif
/etc/glite/info/service/glue2.multi.test.ldif
/etc/glite/info/service/glue2.test.ldif.prev
%doc /usr/share/doc/glite-info-provider-service/README
%doc /usr/share/doc/glite-info-provider-service/README-GLUE2

%changelog
* Thu Aug 01 2013 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.13.1-1
- Die if hostname -f returns a null string, voms providers, bug #101562
* Thu Aug 01 2013 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.13.0-1
- Allow longer strings in GlueServiceData, bug #102168
- Die if hostname -f returns a null string, bug #101562
- Allow for an rpm name change in the WMS templates, bug #100872
- Change the published URL for the Argus PDP templates, bug #100822
- Allow for a move in the pidfile location in the LB templates, bug #100126
* Mon Oct 22 2012 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.12.0-1
- Protect against non-ASCII characters in strings, bug #98374
* Sat Sep 29 2012 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.11.0-2
- Update the site and top BDII configuration, bug #97396
- Publish the OS name and version as OtherInfo items in the Endpoint, bug #97816
* Tue Aug 28 2012 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.10.0-1
- GLUE 2 updates: Export site name, publish EGI profile compliance, publish HostDN
- See bugs #96503, #96787
* Wed Jul 18 2012 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.9.0-1
- GLUE 2 updates: new README, change VOMS ServiceType, fix MyProxy bug
- See bugs #80792, #95869, #95872
* Thu Dec 08 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.1-2
- Fix the spec file
* Thu Dec 08 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.1-1
- Update config for MyProxy, voms-admin and AMGA, see bugs #86398, #86524 and task #21920
* Wed Nov 23 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.0-1
- New Config for Argus, see bug 86646
* Mon Nov 14 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.0-1
- New provider glite-info-glue2-multi, see bug 86646
* Thu Jul 21 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.7.0-1
- Various updates for voms, CREAM and WMS, see bugs 80789, 81840, 82645, 83105, 83313, 84373
* Thu May 05 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.6.3-1
- ... and fix a missing tab in the make file ...
* Thu May 05 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.6.2-1
- Add the ldif from the test config to the rpm
* Thu May 05 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.6.1-1
- Various minor bug fixes, see patch #4534 for details
* Fri Mar 25 2011 Laurence Field <laurence.field@cern.ch> - 1.5.2-1
- Changed the value of MYPROXY_CONF
* Tue Mar 08 2011 Laurence Field <laurence.field@cern.ch> - 1.5.0-1
- Now FHS Compliant
* Tue Apr 06 2010 Laurence Field <laurence.field@cern.ch> - 1.3.3-1
- Improved packaging
