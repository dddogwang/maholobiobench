# MaholoBioBench Benchmark 问答与调研整理

日期：2026-06-08

本文档整理了近期关于 MaholoBioBench 研究定位、机器人 benchmark 概念、已有机器人 benchmark 结构，以及 MaholoBioBench 应该如何对标这些工作的讨论。核心结论是：MaholoBioBench 的主要贡献不应被表述为某个新算法，而应被表述为面向生物实验室机器人的任务层次、任务种类、协议状态语义和评价标准。

## 1. 当前研究的核心定位

### 问题

这个研究主要目的是定义实验室机器人动作任务基础的任务层次和种类，以及判断标准吧？方法不是强调的重点吧？第一页的 Diffusion / DPPO 不需要提吧，Sim-to-Real INFORM 也不需要？

### 结论

是的。MaholoBioBench 更适合定位为一个 **benchmark / evaluation framework**，而不是一个 method paper。

更准确的研究主线应该是：

> 定义实验室机器人动作任务的层次、种类、状态语义与判断标准，让生物实验操作可以被系统化评价。

因此，第一页不应该强调 Diffusion、DPPO、INFORM 或 sim-to-real。它们容易让听众误解为主要贡献是算法或工程迁移。更合适的封面关键词是：

- Bio-Lab Manipulation
- Task Taxonomy
- Protocol State
- Evaluation Criteria

算法可以存在，但只是用于验证 benchmark 是否有效的 reference agents。例如 scripted expert、imitation agent、RL agent、sequence policy、VLA model 等。它们的作用是证明任务可执行、指标有区分度、现有方法会在 protocol-aware metrics 上暴露问题。

## 2. OpenVLA、π0 属于 Benchmark 吗？

### 问题

例如像 OpenVLA、π0 都属于 benchmark 吗？benchmark 指什么？一般都需要包括什么？

### 结论

OpenVLA 和 π0 **不是 benchmark**，它们是模型、policy 或 method。

- OpenVLA 是一个开源 Vision-Language-Action model，用视觉和语言输入输出机器人动作。它可以被拿到 LIBERO 等 benchmark 上测试。
- π0 / pi-zero 是 Physical Intelligence 提出的 generalist robot policy，用 VLA + flow matching 生成动作轨迹，目标是 general robot control。
- Benchmark 则是“考试系统”：它定义任务、环境、输入输出、成功标准、评价指标和复现实验流程。

一个简单类比：

| 角色 | 机器人研究中的对应物 |
|---|---|
| 考试题库 | benchmark 的 task suite |
| 考试规则 | observation/action space、reset、variation、split |
| 评分标准 | success rate、error、protocol violation |
| 考生 | OpenVLA、π0、Diffusion Policy、BC、RL agent |
| 标准答案 / 参考解法 | scripted expert、reference agents |
| 成绩表 | result table / leaderboard |

所以 OpenVLA 和 π0 更像“考生”，不是考试本身。

## 3. Benchmark 一般包括什么？

一个机器人 benchmark 通常至少包括以下部分：

| 组成部分 | 作用 | 例子 |
|---|---|---|
| Task Suite | 定义考题集合 | 50 个桌面操作、100 个语言操作、365 个厨房任务 |
| Task Hierarchy | 定义任务层次 | primitive、skill、long-horizon protocol |
| Environment | 定义场景和物理世界 | MuJoCo、CoppeliaSim、SAPIEN、robosuite |
| Embodiment | 定义机器人身体 | Sawyer、Franka、Panda、dual-arm、mobile manipulator |
| Objects / Assets | 定义交互对象 | block、door、drawer、rack、pipette、tube |
| Observation Space | 定义输入 | state、RGB、RGB-D、point cloud、language |
| Action Space | 定义输出 | joint action、end-effector pose、gripper、primitive API |
| Variations | 定义泛化测试 | object pose、layout、unseen object、language paraphrase |
| Success Conditions | 定义是否成功 | object in target、door open、predicate satisfied |
| Metrics | 定义评分 | success rate、completion rate、progress、collision、error |
| Demonstrations | 提供专家示范 | scripted expert、motion planner、human teleoperation |
| Splits | 定义训练和测试 | seen/unseen object、seen/unseen layout、short/long horizon |
| Reference Agents | 提供参考成绩 | BC、RL、scripted expert、VLA model |
| Evaluation Scripts | 保证可复现 | standardized rollout、logging、scoring |

对 MaholoBioBench 来说，最独特的部分应该是普通机器人 benchmark 很少定义的生物实验语义：

- sample identity
- liquid volume
- concentration
- pipette tip status
- contamination
- equipment door state
- temperature zone
- protocol progress
- step order
- protocol violation

这使得 MaholoBioBench 不只是判断“机器人有没有把东西移动到目标位置”，而是判断“机器人是否正确执行了实验协议”。

