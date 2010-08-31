Name:		bdii-config-top
Version:	0.0.1
Release:	1%{?dist}
Summary:	Top BDII configration files
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	bdii
Requires:	glite-info-provider-ldap
Requires:	glite-info-provider-service
Requires:	glite-info-update-endpoints

%description
Configration files for the Top BDII.

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

/opt/glite/etc/gip/provider/glite-info-provider-service-bdii-top
/opt/glite/etc/gip/provider/glite-info-provider-top
/opt/glite/etc/gip/provider/glite-info-provider-service-bdii-top-glue2
/opt/glite/etc/gip/provider/glite-info-provider-top-glue2

%changelog
* Tue Aug 31 2010 Laurence Field <laurence.field@cern.ch> - 0.0.1-1
- New package