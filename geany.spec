%define name 	geany
%define cname	Geany
%define version	0.12
%define release	1

Summary:	Geany is a small C editor using GTK2
Name: 		%{name}
Version: 	%{version}
Release: 	%mkrel %{release}
License: 	GPL
Group: 		Development/C
URL: 		http://geany.uvena.de/
Source0: 	%{name}-%{version}.tar.bz2
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:  pkgconfig
BuildRequires:  gtk2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  perl-XML-Parser
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

# prepare icons
mkdir -p %{buildroot}%{_miconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_liconsdir}
convert pixmaps/%{name}.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert pixmaps/%{name}.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert pixmaps/%{name}.png -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png

# remove useless file
rm %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

%clean
rm -rf $RPM_BUILD_ROOT

%post 
%{update_desktop_database}
%{update_menus}

%postun
%{clean_desktop_database}
%{clean_menus}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_defaultdocdir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}.ico
%{_mandir}/man1/%{name}.*
%{_datadir}/icons/hicolor/16x16/apps/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/*
