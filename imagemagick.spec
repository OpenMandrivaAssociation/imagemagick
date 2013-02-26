%define _disable_ld_no_undefined 1
# ImageMagick actually uses libtool to load its modules
%define dont_remove_libtool_files 1
%define build_test 0
%define bootstrap 0

# their "official" version
%define rversion 6.8.3

# their "minor" version
%define minor_rev 4

# some other funny version
# (aw) from the docs: Versions with Q8 in the name are 8 bits-per-pixel
# component (e.g. 8-bit red, 8-bit green, etc.), whereas, Q16 in the
# filename are 16 bits-per-pixel component. A Q16 version permits you
# to read or write 16-bit images without losing precision but requires
# twice as much resources as the Q8 version.
%define qlev Q16

# the full file version
%define dversion %{rversion}-%{minor_rev}

%define major 6
%define libname %mklibname magick %{major}
%define develname %mklibname magick -d

Summary:	An X application for displaying and manipulating images
Name:		imagemagick
Version:	%{rversion}.%{minor_rev}
Release:	2
License:	BSD-like
Group:		Graphics
URL:		http://www.imagemagick.org/
Source0:	ftp://ftp.imagemagick.org/pub/ImageMagick/ImageMagick-%dversion.tar.xz
Source1:	ImageMagick.pdf.bz2
Source2:	%{name}.rpmlintrc
# re-scaled from ftp://ftp.imagemagick.org/pub/ImageMagick/images/magick-icon.png
Source10:	magick-icon_16x16.png
Source11:	magick-icon_32x32.png
Source12:	magick-icon_48x48.png
Source13:	magick-icon_64x64.png
Patch7:		imagemagick-urw.diff
Patch17:	imagemagick-fpx.diff
Patch19:	ImageMagick-libpath.diff
Patch20:	imagemagick-6.8.3-pkgconfig.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	chrpath
BuildRequires:	pkgconfig(jasper)
BuildRequires:	jbig-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(lcms)
BuildRequires:	pkgconfig(lqr-1)
BuildRequires:	libtool-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	libwmf-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libgvc)
#gw aclocal:
BuildRequires:	subversion
BuildRequires:	automake > 1.11.1
%if !%bootstrap
BuildRequires:	pkgconfig(ddjvuapi)
%endif
BuildRequires:	ghostscript
BuildConflicts:	%{develname}
Requires:	%{libname} = %{version}

%description
ImageMagick is a powerful image display, conversion and manipulation tool. It
runs in an X session. With this tool, you can view, edit and display a variety
of image formats.

ImageMagick can make use of the following delegate programs, available as
packages in Mandriva Linux: curl enscript ffmpeg ghostscript ghostscript-X gimp
gnuplot graphviz html2ps mplayer ncompress netpbm sane-backends tetex-dvips
transfig ufraw xdg-utils zip autotrace povray

%package 	desktop
Summary:	ImageMagick menus
Group:		Graphics
Requires:	xterm

%description	desktop
This package contains the menu and .desktop entries to run the "display"
command from the menu.

%package -n	%{libname}
Summary:	ImageMagick libraries
Group:		System/Libraries
# (Anssi 02/2008): Wrongly named at first, can be removed when major changes again:
Obsoletes:	%{_lib}magick%{major}.0.0 < %{version}-%{release}

%description -n	%{libname}
This package contains the libraries needed to run programs dynamically linked
with ImageMagick libraries.

%package -n	%{develname}
Summary:	Development libraries and header files for ImageMagick app development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	ImageMagick-devel = %{version}-%{release}

%description -n	%{develname}
If you want to create applications that will use ImageMagick code or APIs,
you'll need to install these packages as well as ImageMagick. These additional
packages aren't necessary if you simply want to use ImageMagick, however.

ImageMagick-devel is an addition to ImageMagick which includes development
libraries and header files necessary to develop applications.

%package -n	perl-Image-Magick
Summary:	Libraries and modules for access to ImageMagick from perl
Group:		Development/Perl
Requires:	%{name} = %{version}
Requires:	graphviz
Requires:	libwmf

%description -n	perl-Image-Magick
This is the ImageMagick perl support package. It includes perl modules and
support files for access to ImageMagick library from perl.

%package	doc
Summary:	%{name} Documentation
Group:		Books/Other
BuildArch:	noarch

%description	doc
This package contains HTML/PDF documentation of %{name}.

%prep
%setup -q -n ImageMagick-%{rversion}-%minor_rev
%patch7 -p0 -b .urw
%patch17 -p0 -b .fpx
%patch19 -p1 -b .libpath
%patch20 -p0 -b .pkgconfig

bzcat %{SOURCE1} > ImageMagick.pdf
install -m 644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} .
libtoolize --copy --force; aclocal -I m4; autoconf; automake -a

%build
#gw the format-string patch is incomplete:
%define Werror_cflags %nil
export CFLAGS="%{optflags} -fno-strict-aliasing -fPIC"
export CXXFLAGS="%{optflags} -fno-strict-aliasing -fPIC"

# don't use icecream
export PATH=/bin:/usr/bin

%configure2_5x \
	--disable-static \
    --docdir=%{_defaultdocdir}/imagemagick \
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
    --with-modules \
    --with-perl \
    --with-perl-options="INSTALLDIRS=vendor CC='%{__cc} -L$PWD/magick/.libs' LDDLFLAGS='-shared -L$PWD/magick/.libs'" \
    --with-jp2 \
    --with-gvc \
    --with-lqr

# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

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
rm -rf %{buildroot}

# (Abel) set LD_RUN_PATH to null, to avoid adding rpath to perlmagick module
%makeinstall_std LD_RUN_PATH="" pkgdocdir=/installed_docs

# fix docs inclusion (fix an unknown new rpm bug)
rm -rf installed_docs; mv %{buildroot}/installed_docs .

