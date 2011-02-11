Summary: GLUE 2.0 Valiation Scripts
Name: glue-validator
Version: 0.0.2
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: EGEE
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Laurence Field <Laurence.Field@cern.ch>
Requires: openldap-clients
Url: http://cern.ch/glue

%description
Valiation scripts for an LDAP based information system using the Glue 2.0 schema

%prep
%setup

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)


%changelog
* Tue Jan 18 2011 Laurence Field <laurence.field@cern.ch>  - 0.0.1-1
- Initial Version
