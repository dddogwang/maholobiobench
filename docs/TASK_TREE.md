# MaholoBioBench Task Tree

Date: 2026-06-08  
Status: planning catalog v0.1

This document lists the broader task tree for MaholoBioBench. Phase B should implement only a small stable subset, while the rest serves as the roadmap for later benchmark expansion.

The task tree is based on:

- current Maholo robosuite environments
- available lab object / equipment assets
- real Maholo JBI / CSV program names under `real2sim/DATA`
- common wet-lab protocol structure
- benchmark design patterns from RLBench, Meta-World, ManiSkill2, CALVIN, BEHAVIOR, and RoboCasa

## 1. Design Principle

Concrete tasks like `ReachPipette` are too narrow as benchmark primitives. They should be instances of broader task families:

```text
Task Family -> Instance -> Variation

ReachTargetPose
  -> ReachPipetteGraspPose
  -> target pose / arm / camera / layout variations

GraspLabObject
  -> GraspPipette
  -> object type / pose / affordance variations
```

This is closer to mature benchmarks:

- Meta-World uses diverse manipulation task families with random object / goal positions.
- RLBench separates task, variation, and demonstration.
- ManiSkill2 emphasizes task families with object-level geometric and topological variation.
- CALVIN and RoboCasa distinguish atomic skills from composite long-horizon tasks.

## 2. Level 1: General Lab Manipulation Primitives

These tasks test robot manipulation independent of biological protocol state.

### 2.1 ReachTargetPose

Goal: move an end-effector to a target pose defined by an object affordance, equipment handle, rack slot, or explicit coordinate.

Phase B instances:

- `ReachPipetteGraspPose`
- `ReachEquipmentHandle`

Future instances:

- `ReachTubePose`
- `ReachRackSlot`
- `ReachPlatePose`
- `ReachTipRackSlot`
- `ReachInstrumentButton`
- `ReachCameraInspectionPose`

Variations:

- object type
- target pose
- target affordance
- left/right arm
- camera view
- clutter level
- source data from real JBI target poses

### 2.2 GraspLabObject

Goal: grasp a laboratory object without excessive displacement or collision.

Phase B instances:

- `GraspPipette`

Future instances:

- `GraspTube`
- `GraspPCRPlate`
- `GraspCulturePlate`
- `GraspBottle`
- `GraspTipBox`
- `GraspRack`
- `GraspLidOrCap`
- `GraspVIAFLOPipette`

Variations:

- object type
- rack slot
- object pose
- grasp affordance
- object mass
- friction
- gripper side

### 2.3 TransportHeldObject

Goal: move a held object to a target location while respecting pose and collision constraints.

Phase B instances:

- `MovePipetteToTube`

Future instances:

- `MoveTubeToRack`
- `MoveTubeToWorkbench`
- `MoveTubeToFreezer`
- `MovePlateToThermalCycler`
- `MovePlateToIncubator`
- `MovePipetteToRack`
- `MoveTipBoxToWorkbench`
- `MoveBottleToWorkbench`

Variations:

- source pose
- target pose
- held object
- orientation constraint
- obstacle layout
- travel distance

### 2.4 PlaceObjectInFixture

Goal: insert or place an object into a constrained holder, rack, slot, or device.

Future instances:

- `PlaceTubeInRackSlot`
- `PlaceTipInTipRack`
- `PlacePCRPlateOnDeck`
- `PlacePlateInThermalCycler`
- `PlaceTubeInStorage48`
- `PlacePipetteInRack`

Variations:

- slot index
- insertion tolerance
- rack type
- object geometry
- approach direction

### 2.5 OpenArticulatedEquipment

Goal: open or close an articulated lab object or instrument.

Phase B instances:

- `OpenCoolIncubator`
- `OpenDeepFreezer`

Future instances:

- `OpenCO2Incubator`
- `CloseStorageDoor`
- `OpenThermalCyclerLid`
- `OpenTubeRackCover`
- `OpenTipBoxLid`
- `OpenBlockBathCover`
- `OpenDoorLock`

Local evidence:

