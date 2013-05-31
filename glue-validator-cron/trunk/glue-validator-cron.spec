Name: glue-validator-cron
Version: 1.2.0
Release: 1%{?dist} 
Summary: Cron job running glue-validator every hour and storing the result in a log file
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/glue-validator-cron/tags/R_1_2_0 %{name}-%{version}
#  tar -czvf %{name}-%{version}.src.tgz %{name}-%{version}
Source: %{name}-%{version}.src.tgz
License: ASL 2.0
Group: Development/Tools
BuildRoot: %{_tmppath}/%{name}-%{version}-build
BuildArch: noarch
Requires: glue-validator
Url: http://gridinfo.web.cern.ch/glue/glue-validator-guide

%description
Cron job running glue-validator every hour and storing the result in a log file 

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
%dir /var/log/glue-validator/
%dir /usr/share/doc/glue-validator-cron
/etc/cron.hourly/glue-validator-cron
%doc /usr/share/doc/glue-validator-cron/README


%changelog
* Fri May 31 2013 Maria Alandes <maria.alandes.pradillo@cern.ch>  - 1.2.0-1
- Fixed command line options after glue-validator changes to be Nagios compliant
- Added command to validate against EGI GLUE 2.0 profile

* Tue Sep 11 2012 Maria Alandes <maria.alandes.pradillo@cern.ch>  - 1.0.2-1
- rpmlint : Fixed length of summary and description in the spec file.
- rpmlint : Created a README file.
- rpmlint : Fixed permissions of the cron job.

* Fri Jul 20 2012 Maria Alandes <maria.alandes.pradillo@cern.ch>  - 1.0.1-1
- Fixes after testing: remove post action from spec file and redirect sdterr and stdout to log file

* Tue Jul 16 2012 Maria Alandes <maria.alandes.pradillo@cern.ch>  - 1.0.0-1
- Initial Release
