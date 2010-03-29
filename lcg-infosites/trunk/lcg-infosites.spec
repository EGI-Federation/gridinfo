Summary: lcg-infosites
Name: lcg-infosites
Version: 2.6.9
Vendor: LCG/CERN
Release: 1
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

%clean
rm -rf %{buildroot}

