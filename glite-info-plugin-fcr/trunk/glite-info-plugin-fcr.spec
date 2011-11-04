Name: glite-info-plugin-fcr
Version: 2.0.2
Release: 2%{?dist} 
Summary: glite-info-plugin-fcr
Group:          System Environment/Daemons
License:        ASL 2.0
URL:            https://twiki.cern.ch/twiki/bin/view/EGEE/BDII
Source:         %{name}-%{version}.src.tgz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
An information plugin to be used with the Generic Information Provider. This provider will download the Freedom of Choices for Resources page. 

%prep

%setup -q

%build
make install prefix=%{buildroot}

%post

%files
%dir /var/cache/fcr
/opt/glite/libexec/glite-info-plugin-fcr

%clean
rm -rf %{buildroot}
