"""Measure concrete and structural diversity in the current case generator."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from case_generator import CaseTruth, generate_case
from case_interview import hypotheses_for
from case_knowledge import derive_knowledge


@dataclass(frozen=True)
class ConcreteCaseSignature:
    """Existing generated values that distinguish one concrete case."""

    patient: str
    witness: str
    location_id: str
    contact_id: str
    contact_observers: tuple[str, ...]
    food_history_participants: tuple[str, ...]


@dataclass(frozen=True, order=True)
class InvestigationStructureSignature:
    """Gameplay structure with identity, location, seed, and wording removed."""

    patient_known_event_ids: tuple[str, ...]
    witness_known_event_ids: tuple[str, ...]
    hypothesis_count: int
    distinguishing_fact_effect: str


@dataclass(frozen=True)
class StructureCount:
    signature: InvestigationStructureSignature
    count: int
    percentage: float


@dataclass(frozen=True)
class DiversityAnalysis:
    start_seed: int
    seeds_analyzed: int
    unique_concrete_cases: int
    structures: tuple[StructureCount, ...]

    @property
    def unique_investigation_structures(self) -> int:
        return len(self.structures)

    @property
    def most_common_structure(self) -> StructureCount:
        return self.structures[0]


def concrete_case_signature(case: CaseTruth) -> ConcreteCaseSignature:
    """Create a signature for one concrete generated combination."""

    return ConcreteCaseSignature(
        patient=case.patient,
        witness=case.witness,
        location_id=case.location_id,
        contact_id=case.contact_id,
        contact_observers=case.contact_observers,
        food_history_participants=case.food_history_participants,
    )


def investigation_structure_signature(
    case: CaseTruth,
) -> InvestigationStructureSignature:
    """Describe the current interview and deduction path without cosmetic data."""

    patient_knowledge = derive_knowledge(case.event_records, case.patient)
    witness_knowledge = derive_knowledge(case.event_records, case.witness)
    hypotheses = hypotheses_for(case)

    return InvestigationStructureSignature(
        patient_known_event_ids=tuple(
            fact.source_event_id for fact in patient_knowledge
        ),
        witness_known_event_ids=tuple(
            fact.source_event_id for fact in witness_knowledge
        ),
        hypothesis_count=len(hypotheses),
        distinguishing_fact_effect=(
            "supports_correct_hypothesis"
            if case.contact_id == "eating_food"
            else "eliminates_alternative"
        ),
    )


def analyze_diversity(start_seed: int = 0, count: int = 500) -> DiversityAnalysis:
    """Analyse a deterministic consecutive seed range."""

    if count < 1:
        raise ValueError("count must be at least 1")

    cases = tuple(generate_case(seed) for seed in range(start_seed, start_seed + count))
    concrete_signatures = {concrete_case_signature(case) for case in cases}
    structure_counts = Counter(
        investigation_structure_signature(case) for case in cases
    )
    sorted_counts = sorted(
        structure_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )
    structures = tuple(
        StructureCount(
            signature=signature,
            count=structure_count,
            percentage=structure_count / count * 100,
        )
        for signature, structure_count in sorted_counts
    )

    return DiversityAnalysis(
        start_seed=start_seed,
        seeds_analyzed=count,
        unique_concrete_cases=len(concrete_signatures),
        structures=structures,
    )


def format_analysis(analysis: DiversityAnalysis) -> str:
    """Render metrics and the exact structural fields used by the analysis."""

    most_common = analysis.most_common_structure
    lines = [
        "STAGE 6 DIVERSITY ANALYSIS",
        "",
        f"Seed range: {analysis.start_seed} to "
        f"{analysis.start_seed + analysis.seeds_analyzed - 1}",
        f"Seeds analysed: {analysis.seeds_analyzed}",
        f"Unique concrete cases: {analysis.unique_concrete_cases}",
        f"Unique investigation structures: "
        f"{analysis.unique_investigation_structures}",
        "",
        "Investigation structure signature fields:",
        "- patient known event categories",
        "- witness known event categories",
        "- number of available hypotheses",
        "- distinguishing fact's role in deduction",
        "Ignored as content/cosmetic: seed, names, location, contact identity, "
        "hypothesis identity, and rendered wording",
        "",
        "Most common structure:",
        f"{most_common.count} / {analysis.seeds_analyzed} "
        f"({most_common.percentage:.1f}%)",
        "",
        "Investigation structures:",
    ]

    for index, structure in enumerate(analysis.structures, start=1):
        signature = structure.signature
        lines.extend(
            (
                "",
                f"{index}. hypotheses available: {signature.hypothesis_count}",
                "   patient knows: "
                + ", ".join(signature.patient_known_event_ids),
                "   witness knows: "
                + ", ".join(signature.witness_known_event_ids),
                f"   distinguishing fact: {signature.distinguishing_fact_effect}",
                f"   count: {structure.count}",
                f"   percentage: {structure.percentage:.1f}%",
            )
        )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse current case diversity.")
    parser.add_argument("--start", type=int, default=0, help="first seed (default: 0)")
    parser.add_argument(
        "--count", type=int, default=500, help="number of seeds (default: 500)"
    )
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    print(format_analysis(analyze_diversity(args.start, args.count)))


if __name__ == "__main__":
    main()
