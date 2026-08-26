%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global auditversion 0.3-1

Summary: A set of tools to gather troubleshooting information from a system
Name: sos
Version: 4.11.2
Release: 4%{?dist}
Group: Applications/System
Source0: https://github.com/sosreport/sos/archive/%{version}/sos-%{version}.tar.gz
Source1: sos-audit-%{auditversion}.tgz
License: GPL-2.0-or-later
BuildArch: noarch
Url: https://github.com/sosreport/sos
BuildRequires: python3-devel
BuildRequires: gettext
BuildRequires: python3-setuptools
Requires: python3-requests
Requires: python3-setuptools
Recommends: python3-magic
Recommends: python3-pexpect
Recommends: python3-pyyaml
Conflicts: vdsm < 4.40
Obsoletes: sos-collector <= 1.9
Patch1: 0001-sosreport-binary.patch
Patch2: 0002-revert-PR4092-and-PR4275.patch
Patch3: 0003-foremanctl-valkey-PR4376.patch
Patch4: 0004-foreman-installer-Scrub-secrets-in-CLI-arg-dumps.patch
Patch5: 0005-policies-Prefer-most-specific-policy-when-multiple-m.patch
Patch6: 0006-processor-Limit-sys-devices-system-cpu-cpu-subdirs-c.patch

%description
Sos is a set of tools that gathers information about system
hardware and configuration. The information can then be used for
diagnostic purposes and debugging. Sos is commonly used to help
support technicians and developers.

%prep
%setup -qn %{name}-%{version}
%setup -T -D -a1 -q
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1

%build
%py3_build

%install
%py3_install '--install-scripts=%{_sbindir}'

install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 700 %{buildroot}%{_sysconfdir}/%{name}/cleaner
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/presets.d
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/groups.d
install -d -m 755 %{buildroot}%{_sysconfdir}/%{name}/extras.d
install -d -m 755 %{buildroot}%{_sysconfdir}/tmpfiles.d/
install -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 644 tmpfiles/tmpfilesd-sos-rh.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

rm -rf %{buildroot}/usr/config/

%find_lang %{name} || echo 0

cd %{name}-audit-%{auditversion}
DESTDIR=%{buildroot} ./install.sh
cd ..

