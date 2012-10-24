Name: glite-info-plugin-fcr
Version: 3.0.5
Release: 1%{?dist} 
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
/usr/libexec/glite-info-plugin-fcr
/etc/cron.hourly/generate-fcr-exclude-file

%clean
rm -rf %{buildroot}

%changelog
* Wed Oct 24 2012 Maria Alandes <Maria.Alandes.Pradillo@cern.ch> - 3.0.5-1
- Fixed rpmlint errors: Changed glite-info-plugin-fcr path from /opt/glite to /usr
