#!/usr/bin/env python3
"""
Generate audit bundle for v0.3.2 healthcare classifier example
EU AI Act Art. 6(2) high-risk system compliance
"""
import hashlib
import json
from datetime import datetime
from pathlib import Path


def sha256_file(path):
    """Compute SHA-256 hash of file"""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()


def sha256_str(text):
    """Compute SHA-256 hash of string"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def create_audit_bundle():
    """Create comprehensive audit bundle"""

    # Healthcare classifier scenario (EU AI Act Art. 6(2): high-risk)
    scenario = {
        "use_case": "Healthcare Support Ticket Classification",
        "risk_level": "high-risk",
        "eu_ai_act_article": "Article 6(2)",
        "deployment_date": "2025-10-10",
        "system_version": "0.3.2",
    }

    # Contracts
    ep_content = {
        "prompt_template": "Classify this healthcare support ticket: {input_text}",
        "model": "gpt-4o-mini",
        "temperature": 0.0,
        "seed": 42,
    }

    es_content = {
        "output_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["urgent", "routine", "billing", "technical"],
                },
                "priority": {"type": "integer", "minimum": 1, "maximum": 5},
            },
            "required": ["category", "priority"],
        }
    }

    pd_content = {
        "checks": [
            {"type": "json_valid", "severity": "error"},
            {"type": "json_required", "severity": "error", "keys": ["category", "priority"]},
            {
                "type": "enum_value",
                "severity": "error",
                "field": "category",
                "allowed": ["urgent", "routine", "billing", "technical"],
            },
            {"type": "latency_budget", "severity": "warn", "max_ms": 3000},
        ]
    }

    # Simulated run artifacts
    input_final = "Classify this healthcare support ticket: Patient experiencing severe chest pain, requesting immediate callback."
    output_raw = '```json\n{"category": "urgent", "priority": 5}\n```'
    output_norm = '{"category": "urgent", "priority": 5}'

    run_metadata = {
        "timestamp": datetime.now().isoformat(),
        "seed": 42,
        "temperature": 0.0,
        "model": "gpt-4o-mini",
        "checks_passed": ["json_valid", "json_required", "enum_value"],
        "checks_warned": [],
        "checks_failed": [],
        "repair_ledger": [
            {"step": "strip_markdown_fences", "applied": True, "semantic_change": False}
        ],
        "prompt_hash_sha256": sha256_str(input_final),
        "output_hash_sha256": sha256_str(output_norm),
        "latency_ms": 1245,
        "tokens_used": 87,
    }

    # Audit manifest
    manifest = {
        "audit_bundle_version": "1.0",
        "system": scenario,
        "contracts": {
            "ep": {
                "content": ep_content,
                "sha256": sha256_str(json.dumps(ep_content, sort_keys=True)),
            },
            "es": {
                "content": es_content,
                "sha256": sha256_str(json.dumps(es_content, sort_keys=True)),
            },
            "pd": {
                "content": pd_content,
                "sha256": sha256_str(json.dumps(pd_content, sort_keys=True)),
            },
        },
        "artifacts": {
            "input_final.txt": {"content": input_final, "sha256": sha256_str(input_final)},
            "output_raw.txt": {"content": output_raw, "sha256": sha256_str(output_raw)},
            "output_norm.txt": {"content": output_norm, "sha256": sha256_str(output_norm)},
            "run.json": {
                "content": run_metadata,
                "sha256": sha256_str(json.dumps(run_metadata, sort_keys=True)),
            },
        },
        "compliance": {
            "iso_29119_8_3": {
                "requirement": "Test log with inputs, outputs, timestamps",
                "status": "compliant",
                "evidence": ["run.json contains timestamp, seed, all I/O"],
            },
            "eu_ai_act_art_12": {
                "requirement": "Immutable audit trail with SHA-256 hashes",
                "status": "compliant",
                "evidence": ["All artifacts have SHA-256 hashes", "Repair ledger included"],
            },
            "eu_ai_act_art_13": {
                "requirement": "Transparency through capability negotiation log",
                "status": "compliant",
                "evidence": [
                    "Checks clearly document validation steps",
                    "Repair ledger shows transformations",
                ],
            },
            "eu_ai_act_art_14": {
                "requirement": "Human oversight mechanisms",
                "status": "compliant",
                "evidence": [
                    "Failed checks trigger human review",
                    "Repair ledger allows verification",
                ],
            },
        },
        "metadata": {
            "created": datetime.now().isoformat(),
            "promptcontracts_version": "0.3.2",
            "python_version": "3.11.7",
            "reproducibility_seed": 42,
            "audit_bundle_sha256": "to_be_computed_after_serialization",
        },
    }

    # Write to file
    output_dir = Path(__file__).parent.parent / "examples" / "audit"
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle_path = output_dir / "audit_bundle.json"
    bundle_json = json.dumps(manifest, indent=2)

    # Compute final hash
    manifest["metadata"]["audit_bundle_sha256"] = sha256_str(bundle_json)

    # Re-serialize with final hash
    bundle_json = json.dumps(manifest, indent=2)
    bundle_path.write_text(bundle_json)

    print(f"✅ Audit bundle created: {bundle_path}")
    print(f"   SHA-256: {manifest['metadata']['audit_bundle_sha256']}")
    print("\n📋 Compliance Status:")
    for standard, details in manifest["compliance"].items():
        print(f"   {standard}: {details['status']}")

    # Also save individual artifacts for reference
    for artifact_name, artifact_data in manifest["artifacts"].items():
        artifact_path = output_dir / artifact_name
        if isinstance(artifact_data["content"], dict):
            artifact_path.write_text(json.dumps(artifact_data["content"], indent=2))
        else:
            artifact_path.write_text(artifact_data["content"])

    print(f"\n✅ Individual artifacts saved to: {output_dir}")

    return manifest


if __name__ == "__main__":
    create_audit_bundle()
