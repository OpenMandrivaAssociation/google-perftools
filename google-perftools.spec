%define	major 0
%define libname %mklibname google-perftools %{major}
%define develname %mklibname google-perftools -d

Summary:	Performance tools for C++
Name:		google-perftools
Version:	0.93
Release:	%mkrel 2
Group:		System/Libraries
License:	BSD
URL:		http://code.google.com/p/google-perftools/
Source0:	http://google-perftools.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	file
BuildRequires:	libtool
BuildRequires:	autoconf2.5
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
The google-perftools packages contains some utilities to improve and analyze
the performance of C++ programs.  This includes an optimized thread-caching
malloc() and cpu and heap profiling utilities.

%package -n	%{libname}
Summary:	Performance tools for C++ libraries
Group:          System/Libraries

%description -n	%{libname}
The google-perftools packages contains some utilities to improve and analyze
the performance of C++ programs.  This includes an optimized thread-caching
malloc() and cpu and heap profiling utilities.

%package -n	%{develname}
Summary:	Static library and header files for the google-perftools library
Group:		Development/C++
Provides:	%{name}-devel = %{version}
Provides:	%{libname}-devel = %{version}
Obsoletes:	%{libname}-devel
Requires:	%{libname} = %{version}

%description -n	%{develname}
The google-perftools packages contains some utilities to improve and analyze
the performance of C++ programs.  This includes an optimized thread-caching
malloc() and cpu and heap profiling utilities.

This package contains the static google-perftools library and its header files.

%prep

%setup -q

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type d -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done
    
# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
rm -f configure
libtoolize --force --copy; aclocal -I m4; autoheader; automake --add-missing --copy --foreign; autoconf

%configure2_5x \
%ifarch x86_64
    --enable-frame-pointer
%endif

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -rf %{buildroot}/usr/share/doc/google-perftools-%{version}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL README
%{_libdir}/lib*.so.*
%{_bindir}/pprof
%{_mandir}/man1/pprof.1*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/*.html doc/*.png doc/*.dot doc/*.gif doc/*.txt TODO
%{_includedir}/google/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
