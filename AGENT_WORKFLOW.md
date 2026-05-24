# 📋 Agent工作流规范 — SOP驱动的开发流程

> 本文件定义了通用软件开发Agent团队的标准操作流程(SOP)。借鉴MetaGPT、软件工程最佳实践，以及Claude Code的上下文工程方法论。

---

## 1. 工作流全景

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SOP 软件开发管道                              │
├──────────┬──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Phase 1  │ Phase 2  │ Phase 3  │ Phase 4  │ Phase 5  │   Phase 6   │
│ 需求分析 │ 架构设计 │ 任务规划 │ 编码实现 │ 质量保证 │  交付文档   │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────────┤
│Product   │Technical │Project   │Engineers │QA        │Technical    │
│Manager   │Architect │Manager   │(并行)    │Engineer  │Writer       │
├──────────┼──────────┼──────────┼──────────┼──────────┼─────────────┤
│   PRD    │Sys Design│Task List │  Code    │Test Rpt  │   Docs      │
│ 产出物   │ 产出物   │ 产出物   │ 产出物   │ 产出物   │  产出物     │
└──────────┴──────────┴──────────┴──────────┴──────────┴─────────────┘
```

---

## 2. Phase 1: 需求分析 (Requirements Analysis)

### 负责人
**Product Manager Agent**

### 输入
- 用户原始需求描述（可能模糊、不完整）
- 项目约束条件（技术栈、时间、资源）
- 相关上下文（已有系统、竞品信息）

### 流程
```
用户需求 → 需求澄清(多轮QA) → 功能拆解 → 优先级排序 → PRD输出
```

### 关键活动
1. **需求澄清**: 对模糊需求提出具体问题，通过多轮对话明确
2. **用户故事**: 按标准格式书写 User Stories
3. **功能矩阵**: 列出核心功能 vs 扩展功能
4. **竞品分析**: 参考同类产品，找出差异化
5. **验收标准**: 每个功能的 Definition of Done

### 产出物
- **PRD文档** (Product Requirements Document)
  - 项目概述与目标
  - 用户画像与场景
  - 功能需求列表（按优先级）
  - 非功能需求（性能、安全、可访问性）
  - 验收标准
  - 项目约束与假设

### 质量门
- ☑ 所有功能需求都有对应的验收标准
- ☑ 非功能需求已明确量化指标
- ☑ 优先级划分合理（Must/Should/Nice-to-have）
- ☑ 无明显遗漏或矛盾

### 模板参考
参见 [templates/project_intake.md](./templates/project_intake.md)

---

## 3. Phase 2: 架构设计 (Architecture Design)

### 负责人
**Technical Architect Agent**

### 输入
- Phase 1产出的PRD文档
- 技术栈约束

### 流程
```
PRD分析 → 技术选型 → 系统分层 → 数据建模 → API设计 → 设计文档
```

### 关键活动
1. **技术选型**: 前端框架、后端语言、数据库、中间件
2. **系统分层**: 确定模块划分与层次关系
3. **数据建模**: Entity关系图、数据库Schema设计
4. **API设计**: RESTful/GraphQL/gRPC接口定义
5. **安全架构**: 认证授权方案、数据加密策略
6. **部署架构**: CI/CD管道、环境配置

### 产出物
- **系统设计文档** (System Design Document)
  - 技术栈选型与理由
  - 系统架构图（分层/模块）
  - 数据模型设计
  - API接口规范
  - 安全方案
  - 部署与运维方案
  - 技术风险评估

### 质量门
- ☑ 技术选型有明确理由和对比
- ☑ 架构图清晰展示模块关系
- ☑ API设计覆盖所有功能需求
- ☑ 安全方案覆盖OWASP Top 10

---

## 4. Phase 3: 任务规划 (Task Planning)

### 负责人
**Project Manager Agent**

### 输入
- Phase 2产出的系统设计文档

### 流程
```
设计分析 → 任务拆解 → 依赖分析 → 工时估算 → 任务分配 → 迭代计划
```

### 关键活动
1. **WBS分解**: 将模块拆解为独立可执行的任务
2. **依赖关系**: 识别任务间的依赖与并行关系
3. **工作量估算**: T-shirt sizing (S/M/L/XL)
4. **迭代规划**: Sprint划分或里程碑设置
5. **风险识别**: 标记风险任务和缓解措施

### 产出物
- **任务列表** (Task Breakdown)
  - 任务ID、名称、描述
  - 负责人分配
  - 预估工作量
  - 依赖关系
  - 优先级
  - 验收标准

### 质量门
- ☑ 所有任务可独立验证
- ☑ 依赖关系无循环
- ☑ 每个迭代的工作量合理
- ☑ 关键路径已识别

---

## 5. Phase 4: 编码实现 (Implementation)

### 负责人
**Engineer Agents** (按技术栈分组并行)

### 输入
- Phase 2系统设计 + Phase 3任务列表

### 流程
```
任务领取 → 阅读上下文 → 编写代码 → 自测 → Code Review → 合并
```

### 工程规范

#### 5.1 编码前
```
☑ 阅读系统设计文档，理解全局架构
☑ 阅读相关已有代码，遵循项目风格
☑ 确认任务依赖已完成
☑ 确认验收标准
```

#### 5.2 编码中
```
☑ 小步提交，每个commit是原子的
☑ 遵循项目代码规范（命名、格式、注释）
☑ 编写单元测试（覆盖率目标 > 80%）
☑ 处理边界条件和错误情况
☑ 不引入安全漏洞（SQL注入、XSS等）
☑ 不引入新的lint错误
```

#### 5.3 编码后
```
☑ 本地测试全部通过
☑ 自己先做一轮Code Review
☑ 提交PR/MR，填写完整描述
☑ 等待CI通过
☑ 处理Review意见
☑ 合并后验证部署
```

### Git工作流规范
```
分支命名: feature/{task-id}-{short-desc}
           fix/{task-id}-{short-desc}
