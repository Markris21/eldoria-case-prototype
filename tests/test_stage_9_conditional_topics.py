from dataclasses import replace

from case_generator import generate_case
from case_interview import (
    UNKNOWN_ANSWER,
    ask_topic,
    available_topics,
    run_interview,
)
from case_knowledge import KnownFact, derive_knowledge


BIOLOGICAL_SEED = 1


def topic_ids(discoveries: list[KnownFact]) -> tuple[str, ...]:
    return tuple(topic.topic_id for topic in available_topics(discoveries))


def topic(topic_id: str, discoveries: list[KnownFact]):
    return next(
        item for item in available_topics(discoveries) if item.topic_id == topic_id
    )


def test_hidden_biological_truth_does_not_unlock_carrier_condition() -> None:
    case = generate_case(BIOLOGICAL_SEED)

    assert case.carrier is not None
    assert "carrier_condition" in {event.event_id for event in case.event_records}
    assert topic_ids([]) == ("where", "contact", "later", "food")


def test_presence_discovery_does_not_unlock_carrier_condition() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    knowledge = derive_knowledge(case.event_records, case.patient)
    discoveries: list[KnownFact] = []

    ask_topic(knowledge, topic("where", discoveries), discoveries)

    assert tuple(fact.source_event_id for fact in discoveries) == ("presence",)
    assert "carrier_condition" not in topic_ids(discoveries)


def test_discovered_contact_unlocks_carrier_condition() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    knowledge = derive_knowledge(case.event_records, case.patient)
    discoveries: list[KnownFact] = []

    ask_topic(knowledge, topic("contact", discoveries), discoveries)

    assert tuple(fact.source_event_id for fact in discoveries) == ("contact",)
    assert "carrier_condition" in topic_ids(discoveries)


def test_interview_stays_with_participant_and_allows_explicit_back(
    monkeypatch, capsys
) -> None:
    case = generate_case(BIOLOGICAL_SEED)
    answers = iter(("1", "1", "2", "5", "0", "0", "1"))
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    run_interview(case)

    output = capsys.readouterr().out
    topic_menus = output.split("\nChoose a topic:")[1:]
    assert "What was that person's condition?" not in topic_menus[0]
    assert "What was that person's condition?" not in topic_menus[1]
    assert "What was that person's condition?" in topic_menus[2]
    assert "0. Back to participants" in output
    assert output.count("Choose a participant:") == 2

    contact_fact = next(
        event.fact for event in case.event_records if event.event_id == "contact"
    )
    after_contact = output.split(f"Answer: {contact_fact}", 1)[1]
    assert after_contact.index("Choose a topic:") < after_contact.index(
        "Choose a participant:"
    )


def test_unlocked_topic_still_cannot_return_unknown_participant_fact() -> None:
    case = generate_case(BIOLOGICAL_SEED)
    changed_case = replace(case, carrier_condition_observers=())
    knowledge = derive_knowledge(changed_case.event_records, changed_case.patient)
    discoveries: list[KnownFact] = []

    ask_topic(knowledge, topic("contact", discoveries), discoveries)
    answer = ask_topic(
        knowledge,
        topic("carrier_condition", discoveries),
        discoveries,
    )

    assert answer == UNKNOWN_ANSWER
    assert "carrier_condition" not in {
        fact.source_event_id for fact in discoveries
    }
