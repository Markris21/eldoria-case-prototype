from dataclasses import replace

from case_generator import CONTACTS, generate_case
from case_interview import (
    TOPICS,
    UNKNOWN_ANSWER,
    ask_topic,
    format_initial_report,
    hypotheses_for,
    is_correct_hypothesis,
)
from case_knowledge import derive_knowledge


def topic(topic_id: str):
    return next(item for item in TOPICS if item.topic_id == topic_id)


def test_exactly_one_of_two_hypotheses_matches_case_truth() -> None:
    case = generate_case(18472)
    hypotheses = hypotheses_for(case)

    assert len(hypotheses) == 2
    assert sum(is_correct_hypothesis(case, item) for item in hypotheses) == 1


def test_alternative_hypothesis_does_not_match_case_truth() -> None:
    case = generate_case(18472)
    alternative = next(
        item for item in hypotheses_for(case) if not is_correct_hypothesis(case, item)
    )

    assert alternative.contact_id != case.contact_id


def test_initial_report_leaves_both_hypotheses_open() -> None:
    case = generate_case(18472)
    report = format_initial_report(case).lower()

    assert "water" not in report
    assert "food" not in report
    assert "contaminat" not in report
    assert case.source.lower() not in report


def test_contact_fact_remains_discoverable() -> None:
    case = generate_case(18472)
    knowledge = derive_knowledge(case.event_records, case.patient)

    answer = ask_topic(knowledge, topic("contact"), [])

    assert answer == f"{case.patient} drank water at the {case.location}."


def test_food_history_is_discoverable_with_event_provenance() -> None:
    case = generate_case(18472)
    knowledge = derive_knowledge(case.event_records, case.patient)
    known_fact = next(
        fact for fact in knowledge if fact.source_event_id == "food_history"
    )

    assert known_fact.fact == f"{case.patient} did not eat anything at the {case.location}."
    assert any(
        event.event_id == known_fact.source_event_id
        and event.fact == known_fact.fact
        for event in case.event_records
    )


def test_new_interview_answer_does_not_reveal_hidden_truth() -> None:
    case = generate_case(18472)
    knowledge = derive_knowledge(case.event_records, case.patient)

    answer = ask_topic(knowledge, topic("food"), [])

    assert case.source not in answer
    assert "contaminat" not in answer.lower()


def test_removing_food_event_participation_makes_answer_unknown() -> None:
    case = generate_case(18472)
    changed_case = replace(case, food_history_participants=())
    changed_knowledge = derive_knowledge(
        changed_case.event_records, changed_case.patient
    )

    assert ask_topic(changed_knowledge, topic("food"), []) == UNKNOWN_ANSWER


def test_correct_and_alternative_choices_are_evaluated_against_case_truth() -> None:
    case = generate_case(18472)
    correct = next(
        item for item in hypotheses_for(case) if is_correct_hypothesis(case, item)
    )
    alternative = next(
        item for item in hypotheses_for(case) if not is_correct_hypothesis(case, item)
    )

    assert is_correct_hypothesis(case, correct)
    assert not is_correct_hypothesis(case, alternative)


def test_evaluation_changes_when_hidden_case_truth_changes() -> None:
    case = generate_case(18472)
    alternative = next(
        item for item in hypotheses_for(case) if not is_correct_hypothesis(case, item)
    )
    changed_case = replace(
        case,
        contact_id=alternative.contact_id,
        contact=CONTACTS[alternative.contact_id],
    )

    assert is_correct_hypothesis(changed_case, alternative)


def test_same_seed_produces_deterministic_hypotheses_and_food_fact() -> None:
    first = generate_case(18472)
    second = generate_case(18472)

    assert hypotheses_for(first) == hypotheses_for(second)
    assert next(
        event for event in first.event_records if event.event_id == "food_history"
    ) == next(
        event for event in second.event_records if event.event_id == "food_history"
    )
