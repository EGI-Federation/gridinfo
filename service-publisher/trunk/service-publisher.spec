Name:		service-publisher
Version:	0.0.1
Release:	1%{?dist}
Summary:	Service Publisher

Group:		Applications/Internet
License:	ASL 2.0
URL:		https://svnweb.cern.ch/trac/gridinfo/browser/service-publisher
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/service-publisher/tags/R_0_0_1 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	python-ldap

%description
Service Publishing Client that translate between LDAP into JSON.

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
%{_bindir}/service-publisher
%{_mandir}/man1/service-publisher.1*
%doc LICENSE

%changelog
* Thu May 25 2012 Laurence Field <laurence.field@cern.ch> - 0.0.1-1
- Initial version
