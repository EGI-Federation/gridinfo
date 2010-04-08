Name:		glite-info-site
Version:	0.2.0
Release:	1%{?dist}
Summary:	Site component for the glite-info-static framework.
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
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
* Thu Apr 08 2010 Laurence Field <laurence.field@cern.ch> - 0.2.0-1
- Refactored
* Mon Feb 15 2010 Laurence Field <laurence.field@cern.ch> - 0.1.0-1
- First release
