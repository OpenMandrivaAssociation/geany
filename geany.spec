%define name 	geany
%define cname	Geany
%define version	0.18
%define release	1

Summary:	Small C editor using GTK2
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel %{release}
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
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  imagemagick
BuildRequires:  perl-XML-Parser
BuildRequires:  intltool
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Geany is a small C editor using GTK2 with basic features of an
integrated development environment. It features syntax highlighting,
code completion, call tips, many supported filetypes (including C,
Java, PHP, HTML, DocBook, Perl, LateX, and Bash), and symbol lists.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# research locale file
%find_lang %{name}

# prepare menu
# we remove the key "Version" and "Encoding" because it's invalid
desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="GNOME" \
	--remove-key="Version" \
	--remove-key="Encoding" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# Install tags files
install -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} $RPM_BUILD_ROOT%{_datadir}/%{name}

# remove useless file
rm %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%{update_desktop_database}
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_desktop_database}
%{clean_menus}
%endif

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_includedir}/%{name}
%{_libdir}/%{name}
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_defaultdocdir}/%{name}
%{_mandir}/man1/%{name}.*
%{_datadir}/icons/hicolor/16x16/apps/*
%{_iconsdir}/hicolor/*/apps/*
