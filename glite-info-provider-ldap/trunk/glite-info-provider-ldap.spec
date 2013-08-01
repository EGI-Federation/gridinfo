Name:		glite-info-provider-ldap
Version:	1.4.5
Release:	1%{?dist}
Summary:	LDAP information provider
Group:		Development/Libraries
License:	ASL 2.0
URL:		http://gridinfo.web.cern.ch
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/glite-info-provider-ldap/tags/R_1_4_5_1 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:       openldap-servers

%description
Information provider to query LDAP sources and return the result. 

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
/usr/libexec/glite-info-provider-ldap
%attr(-, ldap, ldap) /var/lib/bdii/gip/tmp/gip/
%attr(-, ldap, ldap) /var/lib/bdii/gip/tmp/gip/log/
%attr(-, ldap, ldap) /var/lib/bdii/gip/cache/gip/
%doc /usr/share/doc/glite-info-provider-ldap/README

%changelog

* Mon Jul 29 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.4.5-1
- Removed log messages used for debugging and added missing state attributes
- Removed cache for Top BDII and define it only for site BDII
- Fixed missing ";"
- BUG #101805: Set to 'unknown' cached GLUE 2 state attributes

* Wed Apr 24 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.4.4-2
- Added Source URL information

* Tue Dec 04 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.4.4-1
- Fix after testing: Use 'resource' instead of 'services' since new alias is not valid in previous BDII versions.

* Tue Nov 20 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.4.3-1
- BUG #98848: Accept GLUE 2.0 LDAP URLs
- BUG #95681: ARC tree in BDII

* Wed Oct 24 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.4.2-1
- BUG #97395: Fixed rpmlint errors: Changed glite-info-provider-ldap path from /opt/glite to /usr
- Added a README file

* Mon Jun 06 2011 Laurence Field <laurence.field@cern.ch> - 1.4.1-1
- Fix for bug #81637 (Missing dependency)

* Tue Mar 22 2011 Laurence Field <laurence.field@cern.ch> - 1.4.0-1
- Change the location of the var directory

* Fri Mar 4 2011 Laurence Field <laurence.field@cern.ch> - 1.3.5-1
- Implemented IS-220

* Fri Feb 18 2011 Laurence Field <laurence.field@cern.ch> - 1.3.4-1
- Implemented IS-207

* Mon Feb 14 2011 Laurence Field <laurence.field@cern.ch> - 1.3.3-1
- Fixed bug 78067

* Thu Apr 1 2010 Laurence Field <laurence.field@cern.ch> - 1.3.0-1
- New version that can also obtain Glue 2.0 information
