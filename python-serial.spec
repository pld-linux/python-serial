#
# Conditional build:
%bcond_without	python2		# Python 2.x module
%bcond_without	python3		# Python 3.x module

%define 	module	serial
Summary:	Serial port interface module
Summary(pl.UTF-8):	Moduł interfejsu do portu szeregowego
Name:		python-serial
Version:	2.7
Release:	3
License:	GPL
Group:		Development/Languages/Python
Source0:	http://pypi.python.org/packages/source/p/pyserial/pyserial-%{version}.tar.gz
# Source0-md5:	794506184df83ef2290de0d18803dd11
URL:		http://pyserial.wiki.sourceforge.net/pySerial
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
%{__python} setup.py build --build-base py2
%endif
%if %{with python3}
%{__python3} setup.py build --build-base py3
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%{__python} setup.py build \
	--build-base py2 \
	install \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{py_sitescriptdir} -name "*serialjava*" -exec rm {} \;
find $RPM_BUILD_ROOT%{py_sitescriptdir} -name "*serialwin*" -exec rm {} \;
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__python3} setup.py build \
	--build-base py3 \
	install \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT
cp -p examples/*.py $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{py3_sitescriptdir} -name "*serialjava*" -exec rm {} \;
find $RPM_BUILD_ROOT%{py3_sitescriptdir} -name "*serialwin*" -exec rm {} \;
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/*egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.txt
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/*egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%files -n miniterm
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/miniterm.py
