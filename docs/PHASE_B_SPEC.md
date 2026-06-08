# MaholoBioBench Phase B Specification

Date: 2026-06-08  
Status: draft v0.1  
Scope: benchmark task definition, protocol state, evaluation contract, reproducible environment interface, and implementation milestones.

## 1. Phase B Goal

Phase B should turn the current Maholo digital twin into a benchmark, not only a set of demos.

The target deliverable is:

> MaholoBioBench v0.1: a digital-twin benchmark for biological laboratory robot manipulation with standardized tasks, protocol-level state, episode output format, metrics, and baseline-ready task configs.

This phase should produce enough structure to support a benchmark paper later:

- reproducible task definitions
- task hierarchy
- protocol state semantics
- standard metrics
- expert demonstration format
- baseline evaluation protocol

## 2. Scope for v0.1

Do not try to model full wet-lab physics in v0.1. The first version should use:

- MuJoCo / robosuite robot-object interaction for robot motion.
- Symbolic liquid state for aspiration / dispense.
- Rule-based contamination state.
- Rule-based protocol progress.

The key novelty is biological laboratory task semantics and evaluation criteria, not a new robot learning method, fluid simulation, or sim-to-real deployment pipeline.

## 3. Task Hierarchy

v0.1 should include 8 task families across 3 levels. Concrete names such as
`ReachPipette` or `OpenCoolIncubator` are instances under a family, not the
top-level benchmark task itself.

### Level 1: Manipulation Primitives

These evaluate low-level robot manipulation.

| Task family | Existing basis | Main goal | Primary metrics |
|---|---|---|---|
| `ReachTargetPose` | `maholo_eefR_Move2Pipette` / `maholoSingle_eefR_Move2Pipette` | Move gripper to a lab-object affordance or explicit target pose | position error, orientation error, collision |
| `GraspLabObject` | `maholo_eefR_Grip2Pipette` | Grasp a lab object stably | grasp success, object displacement |
| `TransportHeldObject` | `maholo_eefR_Move2Tube` | Move a held lab object to a target pose | target pose error, orientation error, smoothness |
| `OpenArticulatedEquipment` | `maholoSingle_OpenCoolIncubator` / `OpenDeepFreezer` / `OpenCO2Incubator` | Open or close lab equipment doors/lids/covers | door angle, collision, steps |

Example instances:

- `ReachTargetPose/ReachPipetteGraspPose`
- `GraspLabObject/GraspPipette`
- `TransportHeldObject/MovePipetteToTube`
- `OpenArticulatedEquipment/OpenCoolIncubator`

### Level 2: Bio-Lab Skill Tasks

These add sample/container/pipette semantics.

| Task family | Existing basis | Main goal | Primary metrics |
|---|---|---|---|
| `RetrieveContainer` | freezer/incubator + tube rack assets | Retrieve the requested container/sample | sample identity accuracy, container pose error |
| `TransferLiquid` | pipette + tube assets | Transfer symbolic volume from source to target | volume error, sample identity consistency, contamination |

Example instances:

- `RetrieveContainer/RetrieveTubeFromCoolIncubator`
- `RetrieveContainer/RetrieveTubeFromRack`
- `TransferLiquid/TubeToTubeTransfer`

### Level 3: Long-Horizon Protocol Tasks

These evaluate protocol execution.

| Task family | Existing basis | Main goal | Primary metrics |
|---|---|---|---|
| `RetrieveAndTransferSample` | Level 1 + Level 2 tasks | Retrieve sample and transfer volume | protocol completion, volume error, violations |
| `PrepareDilutionSeries` | `LiquidTransfer` repeated over targets | Create multi-step symbolic dilution series | dilution correctness, cumulative volume error |

Additional future task families are cataloged in `docs/MaholoBioBench_TASK_TREE.md`.

## 4. Required State Semantics

Each episode must track these state groups.

### Container State

- `container_id`
- `container_type`
- `pose`
- `is_open`
- `current_location`
- `sample_id`
- `volume_ul`
- `contaminated`
- `temperature_zone`

### Sample State

- `sample_id`
- `sample_type`
- `volume_ul`
- `concentration`
- `container_id`
- `exposure_time_s`
- `contaminated`

### Pipette State

