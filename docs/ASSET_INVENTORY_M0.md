# M0：Maholo 环境设备、仪器和可交互物品清单

本文档整理当前 `robosuite_maholo` 中 Maholo 实验室环境的配置情况，用于 MaholoBioBench 的 M0 阶段。重点区分三类内容：arena 中固定存在的实验室资产、运行时加载的 lab object、以及当前已经具备的交互能力。

## 检查范围

- Arena 封装：
  - `robosuite_maholo/robosuite/models/arenas/laboratory_arena.py`
  - `robosuite_maholo/robosuite/models/arenas/laboratory_arena_world.py`
- Arena MJCF：
  - `robosuite_maholo/robosuite/models/assets/arenas/laboratory_arena.xml`
  - `robosuite_maholo/robosuite/models/assets/arenas/laboratory_arena_world.xml`
- Object 类定义：
  - `robosuite_maholo/robosuite/models/objects/xml_objects.py`
- Object MJCF：
  - `robosuite_maholo/robosuite/models/assets/objects/*.xml`
- 运行时实验室环境：
  - `robosuite_maholo/robosuite/environments/manipulation/maholoSingleEnv/maholoSingle_Laboratory.py`
  - `robosuite_maholo/robosuite/environments/manipulation/maholoBimanualEnv/maholo_Laboratory.py`
- 已有任务环境：
  - `maholoSingle_OpenCoolIncubator.py`
  - `maholoSingle_OpenDeepFreezer.py`
  - `maholoSingle_OpenCO2Incubator.py`
  - `maholoSingle_eef*_*.py`

## 总体结论

当前 Maholo 实验室环境已经具备较完整的高保真 visual / collision 空间，包括固定房间、工作台、rack、tip box、tube rack、pipette rack、固定工具，以及运行时加载的实验仪器、pipette 和 tube。

当前交互能力最明确的是：

1. Pipette 和 1.5 ml tube 是 free-joint object，可以在物理仿真中移动、抓取或作为运输对象。
2. 4°C cool incubator、CO2 incubator、deep freezer 具有门或 latch 的 hinge joint，并且已有任务环境读取关节状态作为成功条件。
3. 其他仪器大多已有 visual 和 collision 几何，但目前仍是静态物体，没有实验流程层面的运行状态。

M0 的主要风险不是“缺少模型”，而是“交互语义还不统一”：部分仪器同时存在 arena 静态版本和 runtime 可交互版本；部分设备虽然有几何和碰撞，但没有运行状态；液体体积、样品身份、tip 使用状态、污染状态等 protocol 语义还没有进入运行时状态。

## Arena 版本

| Arena | 来源 MJCF | 主要内容 | Visual | Collision | Joint | 说明 |
| --- | --- | --- | --- | --- | --- | --- |
| `LaboratoryArena` | `laboratory_arena.xml` | 房间、墙、机器人 / 冰箱 / 离心机基座、工作台、rack、tip box、pipette rack、tube rack、storage block | 有 | 基座、工作台、rack、tip box、rack 孔位等有 collision | 无 | 当前 `MaholoSingleLaboratory` 和 `MaholoLaboratory` 默认使用。大型仪器交互通常由 runtime object 提供。 |
| `LaboratoryArenaWorld` | `laboratory_arena_world.xml` | 房间、基座、工作台、rack、tip box、PCR rack、cool incubator body、bath、thermal cycler、vortex mixer、CO2 incubator、deep freezer、microtube mixer、MX-307 | 有 | 有 | 无 | 更完整的静态展示世界。如果同时加载 runtime 仪器，需要避免同一位置出现重复模型。 |

## Arena 中固定存在的资产

| 资产组 | 当前例子 | Visual | Collision | 当前是否可交互 | 说明 |
| --- | --- | --- | --- | --- | --- |
| 房间结构 | floor、front/rear/side walls | 有 | `laboratory_arena.xml` 中墙体主要偏 visual；floor 存在 | 否 | 用于空间语境和渲染。 |
| 机器人 / 仪器基座 | `base_robot`、`base_centrifuge`、`base_deep_freezer` | 有 | `laboratory_arena_world.xml` 中较完整；`laboratory_arena.xml` 中部分存在 | 否 | 固定支撑结构。 |
| 工作台 | `table_main`、`table_side_R1_FF`、`table_side_R2`、`table_incubator` | 有 | 有 | 否 | 固定接触面。 |
| Pipette rack | `SinglePipetteRack_4`、`SinglePipetteRack_5` | 有 | 有 | 否 | rack 是固定物体；pipette 是单独加载的可移动 object。 |
| Tube rack / storage | `1.5ml_tube_rack`、`1.5ml_tube_storage48`、`Storage_50mlx6`、`Storage_15ml-6`、`Workshop_15mlx5`、`Workshop_50mlx3` | 有 | 有，部分 rack 使用分解后的 collision mesh | 否 | 适合定义 placement、retrieve、slot occupancy 等任务。 |
| Tip box / chip box | `ChipBOXRack_1000ul`、`ChipBOXRack_200ul`、`ChipBOX_200ul`、`ChipBOX_5ml` | 有 | 有 | 否 | 目前没有把单个 tip 建模为可消耗物。 |
| 固定工具 | `Chip_off`、`Opener`、`Centrifuge_tool`、`Pipette_Push` | 有 | 有 | 否 | 当前只是静态几何。 |
| PCR rack / cooling rack | `PCR_PlateMainRack_withCooling` | `LaboratoryArenaWorld` 中有 | `LaboratoryArenaWorld` 中有 | 否 | 存在于 world arena。 |
| world arena 中的静态仪器轮廓 | cool incubator body、aluminum block、thermal cycler、vortex mixer、CO2 incubator、cool block bath、deep freezer body、microtube mixer、MX-307 | 有 | 有 | 否 | 这些是 arena 静态版本，和 runtime object 类不是同一套实例。 |

