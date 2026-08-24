#!/usr/bin/env python3
"""
Test Suite for Phase Mirror Integration

Validates:
1. Skill definition files format and YAML frontmatter.
2. PR/CR template Phase Mirror section.
3. AGENTS.md Phase Mirror gate specification.
4. Memory Dissonance register schema and initial entries.
5. Metrics reporter functionality and JSON schema.
"""

import datetime
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPhaseMirrorIntegration(unittest.TestCase):
    def test_skill_definitions_exist_and_valid(self):
        skill_paths = [
            REPO_ROOT / "skills" / "phase-mirror" / "SKILL.md",
            REPO_ROOT / ".claude" / "skills" / "phase-mirror" / "SKILL.md",
            REPO_ROOT / "packages" / "starter" / "templates" / "base" / ".kortix" / "opencode" / "skills" / "phase-mirror" / "SKILL.md",
        ]
        
        for path in skill_paths:
            self.assertTrue(path.exists(), f"Missing skill file at {path}")
            content = path.read_text(encoding="utf-8")
            
            # Must start with frontmatter ---
            self.assertTrue(content.startswith("---\n"), f"{path} must start with frontmatter ---")
            
            # Extract frontmatter
            parts = content.split("---", 2)
            self.assertGreaterEqual(len(parts), 3, f"{path} must contain closed YAML frontmatter")
            frontmatter = parts[1]
            body = parts[2]
            
            self.assertIn("name: phase-mirror", frontmatter, f"{path} must define name: phase-mirror")
            self.assertIn("description:", frontmatter, f"{path} must define description")
            
            # Required output structure in body
            self.assertIn("Mirror", body, f"{path} body must describe Mirror")
            self.assertIn("Dissonance", body, f"{path} body must describe Dissonance")
            self.assertIn("Phase", body, f"{path} body must describe Phase")
            self.assertIn("ASD-STE100", body, f"{path} body must mention ASD-STE100 standard")

    def test_pr_template_contains_phase_mirror(self):
        pr_template = REPO_ROOT / ".github" / "pull_request_template.md"
        self.assertTrue(pr_template.exists(), "PR template missing")
        content = pr_template.read_text(encoding="utf-8")
        
        self.assertIn("## Phase Mirror", content)
        self.assertIn("- **Claim:**", content)
        self.assertIn("- **Mirror:**", content)
        self.assertIn("- **Dissonance:**", content)
        self.assertIn("- **Phase (Owner + Metric):**", content)

    def test_agents_md_gate(self):
        agents_md = REPO_ROOT / "AGENTS.md"
        self.assertTrue(agents_md.exists(), "AGENTS.md missing")
        content = agents_md.read_text(encoding="utf-8")
        
        self.assertIn("## Phase Mirror: claim vs mechanism gate", content)
        self.assertIn(".kortix/memory/dissonance/", content)
        self.assertIn("Phase Mirror (Claim vs Mechanism)", content)

    def test_dissonance_register_schema(self):
        dissonance_dirs = [
            REPO_ROOT / ".kortix" / "memory" / "dissonance",
            REPO_ROOT / "packages" / "starter" / "templates" / "base" / ".kortix" / "memory" / "dissonance",
        ]
        
        expected_records = [
            "001-open-source-vs-elv2.md",
            "002-memory-durability-vs-plain-files.md",
            "003-security-review-vs-container-defaults.md",
            "004-full-ownership-vs-managed-cloud.md",
        ]

        for dissonance_dir in dissonance_dirs:
            self.assertTrue(dissonance_dir.exists(), f"Dissonance register directory missing at {dissonance_dir}")
            readme = dissonance_dir / "README.md"
            self.assertTrue(readme.exists(), f"Dissonance register README missing at {readme}")
            
            for rec_name in expected_records:
                rec_path = dissonance_dir / rec_name
                self.assertTrue(rec_path.exists(), f"Missing dissonance record {rec_name} in {dissonance_dir}")
                content = rec_path.read_text(encoding="utf-8")
                
                # Check required fields
                self.assertRegex(content, r"^#\s*DISSONANCE-[0-9]+:", f"{rec_name} missing title header")
                self.assertIn("- **ID:**", content, f"{rec_name} missing ID")
                self.assertIn("- **Status:**", content, f"{rec_name} missing Status")
                self.assertIn("- **Created:**", content, f"{rec_name} missing Created")
                self.assertIn("- **Owner:**", content, f"{rec_name} missing Owner")
                self.assertIn("- **Surface:**", content, f"{rec_name} missing Surface")
                self.assertIn("## Claim", content, f"{rec_name} missing Claim section")
                self.assertIn("## Mirror", content, f"{rec_name} missing Mirror section")
                self.assertIn("## Dissonance", content, f"{rec_name} missing Dissonance section")
                self.assertIn("## Phase", content, f"{rec_name} missing Phase section")
                self.assertIn("- **Action:**", content, f"{rec_name} missing Phase Action")
                self.assertIn("- **Owner:**", content, f"{rec_name} missing Phase Owner")
                self.assertIn("- **Metric:**", content, f"{rec_name} missing Phase Metric")
                self.assertIn("## Resolution Log", content, f"{rec_name} missing Resolution Log")

    def test_memory_index_points_to_dissonance(self):
        memory_index = REPO_ROOT / "packages" / "starter" / "templates" / "base" / ".kortix" / "memory" / "MEMORY.md"
        self.assertTrue(memory_index.exists(), "Base MEMORY.md missing")
        content = memory_index.read_text(encoding="utf-8")
        self.assertIn("dissonance/README.md", content, "MEMORY.md must index dissonance/README.md")

    def test_metrics_script(self):
        metrics_script = REPO_ROOT / "scripts" / "phase-mirror-metrics.py"
        self.assertTrue(metrics_script.exists(), "Metrics script missing")
        
        # Test JSON output mode
        res = subprocess.run(
            [sys.executable, str(metrics_script), "--json", "--dir", str(REPO_ROOT)],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(res.stdout)
        self.assertIn("summary", data)
        self.assertGreaterEqual(data["summary"]["total_dissonance_records"], 4)
        self.assertIn("license_audit", data)
        self.assertIn("cr_coverage", data)


if __name__ == "__main__":
    unittest.main()
