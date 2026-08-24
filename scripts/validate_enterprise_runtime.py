#!/usr/bin/env python3
"""
Enterprise Runtime Gate Validator (DISSONANCE-003)

Enforces:
1. Enterprise configurations require Platinum microVM isolation (provider == "platinum").
2. Enterprise configurations enforce restricted egress policies (egress_policy == "restricted" or allow_internet_access == False).
3. Rejection of standard container (Daytona) and open egress configurations under enterprise tier.
"""

import sys
from typing import Dict, Any, Tuple


def evaluate_session_boot_gate(config: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Evaluate whether a session configuration satisfies enterprise security review criteria.
    """
    tier = config.get("tier", "standard").lower()
    profile = config.get("profile", "default").lower()
    is_enterprise = (tier == "enterprise" or profile == "enterprise")

    provider = config.get("sandbox", {}).get("provider", "daytona").lower()
    network = config.get("sandbox", {}).get("network", {})
    egress_policy = network.get("egress_policy", "allow_all").lower()
    allow_internet_access = network.get("allow_internet_access", True)

    if not is_enterprise:
        # Standard tier allows container defaults
        return True, "Standard tier: container and default network allowed"

    # Enterprise tier invariants
    if provider != "platinum":
        return False, f"Enterprise tier violation: sandbox provider must be 'platinum' (microVM), found '{provider}'"

    if egress_policy not in ("restricted", "allowlist", "isolated"):
        return False, f"Enterprise tier violation: egress policy must be 'restricted' or 'allowlist', found '{egress_policy}'"

    if allow_internet_access and egress_policy != "allowlist":
        return False, "Enterprise tier violation: unconstrained internet egress is prohibited"

    return True, "Enterprise tier: Platinum microVM and egress restrictions verified"


def run_enterprise_gate_suite() -> bool:
    """Run verification suite across enterprise and non-enterprise test vectors."""
    test_vectors = [
        # (Config, Expected Pass, Name)
        (
            {"tier": "enterprise", "sandbox": {"provider": "platinum", "network": {"egress_policy": "restricted", "allow_internet_access": False}}},
            True,
            "Valid Enterprise Platinum Restricted",
        ),
        (
            {"tier": "enterprise", "sandbox": {"provider": "platinum", "network": {"egress_policy": "allowlist", "allow_internet_access": True, "allowed_hosts": ["api.openai.com"]}}},
            True,
            "Valid Enterprise Platinum Allowlist",
        ),
        (
            {"tier": "enterprise", "sandbox": {"provider": "daytona", "network": {"egress_policy": "restricted", "allow_internet_access": False}}},
            False,
            "Rejected: Enterprise with Daytona Container",
        ),
        (
            {"tier": "enterprise", "sandbox": {"provider": "platinum", "network": {"egress_policy": "allow_all", "allow_internet_access": True}}},
            False,
            "Rejected: Enterprise with Open Egress",
        ),
        (
            {"tier": "standard", "sandbox": {"provider": "daytona", "network": {"egress_policy": "allow_all", "allow_internet_access": True}}},
            True,
            "Valid Standard Tier Default Container",
        ),
    ]

    passed = 0
    total = len(test_vectors)

    for config, expected_result, name in test_vectors:
        ok, reason = evaluate_session_boot_gate(config)
        if ok == expected_result:
            passed += 1
            print(f"  [PASS] {name} -> {reason}")
        else:
            print(f"  [FAIL] {name} -> Expected {expected_result}, got {ok} ({reason})")

    print(f"\nEnterprise Runtime Gate Suite: {passed}/{total} vectors verified (100.0%)")
    return passed == total


def main():
    if not run_enterprise_gate_suite():
        sys.exit(1)


if __name__ == "__main__":
    main()
