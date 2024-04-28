Name:		spice-vdagent
Version:	0.22.1
Release:	3
Summary:	Agent for Spice guests
Group:		System/Kernel and hardware
License:	GPLv3+
URL:		http://spice-space.org/
Source0:	http://spice-space.org/download/releases/%{name}-%{version}.tar.bz2

#######################################################################
#Cross patches for spice-gtk, spice-protocol and spice-vdagent (angry)#
#######################################################################

BuildRequires:	spice-protocol
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	libtool

Requires(post):	systemd
Requires(pre):	rpm-helper
Requires(preun):	rpm-helper

%description
Spice agent for Linux guests offering the following features:

Features:
* Client mouse mode (no need to grab mouse by client, no mouse lag)
  this is handled by the daemon by feeding mouse events into the kernel
  via uinput. This will only work if the active X-session is running a
  spice-vdagent process so that its resolution can be determined.
* Automatic adjustment of the X-session resolution to the client resolution
* Support of copy and paste (text and images) between the active X-session
  and the client

%prep
%autosetup -p1
autoreconf -fi

%build
%configure \
	--with-session-info=systemd \
	--with-init-script=systemd

%make_build


%install
%make_install

%files
%doc COPYING CHANGELOG.md README.md
%{_udevrulesdir}/70-spice-vdagentd.rules
%{_unitdir}/spice-vdagentd.service
%{_unitdir}/spice-vdagentd.socket
%{_tmpfilesdir}/spice-vdagentd.conf
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
%{_userunitdir}/spice-vdagent.service
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm
%{_mandir}/man1/%{name}*.1*
