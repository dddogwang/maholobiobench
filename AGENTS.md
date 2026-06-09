# Codex Project Guide: MaholoBioBench

## Project Summary

MaholoBioBench is a protocol-aware benchmark for bio-laboratory robot manipulation in a Maholo digital twin.

The project is a benchmark / evaluation framework, not a new robot policy. The main research contribution is the definition of:

- a Maholo bio-laboratory digital-twin environment,
- a three-level task taxonomy,
- Task Families, Instances, and Variations,
- protocol-aware experimental state and metrics,
- standardized episode output,
- baseline evaluation with existing methods.

In this project, "protocol" means semantic state in an experimental workflow, such as step progress, sample identity, liquid volume, tip state, contamination constraints, and equipment state.

## Primary Local Documentation

Read these files first when orienting to the project:

- `README.md`
- `docs/RESEARCH_PROPOSAL.md`
- `docs/PHASE_B_SPEC.md`
- `docs/TASK_TREE.md`
- `docs/BENCHMARK_QA_NOTES.md`
- `presentation/research_direction_summary.html`

The current short research-direction deck is:

- `presentation/research_direction_summary.html`

## GitHub Repository

Repository:

- https://github.com/dddogwang/maholobiobench

## GitHub Project / Roadmap

Project board:

- https://github.com/users/dddogwang/projects/1/views/1

Use this project board as the main GitHub management location for roadmap and milestone tracking.

## GitHub Issues

Current roadmap issues:

- Roadmap: https://github.com/dddogwang/maholobiobench/issues/1
- M1 Environment Readiness: https://github.com/dddogwang/maholobiobench/issues/2
- M2 Task Definition: https://github.com/dddogwang/maholobiobench/issues/3
- M3 Protocol Evaluation: https://github.com/dddogwang/maholobiobench/issues/4
- M4 Episode Output and Evaluation Pipeline: https://github.com/dddogwang/maholobiobench/issues/5
- M5 Baseline Results: https://github.com/dddogwang/maholobiobench/issues/6
- M6 Paper Results and Release Package: https://github.com/dddogwang/maholobiobench/issues/7
- M0 Asset Inventory: https://github.com/dddogwang/maholobiobench/issues/8

## Roadmap Timing

- M0 Asset Inventory: before M1, initial version before 2026.7 work starts.
- M1 Environment Readiness: 2026.7-2026.8.
- M2 Task Definition: 2026.8-2026.9.
- M3 Protocol Evaluation: 2026.9-2026.10.
- M4 Episode Output and Evaluation Pipeline: 2026.9-2026.11.
- M5 Baseline Results: 2026.10-2027.03.
- M6 Paper Results and Release Package: 2027.1-2027.03.

## Research Scope for v0

v0 should cover the frozen task families, with 1-2 representative instances per family for the first baseline pass:

- `ReachTargetPose`
- `GraspLabObject`
- `TransportHeldObject`
- `OpenArticulatedEquipment`
- `RetrieveContainer`
- `TransferLiquid`
- `RetrieveAndTransferSample`
- `PrepareDilutionSeries`

Use a unified task structure:

```text
Task Family -> Instance -> Variation
```

## Baseline Scope

Baseline methods are existing methods used to validate the benchmark, not the core contribution.

Planned baselines:

- scripted expert,
- Behavior Cloning (BC),
- Soft Actor-Critic (SAC),
- Proximal Policy Optimization (PPO),
- optional sequence policy or planner-based baseline.

## Expected Paper Evidence

The benchmark paper should eventually include:

- Task Suite Summary,
- Expert Feasibility,
- Baseline Comparison,
- Metric Gap: geometric success vs protocol success,
- Generalization: seen vs unseen variations,
- Reproducibility: standardized episode output and evaluation scripts.

## Development Notes for Codex

- Prefer preserving the benchmark framing. Do not recast this project as a method paper unless explicitly requested.
- Keep terminology consistent: use `Task Family`, `Instance`, and `Variation`.
- Use `v0`, not `v0.1`, for the current planned release.
- Treat GitHub Project 1 as the roadmap source of truth.
- When adding implementation work, connect it to the relevant issue or milestone.
- Before changing task definitions or schemas, read the registry and docs listed above.
