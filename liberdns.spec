Name: liberdns-applet
Summary: Liber Open DNS update tool
URL: http://www.ojuba.org
Version: 0.1.4
Release: 1%{?dist}
Source0: %{name}-%{version}.tar.bz2
License: Waqf
Group: Applications/Network
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python
Requires: python, pygtk2, xfce4-notifyd

# %{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
Liber Open DNS update tool

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall DESTDIR=$RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc LICENSE-en LICENSE-ar README AUTHORS COPYING VERSION ARTISTS
%{_bindir}/%{name}
%{python_sitelib}/liberdns*
%{python_sitelib}/*.egg-info
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/applications/*.desktop
%{_datadir}/locale/*/*/*.mo
/etc/xdg/autostart/*.desktop

%changelog
* Tue Nov 04 2011  Ehab El-Gedawy <ehabsas@gmail.com> - 0.1.4-1
- Add ARTISTS.
- Fix python Interpreter for ArchLinux users.
  
* Tue Nov 03 2011  Ehab El-Gedawy <ehabsas@gmail.com> - 0.1.3-1
- Add about.
- Fix timer bug.
- Use one nofication object.
- Fix Makefile install and unainstall sections.
  
* Tue Nov 02 2011  Ehab El-Gedawy <ehabsas@gmail.com> - 0.1.2-1
- Fix autostart.
- Add COPYING.
- Translate TODO.

* Tue Nov 01 2011  Ehab El-Gedawy <ehabsas@gmail.com> - 0.1.1-1
- Change file names.
- Change utility name to liberdns.
- Add Arabic translate.
- Fix python Interpreter for ArchLinux users.
- Add DBus service.

* Mon Oct 31 2011  Ehab El-Gedawy <ehabsas@gmail.com> - 0.1.0-1
- Initial packing

