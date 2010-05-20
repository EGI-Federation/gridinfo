Name:		bdii-config-site
Version:	0.6.0
Release:	1%{?dist}
Summary:	Site BDII configration files
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	bdii
Requires:	glite-info-provider-ldap
Requires:	glite-info-provider-service
Requires:	glite-info-static
Requires:	glite-info-site

%description
Configration files for the Site BDII.

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

%dir /opt/glite/etc/gip/ldif
%dir /opt/glite/etc/gip/provider
%dir /opt/glite/etc/gip/plugin
/opt/glite/etc/gip/provider/glite-info-provider-service-bdii-site
/opt/glite/etc/gip/provider/glite-info-provider-site
/opt/glite/etc/gip/site-urls.conf
/opt/glite/etc/gip/provider/glite-info-provider-service-bdii-site-glue2
/opt/glite/etc/gip/provider/glite-info-provider-site-entry
/opt/glite/etc/gip/provider/glite-info-provider-site-entry-glue2
/opt/glite/etc/gip/provider/glite-info-provider-site-glue2



%changelog
* Thu May 20 2010 Laurence Field <laurence.field@cern.ch> - 0.5.0-1
- Changed to /opt/glite/etc
* Wed Apr 07 2010 Laurence Field <laurence.field@cern.ch> - 0.4.0-1
- New package
