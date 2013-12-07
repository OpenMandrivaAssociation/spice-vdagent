Name:		spice-vdagent
Version:	0.12.0
Release:	3
Summary:	Agent for Spice guests
Group:		System/Kernel and hardware
License:	GPLv3+
URL:		http://spice-space.org/
Source0:	http://spice-space.org/download/releases/%{name}-%{version}.tar.bz2
BuildRequires:	spice-protocol
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libsystemd-login) >= 188
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xfixes)
Requires(pre):	rpm-helper
Requires(preun): rpm-helper

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
%setup -q

%build
%configure2_5x \
	--with-session-info=systemd \
	--with-init-script=systemd

%make

%install
%makeinstall_std

%post
%_post_service spice-vdagentd.service

%preun
%_preun_service spice-vdagentd.service

%postun
%systemd_postun_with_restart spice-vdagentd.service

%files
%doc COPYING ChangeLog README TODO
%config(noreplace) %{_sysconfdir}/rsyslog.d/spice-vdagentd.conf
/lib/udev/rules.d/70-spice-vdagentd.rules
%{_unitdir}/spice-vdagentd.service
%{_unitdir}/spice-vdagentd.target
%{_prefix}/lib/tmpfiles.d/spice-vdagentd.conf
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_var}/run/spice-vdagentd
%{_sysconfdir}/modules-load.d/spice-vdagentd.conf
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm
