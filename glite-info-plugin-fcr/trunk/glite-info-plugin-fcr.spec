%define topdir %(pwd)/rpmbuild
%define _topdir %{topdir} 
Summary: glite-info-plugin-fcr
Name: glite-info-plugin-fcr
Version: 2.0.0
Vendor: EGEE
Release: 1
License: EGEE
Group: EGEE
Source: %{name}.src.tgz
BuildArch: noarch
Prefix: /opt/glite
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Packager: EGEE
Requires: glite-info-generic

%description
An information plugin to be used with the Generic Information Provider. This provider will download the Freedom of Choices for Resources page. 

%prep

%setup -c

%build
make install prefix=%{buildroot}

%post

%preun

%postun

%files
%dir /var/cache/fcr
%{prefix}/libexec/glite-info-plugin-fcr
/etc/cron.hourly/generate-fcr-exclude-file

%clean
rm -rf %{buildroot}
