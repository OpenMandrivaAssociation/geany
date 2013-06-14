#for educational needs
%define edm	1

Summary:	Small C editor using GTK2
Name: 		geany
Version: 	1.23
Release: 	1
License: 	GPLv2+
Group: 		Development/C
URL: 		http://geany.uvena.de/
Source0: 	http://download.geany.org/%{name}-%{version}.tar.bz2
# The following tags files were retrieved 17 Aug 2009
Source1:	http://download.geany.org/contrib/tags/sqlite3.c.tags
Source2:	http://download.geany.org/contrib/tags/std.glsl.tags
Source3:	http://download.geany.org/contrib/tags/gtk216.c.tags
Source4:	http://download.geany.org/contrib/tags/xfce46.c.tags
Source5:	http://download.geany.org/contrib/tags/dbus-glib-0.76.c.tags
Source6:	http://download.geany.org/contrib/tags/geany-api-0.18.c.tags
Source7:	http://download.geany.org/contrib/tags/standard.css.tags
Source8:	http://download.geany.org/contrib/tags/std.vala.tags
# Russian help source. You may create another similar file for you language
Source9: 	index.html
Source10: 	images.tar.bz2
# Replace default setup for FreeBasic on MS QB compatable and complex Haskell 
# on simple Hugs98
Patch0:		001_geany_qb_fb.patch
Patch1:		002_geany_hugs98.patch
# Russian doc patch
Patch2:		ru_doc.patch
# Patch3:		ru_compile_typo.patch
Patch4:		geany-1.23-rosaconf.patch

BuildRequires:  desktop-file-utils
BuildRequires:  imagemagick
BuildRequires:  intltool
BuildRequires:	lxterminal
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig(gtk+-2.0)

Suggests:	geany-plugins

%description
Geany is a small C editor using GTK2 with basic features of an
integrated development environment. It features syntax highlighting,
code completion, call tips, many supported filetypes (including C,
Java, PHP, HTML, DocBook, Perl, LateX, and Bash), and symbol lists.

%package devel
Summary:	Header files for building Geany plug-ins
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files and pkg-config file needed for
building Geany plug-ins. You do not need to install this package

%prep
%setup -q
# For future reason add edm distepoch  You may recreate packets set edm to 0
%if %{edm}
%patch0 -p0
%patch1 -p0
%endif
%patch2 -p1
# %patch3 -p0
%patch4 -p1

%build
%configure2_5x
%make LIBS='-lgmodule-2.0'

%install
%makeinstall
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

#Fix for Russian
sed 's/Name\[ru\]=Geany/Name\[ru\]=Среда разработки Geany/g' -i %{buildroot}%{_datadir}/applications/geany.desktop
mkdir -p  %{buildroot}%{_defaultdocdir}/%{name}/html/ru/
install -Dpm 0644 %{SOURCE9} %{buildroot}%{_defaultdocdir}/%{name}/html/ru/
tar -xjvf %SOURCE10
mv images %{buildroot}%{_defaultdocdir}/%{name}/html/ru/

# research locale file
%find_lang %{name}

# prepare menu
# we remove the key "Version" and "Encoding" because it's invalid
desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="GNOME" \
	--remove-key="Version" \
	--remove-key="Encoding" \
	--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Install tags files
install -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{buildroot}%{_datadir}/%{name}

# remove useless file
rm -f %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache
rm -f %{buildroot}%{_datadir}/icons/Tango/icon-theme.cache

