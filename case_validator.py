"""Minimal consistency validator experiment for generated case truths."""

from __future__ import annotations

from dataclasses import dataclass, replace

from case_generator import (
    ALLOWED_CONTACTS_BY_LOCATION,
    CONTACTS,
    CaseTruth,
    generate_case,
)


@dataclass(frozen=True)
class ValidationResult:
    """Machine-readable result of validating one case truth."""

    is_valid: bool
    reasons: tuple[str, ...]

    def __str__(self) -> str:
        if self.is_valid:
            return "VALID"

        reasons = "\n".join(f"- {reason}" for reason in self.reasons)
        return f"INVALID\nReasons:\n{reasons}"


def validate_case(case: CaseTruth) -> ValidationResult:
    """Detect the three consistency failures covered by the Stage 2 experiment."""

    reasons: list[str] = []

    required_values = {
        "patient": case.patient,
        "source": case.source,
        "location_id": case.location_id,
        "location": case.location,
        "contact_id": case.contact_id,
        "contact": case.contact,
    }
    for field_name, value in required_values.items():
        if not value.strip():
            reasons.append(f"missing required value: {field_name}")

    allowed_contacts = ALLOWED_CONTACTS_BY_LOCATION.get(case.location_id)
    if allowed_contacts is not None and case.contact_id not in allowed_contacts:
        reasons.append(
            f"contact '{case.contact_id}' is not allowed at location '{case.location_id}'"
        )

    if case.affected_day <= case.contact_day:
        reasons.append("patient must become affected after contact")

    return ValidationResult(is_valid=not reasons, reasons=tuple(reasons))


def main() -> None:
    valid_case = generate_case(18472)
    invalid_contact_id = next(
        contact_id
        for contact_id in CONTACTS
        if contact_id not in ALLOWED_CONTACTS_BY_LOCATION[valid_case.location_id]
    )

    demonstrations = (
        ("Generated case", valid_case),
        (
            "Invalid location/contact combination",
            replace(
                valid_case,
                contact_id=invalid_contact_id,
                contact=CONTACTS[invalid_contact_id],
            ),
        ),
        ("Missing required patient", replace(valid_case, patient="")),
        (
            "Impossible chronology",
            replace(valid_case, affected_day=valid_case.contact_day - 1),
        ),
    )

    for index, (label, case) in enumerate(demonstrations):
        if index:
            print()
        print(f"{label}:\n{validate_case(case)}")


if __name__ == "__main__":
    main()
