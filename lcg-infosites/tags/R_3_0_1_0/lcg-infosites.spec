Summary: lcg-infosites
Name: lcg-infosites
Version: 3.0.1
Vendor: LCG/CERN
Release: 3
License: LCG
Group: LCG
Source: %{name}.src.tgz
BuildArch: noarch
Prefix: /opt/lcg
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Packager: LCG

Obsoletes: lcg-info-api-ldap

%description
information system wrapper

%prep

%setup -c

%build
make install prefix=%{buildroot}%{prefix}


%files
%defattr(-,root,root)
%{prefix}/bin/lcg-infosites
%{prefix}/man/man1/lcg-infosites.1

%clean
rm -rf %{buildroot}

