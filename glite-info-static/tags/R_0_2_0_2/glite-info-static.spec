Name:		glite-info-static
Version:	0.2.0
Release:	2%{?dist}
Summary:	Core component for the glite-info-static framework.
Group:		System/Monitoring
License:	ASL 2.0
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export http://svnweb.cern.ch/guest/gridinfo/glite-info-static/tags/R_0_2_0_2 %{name}-%{version}
#  tar --gzip -czvf %{name}-%{version}.tar.gz %{name}-%{version} 
Source:		%{name}-%{version}.src.tgz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Core component for the glite-info-static framework.

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
%attr(0755,root,root) /usr/sbin/glite-info-static
%doc /usr/share/doc/%{name}-%{version}/README.txt

%changelog
* Wed Apr 24 2013 Maria Alandes <maria.alandes.pradillo@cern.ch> - 0.2.0-2
- Added Source URL information

* Thu Apr 8 2010 Laurence Field <laurence.field@cern.ch> - 0.2.0-1
- Refactored
* Mon Feb 15 2010 Laurence Field <laurence.field@cern.ch> - 0.1.0-1
- First release
