# MaholoBioBench

MaholoBioBench is a protocol-aware benchmark layer for bio-laboratory robot manipulation in a Maholo digital twin.

This repository is intended to be independent from the broader AutoMaholo research workspace. It defines the benchmark contract, task taxonomy, protocol-state schemas, episode output format, and validation utilities. The executable robot simulation backend is expected to come from `robosuite_maholo`.

## Research Position

MaholoBioBench is not a new robot policy. It is a benchmark:

- defines what bio-lab robot tasks are,
- defines how tasks are grouped into families, instances, and variations,
- defines protocol-aware state semantics,
- defines success conditions and metrics,
- provides a reproducible contract for running reference agents.

The main research claim is:

> A laboratory robot policy can be geometrically successful while still failing the biological protocol. MaholoBioBench makes this gap measurable.

## Project Layout

```text
maholobiobench/
├── configs/
│   ├── task_registry.yaml
│   ├── protocol_state_schema.yaml
│   └── episode_output_schema.yaml
├── docs/
│   ├── RESEARCH_PROPOSAL.md
│   ├── PHASE_B_SPEC.md
│   ├── TASK_TREE.md
│   └── BENCHMARK_QA_NOTES.md
├── examples/
│   └── list_phase_b_tasks.py
├── scripts/
│   └── validate_configs.py
├── src/maholobiobench/
│   ├── __init__.py
│   ├── paths.py
│   ├── registry.py
│   └── validation.py
└── pyproject.toml
```

## Relationship to Other Repositories

Recommended software split:

| Layer | Repository / directory | Responsibility |
|---|---|---|
| Benchmark layer | `maholobiobench` | task registry, protocol state, metrics, evaluation contract |
| Simulation backend | `robosuite_maholo` | Maholo robot model, lab arena, assets, MuJoCo environments |
| Experiment workspace | `AutoMaholo` | training scripts, real2sim/sim2real tools, project-specific experiments |

This separation keeps the benchmark contribution clear. `robosuite_maholo` supplies executable environments; `maholobiobench` defines the standardized examination system.

## Phase B v0.1 Scope

The first benchmark release focuses on 8 task families:

1. `ReachTargetPose`
2. `GraspLabObject`
3. `TransportHeldObject`
4. `OpenArticulatedEquipment`
5. `RetrieveContainer`
6. `TransferLiquid`
7. `RetrieveAndTransferSample`
8. `PrepareDilutionSeries`

The goal is not to model full wet-lab physics. v0.1 should use symbolic protocol state for liquid volume, sample identity, tip status, contamination, equipment state, and protocol progress.

## Install

From this directory:

```bash
python3 -m pip install -e .
```

For config validation only, `PyYAML` is required.

## Validate Configs

```bash
python3 scripts/validate_configs.py
```

Expected output includes:

- all YAML files parse,
- Phase B task families exist in the registry,
- every task family defines instances, variations, success conditions, and metrics.

## List Phase B Tasks

```bash
python3 examples/list_phase_b_tasks.py
```

## Next Implementation Targets

1. Implement a protocol state engine.
2. Add task wrappers that bind registry entries to `robosuite_maholo` environments.
3. Implement an episode evaluator that produces `summary.json` and result tables.
4. Generate scripted expert episodes for all Phase B task families.
5. Run reference agents only after the benchmark contract is stable.

