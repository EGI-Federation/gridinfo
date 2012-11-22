Name:		emi-bdii-top
Version:	1.0.1
Release:	2%{?dist}
Summary:	Metapackage for top BDII 
Group:		Unknown
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:     emi-resource-information-service
Requires:     glite-info-provider-ldap
Requires:     glite-yaim-bdii
Requires:     glite-yaim-core
Requires:     bdii-config-top
Requires:     glite-info-plugin-fcr
Requires:     glite-info-update-endpoints

%description
%{summary}

%prep
%setup -q

%build
rm -rf %{buildroot}
make install prefix=%{buildroot}

%install

%files

%changelog
* Mon Nov 12 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.1-2
- Metapackage for emi-bdii-top
