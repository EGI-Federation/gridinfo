Name:           glite-info-plugin-delayed-delete-status
Version:        1.0.1
Release:        1%{?dist}
Summary:        Updates GLUE state attributes of delayed delete entries in the Top BDII
Group:          Development/Libraries
License:        ASL 2.0
URL:            http://gridinfo.web.cern.ch
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/glite-info-plugin-delayed-delete-status/tags/R_1_0_1_1 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source:         %{name}-%{version}.src.tgz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Updates GLUE state attributes of delayed delete entries in the Top BDII

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%post
touch /var/log/glite/glite-info-plugin-delayed-delete-status.log
chmod 0644 /var/log/glite/glite-info-plugin-delayed-delete-status.log 
chown ldap:ldap /var/log/glite/glite-info-plugin-delayed-delete-status.log

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/libexec/glite-info-plugin-delayed-delete-status
%doc /usr/share/doc/glite-info-plugin-delayed-delete-status/README

%changelog

* Wed Sep 02 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.1-1
- Fixed wrong attribute name GlueCEStatus to GlueCEStateStatus

* Fri Aug 02 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 1.0.0-1
- Initial release


