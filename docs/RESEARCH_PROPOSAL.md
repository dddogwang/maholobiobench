# MaholoBioBench 审稿后研究企划书

日期：2026-06-08  
定位：面向接下来整个研究推进的推荐企划书  
审阅角色：指导教授 + 机器人 benchmark 论文审稿人

## 1. 最终审阅结论

我对当前研究方向 **满意，但满意的前提是必须把主线收敛为 benchmark paper，而不是 method paper**。

推荐研究题目：

> **MaholoBioBench: A Protocol-Aware Benchmark for Bio-Laboratory Robot Manipulation in a Maholo Digital Twin**

推荐中文表述：

> **MaholoBioBench：面向生物实验室机器人的协议感知动作任务基准**

这条路线和当前研究进度高度匹配。你已经拥有 Maholo 数字孪生、实验室设备资产、已有动作环境、真实轨迹/仿真轨迹、视频与任务雏形。当前最有价值的研究产出不是再强调 Diffusion、DPPO、OpenVLA 或 sim-to-real，而是把已有工程基础组织成一个可复现、可评价、可扩展的实验室机器人 benchmark。

## 2. 初审时我不满意的地方

### 2.1 研究主张一度不够聚焦

早期材料同时出现了 benchmark、Diffusion / DPPO、VLA、sim-to-real INFORM 等关键词。这会让审稿人误解论文到底想贡献什么：

- 如果主张是新算法，当前算法创新不足。
- 如果主张是 sim-to-real，真机闭环和统计验证还不够。
- 如果主张是 benchmark，任务定义、评价语义和复现协议才是核心。

审稿意见：

> 必须把 Diffusion / DPPO / VLA / INFORM 降为 reference agents 或 future evaluation，不应作为第一页或核心贡献。

已修改：

- HTML slides 已去掉封面中的 Diffusion / DPPO / Sim-to-Real INFORM。
- Phase B spec 已把 `Baseline Protocol` 改为 `Reference Agent Protocol`。
- Phase B spec 已移除 DPPO / Diffusion / INFORM 作为 v0.1 核心评价要求。

### 2.2 背景介绍原来像“相关工作列表”，不像 benchmark 论文动机

benchmark paper 的背景必须回答：

1. 已有 benchmark 都在考什么？
2. 它们为什么不能覆盖你的问题？
3. 你的 benchmark 新定义了什么考试系统？

当前 slides 已改成大表格形式，能更清楚说明：

- Meta-World / robosuite 考基础操作与控制接口。
- RLBench / ManiSkill 考多任务、视觉和示范学习。
- LIBERO / CALVIN 考长时序、语言和泛化。
- BEHAVIOR / RoboCasa 考活动级 household manipulation。
- MaholoBioBench 要考 bio-lab protocol execution。

审稿判断：

> 修改后背景逻辑成立，已经能解释为什么需要 MaholoBioBench。

### 2.3 “结果”还不能写成已完成结果，只能写成 planned evidence

目前已有成果包括：

- Maholo 数字孪生和 labware / equipment 资产。
- 已有 reach / grasp / transport / open equipment 等任务基础。
- 已有真实轨迹、仿真 episodes、视频和动作日志。
- 已有 Phase B task registry、state schema、episode schema 草案。

但还缺少完整 benchmark paper 所需的最终结果：

- 统一 evaluation script。
- 每个 task family 的 expert feasibility result。
- reference agents 的对比表。
- geometric success vs protocol success 的 metric gap。
- seen / unseen variation 的泛化结果。

所以 slides 中应使用 “Planned Evidence / Expected Results”，而不是暗示已经有完整 benchmark results。

审稿判断：

> 当前阶段可以作为强企划书和研究计划，但还不能直接声称 benchmark 已完成。

## 3. 最终推荐研究主线

### 3.1 一句话主张

MaholoBioBench 是一个在 Maholo 数字孪生中定义和评价生物实验室机器人操作任务的 benchmark，它通过协议状态语义和实验成功标准，区分普通几何操作成功与真正的实验协议成功。

### 3.2 核心科学问题

| 问题 | 研究意义 | 需要证明的证据 |
|---|---|---|
| RQ1: 如何把生物实验协议形式化为机器人 benchmark？ | 把真实实验动作转化为可复现 task families | 任务层级、task registry、family / instance / variation |
| RQ2: 什么状态语义是 bio-lab robot benchmark 必须追踪的？ | 普通 manipulation state 不足以判断实验正确性 | sample、volume、tip、contamination、equipment、protocol state |
| RQ3: protocol-aware metrics 是否揭示普通 success rate 看不到的失败？ | 证明 benchmark 有新价值 | geometric success vs protocol success 的差异表 |
| RQ4: 现有 reference agents 在这些任务上暴露什么能力边界？ | 证明 benchmark 有区分度 | scripted / imitation / RL / sequence policy 结果表 |

