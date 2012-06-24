%define		realname	pcre
Summary:	Perl-Compatible Regular Expression library - Mingw32 cross version
Summary(pl):	Biblioteka perlowych wyra�e� regularnych - wersja skro�na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	6.5
Release:	1
License:	BSD (see LICENCE)
Group:		Libraries
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{realname}-%{version}.tar.bz2
# Source0-md5:	1bd00f173438cbef8b957e3e1711f737
URL:		http://www.pcre.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-w32api
BuildRequires:	libtool
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
PCRE stands for the Perl Compatible Regular Expression library. It
contains routines to match text against regular expressions similar to
Perl's. It also contains a POSIX compatibility library.

%description -l pl
PCRE (Perl-Compatible Regular Expression) oznacza bibliotek� wyra�e�
regularnych kompatybilnych z perlowymi. Zawiera funkcje dopasowuj�ce
tekst do wyra�e� regularnych podobnych do tych znanych z Perla.
Zawiera tak�e bibliotek� kompatybiln� z POSIX.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--host=%{_host} \
	--target=%{target} \
	--enable-utf8 \
	--disable-shared

# we want host binary to generate some tables, not win32 binary
cc -c %{rpmcflags} -I. dftables.c
cc %{rpmcflags} -I. -I. -o dftables dftables.o

# override EXEEXT to use host binaries
%{__make} winshared \
	EXEEXT=

%if 0%{!?debug:1}
%{target}-strip .libs/*.dll
%{target}-strip -g -R.comment -R.note .libs/*.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install pcre.h pcreposix.h pcrecpp.h pcre_scanner.h pcre_stringpiece.h \
	$RPM_BUILD_ROOT%{arch}/include
install .libs/libpcre{,posix,cpp}.a $RPM_BUILD_ROOT%{arch}/lib
install .libs/{libpcre,pcreposix,pcrecpp}.dll.a $RPM_BUILD_ROOT%{arch}/lib
install .libs/pcre{,posix,cpp}.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
