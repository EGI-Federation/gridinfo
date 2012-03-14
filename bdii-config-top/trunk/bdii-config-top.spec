Name:		bdii-config-top
Version:	1.0.5
Release:	1%{?dist}
Summary:	Top BDII configration files
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	bdii
%if 0%{?el5}
Requires: openldap2.4-servers
%else
Requires: openldap-servers 
%endif
Requires:	glite-info-provider-ldap
Requires:	glite-info-provider-service
Requires:	glite-info-update-endpoints

%description
Configration files for the Top BDII.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-top
/var/lib/bdii/gip/provider/glite-info-provider-top
/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-top-glue2
/var/lib/bdii/gip/provider/glite-info-provider-top-glue2
/var/lib/bdii/gip/plugin/glite-info-plugin-fcr

%changelog
* Wed Mar 14 2012 Laurence Field <laurence.field@cern.ch> - 1.0.5-1
- Improved dependency definition
* Tue Aug 22 2011 Laurence Field <laurence.field@cern.ch> - 1.0.4-1
- Fixed #84230 and #84242
* Tue Apr 18 2011 Laurence Field <laurence.field@cern.ch> - 1.0.2-1
- Removed the dependency on glite-info-provider-release
* Tue Apr 05 2011 Laurence Field <laurence.field@cern.ch> - 1.0.1-1
- Fixes for change in glite-info-service
* Tue Mar 15 2011 Laurence Field <laurence.field@cern.ch> - 1.0.0-1
- Made FSH Compliant
* Mon Sep 06 2010 Laurence Field <laurence.field@cern.ch> - 0.0.6-1
- New package