## 4. 常见机器人 Benchmark 及其考试系统

### 4.1 Meta-World

Meta-World 是一个用于 multi-task RL 和 meta-RL 的机器人操作 benchmark，包含 50 个 Sawyer 机械臂桌面操作任务。任务包括 reach、push、pick-place、door、drawer、button、peg insertion 等。

考试系统特点：

- 50 个 manipulation tasks
- MT1 / MT10 / MT50 等 multi-task 设置
- ML1 / ML10 / ML45 等 meta-learning 设置
- 主要评价 success rate
- 强调任务多样性和跨任务泛化

对 MaholoBioBench 的启发：

- 不要把 `ReachPipette` 作为顶层任务，而应定义 `ReachTargetPose` 这样的 task family。
- 具体对象如 pipette、tube、handle 作为 instances。

参考：

- https://meta-world.github.io/
- https://arxiv.org/abs/1910.10897

### 4.2 robosuite

robosuite 是基于 MuJoCo 的模块化机器人学习仿真框架，也提供标准化 benchmark environments。它强调统一机器人模型、控制器、任务环境和可复现实验接口。

考试系统特点：

- 标准化 manipulation environments
- 支持不同机器人、gripper、controller
- 常见任务包括 Lift、Stack、Door、NutAssembly、TwoArmLift 等
- 主要提供可复现的环境接口

对 MaholoBioBench 的启发：

- MaholoBioBench 需要统一 reset / step / evaluate 接口。
- 需要明确 robot model、labware assets、controller modes 和 observation modes。

参考：

- https://robosuite.ai/
- https://arxiv.org/abs/2009.12293

### 4.3 RLBench

RLBench 是面向 vision-guided robotic manipulation 的 benchmark，包含 100 个手工设计任务，从简单 reach、door opening 到 longer multi-stage tasks，例如打开 oven 并把 tray 放入。

考试系统特点：

- 100 个 unique tasks
- CoppeliaSim / PyRep 环境
- RGB、depth、segmentation、proprioception 等 observation
- 通过 motion planners 自动生成 demonstrations
- 面向 imitation learning、RL、multi-task learning、few-shot learning

对 MaholoBioBench 的启发：

- 任务不需要都是真实实验完整流程，也可以是从 primitive 到 multi-stage 的分层任务。
- Expert demonstration / scripted expert 是 benchmark 可信度的重要部分。

参考：

- https://arxiv.org/abs/1909.12271

### 4.4 ManiSkill / ManiSkill2

ManiSkill2 是面向 generalizable manipulation skills 的 benchmark，包含 20 个 task families、2000+ object models 和 4M+ demonstration frames，覆盖单臂、双臂、移动操作、刚体和软体操作。

考试系统特点：

- task families 而不只是单个任务名
- 大量 object models
- 支持 RGB-D、point cloud、state input
- 支持多种 controller 和 action parameterization
- 提供 demonstrations

对 MaholoBioBench 的启发：

- 应采用 family / instance / variation 的结构。
- task family 应保持泛化，例如 `GraspLabObject`、`TransferLiquid`，而不是只定义 `GripPipette`。

参考：

- https://arxiv.org/abs/2302.04659

### 4.5 LIBERO

LIBERO 是用于 lifelong robot learning 和 knowledge transfer 的 benchmark，包含 Spatial、Object、Goal、Long、LIBERO-90 等 task suites，总共约 130 个任务。

考试系统特点：

- Spatial：考察空间关系变化
- Object：考察物体变化
- Goal：考察目标变化
- Long：考察长时序组合任务
- LIBERO-90：大规模短时序任务集合
- 评价 lifelong learning、transfer、forgetting

对 MaholoBioBench 的启发：

- 可以把 MaholoBioBench 也分成不同 evaluation suites：
  - BioLab-Spatial：位置、rack slot、设备布局变化
  - BioLab-Object：pipette、tube、plate、tip box 等对象变化
  - BioLab-Protocol：样品身份、体积、污染、步骤顺序
  - BioLab-Long：长时序实验协议

参考：

- https://arxiv.org/abs/2306.03310
- https://huggingface.co/docs/lerobot/libero

### 4.6 CALVIN

CALVIN 是 language-conditioned long-horizon robot manipulation benchmark，评估机器人是否能根据语言指令连续组合多个操作任务。

考试系统特点：

- 34 个 manipulation tasks
- 语言条件任务
- 长时序组合执行
- 评估 zero-shot 到新语言、新环境和新对象
- 典型任务包括 drawer、blocks、LED、light、slider 等

对 MaholoBioBench 的启发：

- Level 3 protocol task 可以借鉴 CALVIN 的 long-horizon evaluation。
- 生物实验协议天然是长时序任务，比普通 household task 更强调状态正确性。

参考：