%files -f %{name}.lang
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_defaultdocdir}/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/hicolor/*/actions/*
%{_iconsdir}/Tango/*/actions/*
%{_mandir}/man1/%{name}.*

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc



%changelog
* Thu Apr 26 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.20-8
+ Revision: 793483
- split out devel pkg
- rebuild to clean up pkgconfig reqs
- cleaned up spec

* Thu Oct 13 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-7
+ Revision: 704560
- add lxterminal as default terminal for geany. Avoid not works from KDE4

* Sun Sep 04 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-6
+ Revision: 698204
- drop lxterminal from requires. Set default terminal to automate xvt script

* Thu Aug 18 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-5
+ Revision: 695122
- Add patch for new default conf:
    replace xterm for lxterminal
    replace default font Sans on Droid Sans
    replace Monospace on Droid Sans Monospace

* Tue Aug 02 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-4
+ Revision: 692717
- fix compile error due non-latin programm name

* Mon May 30 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-3
+ Revision: 681773
- aplly for default patch FreeBasic and Hascell/Hugs98

* Sun May 29 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-2
+ Revision: 681731
- add locale update

* Sun Jan 09 2011 Александр Казанцев <kazancas@mandriva.org> 0.20-1
+ Revision: 630810
- new version 0.20

* Sat Dec 25 2010 Funda Wang <fwang@mandriva.org> 0.19.2-1mdv2011.0
+ Revision: 624789
- update to new version 0.19.2

* Tue Aug 31 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.19.1-1mdv2011.0
+ Revision: 574916
- update to 0.19.1

* Sun Aug 01 2010 trem <trem@mandriva.org> 0.19-1mdv2011.0
+ Revision: 564855
- update to 0.19

* Sun Feb 14 2010 Funda Wang <fwang@mandriva.org> 0.18.1-1mdv2010.1
+ Revision: 505926
- drop dup files declaration
- update to new version 0.18.1

* Mon Aug 17 2009 Frederik Himpe <fhimpe@mandriva.org> 0.18-1mdv2010.0
+ Revision: 417201
- Update to new version 0.18
- Update tag files
- Don't do custom installation of icons, make install now takes care of
  installing them in fdo icon directories

* Sun May 03 2009 Frederik Himpe <fhimpe@mandriva.org> 0.17-1mdv2010.0
+ Revision: 370910
- Update to new version 0.17
- Fix license
- Fix source URL
- Package contrib tags files

* Sun Feb 15 2009 trem <trem@mandriva.org> 0.16-1mdv2009.1
+ Revision: 340646
- update to 0.16

* Sun Jan 04 2009 Jérôme Soyer <saispo@mandriva.org> 0.15-1mdv2009.1
+ Revision: 324737
- Fix BR
- New upstream release

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat Apr 19 2008 trem <trem@mandriva.org> 0.14-1mdv2009.0
+ Revision: 195799
- update to 0.14

  + Thierry Vignaud <tv@mandriva.org>
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Tue Feb 05 2008 trem <trem@mandriva.org> 0.13-1mdv2008.1
+ Revision: 162874
- update to 0.13

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Oct 14 2007 trem <trem@mandriva.org> 0.12-2mdv2008.1
+ Revision: 98282
- new packaging revision
- remove macro _icons16dir

* Sun Oct 14 2007 Funda Wang <fwang@mandriva.org> 0.12-1mdv2008.1
+ Revision: 98274
- add missing icons
- fix desktop entry and icons

  + trem <trem@mandriva.org>
    - remove unkown macro iconsbasedir
    - add BuildRequires perl-XML-Parser
    - update to 0.12

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'
    - fix man pages

* Mon May 21 2007 trem <trem@mandriva.org> 0.11-1mdv2008.0
+ Revision: 29521
- new release 0.11


* Wed Feb 28 2007 Jérôme Soyer <saispo@mandriva.org> 0.10.2-1mdv2007.0
+ Revision: 127084
- New release 0.10.2

* Sat Dec 23 2006 trem <trem@mandriva.org> 0.10-1mdv2007.1
+ Revision: 101854
- Add buildrequires ImageMagick
- Add buildrequires desktop-file-utils
- Add buildrequires gtk2-devel
- Add buildrequires pkgconfig
- 0.10
- Import geany

* Fri Aug 11 2006 trem <trem@mandriva.org> 0.8-1mdv2007.0
- 0.8

* Thu Jul 20 2006 trem <trem@mandriva.org> 0.7.1-1mdv2007.0
- 0.7.1
- add Patch0 to fix a double free
- switch to XDG menu

* Mon Jun 05 2006 trem <trem@mandriva.org> 0.7-1mdv2007.0
- 0.7

* Mon May 01 2006 trem <trem@mandriva.org> 0.6-2mdk
- fix packager name in changelog

* Mon May 01 2006 <trem@mandriva.org> 0.6-1mdk
- Initial build.