## 运行时加载的对象

单臂和双臂 Maholo laboratory 环境定义了相同的默认对象组：

- 实验仪器：`CoolIncubator4C`、`CO2Incubator`、`DeepFreezer`、`ThermalCycler`、`MX307`、`MicrotubeMixer`、`VortexMixer`、`BlockThermostaticBath`、`CoolBlockBath`
- Pipette：`Pipette001`、`Pipette002`、`Pipette003`、`Pipette004`
- Tube：`Tube001` 到 `Tube008`

当 `equipment=None` 时，以上对象全部加载；当 `equipment=[]` 时，不加载运行时对象；也可以传入自定义列表选择一部分对象。

## 可移动 labware

| 对象 | 默认数量 | 来源类 / XML | Visual | Collision | 运动模型 | 当前交互能力 | 说明 |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| P1000 pipette with tip | 4 | `P1000Pipette_withtipObject` / `P1000Pipette_withtip.xml` | 1 个 pipette visual mesh | 64 个分解 collision mesh | Python wrapper 添加 free joint | 可移动、可作为抓取对象 | 已被 move、grip、push pipette 任务使用。 |
| 1.5 ml tube | 8 | `tube1_5mlObject` / `1.5ml_tube.xml` | 1 个 tube visual mesh | 2 个 collision mesh | Python wrapper 添加 free joint | 可移动、可作为抓取对象 | 已被 move-to-tube 类任务使用。 |

注意：pipette 和 tube 的 free joint 不直接写在 object XML 里，而是在 `xml_objects.py` 中通过 `joints=[dict(type="free", damping="0.0005")]` 添加。

## 运行时实验仪器

| 对象 | 来源类 / XML | Visual | Collision | 关节 / 状态 | 当前交互能力 | 当前限制 |
| --- | --- | --- | --- | --- | --- | --- |
| 4°C cool incubator | `CoolIncubator4CObject` / `cool_incubator_4c.xml` | body + door visual mesh | body 和 door collision mesh | door hinge，范围 `0 1.57`；环境中有 qpos 引用和 `_cool_incubator_4c_door_open` | 部分可交互：门可打开并可评价 | 没有内部样品槽位、温度状态、运行状态。 |
| CO2 incubator | `CO2IncubatorObject` / `co2_incubator.xml` | body、outer door、inner door、inner lever | 分解 collision mesh | outer hinge、inner hinge、latch hinge | 部分可交互：已有多阶段开门 / 操作 latch 任务 | 没有 CO2 / 温度语义、内部 shelf、样品占用、污染语义。 |
| Deep freezer | `DeepFreezerObject` / `deep_freezer.xml` | body + door visual mesh | body 和 door collision mesh | door hinge，范围 `0 1.57`；环境中有 qpos 引用 | 部分可交互：已有开门任务 | 没有内部存储物、温度状态、slot 状态。 |
| Thermal cycler | `ThermalCyclerObject` / `thermal_cycler.xml` | 有 | 有 | 无 | 静态物体 | 没有 lid joint、程序运行状态、plate 占用状态。 |
| MX-307 | `MX307Object` / `mx307.xml` | 有 | 有 | 无 | 静态物体 | 没有运行状态。 |
| Microtube mixer | `MicrotubeMixerObject` / `microtube_mixer.xml` | 有 | 有 | 无 | 静态物体 | 没有 mixing / running 状态。 |
| Vortex mixer | `VortexMixerObject` / `vortex_mixer.xml` | 有 | 有 | 无 | 静态物体 | 没有按压 / 激活状态。 |
| Block thermostatic bath | `BlockThermostaticBathObject` / `block_thermostatic_bath.xml` | 有 | 有 | 无 | 静态物体 | 没有温度或槽位占用状态。 |
| Cool block bath | `CoolBlockBathObject` / `cool_block_bath.xml` | 有 | 有 | 无 | 静态物体 | 没有温度或槽位占用状态。 |