- `CLI1-DOR_OP/CL`
- `C2I1-DOR_OP/CL`
- `CNA1-DOR_OP/CL`
- `DBB1-DOR_OP/CL`
- `DBB2-DOR_OP/CL`
- `FRZ1-DOR_OP/CL`
- `DSK1-COV_OP/CL`
- `T1P5-LD_OP/CL`
- `T50-LD_OP/CL`

Variations:

- equipment type
- initial door/lid angle
- target angle
- handle pose
- latch state
- friction

### 2.6 PressOrToggleInstrumentControl

Goal: press, toggle, rotate, or actuate a physical control.

Future instances:

- `PressMixerButton`
- `ToggleVortexMixer`
- `ToggleMicrotubeMixer`
- `SetCoolBlockBath`
- `ActivateCentrifugeOrMixer`
- `PressDeviceOnOff`

Local evidence:

- `CNA1-ON`
- `CNA1_OFF_PIN`
- `CNA1_ON1_PIN`
- `CNA1_ON2_PIN`
- `CNA1_ON3_PIN`
- `MXR-IO-ON`
- `MXR-IO-OFF`

Variations:

- button pose
- required force proxy
- target state
- instrument type

### 2.7 HandOrBimanualCoordination

Goal: coordinate both arms or grippers.

Future instances:

- `DualArmHoldObject`
- `OneArmHoldOneArmOperate`
- `HandOverTube`
- `StabilizeRackWhileGrasping`
- `DualArmOpenCover`

Local evidence:

- `AIST_DUALARM`
- bimanual Maholo envs in `maholoBimanualEnv`

## 3. Level 2: Bio-Lab Skill Tasks

These tasks add sample, volume, tip, container, contamination, and equipment state.

### 3.1 RetrieveContainer

Goal: retrieve the requested container while preserving sample identity.

Phase B instances:

- `RetrieveTubeFromCoolIncubator`
- `RetrieveTubeFromRack`

Future instances:

- `RetrieveTubeFromDeepFreezer`
- `RetrieveTubeFromCO2Incubator`
- `RetrievePlateFromIncubator`
- `RetrievePCRPlateFromRack`
- `RetrieveTipBox`
- `RetrieveReagentBottle`

Local evidence:

- `T1P5_GT_*`
- `T50_GT_*`
- `DI100_GT_*`
- `PCR96_GT_*`
- `HG*_GT_*`

Metrics:

- sample identity accuracy
- wrong sample count
- container pose error
- temperature-zone violation

### 3.2 StoreContainer

Goal: place a container into the correct storage location.

Future instances:

- `StoreTubeInRack`
- `StoreTubeInFreezer`
- `StorePlateInCO2Incubator`
- `StorePCRPlateInThermalCycler`
- `ReturnTipBox`

Local evidence:

- `T1P5_PT_*`
- `T50_PT_*`
- `DI100_PT_*`
- `PCR96_PT_*`
- `HG*_PT_*`

Metrics:

- correct location
- correct slot
- temperature-zone violation
- exposure time

### 3.3 MountDisposableTip

Goal: attach a clean tip and update pipette state.

Future instances:

- `MountSingleTip`
- `MountMultiChannelTip`
- `AttachVIAFLOTip`
- `CheckTipAttachment`

Local evidence:

- `AIST-VIAFLO-8CH-ATC_TIP`
- `PITASP_ATC`
- `MP-TIP*_GET-CHECK`
- `PTIP-ASP_GET-CHECK`

Metrics:

- tip attached
- tip identity
- clean tip state
- contamination violation

### 3.4 EjectDisposableTip

Goal: eject or discard a used tip.

Future instances:

- `EjectSingleTip`
- `EjectMultiChannelTips`
- `PutOffTipToWaste`

Local evidence:

- `AIST-VIAFLO-TIP_EJCT_*`
- `MP-TIP*_PUTOFF-CHECK`
- `PTIP-ASP_PUTOFF-CHECK`

Metrics:

- tip detached
- waste placement success
- contamination violation

### 3.5 TransferLiquid

