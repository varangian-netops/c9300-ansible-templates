#!/usr/bin/env python3
"""Proves each template was lab-tested in its current form.
For every templates/<slug>/ given (default: all), tests/results.json must exist, say
"status": "pass", and its site_sha256 must equal the SHA-256 of the current site.yml.
"""
import hashlib, json, pathlib, sys


def check(d):
    site, res = d / "site.yml", d / "tests" / "results.json"
    if not site.exists():
        return [f"{d}: missing site.yml"]
    if not res.exists():
        return [f"{d}: missing tests/results.json (run: ccf validate <id>)"]
    try:
        r = json.loads(res.read_text())
    except json.JSONDecodeError as e:
        return [f"{res}: invalid JSON ({e})"]
    out = []
    if r.get("status") != "pass":
        out.append(f"{d}: validator status is {r.get('status')!r}, failed at {r.get('failed_stage')!r}")
    sha = hashlib.sha256(site.read_bytes()).hexdigest()
    if r.get("site_sha256") != sha:
        out.append(f"{d}: site.yml changed after it was tested (sha mismatch) — re-run ccf validate")
    return out


def main():
    dirs = [pathlib.Path(p) for p in sys.argv[1:]] or sorted(p for p in pathlib.Path("templates").glob("*") if p.is_dir())
    problems = [p for d in dirs for p in check(d)]
    for p in problems:
        print(p)
    print(f"{len(dirs)} templates checked, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
