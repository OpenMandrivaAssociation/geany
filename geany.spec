Summary:	Small C editor using GTK2
Name: 		geany
Version: 	1.22
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
# Russian doc patch
Patch2:		ru_doc.patch

BuildRequires:  desktop-file-utils
BuildRequires:  imagemagick
BuildRequires:  intltool
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
%patch2 -p1

%build
%configure2_5x
%make LIBS='-lgmodule-2.0'

%install
%makeinstall
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

#Fix for Russian
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
rm -f %{buildroot}%{_iconsdir}/hicolor/icon-theme.cache

%files -f %{name}.lang
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_defaultdocdir}/%{name}
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/%{name}.*

%files devel
%{_includedir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc

