#for educational needs
%define edm	1

Summary:	Small C editor using GTK2
Name: 		geany
Version: 	0.20
Release: 	8
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
Patch3:		ru_compile_typo.patch
Patch4:		geany-0.20-mdvconf.patch

BuildRequires:  desktop-file-utils
BuildRequires:  imagemagick
BuildRequires:  intltool
BuildRequires:	lxterminal
BuildRequires:  perl-XML-Parser
BuildRequires:  pkgconfig(gtk+-2.0)

Suggests:	geany-plugins
%define __noautoreq 'pkgconfig\\(gtk+-2.0\\)' pkgconfig

%description
Geany is a small C editor using GTK2 with basic features of an
integrated development environment. It features syntax highlighting,
code completion, call tips, many supported filetypes (including C,
Java, PHP, HTML, DocBook, Perl, LateX, and Bash), and symbol lists.

%prep
%setup -q
# For future reason add edm distepoch  You may recreate packets set edm to 0
%if %{edm}
%patch0 -p0
%patch1 -p0
%endif
%patch2 -p1
%patch3 -p0
%patch4 -p1

%build
%configure2_5x
%make

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
rm %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%files -f %{name}.lang
%{_bindir}/%{name}
%{_includedir}/%{name}
%{_libdir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_defaultdocdir}/%{name}
%{_mandir}/man1/%{name}.*
%{_iconsdir}/hicolor/*/apps/*

