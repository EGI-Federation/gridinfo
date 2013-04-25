Name:		ginfo
Version:	1.0.1
Release:	1%{?dist}
Summary:	A versatile tool for discovering Grid services
Group:		Applications/Internet
License:	ASL 2.0
URL:		https://svnweb.cern.ch/trac/gridinfo/browser/ginfo
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/ginfo/tags/R_1_0_1 ginfo-1.0.1
#  tar --gzip -czvf ginfo-1.0.1.tar.gz ginfo-1.0.1

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:      python-ldap
%if "%{?dist}" == ".el5"
Requires:      python-simplejson
%endif

%description
A versatile tool for discovering Grid services by querying either 
LDAP-based Grid information services or the EMI Registry.

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
%{_bindir}/ginfo
%{_mandir}/man1/ginfo.1*
%doc LICENSE

%changelog
* Thu Apr 25 2013 Laurence Field <laurence.field@cern.ch> - 1.0.1-1
- Refactored version enabling general GLUE 2.0 queries
* Thu Oct 25 2012 Laurence Field <laurence.field@cern.ch> - 0.2.4-1
- Added -b --bind option.
* Wed Aug 29 2012 Laurence Field <laurence.field@cern.ch> - 0.2.3-1
- Improved the EMI output.
* Thu Jul 19 2012 Laurence Field <laurence.field@cern.ch> - 0.2.2-1
- Added a timeout for the queries. 
* Fri Jul 13 2012 Laurence Field <laurence.field@cern.ch> - 0.2.1-2
- Initial version
