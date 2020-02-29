Name:		spice-vdagent
Version:	0.19.0
Release:	1
Summary:	Agent for Spice guests
Group:		System/Kernel and hardware
License:	GPLv3+
URL:		http://spice-space.org/
Source0:	http://spice-space.org/download/releases/%{name}-%{version}.tar.bz2

#######################################################################
#Cross patches for spice-gtk, spice-protocol and spice-vdagent (angry)#
#######################################################################

Patch0001:      0001-vdagentd-Fix-session-lookup-for-new-GNOME-versions.patch
# clipboard-race patches: together with patches for spice-protocol
# and spice-gtk these fix problems interacting with mutter's new
# clipboard manager
# https://bugzilla.redhat.com/show_bug.cgi?id=1755038
# https://patchwork.freedesktop.org/series/58418/#rev2
# all rebased by Jakub Janků:
# https://github.com/jjanku/linux-vd_agent/tree/clipboard-race
# with several other commits needed for the clipboard fixes to apply
Patch0002:      0001-vdagent-fix-memory-leak-of-g_memdup.patch
Patch0003:      0002-x11-randr-use-glib-s-MAX-and-MIN.patch
Patch0004:      0003-x11-randr-simplest-fix-for-address-of-packed-member.patch
Patch0005:      0004-vdagent-simple-fix-for-address-of-packed-member.patch
Patch0006:      0005-x11-randr-Avoid-passing-XEvent-as-value.patch
Patch0007:      0006-x11-Avoid-passing-XEvent-as-value.patch
Patch0008:      0007-x11-Constify-XEvent-argument.patch
Patch0009:      0008-device-info-remove-g_list_length-on-compare_addresse.patch
Patch0010:      0009-x11-Change-check-to-make-code-scanners-not-giving-wa.patch
Patch0011:      0010-covscan-avoid-false-positive-on-g_clear_pointer.patch
Patch0012:      0011-covscan-initialize-argv-s-copy.patch
Patch0013:      0012-covscan-add-comment-on-false-positive-on-g_memdup.patch
Patch0014:      0013-virtio-port-handle_fds-make-read-and-write-code-cons.patch
# actual clipboard fix series starts here
Patch0015:      0014-Add-a-.gitpublish.patch
Patch0016:      0015-configure-bump-gtk-3.22.patch
Patch0017:      0016-clipboard-remove-vdagent-selection-id-usage.patch
Patch0018:      0017-configure-depend-on-gobject.patch
Patch0019:      0018-configure-bump-gobject-2.50.patch
Patch0020:      0019-vdagent-use-G_OPTION_FLAG_NONE.patch
Patch0021:      0020-clipboard-gobject-ify-VDAgentClipboards.patch
Patch0022:      0021-clipboard-filter-out-only-our-own-events.patch
Patch0023:      0022-clipboard-only-send-release-when-no-immediate-grab.patch
Patch0024:      0023-clipboard-implement-CAP_CLIPBOARD_GRAB_SERIAL.patch

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
%autosetup -p1
autoreconf -fi

%build
%configure \
	--with-session-info=systemd \
	--with-init-script=systemd

%make_build


%install
%make_install

%post
%_post_service spice-vdagentd.service

%preun
%_preun_service spice-vdagentd.service

%postun
%systemd_postun_with_restart spice-vdagentd.service

%files
%doc COPYING CHANGELOG.md README.md
%{_udevrulesdir}/70-spice-vdagentd.rules
%{_unitdir}/spice-vdagentd.service
%{_unitdir}/spice-vdagentd.socket
%{_tmpfilesdir}/spice-vdagentd.conf
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm
%{_mandir}/man1/%{name}*.1*
