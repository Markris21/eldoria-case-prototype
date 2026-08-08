"""Minimal procedural case-truth generator."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass


PATIENT_NAMES = ("Tomas", "Mira", "Oren", "Lysa", "Bram")

ENVIRONMENTAL_ARCHETYPE = "environmental_exposure"
BIOLOGICAL_CARRIER_ARCHETYPE = "biological_carrier_contact"
ARCHETYPES = (ENVIRONMENTAL_ARCHETYPE, BIOLOGICAL_CARRIER_ARCHETYPE)

SOURCE = "redcap fungus spores"
CARRIER_SOURCE = "biological carrier contact"

LOCATIONS = {
    "forest_camp": "forest camp",
    "farm_storehouse": "farm storehouse",
    "roadside_shelter": "roadside shelter",
}

CONTACTS = {
    "eating_food": "eating food contaminated with spores",
    "drinking_water": "drinking water contaminated with spores",
    "wound_contact": "touching contaminated material with an open wound",
    "carrier_contact": "close contact with an already-unwell person",
}

OBSERVABLE_CONTACT_ACTIONS = {
    "eating_food": "ate food",
    "drinking_water": "drank water",
    "wound_contact": "touched material with an open wound",
}

# The model only offers contacts that make sense at the selected location.
ALLOWED_CONTACTS_BY_LOCATION = {
    "forest_camp": ("eating_food", "drinking_water", "carrier_contact"),
    "farm_storehouse": ("eating_food", "wound_contact", "carrier_contact"),
    "roadside_shelter": ("drinking_water", "wound_contact", "carrier_contact"),
}

ENVIRONMENTAL_CONTACTS_BY_LOCATION = {
    location_id: tuple(
        contact_id for contact_id in contact_ids if contact_id != "carrier_contact"
    )
    for location_id, contact_ids in ALLOWED_CONTACTS_BY_LOCATION.items()
}


@dataclass(frozen=True)
class CaseEvent:
    """One fact-producing event and the people involved in it."""

    event_id: str
    day: int
    fact: str
    participants: tuple[str, ...]
    observers: tuple[str, ...] = ()

    @property
    def description(self) -> str:
        return f"Day {self.day}: {self.fact}"


@dataclass(frozen=True)
class CaseTruth:
    """All facts that form one generated case."""

    seed: int
    archetype_id: str
    patient: str
    witness: str
    carrier: str | None
    source: str
    location_id: str
    location: str
    contact_id: str
    contact: str
    contact_day: int
    affected_day: int
    carrier_condition_day: int | None
    contact_observers: tuple[str, ...]
    carrier_condition_observers: tuple[str, ...]
    food_history_participants: tuple[str, ...]

    @property
    def event_records(self) -> tuple[CaseEvent, ...]:
        """Structured events derived from the complete case facts."""

        if self.archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE:
            assert self.carrier is not None
            assert self.carrier_condition_day is not None
            return (
                CaseEvent(
                    event_id="carrier_causation",
                    day=self.contact_day,
                    fact=(
                        f"{self.source} through {self.carrier} affected "
                        f"{self.patient}."
                    ),
                    participants=(),
                ),
                CaseEvent(
                    event_id="presence",
                    day=self.contact_day,
                    fact=f"{self.patient} was at the {self.location}.",
                    participants=(self.patient, self.carrier),
                ),
                CaseEvent(
                    event_id="contact",
                    day=self.contact_day,
                    fact=(
                        f"{self.patient} spent time with {self.carrier} "
                        f"at the {self.location}."
                    ),
                    participants=(self.patient, self.carrier),
                ),
                CaseEvent(
                    event_id="carrier_condition",
                    day=self.carrier_condition_day,
                    fact=(
                        f"{self.carrier} was visibly unwell before spending time "
                        f"with {self.patient}."
                    ),
                    participants=(self.carrier,),
                    observers=self.carrier_condition_observers,
                ),
                CaseEvent(
                    event_id="affected",
                    day=self.affected_day,
                    fact=f"The exposure affected {self.patient}.",
                    participants=(self.patient,),
                ),
            )

        return (
            CaseEvent(
                event_id="contamination",
                day=self.contact_day,
                fact=f"{self.source} contaminated material at the {self.location}.",
                participants=(),
            ),
            CaseEvent(
                event_id="presence",
                day=self.contact_day,
                fact=f"{self.patient} was at the {self.location}.",
                participants=(self.patient, self.witness),
            ),
            CaseEvent(
                event_id="contact",
                day=self.contact_day,
                fact=(
                    f"{self.patient} {OBSERVABLE_CONTACT_ACTIONS[self.contact_id]} "
                    f"at the {self.location}."
                ),
                participants=(self.patient,),
                observers=self.contact_observers,
            ),
            CaseEvent(
                event_id="food_history",
                day=self.contact_day,
                fact=(
                    f"{self.patient} ate food at the {self.location}."
                    if self.contact_id == "eating_food"
                    else f"{self.patient} did not eat anything at the {self.location}."
                ),
                participants=self.food_history_participants,
            ),
            CaseEvent(
                event_id="affected",
                day=self.affected_day,
                fact=f"The exposure affected {self.patient}.",
                participants=(self.patient,),
            ),
        )

    @property
    def events(self) -> tuple[str, ...]:
        """Technical event descriptions derived from structured case timing."""

        return tuple(event.description for event in self.event_records)

    @property
    def causal_chain(self) -> tuple[str, ...]:
        """Causal steps derived from the selected case facts."""

        if self.archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE:
            assert self.carrier is not None
            return (
                self.source,
                f"{self.carrier} already unwell",
                self.contact,
                f"{self.patient} exposed",
                f"{self.patient} affected",
            )

        return (
            self.source,
            f"material at the {self.location}",
            self.contact,
            f"{self.patient} exposed",
            f"{self.patient} affected",
        )


def generate_case(seed: int) -> CaseTruth:
    """Compose a deterministic case truth from data and compatibility rules."""

    randomizer = random.Random(seed)
    archetype_id = ARCHETYPES[seed % len(ARCHETYPES)]
    patient = randomizer.choice(PATIENT_NAMES)
    location_id = randomizer.choice(tuple(LOCATIONS))
    environmental_contact_id = randomizer.choice(
        ENVIRONMENTAL_CONTACTS_BY_LOCATION[location_id]
    )
    witness = randomizer.choice(tuple(name for name in PATIENT_NAMES if name != patient))

    location = LOCATIONS[location_id]
    is_biological = archetype_id == BIOLOGICAL_CARRIER_ARCHETYPE
    contact_id = "carrier_contact" if is_biological else environmental_contact_id
    contact = CONTACTS[contact_id]
    contact_day = 1
    affected_day = 3
    return CaseTruth(
        seed=seed,
        archetype_id=archetype_id,
        patient=patient,
        witness=witness,
        carrier=witness if is_biological else None,
        source=CARRIER_SOURCE if is_biological else SOURCE,
        location_id=location_id,
        location=location,
        contact_id=contact_id,
        contact=contact,
        contact_day=contact_day,
        affected_day=affected_day,
        carrier_condition_day=contact_day - 1 if is_biological else None,
        contact_observers=() if is_biological else (witness,),
        carrier_condition_observers=(patient,) if is_biological else (),
        food_history_participants=() if is_biological else (patient,),
    )


def format_report(case: CaseTruth) -> str:
    """Render the complete technical truth for human review."""

    events = "\n".join(case.events)
    causal_chain = "\n-> ".join(case.causal_chain)
    second_role = "Carrier" if case.carrier is not None else "Witness"
    return (
        f"CASE SEED: {case.seed}\n\n"
        f"Archetype:\n{case.archetype_id}\n\n"
        f"Patient:\n{case.patient}\n\n"
        f"{second_role}:\n{case.witness}\n\n"
        f"Source:\n{case.source}\n\n"
        f"Location:\n{case.location}\n\n"
        f"Contact:\n{case.contact}\n\n"
        f"Events:\n{events}\n\n"
        f"Causal chain:\n{causal_chain}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate EXP-001 case truths.")
    parser.add_argument("seed", type=int, help="seed of the first generated case")
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="number of consecutive seeds to generate (default: 1)",
    )
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    reports = [format_report(generate_case(args.seed + offset)) for offset in range(args.count)]
    print("\n\n".join(reports))


if __name__ == "__main__":
    main()
