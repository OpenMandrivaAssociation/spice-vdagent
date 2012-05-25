%bcond_without systemd_login

Name:		spice-vdagent
Version:	0.10.1
Release:	2
Summary:	Agent for Spice guests
Group:		System/Kernel and hardware
License:	GPLv3+
URL:		http://spice-space.org/
Source0:	http://spice-space.org/download/releases/%{name}-%{version}.tar.bz2
BuildRequires:	spice-protocol
BuildRequires:	pkgconfig(systemd)
%if %{with systemd_login}
BuildRequires:	pkgconfig(libsystemd-login) >= 42
%endif
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(pciaccess)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xfixes)

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
%if %{with systemd_login}
	--with-session-info=systemd
%endif

%make

%install
%makeinstall_std

%post
/sbin/chkconfig --add spice-vdagentd

%preun
if [ $1 = 0 ] ; then
    /sbin/service spice-vdagentd stop >/dev/null 2>&1
    /sbin/chkconfig --del spice-vdagentd
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service spice-vdagentd condrestart >/dev/null 2>&1 || :
fi

%files
%doc COPYING ChangeLog README TODO
%{_sysconfdir}/tmpfiles.d/spice-vdagentd.conf
%{_initddir}/spice-vdagentd
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_var}/log/spice-vdagentd
%{_var}/run/spice-vdagentd
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm

