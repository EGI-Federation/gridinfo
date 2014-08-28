Name:           check_webdav_endpoint
Version:        1.0.0
Release:        1%{?dist}
Summary:        Nagios module to test webdav interface of egi endpoints.
Group:          Applications/Internet
License:        ASL 2.0
Source:         %{name}-%{version}.tar.gz
URL:            https://svnweb.cern.ch/trac/gridinfo/browser/nagios-plugins-bdii/trunk/src/check_webdav_endpoint
BuildArch:      noarch

BuildRequires:  python2-devel

Requires:       time
Requires:       pycurl
Requires:       ldap
Requires:       lcgdmcommon

%description
This package provides a nagios module to test webdav interface of egi endpoints.

%prep
%setup -qc

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp --preserve=timestamps -r check_webdav_endpoint %{buildroot}/%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/check_webdav_endpoint

%changelog
* Thu Aug 28 2014 Ivan Calvet <ivan.calvet@cern.ch> - 1.0.0-1
- Initial build