# Remove unpackaged files
rm %buildroot%_libdir/*.la
rm -f %{buildroot}%{_libdir}/libltdl* 

# create compatible symlinks
ln -s libMagick++-%{major}.%{qlev}.so %{buildroot}%{_libdir}/libMagick++.so
ln -s libMagickCore-%{major}.%{qlev}.so %{buildroot}%{_libdir}/libMagickCore.so
ln -s libMagickWand-%{major}.%{qlev}.so %{buildroot}%{_libdir}/libMagickWand.so

%multiarch_binaries %{buildroot}%{_bindir}/Magick-config

%multiarch_binaries %{buildroot}%{_bindir}/Magick++-config

%multiarch_binaries %{buildroot}%{_bindir}/MagickCore-config

%multiarch_binaries %{buildroot}%{_bindir}/MagickWand-config

%multiarch_binaries %{buildroot}%{_bindir}/Wand-config

%multiarch_includes %{buildroot}%{_includedir}/ImageMagick/magick/magick-config.h

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
Categories=Graphics;Viewer;
EOF

%files
%doc README.txt
%doc %_docdir/ImageMagick-%rversion
%{_sysconfdir}/ImageMagick
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
%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/coders/*
%dir %{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters
%{_libdir}/ImageMagick-%{rversion}/modules-%{qlev}/filters/*
%{_libdir}/ImageMagick-%{rversion}/config-%{qlev}
%{_datadir}/ImageMagick-%{rversion}
%{_mandir}/man1/*
%{_mandir}/man3/*
%exclude %{_mandir}/man3/*::*.3pm*

%files desktop
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/64x64/apps/%{name}.png

%files -n %{libname}
%{_libdir}/libMagick++-%{major}.%{qlev}.so.*
%{_libdir}/libMagickCore-%{major}.%{qlev}.so.*
%{_libdir}/libMagickWand-%{major}.%{qlev}.so.*

%files -n %{develname}
%{_includedir}/ImageMagick
%{multiarch_bindir}/Magick-config
%{multiarch_bindir}/Magick++-config
%{multiarch_bindir}/MagickCore-config
%{multiarch_bindir}/MagickWand-config
%{multiarch_bindir}/Wand-config
%dir %{multiarch_includedir}/ImageMagick
%dir %{multiarch_includedir}/ImageMagick/magick
%{multiarch_includedir}/ImageMagick/magick/magick-config.h
%{_bindir}/Magick-config
%{_bindir}/Magick++-config
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_bindir}/Wand-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n perl-Image-Magick
%{perl_vendorarch}/Image
%{perl_vendorarch}/auto/Image
%{_mandir}/man3*/*::*.3pm*