### 3.3 论文贡献

建议论文贡献写成 5 点：

1. **Bio-lab robot task taxonomy**  
   定义从 general primitives、bio-lab skills 到 long-horizon protocols 的三层任务结构。

2. **Maholo digital-twin benchmark environment**  
   在 Maholo 数字孪生中实例化 labware、equipment、robot embodiments 和 task wrappers。

3. **Protocol-aware state semantics**  
   定义 sample identity、liquid volume、concentration、tip state、contamination、equipment state 和 protocol progress。

4. **Evaluation criteria beyond geometric success**  
   提出同时评价 robot geometry、protocol progress、sample correctness、liquid semantics 和 bio-lab violations 的指标体系。

5. **Reference agents and reproducible evidence**  
   提供 scripted expert、imitation / RL / sequence policy 等 reference agents，并用 result tables 证明 metric gap 和 variation difficulty。

## 4. 推荐 benchmark 结构

### 4.1 三层任务层次

| 层级 | 定义 | 代表任务 | 评价重点 |
|---|---|---|---|
| Level 1: General Primitives | 不绑定具体实验协议的基础动作能力 | ReachTargetPose、GraspLabObject、TransportHeldObject、OpenArticulatedEquipment | pose error、grasp stability、collision、object displacement |
| Level 2: Bio-Lab Skills | 带实验室物体和操作语义的技能 | RetrieveContainer、TransferLiquid、MountDisposableTip、CapOrSealContainer | sample identity、tip state、volume、equipment state |
| Level 3: Protocol Tasks | 由多个技能组成的长时序实验协议 | RetrieveAndTransferSample、PrepareDilutionSeries、MediaChangeSimplified、PCRPlatePreparation | protocol success、step order、progress、violations |

### 4.2 Phase B v0.1 推荐冻结任务

| Task Family | 层级 | v0.1 价值 |
|---|---|---|
| ReachTargetPose | Level 1 | 覆盖所有实验室对象 affordance reaching |
| GraspLabObject | Level 1 | 证明对象抓取不是只针对 pipette 的单一任务 |
| TransportHeldObject | Level 1 | 支撑取放、转移、定位等通用动作 |
| OpenArticulatedEquipment | Level 1 / 2 | 体现实验室设备交互差异 |
| RetrieveContainer | Level 2 | 引入 sample identity 和 container state |
| TransferLiquid | Level 2 | 引入 symbolic liquid state 和 tip semantics |
| RetrieveAndTransferSample | Level 3 | 组合取样与转移，形成协议任务 |
| PrepareDilutionSeries | Level 3 | 体现长时序液体处理和累计误差 |

审稿判断：

> 这 8 个任务足够构成 v0.1。不要继续扩到太多任务，否则会牺牲完成度。

## 5. 当前已有基础与还缺的关键证据

### 5.1 已有基础

| 已有基础 | 当前价值 | 如何进入论文 |
|---|---|---|
| Maholo 左/右/双臂模型 | 支撑 embodiment 和控制接口 | Environment / Implementation |
| pipette、tube、rack、tip box、incubator、freezer 等资产 | 支撑 bio-lab task instantiation | Benchmark Assets |
| reach / grasp / move / open equipment 任务 | 支撑 Level 1 task families | Task Suite |
| 真实轨迹、仿真 episodes、视频、动作日志 | 支撑 feasibility 和 demonstration | Dataset / Expert Demos |
| Phase B registry 和 schemas | 支撑 benchmark contract | Reproducibility |

### 5.2 还缺的证据

| 缺口 | 为什么重要 | 最小完成标准 |
|---|---|---|
| Unified task wrappers | 没有统一接口就不像 benchmark | 所有 v0.1 tasks 支持 reset / step / evaluate |
| Protocol state engine | 核心贡献依赖状态语义 | 输出 valid `protocol_state.jsonl` |
| Evaluation script | 没有脚本无法复现评分 | 输入 episode，输出 `summary.json` 和 result table |
| Expert feasibility | 证明任务不是不可解 | 每个 family 至少 20 expert demos |
| Metric gap analysis | 证明 protocol-aware metrics 有价值 | 展示 geometric success 与 protocol success 差异 |
| Variation split | 证明任务不是固定 demo | seen / unseen layouts、sample IDs、rack slots |

## 6. 预期结果表

最终论文至少需要以下结果表。

