#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	commonlisp	# Common Lisp interface
%bcond_without	cxx		# C++ interface (GpgMEpp library)
%bcond_without	qt5		# Qt 5 interface (QGpgME library), requires cxx
%bcond_without	qt6		# Qt 6 interface (QGpgME library), requires cxx
%bcond_without	python		# Python interfaces (PyME, both python2+python3)
%bcond_without	python2		# Python 2 interface (PyME)
%bcond_without	python3		# Python 3 interface (PyME)
%bcond_without	tests		# perform tests
%bcond_without	docs		# Qt binding docs (disable for bootstrap: loop through graphviz)
#
%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
%if %{without cxx}
%undefine	with_qt5
%undefine	with_qt6
%endif
Summary:	Library for accessing GnuPG
Summary(pl.UTF-8):	Biblioteka dająca dostęp do funkcji GnuPG
Name:		gpgme
Version:	1.24.3
Release:	1
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.gnupg.org/ftp/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Source0-md5:	c6f85ce24ad46c9469596df0301f32eb
Patch0:		%{name}-info.patch
Patch1:		orig-version.patch
Patch2:		%{name}-largefile.patch
Patch3:		%{name}-python.patch
Patch4:		no_docs.patch
URL:		https://www.gnupg.org/related_software/gpgme/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.14
%if %{with tests}
BuildRequires:	gnupg2
BuildRequires:	gnupg-agent
BuildRequires:	gnupg-smime
%endif
BuildRequires:	libassuan-devel >= 1:2.4.2
BuildRequires:	libgpg-error-devel >= 1.47
%{?with_cxx:BuildRequires:	libstdc++-devel >= 6:5}
%{?with_qt6:BuildRequires:	libstdc++-devel >= 6:7}
BuildRequires:	libtool >= 2:2.2.6
%{?with_python2:BuildRequires:	python-devel >= 1:2.7}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.6}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_python:BuildRequires:	swig-python}
BuildRequires:	texinfo
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5.0.0
%{?with_tests:BuildRequires:	Qt5Test-devel >= 5.8.0}
%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRequires:	qt5-build >= 5.0.0
%endif
%if %{with qt6}
BuildRequires:	Qt6Core-devel >= 6.4.0
%{?with_tests:BuildRequires:	Qt6Test-devel >= 6.4.0}
%if %{with docs}
BuildRequires:	doxygen
BuildRequires:	graphviz
%endif
BuildRequires:	qt6-build >= 6.4.0
%endif
BuildConflicts:	gnupg < 1.3.0
Suggests:	gnupg >= 1.4.0
Suggests:	gnupg-smime >= 1.9.8
Suggests:	gnupg2 >= 2.0.4
Requires:	libassuan >= 1:2.4.2
Requires:	libgpg-error >= 1.47
Obsoletes:	cryptplug < 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for accessing GnuPG.

%description -l pl.UTF-8
Biblioteka dająca dostęp do funkcji GnuPG.

%package devel
Summary:	Header files for GPGME library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GPGME
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libassuan-devel >= 1:2.4.2
Requires:	libgpg-error-devel >= 1.47

%description devel
Header files for GPGME library, needed for compiling programs using
GPGME.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GPGME, potrzebne do kompilacji programów
używających GPGME.

%package static
Summary:	Static version of GPGME library
Summary(pl.UTF-8):	Statyczna wersja biblioteki GPGME
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static version of GPGME library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki GPGME.

%package c++
Summary:	GpgMEpp - C++ interface for GPGME library
Summary(pl.UTF-8):	GpgMEpp - interfejs C++ do biblioteki GPGME
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description c++
GpgMEpp is a C++ wrapper (or C++ bindings) for the GnuPG project's
gpgme (GnuPG Made Easy). It's based on KF5gpgmepp library.

%description c++ -l pl.UTF-8
GpgMEpp to interfejs C++ (wiązania C++) do biblioteki gpgme (GnuPG
Made Easy) z projektu GnuPG. Jest oparty na bibliotece KF5gpgme.pp.

%package c++-devel
Summary:	Header files for GpgMEpp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GpgMEpp
Group:		Development/Libraries
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel >= 6:4.7
Conflicts:	kde4-kdepimlibs-devel

%description c++-devel
Header files for GpgMEpp library.

%description c++-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GpgMEpp.

