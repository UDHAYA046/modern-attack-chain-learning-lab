import hashlib
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(exist_ok=True)


PRIMARY_PIN = "sha256/PRIMARY_VALID_CERTIFICATE_PIN"
BACKUP_PIN = "sha256/BACKUP_ROTATION_CERTIFICATE_PIN"

TEST_CERTIFICATES = [
    {
        "name": "Production Certificate",
        "simulated_spki": "production-public-key-material",
        "expected_result": "Allowed"
    },
    {
        "name": "Backup Rotation Certificate",
        "simulated_spki": "backup-public-key-material",
        "expected_result": "Allowed"
    },
    {
        "name": "mitmproxy Generated Certificate",
        "simulated_spki": "mitmproxy-generated-public-key",
        "expected_result": "Blocked"
    },
    {
        "name": "Unknown Rogue Certificate",
        "simulated_spki": "unknown-attacker-public-key",
        "expected_result": "Blocked"
    }
]


def generate_pin(spki_material):
    digest = hashlib.sha256(spki_material.encode()).hexdigest()
    return f"sha256/{digest}"


PRIMARY_PIN = generate_pin("production-public-key-material")
BACKUP_PIN = generate_pin("backup-public-key-material")


def validate_certificate_pin(received_pin):
    if received_pin == PRIMARY_PIN:
        return {
            "allowed": True,
            "matched_pin": "Primary Pin",
            "reason": "Certificate public key matches the primary trusted pin."
        }

    if received_pin == BACKUP_PIN:
        return {
            "allowed": True,
            "matched_pin": "Backup Pin",
            "reason": "Certificate public key matches the backup rotation pin."
        }

    return {
        "allowed": False,
        "matched_pin": "No Match",
        "reason": "Certificate public key does not match trusted primary or backup pins."
    }


def rotate_pins(current_backup_material, new_backup_material):
    new_primary = generate_pin(current_backup_material)
    new_backup = generate_pin(new_backup_material)

    return {
        "rotation_model": "Backup pin becomes primary, new backup pin is added.",
        "new_primary_pin": new_primary,
        "new_backup_pin": new_backup
    }


def run_validation_tests():
    results = []

    for cert in TEST_CERTIFICATES:
        received_pin = generate_pin(cert["simulated_spki"])
        validation = validate_certificate_pin(received_pin)

        results.append({
            "certificate_name": cert["name"],
            "received_pin": received_pin,
            "expected_result": cert["expected_result"],
            "actual_result": "Allowed" if validation["allowed"] else "Blocked",
            "matched_pin": validation["matched_pin"],
            "reason": validation["reason"],
            "security_decision": "PASS" if cert["expected_result"] == ("Allowed" if validation["allowed"] else "Blocked") else "REVIEW"
        })

    return results


def write_report(results):
    report = {
        "lab": "TLS Certificate Pinning Defensive Validation",
        "pinning_model": {
            "algorithm": "SHA256",
            "pinning_type": "SPKI / Public Key Pinning",
            "primary_pin": PRIMARY_PIN,
            "backup_pin": BACKUP_PIN,
            "fail_closed": True
        },
        "rotation_support": rotate_pins(
            "backup-public-key-material",
            "future-public-key-material"
        ),
        "validation_results": results
    }

    output_file = REPORT_DIR / "pinning_validation_report.json"
    output_file.write_text(json.dumps(report, indent=4), encoding="utf-8")

    return output_file


def main():
    results = run_validation_tests()
    output_file = write_report(results)

    print("Certificate pinning validation complete.")
    print(f"Report generated: {output_file}")

    for item in results:
        print(f"{item['certificate_name']} -> {item['actual_result']} ({item['matched_pin']})")


if __name__ == "__main__":
    main()