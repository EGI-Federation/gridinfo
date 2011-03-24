Name:		lcg-info
Version:	1.12.0
Release:	1%{?dist}
Summary:	lcg-info
Group:		System Environment/Daemons
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This command line tool queries the LCG information system.

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
/usr/bin/lcg-info
/usr/share/man/man1

%changelog
* Thu Mar 24 2011 Laurence Field <laurence.field@cern.ch> - 1.12.0
- FHS compliant
