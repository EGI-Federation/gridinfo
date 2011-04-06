Name:		glite-info-provider-release
Version:	1.0.3
Release:	1%{?dist}
Summary:	glite-info-provider-release
Group:		System/Monitoring
License:	Apache Software License
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires: glite-version >= 3.1.2

%description
Information provider which provides information on the glite version of a service.

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
%dir /opt/glite/libexec
/opt/glite/libexec/glite-info-provider-release

