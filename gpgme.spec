# TODO: package lisp files:
#    /usr/share/common-lisp/source/gpgme/gpgme-package.lisp
#    /usr/share/common-lisp/source/gpgme/gpgme.asd
#    /usr/share/common-lisp/source/gpgme/gpgme.lisp
#
# Conditional build:
%bcond_without	gpgsm		# with gnupg S/MIME support
%bcond_without	pth		# without pth-based version of library
%bcond_without	static_libs	# do not build static libraries
%bcond_with	tests		# perform tests
#
# TODO: separate pth version? disable by default (if !needed at all)?
Summary:	Library for accessing GnuPG
Summary(pl.UTF-8):	Biblioteka dająca dostęp do funkcji GnuPG
Name:		gpgme
Version:	1.3.1
Release:	2
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Source0-md5:	90afa8436ce2b2683c001c824bd22601
Patch0:		%{name}-info.patch
Patch1:		%{name}-kill-tests.patch
Patch2:		%{name}-1.2.0-largefile.patch
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	libassuan-devel >= 1:2.0.2
BuildRequires:	libgpg-error-devel >= 1.8
BuildRequires:	libtool >= 2:2.2.6
%{?with_pth:BuildRequires:	pth-devel >= 1.2.0}
BuildRequires:	texinfo
BuildConflicts:	gnupg < 1.3.0
%{!?with_gpgsm:Requires:	gnupg >= 1.4.0}
%{?with_gpgsm:Requires:	gnupg-smime >= 1.9.8}
%{?with_gpgsm:Requires:	gnupg2 >= 2.0.4}
Requires:	libassuan >= 1:2.0.2
Requires:	libgpg-error >= 1.8
Obsoletes:	cryptplug
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
Requires:	libassuan-devel >= 1:2.0.2
Requires:	libgpg-error-devel >= 1.8

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

%prep
%setup -q
%patch0 -p1
%{!?with_tests:%patch1 -p1}
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static} \
	%{?with_gpgsm:--with-gpgsm=/usr/bin/gpgsm} \
	%{!?with_gpgsm:--without-gpgsm} \
	%{!?with_pth:--without-pth} \
	--with-gpg=/usr/bin/gpg%{?with_gpgsm:2}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%doc README ChangeLog THANKS TODO NEWS AUTHORS
%attr(755,root,root) %{_libdir}/libgpgme.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgme.so.11
%attr(755,root,root) %{_libdir}/libgpgme-pth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgme-pth.so.11
%attr(755,root,root) %{_libdir}/libgpgme-pthread.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgme-pthread.so.11

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gpgme-config
%attr(755,root,root) %{_libdir}/libgpgme.so
%attr(755,root,root) %{_libdir}/libgpgme-pth.so
%attr(755,root,root) %{_libdir}/libgpgme-pthread.so
%{_libdir}/libgpgme.la
%{_libdir}/libgpgme-pth.la
%{_libdir}/libgpgme-pthread.la
%{_includedir}/gpgme.h
%{_aclocaldir}/gpgme.m4
%{_infodir}/gpgme.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgpgme.a
%{_libdir}/libgpgme-pth.a
%{_libdir}/libgpgme-pthread.a
%endif
