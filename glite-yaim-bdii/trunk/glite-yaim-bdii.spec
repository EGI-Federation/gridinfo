Name:		glite-yaim-bdii
Version:	4.3.14
Release:	1%{?dist}
Summary:	glite-yaim-bdii module configures the top level BDII and site BDI
Group:		Development/Tools
License:	Apache Software Li
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package contains the yaim functions necessary to configure the top level and site BDII.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}/opt/glite
make install prefix=%{buildroot}/opt/glite

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/glite/yaim/functions/config_*
/opt/glite/yaim/defaults/*.pre
%config /opt/glite/yaim/node-info.d/emi-*
/opt/glite/yaim/examples/siteinfo/services/emi-*
/opt/glite/yaim/etc/versions/%{name}
%doc LICENSE

%changelog
* Thu Aug 01 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 4.3.14-1
- BUG #101389: Added BDII_RAM_SIZE

* Wed Nov 14 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 4.3.13-1
- Change EMIR integration approach to use the built-in feature provided by EMIR publisher to use the resource BDII

* Wed Oct 24 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 4.3.12-1 
- BUG #98187: EMIR integration
- BUG #98369: cleaning

* Wed Aug 01 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 4.3.11-1
- After integration testing decided to make BDII_IPV6_SUPPORT not mandatory. Default in init.d script is 'no' in any case.

* Wed Jul 18 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 4.3.10-1
- BUG 95839: Added BDII_IPV6_SUPPORT
- BUG 95123: Create /etc/bdii/gip if it doesn't exist
- BUG 95043: Cleaning YAIM variables that are no longer used
- Removed EGEE license text and added missing headers
- Removing functions from gLite that are no longer needed
