%define	major 4
%define libname %mklibname google-perftools %{major}
%define develname %mklibname google-perftools -d

Summary:	Performance tools for C++
Name:		google-perftools
Version:	1.10
Release:	1
Group:		System/Libraries
License:	BSD
URL:		http://code.google.com/p/google-perftools/
Source0:	http://google-perftools.googlecode.com/files/%{name}-%{version}.tar.gz
Patch0:		google-perftools-1.5-antibork.diff
BuildRequires:	file
BuildRequires:	libtool
BuildRequires:	autoconf2.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Obsoletes:	%{mklibname google-perftools 0 -d}

%description -n	%{develname}
The google-perftools packages contains some utilities to improve and analyze
the performance of C++ programs.  This includes an optimized thread-caching
malloc() and cpu and heap profiling utilities.

This package contains the static google-perftools library and its header files.

%prep

%setup -q
%patch0 -p0

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
    --enable-frame-pointers
%endif

%make

#%%check
#make check

%install
rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -rf %{buildroot}/usr/share/doc/google-perftools-%{version}

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL README
%{_libdir}/lib*.so.%{major}*
%{_libdir}/libprofiler.so.0*
%{_bindir}/pprof
%{_mandir}/man1/pprof.1*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/*.html doc/*.png doc/*.dot doc/*.gif doc/*.txt TODO
%{_includedir}/google/*.h
%{_libdir}/*.*a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Aug 23 2012 Crispin Boylan <crisb@mandriva.org> 1.10-1
+ Revision: 815650
- New release

* Wed Jul 27 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.1-1
+ Revision: 691913
- 1.8.1

* Tue Feb 22 2011 Oden Eriksson <oeriksson@mandriva.com> 1.7-1
+ Revision: 639292
- 1.7

* Tue Nov 30 2010 Shlomi Fish <shlomif@mandriva.org> 1.6-2mdv2011.0
+ Revision: 603236
- Bumped the release number for a new gcc-4.5.1 compiled build (with better performance)

* Sun Sep 19 2010 Shlomi Fish <shlomif@mandriva.org> 1.6-1mdv2011.0
+ Revision: 579902
- Upgraded to 1.6 and replaced the tar.gz with tar.lzma

* Tue Feb 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5-1mdv2010.1
+ Revision: 506594
- disable the test suite for now
- 1.5
- fix install
- 1.4
- 1.3

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Feb 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2009.1
+ Revision: 336146
- 1.0

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.98-1mdv2009.0
+ Revision: 239028
- 0.98

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 31 2007 Oden Eriksson <oeriksson@mandriva.com> 0.93-2mdv2008.0
+ Revision: 76891
- rebuild

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 0.93-1mdv2008.0
+ Revision: 66843
- fix build
- 0.93
- conform to the 2008 specs
- Import google-perftools

