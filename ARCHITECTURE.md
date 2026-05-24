# 🏛️ 多Agent协作架构模式

> 本文件详细描述了5种核心多Agent协作架构模式，每种模式有各自的适用场景、优势和权衡。选择合适的架构模式是构建高效Agent团队的第一步。

---

## 架构模式全景图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        多Agent协作架构模式                                │
├───────────────┬────────────────┬───────────────┬────────────────────────┤
│  Supervisor   │   Pipeline     │    Swarm      │    Double-Layer        │
│  (监督者)     │   (流水线)     │   (群体)      │   (双层编排) ⭐ v2.0   │
│  集中控制     │   顺序流转     │   并行协作     │   分层多项目管理        │
├───────────────┼────────────────┼───────────────┼────────────────────────┤
│    Router     │                │   Handoff     │                        │
│   (路由器)    │                │   (交接)      │                        │
│   智能分发    │                │ Agent间传递    │                        │
└───────────────┴────────────────┴───────────────┴────────────────────────┘
```

---

## 1. Supervisor 模式（监督者模式） ⭐ 推荐用于项目开发

### 概述
由一个中心"监督者"Agent负责任务分解、分配和协调，多个专业Agent各司其职。所有执行结果汇聚回Supervisor进行下一步决策。

### 架构图
```
                         ┌─────────────┐
                         │  Supervisor │
                         │  (TeamLead) │
                         └──┬──┬──┬───┘
                            │  │  │
              ┌─────────────┘  │  └─────────────┐
              ▼                ▼                ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Agent A │   │  Agent B │   │  Agent C │
        │ (前端开发)│   │ (后端开发)│   │ (QA测试) │
        └──────────┘   └──────────┘   └──────────┘
```

### 工作流程
1. **Supervisor** 接收任务，分析需求
2. **Supervisor** 将任务分解为子任务，分派给专业Agent
3. **专业Agent** 执行子任务，返回结果
4. **Supervisor** 汇总结果，决定下一步（继续分配 或 FINISH）
5. 循环直到任务完成

### 优势
- ✅ 集中控制，流程清晰，易于调试
- ✅ 天然支持任务优先级与分步执行
- ✅ 适合复杂的多步骤开发任务

### 劣势
- ❌ Supervisor成为单点瓶颈
- ❌ LLM调用总次数 = 所有执行轮次之和，成本较高
- ❌ 不适合需要Agent之间快速直连的场景

### 适用场景
- 复杂软件开发项目
- 需要严格流程控制的任务
- 代码审查流程
- 多模块协调开发

### 伪代码参考
```python
def supervisor(state):
    messages = state["messages"]
    response = llm.analyze(messages)
    if task_complete(response):
        return {"next": "FINISH"}
    next_agent = route_to_agent(response)
    return {"next": next_agent}

# 条件边：Supervisor → 专业Agent
graph.add_conditional_edges("supervisor", supervisor, {
    "frontend": "frontend_agent",
    "backend": "backend_agent",
    "qa": "qa_agent",
    "FINISH": END
})

# 所有专业Agent完成后返回Supervisor
graph.add_edge("frontend_agent", "supervisor")
graph.add_edge("backend_agent", "supervisor")
graph.add_edge("qa_agent", "supervisor")
```

---

## 2. Pipeline 模式（流水线模式） ⭐ 推荐用于标准开发流程

### 概述
任务按固定顺序在不同Agent之间流转，每个Agent完成自己的阶段后将结果传递给下一个Agent。这是MetaGPT采用的核心理念。

### 架构图
```
┌──────┐    ┌───────────┐    ┌────────┐    ┌──────────┐    ┌──────┐
│ 需求  │───▶│ Product   │───▶│  Tech  │───▶│ Engineer │───▶│  QA  │
│ 输入  │    │ Manager   │    │Architect│    │          │    │Engine│
└──────┘    └───────────┘    └────────┘    └──────────┘    └──────┘
                  │               │              │              │
                  ▼               ▼              ▼              ▼
              ┌───────┐     ┌──────────┐  ┌─────────┐   ┌─────────┐
              │  PRD  │     │Sys Design│  │  Code   │   │  Test   │
              │ 文档  │     │   文档   │  │  Repo   │   │ Report  │
              └───────┘     └──────────┘  └─────────┘   └─────────┘
