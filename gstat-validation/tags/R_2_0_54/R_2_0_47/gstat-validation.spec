Summary: Gstat Valiation Scripts
Name: gstat-validation
Version: 2.0.47
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: EGEE
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Laurence Field <Laurence.Field@cern.ch>
Requires: openldap-clients
Obsoletes: gstat-core
Url: http://goc.grid.sinica.edu.tw/gocwiki/GSIndex

%description
Valiation scripts for an LDAP based information system using the Glue 1.2 schema

%prep
%setup

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
chmod 666 $RPM_BUILD_ROOT/var/lib/gstat/locations
chmod 666 $RPM_BUILD_ROOT/var/lib/gstat/wlcg-tier
chmod 666 $RPM_BUILD_ROOT/var/lib/gstat/service-types
chmod 666 $RPM_BUILD_ROOT/var/lib/gstat/NGI.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
/var/lib/gstat 

%changelog
* Thu Jun 09 2011 Laurence Field <laurence.field@cern.ch>  - 2.0.47-1
- Fix for IS-240 
* Thu Jun 09 2011 Laurence Field <laurence.field@cern.ch>  - 2.0.46-1
- Fix for IS-237 
* Tue Jan 25 2011 Laurence Field <laurence.field@cern.ch>  - 2.0.44-1
- Changed the WLCG Topology URL
* Thu Nov 25 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.41-1
- Fixed issues IS-171
* Wed Jun 30 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.37-1
- Fixed issues IS-153, IS-142, IS-149, IS-125, IS-127
* Wed Jun 30 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.35-1
- Fixed issues IS-95, IS-104, IS-124, IS-125, IS-127
- Now checks NGIs from GOC DB list
* Tue May 18 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.34-1
- Improved the testing of GlueHostProcessorOtherDescription
* Mon May 10 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.32-1
- Fixed issue IS-89
- Fixed issue IS-90
- Fixed issue IS-91
* Tue Apr 28 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.31-1
- The SE tests prints the DN rather than UniqueID
- The error message has been improved for missing GlueSA Size attributes
- root has been re-enabled as an SEAccessProtocol
* Thu Apr 13 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.30-1
- Removed constraint on generic CE Capabilities
* Thu Apr 1 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.29-1
- Fixed two small bugs in the site and service tests
* Tue Mar 26 2010 Laurence Field <laurence.field@cern.ch>  - 2.0.28-1
- A number of minor bugs found in the tests have been fixed
* Tue Dec 1 2009 Steve Traylen <steve.traylen@cern.ch>  - 2.0.25-1
- Don't ask.
* Tue Dec 1 2009 Steve Traylen <steve.traylen@cern.ch>  - 2.0.24-1
- Allow a rounding error for cores * physicals = logicals
  https://savannah.cern.ch/bugs/?59619
* Mon Nov 30 2009 Steve Traylen <steve.traylen@cern.ch>  - 2.0.23-1
- Apply patch from Paul Millar @ DESY.
  Accepts a dCache as a prefix to GlueSACapability values.
  More relaxed about accepting cms as well as VO:cms. Can't
  be fixed till glite-sd-query is fixed.
  https://savannah.cern.ch/bugs/?59690
  https://savannah.cern.ch/bugs/?59699
- Correct spelling mistakes in validte-site.
  https://savannah.cern.ch/bugs/?59698
- Drop requirement of WLCG_ICON
  https://savannah.cern.ch/bugs/?59713
