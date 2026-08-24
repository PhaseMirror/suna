#!/usr/bin/env python3
"""
Phase Mirror Metrics & Audit Tool

Tracks:
1. Number and percentage of CRs/PRs that contain a Phase Mirror block.
2. Fraction of mirrored claims that result in a merged phase within 14 days.
3. Count of open dissonance records older than 30 days.
4. Scan of repository documentation for unhedged 'open source' claims without ELv2 restriction context.

Usage:
  python3 scripts/phase-mirror-metrics.py [--json] [--dir <path>]
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

def parse_dissonance_file(filepath: Path) -> dict:
    """Parse a single dissonance markdown record into a structured dictionary."""
    content = filepath.read_text(encoding="utf-8")
    
    record = {
        "file": str(filepath),
        "filename": filepath.name,
        "id": None,
        "title": None,
        "status": "open",
        "created": None,
        "updated": None,
        "closed": None,
        "owner": None,
        "surface": None,
        "claim": None,
        "mirror": None,
        "dissonance": None,
        "phase_action": None,
        "phase_owner": None,
        "phase_metric": None,
        "target_date": None,
        "age_days": 0,
        "resolution_days": None,
    }
    
    # Title
    title_match = re.search(r"^#\s*DISSONANCE-([0-9]+):\s*(.+)$", content, re.MULTILINE)
    if title_match:
        record["id"] = title_match.group(1).strip()
        record["title"] = title_match.group(2).strip()
    
    # Metadata fields
    for field, key in [
        (r"-\s*\*\*ID:\*\*\s*(.+)", "id"),
        (r"-\s*\*\*Status:\*\*\s*(.+)", "status"),
        (r"-\s*\*\*Created:\*\*\s*(.+)", "created"),
        (r"-\s*\*\*Updated:\*\*\s*(.+)", "updated"),
        (r"-\s*\*\*Closed:\*\*\s*(.+)", "closed"),
        (r"-\s*\*\*Owner:\*\*\s*(.+)", "owner"),
        (r"-\s*\*\*Surface:\*\*\s*(.+)", "surface"),
    ]:
        m = re.search(field, content)
        if m:
            val = m.group(1).strip()
            if key == "status":
                record[key] = val.lower()
            elif key in ("created", "updated", "closed"):
                if val.upper() not in ("N/A", "NONE", ""):
                    record[key] = val
            else:
                record[key] = val

    # Sections
    sections = re.split(r"^##\s+", content, flags=re.MULTILINE)
    for sec in sections:
        lines = sec.strip().split("\n", 1)
        header = lines[0].strip().lower()
        body = lines[1].strip() if len(lines) > 1 else ""
        if header == "claim":
            record["claim"] = body
        elif header == "mirror":
            record["mirror"] = body
        elif header == "dissonance":
            record["dissonance"] = body
        elif header == "phase":
            action_m = re.search(r"-\s*\*\*Action:\*\*\s*(.+)", body)
            if action_m:
                record["phase_action"] = action_m.group(1).strip()
            owner_m = re.search(r"-\s*\*\*Owner:\*\*\s*(.+)", body)
            if owner_m:
                record["phase_owner"] = owner_m.group(1).strip()
            metric_m = re.search(r"-\s*\*\*Metric:\*\*\s*(.+)", body)
            if metric_m:
                record["phase_metric"] = metric_m.group(1).strip()
            target_m = re.search(r"-\s*\*\*Target Date:\*\*\s*(.+)", body)
            if target_m:
                record["target_date"] = target_m.group(1).strip()

    # Calculate ages
    today = datetime.date.today()
    if record["created"]:
        try:
            created_dt = datetime.datetime.strptime(record["created"], "%Y-%m-%d").date()
            record["age_days"] = (today - created_dt).days
            if record["closed"] and record["status"] in ("resolved", "closed"):
                try:
                    closed_dt = datetime.datetime.strptime(record["closed"], "%Y-%m-%d").date()
                    record["resolution_days"] = (closed_dt - created_dt).days
                except ValueError:
                    pass
        except ValueError:
            pass

    return record


def audit_dissonance_records(repo_root: Path) -> list:
    """Find and parse all dissonance records in the repository."""
    dissonance_dirs = [
        repo_root / ".kortix" / "memory" / "dissonance",
        repo_root / "packages" / "starter" / "templates" / "base" / ".kortix" / "memory" / "dissonance",
    ]
    records = []
    seen_ids = set()
    
    for d in dissonance_dirs:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name.lower() in ("readme.md", "index.md"):
                continue
            rec = parse_dissonance_file(f)
            rec_id = rec.get("id") or f.stem
            if rec_id not in seen_ids:
                seen_ids.add(rec_id)
                records.append(rec)
                
    return records


def audit_cr_phase_mirror_blocks(repo_root: Path) -> dict:
    """Analyze commit logs and PR descriptions for Phase Mirror blocks."""
    # Check git log for commits mentioning Phase Mirror or PR template matches
    total_non_trivial_commits = 0
    phase_mirrored_commits = 0
    
    try:
        res = subprocess.run(
            ["git", "log", "-n", "100", "--pretty=format:%H%x09%s%x09%b%x1f"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout:
            entries = res.stdout.split("\x1f")
            for entry in entries:
                if not entry.strip():
                    continue
                parts = entry.strip().split("\t", 2)
                subject = parts[1] if len(parts) > 1 else ""
                body = parts[2] if len(parts) > 2 else ""
                
                # Check if non-trivial
                if any(k in subject.lower() for k in ("fix", "feat", "refactor", "chore", "arch", "harness", "claim")):
                    total_non_trivial_commits += 1
                    if "phase mirror" in (subject + " " + body).lower() or "dissonance:" in body.lower():
                        phase_mirrored_commits += 1
    except Exception:
        pass

    return {
        "sample_commits_checked": total_non_trivial_commits,
        "phase_mirrored_commits": phase_mirrored_commits,
        "coverage_percentage": round((phase_mirrored_commits / total_non_trivial_commits * 100), 1) if total_non_trivial_commits > 0 else 0.0,
    }


def audit_license_claims(repo_root: Path) -> dict:
    """Scan docs and markdown files for unqualified 'open source' claims without ELv2 context."""
    findings = []
    target_exts = {".md", ".txt", ".json", ".yaml", ".yml"}
    
    # We inspect top-level and doc files
    scan_paths = [
        repo_root / "README.md",
        repo_root / "MANIFESTO.md",
        repo_root / "AGENTS.md",
        repo_root / ".claude" / "skills" / "comms" / "SKILL.md",
    ]
    
    for p in scan_paths:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        for idx, line in enumerate(lines, 1):
            if re.search(r"\bopen[- ]source\b", line, re.IGNORECASE):
                has_elv2 = bool(re.search(r"\b(ELv2|Elastic License|source-available)\b", line, re.IGNORECASE))
                findings.append({
                    "file": str(p.relative_to(repo_root)),
                    "line": idx,
                    "content": line.strip()[:120],
                    "has_elv2_context": has_elv2,
                })
                
    unhedged_count = sum(1 for f in findings if not f["has_elv2_context"])
    hedged_count = sum(1 for f in findings if f["has_elv2_context"])
    
    return {
        "total_open_source_mentions": len(findings),
        "hedged_with_elv2": hedged_count,
        "unhedged_mentions": unhedged_count,
        "findings": findings[:10],  # Sample
    }


def generate_report(repo_root: Path) -> dict:
    """Generate complete metrics summary."""
    records = audit_dissonance_records(repo_root)
    cr_metrics = audit_cr_phase_mirror_blocks(repo_root)
    license_metrics = audit_license_claims(repo_root)
    
    open_records = [r for r in records if r["status"] in ("open", "in-progress")]
    resolved_records = [r for r in records if r["status"] == "resolved"]
    accepted_risk_records = [r for r in records if r["status"] == "accepted-risk"]
    
    older_than_30_days = [r for r in open_records if r["age_days"] > 30]
    resolved_within_14_days = [
        r for r in resolved_records if r["resolution_days"] is not None and r["resolution_days"] <= 14
    ]
    
    res_fraction = (
        round(len(resolved_within_14_days) / len(resolved_records), 2)
        if resolved_records
        else 0.0
    )
    
    report = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "summary": {
            "total_dissonance_records": len(records),
            "open_count": len(open_records),
            "resolved_count": len(resolved_records),
            "accepted_risk_count": len(accepted_risk_records),
            "open_older_than_30_days": len(older_than_30_days),
            "fraction_resolved_within_14_days": res_fraction,
        },
        "records": records,
        "open_records_older_than_30_days": older_than_30_days,
        "cr_coverage": cr_metrics,
        "license_audit": license_metrics,
    }
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Phase Mirror Metrics Reporter")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--dir", default=".", help="Target repository root")
    args = parser.parse_args()
    
    repo_root = Path(args.dir).resolve()
    report = generate_report(repo_root)
    
    if args.json:
        print(json.dumps(report, indent=2))
        return
        
    print("=" * 65)
    print("PHASE MIRROR METRICS & AUDIT REPORT")
    print("=" * 65)
    print(f"Timestamp: {report['timestamp']}")
    print()
    print("--- Dissonance Register ---")
    s = report["summary"]
    print(f"Total Dissonance Records:        {s['total_dissonance_records']}")
    print(f"  • Open / In-Progress:          {s['open_count']}")
    print(f"  • Resolved:                    {s['resolved_count']}")
    print(f"  • Accepted Risk:               {s['accepted_risk_count']}")
    print(f"Open Records > 30 Days:          {s['open_older_than_30_days']}")
    print(f"Fraction Resolved <= 14 Days:    {s['fraction_resolved_within_14_days'] * 100:.1f}%")
    print()
    print("--- Active Dissonance Entries ---")
    for r in report["records"]:
        print(f"  [{r['id'] or 'N/A'}] ({r['status'].upper()}) {r['title'] or r['filename']}")
        print(f"      Owner: {r['owner'] or 'Unassigned'} | Target: {r['target_date'] or 'N/A'} | Metric: {r['phase_metric'] or 'N/A'}")
    print()
    print("--- License Claim Audit (Open Source vs ELv2) ---")
    l = report["license_audit"]
    print(f"Total 'Open Source' Mentions:    {l['total_open_source_mentions']}")
    print(f"  • Hedged with ELv2/Terms:      {l['hedged_with_elv2']}")
    print(f"  • Unhedged / Raw Claims:       {l['unhedged_mentions']}")
    print()
    print("=" * 65)


if __name__ == "__main__":
    main()
