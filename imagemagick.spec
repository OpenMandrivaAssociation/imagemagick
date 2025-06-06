#ifarch %{ix86}
# Undefined reference to __atomic_load at build time
# when building with clang 7.0-331886
#global optflags %{optflags} -rtlib=compiler-rt
#endif

# (tpg) use LLVM/polly for polyhedra optimization and automatic vector code generation
%ifnarch %{riscv}
%global optflags %{optflags} -O3 -mllvm -polly -mllvm -polly-run-dce -mllvm -polly-run-inliner -mllvm -polly-isl-arg=--no-schedule-serialize-sccs -mllvm -polly-ast-use-context -mllvm -polly-detect-keep-going -mllvm -polly-vectorizer=stripmine
# "-mllvm -polly-invariant-load-hoisting" removed for now because of https://github.com/llvm/llvm-project/issues/57413
%endif

%define _disable_ld_no_undefined 1
# ImageMagick actually uses libtool to load its modules
%define dont_remove_libtool_files 1
%define build_test 0

%bcond_without bootstrap

# some other funny version
# (aw) from the docs: Versions with Q8 in the name are 8 bits-per-pixel
# component (e.g. 8-bit red, 8-bit green, etc.), whereas, Q16 in the
# filename are 16 bits-per-pixel component. A Q16 version permits you
# to read or write 16-bit images without losing precision but requires
# twice as much resources as the Q8 version.
%define qlev Q16HDRI

# their "official" version
%define rversion %(echo %{version} |cut -d. -f1-3)
# their "minor" version
%define minor_rev %(echo %{version} |cut -d. -f4)
# the full file version
%define dversion %{rversion}-%{minor_rev}

%define api 7
%define major 10
%define wandmajor 10
%define cppmajor 5
%define libMagickpp %mklibname Magick++ %{api}.%{qlev} %{cppmajor}
%define libMagickCore %mklibname MagickCore %{api}.%{qlev} %{major}
%define libMagickWand %mklibname MagickWand %{api}.%{qlev} %{wandmajor}
%define devname %mklibname magick -d

Summary:	An X application for displaying and manipulating images
Name:		imagemagick
Version:	7.1.1.47
Release:	1
License:	BSD-like
Group:		Graphics
Url:		https://www.imagemagick.org/
Source0:	https://imagemagick.org/archive/releases/ImageMagick-%{dversion}.tar.xz
# Also:	https://github.com/ImageMagick/ImageMagick/archive/%{dversion}/ImageMagick-%{dversion}.tar.gz
Source1:	ImageMagick.pdf.bz2
Source2:	%{name}.rpmlintrc
# re-scaled from ftp://ftp.imagemagick.org/pub/ImageMagick/images/magick-icon.png
Source10:	magick-icon_16x16.png
Source11:	magick-icon_32x32.png
Source12:	magick-icon_48x48.png
Source13:	magick-icon_64x64.png
Patch0:		perlmagick.rpath.patch
# Libtool stinks -- let's not rely on .la files
# to load modules...
# This patch causes some crashes though, not quite ready yet.
Patch1:		ImageMagick-7.0.6-0-libtool-sucks.patch
Patch3:		imagemagick-7.0.7-openmp-libraries.patch
Patch7:		imagemagick-urw.diff
Patch17:	imagemagick-fpx.diff
Patch19:	ImageMagick-libpath.diff
#Patch20:	imagemagick-6.8.3-pkgconfig.patch

Requires:	%{libMagickCore} = %{EVRD}
BuildRequires:	llvm-polly
BuildRequires:	chrpath
BuildRequires:	ghostscript
BuildRequires:	atomic-devel
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	jbig-devel
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	libtool-devel
BuildRequires:	libwmf-devel
BuildRequires:	perl-devel
BuildRequires:	xdg-utils
# To make aclocal happy
BuildRequires:	git-core
BuildRequires:	pkgconfig(libraw_r)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(libgvc)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libjxl)
%ifnarch %{riscv}
BuildRequires:	pkgconfig(librsvg-2.0)
%endif
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(lqr-1)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(OpenEXR)
%if ! %{with bootstrap}
BuildRequires:	pkgconfig(ddjvuapi)
%endif

