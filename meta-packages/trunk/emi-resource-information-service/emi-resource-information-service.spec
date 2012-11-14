Name:		emi-resource-information-service
Version:	1.0.3
Release:	1%{?dist}
Summary:	Metapackage for the resource information service
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
* Wed Nov 14 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.3-1
- Metapackage for emi-resource-information-service including dependency on glue-validator-cron
