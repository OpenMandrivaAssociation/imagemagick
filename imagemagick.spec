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
Version:	7.1.2.29
Release:	2
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
# Keep OpenMP for pixel loops, but use pthread mutexes for MagickCore
# locks. omp_lock_t is not fork-safe and crashes php-fpm/imagick in
# GetPolicyValue() after the worker has been running for a while.
Patch21:	imagemagick-pthread-mutex-with-openmp.patch
# OpenCL used lt_dlopen; we do not link libltdl (see Patch1). Use libc
# dlopen and the runtime soname (libOpenCL.so is only in -devel).
Patch22:	imagemagick-opencl-dlopen.patch

Requires:	%{libMagickCore} = %{EVRD}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
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
BuildRequires:	pkgconfig(OpenCL)
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
slibtoolize --copy --force; aclocal -I m4; autoconf; automake -a

%build
#gw the format-string patch is incomplete:
%define Werror_cflags %nil
# Keep ${CFLAGS}/${CXXFLAGS} so a %%pgo pass can inject -fprofile-generate/use
export CFLAGS="${CFLAGS:-%{optflags}} -fno-strict-aliasing -fPIC"
export CXXFLAGS="${CXXFLAGS:-%{optflags}} -fno-strict-aliasing -fPIC"

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
	--with-perl-options="INSTALLDIRS=vendor CCFLAGS='${CFLAGS}' CC='%{__cc} -L$PWD/magick/.libs' LDDLFLAGS='${LDFLAGS:-%{?build_ldflags}} -shared -L$PWD/magick/.libs'" \
	--with-openjp2=yes \
	--with-gvc \
	--with-lqr \
	--with-fftw=yes \
	--with-jxl=yes \
	--with-zstd=yes \
	--enable-opencl \
%ifnarch %{riscv}
	--with-rsvg=yes \
%endif
	--with-raw=yes

#head -n20 libtool
#cp -f /usr/bin/libtool .
# Disable rpath
#sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
#sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

# Train the instrumented binary on the paths that dominate real use:
# web/thumbnail convert (jpeg/png/webp/gif), identify, montage, compare,
# composite, annotate, and the MagickWand/Magick++ APIs (php-imagick etc.).
# Optional delegates (svg, pdf, heic, jxl, raw) are tried and ignored if
# the coder or policy is unavailable. No X11.
%pgo
set +e
export LLVM_PROFILE_FILE="%{_pgo_profile_dir}/imagemagick-%%m-%%p.profraw"
# Do not let a GPU on the build host own the profile. CPU OpenCL (pocl
# etc.) still trains the host enqueue path; if no CPU ICD exists, IM
# falls back to the OpenMP implementations and those stay hot.
export MAGICK_OCL_DEVICE=CPU

TOP="$PWD"
# slibtool drops coder .so files in .libs; magick.sh still points at coders/.
MAGICK="$TOP/utilities/.libs/magick"
if [ ! -x "$MAGICK" ]; then
	MAGICK="$TOP/utilities/magick"
fi
if [ ! -x "$MAGICK" ]; then
	echo "PGO: instrumented magick binary missing"
	exit 1
fi
export LD_LIBRARY_PATH="$TOP/MagickCore/.libs:$TOP/MagickWand/.libs:$TOP/Magick++/lib/.libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export MAGICK_CODER_MODULE_PATH="$TOP/coders/.libs"
export MAGICK_FILTER_MODULE_PATH="$TOP/filters/.libs"
export MAGICK_CONFIGURE_PATH="$TOP/config"

im() {
	"$MAGICK" "$@"
}

# Fail only if the core CLI is broken; optional formats just warn.
try() {
	im "$@"
	rc=$?
	if [ $rc -ne 0 ]; then
		echo "PGO: skipped (exit $rc): magick $*"
	fi
	return 0
}

WORKDIR="$PWD/pgo-train"
rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Built-in / generated sources — no extra SourceN files needed
im logo: logo.png || exit 1
im wizard: wizard.png || exit 1
im rose: rose.png || exit 1
try granite: granite.png
try netscape: netscape.gif
# Photo-sized raster so OpenMP / OpenCL-CPU kernels actually have work
try -size 1280x720 plasma:fractal photo.png
if [ ! -f photo.png ]; then
	im logo: -resize 1280x720 photo.png || exit 1
fi
try -size 640x360 gradient:black-white gradient.png
try -size 320x240 xc:'#224466' solid.png
try -size 400x80 -background white -fill black -pointsize 28 caption:'ImageMagick PGO' caption.png

# --- encode/decode the formats people actually convert between ---
for fmt in jpg png webp gif tiff bmp ppm pam miff; do
	try photo.png -quality 85 "enc.$fmt"
	try "enc.$fmt" "round.png"
