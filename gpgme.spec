Summary:	Library for accessing GnuPG
Summary(pl):	Biblioteka daj±ca dostep do funkcji GnuPG
Name:		gpgme
Version:	0.3.16
Release:	3
Epoch:		1
License:	GPL v2
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.gz
# Source0-md5:	0476b219695ea25cb2a97b18b717e381
Patch0:		%{name}-info.patch
Patch1:		%{name}-ac_quotation_fix.patch
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libgpg-error-devel
BuildRequires:	libtool
BuildRequires:	texinfo
Requires:	gnupg >= 1.2.0
Obsoletes:	cryptplug
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for accessing GnuPG.

%description -l pl
Biblioteka daj±ca dostêp do funkcji GnuPG.

%package devel
Summary:	Header files for %{name}
Summary(pl):	Pliki nag³ówkowe dla %{name}
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgpg-error-devel

%description devel
Header files for %{name}, needed for compiling programs using %{name}.

%description devel -l pl
Pliki nag³ówkowe dla %{name}, potrzebne do kompilacji programów
u¿ywaj±cych %{name}.

%package static
Summary:	Static version of %{name} library
Summary(pl):	Statyczna wersja biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static version of %{name} library.

%description static -l pl
Statyczna wersja biblioteki %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--without-gpgsm

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_libdir}/*.so.*.*

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
