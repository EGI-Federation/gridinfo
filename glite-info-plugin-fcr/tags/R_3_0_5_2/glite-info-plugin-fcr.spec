Name: glite-info-plugin-fcr
Version: 3.0.5
Release: 2%{?dist} 
Summary: Implementation of the Freedom of Choices for Resources contacting SAM
Group:          System Environment/Daemons
License:        ASL 2.0
URL:            https://twiki.cern.ch/twiki/bin/view/EGEE/BDII
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/glite-info-plugin-fcr/tags/R_3_0_5_2 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 
Source:         %{name}-%{version}.src.tgz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Implementation of the Freedom of Choices for Resources contacting SAM

%prep

%setup -q

%build
make install prefix=%{buildroot}

%files
%dir /var/cache/fcr
/usr/libexec/glite-info-plugin-fcr
/etc/cron.hourly/generate-fcr-exclude-file
%doc /usr/share/doc/glite-info-plugin-fcr/README

%clean
rm -rf %{buildroot}

%changelog
* Wed Apr 24 2013 Maria Alandes <Maria.Alandes.Pradillo@cern.ch> - 3.0.5-2
- Added Source URL information

* Wed Oct 24 2012 Maria Alandes <Maria.Alandes.Pradillo@cern.ch> - 3.0.5-1
- Fixed rpmlint errors: Changed glite-info-plugin-fcr path from /opt/glite to /usr
- Added a README file
