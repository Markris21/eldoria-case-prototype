from dataclasses import replace

import pytest

from case_generator import generate_case
from case_knowledge import derive_knowledge


@pytest.mark.parametrize("seed", range(20))
def test_generated_case_has_distinct_patient_and_witness(seed: int) -> None:
    case = generate_case(seed)

    assert case.patient != case.witness


def test_knowledge_is_deterministic_for_same_seed() -> None:
    first = generate_case(18472)
    second = generate_case(18472)

    assert derive_knowledge(first.event_records, first.patient) == derive_knowledge(
        second.event_records, second.patient
    )
    assert derive_knowledge(first.event_records, first.witness) == derive_knowledge(
        second.event_records, second.witness
    )


def test_patient_knows_events_they_participated_in() -> None:
    case = generate_case(18472)
    knowledge = derive_knowledge(case.event_records, case.patient)

    assert tuple(fact.source_event_id for fact in knowledge) == (
        "presence",
        "contact",
        "affected",
    )


def test_witness_knows_presence_and_observed_contact_only() -> None:
    case = generate_case(18472)
    knowledge = derive_knowledge(case.event_records, case.witness)

    assert tuple(fact.source_event_id for fact in knowledge) == ("presence", "contact")
    assert "affected" not in {fact.source_event_id for fact in knowledge}


@pytest.mark.parametrize("participant_role", ("patient", "witness"))
def test_every_known_fact_has_matching_event_provenance(participant_role: str) -> None:
    case = generate_case(18472)
    participant = getattr(case, participant_role)
    events_by_id = {event.event_id: event for event in case.event_records}

    for known_fact in derive_knowledge(case.event_records, participant):
        source_event = events_by_id[known_fact.source_event_id]
        assert known_fact.fact == source_event.fact
        assert participant in source_event.participants or participant in source_event.observers


def test_removing_observation_removes_derived_contact_knowledge() -> None:
    case = generate_case(18472)
    changed_case = replace(case, contact_observers=())

    original_knowledge = derive_knowledge(case.event_records, case.witness)
    changed_knowledge = derive_knowledge(changed_case.event_records, changed_case.witness)

    assert "contact" in {fact.source_event_id for fact in original_knowledge}
    assert "contact" not in {fact.source_event_id for fact in changed_knowledge}
