Name:		emi-resource-information-service
Version:	1.0.4
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
* Fri Sep 04 2015 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.4-1
- Removing obsolete dependencies and dependencies in yaim (Not available in CENTOS7)

* Wed Nov 14 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.3-1
- Metapackage for emi-resource-information-service including dependency on glue-validator-cron
