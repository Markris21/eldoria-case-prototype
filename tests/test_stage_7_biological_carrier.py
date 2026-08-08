from dataclasses import fields, replace

from case_diversity import (
    InvestigationStructureSignature,
    analyze_diversity,
    investigation_structure_signature,
)
from case_generator import (
    BIOLOGICAL_CARRIER_ARCHETYPE,
    ENVIRONMENTAL_ARCHETYPE,
    ENVIRONMENTAL_CONTACTS_BY_LOCATION,
    generate_case,
)
from case_interview import (
    TOPICS,
    UNKNOWN_ANSWER,
    Hypothesis,
    ask_topic,
    format_initial_report,
    hypotheses_for,
    is_correct_hypothesis,
    run_interview,
)
from case_knowledge import derive_knowledge
from case_validator import validate_case


ENVIRONMENTAL_SEED = 18472
BIOLOGICAL_SEED = 1


def topic(topic_id: str):
    return next(item for item in TOPICS if item.topic_id == topic_id)


def event(case, event_id: str):
    return next(item for item in case.event_records if item.event_id == event_id)


def ask(case, participant: str, topic_id: str) -> str:
    knowledge = derive_knowledge(case.event_records, participant)
    return ask_topic(knowledge, topic(topic_id), [])


def test_known_seed_generates_biological_carrier_archetype() -> None:
    case = generate_case(BIOLOGICAL_SEED)

    assert case.archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE
    assert case.contact_id == "carrier_contact"
    assert case.carrier == case.witness


def test_biological_case_is_deterministic() -> None:
    first = generate_case(BIOLOGICAL_SEED)
    second = generate_case(BIOLOGICAL_SEED)

    assert first == second
    assert first.event_records == second.event_records
    assert hypotheses_for(first) == hypotheses_for(second)


def test_carrier_is_distinct_from_patient() -> None:
    case = generate_case(BIOLOGICAL_SEED)

    assert case.carrier is not None
    assert case.carrier != case.patient


def test_carrier_truth_and_chronology_are_coherent() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    contact = event(case, "contact")
    carrier_condition = event(case, "carrier_condition")

    assert case.carrier_condition_day is not None
    assert case.carrier_condition_day < case.contact_day < case.affected_day
    assert contact.participants == (case.patient, case.carrier)
    assert carrier_condition.participants == (case.carrier,)
    assert carrier_condition.observers == (case.patient,)
    assert validate_case(case).is_valid


def test_observable_carrier_facts_do_not_reveal_hidden_causation() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    report = format_initial_report(case)

    assert case.source not in report
    assert case.carrier not in report
    for participant in (case.patient, case.carrier):
        assert participant is not None
        for known_fact in derive_knowledge(case.event_records, participant):
            observable = known_fact.fact.lower()
            assert case.source not in known_fact.fact
            assert "carrier" not in observable
            assert "infect" not in observable
            assert "transmission" not in observable
            assert "caused" not in observable


def test_biological_interview_uses_neutral_participant_label(
    monkeypatch, capsys
) -> None:
    case = generate_case(BIOLOGICAL_SEED)
    answers = iter(("0", "0"))
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    run_interview(case)

    participant_menu = capsys.readouterr().out.split("0. End interview", 1)[0]
    assert f"2. {case.carrier} (participant)" in participant_menu
    for hidden_role_word in ("carrier", "infected", "source", "transmission"):
        assert hidden_role_word not in participant_menu.lower()


def test_carrier_knowledge_comes_only_from_event_involvement_with_provenance() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    assert case.carrier is not None
    events_by_id = {item.event_id: item for item in case.event_records}
    knowledge = derive_knowledge(case.event_records, case.carrier)

    assert tuple(fact.source_event_id for fact in knowledge) == (
        "presence",
        "contact",
        "carrier_condition",
    )
    for known_fact in knowledge:
        source_event = events_by_id[known_fact.source_event_id]
        assert known_fact.fact == source_event.fact
        assert (
            case.carrier in source_event.participants
            or case.carrier in source_event.observers
        )


def test_removing_observation_removes_patient_carrier_condition_knowledge() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    changed_case = replace(case, carrier_condition_observers=())

    original_ids = {
        fact.source_event_id
        for fact in derive_knowledge(case.event_records, case.patient)
    }
    changed_ids = {
        fact.source_event_id
        for fact in derive_knowledge(changed_case.event_records, changed_case.patient)
    }

    assert "carrier_condition" in original_ids
    assert "carrier_condition" not in changed_ids
    assert "carrier_causation" not in original_ids


def test_biological_case_has_exactly_one_correct_hypothesis_out_of_two() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    hypotheses = hypotheses_for(case)

    assert len(hypotheses) == 2
    assert sum(is_correct_hypothesis(case, item) for item in hypotheses) == 1
    alternative = next(
        item for item in hypotheses if not is_correct_hypothesis(case, item)
    )
    assert alternative.contact_id in ENVIRONMENTAL_CONTACTS_BY_LOCATION[
        case.location_id
    ]


def test_biological_hypothesis_evaluation_uses_case_truth_not_observations() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    case_without_condition_observation = replace(
        case, carrier_condition_observers=()
    )
    selected = Hypothesis("Same proposed cause", case.contact_id)

    assert is_correct_hypothesis(case, selected)
    assert is_correct_hypothesis(case_without_condition_observation, selected)


def test_interview_exposes_contact_and_prior_carrier_condition() -> None:
    case = generate_case(BIOLOGICAL_SEED)

    contact_answer = ask(case, case.patient, "contact")
    condition_answer = ask(case, case.patient, "carrier_condition")

    assert case.carrier in contact_answer
    assert "spent time" in contact_answer
    assert case.carrier in condition_answer
    assert "visibly unwell before" in condition_answer


def test_biological_deduction_does_not_depend_on_food_history() -> None:
    case = generate_case(BIOLOGICAL_SEED)

    assert "food_history" not in {item.event_id for item in case.event_records}
    assert ask(case, case.patient, "food") == UNKNOWN_ANSWER
    assert ask(case, case.patient, "carrier_condition") != UNKNOWN_ANSWER


def test_structure_differs_by_knowledge_and_deduction_path_not_content_ids() -> None:
    environmental = generate_case(ENVIRONMENTAL_SEED)
    biological = generate_case(BIOLOGICAL_SEED)
    biological_with_different_content = replace(
        biological,
        contact_id="different_carrier_contact_content",
        contact="different hidden carrier-contact wording",
    )

    environmental_signature = investigation_structure_signature(environmental)
    biological_signature = investigation_structure_signature(biological)

    assert environmental.archetype_id == ENVIRONMENTAL_ARCHETYPE
    assert biological_signature != environmental_signature
    assert biological_signature.patient_known_event_ids != (
        environmental_signature.patient_known_event_ids
    )
    assert biological_signature.distinguishing_fact_effect != (
        environmental_signature.distinguishing_fact_effect
    )
    assert investigation_structure_signature(
        biological_with_different_content
    ) == biological_signature
    assert {item.name for item in fields(InvestigationStructureSignature)} == {
        "patient_known_event_ids",
        "witness_known_event_ids",
        "hypothesis_count",
        "distinguishing_fact_effect",
    }


def test_expanded_500_seed_analysis_is_deterministic() -> None:
    first = analyze_diversity()
    second = analyze_diversity()

    assert first == second
    assert first.seeds_analyzed == 500
