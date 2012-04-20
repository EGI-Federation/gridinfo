Name:				lcg-infosites
Version:			3.1.0
Release:			2%{?dist}
Summary:			Command line tool for the lcg information system
Group:				Applications/Internet
License:			ASL 2.0
URL:				http://svnweb.cern.ch/trac/gridinfo/wiki
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/lcg-infosites/tags/R_3_1_0 %{name}-%{version}
#   tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0:			%{name}-%{version}.tar.gz

BuildRoot:			%{_tmppath}/%{name}-%{version}-build
BuildArch:			noarch

Requires:			perl
Requires:			perl(Net::LDAP)

%description
lcg-infosites is a simple command line tool in Perl for \
the lcg information system

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/lcg-infosites
%{_mandir}/man1/lcg-infosites.*

%changelog
* Fri Apr 20 2012 Adrien Devresse <adevress at cern.ch> -  3.1.0-2%{?dist}
 - Improved the spec file epel compliance

* Thu Mar 24 2011 Laurence Field <laurence.field@cern.ch> - 3.1.0
- FHS compliant
