Name:		glue-service-provider
Version:	1.8.2
Release:	1%{?dist}
Summary:	The GLUE service information provider
License:	ASL 2.0
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#   svn export http://svnweb.cern.ch/guest/gridinfo/glue-service-provider/tags/R_1_8_2_1 %{name}-%{version}
#  tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Group: Development/Libraries
URL: https://tomtools.cern.ch/confluence/display/IS/ResourceBDII

%description
The GLUE service information provider. This enables Grid services to publish 
information according to the GLUE information model.

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
%dir /etc/glue/service-provider
%doc /usr/share/doc/glue-service-provider
%dir %{_libexecdir}/%name
%{_libexecdir}/%name/*

%changelog
* Wed Dec 14 2011 Laurence Field <Laurence.Field@cern.ch> - 1.8.2-1
- Updates for Fedora
* Thu Dec 08 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.1-2
- Fix the spec file
* Thu Dec 08 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.1-1
- Update config for MyProxy, voms-admin and AMGA, see bugs #86398, #86524 and task #21920
* Wed Nov 23 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.0-1
- New Config for Argus, see bug 86646
* Mon Nov 14 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.8.0-1
- New provider glite-info-glue2-multi, see bug 86646
* Thu Jul 21 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.7.0-1
- Various updates for voms, CREAM and WMS, see bugs 80789, 81840, 82645, 83105, 83313, 84373
* Thu May 05 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.6.3-1
- ... and fix a missing tab in the make file ...
* Thu May 05 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.6.2-1
- Add the ldif from the test config to the rpm
* Thu May 05 2011 Stephen Burke <stephen.burke@stfc.ac.uk> - 1.6.1-1
- Various minor bug fixes, see patch #4534 for details
* Fri Mar 25 2011 Laurence Field <laurence.field@cern.ch> - 1.5.2-1
- Changed the value of MYPROXY_CONF
* Tue Mar 08 2011 Laurence Field <laurence.field@cern.ch> - 1.5.0-1
- Now FHS Compliant
* Tue Apr 06 2010 Laurence Field <laurence.field@cern.ch> - 1.3.3-1
- Improved packaging
