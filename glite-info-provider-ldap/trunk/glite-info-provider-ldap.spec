%define topdir %(pwd)/rpmbuild
%define _topdir %{topdir} 
Summary: glite-info-provider-ldap
Name: glite-info-provider-ldap
Version: 1.2.4
Vendor: EGEE
Release: 2
License: EGEE
Group: EGEE
Source: %{name}.src.tgz
BuildArch: noarch
Prefix: /opt/glite
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Packager: EGEE
Requires: glite-info-generic

%description
An information provider to be used with the Generic Information Provider.
This provider will query a number of LDAP sources and return the result. 

%prep

%setup -c

%build
make install prefix=%{buildroot}%{prefix}

%post

%preun

%postun

%files
%defattr(-,root,root)
%{prefix}/libexec/glite-info-provider-ldap

%clean
rm -rf %{buildroot}
