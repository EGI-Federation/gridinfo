%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif
Summary: A validation framework for Grid information providers
Name: glue-validator
Version: 2.0.17
Release: 0%{?dist}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/glue-validator/tags/R_2_0_17 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0: %{name}-%{version}.tar.gz
License: ASL 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildArch: noarch
BuildRequires: python-devel
Requires: openldap-clients
Url: http://gridinfo.web.cern.ch/glue/glue-validator-guide

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE
%{python_sitelib}/*
%{_bindir}/glue-validator
%{_mandir}/man1/glue-validator.1.gz

%changelog

* Fri May 31 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.17-0
- Fixed messages in EntryTest that were not concatenated
- Removed obsolete of glue-validator-cron that is now fixed
- Update spec URL to point to new Information System web pages

* Mon May 06 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.16-0
- Fixed bug with dates: GLUE dates were transformed into UTC when they already are UTC 

* Tue Apr 30 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.15-0
- Defined new verbose level 2 for nagios output
- Added associated attribute to message dictionary
- Added sanity checks for the command line options (nagios, verbosity level and separator) 

* Mon Apr 29 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.14-0
- Defined a general message generator function and added an option to define a separator
- Added missing type
- Fixed OtherInfo type check that is not done in the general test but on specific tests

* Fri Apr 26 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.13-0
- Improved error, warning and info messages defining a common structure for all tests
- Defined OtherInfo as a multivalued attribute in the EGI profile
- Improved the EGI profile types

* Fri Apr 12 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.12-0
- Modified Entrytest to collect all erros within an object instead of terminating after the first error is found
- Modified EGIProfile to fix bug related to date and time and references to non existing attributes
- Removed extra type checks from individual tests in EGIProfile
- Defined OtherInfo attribute as optional
- Updated the nagios output function in utils to deal with 'grouped' failure messages coming from Entrytest tests  

* Tue Mar 12 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.11-0
- Transformed creation times into UTC
- Extended types after reviewing information providers

* Fri Mar 08 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.10-0
- Fixed datetime problem not working in SL5
- Removed tests that were already part of the general type check test
- Reviewed ForeignKey attributes

* Thu Mar 07 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.9-0
- Improved error messages and fixed bugs in existing tests after feedback from beta testing
- Fixed problem with output redirection to file for the testsuite output
- Added exclude-known-issues flag 

* Tue Mar 05 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.8-0
- BUG #100733: Applied changes requested by Nagios team to be Nagios compliant

* Thu Feb 28 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.7-0
- Added missing error message type
- Added missing Endpoint_t, Capability_t and ServiceType_t requested by ARC

* Wed Feb 27 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 2.0.6-0
- Added types for Middleware names
- Fixed typo in data.py
- Added specific attribute tests: ExecutionEnvironment, ApplicationEnvironment, Storage, Endpoint

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
