Name:		bdii-config-site
Version:	0.1.0
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
/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-site
/var/lib/bdii/gip/provider/glite-info-provider-site

%changelog
* Wed Apr 07 2010 Laurence Field <laurence.field@cern.ch> - 0.1.0-1
- New package