- https://arxiv.org/abs/2112.03227

### 4.7 BEHAVIOR / BEHAVIOR-1K

BEHAVIOR 是 embodied AI benchmark，关注真实人类日常需求中的 household activities。BEHAVIOR-1K 包含 1000 个 everyday activities、50 个 fully interactive scenes 和 10000+ objects。

考试系统特点：

- activity-level benchmark
- 不只是单个动作，而是完整活动目标
- 强调 task definition、simulation instantiation、evaluation
- 覆盖清洁、维护、食物准备等 household activities

对 MaholoBioBench 的启发：

- MaholoBioBench 的 Level 3 可以类似 activity-level benchmark，但领域从 household activity 换成 bio-lab protocol。
- 核心难点不是单个 grasp，而是活动是否完整且正确完成。

参考：

- https://behavior.stanford.edu/
- https://proceedings.mlr.press/v205/li23a.html

### 4.8 RoboCasa / RoboCasa365

RoboCasa 是面向 everyday kitchen tasks 的大规模仿真和 benchmark 框架。RoboCasa365 包含 365 个 everyday tasks 和 2500 个厨房环境。

考试系统特点：

- 10 个 foundational skills：pick-place、open/close doors、open/close drawers、twist knobs、turn levers、press buttons、insertion、navigation、sliding racks、open/close lids
- atomic tasks + composite tasks
- kitchen scenes
- human demonstrations 和 synthetic demonstrations

对 MaholoBioBench 的启发：

- 可以先定义 bio-lab foundational skills，再组合成 protocol tasks。
- 例如：
  - reach / grasp / transport / open
  - retrieve container / mount tip / aspirate / dispense
  - dilution series / PCR setup / media change

参考：

- https://robocasa.ai/
- https://arxiv.org/abs/2406.02523

### 4.9 VLABench

VLABench 是面向 language-conditioned robotics manipulation 和 long-horizon reasoning 的 benchmark，包含 100 个任务类别、2000+ objects，考察 VLA 模型和 embodied agents 的多维能力。

考试系统特点：

- 100 task categories
- 2000+ objects
- natural language instructions
- long-horizon reasoning
- world knowledge / common sense transfer
- 评估 mesh / texture、spatial relationship、semantic instruction、physical laws、knowledge transfer、planning 等能力

对 MaholoBioBench 的启发：

- VLABench 的价值在于把“语言和常识推理能力”变成可测任务。
- MaholoBioBench 的价值应是把“生物实验协议语义”变成可测任务。

参考：

- https://vlabench.github.io/
- https://arxiv.org/abs/2412.18194

### 4.10 SimplerEnv

SimplerEnv 不是传统大规模任务 taxonomy benchmark，而是用于真实机器人策略的可复现仿真评估框架。它尝试让仿真评估和真实机器人评估表现相关。

考试系统特点：

- 常见真实机器人设置的仿真环境
- 关注 scalable and reproducible evaluation
- 通过 paired sim-and-real evaluation 证明仿真和真实性能相关
- 可用于评估 RT-1、RT-1-X、Octo、OpenVLA 等策略

对 MaholoBioBench 的启发：

- MaholoBioBench 早期不必强调 sim-to-real，但后续可以借鉴其“可复现评估”和“仿真评价可信度验证”思路。
- 当前阶段更应先定义 task contract 和 protocol-aware metrics。

参考：

- https://simpler-env.github.io/
- https://arxiv.org/abs/2405.05941

## 5. MaholoBioBench 应该如何对标这些 Benchmark

MaholoBioBench 可以被定位为：

> A benchmark for defining and evaluating bio-laboratory robot manipulation tasks with protocol-aware state semantics and success criteria.

它应该吸收已有 benchmark 的结构：

| 已有 Benchmark | 可借鉴部分 | MaholoBioBench 中的对应设计 |
|---|---|---|
| Meta-World | task family 和多任务设置 | `ReachTargetPose`、`GraspLabObject`、`OpenArticulatedEquipment` |
| robosuite | 统一环境接口和控制器 | Maholo digital twin + reset / step / evaluate |
| RLBench | 多任务、视觉输入、示范生成 | 任务 wrapper、expert demos、episode schema |
| ManiSkill2 | family / object / variation | labware object variation、layout variation |
| LIBERO | spatial / object / goal / long suites | BioLab-Spatial、BioLab-Object、BioLab-Protocol、BioLab-Long |
| CALVIN | language-conditioned long-horizon | protocol instruction sequence |
| BEHAVIOR | activity-level evaluation | bio-lab protocol as activity |
| RoboCasa | foundational skills + composite tasks | primitive → bio-lab skill → protocol |
| VLABench | semantic reasoning evaluation | protocol state and biological constraints |
| SimplerEnv | reproducible policy evaluation | episode logs、state trace、evaluation scripts |

