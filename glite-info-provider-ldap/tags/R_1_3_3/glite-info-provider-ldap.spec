Name:		glite-info-provider-ldap
Version:	1.3.3
Release:	1%{?dist}
Summary:	LDAP information provider
Group:		System/Monitoring
License:	ASL 2.0
URL:		https://twiki.cern.ch/twiki/bin/view/EGEE/BDII
#               wget -O %{name}-%{version}-443.tar.gz "http://svnweb.cern.ch/world/wsvn/gridinfo/bdii/tags/R_5_1_0?op=dl&rev=443"
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
An informatio provider that queries a number of LDAP sources and return the result. 

%prep
%setup -q
#change to the one below if you are building against downloaded tarball from svnweb.cern.ch
#%setup -q -n trunk.r443

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/glite/libexec/glite-info-provider-ldap
%attr(-, ldap, ldap) /opt/glite/var/tmp/gip/
%attr(-, ldap, ldap) /opt/glite/var/tmp/log/
%attr(-, ldap, ldap) /opt/glite/var/cache/gip/

%changelog
* Mon Feb 14 2011 Laurence Field <laurence.field@cern.ch> - 1.3.3-1
- Fixed bug 78067
* Thu Apr 1 2010 Laurence Field <laurence.field@cern.ch> - 1.3.0-1
- New version that can also obtain Glue 2.0 information
