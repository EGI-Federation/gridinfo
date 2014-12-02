Name:           nagios-plugins-emi.webdav
Version:        1.2.1
Release:        1%{?dist}
Summary:        Nagios module to test webdav interface of egi endpoints
Group:          Applications/Internet
License:        ASL 2.0
Source0:        %{name}-%{version}.tar.gz
URL:            https://svnweb.cern.ch/trac/gridinfo/browser/nagios-plugins-webdav/trunk/README
BuildArch:      noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       time
Requires:       pycurl
Requires:       openldap
Requires:       nagios-plugins-lcgdm-common
Requires:       ca-policy-egi-core

%description
This package provides a nagios module to test webdav interface of egi endpoints

%prep
%setup -q
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libexecdir}/grid-monitoring/probes
mkdir -p %{buildroot}%{python2_sitelib}
mkdir -p %{buildroot}%{_localstatedir}/lib/grid-monitoring/%{name}
cp --preserve=timestamps src/check_webdav_endpoint %{buildroot}%{_libexecdir}/grid-monitoring/probes
cp --preserve=timestamps src/lcgdmcommon.py %{buildroot}%{python2_sitelib}

%files
%{_libexecdir}/grid-monitoring/probes/check_webdav_endpoint
%{python2_sitelib}/lcgdmcommon.py*
%dir %attr(0750,nagios,nagios) %{_localstatedir}/lib/grid-monitoring/%{name}
%doc LICENSE
%doc README


%clean
rm -rf %{buildroot}

%changelog
* Mon Dec 1 2014 Ivan Calvet <ivan.calvet@cern.ch> - 1.2.1-1
- Changed the return status from UNKNOWN to OK if there is no entry in the BDII.

* Thu Sep 25 2014 Ivan Calvet <ivan.calvet@cern.ch> - 1.2.0-1
- Added the possibility of specify the VO and improved return status.

* Tue Sep 23 2014 Ivan Calvet <ivan.calvet@cern.ch> - 1.1.0-1
- Improved test to check writing too.

* Wed Sep 10 2014 Ivan Calvet <ivan.calvet@cern.ch> - 1.0.0-1
- Initial build
