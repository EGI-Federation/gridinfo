%define debug_package %{nil} 

Summary: grid-monitoring-probes-org.bdii
Name: grid-monitoring-probes-org.bdii
Version: 1.0.9
Vendor: EGEE
Release: 1%{?dist}
License: EGEE
Group: Grid
Source: %{name}-%{version}.src.tgz
Prefix: /
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: openldap
BuildRequires: openldap-devel

%description
This package contains Nagios compatible checks for a WLCG Information System instance (BDII).

%prep

%setup -c

%build
make -f BUILD compile prefix=%{buildroot}%{prefix}

%install
make -f INSTALL install prefix=%{buildroot}%{prefix}

%files
%defattr(-,root,root)
%{prefix}/usr/libexec/grid-monitoring/probes/org.bdii/check_bdii_entries

%clean
rm -rf %{buildroot}

%changelog
* Wed Jul 7 2010 Laurence Field <laurence.field@cern.ch> - 1.0.9-1%{?dist}
- Fix for IS-132.

* Tue Jul 28 2009 Laurence Field <laurence.field@cern.ch> - 1.0.2-1%{?dist}
- Refactored the probe.

* Wed Mar 11 2009 Steve Traylen <steve.traylen@cern.ch> - 1.0.1-2%{?dist}
- Add a dist tag,  %{?dist}.

* Wed Jan 28 2009 James Casey <james.casey@cern.ch> - 1.0.1-1
- Fix bug #46329: check_bdii_published needs to support host aliases better.

* Mon Jan 26 2009 Steve Traylen <steve.traylen@cern.ch> - 1.0.0-4
- Rebuild on SL4 this time. - Paolo Veronesi

* Fri Jan 23 2009 Laurence Field <laurence.field@cern.ch> - 1.0.0-3
- Added generic entries probe

* Thu Dec 18 2008 James Casey <james.casey@cern.ch> - 1.0.0-2
- Moved to usr/libexec/grid/monitoring

* Thu Dec 18 2008 James Casey <james.casey@cern.ch> - 1.0.0-1
- Initial packaging from gstat-nagios-plugins

