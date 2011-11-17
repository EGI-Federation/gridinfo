Name:		glite-info-provider-service
Version:	1.4.4
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
%dir /opt/glite/libexec
%dir /opt/glite/etc
%dir /opt/glite/doc
/opt/glite/libexec/glite-info-glue2-service
/opt/glite/libexec/glite-info-glue2-endpoint
/opt/glite/libexec/glite-info-glue2-simple
/opt/glite/libexec/glite-info-service
/opt/glite/libexec/glite-info-service-glue2
/opt/glite/libexec/glite-info-service-test
/opt/glite/libexec/glite-info-service-amga
/opt/glite/libexec/glite-info-service-bdii
/opt/glite/libexec/glite-info-service-gridice
/opt/glite/libexec/glite-info-service-vobox
/opt/glite/libexec/glite-info-service-voms
/opt/glite/libexec/glite-info-service-voms-wrapper
/opt/glite/libexec/glite-info-service-voms-admin
/opt/glite/libexec/glite-info-service-myproxy
/opt/glite/libexec/glite-info-service-wmproxy
/opt/glite/libexec/glite-info-service-lbserver
/opt/glite/libexec/glite-info-service-frontier
/opt/glite/libexec/glite-info-service-squid
/opt/glite/libexec/glite-info-service-cream
/opt/glite/libexec/glite-info-service-dcache
/opt/glite/libexec/glite-info-service-dpm
/opt/glite/libexec/glite-info-service-rtepublisher
/opt/glite/libexec/glite-info-service-gatekeeper
/opt/glite/libexec/glite-info-service-status
/opt/glite/etc/glite-info-glue2-amga.conf.template
/opt/glite/etc/glite-info-glue2-bdii-top.conf.template
/opt/glite/etc/glite-info-glue2-lbserver.conf.template
/opt/glite/etc/glite-info-glue2-rtepublisher.conf.template
/opt/glite/etc/glite-info-glue2-vobox.conf.template
/opt/glite/etc/glite-info-glue2-frontier.conf.template
/opt/glite/etc/glite-info-glue2-squid.conf.template
/opt/glite/etc/glite-info-service-test.conf.template
/opt/glite/etc/glue1.test.ldif
/opt/glite/etc/glue2.test.ldif
/opt/glite/etc/glite-info-service-amga.conf.template
/opt/glite/etc/glite-info-service-bdii.conf.template
/opt/glite/etc/glite-info-service-bdii-site.conf.template
/opt/glite/etc/glite-info-service-bdii-top.conf.template
/opt/glite/etc/glite-info-service-gridice.conf.template
/opt/glite/etc/glite-info-service-gsirfio.conf.template
/opt/glite/etc/glite-info-service-lbserver.conf.template
/opt/glite/etc/glite-info-service-frontier.conf.template
/opt/glite/etc/glite-info-service-squid.conf.template
/opt/glite/etc/glite-info-service-cream.conf.template
/opt/glite/etc/glite-info-service-cemon.conf.template
/opt/glite/etc/glite-info-service-myproxy.conf.template
/opt/glite/etc/glite-info-service-vobox.conf.template
/opt/glite/etc/glite-info-service-voms.conf.template
/opt/glite/etc/glite-info-service-voms-admin.conf.template
/opt/glite/etc/glite-info-service-srm-dcache-v1.conf.template
/opt/glite/etc/glite-info-service-srm-dcache-v2.conf.template
/opt/glite/etc/glite-info-service-srm-dpm-v1.conf.template
/opt/glite/etc/glite-info-service-srm-dpm-v2.conf.template
/opt/glite/etc/glite-info-service-wmproxy.conf.template
/opt/glite/etc/glite-info-service-rtepublisher.conf.template
/opt/glite/etc/glite-info-service-gatekeeper.conf.template
/opt/glite/etc/glite-info-glue2-test.conf.template
/opt/glite/etc/glite-info-glue2-service-test.conf.template
/opt/glite/etc/glite-info-glue2-bdii-site.conf.template
%doc /opt/glite/doc/README
%doc /opt/glite/doc/README-GLUE2


%changelog
* Tue Apr 06 2010 Laurence Field <laurence.field@cern.ch> - 1.3.3-1
- Improved packaging
