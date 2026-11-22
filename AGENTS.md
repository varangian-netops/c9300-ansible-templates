# Template rules (read by the local model, Claude Code and its subagents)

Every template lives in `templates/<slug>/` with exactly:
- `site.yml` — the playbook
- `vars.example.yml` — every variable, placeholder defaults, one comment each
- `README.md` — summary, requirements, variables table, usage, what it was tested on, limits
- `tests/results.json` — written ONLY by `ccf validate`; its `site_sha256` must match `site.yml`

## Playbook rules
- Target: Cisco Catalyst 9300, IOS-XE 17.x. `hosts: c9300_switches`, `gather_facts: false`.
- cisco.ios resource modules first (state: merged unless the spec says otherwise). `cisco.ios.ios_config` only when no resource module covers the feature, with idempotent `parents`/`lines`.
- Fully qualified module names. Every task named, starting with a capital letter.
- No hard-coded interface names: use `access_ports` and `uplink_ports`.
- Never touch Ethernet0/0, Mgmt-vrf, AAA, line vty, local users or enable secrets.
- Addresses only from 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24. Hostnames like `ACCESS-SW-01`. Secrets are `vault_*` variables with no literal value.
- A second run must report `changed=0` (idempotency is tested).
- Features that can't run in the IOL-L2 lab (StackWise, PoE, uplink modules, hardware QoS queues) get `hw_only: true` in the backlog item and say so under "Limits".

## Commits
Conventional Commits: `feat(<slug>): …`, `fix(<slug>): …`, `docs(<slug>): …`. One template per PR.
