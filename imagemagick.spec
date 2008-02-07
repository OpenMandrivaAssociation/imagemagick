# V E R S I O N   P A R T S

# their "official" version
%define rversion 6.3.8

# their "minor" version
%define minor_rev 3

# some other funny version
%define qlev Q16

# the full file version
%define dversion %{rversion}-%{minor_rev}

# their "major" changes with every release it seems
%define major 10.10.0

# S T A N D A R D   M A N D R I V A   S T U F F
%define libname %mklibname magick %{major}
%define develname %mklibname magick -d

Summary:	An X application for displaying and manipulating images
Name:		imagemagick
Version:	%{rversion}
Release:	%mkrel 1
License:	BSD style
Group:		Graphics
URL:		http://www.imagemagick.org/
Source0:	ftp://ftp.sunet.se/pub/multimedia/graphics/ImageMagick/ImageMagick-%{dversion}.tar.gz
Source1:	ImageMagick.pdf.bz2
# re-scaled from ftp://ftp.imagemagick.org/pub/ImageMagick/images/magick-icon.png
Source10:	magick-icon_16x16.png
Source11:	magick-icon_32x32.png
Source12:	magick-icon_48x48.png
Source13:	magick-icon_64x64.png
Patch0:		imagemagick-docdir.diff
Patch4:		ImageMagick-6.0.1-includedir.patch
Patch7:		imagemagick-urw.diff
Patch17:	imagemagick-fpx.diff
Patch19:	ImageMagick-libpath.diff
Patch20:	ImageMagick-6.2.5-fix-montageimages-test.patch
Requires:	%{libname} = %{version}
Requires:	ghostscript
Requires:	graphviz
Requires:	html2ps
Obsoletes:	ImageMagick < 6.3.2.9-6
Provides:	ImageMagick = %{version}-%{release}
BuildRequires:	XFree86-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.8
BuildRequires:	avahi-client-devel
BuildRequires:	avahi-common-devel
BuildRequires:	avahi-glib-devel
BuildRequires:	bzip2-devel
BuildRequires:	cairo-devel
BuildRequires:	chrpath
BuildRequires:	dbus-glib-devel
BuildRequires:	djvulibre-devel
BuildRequires:	expat-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype2-devel >= 2.1.7
BuildRequires:	gd-devel
BuildRequires:	ghostscript
BuildRequires:	glib2-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	graphviz-devel >= 2.9.0
BuildRequires:	lcms-devel >= 1.15
BuildRequires:	libGConf2-devel
BuildRequires:	libcroco0.6-devel
BuildRequires:	libexif-devel
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	libgsf-devel
BuildRequires:	libjasper-devel
BuildRequires:	libjbig-devel
BuildRequires:	libltdl-devel >= 1.4.3-10
BuildRequires:	librsvg-devel
BuildRequires:	libwmf
BuildRequires:	libwmf-devel
BuildRequires:	libxml2-devel
BuildRequires:	lqr-devel
BuildRequires:	openssl-devel
BuildRequires:	pango-devel
BuildRequires:	perl-devel
BuildRequires:	pixman-devel
BuildRequires:	tiff-devel
BuildConflicts:	%{name}-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ImageMagick is a powerful image display, conversion and manipulation tool. It
runs in an X session. With this tool, you can view, edit and display a variety
of image formats.

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

%description -n	%{libname}
This package contains the libraries needed to run programs dynamically linked
with ImageMagick libraries.

%package -n	%{develname}
Summary:	Static libraries and header files for ImageMagick app development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	ImageMagick-devel = %{version}-%{release}
Provides:	libmagick-devel = %{version}-%{release}
Provides:	libMagick-devel = %{version}-%{release}
Obsoletes:	ImageMagick-devel
Provides:	libMagick5-devel = %{version}-%{release}
Obsoletes:	libMagick5-devel
# 2006
Obsoletes:	%{mklibname Magick 8.3.2 -d}
# 2007.0
Obsoletes:	%{mklibname magick 10.4.0 -d} %{mklibname Magick 10.4.0 -d}
# 2007.1/2008.0
Obsoletes:	%{mklibname magick 10.7.0 -d} %{mklibname Magick 10.7.0 -d}
# pre 2008.1
Obsoletes:	%{mklibname magick 10.9.0 -d} %{mklibname Magick 10.9.0 -d}

%description -n	%{develname}
If you want to create applications that will use ImageMagick code or APIs,
you'll need to install these packages as well as ImageMagick. These additional
packages aren't necessary if you simply want to use ImageMagick, however.

ImageMagick-devel is an addition to ImageMagick which includes static libraries
and header files necessary to develop applications.