```

### 标准SOP阶段

| 阶段 | 角色 | 输入 | 输出 | 质量门 |
|------|------|------|------|--------|
| 1. 需求分析 | Product Manager | 用户原始需求 | PRD文档 | Review通过 |
| 2. 架构设计 | Technical Architect | PRD文档 | 系统设计文档 | 架构评审 |
| 3. 任务规划 | Project Manager | 设计文档 | 任务拆分列表 | 工期合理 |
| 4. 编码实现 | Engineer(s) | 任务列表+设计 | 源代码 | Code Review |
| 5. 质量测试 | QA Engineer | 源代码 | 测试报告 | 覆盖率达标 |
| 6. 文档产出 | Technical Writer | 全部产物 | 使用文档 | 完整性检查 |

### 优势
- ✅ 流程标准化，产出可预期
- ✅ 每个阶段有明确的质量门
- ✅ 适合瀑布式或迭代式开发
- ✅ 文档齐全，可追溯

### 劣势
- ❌ 串行效率较低
- ❌ 上游错误会传导到下游
- ❌ 缺乏灵活性，不适合探索性任务

### 适用场景
- 需求明确的标准化软件开发
- 企业内部系统开发
- API服务开发
- 需要完整文档的项目

---

## 3. Swarm 模式（群体智能模式）

### 概述
多个Agent同时并行工作，通过共享状态（如黑板架构）或消息总线进行协调。无中心控制，通过涌现行为完成任务。

### 架构图
```
        ┌──────────────────────────┐
        │     Shared Blackboard    │
        │    (共享状态/消息总线)    │
        └──┬────────┬──────────┬───┘
           │        │          │
     ┌─────▼──┐ ┌──▼─────┐ ┌──▼─────┐
     │Agent A │ │Agent B │ │Agent C │
     │(并行)  │ │(并行)  │ │(并行)  │
     └────────┘ └────────┘ └────────┘
           │        │          │
           └────────┼──────────┘
                    ▼
           ┌───────────────┐
           │  Synthesizer  │
           │  (结果合成器)  │
           └───────────────┘
```

### 优势
- ✅ 真正并行执行，效率最高
- ✅ 去中心化，无单点故障
- ✅ Agent之间可互相启发

### 劣势
- ❌ 协调复杂，可能有重复工作
- ❌ 结果合成困难
- ❌ 行为不易预测和调试

### 适用场景
- 多源信息搜集与分析
- 创新/头脑风暴
- 代码库全面审计
- 并行测试生成

---

## 4. Router 模式（路由器模式）

### 概述
一个轻量级路由层根据输入特征快速分发到对应专业Agent。路由本身不参与后续处理。

### 架构图
```
                    ┌──────────┐
        ┌──────────▶│Frontend  │
        │           │  Agent   │
        │           └──────────┘
┌───────┴──┐
│  Router  │      ┌──────────┐
│ (Triage) │─────▶│ Backend  │
└───────┬──┘      │  Agent   │
        │           └──────────┘
        │           ┌──────────┐
        └──────────▶│   QA     │
                    │  Agent   │
                    └──────────┘
