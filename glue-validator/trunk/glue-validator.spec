Summary: GLUE 2.0 Valiation Scripts
Name: glue-validator
Version: 1.0.0
Release: 1%{?dist}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/glue-validator/tags/R_1_0_0 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0: %{name}-%{version}.tar.gz
License: ASL 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
BuildRequires: python2-devel
Requires: openldap-clients
Url: http://cern.ch/glue

%if 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%description
Valiation scripts for an LDAP based information system using the Glue 2.0 schema

%prep
%setup -q

%build
python setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/glue-validator

%changelog
* Fri Nov 11 2011 Laurence Field <laurence.field@cern.ch>  - 1.0.0-1
- Initial Release
