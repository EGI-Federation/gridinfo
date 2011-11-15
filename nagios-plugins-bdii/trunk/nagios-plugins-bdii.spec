Summary: BDII Nagios monitoring Probe
Name: nagios-plugins-bdii
Version: 1.0.11
Release: 1%{?dist}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/nagios-plugins-bdii/tags/R_1_0_11 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0: %{name}-%{version}.tar.gz
License: ASL 2.0
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-build
Requires: openldap
BuildRequires: openldap-devel
Url: http://tomtools.cern.ch/confluence/display/IS/BDII+Nagios+Probe

%description
Nagios checks for a the BDII.

%prep
%setup -q

%build
make compile prefix=%{buildroot}

%install
make install prefix=%{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nagios/plugins/contrib/check_bdii_entries

%clean
rm -rf %{buildroot}

%changelog
* Fri Nov 11 2011 Laurence Field <laurence.field@cern.ch> - 1.0.11-1%{?dist}
- Initial Release
