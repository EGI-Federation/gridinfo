Name:		bdii-config-top
Version:	1.0.8
Release:	1%{?dist}
Summary:	Top BDII configuration files
Group:		Development/Libraries
License:	ASL 2.0
URL:            http://gridinfo.web.cern.ch
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/bdii-config-top/tags/R_1_0_8_1 %{name}-%{version}
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
Requires:	glite-info-update-endpoints
Requires:	glite-info-plugin-fcr
Requires:       glite-info-plugin-delayed-delete-status

%description
Configuration files for the Top BDII

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
%dir /var/log/glite/
/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-top
/var/lib/bdii/gip/provider/glite-info-provider-top
/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-top-glue2
/var/lib/bdii/gip/provider/glite-info-provider-top-glue2
/var/lib/bdii/gip/plugin/glite-info-plugin-fcr
/var/lib/bdii/gip/plugin/glite-info-plugin-delayed-delete-status

%changelog

* Wed Apr 24 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.8-1
- BUG #99298: new plugin to set state attributes of cached entries to 'Unknown'

* Wed Apr 24 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.7-2
- Added Source URL information

* Wed Oct 24 2012 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.7-1
- BUG #97395: Fix rpmlint errors: refer to /usr/libexec instead of /opt/glite/libexec

* Mon May 25 2012 Laurence Field <laurence.field@cern.ch> - 1.0.6-1
- Changed the location of top-urls.conf to address GGUS #73823
* Wed Mar 14 2012 Laurence Field <laurence.field@cern.ch> - 1.0.5-1
- Improved dependency definition
* Tue Aug 22 2011 Laurence Field <laurence.field@cern.ch> - 1.0.4-1
- Fixed #84230 and #84242
* Tue Apr 18 2011 Laurence Field <laurence.field@cern.ch> - 1.0.2-1
- Removed the dependency on glite-info-provider-release
* Tue Apr 05 2011 Laurence Field <laurence.field@cern.ch> - 1.0.1-1
- Fixes for change in glite-info-service
* Tue Mar 15 2011 Laurence Field <laurence.field@cern.ch> - 1.0.0-1
- Made FSH Compliant
* Mon Sep 06 2010 Laurence Field <laurence.field@cern.ch> - 0.0.6-1
- New package
