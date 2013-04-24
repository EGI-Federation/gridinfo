Name:		bdii-config-site
Version:	1.0.7
Release:	2%{?dist}
Summary:	Site BDII configration files
Group:		Development/Libraries
License:	ASL 2.0
URL:            https://tomtools.cern.ch/confluence/display/IS/Home 
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/bdii-config-site/tags/R_1_0_7_2 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	bdii
%if "%{?dist}" == ".el5"
Requires: openldap2.4-servers
%else
Requires: openldap-servers 
%endif
Requires:	glite-info-provider-ldap
Requires:	glite-info-provider-service
Requires:	glite-info-static
Requires:	glite-info-site

%description
Configuration files for the Site BDII.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-site
/var/lib/bdii/gip/provider/glite-info-provider-site
%config(noreplace) /etc/bdii/gip/site-urls.conf
/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-site-glue2
/var/lib/bdii/gip/provider/glite-info-provider-site-entry
/var/lib/bdii/gip/provider/glite-info-provider-site-entry-glue2
/var/lib/bdii/gip/provider/glite-info-provider-site-glue2

%changelog
* Wed Apr 24 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.7-2
- Added Source URL information

* Wed Oct 24 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.7-1
- #BUG 98427: Fixed rpmlint errors: Changed /opt/glite/libexec to /usr/libexec

* Wed Mar 14 2012 Laurence Field <laurence.field@cern.ch> - 1.0.6-1
- Improved dependency definition
* Tue Aug 22 2011 Laurence Field <laurence.field@cern.ch> - 1.0.5-1
- Fixed #84241
* Tue Apr 18 2011 Laurence Field <laurence.field@cern.ch> - 1.0.3-1
- Removed the dependency on glite-info-provider-release
* Tue Apr 05 2011 Laurence Field <laurence.field@cern.ch> - 1.0.2-1
- Fixed error due to new version of glite-info-provider-service
* Mon Mar 21 2011 Laurence Field <laurence.field@cern.ch> - 1.0.1-1
- Changed config location to /etc/bdii/gip
* Tue Mar 15 2011 Laurence Field <laurence.field@cern.ch> - 1.0.0-1
- Fixed Is-148
* Mon Sep 06 2010 Laurence Field <laurence.field@cern.ch> - 0.9.0-1
- Fixed Is-148
* Thu May 20 2010 Laurence Field <laurence.field@cern.ch> - 0.7.0-1
- Changed to /opt/glite/etc
* Wed Apr 07 2010 Laurence Field <laurence.field@cern.ch> - 0.4.0-1
- New package
