%global systemd_unit gnome-remote-desktop.service
 
%global tarball_version %%(echo %{version} | tr '~' '.')
 
Name:           gnome-remote-desktop
Version:        43.2
Release:        1
Summary:        GNOME Remote Desktop screen share service
 
License:        GPLv2+
URL:            https://gitlab.gnome.org/jadahl/gnome-remote-desktop
Source0:        https://download.gnome.org/sources/gnome-remote-desktop/40/%{name}-%{tarball_version}.tar.xz
 
BuildRequires:  a2x
BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  meson >= 0.36.0
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libpipewire-0.3) >= 0.3.0
BuildRequires:  pkgconfig(libvncserver) >= 0.9.11-7
BuildRequires:  pkgconfig(freerdp2)
BuildRequires:  pkgconfig(fuse3)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(tss2-esys)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  systemd
 
Requires:       pipewire >= 0.3.0
 
%description
GNOME Remote Desktop is a remote desktop and screen sharing service for the
GNOME desktop environment.
 
%prep
%autosetup -p1
 
# disabe fdk-acc because it comes from restricted (lets switch to fdk-acc-free in future). Disable rdp bc it need fdk-acc...
%build
%meson \
       -Drdp=false \
       -Dvnc=true\
       -Dfdk_aac=false
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
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.desktop.remote-desktop.enums.xml
#{_datadir}/gnome-remote-desktop/grd-cuda-avc-utils_*.ptx
#{_datadir}/gnome-remote-desktop/grd-cuda-damage-utils_30.ptx
%{_mandir}/man1/grdctl.1.*

