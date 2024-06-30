%global optflags %{optflags} -Wno-error -Wno-implicit-function-declaration
%global optflags %{optflags} -Wno-incompatible-function-pointer-types
#%global build_ldflags %{build_ldflags} -Wl,--undefined-version
#define _disable_lto 1

%global systemd_unit gnome-remote-desktop.service
 
%global tarball_version %%(echo %{version} | tr '~' '.')
 
Name:           gnome-remote-desktop
Version:        46.3
Release:        1
Summary:        GNOME Remote Desktop screen share service
 
License:        GPLv2+
URL:            https://gitlab.gnome.org/GNOME/gnome-remote-desktop
Source0:        https://download.gnome.org/sources/gnome-remote-desktop/40/%{name}-%{tarball_version}.tar.xz
# Fix build without RDP backend
#Patch0:         https://gitlab.gnome.org/GNOME/gnome-remote-desktop/-/merge_requests/267.patch
 
BuildRequires: a2x
BuildRequires: git
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: dbus-daemon
BuildRequires: pkgconfig(dbus-1)
BuildRequires: meson >= 0.36.0
BuildRequires: mutter
BuildRequires: wireplumber
BuildRequires: pkgconfig
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(glib-2.0) >= 2.32
BuildRequires: pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libei-1.0)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libpipewire-0.3) >= 0.3.0
BuildRequires: pkgconfig(libvncserver) >= 0.9.11-7
BuildRequires: pkgconfig(freerdp2)
BuildRequires: pkgconfig(fuse3)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: pkgconfig(libnotify)
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(ffnvcodec)
BuildRequires: pkgconfig(tss2-esys)
BuildRequires: pkgconfig(systemd)
BuildRequires: systemd
 
Requires:       pipewire >= 0.3.0
 
%description
GNOME Remote Desktop is a remote desktop and screen sharing service for the
GNOME desktop environment.
 
%prep
%autosetup -n %{name}-%{version} -p1

%build
#export CC=gcc
#export CXX=g++
%meson \
       -Drdp=false \
       -Dvnc=true
%meson_build
 
%install
%meson_install

%find_lang %{name}
 
%post
%systemd_user_post %{systemd_unit}
 
%preun
%systemd_user_preun %{systemd_unit}

%postun
%systemd_user_postun_with_restart %{systemd_unit}
 
%files -f %{name}.lang
%license COPYING
%doc README*
%{_bindir}/grdctl
%{_libexecdir}/gnome-remote-desktop-daemon
%{_userunitdir}/gnome-remote-desktop.service
%{_userunitdir}/gnome-remote-desktop-headless.service
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.enums.xml
%{_datadir}/dbus-1/system-services/org.gnome.RemoteDesktop.service
%{_datadir}/polkit-1/actions/org.gnome.remotedesktop.configure-system-daemon.policy
%{_datadir}/polkit-1/actions/org.gnome.remotedesktop.enable-system-daemon.policy
%{_datadir}/polkit-1/rules.d/20-gnome-remote-desktop.rules
%{_mandir}/man1/grdctl.1.*