Goal: transfer symbolic liquid volume with correct sample identity.

Phase B instances:

- `TubeToTubeTransfer`

Future instances:

- `TubeToPlateTransfer`
- `PlateToTubeTransfer`
- `BottleToTubeTransfer`
- `MultiChannelPlateTransfer`
- `AspirateFromRackTube`
- `DispenseToPCRPlate`

Local evidence:

- `ASP_*`
- `*_ASP_*`
- `AIST-VIAFLO-8CH_ASP_*`
- `AIST-VIAFLO-8CH_PT_*`
- `AIST-VIAFLO-8CH_GT_*`

Metrics:

- volume error
- sample identity consistency
- contamination violation
- tip reuse violation

### 3.6 MixSample

Goal: mix the sample by pipetting or instrument operation.

Future instances:

- `PipetteMixTube`
- `VortexTube`
- `MicrotubeMixerRun`
- `PlateMixByPipetting`

Local evidence:

- `MXR1-DL_TRN_HN`
- `DI100_MX_HN`
- `microtube_mixer.xml`
- `vortex_mixer.xml`

Metrics:

- mix completion
- volume retention
- contamination violation

### 3.7 CapOrSealContainer

Goal: open/close caps, lids, covers, or seals.

Future instances:

- `OpenTubeCap`
- `CloseTubeCap`
- `RemovePlateLid`
- `PlacePlateLid`
- `OpenTipBoxLid`
- `CloseTipBoxLid`

Local evidence:

- `BO30-CP_OP/CL`
- `DI100-CP_OP/CL`
- `DSK1-COV_OP/CL`
- `T1P5-LD_OP/CL`
- `T50-LD_OP/CL`

Metrics:

- open/closed state
- container displacement
- exposure time
- contamination violation

### 3.8 InspectOrVerifyState

Goal: inspect sample/container/device state.

Future instances:

- `TubePresenceCheck`
- `DoorStateCheck`
- `TipAttachmentCheck`
- `BarcodeOrLabelInspection`
- `PlateWellInspection`
- `PipetteVolumeStateCheck`

Local evidence:

- `DBB*_DOR-CHECK`
- `MP-TIP*_GET-CHECK`
- `MP-TIP*_PUTOFF-CHECK`
- `CF_GETPOS_CALC`
- `CF_PUTPOS_CALC`

Metrics:

- inspection accuracy
- false positive/negative
- observation quality proxy

### 3.9 InstrumentRun

Goal: place sample into an instrument and trigger an instrument step.

Future instances:

- `RunThermalCycler`
- `RunVortexMixer`
- `RunMicrotubeMixer`
- `RunCoolBlockBath`
- `RunBlockThermostaticBath`
- `OpenCloseDeviceForRun`

Local evidence:

- `thermal_cycler.xml`
- `vortex_mixer.xml`
- `microtube_mixer.xml`
- `block_thermostatic_bath.xml`
- `cool_block_bath.xml`

Metrics:

- correct device state
- timing violation
- temperature-zone violation
- protocol progress

## 4. Level 3: Long-Horizon Protocol Tasks

These tasks compose Level 1 and Level 2 families into protocol-level workflows.

### 4.1 RetrieveAndTransferSample

Phase B.

Example sequence:

```text
open storage -> retrieve correct sample -> mount clean tip ->
aspirate -> dispense -> return sample -> close storage
```

Core metrics:

- protocol completion
- progress score
- volume error
- sample identity error
- contamination violation

### 4.2 PrepareDilutionSeries

Phase B.

Example sequence:

```text
mount tip -> transfer stock to tube 1 -> mix ->
transfer tube 1 to tube 2 -> mix -> transfer tube 2 to tube 3
```

Core metrics:

- dilution correctness
- cumulative volume error
- protocol completion
- contamination violation

### 4.3 PipettingWorkflowWithTipChange

Future.

Purpose: explicitly test contamination-aware tip policy.

Example sequence:

```text
mount tip -> transfer sample A -> eject tip ->
mount new tip -> transfer sample B -> eject tip
```

Core metrics:

- tip reuse violation
- cross-sample contamination
- volume error

