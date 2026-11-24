# Trunk uplinks with allowed VLAN pruning

This Ansible template configures Cisco Catalyst 9300 switches to use 802.1Q trunk interfaces with a configurable native VLAN and allowed VLAN list. It also sets descriptions for each uplink port.

#### Requirements
- Ansible-core: 2.10 or later
- cisco.ios collection: 2.0 or later
- IOS-XE 17.x

#### Variables
| Name                 | Default     | Meaning                                                                 |
|----------------------|-------------|-------------------------------------------------------------------------|
| `uplink_ports`       | `[Ethernet0/1, Ethernet0/2]` | List of uplink ports to configure as trunk interfaces. Set it for your switches. |
| `allowed_vlans`      | `[10, 20, 30]` | VLANs allowed on the trunks (all others are pruned). Set it for your network. |
| `native_vlan`        | `99`        | Native VLAN for trunk interfaces.                                       |
| `uplink_port_descriptions` | see `vars.example.yml` | Description per uplink, keyed by interface name. Ports without an entry get `Uplink to Core Switch`. |

#### Usage
To use this template, ensure your inventory file has a group `c9300_switches` containing the target switches. Run the playbook with the following command:

```sh
cp vars.example.yml my_vars.yml
ansible-playbook -i inventory.yml site.yml -e @my_vars.yml --check
```

Edit `my_vars.yml` for your switches first; `-e` overrides the defaults that `site.yml` loads from `vars.example.yml`. Replace `inventory.yml` with your actual inventory file. The `--check` option is recommended to ensure the playbook runs as expected without making any changes.

#### What it was tested on
- Lab: CML-Free IOL-L2 x2 (IOS-XE 17.x)
- Stages passed: yamllint, ansible-lint, syntax, reset, check, apply, idempotency
- Date: 2026-11-24

#### Limits
- This template assumes the switches are running IOS-XE 17.x.
- It does not create the native or allowed VLANs; VLAN 99 and the allowed VLANs must already exist.
- `Ethernet0/1` and `Ethernet0/2` are lab placeholders; a real 9300 uses names like `GigabitEthernet1/1/1`.
- `state: merged` adds to existing trunk settings and does not remove stale allowed VLANs.
- `allowed_vlans` must not be empty.

Advanced templates (access-edge protection, DHCP snooping/DAI, multi-feature site builds) are in the pro collection for sponsors: **[Sponsor to get access →](https://github.com/sponsors/varangian-netops)**
