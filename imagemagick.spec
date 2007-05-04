%define build_plf 0
%{?_with_plf: %global build_plf 1}

%define build_modules 0
%{?_with_modules: %global build_modules 1}

%define enable_jasper	1
%{?_with_jasper: %global enable_jasper 1}

%define enable_graphwiz	0
%{?_with_graphwiz: %global enable_graphwiz 1}

%define Name		ImageMagick

%define major		10.7.0
%define libname		%mklibname magick %{major}
%define fversion	6.3.2
%define rev 		9
%define rel 		7
%define qlev		Q16

%define dversion	%{fversion}-%{rev}

# enablefpx = 0 (don't use libfpx)
# enablefpx = 1 (use libfpx)
%define enablefpx	0

%if %build_plf
# fpx build is broken, tests fail
%define enablefpx	0
%define distsuffix plf
%endif

Summary:	An X application for displaying and manipulating images
Name:		imagemagick
%if %rev > 0
Version:	%{fversion}.%{rev}
%else
Version:	%{fversion}
%endif
Release:	%mkrel %rel
License:	BSD style
Group:		Graphics
URL:		http://www.imagemagick.org/
Source0:	ftp://ftp.sunet.se/pub/multimedia/graphics/ImageMagick/ImageMagick-%{dversion}.tar.bz2
Source1:	ImageMagick.pdf.bz2
# re-scaled from ftp://ftp.imagemagick.org/pub/ImageMagick/images/magick-icon.png
Source10:	magick-icon_16x16.png
Source11:	magick-icon_32x32.png
Source12:	magick-icon_48x48.png
Source13:	magick-icon_64x64.png
#
Patch0:		ImageMagick-6.2.7-docdir.patch
Patch4:		ImageMagick-6.0.1-includedir.patch
Patch7:		ImageMagick-6.3.2-urw.patch
Patch8:		ImageMagick-6.2.7-libname.patch
Patch17:	ImageMagick-6.3.2-fpx.patch
Patch18:	ImageMagick-6.1.7-windows-fontdir.patch
Patch19:	ImageMagick-6.2.9-8-libpath.patch
Patch20:	ImageMagick-6.2.5-fix-montageimages-test.patch
Requires:	%{libname} = %{version}
Requires:	ghostscript
Obsoletes:	ImageMagick < 6.3.2.9-6
Provides:	ImageMagick = %{version}-%{release}
BuildRequires:	ghostscript
BuildRequires:	bzip2-devel
BuildRequires:	freetype2-devel >= 2.1.7
%if %{enablefpx}
BuildRequires:	libfpx-devel
%endif
%if %{enable_jasper}
BuildRequires:	libjasper-devel
%endif
%if %{enable_graphwiz}
Requires:	graphviz
BuildRequires:	libgraphviz-devel >= 2.9.0
%endif
BuildRequires:	libexif-devel
BuildRequires:	libjbig-devel
BuildRequires:	lcms-devel >= 1.15
BuildRequires:	tiff-devel
BuildRequires:	libdjvulibre-devel
BuildRequires:	libwmf-devel
BuildRequires:	libxml2-devel
BuildRequires:	XFree86-devel
BuildRequires:	perl-devel
# (oe) P19 should take care of the linking against old libs
# problem, at least for the perl-Image-Magick package
#BuildConflicts:	libMagick-devel < %{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
BuildRequires:	libltdl-devel >= 1.4.3-10mdk
BuildRequires:	libgd-devel
BuildRequires:	chrpath
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
ImageMagick is a powerful image display, conversion and manipulation tool. It
runs in an X session. With this tool, you can view, edit and display a variety
of image formats.

Build Options:
--with plf		Build for PLF (fpx support)
--with modules		Compile all supported image types as modules
--with jasper		Enable JPEG2000 support (enabled)
--with graphviz		Enable Graphviz support (enabled)

%if %build_plf
This package is in PLF because it provides additional support for:
- libfpx
which is covered by software patents.
%endif

%package 	desktop
Summary:	ImageMagick menus
Group:		Graphics
Requires:	xterm
Obsoletes:	ImageMagick-desktop < 6.3.2.9-6

%description	desktop
This package contains the menu and .desktop entries to run the "display"
command from the menu.

%package -n	%{libname}
Summary:	ImageMagick libraries
Group:		System/Libraries
Obsoletes:	ImageMagick-lib	libMagick5
Obsoletes:	%mklibname Magick %{major}
Provides:	ImageMagick-lib = %{version}-%{release}
Provides:	libMagick5 = %{version}-%{release}

