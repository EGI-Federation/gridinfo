Summary: GStat Web Applciation
Name: gstat-web
Version: 1.0.11
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: Apache license v2.0
Group: Web Application
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Laurence Field <Laurence.Field@cern.ch>, David Horat <David.Horat@cern.ch>, Joanna Huang <joanna@twgrid.org>
Url: https://svnweb.cern.ch/trac/gridinfo/wiki#GStat
Requires: gstat-validation
Requires: glite-yaim-nagios
Requires: grid-monitoring-probes-org.bdii
Requires: nagios >= 3
Requires: voms-htpasswd
Requires: nagios-plugins
Requires: pnp4nagios
Requires: mod_wsgi
Requires: mod_ssl
Requires: mysql-server
Requires: django > 1.2.1
Requires: php
Requires: MySQL-python > 1.2.1

%description
The GStat web application

%prep
%setup

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mv %{buildroot}/usr/share/gstat/manage.py %{buildroot}/usr/share/gstat/manage
sed -i 's/manage.py/manage/' INSTALLED_FILES
chmod +x %{buildroot}/usr/share/gstat/manage
chmod +x %{buildroot}/usr/share/gstat/gstat.wsgi
mkdir -p  %{buildroot}/var/log/gstat/


%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
/var/log/gstat

%changelog -f ChangeLog