%files doc
%doc ImageMagick.pdf ChangeLog LICENSE NEWS* NOTICE
%doc QuickStart.txt installed_docs/*




%changelog
* Mon May 21 2012 Bernhard Rosenkraenzer <bero@bero.eu> 6.7.7.0-1
+ Revision: 799744
- Update to 6.7.7-0

* Fri May 11 2012 Alexander Khrukin <akhrukin@mandriva.org> 6.7.6.9-2
+ Revision: 798264
- version update 6.7.6-9

* Fri Apr 27 2012 Bernhard Rosenkraenzer <bero@bero.eu> 6.7.6.7-2
+ Revision: 794146
- Don't remove libtool files that are actually needed

* Thu Apr 26 2012 Bernhard Rosenkraenzer <bero@bero.eu> 6.7.6.7-1
+ Revision: 793667
- Update to 6.7.6-7
- Re-enable module support, it's working again

* Wed Apr 04 2012 Götz Waschk <waschk@mandriva.org> 6.7.6.0-1
+ Revision: 789146
- update build deps
- update build deps
- readd obsoletes for backports

  + Bernhard Rosenkraenzer <bero@bero.eu>
    - Update to 6.7.6-0

* Sun Mar 04 2012 Bernhard Rosenkraenzer <bero@bero.eu> 6.7.5.9-1
+ Revision: 782106
- Update to 6.7.5-9

* Sun Feb 26 2012 Bernhard Rosenkraenzer <bero@bero.eu> 6.7.5.7-1
+ Revision: 780839
- Update to 6.7.5-7

* Sun Feb 05 2012 Alexander Khrukin <akhrukin@mandriva.org> 6.7.5.0-1
+ Revision: 771295
- version update 6.7.5

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 6.7.4.7-2
+ Revision: 765933
- rebuilt for perl-5.14.2

* Thu Jan 19 2012 Matthew Dawkins <mattydaw@mandriva.org> 6.7.4.7-1
+ Revision: 762407
- fix build
- adding new source
- new version 6.7.4-7
- cleaned up spec
- removed legacy provides and obsoletes

* Thu Dec 22 2011 Oden Eriksson <oeriksson@mandriva.com> 6.7.3.9-3
+ Revision: 744406
- rebuilt against libtiff.so.5

* Thu Dec 01 2011 Matthew Dawkins <mattydaw@mandriva.org> 6.7.3.9-2
+ Revision: 737085
- rename typo
- new version 6.7.3-9
- removed defattr, clean section, BuildRoot, mkrel
- removed old scriptlets
- removed .la files
- fixed devel desc & summary

* Mon Nov 21 2011 Andrey Bondrov <abondrov@mandriva.org> 6.7.3.7-1
+ Revision: 732121
- New version 6.7.3.7

* Mon Nov 07 2011 Andrey Bondrov <abondrov@mandriva.org> 6.7.3.4-1
+ Revision: 725140
- New version 6.7.3.4, new library major 5

* Fri Oct 21 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 6.7.3.1-1
+ Revision: 705613
- update to new version 6.7.3.1

* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 6.7.3.0-1
+ Revision: 704286
- update to new version 6.7.3.0

* Thu Sep 29 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 6.7.0.9-2
+ Revision: 702027
- rebuild for new libpng15

* Mon Jun 27 2011 Funda Wang <fwang@mandriva.org> 6.7.0.9-1
+ Revision: 687410
- new version 6.7.0-9

* Thu Jun 16 2011 Funda Wang <fwang@mandriva.org> 6.7.0.8-1
+ Revision: 685476
- new verison 6.7.0-8

* Wed Jun 15 2011 Funda Wang <fwang@mandriva.org> 6.7.0.7-1
+ Revision: 685227
- new version 6.7.0-7

* Fri Jun 10 2011 Funda Wang <fwang@mandriva.org> 6.7.0.6-1
+ Revision: 683813
- new version 6.7.0-6

* Tue Jun 07 2011 Funda Wang <fwang@mandriva.org> 6.7.0.4-1
+ Revision: 683027
- new version 6.7.0-4

* Sat Jun 04 2011 Funda Wang <fwang@mandriva.org> 6.7.0.3-1
+ Revision: 682699
- new version 6.7.0-3

* Fri May 27 2011 Funda Wang <fwang@mandriva.org> 6.7.0.2-1
+ Revision: 679321
- new verison 6.7.0-2

* Fri May 27 2011 Funda Wang <fwang@mandriva.org> 6.7.0.1-1
+ Revision: 679236
- new version 6.7.0-1

* Wed May 25 2011 Funda Wang <fwang@mandriva.org> 6.7.0.0-1
+ Revision: 678923
- new version 6.7.0-0

* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 6.6.9.10-1
+ Revision: 676970
- new version 6.6.9-10

* Mon May 16 2011 Funda Wang <fwang@mandriva.org> 6.6.9.9-1
+ Revision: 674986
- new version 6.6.9-9

* Wed May 11 2011 Funda Wang <fwang@mandriva.org> 6.6.9.8-2
+ Revision: 673595
- rebuild for new graphviz

* Fri May 06 2011 Funda Wang <fwang@mandriva.org> 6.6.9.8-1
+ Revision: 669918
- new version 6.6.9-8

* Sun May 01 2011 Funda Wang <fwang@mandriva.org> 6.6.9.7-1
+ Revision: 661295
- fix usage of multiarch
- new verison 6.6.9-7

* Fri Apr 15 2011 Funda Wang <fwang@mandriva.org> 6.6.9.5-1
+ Revision: 653205
- new version 6.6.9-5

* Sat Apr 02 2011 Funda Wang <fwang@mandriva.org> 6.6.9.3-1
+ Revision: 649774
- new version 6.6.9-3

* Thu Mar 31 2011 Funda Wang <fwang@mandriva.org> 6.6.9.1-1
+ Revision: 649354
- update file list
- new version 6.6.9-1
- new verison 6.6.8-10

* Sat Mar 26 2011 Funda Wang <fwang@mandriva.org> 6.6.8.8-1
+ Revision: 648579
- new version 6.6.8-8

* Fri Mar 25 2011 Funda Wang <fwang@mandriva.org> 6.6.8.7-1
+ Revision: 648449
- update file list
- new version 6.6.8-7

* Tue Mar 22 2011 Funda Wang <fwang@mandriva.org> 6.6.8.6-1
+ Revision: 647492
- update file list
- update file list
- new version 6.6.8-6

* Sat Mar 19 2011 Funda Wang <fwang@mandriva.org> 6.6.8.5-1
+ Revision: 646504
- new version 6.6.8-5

* Sun Mar 13 2011 Funda Wang <fwang@mandriva.org> 6.6.8.4-1
+ Revision: 644109
- new version 6.6.8-4

* Fri Mar 11 2011 Funda Wang <fwang@mandriva.org> 6.6.8.3-2
+ Revision: 643818
- new version 6.6.8-3

* Mon Mar 07 2011 Funda Wang <fwang@mandriva.org> 6.6.8.1-2
+ Revision: 642477
- do not build libgs support (bug#62727)

* Mon Mar 07 2011 Funda Wang <fwang@mandriva.org> 6.6.8.1-1
+ Revision: 642402
- new version 6.6.8-1

* Sun Mar 06 2011 Funda Wang <fwang@mandriva.org> 6.6.8.0-1
+ Revision: 642212
- new version 6.6.8

* Sat Feb 26 2011 Funda Wang <fwang@mandriva.org> 6.6.7.10-1
+ Revision: 639837
- New version 6.6.7-10

* Mon Feb 21 2011 Funda Wang <fwang@mandriva.org> 6.6.7.8-1
+ Revision: 639079
- New version 6.6.7-8

* Thu Feb 17 2011 Funda Wang <fwang@mandriva.org> 6.6.7.7-1
+ Revision: 638092
- new version 6.6.7-7

* Tue Feb 08 2011 Funda Wang <fwang@mandriva.org> 6.6.7.6-1
+ Revision: 636832
- New version 6.6.7-6

* Mon Feb 07 2011 Funda Wang <fwang@mandriva.org> 6.6.7.5-2
+ Revision: 636521
- tighten BR

* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 6.6.7.5-1
+ Revision: 636167
- new version 6.6.7-5

* Sun Jan 30 2011 Funda Wang <fwang@mandriva.org> 6.6.7.4-1
+ Revision: 634102
- new version 6.6.7-4

* Thu Jan 27 2011 Funda Wang <fwang@mandriva.org> 6.6.7.3-1
+ Revision: 633181
- new version 6.6.7-3

* Sun Jan 23 2011 Funda Wang <fwang@mandriva.org> 6.6.7.2-1
+ Revision: 632423
- new version 6.6.7-2

* Wed Jan 19 2011 Funda Wang <fwang@mandriva.org> 6.6.7.1-1
+ Revision: 631657
- new version 6.6.7-1
- 6.6.7-0

* Sun Jan 02 2011 Funda Wang <fwang@mandriva.org> 6.6.6.10-1mdv2011.0
+ Revision: 627494
- New version 6.6.6-10

* Sat Jan 01 2011 Funda Wang <fwang@mandriva.org> 6.6.6.9-1mdv2011.0
+ Revision: 626953
- new version 6.6.6-9

* Thu Dec 30 2010 Funda Wang <fwang@mandriva.org> 6.6.6.8-1mdv2011.0
+ Revision: 626269
- new version 6.6.6-8

* Sun Dec 26 2010 Funda Wang <fwang@mandriva.org> 6.6.6.7-1mdv2011.0
+ Revision: 625144
- new verison 6.6.6-7

* Mon Dec 20 2010 Funda Wang <fwang@mandriva.org> 6.6.6.6-1mdv2011.0
+ Revision: 623224
- new version 6.6.6-6

* Tue Dec 14 2010 Funda Wang <fwang@mandriva.org> 6.6.6.5-1mdv2011.0
+ Revision: 621734
- new version 6.6.6-5

* Sun Dec 05 2010 Funda Wang <fwang@mandriva.org> 6.6.6.3-1mdv2011.0
+ Revision: 609581
- new version 6.6.6-3

* Thu Dec 02 2010 Funda Wang <fwang@mandriva.org> 6.6.6.2-1mdv2011.0
+ Revision: 604665
- new version 6.6.6-2

* Mon Nov 29 2010 Funda Wang <fwang@mandriva.org> 6.6.6.1-1mdv2011.0
+ Revision: 602959
- new version 6.6.6-1

* Sun Nov 28 2010 Funda Wang <fwang@mandriva.org> 6.6.6.0-1mdv2011.0
+ Revision: 602173
- 6.6.6.0

* Tue Nov 23 2010 Funda Wang <fwang@mandriva.org> 6.6.5.10-1mdv2011.0
+ Revision: 599890
- new version 6.6.5-10

* Sun Nov 21 2010 Funda Wang <fwang@mandriva.org> 6.6.5.9-1mdv2011.0
+ Revision: 599328
- new version 6.6.5-9

* Fri Nov 12 2010 Funda Wang <fwang@mandriva.org> 6.6.5.8-1mdv2011.0
+ Revision: 596421
- new version 6.6.5-8
- new version 6.6.5-7

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 6.6.5.6-1mdv2011.0
+ Revision: 594128
- new version 6.6.5-6

* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 6.6.5.5-1mdv2011.0
+ Revision: 590736
- new version 6.6.5-5

* Tue Oct 26 2010 Funda Wang <fwang@mandriva.org> 6.6.5.4-1mdv2011.0
+ Revision: 589407
- new version 6.6.5-4

* Sun Oct 24 2010 Funda Wang <fwang@mandriva.org> 6.6.5.3-1mdv2011.0
+ Revision: 587901
- patch21 not needed anymore
- new version 6.6.5-3

* Fri Oct 22 2010 Funda Wang <fwang@mandriva.org> 6.6.5.2-1mdv2011.0
+ Revision: 587211
- new version 6.6.5-2

* Wed Oct 20 2010 Funda Wang <fwang@mandriva.org> 6.6.5.1-1mdv2011.0
+ Revision: 586868
- new version 6.6.5-1

* Thu Oct 14 2010 Funda Wang <fwang@mandriva.org> 6.6.5.0-1mdv2011.0
+ Revision: 585631
- new version 6.6.5-0

* Mon Oct 11 2010 Funda Wang <fwang@mandriva.org> 6.6.4.10-1mdv2011.0
+ Revision: 584868
- new version 6.6.4-10

* Wed Oct 06 2010 Funda Wang <fwang@mandriva.org> 6.6.4.9-1mdv2011.0
+ Revision: 583356
- new verson 6.6.4-9

* Fri Oct 01 2010 Funda Wang <fwang@mandriva.org> 6.6.4.8-1mdv2011.0
+ Revision: 582218
- fix build
- new version 6.6.4-8
- new version 6.6.4-7
- new version 6.6.4-6

* Wed Sep 22 2010 Funda Wang <fwang@mandriva.org> 6.6.4.5-1mdv2011.0
+ Revision: 580498
- new version 6.6.4-5

* Sun Sep 19 2010 Funda Wang <fwang@mandriva.org> 6.6.4.4-1mdv2011.0
+ Revision: 579763
- new version 6.6.4-4

* Sat Sep 18 2010 Funda Wang <fwang@mandriva.org> 6.6.4.3-1mdv2011.0
+ Revision: 579313
- new version 6.6.4-3

* Wed Sep 15 2010 Funda Wang <fwang@mandriva.org> 6.6.4.2-1mdv2011.0
+ Revision: 578520
- new version 6.6.4-2

* Mon Sep 13 2010 Funda Wang <fwang@mandriva.org> 6.6.4.1-1mdv2011.0
+ Revision: 577845
- new version 6.6.4-1

* Sun Sep 05 2010 Funda Wang <fwang@mandriva.org> 6.6.4.0-1mdv2011.0
+ Revision: 576059
- new version 6.6.4-0

* Wed Sep 01 2010 Funda Wang <fwang@mandriva.org> 6.6.3.10-1mdv2011.0
+ Revision: 574997
- new version 6.6.3-10

* Mon Aug 23 2010 Funda Wang <fwang@mandriva.org> 6.6.3.9-1mdv2011.0
+ Revision: 572099
- new version 6.6.3-9

* Sun Aug 22 2010 Funda Wang <fwang@mandriva.org> 6.6.3.8-1mdv2011.0
+ Revision: 571789
- new version 6.6.3-8

* Fri Aug 20 2010 Funda Wang <fwang@mandriva.org> 6.6.3.7-1mdv2011.0
+ Revision: 571403
- new version 6.6.3-7

* Sun Aug 15 2010 Funda Wang <fwang@mandriva.org> 6.6.3.6-1mdv2011.0
+ Revision: 569908
- new version 6.6.3-6

* Sat Aug 14 2010 Funda Wang <fwang@mandriva.org> 6.6.3.5-1mdv2011.0
+ Revision: 569514
- new version 6.6.3-5

* Sat Aug 07 2010 Funda Wang <fwang@mandriva.org> 6.6.3.3-1mdv2011.0
+ Revision: 567411
- patch22 merged upstream
- new version 6.6.3-3

* Mon Aug 02 2010 Funda Wang <fwang@mandriva.org> 6.6.3.2-1mdv2011.0
+ Revision: 564918
- Makefile should use tab instead space
- new version 6.6.3-2

* Wed Jul 28 2010 Funda Wang <fwang@mandriva.org> 6.6.3.1-1mdv2011.0
+ Revision: 562561
- new version 6.6.3-1

* Thu Jul 22 2010 Jérôme Quelin <jquelin@mandriva.org> 6.6.3.0-2mdv2011.0
+ Revision: 556777
- perl 5.12 rebuild

* Sat Jul 10 2010 Funda Wang <fwang@mandriva.org> 6.6.3.0-1mdv2011.0
+ Revision: 549961
- new libmajor
- New version 6.6.3-0

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 6.6.1.5-2mdv2010.1
+ Revision: 540029
- rebuild so that shared libraries are properly stripped again

* Sat Apr 24 2010 Funda Wang <fwang@mandriva.org> 6.6.1.5-1mdv2010.1
+ Revision: 538410
- new version 6.6.1-5

* Sun Apr 18 2010 Funda Wang <fwang@mandriva.org> 6.6.1.4-1mdv2010.1
+ Revision: 536084
- new version 6.6.1-4

* Mon Apr 12 2010 Funda Wang <fwang@mandriva.org> 6.6.1.2-1mdv2010.1
+ Revision: 533694
- new version 6.6.1-2

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 6.6.1.1-1mdv2010.1
+ Revision: 533313
- new version 6.6.1-1

* Mon Apr 05 2010 Funda Wang <fwang@mandriva.org> 6.6.1.0-1mdv2010.1
+ Revision: 531523
- new version 6.6.1-0

* Sat Mar 27 2010 Funda Wang <fwang@mandriva.org> 6.6.0.10-1mdv2010.1
+ Revision: 527890
- new version 6.6.0-10

* Thu Mar 25 2010 Funda Wang <fwang@mandriva.org> 6.6.0.9-1mdv2010.1
+ Revision: 527326
- new version 6.6.0-9

* Sun Mar 21 2010 Funda Wang <fwang@mandriva.org> 6.6.0.8-1mdv2010.1
+ Revision: 525949
- new version 6.6.0-8

* Fri Mar 19 2010 Funda Wang <fwang@mandriva.org> 6.6.0.7-1mdv2010.1
+ Revision: 525188
- new version 6.6.0-7

* Wed Mar 17 2010 Funda Wang <fwang@mandriva.org> 6.6.0.6-1mdv2010.1
+ Revision: 522676
- new version 6.6.0-6

* Sat Mar 13 2010 Funda Wang <fwang@mandriva.org> 6.6.0.5-1mdv2010.1
+ Revision: 518642
- new version 6.6.0-5

* Tue Mar 09 2010 Funda Wang <fwang@mandriva.org> 6.6.0.4-1mdv2010.1
+ Revision: 516824
- new version 6.6.0-4

* Sun Mar 07 2010 Funda Wang <fwang@mandriva.org> 6.6.0.3-1mdv2010.1
+ Revision: 515318
- new version 6.6.0-3

* Sat Mar 06 2010 Funda Wang <fwang@mandriva.org> 6.6.0.2-1mdv2010.1
+ Revision: 514913
- new version 6.6.0-2

* Fri Mar 05 2010 Funda Wang <fwang@mandriva.org> 6.6.0.1-1mdv2010.1
+ Revision: 514380
- New version 6.6.0-1

* Sat Feb 27 2010 Funda Wang <fwang@mandriva.org> 6.6.0.0-1mdv2010.1
+ Revision: 512186
- new version 6.6.0.0

* Tue Feb 23 2010 Funda Wang <fwang@mandriva.org> 6.5.9.10-1mdv2010.1
+ Revision: 509886
- new version 6.5.9-10

* Sun Feb 21 2010 Funda Wang <fwang@mandriva.org> 6.5.9.9-1mdv2010.1
+ Revision: 508916
- new version 6.5.9-9

* Fri Feb 19 2010 Funda Wang <fwang@mandriva.org> 6.5.9.8-1mdv2010.1
+ Revision: 507963
- new version 6.5.9-8

* Thu Feb 18 2010 Funda Wang <fwang@mandriva.org> 6.5.9.7-1mdv2010.1
+ Revision: 507367
- new version 6.5.9-7

* Tue Feb 16 2010 Funda Wang <fwang@mandriva.org> 6.5.9.6-1mdv2010.1
+ Revision: 506599
- new version 6.5.9-6

* Sun Feb 14 2010 Funda Wang <fwang@mandriva.org> 6.5.9.5-1mdv2010.1
+ Revision: 505850
- new version 6.5.9-5

* Sat Feb 13 2010 Funda Wang <fwang@mandriva.org> 6.5.9.4-1mdv2010.1
+ Revision: 505507
- new version 5.6.9-4

* Mon Feb 08 2010 Funda Wang <fwang@mandriva.org> 6.5.9.3-1mdv2010.1
+ Revision: 502221
- New version 6.5.9-3

* Sat Feb 06 2010 Funda Wang <fwang@mandriva.org> 6.5.9.2-1mdv2010.1
+ Revision: 501277
- New version 6.5.9-2

* Tue Feb 02 2010 Funda Wang <fwang@mandriva.org> 6.5.9.1-1mdv2010.1
+ Revision: 499422
- new version 6.5.9-1

* Thu Jan 14 2010 Funda Wang <fwang@mandriva.org> 6.5.9.0-1mdv2010.1
+ Revision: 491130
- bump libmajor
- New version 6.5.9-0

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 6.5.8.10-2mdv2010.1
+ Revision: 488767
- rebuilt against libjpeg v8

* Fri Jan 01 2010 Funda Wang <fwang@mandriva.org> 6.5.8.10-1mdv2010.1
+ Revision: 484800
- new version 6.5.8-10

* Tue Dec 29 2009 Funda Wang <fwang@mandriva.org> 6.5.8.9-1mdv2010.1
+ Revision: 483212
- new version 6.5.8-9

* Fri Dec 25 2009 Funda Wang <fwang@mandriva.org> 6.5.8.8-1mdv2010.1
+ Revision: 482220
- new version 6.5.8-8

* Thu Dec 17 2009 Funda Wang <fwang@mandriva.org> 6.5.8.6-1mdv2010.1
+ Revision: 479766
- new version 6.5.8-6

* Sat Dec 12 2009 Funda Wang <fwang@mandriva.org> 6.5.8.5-1mdv2010.1
+ Revision: 477604
- new version 6.5.8-5

* Mon Dec 07 2009 Funda Wang <fwang@mandriva.org> 6.5.8.4-1mdv2010.1
+ Revision: 474334
- new version 6.5.8-4

* Sun Dec 06 2009 Funda Wang <fwang@mandriva.org> 6.5.8.3-1mdv2010.1
+ Revision: 474213
- new version 6.5.8.3

* Mon Nov 16 2009 Eugeni Dodonov <eugeni@mandriva.com> 6.5.7.7-1mdv2010.1
+ Revision: 466653
- Updated to 6.5.7.7.

* Thu Oct 22 2009 Eugeni Dodonov <eugeni@mandriva.com> 6.5.7.0-1mdv2010.0
+ Revision: 458947
- New version: 6.5.7.0

* Fri Sep 25 2009 Olivier Blin <blino@mandriva.org> 6.5.4.9-3mdv2010.0
+ Revision: 449104
- allow to bootstrap build by breaking buildloop imagemagick<>djvulibre
  (from Arnaud Patard)

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 6.5.4.9-2mdv2010.0
+ Revision: 416520
- rebuilt against libjpeg v7

* Sat Aug 08 2009 Funda Wang <fwang@mandriva.org> 6.5.4.9-1mdv2010.0
+ Revision: 411562
- new version 6.5.4-9

* Wed Aug 05 2009 Funda Wang <fwang@mandriva.org> 6.5.4.8-1mdv2010.0
+ Revision: 409926
- new version 6.5.4-8

* Sun Jul 26 2009 Funda Wang <fwang@mandriva.org> 6.5.4.5-1mdv2010.0
+ Revision: 400056
- New version 6.5.4-5

* Fri Jul 03 2009 Funda Wang <fwang@mandriva.org> 6.5.4.2-1mdv2010.0
+ Revision: 391882
- New version 6.5.4-2

* Sun Jun 28 2009 Funda Wang <fwang@mandriva.org> 6.5.4.0-1mdv2010.0
+ Revision: 390144
- New version 6.5.4-0

* Tue Jun 09 2009 Funda Wang <fwang@mandriva.org> 6.5.2.10-1mdv2010.0
+ Revision: 384212
- New version 6.5.2.10

* Thu May 28 2009 Eugeni Dodonov <eugeni@mandriva.com> 6.5.2.9-1mdv2010.0
+ Revision: 380390
- Updated to 6.5.2.9.

* Tue May 26 2009 Eugeni Dodonov <eugeni@mandriva.com> 6.5.2.8-1mdv2010.0
+ Revision: 379915
- Updated to 6.5.2.8.

* Fri Mar 20 2009 Eugeni Dodonov <eugeni@mandriva.com> 6.5.0.2-1mdv2009.1
+ Revision: 359219
- Updated to latest upstream release.
  Updated to use correct docdir in man pages (#46104).
  Added correct BuildConflicts.

* Thu Mar 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 6.4.8.9-3mdv2009.1
+ Revision: 358191
- rebuild for latest graphviz

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 6.4.8.9-2mdv2009.1
+ Revision: 335843
- rebuilt against new jbigkit major

  + Götz Waschk <waschk@mandriva.org>
    - back to autoconf 2.5

* Wed Jan 28 2009 Götz Waschk <waschk@mandriva.org> 6.4.8.9-1mdv2009.1
+ Revision: 334964
- new version
- new major
- rediff patches 0,4,20
- patch format-string errors
- disable Werror, the perl binding does not work
- use the right configure macro

* Thu Nov 06 2008 Adam Williamson <awilliamson@mandriva.org> 6.4.5.4-1mdv2009.1
+ Revision: 300369
- rebuild for libxcb changes
- drop mgk.patch (merged upstream)
- new release 6.4.5-4

* Mon Sep 15 2008 Oden Eriksson <oeriksson@mandriva.com> 6.4.2.10-5mdv2009.0
+ Revision: 284863
- move suggests into the description (pixel)

* Fri Sep 12 2008 Oden Eriksson <oeriksson@mandriva.com> 6.4.2.10-4mdv2009.0
+ Revision: 284083
- turn delegate programs into suggests, fixes #40199

* Sun Sep 07 2008 Frederik Himpe <fhimpe@mandriva.org> 6.4.2.10-3mdv2009.0
+ Revision: 282371
- Rebuild for new djvulibre

* Tue Aug 19 2008 Adam Williamson <awilliamson@mandriva.org> 6.4.2.10-2mdv2009.0
+ Revision: 274053
- whoops, fix patch
- correct license
- add mgk.patch: fixes a small upstream error in configure

* Tue Aug 19 2008 Adam Williamson <awilliamson@mandriva.org> 6.4.2.10-1mdv2009.0
+ Revision: 274008
- rediff libpath.diff (part has been merged upstream)
- drop mpeg2.patch (superseded upstream)
- new release 6.4.2-10 (includes full replacement of mpeg2 tools with ffmpeg)

* Sat Aug 09 2008 Adam Williamson <awilliamson@mandriva.org> 6.4.2.6-1mdv2009.0
+ Revision: 270081
- add mpeg2.patch (from upstream svn, use ffmpeg in place of mpeg2decode)
- drop djvulibre_fix.diff (it wasn't actually fixing anything any more, just
  unnecessarily renaming options)
- new release 6.4.2-6

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 6.4.2.4-1mdv2009.0
+ Revision: 238905
- 6.4.2-4
- fix linkage against djvulibre (P1)
- fix ugly internal linkage (P21)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 16 2008 Oden Eriksson <oeriksson@mandriva.com> 6.4.1.1-1mdv2009.0
+ Revision: 208235
- disable the test suite for now
- second build attempt (duh!!!)
- 6.4.1-1
- nuke rpath (looked at fedora)

* Fri Apr 25 2008 Oden Eriksson <oeriksson@mandriva.com> 6.4.0.9-0mdv2009.0
+ Revision: 197411
- 6.4.0-9

* Tue Feb 19 2008 Oden Eriksson <oeriksson@mandriva.com> 6.3.8.9-1mdv2008.1
+ Revision: 172929
- 6.3.8-9

* Sat Feb 09 2008 Anssi Hannula <anssi@mandriva.org> 6.3.8.5-1mdv2008.1
+ Revision: 164617
- add %%minor_rev to %%version, it is not so minor (even libs were renamed
  with only it being raised)

* Sat Feb 09 2008 Anssi Hannula <anssi@mandriva.org> 6.3.8-2mdv2008.1
+ Revision: 164569
- drop library major check from prep (major is not supposed to be
  LIBRARY_CURRENT.LIBRARY_REVISION.LIBRARY_AGE, rather
  LIBRARY_CURRENT - LIBRARY_AGE; if upstream assumes something
  else, a proper fix is needed to avoid breakage in upgrade)
- rename library package to reflect correct major
- simplify file list
- own some unowned directories
- ensure major correctness

* Fri Feb 08 2008 Oden Eriksson <oeriksson@mandriva.com> 6.3.8-1mdv2008.1
+ Revision: 164215
- trying "make -j1" again...
- fix the multiarch stuff
- 6.3.8-5
- it cannot utilize %%make on x86_64, so just don't use that...
- bump release
- can't link against umem due to licensing issues
- added umem support
- 6.3.8-3
- dropped the libname patch, it's useless
- fixed deps
- added lqr support (experimental)

* Mon Jan 14 2008 Pixel <pixel@mandriva.com> 6.3.7-3mdv2008.1
+ Revision: 151250
- rebuild for perl-5.10.0

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

* Tue Jan 08 2008 Oden Eriksson <oeriksson@mandriva.com> 6.3.7-2mdv2008.1
+ Revision: 146681
- really fix it
- --with-modules is borked, use --without-modules
- 6.3.7-9

* Fri Jan 04 2008 Oden Eriksson <oeriksson@mandriva.com> 6.3.7-1mdv2008.1
+ Revision: 144861
- 6.3.7-8
- major spec file rework
- fix deps
- repatched needed patches
- dropped obsolete patches
- fix #27044 (convert needs html2ps to convert HTML to PostScript)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - buildrequires X11-devel instead of XFree86-devel

* Wed Sep 26 2007 Andreas Hasenack <andreas@mandriva.com> 6.3.2.9-10mdv2008.0
+ Revision: 93085
- fixed (lib)djvulibre-devel buildrequires
- fix build because of wrong font path (#34054)
- added security patch for CVE-2007-1667_1797 (#31911)

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Fri May 04 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.3.2.9-8mdv2008.0
+ Revision: 22582
- Revert bogus Obsoletes+major change from previous commit.

* Fri May 04 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 6.3.2.9-7mdv2008.0
+ Revision: 22554
- Rebuild with new jasper.
- Don't use major define on obsoletes because it can be modified making
  room for potential future errors (user changing major without noticing
  it has to change Obsoletes too).

* Sat Apr 21 2007 Anssi Hannula <anssi@mandriva.org> 6.3.2.9-6mdv2008.0
+ Revision: 16613
- rename to imagemagick
- move Imagemagick package tree to imagemagick


* Sun Mar 11 2007 Giuseppe Ghibò <ghibo@mandriva.com> 6.3.2.9-5mdv2007.1
+ Revision: 141362
- Added desktop subpackage and menu (fix bug #29331). "display" won't start without xterm (KDE bug?).

* Tue Mar 06 2007 Giuseppe Ghibò <ghibo@mandriva.com> 6.3.2.9-4mdv2007.1
+ Revision: 133476
- Fixed conflict in man pages between main and perl package (thanks to Pixel).

  + Anssi Hannula <anssi@mandriva.org>
    - remove unused options and fix description

* Sun Mar 04 2007 Anssi Hannula <anssi@mandriva.org> 6.3.2.9-3mdv2007.1
+ Revision: 132189
- plf: disable fpx build (broken)

* Thu Mar 01 2007 Giuseppe Ghibò <ghibo@mandriva.com> 6.3.2.9-2mdv2007.1
+ Revision: 130660
- Rebuilt.

* Sat Feb 24 2007 Giuseppe Ghibò <ghibo@mandriva.com> 6.3.2.9-1mdv2007.1
+ Revision: 125369
- Release: 6.3.2-9.

* Tue Feb 20 2007 Giuseppe Ghibò <ghibo@mandriva.com> 6.3.2.8-1mdv2007.1
+ Revision: 122953
- Release: 6.3.2-8.

* Fri Feb 16 2007 Götz Waschk <waschk@mandriva.org> 6.3.2.5-2mdv2007.1
+ Revision: 121898
- add djvulibre support
- fix description

* Fri Feb 16 2007 Götz Waschk <waschk@mandriva.org> 6.3.2.5-1mdv2007.1
+ Revision: 121701
- new version
- new major
- drop patches 1, 21
- rediff patch 17
- fix patch 7, it was producing invalid xml in a font configuration file

  + Giuseppe Ghibò <ghibo@mandriva.com>
    - Release: 6.2.9-8.
    - Removed Patch10 (no longer needed).
    - Rebuilt Patch19.
    - Merged Patch21 from Stew Benetict (security fix for CVE-2006-5456).
    - Import ImageMagick

* Thu Aug 31 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.9.2-1mdv2007.0
- Release: 6.2.9-2 (also fixes CVE-2006-3743,3744,4144).
- Bumped lib %%major to 10.4.0.

* Tue Aug 22 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.8.8-1mdv2007.0
- Release: 6.2.8-8.

* Thu Aug 03 2006 G�tz Waschk <waschk@mandriva.org> 6.2.8.7-1mdv2007.0
- new version

* Wed Aug 02 2006 Frederic Crozat <fcrozat@mandriva.com> 6.2.8.4-2mdv2007.0
- Rebuild with latest dbus

* Wed Jul 19 2006 G�tz Waschk <waschk@mandriva.org> 6.2.8.4-1mdv2007.0
- new release

* Tue Jul 04 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.8.3-1mdv2007.0
- Release: 6.2.8-3.

* Mon Jul 03 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.8.2-1mdv2007.0
- Release: 6.2.8-2.

* Fri Jun 30 2006 G�tz Waschk <waschk@mandriva.org> 6.2.8.1-1mdv2007.0
- fix doc patch again
- update file list
- new version

* Mon Jun 19 2006 Stefan van der Eijk <stefan@eijk.nu.lurtspam> 6.2.8-1mdv2007.0
- rebuild for png

* Fri Jun 09 2006 G�tz Waschk <waschk@mandriva.org> 6.2.8-1mdv2007.0
- new major
- new version

* Wed Apr 19 2006 G�tz Waschk <waschk@mandriva.org> 6.2.7-1mdk
- move tests to %%check
- drop patch 12
- disable graphviz for now (needs 2.9 development snapshot)
- update deps
- fix doc location
- update patch 8,17
- new version

* Wed Apr 05 2006 G�tz Waschk <waschk@mandriva.org> 6.2.6.8-1mdk
- new version

* Fri Mar 31 2006 G�tz Waschk <waschk@mandriva.org> 6.2.6.7-1mdk
- New release 6.2.6.7

* Wed Mar 29 2006 G�tz Waschk <waschk@mandriva.org> 6.2.6.4-4mdk
- fix devel exceptions for graphviz

* Fri Mar 24 2006 G�tz Waschk <waschk@mandriva.org> 6.2.6.4-3mdk
- rebuild for graphviz

* Wed Mar 15 2006 G�tz Waschk <waschk@mandriva.org> 6.2.6.4-2mdk
- spec fixes

* Mon Mar 13 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.6.4-1mdk
- 6.2.6-4.
- Rebuilt Patch8.

* Tue Feb 28 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.6.2-1mdk
- 6.2.6-2.

* Mon Jan 30 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.6.1-2mdk
- Bump major to 10.1.0.

* Mon Jan 30 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.6.1-1mdk
- 6.2.6-1.
- Rebuilt Patch10.
- Bump major to 10.0.0.

* Fri Jan 20 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.2.5.5-4mdk
- patch20: fix bug detected by montageImages test case on ppc

* Tue Jan 03 2006 Giuseppe Ghib� <ghibo@mandriva.com> 6.2.5.5-3mdk
- fix major: should be derived from LIBRARY_CURRENT|REVISION|AGE.

* Sat Dec 31 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 6.2.5.5-2mdk
- fix major

* Fri Dec 23 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 6.2.5.5-1mdk
- 6.2.5-5
- regenerate P10
- convert to utf-8

* Tue Aug 30 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.4.3-1mdk
- Release: 6.2.4.3.

* Fri Aug 26 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.4.2-2mdk
- Removed type-windows.xml from type.xml (bug #10193).

* Thu Aug 25 2005 Oden Eriksson <oeriksson@mandriva.com> 6.2.4.2-1mdk
- 6.2.4-2
- nuke rpath
- new major

* Sun Aug 14 2005 GÃ¶tz Waschk <waschk@mandriva.org> 6.2.3.6-3mdk
- rebuild for new xorg

* Sat Aug 06 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.3.6-2mdk
- Rebuilt Patch8.

* Sat Aug 06 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.3.6-1mdk
- Release: 6.2.3-6.

* Fri Jul 22 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.3.4-1mdk
- Release: 6.2.3-4.

* Sun Jul 10 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.3.3-1mdk
- Release: 6.2.3-3.

* Sat Jun 25 2005 Giuseppe Ghibò <ghibo@mandriva.com> 6.2.3.2-1mdk
- Release: 6.2.3-2.
- Removed Patch20 (alphachannel), merged upstream.
- Rebuilt Patch10 (textfontsize).

* Thu Mar 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 6.2.0.3-8mdk
- fix #15097

* Sun Mar 20 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.2.0.3-7mdk
- add BuildRequires: libgd-devel

* Sat Mar 19 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.2.0.3-6mdk
- Rebuilt against latest jbigkit.

* Wed Mar 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 6.2.0.3-5mdk
- Rebuilt against fixed graphwiz libs

* Wed Mar 16 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.2.0.3-4mdk
- Backported patch from 6.2.0-8, for fixing wrong returned alpha channel when
  image don't have one.

* Thu Mar 10 2005 Pixel <pixel@mandrakesoft.com> 6.2.0.3-3mdk
- ensure "make -j 4" doesn't cause "perl Makefile.PL" to discard libMagick
  this fixes perl-Image-Magick which segfaulted because it was not linked with -lMagick.
- drop buggy patch14
  (the bugginess of patch14 comes from 5.5.7.15-3mdk)

* Wed Mar 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 6.2.0.3-2mdk
- fix the make test stuff with a twist

* Mon Feb 28 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.2.0.3-1mdk
- Release: 6.2.0-3.
- Disabled tests (problem with perl).

* Tue Feb 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 6.1.9.4-2mdk
- fix linking in the perl stuff (PLD)
- enable graphviz support
- run the tests (except x as it requires hands on)

* Mon Jan 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 6.1.9.4-1mdk
- fix deps and conditional %%multiarch.
- Release: 6.1.9-4.

* Sat Jan 22 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.9.2-1mdk
- Release: 6.1.9-2.

* Tue Jan 18 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.8.9-1mdk
- Release: 6.1.8-9.

* Sun Jan 16 2005 Guillaume Rousse <guillomovitch@mandrake.org> 6.1.8.7-3plf 
- fix perl module linkage
- use automake 1.8

* Sun Jan 16 2005 Luca Berra <bluca@vodka.it> 6.1.8.7-2mdk
- include parent directories in %%files

* Sat Jan 15 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.8.7-1mdk
- Release 6.8.1-7.

* Tue Jan 11 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.8.3-1mdk
- Release 6.8.1-3.

* Tue Jan 11 2005 Guillaume Rousse <guillomovitch@mandrake.org> 6.1.8.1-2mdk
- rebuild to have proper perl module linking (it still fails sometimes for unknwon reasons)
- perl package is perl-Image-Magick

* Sat Jan 08 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.8.1-1mdk
- Release 6.1.8-1.

* Thu Jan 06 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.7.6-1mdk
- Release 6.1.7-6.
- Rebuilt Patch7.
- Rebuilt Patch14.
- Added Patch18 (bug #10093).
- Jasper is in main, so use it.

* Tue Dec 28 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.7.5-1mdk
- Merged Charles A Edwards changes:
  - Release 6.1.7-5.
  - rm libltdl* files.

* Mon Dec 27 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.1.7.4-1mdk
- Removed Patch18 (merged upstream).
- Rebuilt Patch8.

* Sat Nov 27 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.4-8mdk
- security fix for CAN-2004-0981 (Vincent Danen).

* Wed Nov 24 2004 Götz Waschk <waschk@linux-mandrake.com> 6.0.4.4-7mdk
- enable jasper, it's in main

* Tue Nov 23 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 6.0.4.4-6mdk
- Rebuild for new perl

* Sat Oct 09 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.4-5mdk
- Added Patch21, to fix security problems, CAN-2004-0827.

* Tue Sep 28 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.4-4mdk
- Added Patch20, to fix antialias problem during PS converting
  with ghostscript delegate (bug #11765).

* Sun Sep 12 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.4-3mdk
- Added Patch19, to fix grab button problem (bug #11207).

* Sun Sep 12 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.4-2mdk
- Added Patch18, to move windows font path later in type.mgk
  (fixes bug #10193).

* Tue Aug 17 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.4-1mdk
- Release: 6.0.4-4.

* Fri Aug 13 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.3-1mdk
- Release: 6.0.4-3.

* Fri Aug 06 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.2-1mdk
- Release: 6.0.4-2.
- Added -fPIC and --with-pic to have ImageMagick libraries working 
  with prelink (Thierry).

* Mon Aug 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 6.0.4.1-2mdk
- rebuilt to fix invalid vendor and distribution
- misc spec file fixes

* Thu Jul 29 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.4.1-1mdk
- Release: 6.0.4-1.

* Tue Jul 27 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.3.5-1mdk
- Release: 6.0.3-5.

* Tue Jul 20 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.3.3-1mdk
- Release: 6.0.3-3.
- Removed Patch15 (browser), merged upstream.

* Fri Jun 25 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.2.7-1mdk
- Release: 6.0.2-7.

* Sun Jun 13 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.2.6-1mdk
- Release: 6.0.2-6.

* Sat Jun 05 2004 Laurent Montel <lmontel@mandrakesoft.com> 6.0.1.4-2mdk
- Rebuild

* Tue Jun 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 6.0.1.4-1mdk
- Release: 6.0.1-4.
- Removed Patch11, merged upstream.
- Rebuilt Patch4, Patch7, Patch8, Patch14, Patch17.
- Force enable-lzw=no (probably up to 7 July 2004, when LZW patents
  will expire in Canada too).

* Tue Jun 01 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 5.5.7.20-1mdk
- Revision: 5.5.7-20.
- Updated Patch12.

* Thu Apr 08 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 5.5.7.17-2mdk
- Merged Götz patches from 5.5.7.15-6mdk.

* Sun Apr 04 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 5.5.7.17-1mdk
- Revision: 5.5.7-17.
- Removed Patch16 for freetype2 (no longer needed).