### 4.4 SampleStorageProtocol

Future.

Purpose: test temperature/location constraints.

Example sequence:

```text
retrieve sample from freezer -> move to workbench ->
perform operation -> return to correct temperature zone
```

Core metrics:

- correct storage
- exposure time
- temperature-zone violation
- sample identity accuracy

### 4.5 MediaChangeSimplified

Future.

Purpose: simplified cell culture workflow with symbolic liquid state.

Example sequence:

```text
retrieve plate -> remove old media -> add fresh media ->
return plate to CO2 incubator
```

Core metrics:

- media volume correctness
- contamination violation
- incubator state correctness

### 4.6 PCRPlatePreparation

Future.

Purpose: multi-well, multi-reagent assignment task.

Example sequence:

```text
retrieve PCR plate -> add reagent -> add sample ->
seal or place plate -> move to thermal cycler
```

Core metrics:

- well assignment accuracy
- volume error
- sample identity
- contamination violation

### 4.7 MultiomicsSamplePreparation

Future.

Purpose: connect to broader automated biology workflows.

Example modules:

- sample retrieval
- aliquoting
- reagent addition
- mixing
- incubation
- storage

Core metrics:

- protocol completion
- sample lineage correctness
- cumulative handling error
- contamination violation

### 4.8 CellCulturePassageSimplified

Future.

Purpose: simplified iPSC / mammalian cell maintenance flow.

Example sequence:

```text
retrieve plate -> aspirate old medium -> wash ->
add dissociation reagent -> transfer cell suspension ->
seed new plate -> return to incubator
```

Core metrics:

- protocol progress
- volume correctness
- exposure time
- contamination violation

### 4.9 DeviceIncubationWorkflow

Future.

Purpose: test device operation with timing and temperature constraints.

Example sequence:

```text
place prepared container into device -> close device ->
start run -> wait symbolic time -> retrieve output
```

Core metrics:

- timing violation
- equipment state error
- temperature-zone violation

## 5. Phase Prioritization

### Phase B v0.1: implement first

Task families:

1. `ReachTargetPose`
2. `GraspLabObject`
3. `TransportHeldObject`
4. `OpenArticulatedEquipment`
5. `RetrieveContainer`
6. `TransferLiquid`
7. `RetrieveAndTransferSample`
8. `PrepareDilutionSeries`

Reason:

- These map to existing environments or existing assets.
- They cover primitive, skill, and protocol levels.
- They are enough for a first benchmark paper if metrics and baselines are solid.

### Phase C: likely next expansion

Task families:

1. `MountDisposableTip`
2. `EjectDisposableTip`
3. `PlaceContainerInStorage`
4. `CapOrSealContainer`
5. `PipettingWorkflowWithTipChange`
6. `SampleStorageProtocol`

Reason:

- Strong biological semantics.
- Directly tests contamination and protocol constraints.
- Supported by many real JBI names.

### Phase D: advanced biological workflows

Task families:

1. `MediaChangeSimplified`
2. `PCRPlatePreparation`
3. `DeviceIncubationWorkflow`
4. `CellCulturePassageSimplified`
5. `MultiomicsSamplePreparation`

Reason:

- Strong paper value.
- Requires more assets, symbolic state, and possibly real validation.

## 6. How To Present This In The Paper

Use task families in the main paper:

```text
Level 1: ReachTargetPose, GraspLabObject, TransportHeldObject, OpenArticulatedEquipment
Level 2: RetrieveContainer, TransferLiquid
Level 3: RetrieveAndTransferSample, PrepareDilutionSeries
```

Use concrete instances in dataset tables:

```text
ReachTargetPose/ReachPipetteGraspPose
OpenArticulatedEquipment/OpenCoolIncubator
TransferLiquid/TubeToTubeTransfer
```

Use variations for train/test splits:

```text
train: known object types, known rack layouts, known storage device
test: held-out object poses, held-out sample IDs, held-out rack slots, held-out equipment
```

This avoids the impression of a narrow demo collection and makes the benchmark look generalizable from the beginning.

