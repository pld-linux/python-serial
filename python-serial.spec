#TODO:
# - add descriptions, all kind of cosmetics, subpackage examples, docs


%define	module	serial

Summary:	Serial port interface module
Summary(pl):	Modu³ interfejsu do portu szeregowego
Name:		python-serial
Version:	2.0
Release:	0.1
License:	GPL
Group:		Development/Languages/Python
Source0:	http://dl.sourceforge.net/pyserial/pyserial-%{version}.zip
# Source0-md5:	80a26774156ba38b63b0945f2b511695
URL:		http://pyserial.sf.net
%pyrequires_eq	python
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov >= 4.0.2-50
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module encapsulates the access for the serial port. It provides
backends for Python running on Windows, Linux, BSD (possibly any POSIX
compilant system) and Jython. The module named "serial" automatically
selects the appropriate backend.

%description -l pl
Ten modu³ opakowuje dostêp do portu szeregowego. Dostarcza backendy
dla Pythona dzia³aj±cego na Windows, Linuksie, BSD (byæ mo¿e dowolnym
systemie zgodnym z POSIX) oraz Jythona. Modu³ o nazwie "serial"
automatycznie wybiera w³a¶ciwy backend.

%prep
%setup  -q -n pyserial-%{version}

%build
python ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python ./setup.py install \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/__init__.pyc
%{py_sitedir}/%{module}/__init__.pyo
%{py_sitedir}/%{module}/serialposix.pyc
%{py_sitedir}/%{module}/serialposix.pyo
%{py_sitedir}/%{module}/serialutil.pyc
%{py_sitedir}/%{module}/serialutil.pyo
