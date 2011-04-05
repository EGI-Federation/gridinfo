Name:		bdii-config-site
Version:	1.0.2
Release:	1%{?dist}
Summary:	Site BDII configration files
Group:		System/Monitoring
License:	ASL 2.0
Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	bdii
Requires:	glite-info-provider-release
Requires:	glite-info-provider-ldap
Requires:	glite-info-provider-service
Requires:	glite-info-static
Requires:	glite-info-site

%description
Configration files for the Site BDII.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf %{buildroot}
make install prefix=%{buildroot}

%post
if [ ! -f /opt/glite/etc/gip/provider/glite-info-provider-release ]; then 
    if [ -f /opt/glite/libexec/glite-info-provider-release ]; then 
        ln -s /opt/glite/libexec/glite-info-provider-release /var/lib/bdii/gip/provider/glite-info-provider-release
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)

/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-site
/var/lib/bdii/gip/provider/glite-info-provider-site
/etc/bdii/gip/site-urls.conf
/var/lib/bdii/gip/provider/glite-info-provider-service-bdii-site-glue2
/var/lib/bdii/gip/provider/glite-info-provider-site-entry
/var/lib/bdii/gip/provider/glite-info-provider-site-entry-glue2
/var/lib/bdii/gip/provider/glite-info-provider-site-glue2

%changelog
* Tue Apr 05 2011 Laurence Field <laurence.field@cern.ch> - 1.0.2-1
- Fixed error due to new version of glite-info-provider-service
* Mon Mar 21 2011 Laurence Field <laurence.field@cern.ch> - 1.0.1-1
- Changed config location to /etc/bdii/gip
* Tue Mar 15 2011 Laurence Field <laurence.field@cern.ch> - 1.0.0-1
- Fixed Is-148
* Mon Sep 06 2010 Laurence Field <laurence.field@cern.ch> - 0.9.0-1
- Fixed Is-148
* Thu May 20 2010 Laurence Field <laurence.field@cern.ch> - 0.7.0-1
- Changed to /opt/glite/etc
* Wed Apr 07 2010 Laurence Field <laurence.field@cern.ch> - 0.4.0-1
- New package
