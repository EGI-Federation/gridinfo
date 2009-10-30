Summary: GStat Web Applciation
Name: gstat-web
Version: 0.0.17
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.gz
License: Apache license v2.0
Group: Web Application
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
Vendor: Laurence Field <Laurence.Field@cern.ch>
Url: http://goc.grid.sinica.edu.tw/gocwiki/GSIndex
Requires: gstat-core
Requires: gstat-validation
Requires: glite-yaim-nagios
Requires: grid-monitoring-probes-org.bdii
Requires: nagios >= 3.0.0
Requires: nagios-htpasswd
Requires: nagios-plugins
Requires: nagios-plugins-ping
Requires: nagios-plugins-dns
Requires: nagios-plugins-ldap
Requires: pnp4nagios
Requires: mod_wsgi
Requires: mod_ssl
Requires: mysql-server
Requires: Django
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

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog -f ChangeLog
