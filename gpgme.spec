#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	commonlisp	# Common Lisp interface
%bcond_without	tests		# perform tests
#
Summary:	Library for accessing GnuPG
Summary(pl.UTF-8):	Biblioteka dająca dostęp do funkcji GnuPG
Name:		gpgme
Version:	2.0.0
Release:	1
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.gnupg.org/ftp/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Source0-md5:	60f6871b948060572c7d952e39b42bd8
Patch0:		%{name}-info.patch
Patch1:		orig-version.patch
Patch2:		%{name}-largefile.patch
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
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	texinfo
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

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PACKAGE_VERSION=%{version} \
%if %{without tests}
	--disable-g13-test \
	--disable-gpg-test \
	--disable-gpgconf-test \
	--disable-gpgsm-test \
%endif
	--enable-languages="%{?with_commonlisp:cl}" \
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS THANKS TODO
%attr(755,root,root) %{_bindir}/gpgme-json
%attr(755,root,root) %{_bindir}/gpgme-tool
%attr(755,root,root) %{_libdir}/libgpgme.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgme.so.45
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

%if %{with commonlisp}
%files -n common-lisp-gpgme
%defattr(644,root,root,755)
%doc lang/cl/README
%{_datadir}/common-lisp/source/gpgme
%endif
