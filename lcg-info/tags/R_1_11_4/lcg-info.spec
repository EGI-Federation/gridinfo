Summary: Command to interrogate the LCG information system
Name: lcg-info
Version: 1.11.4
Release: 1
License: LCG
Vendor: LCG/CERN
Group: LCG
BuildArch: noarch
Source: %{name}.src.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Prefix: /opt/lcg
Packager: Andrea.Sciaba@cern.ch

%description
This command allows to make queries to the LCG information system.

%prep
%setup -c

%build
make install prefix=%{buildroot}%{prefix}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{prefix}/bin/lcg-info
%{prefix}/man/man1/lcg-info.1
