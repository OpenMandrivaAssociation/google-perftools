%define	major 0
%define libname	%mklibname google-perftools %{major}

Summary:	Performance tools for C++
Name:		google-perftools
Version:	0.8
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://goog-perftools.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/goog-perftools/%{name}-%{version}.tar.bz2
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

%package -n	%{libname}-devel
Summary:	Static library and header files for the google-perftools library
Group:		Development/C++
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
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

%configure2_5x

make

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

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/*.html doc/*.png doc/*.dot doc/*.gif doc/*.txt TODO
%dir %{_includedir}/google/perftools
%{_includedir}/google/perftools/*.h
%{_includedir}/google/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
