Name:		glite-yaim-bdii
Version:	4.3.8
Release:	1%{?dist}
Summary:	glite-yaim-bdii module configures the top level BDII and site BDI
Group:		Development/Tools
License:	Apache Software Li
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package contains the yaim functions necessary to configure the top level and site BDII.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}/opt/glite
make install prefix=%{buildroot}/opt/glite

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/glite/yaim/functions/config_*
/opt/glite/yaim/defaults/*.pre
%config /opt/glite/yaim/node-info.d/glite-*
%config /opt/glite/yaim/node-info.d/emi-*
/opt/glite/yaim/examples/siteinfo/services/glite-*
/opt/glite/yaim/etc/versions/%{name}
%doc LICENSE