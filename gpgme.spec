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
Version:	1.1.5
Release:	2
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Source0-md5:	db7d7dfc10edcc20e8a15a7a8fdc1080
Patch0:		%{name}-info.patch
Patch1:		%{name}-gpg2.patch
Patch2:		%{name}-kill-tests.patch
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9.3
BuildRequires:	libgpg-error-devel >= 1.4
BuildRequires:	libtool
%{?with_pth:BuildRequires:	pth-devel >= 1.2.0}
BuildRequires:	texinfo
BuildConflicts:	gnupg < 1.3.0
%{!?with_gpgsm:Requires:	gnupg >= 1.3.0}
%{?with_gpgsm:Requires:	gnupg2 >= 2.0.3}
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

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc README ChangeLog THANKS TODO NEWS AUTHORS
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gpgme-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_aclocaldir}/*.m4
%{_infodir}/*.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
