"""Minimal procedural case-truth generator for EXP-001."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass


PATIENT_NAMES = ("Tomas", "Mira", "Oren", "Lysa", "Bram")

SOURCE = "redcap fungus spores"

LOCATIONS = {
    "forest_camp": "forest camp",
    "farm_storehouse": "farm storehouse",
    "roadside_shelter": "roadside shelter",
}

CONTACTS = {
    "eating_food": "eating food contaminated with spores",
    "drinking_water": "drinking water contaminated with spores",
    "wound_contact": "touching contaminated material with an open wound",
}

# The model only offers contacts that make sense at the selected location.
ALLOWED_CONTACTS_BY_LOCATION = {
    "forest_camp": ("eating_food", "drinking_water"),
    "farm_storehouse": ("eating_food", "wound_contact"),
    "roadside_shelter": ("drinking_water", "wound_contact"),
}


@dataclass(frozen=True)
class CaseTruth:
    """All facts that form one generated case."""

    seed: int
    patient: str
    source: str
    location_id: str
    location: str
    contact_id: str
    contact: str
    contact_day: int
    affected_day: int

    @property
    def events(self) -> tuple[str, ...]:
        """Technical event descriptions derived from structured case timing."""

        return (
            f"Day {self.contact_day}: {self.source} contaminated material at the {self.location}.",
            f"Day {self.contact_day}: {self.patient} was at the {self.location}.",
            f"Day {self.contact_day}: {self.patient} came into contact by {self.contact}.",
            f"Day {self.affected_day}: The exposure affected {self.patient}.",
        )

    @property
    def causal_chain(self) -> tuple[str, ...]:
        """Causal steps derived from the selected case facts."""

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
    patient = randomizer.choice(PATIENT_NAMES)
    location_id = randomizer.choice(tuple(LOCATIONS))
    contact_id = randomizer.choice(ALLOWED_CONTACTS_BY_LOCATION[location_id])

    location = LOCATIONS[location_id]
    contact = CONTACTS[contact_id]
    return CaseTruth(
        seed=seed,
        patient=patient,
        source=SOURCE,
        location_id=location_id,
        location=location,
        contact_id=contact_id,
        contact=contact,
        contact_day=1,
        affected_day=3,
    )


def format_report(case: CaseTruth) -> str:
    """Render the complete technical truth for human review."""

    events = "\n".join(case.events)
    causal_chain = "\n-> ".join(case.causal_chain)
    return (
        f"CASE SEED: {case.seed}\n\n"
        f"Patient:\n{case.patient}\n\n"
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
