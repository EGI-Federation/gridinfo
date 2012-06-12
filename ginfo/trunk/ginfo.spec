Name:		service-discovery
Version:	0.0.72
Release:	1%{?dist}
Summary:	Service Discovery Client

Group:		Applications/Internet
License:	ASL 2.0
URL:		https://svnweb.cern.ch/trac/gridinfo/browser/service-discovery
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/service-discovery/tags/R_0_0_35 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:      python-ldap
Requires:      python-json

%description
Service Discovery Client for obtaining GLUE 2.0 information on Grid services. 

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
%{_bindir}/serviceInfo
%{_mandir}/man1/serviceInfo.1*
%doc LICENSE

%changelog
* Thu Jun 07 2012 Laurence Field <laurence.field@cern.ch> - 0.0.72-1
- Initial version