# internationalization is currently broken. Uncomment this line once fixed.
# %%files -f %%{name}.lang
%files
%{_sbindir}/sos
%{_sbindir}/sosreport
%{_sbindir}/sos-collector
#%dir /etc/sos/cleaner
%dir /etc/sos/presets.d
%dir /etc/sos/extras.d
%dir /etc/sos/groups.d
%{_sysconfdir}/tmpfiles.d/%{name}.conf
%{python3_sitelib}/*
%{_mandir}/man1/*
%{_mandir}/man5/sos.conf.5.gz
%doc AUTHORS README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/sos/sos.conf
%config(noreplace) %{_sysconfdir}/sos/cleaner


%package audit
Summary: Audit use of some commands for support purposes
License: GPL-2.0-or-later
Group: Application/System

%description audit

Sos-audit provides configuration files for the Linux Auditing System
to track the use of some commands capable of changing the configuration
of the system.  Currently storage and filesystem commands are audited.

%post audit
%{_sbindir}/sos-audit.sh

%files audit
%defattr(755,root,root,-)
%{_sbindir}/sos-audit.sh
%defattr(644,root,root,-)
%config(noreplace) %{_sysconfdir}/sos/sos-audit.conf
%defattr(444,root,root,-)
%{_prefix}/lib/sos/audit/*
%{_mandir}/man5/sos-audit.conf.5.gz
%{_mandir}/man8/sos-audit.sh.8.gz
%ghost /etc/audit/rules.d/40-sos-filesystem.rules
%ghost /etc/audit/rules.d/40-sos-storage.rules
%license LICENSE

%changelog
* Wed Aug 05 2026 Jan Jansky <jjansky@redhat.com> = 4.11.2-4
- Update to 4.11.2-4

* Fri Jul 17 2026 Jan Jansky <jjansky@redhat.com> = 4.11.2-3
- Update to 4.11.2-3

* Fri Jul 17 2026 Jan Jansky <jjansky@redhat.com> = 4.11.2-2
- Update to 4.11.2-2

* Wed Jul 15 2026 Jan Jansky <jjansky@redhat.com> = 4.11.2-1
- Update to 4.11.2-1

* Thu Apr 02 2026 Jan Jansky <jjansky@redhat.com> = 4.11.0-1
- Update to 4.11.0-1
  Resolves: RHEL-157817

* Thu Feb 26 2026 Jan Jansky <jjansky@redhat.com> = 4.10.2-2
- Update to 4.10.2-2
  Resolves: RHEL-152471

* Thu Jan 22 2026 Jan Jansky <jjansky@redhat.com> = 4.10.2-1
- Update to 4.10.2-1
  Resolves: RHEL-142635

* Fri Dec 05 2025 Jan Jansky <jjansky@redhat.com> = 4.10.1-2
- Update to 4.10.1-2
  Resolves: RHEL-121474

* Tue Nov 25 2025 Jan Jansky <jjansky@redhat.com> = 4.10.1-1
- Update to 4.10.1-1
  Resolves: RHEL-121474

* Tue Sep 23 2025 Jan Jansky <jjansky@redhat.com> = 4.10.0-4
- Update to 4.10.0-4
  Resolves: RHEL-113795

* Wed Sep 17 2025 Jan Jansky <jjansky@redhat.com> = 4.10.0-3
- Update to 4.10.0-3
  Resolves: RHEL-113795

* Wed Sep 17 2025 Jan Jansky <jjansky@redhat.com> = 4.10.0-2
- Update to 4.10.0-2
  Resolves: RHEL-113795

* Thu Aug 21 2025 Jan Jansky <jjansky@redhat.com> = 4.10.0-1
- Update to 4.10.0
  Resolves: RHEL-110500
  Resolves: RHEL-110501
  Resolves: RHEL-110502
  Resolves: RHEL-110503

* Fri Jul 04 2025 Jan Jansky <jjansky@redhat.com> = 4.9.2-1
- Update to 4.9.2 
  Resolves: RHEL-101717
  Resolves: RHEL-101718
  Resolves: RHEL-101719
  Resolves: RHEL-101720

* Fri May 30 2025 Jan Jansky <jjansky@redhat.com> = 4.9.1-2
- Update to 4.9.1-2 in RHEL 9
  Resolves: RHEL-86668
  Resolves: RHEL-86644
  Resolves: RHEL-86647
  Resolves: RHEL-86646

* Tue Apr 15 2025 Jan Jansky <jjansky@redhat.com> = 4.9.1-1
- Update to 4.9.1 in RHEL 9
  Resolves: RHEL-86668
  Resolves: RHEL-86644
  Resolves: RHEL-86647
  Resolves: RHEL-86646

* Fri Jan 24 2025 Jan Jansky <jjansky@redhat.com> = 4.8.2-2
- Add new plugin aap_containerized
  Resolves: RHEL-76057

* Tue Jan 07 2025 Jan Jansky <jjansky@redhat.com> = 4.8.2-1
- Update to 4.8.2 in RHEL 9
  Resolves: RHEL-72942

* Wed Oct 23 2024 Jan Jansky <jjansky@redhat.com> = 4.8.1-1
- Update to 4.8.1 in RHEL 9
  Resolves: RHEL-64159
 
* Tue Oct 15 2024 Jan Jansky <jjansky@redhat.com> = 4.8.0-5
- Rebase to 4.8.0 and adding credential obfuscation
  Resolves: RHEL-58096

* Fri Sep 27 2024 Jan Jansky <jjansky@redhat.com> = 4.8.0-4
- Added credentials obfuscation from multiple files
  Resolves: RHEL-58096

* Wed Sep 25 2024 Jan Jansky <jjansky@redhat.com> = 4.8.0-3
- Update 4.8.0
  Resolves: RHEL-58096

* Thu Sep 19 2024 Jan Jansky <jjansky@redhat.com> = 4.8.0-2
- Update to 4.8.0
  Resolves: RHEL-58096

* Mon Sep 09 2024 Pierguido Lambri <plambri@redhat.com> = 4.8.0-1
- New upstream release
  Resolves: RHEL-58096

* Wed Aug 21 2024 Pavel Moravec <pmoravec@redhat.com> = 4.7.2-3
- reverting RHEL-22732 patch due to regressions
  Resolves: RHEL-49781

* Fri Jun 21 2024 Pierguido Lambri <plambri@redhat.com> = 4.7.2-1
- New upstream release
  Resolves: RHEL-49781

* Thu May 09 2024 Pavel Moravec <pmoravec@redhat.com> = 4.7.1-3
- [archive] Fix get_archive_root after files reordering
  Resolves: RHEL-35945

* Mon Apr 08 2024 Jan Jansky <jjansky@redhat.com> = 4.7.1-1
- rebase to upstream 4.7.1
  Resolves: RHEL-32106

* Tue Feb 20 2024 Jan Jansky <jjansky@redhat.com> = 4.7.0-1
- rebase to upstream 4.7.0
  Resolves: RHEL-26115

* Thu Jan 11 2024 Pavel Moravec <pmoravec@redhat.com> = 4.6.1-1
- rebase to upstream 4.6.1
  Resolves: RHEL-21174
- [redhat] Change authentication method for RHEL
  Resolves: RHEL-21178

* Wed Oct 18 2023 Pavel Moravec <pmoravec@redhat.com> = 4.6.0-5
  [pulpcore] Scrub AUTH_LDAP_BIND_PASSWORD value
  Resolves: RHEL-13701

* Tue Oct 17 2023 Pavel Moravec <pmoravec@redhat.com> = 4.6.0-4
- [pulp] Fix dynaconf obfuscation and add AUTH_LDAP_BIND_PASSWORD
  Resolves: RHEL-13701

* Thu Oct 12 2023 Pavel Moravec <pmoravec@redhat.com> = 4.6.0-3
- [greenboot] seperate logs to a standalone plugin; enhance [microshift]
  Resolves: SUPDEV148

* Fri Sep 01 2023 Pavel Moravec <pmoravec@redhat.com> = 4.6.0-2
- [openshift_ovn] Collect additional ovnkube node logs
  Resolves: SUPDEV145

* Wed Aug 23 2023 Jan Jansky <jjansky@redhat.com> = 4.6.0-1
- [ultrapath] Add new plugin for Huawei UltraPath
  Resolves: bz2187407
- [cleaner] Use data filter for extraction
  Resolves: bz2217906
- [discovery] Enable the plugin by containers
  Resolves: bz2222134

* Thu Jul 27 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.6-1
- Collect db files for ovn interconnect environment
  Resolves: bz2226682

* Fri Jul 14 2023 Jan Jansky <jjansky@redhat.com> - 4.5.5-2
- Adding patch for cleaning mac addresses
  Resolves: bz2217943

* Mon Jul 03 2023 Jan Jansky <jjansky@redhat.com> = 4.5.5-1
- Rebase on upstream 4.5.5
  Resolves: bz2217943

* Wed May 31 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.4-1
- [specfile] add runtime requirement to python3-setuptools
  Resolves: bz2207776

* Thu May 04 2023 Jan Jansky <jjansky@redhat.com> = 4.5.3-1
- [unpackaged] Print unpackaged symlinks instead of targets
  Resolves: bz2169684
- [report] Ignore case when scrubbing via do_file_sub
  Resolves: bz2174254
- [powerpc]: To collect lparnumascore logs
  Resolves: bz2177984

* Wed Mar 08 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.1-3
- Rebase on upstream 4.5.1
  Resolves: bz2175808
- [microshift] Fix microshift get and add commands
  Resolves: bz2175650

* Tue Feb 07 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.0-1
- Rebase on upstream 4.5.0
  Resolves: bz2082615

* Thu Nov 03 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-4
- [ocp] Add newly required labels to temp OCP namespace
  Resolves: bz2130976

* Fri Oct 28 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-3
- [cleaner] Apply compile_regexes after a regular parse line
  Resolves: bz2138174

* Thu Sep 22 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-2
- [utilities] Relax from hard dependency of python3-magic
  Resolves: bz2126089
- [dnf] Collect legacy yum config symlinks, properly obfuscate pwds
  Resolves: bz2125499

* Fri Sep 09 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-1
- Rebase on upstream 4.4
  Resolves: bz2082615
- [redhat] Honour credential-less --upload-url on RedHat distro properly
  Resolves: bz2059573
- [md] Restrict data capture to raid members
  Resolves: bz2062283
- [sos] Fix unhandled exception when concurrently removing temp dir
  Resolves: bz2088440

* Mon Aug 29 2022 Pavel Moravec <pmoravec@redhat.com> = 4.3-3
- [vdsm] Set LVM option use_devicesfile=0
  Resolves: bz2122355
- [Plugin] Make forbidden path checks more efficient
  Resolves: bz2122354

* Thu Jun 16 2022 Pavel Moravec <pmoravec@redhat.com> = 4.3-2
- [ocp, openshift] Re-align API collection options and rename
  Resolves: bz2065563
- [utilities] Close file only when storing to file
  Resolves: bz2079492
- [report] --list-plugins should report used, not default,
  Resolves: bz2079490
- [report] Honor plugins' hardcoded plugin_timeout
  Resolves: bz2079188
- crio: switch from parsing output in table format to json
  Resolves: bz2097674
- [pacemaker] Redesign node enumeration logic
  Resolves: bz2082914
- [tigervnc] Update collections for newer versions of TigerVNC
  Resolves: bz2066181
- [plugins] Allow 'str' PlugOpt type to accept any value
  Resolves: bz2079491
- [ovirt] answer files: Filter out all password keys
  Resolves: bz2095267

* Thu Mar 24 2022 Pavel Moravec <pmoravec@redhat.com> = 4.3-1
- Rebase on upstream 4.3
  Resolves: 2055003
- [sapnw] Fix IndexError exception
  Resolves: 2065551
- [subscription_manager] collect syspurpose data via sub-man
  Resolves: 2002333
- [Plugin, utilities] Allow writing command output directly to disk
  Resolves: 2065564
- [Ceph] Add support for containerized Ceph setup
  Resolves: 2065562
- [unbound] Add new plugin for Unbound DNS resolver
  Resolves: 2065560
- [discovery] Add new discovery plugin
  Resolves: 2065558
- [system] Collect glibc tuning decisions
  Resolves: 2032913

* Wed Feb 23 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-15
- [sosnode] Handle downstream versioning for runtime option
  Resolves: bz2037350
- [options] Fix logging on plugopts in effective sos command
  Resolves: bz2054883
- [report] Honor plugins' hardcoded plugin_timeout
  Resolves: bz2055548
- [policies] Set fallback to None sysroot, don't chroot to '/'
  Resolves: bz2011537
- [ovn_central] Rename container responsable of Red Hat
  Resolves: bz2043488

* Wed Jan 26 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-13
- [virsh] Catch parsing exception
  Resolves: bz2041855

* Tue Jan 25 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-12
- [foreman] Use psql-msgpack-decode wrapper for dynflow >= 1.6
  Resolves: bz2043104
- [virsh] Call virsh commands in the foreground / with a TTY
  Resolves: bz2041855
- [ovn_central] Account for Red Hat ovn package naming
  Resolves: bz2043488
- [clean,parsers] Build regex lists for static items only once
  Resolves: bz2037350

* Mon Jan 10 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-11
- [report] Add journal logs for NetworkManager plugin
  Resolves: bz2037350

* Fri Jan 07 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-9
- add oc transport, backport various PRs for OCP
  Resolves: bz2037350
- [report] Provide better warning about estimate-mode
  Resolves: bz2011537
- [hostname] Fix loading and detection of long base domains
  Resolves: bz2024893

* Sun Dec 19 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-8
- [rhui] New log folder
  Resolves: bz2031777
- nvidia]:Patch to update nvidia plugin for GPU info
  Resolves: bz2034001
- [hostname] Fix edge case for new hosts in a known subdomain
  Resolves: bz2024893

* Wed Dec 08 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-7
- [hostname] Simplify case matching for domains
  Resolves: bz2024893

* Tue Nov 30 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-6
- [redhat] Fix broken URI to upload to customer portal
  Resolves: bz2025611

* Mon Nov 22 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-5
- [clean,hostname_parser] Source /etc/hosts for obfuscation
  Resolves: bz2024893
- [clean, hostname] Fix unintentionally case sensitive
  Resolves: bz2024892
- [redhat] update SFTP API version to v2
  Resolves: bz2025611

* Tue Nov 16 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-4
- [report] Calculate sizes of dirs, symlinks and manifest in
  Resolves: bz2011537
- [report] shutdown threads for timeouted plugins
  Resolves: bz2012859
- [report] fix filter_namespace per pattern
  Resolves: bz2020778
- Ensure specific plugin timeouts are only set
  Resolves: bz2023481

* Wed Nov 03 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-2
- [firewall_tables] call iptables -t <table> based on nft
  Resolves: bz2011536
- [report] Count with sos_logs and sos_reports in
  Resolves: bz2011537
- [foreman] Collect puma status and stats
  Resolves: bz2011507
- [report] Overwrite pred=None before refering predicate
  Resolves: bz2012858
- [openvswitch] add commands for offline analysis
  Resolves: bz2019697

* Wed Oct 06 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-1
- Rebase on upstream 4.2
  Resolves: bz1998134
- [report] Implement --estimate-only
  Resolves: bz2011537
- [omnipath_client] Opacapture to run only with allow changes
  Resolves: bz2011534
- [unpackaged] deal with recursive loop of symlinks properly
  Resolves: bz2011533
- [networking] prevent iptables-save commands to load nf_tables
  Resolves: bz2011538
- [kernel] Capture Pressure Stall Information
  Resolves: bz2011535
- [processor] Apply sizelimit to /sys/devices/system/cpu/cpuX
  Resolves: bz1869561

* Wed Aug 11 2021 Pavel Moravec <pmoravec@redhat.com> = 4.1-8
- [report,collect] unify --map-file arguments
  Resolves: bz1985985
- [rhui] add new plugin for RHUI 4
  Resolves: bz1992859
- [username parser] Load usernames from `last` for LDAP users
  Resolves: bz1992861

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 4.1-7
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Jul 27 2021 Pavel Moravec <pmoravec@redhat.com> - 4.1-6
- [networking] collect also tc filter show ingress
  Resolves: bz1985976
- [cleaner] Only skip packaging-based files for the IP parser
  Resolves: bz1985982
- [sssd] sssd plugin when sssd-common
  Resolves: bz1967718
- Various OCP/cluster/cleanup enhancements
  Resolves: bz1985983
- [options] allow variant option names in config file
  Resolves: bz1985985
- [plugins] Set default predicate instead of None
  Resolves: bz1938874
- [MigrationResults] collect info about conversions and
  Resolves: bz1959779

* Wed Jun 02 2021 Pavel Moravec <pmoravec@redhat.com> - 4.1-4
- [archive] skip copying SELinux context for /proc and /sys everytime
  Resolves: bz1965002
- Load maps from all archives before obfuscation
  Resolves: bz1967110
- Multiple fixes in man pages
  Resolves: bz1967111
- [ds] Mask password and encryption keys in ldif files
  Resolves: bz1967112
- [report] add --cmd-timeout option
  Resolves: bz1967113
- [cups] Add gathering cups-browsed logs
  Resolves: bz1967114
- [sssd] Collect memory cache / individual logfiles
  Resolves: bz1967115
- Collect ibmvNIC dynamic_debugs
  Resolves: bz1967116
- [pulpcore] add plugin for pulp-3
  Resolves: bz1967117
- [saphana] remove redundant unused argument of get_inst_info
  Resolves: bz1967118
- [networking] Add nstat command support
  Resolves: bz1967119
- [snapper] add a new plugin
  Resolves: bz1967120

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 4.1-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Thu Apr 01 2021 Pavel Moravec <pmoravec@redhat.com> - 4.1-3
- adding sos-audit
- [gluster] Add glusterd public keys and status files
  Resolves: bz1925419

* Wed Mar 10 2021 Sandro Bonazzola <sbonazzo@redhat.com> - 4.1-1
- Rebase to 4.1
