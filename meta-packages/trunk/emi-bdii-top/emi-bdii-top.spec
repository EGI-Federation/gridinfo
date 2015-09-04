Name:		emi-bdii-top
Version:	1.0.3
Release:	2%{?dist}
Summary:	Metapackage for top BDII 
Group:		Unknown
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       emi-resource-information-service
Requires:       glite-info-provider-ldap
Requires:       bdii-config-top
Obsoletes:      glite-info-plugin-fcr
Requires:       glite-info-update-endpoints

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
* Fri Sep 04 2015 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.3-2
- Removing yaim dependeny (Which is not available in CENTOS7)

* Fri Nov 22 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.2-2
- BUG https://its.cern.ch/jira/browse/GRIDINFO-8: Decommission FCR mechanism

* Mon Nov 12 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.1-2
- Metapackage for emi-bdii-top
