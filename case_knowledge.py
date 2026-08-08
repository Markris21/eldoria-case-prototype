"""Minimal participant-knowledge experiment for EXP-002."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from case_generator import (
    BIOLOGICAL_CARRIER_ARCHETYPE,
    CaseEvent,
    CaseTruth,
    format_report,
    generate_case,
)


@dataclass(frozen=True)
class KnownFact:
    """A fact known because of one identifiable event."""

    fact: str
    source_event_id: str


def derive_knowledge(
    events: tuple[CaseEvent, ...], participant: str
) -> tuple[KnownFact, ...]:
    """Derive facts from events the participant joined or observed."""

    return tuple(
        KnownFact(fact=event.fact, source_event_id=event.event_id)
        for event in events
        if participant in event.participants or participant in event.observers
    )


def format_participant_knowledge(case: CaseTruth) -> str:
    """Show complete truth and event-derived knowledge with provenance."""

    sections = ["COMPLETE TRUTH", format_report(case), "PARTICIPANT KNOWLEDGE"]
    second_role = (
        "carrier"
        if case.archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE
        else "witness"
    )
    for participant, role in (
        (case.patient, "patient"),
        (case.witness, second_role),
    ):
        facts = derive_knowledge(case.event_records, participant)
        lines = [f"{participant} ({role}):"]
        lines.extend(
            f"- {known.fact} [source event: {known.source_event_id}]" for known in facts
        )
        sections.append("\n".join(lines))

    return "\n\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(description="Demonstrate EXP-002 knowledge.")
    parser.add_argument("seed", type=int, help="case seed")
    args = parser.parse_args()

    print(format_participant_knowledge(generate_case(args.seed)))


if __name__ == "__main__":
    main()