%description -n	%{libname}
This package contains the libraries needed to run programs dynamically
linked with ImageMagick libraries.

%package -n	%{libname}-devel
Summary:	Static libraries and header files for ImageMagick app development
Group:		Development/C
Obsoletes:	%{Name}-devel
Obsoletes:	libMagick5-devel
Obsoletes:	%mklibname Magick %{major} -d
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{Name}-devel = %{version}-%{release}
Provides:	libmagick-devel = %{version}-%{release}
Provides:	libMagick-devel = %{version}-%{release}
Provides:	libMagick5-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	libjbig-devel
%if %{enable_jasper}
Requires:	libjasper-devel
%endif
%if %{enablefpx}
Requires:	libfpx-devel
%endif
%if %{enable_graphwiz}
Requires:	libgraphviz-devel
%define _requires_exceptions devel(libcdt)\\|devel(libcircogen)\\|devel(libcommon)\\|devel(libdotgen)\\|devel(libdotneato)\\|devel(libfdpgen)\\|devel(libgraph)\\|devel(libgvrender)\\|devel(libneatogen)\\|devel(libpack)\\|devel(libpathplan)\\|devel(libtwopigen)\\|devel(libgvc)\\|devel(libgvgd)
%endif

%description -n	%{libname}-devel
If you want to create applications that will use ImageMagick code or
APIs, you'll need to install these packages as well as
ImageMagick. These additional packages aren't necessary if you simply
want to use ImageMagick, however.

ImageMagick-devel is an addition to ImageMagick which includes static
libraries and header files necessary to develop applications.

%package -n	perl-Image-Magick
Summary:	Libraries and modules for access to ImageMagick from perl
Group:		Development/Perl
Requires:	%{name} = %{version}
Obsoletes:	perl-Magick
Provides:	perl-Magick
%if %{enable_graphwiz}
Requires:	graphviz
%endif

%description -n	perl-Image-Magick
This is the ImageMagick perl support package. It includes perl modules 
and support files for access to ImageMagick library from perl.

%package	doc
Summary:	%{name} Documentation
Group:		Books/Other
Obsoletes:	ImageMagick-doc < 6.3.2.9-6

%description	doc
This package contains HTML/PDF documentation of %{name}.

%prep

%setup -q -n %{Name}-%{fversion}
%patch0 -p1 -b .docdir
%patch4 -p1 -b .include
%patch7 -p1 -b .urw
%patch8 -p1 -b .libname
%patch17 -p1 -b .fpx
%patch18 -p1 -b .windows
%patch19 -p1 -b .libpath
%patch20 -p1 -b .ppc

%__libtoolize --copy --force
aclocal-1.8 -I m4
WANT_AUTOCONF_2_5=1 autoconf
automake-1.8

bzcat %{SOURCE1} > ImageMagick.pdf
install -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} .

%build
#define __libtoolize /bin/true

export CFLAGS="$CFLAGS -fno-strict-aliasing -fPIC"
export CXXFLAGS="$CXXFLAGS -fno-strict-aliasing -fPIC"

# don't use icecream
export PATH=/bin:/usr/bin:/usr/X11R6/bin

%configure2_5x \
    --enable-fast-install \
    --disable-ltdl-install \
    --without-dps \
%if %build_modules
    --with-modules \
%else
    --without-modules \
%endif
    --enable-shared \
    --with-pic \
    --with-perl-options="INSTALLDIRS=vendor" \
%if %{enablefpx}
    --with-fpx=yes \
%endif
%if %{enable_jasper}
    --with-jp2 \
%else
    --without-jp2 \
%endif
%if %{enable_graphwiz}
    --with-dot \
%else
    --without-dot \
%endif

# without the following, it doesn't build correctly with "make -j 4"
perl -lpi -e '$_ .= " magick/libMagick.la" if index($_, q($(PERLMAKEFILE))) == 0' Makefile

%make

%check
# these tests require X
if [ -f PerlMagick/t/x/read.t ]; then
	mv PerlMagick/t/x/read.t PerlMagick/t/x/read.t.disabled
fi
if [ -f PerlMagick/t/x/write.t ]; then
	mv PerlMagick/t/x/write.t PerlMagick/t/x/write.t.disabled
fi
#dlname=`grep "^dlname" Magick++/lib/.libs/libMagick++.la | cut -d\' -f2`
#LD_PRELOAD="$PWD/Magick++/lib/.libs/$dlname" VERBOSE="1" make check

make check

%install
rm -rf %{buildroot}

