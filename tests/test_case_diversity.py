from collections import Counter
from dataclasses import replace

import pytest

from case_diversity import (
    analyze_diversity,
    concrete_case_signature,
    investigation_structure_signature,
)
from case_generator import CONTACTS, LOCATIONS, generate_case


def test_same_case_produces_same_concrete_signature() -> None:
    first = generate_case(18472)
    second = generate_case(18472)

    assert concrete_case_signature(first) == concrete_case_signature(second)


def test_same_case_produces_same_investigation_structure_signature() -> None:
    first = generate_case(18472)
    second = generate_case(18472)

    assert investigation_structure_signature(
        first
    ) == investigation_structure_signature(second)


def test_names_do_not_change_investigation_structure_signature() -> None:
    case = generate_case(18472)
    renamed_case = replace(
        case,
        patient="Different patient",
        witness="Different witness",
        contact_observers=("Different witness",),
        food_history_participants=("Different patient",),
    )

    assert investigation_structure_signature(
        renamed_case
    ) == investigation_structure_signature(case)
    assert concrete_case_signature(renamed_case) != concrete_case_signature(case)


def test_cosmetic_wording_is_not_in_investigation_structure_signature() -> None:
    case = generate_case(18472)
    reworded_case = replace(
        case,
        location="the same place with different wording",
        contact="the same contact with different wording",
    )

    assert investigation_structure_signature(
        reworded_case
    ) == investigation_structure_signature(case)


def test_different_contact_content_with_same_deduction_path_has_same_structure() -> None:
    case = generate_case(18472)
    changed_case = replace(
        case,
        location_id="farm_storehouse",
        location=LOCATIONS["farm_storehouse"],
        contact_id="wound_contact",
        contact=CONTACTS["wound_contact"],
    )

    assert investigation_structure_signature(
        changed_case
    ) == investigation_structure_signature(case)


def test_different_knowledge_pattern_changes_investigation_structure() -> None:
    case = generate_case(18472)
    changed_case = replace(case, contact_observers=())

    assert investigation_structure_signature(
        changed_case
    ) != investigation_structure_signature(case)


def test_default_500_seed_analysis_is_deterministic() -> None:
    first = analyze_diversity()
    second = analyze_diversity()

    assert first == second
    assert first.start_seed == 0
    assert first.seeds_analyzed == 500


def test_structure_counts_and_percentages_match_analysed_seed_count() -> None:
    analysis = analyze_diversity()

    assert sum(item.count for item in analysis.structures) == analysis.seeds_analyzed
    for item in analysis.structures:
        assert item.percentage == pytest.approx(
            item.count / analysis.seeds_analyzed * 100
        )


def test_most_common_structure_comes_from_actual_generated_signatures() -> None:
    analysis = analyze_diversity()
    expected_counts = Counter(
        investigation_structure_signature(generate_case(seed)) for seed in range(500)
    )
    expected_maximum = max(expected_counts.values())

    assert analysis.most_common_structure.count == expected_maximum
    assert (
        expected_counts[analysis.most_common_structure.signature] == expected_maximum
    )