%package -n	perl-Image-Magick
Summary:	Libraries and modules for access to ImageMagick from perl
Group:		Development/Perl
Requires:	%{name} = %{version}
Provides:	perl-Magick = %{version}-%{release}
Obsoletes:	perl-Magick
Requires:	graphviz
Requires:	libwmf

%description -n	perl-Image-Magick
This is the ImageMagick perl support package. It includes perl modules and
support files for access to ImageMagick library from perl.

%package	doc
Summary:	%{name} Documentation
Group:		Books/Other
Obsoletes:	ImageMagick-doc < 6.3.2.9-6

%description	doc
This package contains HTML/PDF documentation of %{name}.

%prep

%setup -q -n ImageMagick-%{rversion}

# major check
LIBRARY_CURRENT=`grep "^LIBRARY_CURRENT=" version.sh | cut -d= -f2`
LIBRARY_REVISION=`grep "^LIBRARY_REVISION=" version.sh | cut -d= -f2`
LIBRARY_AGE=`grep "^LIBRARY_AGE=" version.sh | cut -d= -f2`
real_major="`echo ${LIBRARY_CURRENT}.${LIBRARY_REVISION}.${LIBRARY_AGE} | perl -pi -e 's|\.||g'`"
package_major="`echo %{major} | perl -pi -e 's|\.||g'`"

if [ "${package_major}" -ne "${real_major}" ]; then
    echo "%{major} is not ${LIBRARY_CURRENT}.${LIBRARY_REVISION}.${LIBRARY_AGE}"
    exit 1
fi

%patch0 -p0 -b .docdir
%patch4 -p1 -b .include
%patch7 -p0 -b .urw
%patch17 -p0 -b .fpx
%patch19 -p1 -b .libpath
%patch20 -p1 -b .ppc

bzcat %{SOURCE1} > ImageMagick.pdf
install -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} .

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
#libtoolize --copy --force; aclocal -I m4; autoconf; automake
aclocal -I m4; autoconf; automake

export CFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
export CXXFLAGS="%{optflags} -fno-strict-aliasing -fPIC"

# don't use icecream
export PATH=/bin:/usr/bin:/usr/X11R6/bin

%configure2_5x \
    --with-pic \
    --enable-shared \
    --enable-fast-install \
    --disable-ltdl-install \
    --with-threads \
    --with-magick_plus_plus \
    --with-gslib \
    --with-wmf \
    --with-lcms \
    --with-rsvg \
    --with-xml \
    --without-dps \
    --without-windows-font-dir \
    --without-modules \
    --with-perl \
    --with-perl-options="INSTALLDIRS=vendor" \
    --with-jp2 \
    --with-dot \
    --with-lqr

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
%makeinstall_std LD_RUN_PATH="" pkgdocdir=/installed_docs

# fix docs inclusion (fix an unknown new rpm bug)
rm -rf installed_docs; mv %{buildroot}/installed_docs .

# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders/*.a \
      %{buildroot}%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters/*.a \
      %{buildroot}%{_libdir}/libltdl* 

%multiarch_binaries %{buildroot}%{_bindir}/Magick-config
%multiarch_binaries %{buildroot}%{_bindir}/Magick++-config
%multiarch_binaries %{buildroot}%{_bindir}/Wand-config
%multiarch_includes %{buildroot}%{_includedir}/magick/magick-config.h

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


install -m 755 -d %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=ImageMagick
Comment=Views Graphics files
Exec=%{_bindir}/xterm -geometry 40x15 -title ImageMagick +sb -iconic -e %{_bindir}/display
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Office-Graphs;Graphics;Viewer;
EOF

%post desktop
%update_menus

%postun desktop
%clean_menus

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

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
%dir %{_libdir}/ImageMagick-%{rversion}
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders
%dir %{_libdir}/ImageMagick-%{rversion}/config
%{_datadir}/ImageMagick-%{rversion}
%{_libdir}/ImageMagick-%{rversion}/config/*.xml
#%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters
#%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders/*.so
#%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders/*.la
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/*::*.3pm*

%files desktop
%defattr(-,root,root)
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png

%files -n %{libname}
%defattr(-,root,root,755)
%{_libdir}/libMagick++.so.*
%{_libdir}/libMagick.so.*
%{_libdir}/libWand.so.*

%files -n %{develname}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/Magick-config
%multiarch %{multiarch_bindir}/Magick++-config
%multiarch %{multiarch_bindir}/Wand-config
%multiarch %{multiarch_includedir}/magick/magick-config.h
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
%{perl_vendorarch}/Image
%{perl_vendorarch}/auto/Image
%{_mandir}/man3*/*::*.3pm*

%files doc
%defattr(-,root,root)
%doc ImageMagick.pdf ChangeLog LICENSE NEWS NOTICE
%doc QuickStart.txt installed_docs/*
