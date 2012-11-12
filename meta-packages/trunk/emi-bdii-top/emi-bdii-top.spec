Name:		emi-bdii-top
Version:	1.0.1
Release:	2%{?dist}
Summary:	Metapackage for top BDII 
Group:		Unknown
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:     bdii
Requires:     glue-schema
Requires:     glite-info-provider-service
Requires:     glue-validator
Requires:     glue-validator-cron
Requires:     emi-version
Requires:     glite-info-provider-ldap
Requires:     glite-yaim-bdii
Requires:     glite-yaim-core
Requires:     bdii-config-top
Requires:     glite-info-plugin-fcr
Requires:     gliteinfo-update-endpoints

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
* Mon Nov 12 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.1-1
- Metapackage for emi-bdii-top