## 6. 推荐的 MaholoBioBench 三层任务结构

### Level 1: General Lab Manipulation Primitives

目标是定义最基础、可泛化的实验室操作 primitive。

示例 task families：

- `ReachTargetPose`
- `GraspLabObject`
- `TransportHeldObject`
- `PlaceObjectAtTarget`
- `OpenArticulatedEquipment`
- `CloseArticulatedEquipment`
- `PressOrToggleControl`
- `InsertOrRemoveObject`
- `HoldPoseUnderConstraint`
- `AlignToolToTarget`

这些 family 下的 pipette、tube、rack、door handle 都只是 instances。

### Level 2: Bio-Lab Skills

目标是定义具有生物实验语义的操作技能。

示例 task families：

- `RetrieveContainer`
- `MountDisposableTip`
- `UnmountDisposableTip`
- `AspirateLiquid`
- `DispenseLiquid`
- `TransferLiquid`
- `MixLiquid`
- `CapOrSealContainer`
- `UncapContainer`
- `LoadContainerIntoEquipment`
- `RetrieveContainerFromEquipment`
- `OperateIncubatorDoor`
- `OperateFreezerDoor`
- `PlaceTubeInRack`
- `PlacePlateOnDeck`

这些任务开始涉及 sample id、liquid volume、tip status、contamination 等 symbolic protocol state。

### Level 3: Long-Horizon Bio-Lab Protocol Tasks

目标是评估是否能正确执行实验协议，而不仅是完成几何动作。

示例 task families：

- `RetrieveAndTransferSample`
- `PrepareDilutionSeries`
- `PCRPlatePreparation`
- `MediaChangeSimplified`
- `SampleAliquoting`
- `CellCultureHandlingSimplified`
- `IncubatorTransferProtocol`
- `FreezerSampleRetrievalProtocol`
- `TubeToPlatePreparation`
- `MultiStepLiquidHandlingProtocol`

这些任务的成功标准不只是物体位置，而是 protocol state 是否满足约束。

## 7. MaholoBioBench 的独特评分标准

普通 manipulation benchmark 常见评分：

- object 到达目标
- pose error 小于阈值
- door angle 达到目标
- collision 少
- episode 成功率

MaholoBioBench 应增加 bio-lab protocol-aware metrics：

| 指标 | 含义 |
|---|---|
| Geometric Success | 几何动作是否完成 |
| Protocol Success | 实验协议是否完成 |
| Sample Identity Accuracy | 是否拿对样品 |
| Volume Error | 液体体积误差 |
| Concentration Error | 浓度或稀释比例误差 |
| Contamination Violation | 是否污染或复用 tip |
| Tip State Correctness | tip 是否安装 / 更换 / 丢弃正确 |
| Equipment State Correctness | incubator/freezer/door/temperature 状态是否正确 |
| Step Order Violation | 是否违反实验步骤顺序 |
| Progress Score | 长时序协议完成比例 |
| Recovery / Partial Credit | 错误后是否可恢复 |

关键论点：

> 一个策略可以几何上成功，但实验上失败。

例如：

- 管子放到了 rack 上，但 sample id 错了：实验失败。
- pipette 到达目标 tube，但 tip 已污染：实验失败。
- 液体被转移了，但 volume error 超阈值：实验失败。
- incubator 门打开了，但最终状态不对：部分失败或失败。
- 任务步骤顺序错误：protocol failure。

## 8. 对论文和 Slides 的建议表述

不建议这样表述：

> We propose a new robot learning method for Maholo using Diffusion / DPPO.

更建议这样表述：

> We introduce MaholoBioBench, a benchmark for defining and evaluating bio-laboratory robot manipulation tasks with protocol-aware state semantics and success criteria.

论文贡献可以写成：

1. A hierarchical task taxonomy for bio-laboratory robot manipulation, spanning general primitives, bio-lab skills, and long-horizon protocols.
2. A protocol-aware state representation covering sample identity, liquid volume, contamination, tip state, equipment state, and protocol progress.
3. A set of task families, instances, and variations instantiated in the Maholo digital twin.
4. Evaluation metrics that distinguish geometric manipulation success from biological protocol success.
5. Reference agents and reproducible evaluation scripts to expose the limitations of existing robot policies under bio-lab constraints.

## 9. 当前阶段最重要的工作

阶段 B 当前最应该完成的不是训练最强模型，而是冻结 benchmark contract：

- task family 定义
- instance / variation 定义
- reset 规则
- observation / action interface
- protocol state schema
- episode output schema
- success predicates
- metrics
- evaluation script
- scripted expert / sanity-check rollouts
- result table template

只有这些定义清楚，后续使用 OpenVLA、π0、Diffusion Policy、BC 或 RL agent 来测试才有意义。否则方法结果没有统一评分标准，也无法构成 benchmark paper。

