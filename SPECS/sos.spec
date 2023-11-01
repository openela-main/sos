%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global auditversion 0.3

Summary: A set of tools to gather troubleshooting information from a system
Name: sos
Version: 4.6.0
Release: 2%{?dist}
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
Obsoletes: sos-collector
Patch1: sos-SUPDEV145-ovnkube-logs.patch

%description
Sos is a set of tools that gathers information about system
hardware and configuration. The information can then be used for
diagnostic purposes and debugging. Sos is commonly used to help
support technicians and developers.

%prep
%setup -qn %{name}-%{version}
%setup -T -D -a1 -q
%patch1 -p1


%build
%py3_build

%install
%py3_install '--install-scripts=%{_sbindir}'
rm -f %{buildroot}/usr/config/sos.conf
rm -f %{buildroot}/usr/config/tmpfilesd-sos-rh.conf
install -Dm644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/tmpfiles.d/
install -m 644 tmpfiles/tmpfilesd-sos-rh.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

%find_lang %{name} || echo 0

cd %{name}-audit-%{auditversion}
DESTDIR=%{buildroot} ./install.sh
cd ..

mkdir -p %{buildroot}%{_sysconfdir}/sos/{cleaner,presets.d,extras.d,groups.d}

# internationalization is currently broken. Uncomment this line once fixed.
# %%files -f %%{name}.lang
%files
%{_sbindir}/sosreport
%{_sbindir}/sos
%{_sbindir}/sos-collector
%dir /etc/sos/presets.d
%dir /etc/sos/extras.d
%dir /etc/sos/groups.d
/etc/tmpfiles.d/%{name}.conf
%{python3_sitelib}/*
%{_mandir}/man1/sosreport.1.gz
%{_mandir}/man1/sos-clean.1.gz
%{_mandir}/man1/sos-collect.1.gz
%{_mandir}/man1/sos-collector.1.gz
%{_mandir}/man1/sos-help.1.gz
%{_mandir}/man1/sos-mask.1.gz
%{_mandir}/man1/sos-report.1.gz
%{_mandir}/man1/sos.1.gz
%{_mandir}/man5/sos.conf.5.gz
%doc AUTHORS README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/sos/sos.conf
%config(noreplace) %{_sysconfdir}/sos/cleaner

%package audit
Summary: Audit use of some commands for support purposes
License: GPLv2+
Group: Application/System

%description audit

Sos-audit provides configuration files for the Linux Auditing System
to track the use of some commands capable of changing the configuration
of the system. Currently storage and filesystem commands are audited.

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

%changelog
* Fri Sep 01 2023 Pavel Moravec <pmoravec@redhat.com> = 4.6.0-2
- [openshift_ovn] Collect additional ovnkube node logs
  Resolves: SUPDEV145

* Wed Aug 23 2023 Jan Jansky <jjansky@redhat.com> = 4.6.0-1
- [cleaner] Use data filter for extraction
  Resolves: bz2218873

* Thu Jul 27 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.6-1
- Rebase sos to 4.5.6
  Resolves: bz2226724

* Fri Jul 14 2023 Jan Jansky <jjansky@redhat.com> = 4.5.5-2
- Adding patch for mac obfuscation
  Resolves: bz2218279
  Resolves: bz2216608
  Resolves: bz2207562

* Mon Jul 03 2023 Jan Jansky <jjansky@redhat.com> = 4.5.5-1
- [clean] Respect permissions of sanitised files
  Resolves: bz2218279
- [plugin] Fix exception when calling os.makedirs
  Resolves: bz2216608
- [cleaner] Enhance trailing characters list after AMC address
  Resolves: bz2207562

* Thu Jun 01 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.4-1
- [plugins] collect strings before commands
  Resolves: bz2203141
- [collector] collect report from primary node if in node_list
  Resolves: bz2186460
- [powerpc] collect invscout logs
  Resolves: bz2210543
- [rhc] New plugin for RHC
  Resolves: bz2196649

* Fri May 05 2023 Jan Jansky <jjansky@redhat.com> = 4.5.3-1
- [report] Ignore case when scrubbing via do_file_sub
  Resolves: bz2143272
- [subscription_manager] Scrub proxy passwords from repo_server_val
  Resolves: bz2177282
- [virsh] Scrub passwords in virt-manager logs
  Resolves: bz2184062

* Wed Mar 08 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.1-3
- Rebase on upstream 4.5.1
  Resolves: bz2175806
- [composer] Capure /etc/osbuild-composer file
  Resolves: bz2169776
- [ostree] Collect "ostree fsck" under plugin specific opt
  Resolves: bz2161533
- [iprconfig] guard whole plugin by sg kmod predicate
  Resolves: bz2176086
- [cleaner] dont clean sys_tmp from final_path
  Resolves: bz2176218

* Tue Feb 07 2023 Pavel Moravec <pmoravec@redhat.com> = 4.5.0-1
- Rebase on upstream 4.5.0
  Resolves: bz2082614

* Thu Nov 03 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-4
- [ocp] Add newly required labels to temp OCP namespace
  Resolves: bz2130922

* Fri Oct 28 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-3
- [cleaner] Apply compile_regexes after a regular parse line
  Resolves: bz2138173

* Thu Sep 22 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-2
- [utilities] Relax from hard dependency of python3-magic
  Resolves: bz2129038
- [dnf] Collect legacy yum config symlinks, properly obfuscate pwds
  Resolves: bz2100154

* Fri Sep 09 2022 Pavel Moravec <pmoravec@redhat.com> = 4.4-1
- Rebase on upstream 4.4
  Resolves: bz2082614
- [redhat] Honour credential-less --upload-url on RedHat distro properly
  Resolves: bz2059572
- [sos] Fix unhandled exception when concurrently removing temp dir
  Resolves: bz2088439
- [specfile] drop python3-libxml2 dependency
  Resolves: bz2125486
- [md] Restrict data capture to raid members
  Resolves: bz2125485
- [cleaner] Use compiled regex lists for parsers by default
  Resolves: bz2043233
- [cgroups] not collect memory.kmem.slabinfo
  Resolves: bz1995120
- [report] Fix loop devices data gathering
  Resolves: bz2010735
- [insights] Collect /var/lib/insights
  Resolves: bz2103233
- [candlepin] collect information about SCA
  Resolves: bz2060925
- [manpages] Clarify --upload-directory applicable to FTP protocol only
  Resolves: bz2063259
- [cleaner] Dont obfuscate tmpdir path of local private_map
  Resolves: bz2064815
- [fibrechannel] collect Cisco fnic statistics
  Resolves: bz2074715
- [pulpcore] Collect db_tables_sizes
  Resolves: bz2081433
- [fibrechannel]: Update fibrechannel plugin to collect HBA logs
  Resolves: bz2089591
- [arcconf]: Update arcconf plugin to collect UART logs
  Resolves: bz2090283
- [pulpcore] Stop collecting commands relevant to old taskig system
  Resolves: bz2093191
- [dnf,yum] Merge plugins into dnf, remove yum plugin
  Resolves: bz2100154
- [policies] Simplify flow in _container_init()
  Resolves: bz2100480
- [pacemaker] Update collect cluster profile for pacemaker
  Resolves: bz2065821

* Mon Aug 29 2022 Pavel Moravec <pmoravec@redhat.com> = 4.3-3
- [vdsm] Set LVM option use_devicesfile=0
  Resolves: bz2093993
- [Plugin] Make forbidden path checks more efficient
  Resolves: bz2099598

* Thu Jun 16 2022 Pavel Moravec <pmoravec@redhat.com> = 4.3-2
- [ovirt] answer files: Filter out all password keys
  Resolves: bz2095263
- [plugins] Allow 'str' PlugOpt type to accept any value
  Resolves: bz2079485
- [tigervnc] Update collections for newer versions of TigerVNC
  Resolves: bz2062908
- [pacemaker] Redesign node enumeration logic
  Resolves: bz2065805
- crio: switch from parsing output in table format to json
  Resolves: bz2092969
- [report] Honor plugins' hardcoded plugin_timeout
  Resolves: bz2079187
- [report] --list-plugins should report used, not default,
  Resolves: bz2079484
- [utilities] Close file only when storing to file
  Resolves: bz2079486
- [presets] Adjust OCP preset options, more OCP backports
  Resolves: bz2058279

* Mon Apr 04 2022 Pavel Moravec <pmoravec@redhat.com> = 4.3-1
- Rebase on upstream 4.3
  Resolves: bz2055002
- [sapnw] Fix IndexError exception
  Resolves: bz1992938
- [Plugin, utilities] Allow writing command output directly to disk
  Resolves: bz1726023
- [Ceph] Add support for containerized Ceph setup
  Resolves: bz1882544
- [unbound] Add new plugin for Unbound DNS resolver
  Resolves: bz2018228
- [discovery] Add new discovery plugin
  Resolves: bz2018549
- [vdsm] Exclude /var/lib/vdsm/storage/transient_disks
  Resolves: bz2029154

* Wed Feb 23 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-15
- [sosnode] Handle downstream versioning for runtime option
  Resolves: bz2036697
- [options] Fix logging on plugopts in effective sos command
  Resolves: bz2054882
- [report] Honor plugins' hardcoded plugin_timeout
  Resolves: bz2055547
- [policies] Set fallback to None sysroot, don't chroot to '/'
  Resolves: bz1873185
- [ovn_central] Rename container responsable of Red Hat
  Resolves: bz2042966

* Wed Jan 26 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-13
- [virsh] Catch parsing exception
  Resolves: bz2041488

* Tue Jan 25 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-12
- [foreman] Use psql-msgpack-decode wrapper for dynflow >= 1.6
  Resolves: bz2043102
- [virsh] Call virsh commands in the foreground / with a TTY
  Resolves: bz2041488
- [ovn_central] Account for Red Hat ovn package naming
  Resolves: bz2042966
- [clean,parsers] Build regex lists for static items only once
  Resolves: bz2036697

* Mon Jan 10 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-11
- [report] Add journal logs for NetworkManager plugin
  Resolves: bz2036697

* Fri Jan 07 2022 Pavel Moravec <pmoravec@redhat.com> = 4.2-9
- add oc transport, backport various PRs for OCP
  Resolves: bz2036697
- [report] Provide better warning about estimate-mode
  Resolves: bz1873185
- [hostname] Fix loading and detection of long base domains
  Resolves: bz2023867

* Sun Dec 19 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-8
- [rhui] New log folder
  Resolves: bz2030741
- nvidia]:Patch to update nvidia plugin for GPU info
  Resolves: bz2025403
- [hostname] Fix edge case for new hosts in a known subdomain
  Resolves: bz2023867

* Wed Dec 08 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-7
- [hostname] Simplify case matching for domains
  Resolves: bz2023867

* Tue Nov 30 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-6
- [redhat] Fix broken URI to upload to customer portal
  Resolves: bz2025610

* Mon Nov 22 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-5
- [clean,hostname_parser] Source /etc/hosts for obfuscation
  Resolves: bz2023867
- [clean, hostname] Fix unintentionally case sensitive
  Resolves: bz2023863
- [redhat] update SFTP API version to v2
  Resolves: bz2025610

* Tue Nov 16 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-4
- [report] Calculate sizes of dirs, symlinks and manifest in
  Resolves: bz1873185
- [report] shutdown threads for timeouted plugins
  Resolves: bz2012857
- [report] fix filter_namespace per pattern
  Resolves: bz2020777
- Ensure specific plugin timeouts are only set
  Resolves: bz2018033

* Wed Nov 03 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-2
- [firewall_tables] call iptables -t <table> based on nft
  Resolves: bz2005195
- [report] Count with sos_logs and sos_reports in
  Resolves: bz1873185
- [foreman] Collect puma status and stats
  Resolves: bz2011506
- [report] Overwrite pred=None before refering predicate
  Resolves: bz2012856
- [openvswitch] add commands for offline analysis
  Resolves: bz2004929

* Wed Oct 06 2021 Pavel Moravec <pmoravec@redhat.com> = 4.2-1
- Rebase on upstream 4.2
  Resolves: bz1998133
- [report] Implement --estimate-only
  Resolves: bz1873185
- [omnipath_client] Opacapture to run only with allow changes
  Resolves: bz1998433
- [unpackaged] deal with recursive loop of symlinks properly
  Resolves: bz1998521
- [networking] prevent iptables-save commands to load nf_tables
  Resolves: bz2001096
- [kernel] Capture Pressure Stall Information
  Resolves: bz2002145
- [processor] Apply sizelimit to /sys/devices/system/cpu/cpuX
  Resolves: bz2011413

* Wed Aug 11 2021 Pavel Moravec <pmoravec@redhat.com> = 4.1-5
- [report,collect] unify --map-file arguments
  Resolves: bz1923938
- [rhui] add new plugin for RHUI 4
  Resolves: bz1665947
- [username parser] Load usernames from `last` for LDAP users
  Resolves: bz1985037

* Mon Jul 26 2021 Pavel Moravec <pmoravec@redhat.com> = 4.1-4
- [options] allow variant option names in config file
  Resolves: bz1923938
- [plugins] Set default predicate instead of None
  Resolves: bz1985986
- [MigrationResults] collect info about conversions
  Resolves: bz1959598

* Mon Jun 21 2021 Pavel Moravec <pmoravec@redhat.com> = 4.1-3
- [gluster] collect public keys from the right dir
  Resolves: bz1925419
- [cleaner] Only skip packaging-based files for the IP parse
  Resolves: bz1964499
- [networking] collect also tc filter show ingress
  Resolves: bz1886711
- [archive] skip copying SELinux context for /proc and /sys
  Resolves: bz1965001
- [sssd] sssd plugin when sssd-common
  Resolves: bz1967613
- Various OCP/cluster/cleanup enhancements
  Resolves: bz1973675

* Tue May 18 2021 Pavel Moravec <pmoravec@redhat.com> = 4.1-2
- Load maps from all archives before obfuscation
  Resolves: bz1930181
- Multiple fixes in man pages
  Resolves: bz1935603
- [ds] Mask password and encryption keys in ldif files
  Resolves: bz1937298
- [report] add --cmd-timeout option
  Resolves: bz1937418
- [cups] Add gathering cups-browsed logs
  Resolves: bz1939963
- [sssd] Collect memory cache / individual logfiles
  Resolves: bz1940502
- Collect ibmvNIC dynamic_debugs
  Resolves: bz1942276
- [pulpcore] add plugin for pulp-3
  Resolves: bz1956673
- [saphana] remove redundant unused argument of get_inst_info
  Resolves: bz1959413
- [networking] Add nstat command support
  Resolves: bz1961458
- [snapper] add a new plugin
  Resolves: bz1961229

* Mon Apr 26 2021 Pavel Moravec <pmoravec@redhat.com> = 4.1-1
- Rebase on upstream 4.1
  Resolves: bz1928679

* Tue Feb 16 2021 Pavel Moravec <pmoravec@redhat.com> = 4.0-8
- Automatically create directory for sos-cleaner default_mapping
  Resolves: bz1923937

* Fri Jan 29 2021 Pavel Moravec <pmoravec@redhat.com> = 4.0-7
- [kdump] Gather the file kexec-dmesg.log
  Resolves: bz1887402
- [Policy] Handle additional FTP authentication issues
  Resolves: bz1916729

* Thu Jan 21 2021 Pavel Moravec <pmoravec@redhat.com> = 4.0-6
- [networking] Collect 'ethtool -e <device>' conditionally only
  Resolves: bz1917196

* Wed Jan 06 2021 Pavel Moravec <pmoravec@redhat.com> = 4.0-5
- [component] honour plugopts from config file
  Resolves: bz1912889
- [collector] declare sysroot for each component
  Resolves: bz1912821
- [plugins] Dont stop collecting by empty specfile when sizelimit=0
  Resolves: bz1912910

* Mon Jan 04 2021 Pavel Moravec <pmoravec@redhat.com> = 4.0-4
- [component] Use sysroot from Policy when opts doesn't specify it
  Resolves: bz1881118

* Mon Dec 14 2020 Pavel Moravec <pmoravec@redhat.com> = 4.0-3
- [ovirt] collect /etc/pki/ovirt-engine/.truststore
  Resolves: bz1848095
- [collector] allow overriding plain --cluster-type
  Resolves: bz1895316
- [component] Add log verbosity from presets
  Resolves: bz1904045
- [options] Fix --log-size=0 being ignored and unreported
  Resolves: bz1905657
- [report] collect broken symlinks
  Resolves: bz1906598

* Thu Oct 29 2020 Pavel Moravec <pmoravec@redhat.com> = 4.0-2
- [cleaner] more streamlined sanitize_item method
  Resolves: bz1827801
- [openstack_ironic] Missing ironic-inspector configs
  Resolves: bz1874295
- Add support to collect hardware component logs
  Resolves: bz1880372
- [crio] collect /etc/crio/crio.conf.d/
  Resolves: bz1881118
- [policy] Handle additional failure conditions for FTP uploads
  Resolves: bz1882368
- [filesys] never collect content of /proc/fs/panfs
  Resolves: bz1886782
- [kdump] Collect new kdump logfiles
  Resolves: bz1887390
- [stratis] Collect key list and report engine
  Resolves: bz1888012
- return tmp-dir with absolute path
  Resolves: bz1891562

* Tue Oct 13 2020 Pavel Moravec <pmoravec@redhat.com> = 4.0-1
- Rebase on upstream 4.0
  Resolves: bz1827801
