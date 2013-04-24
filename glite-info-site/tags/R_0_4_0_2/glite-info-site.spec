Name:		glite-info-site
Version:	0.4.0
Release:	2%{?dist}
Summary:	Site component for the glite-info-static framework.
Group:		System/Monitoring
License:	ASL 2.0
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/glite-info-site/tags/R_0_0_4_2 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Site component for the glite-info-static framework.

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
%dir /etc/glite-info-static/site
%config(noreplace) /etc/glite-info-static/site/site.cfg
%config /etc/glite-info-static/site/site.glue.ifc
%config /etc/glite-info-static/site/site.glue1.tpl
%config /etc/glite-info-static/site/site.glue2.tpl
%config /etc/glite-info-static/site/site.wlcg.ifc

%changelog
* Wed Apr 24 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 0.4.0-2
- Added Source URL information

* Mon Sep 06 2010 Laurence Field <laurence.field@cern.ch> - 0.4.0-1
- Fixes for IS-143, IS-146 and IS-147
* Thu Apr 08 2010 Laurence Field <laurence.field@cern.ch> - 0.2.0-1
- Refactored
* Mon Feb 15 2010 Laurence Field <laurence.field@cern.ch> - 0.1.0-1
- First release