- `pipette_id`
- `held_by`
- `tip_attached`
- `tip_used`
- `tip_sample_id`
- `current_volume_ul`
- `max_volume_ul`

### Equipment State

- `equipment_id`
- `equipment_type`
- `door_open_angle`
- `is_open`
- `temperature`
- `contains`

### Protocol State

- `protocol_id`
- `current_step`
- `completed_steps`
- `remaining_steps`
- `violations`
- `elapsed_time_s`
- `progress_score`

## 5. Required Episode Output

Each rollout should be written to:

```text
episode_xxxxxx/
├── task_config.yaml
├── observations.npz
├── actions.csv
├── joint.csv
├── protocol_state.jsonl
├── metrics.csv
├── summary.json
├── frontview.mp4
└── agentview.mp4
```

For early debugging, videos can be optional, but `summary.json` and `protocol_state.jsonl` should not be optional.

## 6. Metrics

### Robot Metrics

- `task_success`
- `final_position_error`
- `final_orientation_error`
- `trajectory_length`
- `trajectory_smoothness`
- `collision_count`
- `collision_rate`
- `joint_limit_violation_count`
- `episode_steps`

### Protocol Metrics

- `protocol_completion_rate`
- `progress_score`
- `step_order_accuracy`
- `wrong_step_count`
- `recovery_success`

### Bio-Lab Metrics

- `sample_identity_accuracy`
- `wrong_sample_count`
- `volume_error_ul`
- `relative_volume_error`
- `contamination_violation_count`
- `tip_reuse_violation_count`
- `open_container_exposure_time_s`
- `temperature_zone_violation_count`

### Reproducibility Metrics

- `episode_schema_valid`
- `protocol_trace_valid`
- `task_config_complete`
- `evaluation_script_pass`
- `result_table_generated`

## 7. Reference Agent Protocol

The benchmark should be prepared for reference agents that demonstrate task feasibility and metric discriminability. These agents are not the main contribution.

Recommended v0.1 reference agents:

1. `scripted_expert`
2. `imitation_state`
3. `rl_state`
4. `sequence_policy_state`
5. `high_level_planner`

OpenVLA, π0, Octo, Diffusion Policy, and DPPO can be discussed as future external policies that may be evaluated on MaholoBioBench, but they should not define the core contribution of v0.1.

## 8. Phase B Implementation Milestones

### B1: Specification Freeze

- Finish this spec.
- Finalize `task_registry.yaml`.
- Finalize `protocol_state_schema.yaml`.
- Finalize `episode_output_schema.yaml`.

Exit criterion:

- Every benchmark task has a task id, level, environment basis, goal, success condition, and metrics.

### B2: Protocol State Engine

- Implement symbolic container/sample/pipette/equipment/protocol state.
- Implement liquid state updates.
- Implement contamination rules.
- Implement progress score.

Exit criterion:

- A scripted rollout can emit valid `protocol_state.jsonl` and `summary.json`.

### B3: Task Wrappers

- Wrap existing Maholo tasks into benchmark API.
- Add missing Level 2 symbolic task wrappers.
- Add Level 3 protocol task state machine.

Exit criterion:

- All v0.1 tasks reset, step, terminate, and evaluate through one interface.

### B4: Expert Dataset

- Generate at least 20 expert demonstrations per task.
- Save episodes in standard format.
- Validate metrics.

Exit criterion:

- Expert success rate is high enough to prove task feasibility.

### B5: Reference Agent Table

- Run the selected reference agents under the same task contract.
- Report both geometric success and protocol-aware metrics.
- Include representative failure cases.

Exit criterion:

- At least one result table shows that protocol-aware metrics reveal failures that geometric success alone would hide.

### B6: Generalization and Metric Gap

- Evaluate seen vs unseen layouts, rack slots, sample IDs, and equipment states.
- Compare geometric success against protocol success.
- Analyze task family / instance / variation coverage.

Exit criterion:

- The benchmark demonstrates measurable difficulty differences across variations and at least one clear metric gap.

### B7: Release Package

- Package task configs.
- Package schemas.
- Package evaluation scripts.
- Package example episodes and result-table templates.

Exit criterion:

- Another user can run the evaluation script on a saved episode and reproduce the summary metrics.

## 9. Immediate Next Step

Start with B1. Do not implement new learning algorithms until the task registry and schemas are stable.
