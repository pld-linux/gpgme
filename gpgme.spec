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
Version:	1.1.7
Release:	1
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Source0-md5:	0f9347890339d491241fbdb8812673ff
Patch0:		%{name}-info.patch
Patch1:		%{name}-gpg2.patch
Patch2:		%{name}-kill-tests.patch
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.10
BuildRequires:	libgpg-error-devel >= 1.4
BuildRequires:	libtool
%{?with_pth:BuildRequires:	pth-devel >= 1.2.0}
BuildRequires:	texinfo
BuildConflicts:	gnupg < 1.3.0
%{!?with_gpgsm:Requires:	gnupg >= 1.3.0}
%{?with_gpgsm:Requires:	gnupg2 >= 2.0.4}
%{?with_gpgsm:Requires:	gnupg-smime >= 1.9.8}
Requires:	libgpg-error >= 1.4
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
Requires:	libgpg-error-devel >= 1.4

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
%{?with_gpgsm:%patch1 -p1}
%{!?with_tests:%patch2 -p1}

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static} \
	%{?with_gpgsm:--with-gpgsm=%{_bindir}/gpgsm} \
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

%post devel	-p	/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun devel	-p	/sbin/postshell
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
