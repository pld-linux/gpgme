#
# Conditional build:
%bcond_without	pth	# without pth-based version of library
#
# TODO: separate pth version? disable by default (if !needed at all)?
Summary:	Library for accessing GnuPG
Summary(pl):	Biblioteka daj±ca dostêp do funkcji GnuPG
Name:		gpgme
Version:	0.4.7
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/alpha/gpgme/%{name}-%{version}.tar.gz
# Source0-md5:	c43a50de6b1220d5a1b59b0deb142e14
Patch0:		%{name}-info.patch
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.7.6
BuildRequires:	libgpg-error-devel >= 0.5
BuildRequires:	libtool
%{?with_pth:BuildRequires:	pth-devel >= 1.2.0}
BuildRequires:	texinfo
BuildConflicts:	gnupg < 1.2.2
Requires:	gnupg >= 1.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for accessing GnuPG.

%description -l pl
Biblioteka daj±ca dostêp do funkcji GnuPG.

%package devel
Summary:	Header files for GPGME library
Summary(pl):	Pliki nag³ówkowe biblioteki GPGME
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libgpg-error-devel >= 0.5

%description devel
Header files for GPGME library, needed for compiling programs using
GPGME.

%description devel -l pl
Pliki nag³ówkowe biblioteki GPGME, potrzebne do kompilacji programów
u¿ywaj±cych GPGME.

%package static
Summary:	Static version of GPGME library
Summary(pl):	Statyczna wersja biblioteki GPGME
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of GPGME library.

%description static -l pl
Statyczna wersja biblioteki GPGME.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-shared \
	--enable-static \
	--without-gpgsm \
	%{!?with_pth:--without-pth}

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

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