```

### 路由策略
1. **规则匹配优先**: 关键词/正则匹配 → 零LLM调用
2. **LLM语义分类**: 规则未命中时 → 语义理解分发
3. **单次分发**: 一个请求只分配一个Agent

### 适用场景
- 简单分类分发（技术/产品/测试）
- 延迟和成本敏感的系统
- 客服/问答类型场景

---

## 5. Handoff 模式（交接模式）

### 概述
Agent之间直接传递控制权，无需中间Supervisor。每个Agent可声明可以交接给哪些Agent。

### 适用场景
- 客服对话流转
- 需要领域专家直接协作的交互
- 复杂的多轮对话系统

---

## 🎯 架构选型决策树

```
开始
 │
 ├─ 是否同时管理 2+ 个活跃项目？
 │   ├─ 是 → 是否需要跨项目资源协调？
 │   │   ├─ 是 → 【Double-Layer Orchestration 模式】
 │   │   └─ 否 → 独立运行多个 【Supervisor 实例】
 │   │
 │   └─ 否 → 任务是否可预先分解为固定步骤？
 │       ├─ 是 → 各步骤是否需要严格顺序？
 │       │   ├─ 是 → 【Pipeline模式】
 │       │   └─ 否 → 【Swarm模式】
 │       │
 │       └─ 否 → 需要集中控制还是分布式？
 │           ├─ 集中控制 → 【Supervisor模式】
 │           ├─ 简单分发 → 【Router模式】
 │           └─ Agent直连 → 【Handoff模式】
```

### 模式对比速查表

| 维度 | Supervisor | Pipeline | Swarm | Router | Handoff | Double-Layer |
|------|-----------|----------|-------|--------|---------|-------------|
| 控制方式 | 集中式 | 顺序流转 | 去中心化 | 入口集中 | 分布式 | 分层集中 |
| 并行度 | 中 | 低 | 高 | 低 | 中 | 高 |
| 延迟 | 高（多轮） | 中 | 低 | 低 | 中 | 中高（两层） |
| LLM成本 | 高 | 中 | 高 | 低 | 中 | 高 |
| 可调试性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 典型场景 | 复杂项目 | 标准开发 | 研究探索 | 分类分发 | 客服对话 | 多项目管理 |
| 代表项目 | CodeBuddy Teams | MetaGPT | AutoGen | — | OpenAI Agents SDK | agent-design v2 |

### 复合应用

实际项目中，可以组合多种模式：

```
项目入口 ──[Router]──▶ 简单任务 → 直接处理
                    └─▶ 标准开发 → [Pipeline]
                    └─▶ 复杂任务 → [Supervisor] → [Pipeline+Swarm混合]
```

---

## 6. Double-Layer Orchestration 模式（双层编排模式）⭐ v2.0 新增

### 概述
在 Supervisor 模式基础上引入 **Dev Lead 中间层**，形成 `team-lead → Dev Lead → Specialist` 三级架构。team-lead 负责跨项目协调和全局决策，每个项目由独立的 Dev Lead 管理，Dev Lead 再孵化和管理项目专属 Specialist。

### 架构图
```
                         ┌────────────────────┐
                         │   Team Lead         │
                         │   (Supervisor)      │
                         │   跨项目协调·审批   │
                         └──┬───────┬──────┬───┘
                            │       │      │
              ┌─────────────┘       │      └─────────────┐
              ▼                     ▼                    ▼
        ┌──────────┐         ┌──────────┐         ┌──────────┐
        │ Dev Lead │         │ Dev Lead │         │ Dev Lead │
        │ (项目A)  │         │ (项目B)  │         │ (项目C)  │
        │ 任务分解 │         │ 任务分解 │         │  已暂停   │
        └────┬─────┘         └────┬─────┘         └──────────┘
             │                    │
    ┌────────┼────────┐    ┌──────┼──────┐
    ▼        ▼        ▼    ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐ ┌───┐┌────┐┌────┐
│Spec. ││Spec. ││Spec. │ │Sp.││Sp. ││Sp. │
│ A    ││ B    ││ C    │ │A  ││B   ││C   │
└──────┘└──────┘└──────┘ └───┘└────┘└────┘
```

### 三层职责

| 层级 | 角色 | 职责 |
|------|------|------|
| **L1: Orchestrator** | Team Lead | 跨项目优先级管理、资源分配、重大决策审批、最终汇总汇报 |
| **L2: Dev Lead** | claw-dev / wc-dev | 单项目任务分解、子Agent孵化和管理、项目内质量把关 |
| **L3: Specialist** | 各专业Agent | 具体任务执行（编码/美术/UI/QA），向Dev Lead汇报 |

### 通信流向
```
Specialist → Dev Lead inbox → Team Lead inbox → User
                                        ↑
                               User决策返程
