#
# Conditional build:
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module

%define		module	serial
Summary:	Serial port interface module
Summary(pl.UTF-8):	Moduł interfejsu do portu szeregowego
Name:		python-serial
Version:	3.3
Release:	2
License:	GPL
Group:		Development/Languages/Python
Source0:	https://github.com/pyserial/pyserial/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	af48f8f9b338c187f791d2f560f8b230
URL:		http://pyserial.wiki.sourceforge.net/pySerial
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-modules
Requires:	python
%endif
%if %{with python3}
BuildRequires:	python3-2to3
BuildRequires:	python3-devel
BuildRequires:	python3-modules
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module encapsulates the access for the serial port. It provides
backends for Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automatically
selects the appropriate backend.

%description -l pl.UTF-8
Ten moduł opakowuje dostęp do portu szeregowego. Dostarcza backendy
dla Pythona działającego na Windows, Linuksie, BSD (być może dowolnym
systemie zgodnym z POSIX) oraz Jythona. Moduł o nazwie "serial"
automatycznie wybiera właściwy backend.

%package -n	python3-%{module}
Summary:	Serial port interface module
Group:		Libraries/Python
Requires:	python3

%description -n python3-%{module}
This module encapsulates the access for the serial port. It provides
backends for Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automatically
selects the appropriate backend.

%package -n miniterm
Summary:	Very simple serial terminal
Group:		Applications/Communications
Requires:	python%{?with_python3:3}-%{module} = %{version}-%{release}

%description -n miniterm
Very simple serial terminal written in Python.

%prep
%setup  -q -n pyserial-%{version}

%build
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%py_install

cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{py_sitescriptdir} -name "*serialjava*" -exec rm {} \;
find $RPM_BUILD_ROOT%{py_sitescriptdir} -name "*serialwin*" -exec rm {} \;
%endif

%if %{with python3}
# Always prefer python3 version
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/miniterm.py

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%py3_install

cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{py3_sitescriptdir} -name "*serialjava*" -exec rm {} \;
find $RPM_BUILD_ROOT%{py3_sitescriptdir} -name "*serialwin*" -exec rm {} \;
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/*egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/*egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%files -n miniterm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/miniterm.py