done
# ICO rejects large images; HEIC here wants 8-bit (HDRI default is 16)
try rose.png enc.ico
try enc.ico ico-round.png
try photo.png -depth 8 out.heic
try out.heic heic-round.png
# JPEG variants: baseline, progressive, 4:2:0, grayscale
try photo.png -quality 82 -sampling-factor 4:2:0 jpeg420.jpg
try photo.png -interlace Plane -quality 80 jpegprog.jpg
try photo.png -colorspace Gray -quality 80 jpeggray.jpg
# PNG with alpha
try wizard: -resize 400x PNG32:alpha.png
try alpha.png -background none -resize 200x alpha-small.png
# Animated GIF (WordPress / stickers)
try -delay 8 -loop 0 logo: -resize 120x \
	\( +clone -roll +8+0 \) \( +clone -roll +0+8 \) anim.gif
try anim.gif -coalesce -resize 80x -layers optimize anim-opt.gif

# Delegates that exist on this package but may be policy-gated
try photo.png out.jxl
try photo.png out.jp2
try photo.png out.exr
try rose.png out.svg
try photo.png pdf:out.pdf
try out.pdf[0] pdfpage.png
if [ -f ../tests/input_svg_gradient_transform.svg ]; then
	try ../tests/input_svg_gradient_transform.svg svg-in.png
fi
if [ -f ../tests/rose.pnm ]; then
	try ../tests/rose.pnm rose-pnm.png
fi

# --- geometry / colors / filters (web + CLI workhorses) ---
try photo.png -auto-orient -resize '1024x1024>' -strip -quality 82 web.jpg
try photo.png -thumbnail 150x150^ -gravity center -extent 150x150 thumb.jpg
try photo.png -crop 640x360+80+40 +repage crop.png
try photo.png -rotate 90 rot.png
try photo.png -flip -flop flip.png
try photo.png -resize 50% -unsharp 0x0.75+0.75+0.008 unsharp.jpg
try photo.png -gaussian-blur 0x1.2 blur.png
try photo.png -sharpen 0x1.0 sharp.png
try photo.png -brightness-contrast 5x5 bc.png
try photo.png -modulate 105,110,100 mod.png
try photo.png -level 5%,95% level.png
try photo.png -normalize norm.png
try photo.png -colorspace sRGB srgb.png
try photo.png -colorspace Gray gray.png
try photo.png -colorspace CMYK cmyk.jpg
try photo.png -gamma 1.1 gamma.png
try photo.png -posterize 16 post.png
try photo.png -colors 64 +dither pal.png
try photo.png -trim +repage trim.png
try photo.png -bordercolor white -border 8 border.png
try photo.png -resize 800x -quality 70 -strip -interlace Plane web-sm.jpg
# liquid-rescale is lqr; cheap size so it does not dominate the train time
try rose.png -liquid-rescale 50%x50% lqr.png

# --- composite / annotate / draw (watermarks, captions) ---
try photo.png -gravity southeast -pointsize 22 -fill white \
	-annotate +16+16 'PGO watermark' annotated.jpg
try photo.png caption.png -gravity south -geometry +0+10 -compose over -composite marked.png
try -size 200x200 xc:none -fill '#cc3333' -draw 'circle 100,100 100,20' ball.png
try photo.png ball.png -gravity northeast -geometry +20+20 -compose over -composite badged.png

# --- CLI tools beyond convert ---
try identify -verbose photo.png
try identify jpeg420.jpg png:enc.png anim.gif
try compare -metric RMSE photo.png web.jpg diff.png
try montage logo.png wizard.png rose.png -geometry 120x120+4+4 -tile 3x1 sheet.png
try mogrify -resize 320x -quality 80 jpeg420.jpg
try stream -map rgb -storage-type char rose.png stream.rgb

# --- MagickWand / Magick++ (php-imagick, PerlMagick, C++ users) ---
cd "$TOP"
make %{?_smp_mflags} tests/wandtest tests/drawtest tests/validate \
	Magick++/tests/appendImages Magick++/tests/readWriteImages \
	Magick++/tests/attributes Magick++/tests/color \
	Magick++/tests/montageImages Magick++/tests/morphImages \
	Magick++/tests/averageImages Magick++/tests/coalesceImages
tests/wandtest
tests/drawtest
if [ -x tests/validate ]; then
	# lowercase names match tests/validate-*.tap
	for kind in convert identify compare composite montage magick stream colorspace; do
		tests/validate -validate "$kind"
	done
fi
export SRCDIR="$TOP/Magick++/tests/"
for t in appendImages readWriteImages attributes color montageImages \
	morphImages averageImages coalesceImages; do
	if [ -x Magick++/tests/$t ]; then
		Magick++/tests/$t
	fi
done

rm -rf "$WORKDIR"
exit 0

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