# (Abel) set LD_RUN_PATH to null, to avoid adding rpath to perlmagick module
%makeinstall_std LD_RUN_PATH="" pkgdocdir=%{_datadir}/doc/%{name}-doc-%{fversion}

# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/%{Name}-%{fversion}/modules-%{qlev}/coders/*.a \
      %{buildroot}%{_libdir}/%{Name}-%{fversion}/modules-%{qlev}/filters/*.a \
      %{buildroot}%{_libdir}/libltdl* 

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/Magick-config
%multiarch_binaries %{buildroot}%{_bindir}/Magick++-config
%multiarch_binaries %{buildroot}%{_bindir}/Wand-config
%multiarch_includes %{buildroot}%{_includedir}/magick/magick-config.h
%multiarch_includes %{buildroot}%{_includedir}/wand/wand-config.h
%endif

# nuke rpath
chrpath -d %{buildroot}%{perl_vendorarch}/auto/Image/Magick/Magick.so

# icons
install -m 755 -d %{buildroot}%{_liconsdir} \
	   %{buildroot}%{_iconsdir} \
	   %{buildroot}%{_iconsdir}/hicolor/64x64/apps \
           %{buildroot}%{_miconsdir}
install -m 644 magick-icon_16x16.png %{buildroot}%{_miconsdir}/%{name}.png
install -m 644 magick-icon_32x32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 magick-icon_48x48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 magick-icon_64x64.png %{buildroot}%{_iconsdir}/hicolor/64x64/apps/%{name}.png

install -m 755 -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} <<EOF
?package(ImageMagick): command="%{_bindir}/display" \
	needs="X11" \
	icon="%{name}.png" \
	section="Office/Graphics" \
	title="ImageMagick Viewer" \
	terminal="true" \
%if %{mdkversion} >= 200610
	xdg=true \
%endif
	longtitle="Views Graphics files"
EOF

install -m 755 -d %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{Name}
Comment=Views Graphics files
Exec=%{_bindir}/xterm -geometry 40x15 -title ImageMagick +sb -iconic -e %{_bindir}/display
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Office-Graphs;Graphics;Viewer;
EOF


%clean
rm -rf %{buildroot}

%post desktop
%update_menus

%postun desktop
%clean_menus

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README.txt
%{_bindir}/animate
%{_bindir}/compare
%{_bindir}/composite
%{_bindir}/convert
%{_bindir}/conjure
%{_bindir}/display
%{_bindir}/identify
%{_bindir}/import
%{_bindir}/mogrify
%{_bindir}/montage
%{_bindir}/stream
%dir %{_libdir}/%{Name}-%{fversion}
%dir %{_libdir}/%{Name}-%{fversion}/modules-%{qlev}
%dir %{_libdir}/%{Name}-%{fversion}/modules-%{qlev}/coders
%dir %{_libdir}/%{Name}-%{fversion}/config
%{_datadir}/%{Name}-%{fversion}
%{_libdir}/%{Name}-%{fversion}/config/*.xml
%if %build_modules
%{_libdir}/%{Name}-%{fversion}/modules-%{qlev}/filters
%{_libdir}/%{Name}-%{fversion}/modules-%{qlev}/coders/*.so
%{_libdir}/%{Name}-%{fversion}/modules-%{qlev}/coders/*.la
%endif
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/*::*.3pm*

%files desktop
%defattr(-,root,root)
%{_menudir}/%{name}
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png

%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/libMagick++-%{major}.so.0*
%{_libdir}/libMagick-%{major}.so.0*
%{_libdir}/libWand-%{major}.so.0*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc ChangeLog
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/Magick-config
%multiarch %{multiarch_bindir}/Magick++-config
%multiarch %{multiarch_bindir}/Wand-config
%multiarch %{multiarch_includedir}/magick/magick-config.h
%multiarch %{multiarch_includedir}/wand/wand-config.h

%endif
%{_bindir}/Magick-config
%{_bindir}/Magick++-config
%{_bindir}/Wand-config
%{_libdir}/*.a
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%files -n perl-Image-Magick
%defattr(-,root,root)
%{_mandir}/man3*/*::*.3pm*
%{perl_vendorarch}/Image
%{perl_vendorarch}/auto/Image

%files doc
%defattr(-,root,root)
%doc ImageMagick.pdf ChangeLog LICENSE NEWS
%doc NOTICE QuickStart.txt
#doc www/ images/ index.html
# gw maybe we should the doc location in configure instead
%doc %_datadir/doc/%name-doc-%fversion/



