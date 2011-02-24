%define topdir %(pwd)/rpmbuild
%define _topdir %{topdir} 
Summary: glite-info-provider-release
Name: glite-info-provider-release
Version: 1.0.2
Release: 1%{?dist}
License: ASL 2.0
Group:          System/Middleware
Source: %{name}.src.tgz
BuildArch: noarch
Prefix: /opt/glite
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: glite-version >= 3.1.2

%description
Information provider which provides information on the glite version of a service.

%prep

%setup -c

%build
make install prefix=%{buildroot}%{prefix}

%files
%defattr(-,root,root)
%dir %{prefix}/libexec
%{prefix}/libexec/glite-info-provider-release

%clean
rm -rf %{buildroot}
