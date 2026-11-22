# C9300 Ansible Templates

Lab-tested Ansible templates for Cisco Catalyst 9300 switches (IOS-XE 17.x).
Every template in this repo passed a 7-stage validation before it merged: yamllint, ansible-lint, syntax check, a reset of the lab switches to a clean baseline, check mode, a real apply, and a second apply that must change nothing. Each template's `tests/results.json` holds the result and a SHA-256 of the exact playbook that was tested, and CI rejects any template that has changed since.

## Templates

| Template | What it configures | Lab-tested |
| --- | --- | --- |
| _first release coming soon_ | | |

## Use one

```bash
ansible-galaxy collection install cisco.ios ansible.netcommon
cd templates/<name>
cp vars.example.yml vars.yml   # edit for your network
ansible-playbook -i <your inventory> site.yml -e @vars.yml --check   # always dry-run first
```

Your inventory needs a `c9300_switches` group with `access_ports` and `uplink_ports` lists.

## How they're built

Templates come from a small automation factory: a local LLM drafts each one, Claude reviews and fixes, and a Cisco Modeling Labs topology of IOS-XE switches decides pass or fail. A human approves every template before it's built. See the [release notes](../../releases) for what's new each week.

## Want more?

Advanced templates (access-edge protection, DHCP snooping/DAI, multi-feature site builds) are in the pro collection for sponsors. **[Sponsor to get access →](https://github.com/sponsors/YOUR_ORG)**

Request a template: [open a template request](../../issues/new?template=template-request.yml).

## License

MIT. Test in a lab before production; you're responsible for what you push to your network.
