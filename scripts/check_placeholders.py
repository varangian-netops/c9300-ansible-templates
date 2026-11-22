#!/usr/bin/env python3
"""Fails if a template contains anything that looks like real-world data.

- IPv4 addresses must be in documentation ranges (RFC 5737) or be masks/wildcards.
- No literal secrets: password/secret/key/community values must be {{ vault_* }} variables.
- No protected config: Ethernet0/0, Mgmt-vrf, line vty, aaa, username.
Usage: check_placeholders.py [paths...]   (default: templates/)
"""
import ipaddress, pathlib, re, sys

DOC_NETS = [ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")]
IP_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?![\d.])")
SECRET_RE = re.compile(r"^\s*([\w-]*(password|secret|key|community)[\w-]*)\s*:\s*(.+)$", re.I)
PROTECTED_RE = re.compile(r"(ethernet0/0\b|mgmt-vrf|line vty|^\s*-?\s*['\"]?aaa |username )", re.I)


def is_mask(addr):
    n = int(ipaddress.ip_address(addr))
    inv = n ^ 0xFFFFFFFF
    return (n & (n + 1) == 0) or (inv & (inv + 1) == 0)  # wildcard (0..01..1) or netmask (1..10..0)


def allowed_ip(text):
    try:
        ip = ipaddress.ip_address(text)
    except ValueError:
        return True  # not an IP (e.g. a version string like 17.12.1.0 is still caught above as invalid)
    return any(ip in n for n in DOC_NETS) or is_mask(text) or text == "0.0.0.0"


def check(path):
    problems = []
    for no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        for m in IP_RE.finditer(line):
            if not allowed_ip(m.group(1)):
                problems.append(f"{path}:{no}: non-documentation IP {m.group(1)} (use 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24)")
        s = SECRET_RE.match(line)
        if s and not re.search(r"\{\{\s*vault_\w+", s.group(3)) and s.group(3).strip() not in ('""', "''", "null", "~"):
            if path.name != "README.md":
                problems.append(f"{path}:{no}: literal value for '{s.group(1)}' (use a vault_* variable)")
        if path.suffix in (".yml", ".yaml") and PROTECTED_RE.search(line):
            problems.append(f"{path}:{no}: touches protected config: {line.strip()[:80]}")
    return problems


def main():
    roots = [pathlib.Path(p) for p in (sys.argv[1:] or ["templates"])]
    files = [f for r in roots for f in ([r] if r.is_file() else r.rglob("*"))
             if f.is_file() and f.suffix in (".yml", ".yaml", ".md", ".j2") and "tests" not in f.parts]
    problems = [p for f in files for p in check(f)]
    for p in problems:
        print(p)
    print(f"{len(files)} files checked, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
