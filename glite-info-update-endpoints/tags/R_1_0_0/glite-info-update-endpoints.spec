Name:		glite-info-update-endpoints
Version:	1.0.0
Release:	1%{?dist}
Summary:	Updates LDAP endpoins for EGI and OSG
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Updates LDAP endpoins for EGI and OSG

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
%dir /etc/glite/
%config(noreplace) /etc/glite/glite-info-update-endpoints.conf
/usr/bin/glite-info-update-endpoints
/var/cache/glite/glite-info-update-endpoints
%changelog
* Fri Aug 20 2010 Laurence Field <laurence.field@cern.ch> - 1.0.0-1
- First release
