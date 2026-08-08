"""Minimal terminal interview experiment for EXP-003."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from case_generator import (
    BIOLOGICAL_CARRIER_ARCHETYPE,
    ENVIRONMENTAL_CONTACTS_BY_LOCATION,
    CaseTruth,
    format_report,
    generate_case,
)
from case_knowledge import KnownFact, derive_knowledge


UNKNOWN_ANSWER = "I don't know."


@dataclass(frozen=True)
class InterviewTopic:
    """One question topic selecting a kind of known event fact."""

    topic_id: str
    label: str
    source_event_id: str


@dataclass(frozen=True)
class Hypothesis:
    """One player-visible explanation tied to a possible case contact."""

    label: str
    contact_id: str


TOPICS = (
    InterviewTopic("where", "Where did this happen?", "presence"),
    InterviewTopic("contact", "What happened there?", "contact"),
    InterviewTopic("later", "What happened later?", "affected"),
    InterviewTopic("food", "What did the patient eat?", "food_history"),
    InterviewTopic(
        "carrier_condition",
        "What was that person's condition?",
        "carrier_condition",
    ),
)


def format_initial_report(case: CaseTruth) -> str:
    """Show only the information available before interviews begin."""

    return f"CASE REPORT\n\n{case.patient} became unwell after a recent outing."


def ask_topic(
    knowledge: tuple[KnownFact, ...],
    topic: InterviewTopic,
    discoveries: list[KnownFact],
) -> str:
    """Answer from known facts and record only a fact actually returned."""

    known_fact = next(
        (
            fact
            for fact in knowledge
            if fact.source_event_id == topic.source_event_id
        ),
        None,
    )
    if known_fact is None:
        return UNKNOWN_ANSWER

    if known_fact not in discoveries:
        discoveries.append(known_fact)
    return known_fact.fact


def hypotheses_for(case: CaseTruth) -> tuple[Hypothesis, Hypothesis]:
    """Build exactly one true contact explanation and one alternative."""

    if case.archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE:
        contact_ids = (
            case.contact_id,
            ENVIRONMENTAL_CONTACTS_BY_LOCATION[case.location_id][0],
        )
    elif case.contact_id == "eating_food":
        contact_ids = ("drinking_water", "eating_food")
    else:
        contact_ids = (case.contact_id, "eating_food")

    return (
        _hypothesis_for_contact(contact_ids[0]),
        _hypothesis_for_contact(contact_ids[1]),
    )


def _hypothesis_for_contact(contact_id: str) -> Hypothesis:
    if contact_id == "carrier_contact":
        label = "Illness followed close contact with an already-unwell person."
    elif contact_id == "drinking_water":
        label = "Contaminated water caused the patient's illness."
    elif contact_id == "eating_food":
        label = "Food eaten during the outing caused the patient's illness."
    else:
        label = "Contaminated material entering a wound caused the patient's illness."

    return Hypothesis(
        label=label,
        contact_id=contact_id,
    )


def is_correct_hypothesis(case: CaseTruth, hypothesis: Hypothesis) -> bool:
    """Evaluate a choice directly against the hidden case contact truth."""

    return hypothesis.contact_id == case.contact_id


def run_interview(case: CaseTruth) -> None:
    """Run the deliberately small EXP-003 terminal interaction."""

    discoveries: list[KnownFact] = []
    second_role = (
        "carrier"
        if case.archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE
        else "witness"
    )
    participants = ((case.patient, "patient"), (case.witness, second_role))

    print(format_initial_report(case))

    while True:
        print("\nChoose a participant:")
        for index, (participant, role) in enumerate(participants, start=1):
            print(f"{index}. {participant} ({role})")
        print("0. End interview")

        participant_choice = input("> ").strip()
        if participant_choice == "0":
            break
        if participant_choice not in ("1", "2"):
            print("Invalid choice.")
            continue

        participant = participants[int(participant_choice) - 1][0]
        print("\nChoose a topic:")
        for index, topic in enumerate(TOPICS, start=1):
            print(f"{index}. {topic.label}")

        topic_choice = input("> ").strip()
        if topic_choice not in tuple(str(index) for index in range(1, len(TOPICS) + 1)):
            print("Invalid choice.")
            continue

        topic = TOPICS[int(topic_choice) - 1]
        knowledge = derive_knowledge(case.event_records, participant)
        print(f"\nAnswer: {ask_topic(knowledge, topic, discoveries)}")

    print("\nPLAYER DISCOVERIES")
    if discoveries:
        for fact in discoveries:
            print(f"- {fact.fact}")
    else:
        print("- None")

    hypotheses = hypotheses_for(case)
    print("\nHYPOTHESES")
    for index, hypothesis in enumerate(hypotheses, start=1):
        print(f"{index}. {hypothesis.label}")

    hypothesis_choice = input("> ").strip()
    if hypothesis_choice in ("1", "2"):
        selected = hypotheses[int(hypothesis_choice) - 1]
        result = "CORRECT" if is_correct_hypothesis(case, selected) else "INCORRECT"
        print(f"\nHYPOTHESIS RESULT: {result}")
    else:
        print("\nHYPOTHESIS RESULT: Invalid choice.")

    print(f"\nCOMPLETE CASE TRUTH\n\n{format_report(case)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the EXP-003 interview.")
    parser.add_argument("seed", type=int, help="case seed")
    args = parser.parse_args()

    run_interview(generate_case(args.seed))


if __name__ == "__main__":
    main()
