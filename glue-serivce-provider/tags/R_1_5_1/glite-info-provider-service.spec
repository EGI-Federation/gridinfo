Name:		glite-info-provider-service
Version:	1.5.1
Release:	1%{?dist}
Summary:	The GLUE service information provider
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
The GLUE service information provider

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir /usr/bin
%dir /etc/glite/info/service
%dir /usr/share/doc/%{name}
/usr/bin/glite-info-glue2-service
/usr/bin/glite-info-glue2-endpoint
/usr/bin/glite-info-glue2-simple
/usr/bin/glite-info-service
/usr/bin/glite-info-service-glue2
/usr/bin/glite-info-service-test
/usr/bin/glite-info-service-amga
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
/etc/glite/info/service/glite-info-glue2-bdii-top.conf.template
/etc/glite/info/service/glite-info-glue2-lbserver.conf.template
/etc/glite/info/service/glite-info-glue2-rtepublisher.conf.template
/etc/glite/info/service/glite-info-glue2-vobox.conf.template
/etc/glite/info/service/glite-info-glue2-frontier.conf.template
/etc/glite/info/service/glite-info-glue2-squid.conf.template
/etc/glite/info/service/glite-info-glue2-myproxy.conf.template
/etc/glite/info/service/glite-info-service-test.conf.template
/etc/glite/info/service/glite-info-service-amga.conf.template
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
/etc/glite/info/service/glite-info-glue2-service-test.conf.template
/etc/glite/info/service/glite-info-glue2-bdii-site.conf.template
%doc /usr/share/doc/%{name}/README
%doc /usr/share/doc/%{name}/README-GLUE2


%changelog
* Tue Mar 08 2011 Laurence Field <laurence.field@cern.ch> - 1.5.0-1
- Now FHS Compliant
* Tue Apr 06 2010 Laurence Field <laurence.field@cern.ch> - 1.3.3-1
- Improved packaging
