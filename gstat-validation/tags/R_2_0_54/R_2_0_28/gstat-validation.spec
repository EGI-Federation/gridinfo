Summary: Gstat Valiation Scripts
Name: gstat-validation
Version: 2.0.28
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: EGEE
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Laurence Field <Laurence.Field@cern.ch>
Requires: openldap-clients
Requires: python-dns
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
chmod 777 $RPM_BUILD_ROOT/usr/share/gstat/locations
chmod 777 $RPM_BUILD_ROOT/usr/share/gstat/wlcg-tier
chmod 777 $RPM_BUILD_ROOT/usr/share/gstat/service-types

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
/usr/share/gstat 

%changelog
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