%description
ImageMagick is a powerful image display, conversion and manipulation tool. It
runs in an X session. With this tool, you can view, edit and display a variety
of image formats.

ImageMagick can make use of the following delegate programs, available as
packages in Mandriva Linux: curl enscript ffmpeg ghostscript ghostscript-X gimp
gnuplot graphviz html2ps mplayer ncompress netpbm sane-backends tetex-dvips
transfig ufraw xdg-utils zip autotrace povray

%package desktop
Summary:	ImageMagick menus
Group:		Graphics
Requires:	xterm

%description desktop
This package contains the menu and .desktop entries to run the "display"
command from the menu.

%package -n %{libMagickpp}
Summary:	ImageMagick libraries
Group:		System/Libraries
Obsoletes:	%{_lib}magick6 < 6.8.5.6-1

%description -n %{libMagickpp}
This package contains a library for %{name}.

%package -n %{libMagickCore}
Summary:	ImageMagick libraries
Group:		System/Libraries
Conflicts:	%{_lib}magick6 < 6.8.5.6-1

%description -n %{libMagickCore}
This package contains a library for %{name}.

%package -n %{libMagickWand}
Summary:	ImageMagick libraries
Group:		System/Libraries
Conflicts:	%{_lib}magick6 < 6.8.5.6-1

%description -n %{libMagickWand}
This package contains a library for %{name}.

%package -n %{devname}
Summary:	Development libraries and header files for ImageMagick app development
Group:		Development/C
Requires:	%{libMagickpp} = %{version}-%{release}
Requires:	%{libMagickCore} = %{version}-%{release}
Requires:	%{libMagickWand} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
If you want to create applications that will use ImageMagick code or APIs,
you'll need to install these packages as well as ImageMagick. These additional
packages aren't necessary if you simply want to use ImageMagick, however.

ImageMagick-devel is an addition to ImageMagick which includes development
libraries and header files necessary to develop applications.

%package -n perl-Image-Magick
Summary:	Libraries and modules for access to ImageMagick from perl
Group:		Development/Perl
Requires:	%{name} = %{version}
Requires:	graphviz
Requires:	libwmf

%description -n perl-Image-Magick
This is the ImageMagick perl support package. It includes perl modules and
support files for access to ImageMagick library from perl.

%package doc
Summary:	%{name} Documentation
Group:		Books/Other
BuildArch:	noarch

%description doc
This package contains HTML/PDF documentation of %{name}.

%prep
%autosetup -n ImageMagick-%{rversion}-%{minor_rev} -p1

# automake looks for a git id...
rm -f .gitignore
git init
git config user.name "OpenMandriva build system"
git config user.email "root@openmandriva.org"
git add *
git commit -am "OpenMandriva %{version}-%{release}"

# Wipe bundled libtool mess, it isn't LTO aware
rm -rf config/lt* m4/libtool.m4

bzcat %{SOURCE1} > ImageMagick.pdf
install -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} .
libtoolize --copy --force; aclocal -I m4; autoconf; automake -a

%build
#gw the format-string patch is incomplete:
%define Werror_cflags %nil
export CFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
export CXXFLAGS="%{optflags} -fno-strict-aliasing -fPIC"

%configure \
	--disable-static \
	--docdir=%{_defaultdocdir}/imagemagick \
	--with-pic \
	--enable-shared \
	--enable-fast-install \
	--with-threads \
	--with-magick_plus_plus \
	--with-gslib \
	--with-wmf \
	--with-gcc-arch=generic \
	--with-lcms=yes \
	--with-xml \
	--without-dps \
	--without-windows-font-dir \
	--with-modules \
	--with-perl \
	--with-perl-options="INSTALLDIRS=vendor CCFLAGS='%{optflags}' CC='%{__cc} -L$PWD/magick/.libs' LDDLFLAGS='%{build_ldflags} -shared -L$PWD/magick/.libs'" \
	--with-openjp2=yes \
	--with-gvc \
	--with-lqr \
	--with-fftw=yes \
	--with-jxl=yes \
	--with-zstd=yes \
