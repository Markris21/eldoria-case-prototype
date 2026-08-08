from dataclasses import replace

import pytest

from case_generator import generate_case
from case_interview import TOPICS, UNKNOWN_ANSWER, ask_topic, format_initial_report
from case_knowledge import KnownFact, derive_knowledge


def topic(topic_id: str):
    return next(item for item in TOPICS if item.topic_id == topic_id)


def event_fact(case, event_id: str) -> str:
    return next(event.fact for event in case.event_records if event.event_id == event_id)


def ask(case, participant: str, topic_id: str) -> str:
    knowledge = derive_knowledge(case.event_records, participant)
    return ask_topic(knowledge, topic(topic_id), [])


def test_initial_report_does_not_reveal_hidden_truth() -> None:
    case = generate_case(18472)
    report = format_initial_report(case)

    assert case.patient in report
    assert case.source not in report
    assert case.contact not in report
    assert "contaminat" not in report.lower()
    assert "causal" not in report.lower()


def test_location_topic_neutrally_asks_about_presence_event() -> None:
    location_topic = topic("where")

    assert location_topic.label == "Where did this happen?"
    assert location_topic.source_event_id == "presence"


@pytest.mark.parametrize(
    ("topic_id", "event_id"),
    (("where", "presence"), ("contact", "contact"), ("later", "affected")),
)
def test_patient_topics_return_relevant_known_facts(
    topic_id: str, event_id: str
) -> None:
    case = generate_case(18472)

    assert ask(case, case.patient, topic_id) == event_fact(case, event_id)


@pytest.mark.parametrize(
    ("topic_id", "event_id"), (("where", "presence"), ("contact", "contact"))
)
def test_witness_topics_return_relevant_known_facts(
    topic_id: str, event_id: str
) -> None:
    case = generate_case(18472)

    assert ask(case, case.witness, topic_id) == event_fact(case, event_id)


def test_witness_does_not_know_later_condition() -> None:
    case = generate_case(18472)

    assert ask(case, case.witness, "later") == UNKNOWN_ANSWER


@pytest.mark.parametrize("participant_role", ("patient", "witness"))
def test_interview_answers_do_not_reveal_hidden_truth(participant_role: str) -> None:
    case = generate_case(18472)
    participant = getattr(case, participant_role)

    for interview_topic in TOPICS:
        answer = ask(case, participant, interview_topic.topic_id)
        assert case.source not in answer
        assert "contaminat" not in answer.lower()


def test_removing_contact_observation_changes_witness_answer_to_unknown() -> None:
    case = generate_case(18472)
    changed_case = replace(case, contact_observers=())

    assert ask(case, case.witness, "contact") == event_fact(case, "contact")
    assert ask(changed_case, changed_case.witness, "contact") == UNKNOWN_ANSWER


def test_discoveries_contain_only_returned_facts() -> None:
    case = generate_case(18472)
    patient_knowledge = derive_knowledge(case.event_records, case.patient)
    witness_knowledge = derive_knowledge(case.event_records, case.witness)
    discoveries: list[KnownFact] = []

    returned_location = ask_topic(patient_knowledge, topic("where"), discoveries)
    unknown = ask_topic(witness_knowledge, topic("later"), discoveries)

    assert unknown == UNKNOWN_ANSWER
    assert [fact.fact for fact in discoveries] == [returned_location]


def test_same_seed_produces_deterministic_interview_data() -> None:
    first = generate_case(18472)
    second = generate_case(18472)

    assert format_initial_report(first) == format_initial_report(second)
    for participant_role in ("patient", "witness"):
        first_participant = getattr(first, participant_role)
        second_participant = getattr(second, participant_role)
        assert tuple(
            ask(first, first_participant, interview_topic.topic_id)
            for interview_topic in TOPICS
        ) == tuple(
            ask(second, second_participant, interview_topic.topic_id)
            for interview_topic in TOPICS
        )
