Summary:	Library for accessing GnuPG
Summary(pl):	Biblioteka daj±ca dostep do funkcji GnuPG
Name:		gpgme
Version:	0.3.5
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/alpha/gpgme/%{name}-%{version}.tar.gz
URL:		http://www.gnupg.org/gpgme.html
Requires:	gnupg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for accessing GnuPG.

%description -l pl
Biblioteka daj±ca dostep do funkcji GnuPG.

%package devel
Summary:	Header files for %{name}
Summary(pl):	Pliki nag³ównkowe dla %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for %{name}, needed for compiling programs using %{name}.

%description devel -l pl
Pliki nag³ównkowe dla %{name} potrzebne do kompilacji programów
u¿ywaj±cych %{name}.

%package static
Summary:	Static version of %{name} library
Summary:	Statyczna wersja biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of %{name} library.

%description static -l pl
Statyczna wersja biblioteki %{name}.

%prep
%setup -q

%build
%configure \
	--without-gpgsm

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README ChangeLog THANKS TODO NEWS AUTHORS

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gpgme-config
%{_includedir}/*
%{_libdir}/*.so
%{_aclocaldir}/%{name}.m4
%{_infodir}/*.info*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