%ifnarch %{riscv}
	--with-rsvg=yes \
%endif
	--with-raw=yes

head -n20 libtool
cp -f /usr/bin/libtool .
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%if %{build_test}
%check
# these tests require X
if [ -f PerlMagick/t/x11/read.t ]; then
    mv PerlMagick/t/x11/read.t PerlMagick/t/x11/read.t.disabled
fi
if [ -f PerlMagick/t/x11/write.t ]; then
    mv PerlMagick/t/x11/write.t PerlMagick/t/x11/write.t.disabled
fi
#dlname=`grep "^dlname" Magick++/lib/.libs/libMagick++.la | cut -d\' -f2`
#LD_PRELOAD="$PWD/Magick++/lib/.libs/$dlname" VERBOSE="1" make check
make check
%endif

%install
# (Abel) set LD_RUN_PATH to null, to avoid adding rpath to perlmagick module
%make_install LD_RUN_PATH="" pkgdocdir=/installed_docs

# fix docs inclusion (fix an unknown new rpm bug)
rm -rf installed_docs; mv %{buildroot}/installed_docs .

# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/libltdl* 
rm -f %{buildroot}%{_libdir}/ImageMagick-*/modules-*/*/*.la

# create compatible symlinks
ln -s libMagick++-%{api}.%{qlev}.so %{buildroot}%{_libdir}/libMagick++.so
ln -s libMagickCore-%{api}.%{qlev}.so %{buildroot}%{_libdir}/libMagickCore.so
ln -s libMagickWand-%{api}.%{qlev}.so %{buildroot}%{_libdir}/libMagickWand.so

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
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=ImageMagick
Name[ru]=ImageMagick
Comment=Views Graphics files
Comment[ru]=Просмотр графических файлов
Exec=%{_bindir}/xterm -geometry 40x15 -title ImageMagick +sb -iconic -e %{_bindir}/display
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;Viewer;
EOF

%files
%doc %{_docdir}/ImageMagick-%{api}
%{_sysconfdir}/ImageMagick-%{api}
%{_bindir}/animate
%{_bindir}/compare
%{_bindir}/composite
%{_bindir}/convert
%{_bindir}/conjure
%{_bindir}/display
%{_bindir}/identify
%{_bindir}/import
%{_bindir}/magick
%{_bindir}/magick-script
%{_bindir}/mogrify
%{_bindir}/montage
%{_bindir}/stream
%dir %{_libdir}/ImageMagick-%{rversion}
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders
%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders/*
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters
%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters/*
%{_libdir}/ImageMagick-%{rversion}/config-%{qlev}
%{_datadir}/ImageMagick-%{api}
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
%exclude %{_mandir}/man3/*::*.3pm*

%files desktop
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %{libMagickpp}
%{_libdir}/libMagick++-%{api}.%{qlev}.so.%{cppmajor}*

%files -n %{libMagickCore}
%{_libdir}/libMagickCore-%{api}.%{qlev}.so.%{major}*

%files -n %{libMagickWand}
%{_libdir}/libMagickWand-%{api}.%{qlev}.so.%{wandmajor}*

%files -n %{devname}
%{_includedir}/ImageMagick-%{api}
%{_bindir}/Magick++-config
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n perl-Image-Magick
%{perl_vendorarch}/Image
%{perl_vendorarch}/auto/Image
%doc %{_mandir}/man3*/*::*.3pm*

%files doc
%doc ImageMagick.pdf LICENSE NOTICE
%doc installed_docs/*

