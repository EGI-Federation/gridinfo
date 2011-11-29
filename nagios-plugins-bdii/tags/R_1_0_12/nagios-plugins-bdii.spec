Summary: BDII Nagios monitoring Probe
Name: nagios-plugins-bdii
Version: 1.0.12
Release: 1%{?dist}
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/nagios-plugins-bdii/tags/R_1_0_12 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0: %{name}-%{version}.tar.gz
License: ASL 2.0
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildRequires: openldap-devel%{?_isa}
Requires: nagios-common
URL: http://tomtools.cern.ch/confluence/display/IS/BDII+Nagios+Probe

%description
Nagios checks for the BDII.

%prep
%setup -q

%build
CFLAGS='%{optflags}' make compile

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/nagios/plugins/check_bdii_entries

%clean
rm -rf %{buildroot}

%changelog
* Wed Nov 16 2011 Laurence Field <laurence.field@cern.ch> - 1.0.12-1%{?dist}
- Initial Release
