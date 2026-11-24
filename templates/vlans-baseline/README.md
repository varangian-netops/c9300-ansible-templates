# vlans-baseline

This Ansible template creates VLANs and assigns access ports on Cisco Catalyst 9300 switches. It ensures that every port in the `access_ports` list is set to an access VLAN and enabled with a specified description.

## Requirements
- **ansible-core**: 2.17 or 2.18 (the range CI installs)
- **cisco.ios collection**: not version-pinned; CI installs the current release
- **IOS-XE 17.x**: The target switches must run this version of IOS-XE.

## Variables
Defaults below match `vars.example.yml`.

| Name                      | Default                                              | Meaning                                                    |
|---------------------------|------------------------------------------------------|------------------------------------------------------------|
| `vlans`                   | 10 USERS, 20 VOICE, 30 PRINTERS, 99 PARKING          | List of VLANs to create, each with an `id` and `name`.     |
| `access_vlan`             | 10                                                   | VLAN ID assigned to every port in `access_ports`.          |
| `access_port_description` | "Access port"                                        | Description applied to every access port.                  |

`access_ports` is required, and it is not in `vars.example.yml`. Define it in your inventory (host_vars or group_vars). `uplink_ports` is also not in `vars.example.yml`; this template does not read it, because `site.yml` does not reference it.

Example inventory (`host_vars/ACCESS-SW-01.yml`):

```yaml
ansible_network_os: cisco.ios.ios
access_ports:
  - GigabitEthernet1/0/2
  - GigabitEthernet1/0/3
  - GigabitEthernet1/0/4
# Not read by this template. Shown for the shared inventory layout.
uplink_ports:
  - TenGigabitEthernet1/1/1
```

Host entry (`inventory/hosts.yml`):

```yaml
all:
  children:
    c9300_switches:
      hosts:
        ACCESS-SW-01:
          ansible_host: 192.0.2.11
```

## Usage
1. **Inventory**: Create a group named `c9300_switches` and define `access_ports` for each host, as shown above.
2. **Run Command**: Execute the playbook with the example variables file and `--check` first to simulate the changes.
   ```bash
   ansible-playbook -i inventory site.yml -e @vars.example.yml --check
   ```
3. **Apply Changes**: If the check is successful, apply the changes.
   ```bash
   ansible-playbook -i inventory site.yml -e @vars.example.yml
   ```

## What it was tested on
- **Lab**: CML-Free IOL-L2 x2 (IOS-XE 17.x)
- **Result**: pass
- **Stages Passed**: yamllint, ansible-lint, syntax, reset, check, apply, idempotency
- **Date**: 2026-11-23T20:26:36

## Limits
- This template is designed for Catalyst 9300 switches running IOS-XE 17.x.
- Tested only in the CML-Free IOL-L2 lab. IOL-L2 is a virtual Layer 2 image, not Catalyst 9300 hardware. It has not been run on physical hardware.
- It reads only `access_ports`. It does not configure `uplink_ports` or trunks.
- It uses `state: merged`. It does not remove VLANs or reset ports that are not in the lists.

Advanced templates (access-edge protection, DHCP snooping/DAI, multi-feature site builds) are in the pro collection for sponsors: **[Sponsor to get access →](https://github.com/sponsors/varangian-netops)**
