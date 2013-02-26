%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif
Summary: A validation framework for Grid information providers
Name: glue-validator
Version: 2.0.5
Release: 0%{?dist}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/glue-validator/tags/R_1_0_5 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0: %{name}-%{version}.tar.gz
License: ASL 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch
BuildRequires: python-devel
Requires: openldap-clients
Url: http://cern.ch/glue

%description
A validation framework for Grid information providers. 
This framework validates the information return against the GLUE information 
model from the Open Grid Forum. 

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT 
mkdir -p %{buildroot}/usr/share/man/man1
install -m 0644 man/glue-validator.1 %{buildroot}/usr/share/man/man1

%post
mkdir -p /var/lib/grid-monitoring/glue-validator

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE
%{python_sitelib}/*
%{_bindir}/glue-validator
%{_mandir}/man1/glue-validator.1.gz

%changelog
* Tue Feb 26 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.5-0
- Added types for WLCG names, VO names and EGI NGIs.
- Added specific attribute tests: OtherInfo, ComputingManager and ExecutionEnvironment (ongoing)

* Mon Feb 25 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.4-0
- Added specific attribute tests: ComputingShare and ComputingManager (ongoing)
- BUG #100467: Fixed typo in Capability_t and added values reported at the EMT
- BUG #100608: Added values reported at the EMT for ServiceType_t and InterfaceName_t 

* Wed Feb 13 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.3-0
- Modified EntryTest to check Undesirable attributes
- Added specific attribute tests in EGIProfileTest
- Added types in egi-glue2 types

* Wed Feb 06 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.2-0
- Adapt EntryTest to be used also for EGI profile and leave specific attribute tests in EGIProfileTest
- Tuning of egi-glue2/data.py and egi-glue2/types.py
- Added verbose debug level in nagios output

* Tue Feb 05 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.1-0
- New option to produce nagios output 

* Mon Jan 28 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.0-0
- Changes to include validation against EGI profile for GLUE 2.0 and WLCG specific tests

* Wed Nov 21 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.5-1
- BUG #98982: voms added to is_allowed_URL_Schema in GLUE 1 and 2

* Tue Nov 20 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.4-1
- BUG #98683: New test to check attributes are not empty  
- BUG #98948: GLUE2Group class has been updated with GLUE2GroupName

* Fri Oct 12 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.3-1
- BUG #98104: ldap added to is_allowed_URL_Schema in GLUE 1 and 2
- BUG #97155: information.publication is now added to Capability_t

* Wed Dec 14 2011 Laurence Field <laurence.field@cern.ch>  - 1.0.2-1
- New upstream version and packaging improvements

* Mon Dec 05 2011 Laurence Field <laurence.field@cern.ch>  - 1.0.1-1
- New upstream version and packaging improvements

* Fri Nov 11 2011 Laurence Field <laurence.field@cern.ch>  - 1.0.0-1
- Initial Release
