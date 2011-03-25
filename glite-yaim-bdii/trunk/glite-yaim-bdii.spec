%define topdir %(pwd)/rpmbuild
%define _topdir %{topdir} 
Summary: glite-yaim-bdii module configures the top level BDII and site BDII.
Name: glite-yaim-bdii
Version: 4.3.1
Vendor: EGEE
Release: 1
License: EGEE
Group: EGEE
Source: %{name}.src.tgz
BuildArch: noarch
Prefix: /opt/glite
Requires: glite-yaim-core
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Packager: EGEE

%description
This package contains the yaim functions necessary to configure the top level and site BDII.

%prep

%setup -c

%build
make install prefix=%{buildroot}%{prefix}

%files
%defattr(-,root,root)
%{prefix}/yaim/functions/config_*
%{prefix}/yaim/defaults/*.pre
%config %{prefix}/yaim/node-info.d/glite-*
%config %{prefix}/yaim/node-info.d/emi-*
%{prefix}/yaim/examples/siteinfo/services/glite-*
%{prefix}/yaim/etc/versions/%{name}
%doc LICENSE


%clean
rm -rf %{buildroot}