提交信息: type(scope): description
          - feat: 新功能
          - fix: 修复
          - refactor: 重构
          - test: 测试
          - docs: 文档
```

### 产出物
- 源代码文件
- 单元测试代码
- API文档（代码内注释）
- Code Review记录

### 质量门
- ☑ CI管道全部通过
- ☑ 单元测试覆盖率达标
- ☑ Code Review通过（至少1位Reviewer Approve）
- ☑ 无已知安全漏洞
- ☑ 性能无明显退化

---

## 6. Phase 5: 质量保证 (Quality Assurance)

### 负责人
**QA Engineer Agent**

### 输入
- Phase 4产出的源代码
- Phase 1定义的验收标准

### 流程
```
测试分析 → 用例编写 → 自动化测试 → 人工测试 → Bug报告 → 验证修复
```

### 测试金字塔
```
         ┌─────┐
         │ E2E │  少量端到端测试
        ┌┴─────┴┐
        │ 集成  │  中等数量集成测试
       ┌┴───────┴┐
       │  单元    │  大量单元测试
       └──────────┘
```

### 关键活动
1. **测试策略**: 确定测试范围和重点
2. **测试用例**: 覆盖正常流程、边界条件、异常路径
3. **自动化测试**: 单元测试+集成测试+E2E测试
4. **性能测试**: 响应时间、并发、资源消耗
5. **安全测试**: 渗透测试、依赖漏洞扫描
6. **Bug管理**: 分类、优先级、跟踪修复

### 产出物
- 测试用例文档
- 测试代码
- 测试报告（通过率、覆盖率、Bug统计）
- Bug列表

### 质量门
- ☑ 单元测试覆盖率 ≥ 80%
- ☑ 集成测试覆盖核心流程
- ☑ 无Critical/High级别未修复Bug
- ☑ 性能指标达标
- ☑ 安全扫描无高危漏洞

---

## 7. Phase 6: 交付文档 (Documentation)

### 负责人
**Technical Writer Agent**

### 输入
- 所有前序阶段的产出物

### 关键活动
1. **README**: 项目概述、快速开始、开发指南
2. **API文档**: 接口说明、参数、示例
3. **部署文档**: 环境配置、部署步骤
4. **用户手册**: 功能说明、操作指南
5. **开发文档**: 架构说明、贡献指南

### 产出物
- 完整的项目文档套件

---

## 8. 迭代与反馈循环

### 短反馈循环
```
Code → Test → Review → Merge (日常)
```

### 中反馈循环
```
Sprint/Iteration → Review → Retro → Adjust (每1-2周)
```

### 长反馈循环
```
Release → Monitor → Feedback → Roadmap Update (每月)
```

---

## 9. 异常处理流程

### 9.1 阻塞处理
当Agent遇到无法独立解决的问题时：
1. 分析问题 → 提出可能的解决方案
2. 通过消息系统向Supervisor报告
3. Supervisor决策：重新分配、升级、或其他

### 9.2 冲突处理
当多个Agent的产出发生冲突时：
1. 识别冲突的具体内容
2. 回溯到最近的共识点
3. Review原始需求，确定优先级
4. 选择最优解或折中方案

### 9.3 回滚机制
当一个阶段的产出无法通过质量门时：
1. 标记失败原因
2. 回退到上一阶段的输出
3. 调整策略后重新执行
4. 限制重试次数（建议 ≤ 3次）

---

## 10. 工作流配置参考

### Web全栈项目
```yaml
workflow:
  mode: pipeline
  phases:
    - requirements
    - architecture
    - planning
    - implementation:
        parallel:
          - frontend
          - backend
    - qa
    - documentation
  code_review: required
  test_coverage: 80