%package c++-static
Summary:	Static GpgMEpp library
Summary(pl.UTF-8):	Statyczna biblioteka GpgMEpp
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{epoch}:%{version}-%{release}

%description c++-static
Static GpgMEpp library.

%description c++-static -l pl.UTF-8
Statyczna biblioteka GpgMEpp.

%package qt5
Summary:	QGpgME - Qt 5 interface for GPGME library
Summary(pl.UTF-8):	QGpgME - interfejs Qt 5 do biblioteki GPGME
License:	GPL v2+ with Qt linking exception
Group:		Libraries
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	Qt5Core >= 5.0.0

%description qt5
QGpgME is Qt 5 interface for GPGME library, based on library from
KF5gpgmepp. QGpgME provides a very high level Qt API around GpgMEpp.

%description qt5 -l pl.UTF-8
QGpgME to interfejs Qt 5 do biblioteki GPGME, oparty na bibliotece z
KF5gpgmepp. QGpgME udostępnia API Qt do GpgMEpp bardzo wysokiego
poziomu.

%package qt5-devel
Summary:	Header files for QGpgME library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki QGpgME
License:	GPL v2+ with Qt linking exception
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-qt5 = %{epoch}:%{version}-%{release}
Requires:	Qt5Core-devel >= 5.0.0
Conflicts:	kde4-kdepimlibs-devel

%description qt5-devel
Header files for QGpgME library.

%description qt5-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki QGpgME.

%package qt5-static
Summary:	Static QGpgME library
Summary(pl.UTF-8):	Statyczna biblioteka QGpgME
License:	GPL v2+ with Qt linking exception
Group:		Development/Libraries
Requires:	%{name}-qt5-devel = %{epoch}:%{version}-%{release}

%description qt5-static
Static QGpgME library.

%description qt5-static -l pl.UTF-8
Statyczna biblioteka QGpgME.

%package qt6
Summary:	QGpgME - Qt 6 interface for GPGME library
Summary(pl.UTF-8):	QGpgME - interfejs Qt 6 do biblioteki GPGME
License:	GPL v2+ with Qt linking exception
Group:		Libraries
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	Qt6Core >= 6.4.0

%description qt6
QGpgME is Qt 6 interface for GPGME library, based on library from
KF5gpgmepp. QGpgME provides a very high level Qt API around GpgMEpp.

%description qt6 -l pl.UTF-8
QGpgME to interfejs Qt 6 do biblioteki GPGME, oparty na bibliotece z
KF5gpgmepp. QGpgME udostępnia API Qt do GpgMEpp bardzo wysokiego
poziomu.

%package qt6-devel
Summary:	Header files for QGpgME library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki QGpgME
License:	GPL v2+ with Qt linking exception
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{epoch}:%{version}-%{release}
Requires:	%{name}-qt6 = %{epoch}:%{version}-%{release}
Requires:	Qt6Core-devel >= 6.4.0
Conflicts:	kde4-kdepimlibs-devel

%description qt6-devel
Header files for QGpgME library.

%description qt6-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki QGpgME.

%package qt6-static
Summary:	Static QGpgME library
Summary(pl.UTF-8):	Statyczna biblioteka QGpgME
License:	GPL v2+ with Qt linking exception
Group:		Development/Libraries
Requires:	%{name}-qt6-devel = %{epoch}:%{version}-%{release}

%description qt6-static
Static QGpgME library.

%description qt6-static -l pl.UTF-8
Statyczna biblioteka QGpgME.

%package -n common-lisp-gpgme
Summary:	Common Lisp binding for GPGME library
Summary(pl.UTF-8):	Wiązanie Common Lispa do biblioteki GPGME
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	common-lisp-controller

%description -n common-lisp-gpgme
Common Lisp binding for GPGME library.

%description -n common-lisp-gpgme -l pl.UTF-8
Wiązanie Common Lispa do biblioteki GPGME.

%package -n python-gpg
Summary:	PyME - Python 2 interface for GPGME library
Summary(pl.UTF-8):	PyME - interfejs Pythona 2 do biblioteki GPGME
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python-libs >= 1:2.7
Obsoletes:	python-pyme < 1.8.0

%description -n python-gpg
PyME is a Python interface for GPGME library.

%description -n python-gpg -l pl.UTF-8
PyME to interfejs Pythona do biblioteki GPGME.