| Result Table | Rows | Columns / Evidence | 目的 |
|---|---|---|---|
| Task Suite Summary | 8 task families + instances | level、objects、variation、metrics | 证明任务定义完整 |
| Expert Feasibility | 8 task families | expert SR、steps、collision、progress | 证明任务可执行 |
| Reference Agent Comparison | scripted / imitation / RL / sequence | Level 1/2/3 SR、volume error、violations | 证明评分系统有区分度 |
| Metric Gap | agents / tasks | geometric success vs protocol success | 证明传统成功率不够 |
| Generalization | seen vs unseen | layout、sample ID、rack slot、equipment state | 证明可测泛化能力 |
| Reproducibility | saved episodes | schema pass、script pass、summary reproduced | 证明 benchmark 可复现 |

核心目标发现应该是：

> 现有 reference agents 可能在普通几何成功上表现可行，但在 protocol-level constraints 下明显退化。

这句话需要通过结果表支持，不能只作为口号。

## 7. 实施路线与验收标准

| 阶段 | 目标 | 交付物 | 验收标准 |
|---|---|---|---|
| B1 Spec Freeze | 冻结任务合同 | `task_registry.yaml`、state schema、episode schema | 每个 task family 有 goal、success、metrics、instances、variations |
| B2 Protocol Engine | 实现实验语义状态 | container / sample / pipette / equipment / protocol state | scripted rollout 能输出 valid protocol trace |
| B3 Task Wrappers | 统一任务接口 | reset / step / evaluate wrappers | 8 个 family 都能通过同一 API 运行 |
| B4 Expert Dataset | 证明可执行性 | 每个 family expert demos | expert SR 足够高，失败案例可解释 |
| B5 Reference Agents | 验证指标区分度 | scripted / imitation / RL / sequence policy 表 | 至少一张对比表显示 protocol metrics 差异 |
| B6 Generalization | 验证 variation 设计 | seen / unseen splits | unseen 条件显著更难或暴露不同失败 |
| B7 Release Package | 保证可复现 | configs、logs、evaluation scripts | 另一个用户可复现 summary metrics |

## 8. 风险与处理策略

| 风险 | 审稿人会怎样质疑 | 处理策略 |
|---|---|---|
| 只有 taxonomy，没有可运行环境 | “这不是 benchmark，只是任务分类” | 必须完成 reset / step / evaluate wrappers |
| 只有几何成功，没有实验语义 | “和 RLBench / ManiSkill 差异不大” | 强制加入 sample、volume、tip、contamination、equipment state |
| 任务太具体 | “只是 pipette demo，不可泛化” | 坚持 family / instance / variation 结构 |
| 算法结果弱 | “没有 method contribution” | 明确算法不是主贡献，reference agents 只是测试工具 |
| 没有真机结果 | “sim-to-real 不足” | 不把 sim-to-real 作为 v0.1 主张，只强调 digital-twin benchmark 和可复现评价 |
| 任务太多完不成 | “范围失控” | v0.1 锁定 8 个 task families，future tasks 只放 appendix / roadmap |

## 9. 投稿路线建议

### 首选方向

- ICRA / IROS workshop 或 main conference benchmark track，如果完成度足够。
- CoRL workshop，适合强调 robot learning benchmark 和 reference policies。
- RA-L，如果 benchmark 环境、指标和实验表足够完整。

### 备选方向

- CASE，适合实验室自动化和系统工程结合。
- SLAS Technology，适合 laboratory automation audience。
- IEEE Robotics and Automation Letters + conference option，如果实验证据扎实。

### 不建议现在主攻

- 纯算法顶会主线，因为当前最强贡献不是新 policy。
- 纯生命科学自动化期刊，如果没有真实湿实验闭环和生物实验结果。

## 10. 最终复审意见

### 是否满意？

**满意。**

但满意的是下面这个版本：

> MaholoBioBench 是一个 protocol-aware bio-lab robot manipulation benchmark。它的贡献是任务层级、任务种类、状态语义、评价标准、可执行环境和可复现评价，而不是某个新学习算法。

### 是否足以作为接下来研究企划书？

**可以。**

这份企划书已经具备：

- 清楚的问题背景。
- 和已有 robot benchmark 的明确差异。
- 和当前 Maholo 工程进度的自然连接。
- 可执行的 Phase B 任务范围。
- 明确的验收标准。
- 可预期的论文结果表。
- 可防御的风险边界。

### 下一步最重要的原则

不要再扩散到“我要同时做 VLA、DPPO、sim-to-real、LLM planner”。接下来 1-2 个月只做一件事：

> 把 MaholoBioBench v0.1 变成一个真正能 reset / step / evaluate / log / score 的 benchmark。

完成这个最小闭环后，方法、VLA、sim-to-real 都可以自然接上；在此之前，它们都会分散主贡献。

