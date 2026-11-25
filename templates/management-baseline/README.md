# management-baseline

This Ansible template configures a baseline management plane on Cisco Catalyst 9300 switches. It configures NTP servers, syslog hosts and buffered logging, enables LLDP, sets a login banner, and adds datetime timestamps to log messages.

## Requirements
- **ansible-core**: 2.17 or 2.18 (the range CI installs)
- **cisco.ios collection**: not version-pinned; CI installs the current release
- **IOS-XE 17.x**: The target switches must run this version of IOS-XE.

## Variables
Defaults below match `vars.example.yml`.

| Name                     | Default Value                                                        | Meaning                                                  |
|--------------------------|----------------------------------------------------------------------|----------------------------------------------------------|
| `ntp_servers`            | `[{server: 192.0.2.1}, {server: 192.0.2.2}]`                         | List of NTP servers (list of dicts, key `server`).       |
| `syslog_hosts`           | `[{hostname: 192.0.2.3}]`                                            | List of syslog hosts (list of dicts, key `hostname`).    |
| `buffered_logging_level` | `informational`                                                      | Buffered logging severity level.                         |
| `buffered_logging_size`  | `16384`                                                              | Buffered logging size in bytes.                          |
| `lldp_enabled`           | `true`                                                               | Enable LLDP globally.                                    |
| `login_banner`           | `"Authorized access only - ACCESS-SW-01"`                            | Login banner text.                                       |
| `timestamps_on_logs`     | `true`                                                               | Add datetime timestamps to log messages.                 |

## Usage
Create an inventory file with a group `c9300_switches` that contains your switches. Then run the playbook:

```sh
ansible-playbook site.yml -i inventory.ini -e @vars.example.yml --check
```

Replace `inventory.ini` with the path to your inventory file. Drop `--check` to apply the configuration.

## What it was tested on
This template was tested on the CML-Free IOL-L2 x2 (IOS-XE 17.x) lab environment. It passed all 7 validator stages, including yamllint, ansible-lint, syntax, reset, check, apply, and idempotency.

## Limits
- This template is designed for Cisco Catalyst 9300 switches running IOS-XE 17.x.
- LLDP is enabled with the `lldp run` command through `cisco.ios.ios_config`. The LLDP resource module cannot enable LLDP globally.
- Log timestamps (`service timestamps log datetime msec`) also use `cisco.ios.ios_config`, because no resource module covers that command.
- Replace the example 192.0.2.x NTP and syslog addresses in `vars.example.yml` with your own before applying.

Advanced templates (access-edge protection, DHCP snooping/DAI, multi-feature site builds) are in the pro collection for sponsors: **[Sponsor to get access →](https://github.com/sponsors/varangian-netops)**
