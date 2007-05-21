%define name 	geany
%define cname	Geany
%define version	0.11
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
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%name): needs="x11" \
	section="More Applications/Development/Development Environments" \
	title=%{cname} \
	longtitle="Small C editor using GTK2" \
	command="%{_bindir}/%{name}" \
	icon="%{name}.png" \
	xdg="true"
EOF

perl -pi -e 's/Encoding=UTF-8//' $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="GNOME" \
	--add-category="GTK" \
	--add-category="Development" \
	--add-category="X-MandrivaLinux-MoreApplications-Development-DevelopmentEnvironments" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# prepare icons
mkdir -p %{buildroot}%{_miconsdir} %{buildroot}%{_iconsdir} %{buildroot}%{_liconsdir}
convert pixmaps/%{name}.png -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert pixmaps/%{name}.png -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert pixmaps/%{name}.png -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png

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
%doc AUTHORS COPYING INSTALL NEWS README THANKS TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_defaultdocdir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}.ico
%{_mandir}/man1/%{name}.1.bz2
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}

