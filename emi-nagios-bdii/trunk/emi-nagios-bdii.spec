Summary: BDII Nagios monitoring Probe
Name: emi-nagios-bdii
Version: 1.0.10
Vendor: EMI
Release: 2%{?dist}
License: Apache Software License
Group: Unspecified
Source: %{name}-%{version}.src.tgz
Prefix: /
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Obsoletes: grid-monitoring-probes-org.bdii
Provides: grid-monitoring-probes-org.bdii
Requires: openldap
BuildRequires: openldap-devel

%description
Nagios checks for a the BDII.

%prep

%setup -c

%build
make compile prefix=%{buildroot}%{prefix}

%install
make install prefix=%{buildroot}%{prefix}

%files
%defattr(-,root,root)
%{prefix}/usr/lib64/nagios/plugins/contrib/check_bdii_entries

%clean
rm -rf %{buildroot}

%changelog
* Wed Jul 13 2011 Laurence Field <laurence.field@cern.ch> - 1.0.10-1%{?dist}
- Repackaged for EMI
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

