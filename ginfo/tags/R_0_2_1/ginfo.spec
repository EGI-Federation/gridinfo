Name:		ginfo
Version:	0.2.1
Release:	1%{?dist}
Summary:	A verstile tool for discovering Grid services
Group:		Applications/Internet
License:	ASL 2.0
URL:		https://svnweb.cern.ch/trac/gridinfo/browser/ginfo
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/ginfo/tags/R_0_2_1 ginfo-0.2.1
#  tar --gzip -czvf %{name}-%{version}.tar.gz ginfo-0.2.1

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:      python-ldap
%if "%{?dist}" == ".el5"
Requires:      python-json
%endif

%description
A verstile tool for discovering Grid services

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
* Fri Jul 13 2012 Laurence Field <laurence.field@cern.ch> - 0.2.1-1
- Initial version
