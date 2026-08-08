import pytest

from case_generator import (
    ALLOWED_CONTACTS_BY_LOCATION,
    CONTACTS,
    LOCATIONS,
    PATIENT_NAMES,
    SOURCE,
    format_report,
    generate_case,
)


def test_same_seed_generates_identical_case() -> None:
    first = generate_case(18472)
    second = generate_case(18472)

    assert first == second
    assert format_report(first) == format_report(second)


@pytest.mark.parametrize("seed", range(20))
def test_generated_case_contains_required_truth(seed: int) -> None:
    case = generate_case(seed)
    report = format_report(case)

    assert case.seed == seed
    assert case.patient in PATIENT_NAMES
    assert case.source == SOURCE
    assert case.location == LOCATIONS[case.location_id]
    assert case.contact == CONTACTS[case.contact_id]
    assert len(case.events) == 4
    assert all(case.patient in event or case.source in event for event in case.events)
    assert len(case.causal_chain) == 5
    assert str(seed) in report
    assert case.patient in report
    assert case.source in report
    assert case.location in report
    assert case.contact in report


@pytest.mark.parametrize("seed", range(100))
def test_contact_is_allowed_at_generated_location(seed: int) -> None:
    case = generate_case(seed)

    assert case.contact_id in ALLOWED_CONTACTS_BY_LOCATION[case.location_id]


def test_sample_contains_more_than_one_composed_variant() -> None:
    variants = {
        (case.patient, case.location_id, case.contact_id)
        for case in (generate_case(seed) for seed in range(20))
    }

    assert len(variants) > 1