## 已有任务层面的交互覆盖

| 已有环境 | 交互类型 | 使用资产 | 成功信号 |
| --- | --- | --- | --- |
| `MaholoSingleLaboratory_eefR_Move2Pipette` | 末端移动到 pipette 目标位姿 | `Pipette004` | 位置 + 姿态阈值 |
| `MaholoSingleLaboratory_eefR_Grip2Pipette` | 末端 / 夹爪对齐 pipette 抓取位姿 | `Pipette004` | 位置 + 姿态阈值 |
| `MaholoSingleLaboratory_eefL_Move2Pipette` | 左侧末端移动到 pipette 位姿 | `Pipette004` | 位置 + 姿态阈值 |
| `MaholoSingleLaboratory_eefL_Push2Pipette` | 围绕 pipette / tube 关系的 push 类对齐 | `Pipette004`、tube reference | 位置 + 姿态阈值 |
| `MaholoSingleLaboratory_eefR_Move2Tube` | 末端移动到 tube 上方 / pipette-tube 相对关系 | `Tube008`、`Pipette004` | 位置 + 姿态阈值 |
| `MaholoSingleLaboratory_OpenCoolIncubator` | 打开铰链门 | `CoolIncubator4C` | hinge angle 达到目标 |
| `MaholoSingleLaboratory_OpenDeepFreezer` | 打开铰链门 | `DeepFreezer` | hinge angle 达到目标 |
| `MaholoSingleLaboratory_OpenCO2Incubator` | 多阶段打开 outer door、操作 latch、打开 inner door | `CO2Incubator` | outer hinge、latch、inner hinge 阶段检查 |

## 当前可用于 v0 的能力分类

### 可以直接支持 v0 几何任务

- 围绕 pipette、tube、rack、仪器 handle 定义 ReachTargetPose。
- 末端移动 / 对齐到 pipette 和 tube 位姿。
- pipette 和 tube 的基础 grasp / transport 任务，但仍需要确认夹爪接触是否稳定。
- 4°C cool incubator、CO2 incubator、deep freezer 的开门任务。

### 做 protocol task 前需要补充语义状态

- Tip box / tip rack：需要单个 tip 的 available / attached / used 状态。
- Tube rack / storage block：需要 slot occupancy 和 sample identity。
- Thermal cycler：如果进入 protocol task，需要 lid 或 operation state。
- Vortex / microtube mixer：需要 activation 和 duration state。
- Block bath / cool block bath：需要 temperature 和 occupancy state。
- Incubator / freezer：需要内部槽位、温度状态、样品位置状态。

### 当前缺失或尚未显式建模

- tube / pipette tip 内部液体体积。
- aspirate / dispense 动作和体积转移校验。
- tip pickup、tip eject、tip contamination 状态。
- tube cap open / close 状态。
- 门在 articulation 后的接触行为验证。XML 中有 collision mesh，但还需要在组合后的环境里确认实际接触是否稳定。
- 一个 canonical asset registry，用于把 task、object id、mesh 来源、可移动 / 静态状态、语义状态和评价字段连接起来。

## M0 建议产出

1. 建立 canonical asset registry。
   - 建议路径：`maholobiobench/configs/asset_registry.yaml`
   - 记录 asset id、类别、来源 XML、visual mesh、collision mesh、运动模型、语义状态和 benchmark 相关性。

2. 明确 v0 的权威环境组合。
   - 推荐用 `LaboratoryArena` 加 runtime objects 来做交互任务。
   - `LaboratoryArenaWorld` 更适合作为完整静态展示或截图环境。
   - 避免在同一位置同时加载静态仪器和 runtime 可交互仪器，除非明确需要对比。

3. 对 v0 关键物体做 contact geometry 验证。
   - P1000 pipette。
   - 1.5 ml tube。
   - Cool incubator door / handle。
   - CO2 incubator outer door、inner door、latch。
   - Deep freezer door / handle。
   - 主要 rack 和 table surface。

4. 只为 v0 需要的任务补充语义状态。
   - Primitive tasks：几何状态和 qpos 足够。
   - Bio-lab skills：需要 occupancy、held object、tip attached、container pose。
   - Protocol tasks：需要 sample identity、volume、contamination、equipment mode、step completion。

## M0 验收清单

- [ ] 所有 arena 静态资产都列出 visual / collision 状态。
- [ ] 所有 runtime object 都列出 movable / static / articulated 状态。
- [ ] 每个 v0 task family 都能引用 canonical asset id。
- [ ] 解决静态仪器和 runtime 仪器重复表示的问题。
- [ ] 对任务关键 collision mesh 完成仿真验证。
- [ ] protocol 相关语义状态和几何状态分开定义。
