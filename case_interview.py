"""Minimal terminal interview experiment for EXP-003."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from case_generator import CaseTruth, format_report, generate_case
from case_knowledge import KnownFact, derive_knowledge


UNKNOWN_ANSWER = "I don't know."


@dataclass(frozen=True)
class InterviewTopic:
    """One question topic selecting a kind of known event fact."""

    topic_id: str
    label: str
    source_event_id: str


TOPICS = (
    InterviewTopic("where", "Where did this happen?", "presence"),
    InterviewTopic("contact", "What happened there?", "contact"),
    InterviewTopic("later", "What happened later?", "affected"),
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


def run_interview(case: CaseTruth) -> None:
    """Run the deliberately small EXP-003 terminal interaction."""

    discoveries: list[KnownFact] = []
    participants = ((case.patient, "patient"), (case.witness, "witness"))

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
        if topic_choice not in ("1", "2", "3"):
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

    print(f"\nCOMPLETE CASE TRUTH\n\n{format_report(case)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the EXP-003 interview.")
    parser.add_argument("seed", type=int, help="case seed")
    args = parser.parse_args()

    run_interview(generate_case(args.seed))


if __name__ == "__main__":
    main()
