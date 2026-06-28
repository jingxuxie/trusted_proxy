from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    condition_id: str
    topology: str
    defense: str
    stages: tuple[str, ...]
    tracegate: bool = False


CONDITIONS: dict[str, Condition] = {
    "c0_single_direct": Condition(
        condition_id="c0_single_direct",
        topology="single_direct",
        defense="none",
        stages=("direct_executor",),
    ),
    "c1_2agent_naive": Condition(
        condition_id="c1_2agent_naive",
        topology="reader_executor",
        defense="naive",
        stages=("reader", "executor"),
    ),
    "c2_3agent_naive": Condition(
        condition_id="c2_3agent_naive",
        topology="reader_planner_executor",
        defense="naive",
        stages=("reader", "planner", "executor"),
    ),
    "c2x_3agent_extractive_naive": Condition(
        condition_id="c2x_3agent_extractive_naive",
        topology="reader_planner_executor",
        defense="extractive_naive",
        stages=("reader", "planner", "executor"),
    ),
    "c2o_3agent_oracle_laundered": Condition(
        condition_id="c2o_3agent_oracle_laundered",
        topology="reader_planner_executor",
        defense="oracle_laundered",
        stages=("reader", "planner", "executor"),
    ),
    "c3_source_preserving": Condition(
        condition_id="c3_source_preserving",
        topology="reader_planner_executor",
        defense="source_preserving",
        stages=("reader", "planner", "executor"),
    ),
    "c4_capability_scoped": Condition(
        condition_id="c4_capability_scoped",
        topology="reader_planner_executor",
        defense="capability_scoped",
        stages=("reader", "planner", "executor"),
    ),
    "c5_tracegate": Condition(
        condition_id="c5_tracegate",
        topology="reader_planner_executor",
        defense="naive",
        stages=("reader", "planner", "executor"),
        tracegate=True,
    ),
    "c5x_tracegate_extractive_naive": Condition(
        condition_id="c5x_tracegate_extractive_naive",
        topology="reader_planner_executor",
        defense="extractive_naive",
        stages=("reader", "planner", "executor"),
        tracegate=True,
    ),
    "c5o_tracegate_oracle_laundered": Condition(
        condition_id="c5o_tracegate_oracle_laundered",
        topology="reader_planner_executor",
        defense="oracle_laundered",
        stages=("reader", "planner", "executor"),
        tracegate=True,
    ),
}


def get_condition(condition_id: str) -> Condition:
    try:
        return CONDITIONS[condition_id]
    except KeyError as exc:
        known = ", ".join(sorted(CONDITIONS))
        raise ValueError(f"unknown condition {condition_id!r}; known: {known}") from exc
