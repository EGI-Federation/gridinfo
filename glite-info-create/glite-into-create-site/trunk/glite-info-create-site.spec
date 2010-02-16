Name:           glite-info-create-site
Version:        0.1.0
Release:        1%{?dist}
Summary:        Site components for the glite-info-create framework.
Group:          Development/Tools
License:        Apache Software License 2
URL:            http://svnweb.cern.ch/guest/gridinfo/%{name}
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Source:         %{name}-%{version}.src.tgz
Requires:       glite-info-create-core

%description
Site components for the glite-info-create framework.

%prep
%setup -q -c

%build 

%install
rm -rf %{buildroot}
make prefix=%{buildroot} install 


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(0644,root,root) /etc/glite-info-create/site
%attr(0644,root,root) %config(noreplace) /etc/glite-info-create/site.1.cfg

%changelog
* Mon Feb 15 2010 Laurence Field <laurence.field@cern.ch> - 0.1.0-1
- First release