%package -n python3-gpg
Summary:	PyME - Python 3 interface for GPGME library
Summary(pl.UTF-8):	PyME - interfejs Pythona 3 do biblioteki GPGME
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	python3-libs >= 1:3.6
Obsoletes:	python3-pyme < 1.8.0

%description -n python3-gpg
PyME is a Python interface for GPGME library.

%description -n python3-gpg -l pl.UTF-8
PyME to interfejs Pythona do biblioteki GPGME.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%{!?with_docs:%patch -P4 -p1}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# in enable-languages:
# "python" means all installed python version (if any)
%configure \
	PACKAGE_VERSION=%{version} \
%if %{without tests}
	--disable-g13-test \
	--disable-gpg-test \
	--disable-gpgconf-test \
	--disable-gpgsm-test \
%endif
	--enable-languages="%{?with_commonlisp:cl} %{?with_cxx:cpp} %{?with_python:python} %{?with_qt5:qt5} %{?with_qt6:qt6}" \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Win32 specific
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/gpgme-glib.pc

# obsoleted by pkg-config/cmake configs
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %{with python2}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	c++ -p /sbin/ldconfig
%postun	c++ -p /sbin/ldconfig

%post	qt5 -p /sbin/ldconfig
%postun	qt5 -p /sbin/ldconfig

%post	qt6 -p /sbin/ldconfig
%postun	qt6 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS THANKS TODO
%attr(755,root,root) %{_bindir}/gpgme-json
%attr(755,root,root) %{_bindir}/gpgme-tool
%attr(755,root,root) %{_libdir}/libgpgme.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgme.so.11
%{_mandir}/man1/gpgme-json.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpgme.so
%{_includedir}/gpgme.h
%{_pkgconfigdir}/gpgme.pc
%{_aclocaldir}/gpgme.m4
%{_infodir}/gpgme.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgpgme.a
%endif

%if %{with cxx}
%files c++
%defattr(644,root,root,755)
%doc lang/cpp/README
%attr(755,root,root) %{_libdir}/libgpgmepp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgmepp.so.6

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpgmepp.so
%{_includedir}/gpgme++
%{_libdir}/cmake/Gpgmepp
%{_pkgconfigdir}/gpgmepp.pc

%if %{with static_libs}
%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libgpgmepp.a
%endif

%if %{with qt5}
%files qt5
%defattr(644,root,root,755)
%doc lang/qt/README
%attr(755,root,root) %{_libdir}/libqgpgme.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqgpgme.so.15

%files qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqgpgme.so
%{_includedir}/qgpgme-qt5
%{_libdir}/cmake/QGpgme

%if %{with static_libs}
%files qt5-static
%defattr(644,root,root,755)
%{_libdir}/libqgpgme.a
%endif
%endif

%if %{with qt6}
%files qt6
%defattr(644,root,root,755)
%doc lang/qt/README
%attr(755,root,root) %{_libdir}/libqgpgmeqt6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqgpgmeqt6.so.15

%files qt6-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqgpgmeqt6.so
%{_includedir}/qgpgme-qt6
%{_libdir}/cmake/QGpgmeQt6

%if %{with static_libs}
%files qt6-static
%defattr(644,root,root,755)
%{_libdir}/libqgpgmeqt6.a
%endif
%endif
%endif

%if %{with commonlisp}
%files -n common-lisp-gpgme
%defattr(644,root,root,755)
%doc lang/cl/README
%{_datadir}/common-lisp/source/gpgme
%endif

%if %{with python2}
%files -n python-gpg
%defattr(644,root,root,755)
%doc lang/python/README
%dir %{py_sitedir}/gpg
%attr(755,root,root) %{py_sitedir}/gpg/_gpgme.so
%{py_sitedir}/gpg/*.py[co]
%{py_sitedir}/gpg/constants
%{py_sitedir}/gpg-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-gpg
%defattr(644,root,root,755)
%doc lang/python/README
%dir %{py3_sitedir}/gpg
%attr(755,root,root) %{py3_sitedir}/gpg/_gpgme.cpython-*.so
%{py3_sitedir}/gpg/*.py
%{py3_sitedir}/gpg/__pycache__
%{py3_sitedir}/gpg/constants
%{py3_sitedir}/gpg-%{version}-py*.egg-info
%endif
