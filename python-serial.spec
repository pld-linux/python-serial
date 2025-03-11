#
# Conditional build:
%bcond_without	doc		# Sphinx documentation
%bcond_with	tests		# unit tests (test_pty.Test_Pty_Serial_Open tests require ptys)
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module

%define		module	serial
Summary:	Serial port interface module
Summary(pl.UTF-8):	Moduł interfejsu do portu szeregowego
Name:		python-serial
Version:	3.5
Release:	3
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://github.com/pyserial/pyserial/releases
Source0:	https://github.com/pyserial/pyserial/archive/v%{version}/pyserial-%{version}.tar.gz
# Source0-md5:	ce1cf20f1bbf608027b14d4a97a377fc
URL:		https://pypi.org/project/pyserial/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	rpm-pythonprov
Requires:	python-modules >= 1:2.7
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

%package -n python3-%{module}
Summary:	Serial port interface module
Summary(pl.UTF-8):	Moduł interfejsu do portu szeregowego
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-%{module}
This module encapsulates the access for the serial port. It provides
backends for Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automatically
selects the appropriate backend.

%description -n python3-%{module} -l pl.UTF-8
Ten moduł opakowuje dostęp do portu szeregowego. Dostarcza backendy
dla Pythona działającego na Windows, Linuksie, BSD (być może dowolnym
systemie zgodnym z POSIX) oraz Jythona. Moduł o nazwie "serial"
automatycznie wybiera właściwy backend.

%package apidocs
Summary:	API documentation for Python serial module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona serial
Group:		Documentation

%description apidocs
API documentation for Python serial module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona serial.

%package -n miniterm
Summary:	Very simple serial terminal
Summary(pl.UTF-8):	Bardzo prosty terminal szeregowy
Group:		Applications/Communications
Requires:	python%{?with_python3:3}-%{module} = %{version}-%{release}

%description -n miniterm
Very simple serial terminal written in Python.

%description -n miniterm -l pl.UTF-8
Bardzo prosty terminal szeregowy napisany w Pythonie.

%prep
%setup  -q -n pyserial-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -s test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s test
%endif
%endif

%if %{with doc}
%{__make} -C documentation html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}/*.py

# remove .NET (IronPython), Jython, Win32 specific code
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/serial/{serialcli,serialjava,serialwin32,win32}.py*
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/serial/tools/list_ports_{osx,windows}.py*

%py_postclean
%endif

%if %{with python3}
# prefer python3 version
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pyserial-miniterm
%{__rm} $RPM_BUILD_ROOT%{_bindir}/pyserial-ports

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__sed} -i -e '1s,/usr/bin/env python,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*.py

# remove .NET (IronPython), Jython, Win32 specific code
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/serial/{serialcli,serialjava,serialwin32,win32}.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/serial/tools/list_ports_{osx,windows}.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/serial/__pycache__/{serialcli,serialjava,serialwin32,win32}.*.py*
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/serial/tools/__pycache__/list_ports_{osx,windows}.*.py*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%{py_sitescriptdir}/serial
%{py_sitescriptdir}/pyserial-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/serial
%{py3_sitescriptdir}/pyserial-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc documentation/_build/html/{_static,*.html,*.js}
%endif

%files -n miniterm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pyserial-miniterm
%attr(755,root,root) %{_bindir}/pyserial-ports
