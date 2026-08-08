from dataclasses import replace

from case_generator import ALLOWED_CONTACTS_BY_LOCATION, CONTACTS, generate_case
from case_validator import validate_case


def test_generated_case_is_valid() -> None:
    result = validate_case(generate_case(18472))

    assert result.is_valid
    assert result.reasons == ()
    assert str(result) == "VALID"


def test_incompatible_location_and_contact_is_invalid() -> None:
    case = generate_case(18472)
    invalid_contact_id = next(
        contact_id
        for contact_id in CONTACTS
        if contact_id not in ALLOWED_CONTACTS_BY_LOCATION[case.location_id]
    )
    invalid_case = replace(
        case,
        contact_id=invalid_contact_id,
        contact=CONTACTS[invalid_contact_id],
    )

    result = validate_case(invalid_case)

    assert not result.is_valid
    assert result.reasons == (
        f"contact '{invalid_contact_id}' is not allowed at location '{case.location_id}'",
    )


def test_missing_required_value_is_invalid() -> None:
    invalid_case = replace(generate_case(18472), patient="")

    result = validate_case(invalid_case)

    assert not result.is_valid
    assert result.reasons == ("missing required value: patient",)


def test_impossible_chronology_is_invalid() -> None:
    case = generate_case(18472)
    invalid_case = replace(case, affected_day=case.contact_day - 1)

    result = validate_case(invalid_case)

    assert not result.is_valid
    assert result.reasons == ("patient must become affected after contact",)
