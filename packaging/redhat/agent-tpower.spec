#
#    agent-tpower - Computes power metrics
#
#    Copyright (C) 2014 - 2015 Eaton                                        
#                                                                           
#    This program is free software; you can redistribute it and/or modify   
#    it under the terms of the GNU General Public License as published by   
#    the Free Software Foundation; either version 2 of the License, or      
#    (at your option) any later version.                                    
#                                                                           
#    This program is distributed in the hope that it will be useful,        
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
#    GNU General Public License for more details.                           
#                                                                           
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.            
#

# To build with draft APIs, use "--with drafts" in rpmbuild for local builds or add
#   Macros:
#   %_with_drafts 1
# at the BOTTOM of the OBS prjconf
%bcond_with drafts
%if %{with drafts}
%define DRAFTS yes
%else
%define DRAFTS no
%endif
Name:           agent-tpower
Version:        0.1.0
Release:        1
Summary:        computes power metrics
License:        GPL-2.0+
URL:            https://eaton.com/
Source0:        %{name}-%{version}.tar.gz
Group:          System/Libraries
# Note: ghostscript is required by graphviz which is required by
#       asciidoc. On Fedora 24 the ghostscript dependencies cannot
#       be resolved automatically. Thus add working dependency here!
BuildRequires:  ghostscript
BuildRequires:  asciidoc
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel
BuildRequires:  systemd
%{?systemd_requires}
BuildRequires:  xmlto
BuildRequires:  gcc-c++
BuildRequires:  zeromq-devel
BuildRequires:  czmq-devel
BuildRequires:  malamute-devel
BuildRequires:  libbiosproto-devel
BuildRequires:  cxxtools-devel
BuildRequires:  tntdb-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
agent-tpower computes power metrics.

%package -n libagent_tpower0
Group:          System/Libraries
Summary:        computes power metrics

%description -n libagent_tpower0
agent-tpower computes power metrics.
This package contains shared library.

%post -n libagent_tpower0 -p /sbin/ldconfig
%postun -n libagent_tpower0 -p /sbin/ldconfig

%files -n libagent_tpower0
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libagent_tpower.so.*

%package devel
Summary:        computes power metrics
Group:          System/Libraries
Requires:       libagent_tpower0 = %{version}
Requires:       zeromq-devel
Requires:       czmq-devel
Requires:       malamute-devel
Requires:       libbiosproto-devel
Requires:       cxxtools-devel
Requires:       tntdb-devel

%description devel
agent-tpower computes power metrics.
This package contains development files.

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libagent_tpower.so
%{_libdir}/pkgconfig/libagent_tpower.pc
%{_mandir}/man3/*
%{_mandir}/man7/*

%prep
%setup -q

%build
sh autogen.sh
%{configure} --enable-drafts=%{DRAFTS} --with-systemd-units
make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# remove static libraries
find %{buildroot} -name '*.a' | xargs rm -f
find %{buildroot} -name '*.la' | xargs rm -f

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/bios-agent-tpower
%{_prefix}/lib/systemd/system/bios-agent-tpower*.service
%{_mandir}/man1/bios-agent-tpower*
%config(noreplace) %{_sysconfdir}/agent-tpower/bios-agent-tpower.cfg
%dir %{_sysconfdir}/agent-tpower
%if 0%{?suse_version} > 1315
%post
%systemd_post bios-agent-tpower.service
%preun
%systemd_preun bios-agent-tpower.service
%postun
%systemd_postun_with_restart bios-agent-tpower.service
%endif

%changelog
