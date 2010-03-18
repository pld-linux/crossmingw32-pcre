%define		realname	pcre
Summary:	Perl-Compatible Regular Expression library - Mingw32 cross version
Summary(pl.UTF-8):	Biblioteka perlowych wyrażeń regularnych - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	8.01
Release:	1
License:	BSD (see LICENCE)
Group:		Development/Libraries
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{realname}-%{version}.tar.bz2
# Source0-md5:	413be1c23dabe91f637fb3770f640006
URL:		http://www.pcre.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32

%define		_prefix		/usr/%{target}
%define		_libdir		%{_prefix}/lib
%define		_pkgconfigdir	%{_prefix}/lib/pkgconfig
%define		_dlldir		/usr/share/wine/windows/system

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
PCRE stands for the Perl Compatible Regular Expression library. It
contains routines to match text against regular expressions similar to
Perl's. It also contains a POSIX compatibility library.

%description -l pl.UTF-8
PCRE (Perl-Compatible Regular Expression) oznacza bibliotekę wyrażeń
regularnych kompatybilnych z perlowymi. Zawiera funkcje dopasowujące
tekst do wyrażeń regularnych podobnych do tych znanych z Perla.
Zawiera także bibliotekę kompatybilną z POSIX.

%package static
Summary:	Static PCRE libraries (cross mingw32 version)
Summary(pl.UTF-8):	Statyczne biblioteki PCRE (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static PCRE libraries (cross mingw32 version).

%description static -l pl.UTF-8
Statyczne biblioteki PCRE (wersja skrośna mingw32).

%package dll
Summary:	%{realname} - DLL libraries for Windows
Summary(pl.UTF-8):	%{realname} - biblioteki DLL dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
%{realname} - DLL libraries for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteki DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--host=%{target} \
	--target=%{target} \
	--enable-unicode-properties \
	--enable-utf8

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/{doc,man}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENCE NEWS NON-UNIX-USE README
%{_libdir}/libpcre.dll.a
%{_libdir}/libpcrecpp.dll.a
%{_libdir}/libpcreposix.dll.a
%{_libdir}/libpcre.la
%{_libdir}/libpcrecpp.la
%{_libdir}/libpcreposix.la
%{_includedir}/pcre*.h
%{_pkgconfigdir}/libpcre.pc
%{_pkgconfigdir}/libpcrecpp.pc
%{_pkgconfigdir}/libpcreposix.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpcre.a
%{_libdir}/libpcrecpp.a
%{_libdir}/libpcreposix.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpcre-*.dll
%{_dlldir}/libpcrecpp-*.dll
%{_dlldir}/libpcreposix-*.dll