```

### 关键机制

#### M1: Batch Reporting（批量汇报）
- **原则**: 静默收集所有子Agent消息，全部完成后一次性汇总汇报
- **禁止**: 每个子Agent完成后立即单独汇报
- **超时**: 5分钟无响应的子Agent标记为 ⏳ 超时，不影响汇总
- **优点**: 减少噪音、提升用户决策效率、降低上下文切换成本

#### M2: Spawn Approval Flow（孵化审批流）
- **原则**: Team Lead 不直接孵化子Agent，需先向用户提交孵化提案
- **流程**: 识别缺口 → 向 main 提交孵化提案 → 用户确认 → main 执行孵化
- **优点**: 用户对团队规模有完全掌控，避免Agent泛滥

#### M3: Async Sequencing（异步排序）
- **原则**: 在启动子Agent的 prompt 中写入依赖关系声明
- **格式**: `"你的前置依赖：等待 {agent-X} 产出 {产出物} 后再开始"`
- **策略**: 无依赖→并行启动；有依赖→等待前置完成；需审批→等待审查

### 配置文件格式

团队用 JSON 配置管理，支持 mechanics 开关：

```json
{
  "name": "orchestrator",
  "version": "2.0",
  "mechanics": {
    "batch_reporting": { "enabled": true, "timeout_minutes": 5 },
    "spawn_approval_flow": { "enabled": true },
    "async_sequencing": { "enabled": true }
  },
  "members": [
    { "memberId": "team-lead@orchestrator", "role": "Team Lead" },
    { "memberId": "claw-dev@orchestrator", "role": "Claw Dev Lead" },
    { "memberId": "wc-dev@orchestrator", "role": "WC Dev Lead" },
    // ... Specialist members
  ]
}
```

### 优势
- ✅ 支持多项目并行管理，聚焦资源在活跃项目
- ✅ Dev Lead 层隔离项目复杂度，Team Lead 专注全局
- ✅ 批量汇报消除噪音，用户始终看到全局视图
- ✅ 审批流防止 Agent 无序膨胀

### 劣势
- ❌ 增加一层通信延迟
- ❌ 配置文件复杂度上升
- ❌ 对 Team Lead 的全局协调能力要求更高

### 适用场景
- 同时管理 2+ 个活跃项目的场景
- 需要清晰的项目边界和资源分配
- 团队规模较大（10+ Agent）时需要分层管理

---

## 📊 参考架构：MetaGPT的SOP实现

MetaGPT展示了Pipeline模式在软件开发中的经典应用：

```python
class SoftwareCompany(Role):
    """软件公司的SOP流程"""
    def __init__(self):
        # 按顺序定义角色
        self.roles = [
            ProductManager(),   # Step 1: 需求分析
            Architect(),        # Step 2: 架构设计
            ProjectManager(),   # Step 3: 任务规划
            Engineer(),         # Step 4: 编码实现
            QaEngineer(),       # Step 5: 测试验证
        ]
    
    def hire(self, roles: list[Role]):
        """组建团队"""
        for role in roles:
            role.watch([prev_role.action for prev_role in roles])
    
    def run(self, idea: str):
        """执行SOP流程"""
        # 每个角色监听上游动作，产出下游所需
        self.environment.publish_message(Message(content=idea))
```

**关键设计原则**：
- **Observe-Think-Act 循环**: 每个Agent观察上游产出 → 思考分析 → 行动产出
- **结构化文档传递**: 所有中间产物通过结构化JSON/文档传递，而非自然语言
- **质量门机制**: 每个阶段完成后通过Review才进入下一阶段
- **Git版本管理**: 所有产物自动纳入版本控制

---

> **推荐组合**: 对于单项目开发，使用 **Supervisor + Pipeline 混合模式** 效果最佳。对于多项目并行管理，使用 **Double-Layer Orchestration** 模式（v2.0 新增），通过 Dev Lead 中间层隔离项目复杂度，配合批量汇报、孵化审批流、异步排序三大机制。