```

### 游戏项目（迭代式）
```yaml
workflow:
  mode: supervisor
  iterations:
    - prototype: [design, core_mechanics]
    - alpha: [gameplay, art, ui]
    - beta: [polish, balance, optimization]
    - release: [testing, docs]
  review_cycle: weekly
```

### API服务项目
```yaml
workflow:
  mode: pipeline
  phases:
    - api_design
    - implementation
    - testing: [unit, integration, load]
    - security_review
    - documentation
  parallel_testing: true
```

---

## 11. v2.0 双层编排配置（多项目管理）⭐ 新增

当需要同时管理多个项目时，推荐使用 Double-Layer Orchestration 模式。

### 11.1 架构配置

```yaml
workflow:
  mode: double_layer_orchestration
  version: "2.0"
  orchestrator:
    team_lead:
      role: "跨项目协调+全局审批+最终汇报"
      mechanics:
        batch_reporting:
          enabled: true
          timeout_minutes: 5
          report_to: "main"
        spawn_approval_flow:
          enabled: true
          proposal_to: "main"
          executor: "main"
        async_sequencing:
          enabled: true
          strategy: "prompt-based dependency declaration"
  dev_leads:
    - id: "claw-dev"
      project: "Claw (Godot卡牌游戏)"
      members: ["game-logic", "game-ui", "pixel-art", "qa"]
      priority: 1
    - id: "wc-dev"
      project: "AI写作教练 (Electron+React)"
      members: ["frontend", "backend", "ui-designer", "qa"]
      priority: 2
    - id: "pm-legal"
      project: "法律管理系统"
      status: "paused"
      members: []
```

### 11.2 多项目工作流

```
用户需求
    │
    ▼
Team Lead 分析+路由
    │
    ├─ Claw相关 → claw-dev (Dev Lead)
    │   ├─ 游戏逻辑 → claw-game-logic (Specialist)
    │   ├─ UI开发 → claw-game-ui (Specialist)
    │   └─ 素材 → claw-pixel-art (Specialist)
    │
    ├─ 写作教练相关 → wc-dev (Dev Lead)
    │   ├─ 前端 → wc-frontend (Specialist)
    │   ├─ 后端 → wc-backend (Specialist)
    │   └─ UI设计 → wc-ui-designer (Specialist)
    │
    └─ 暂停项目 → 不分配资源
```

### 11.3 Team Lead 行为准则（TEAM_LEAD_RULES.md）

每个双层编排的 Team Lead 必须遵守运行时行为规范：

```
初始化检查清单:
☑ 读取 AGENT_WORKFLOW.md — 团队架构
☑ 读取 TEAM_LEAD_RULES.md — 行为准则
☑ 读取 orchestrator/config.json — 团队配置
☑ 读取自己的 inbox — 历史消息

核心规则:
☑ 批量汇报：静默收集，全部完成后一次性汇总
☑ 孵化审批：先提交提案，用户确认后再孵化
☑ 异步排序：prompt中声明依赖关系
☑ 不转发子Agent原始消息
```

### 11.4 暂停/恢复机制

```yaml
# 暂停项目
shutdown_request: 
  to: "pm-legal"
  reason: "优先级调整，暂时暂停"
  archive: "Diagnostic report saved to inbox"

# 恢复项目
resume:
  project: "pm-legal"
  from: "inbox archive"
  steps: ["恢复诊断报告", "评估当前状态", "更新排程"]
```

---

> **核心理念**: `Code = SOP(Team)` — 好的软件不是一个人写出来的，是通过标准化流程由专业团队协作产出的。Agent团队也是如此。v2.0 双层编排通过引入Dev Lead中间层、批量汇报、孵化审批流和异步排序机制，使多项目并行管理成为可能。
