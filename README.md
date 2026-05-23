# 🏗️ 项目开发Agent团队设计方案

> 版本：v2.0  
> 日期：2026-05-23  
> 目的：将一个AI Agent驱动的软件开发团队设计，成立为独立项目，供任何多项目开发场景复用。

---

## 项目概述

本项目定义了一套完整的**AI Agent驱动的多项目软件开发团队架构**。核心理念是将软件开发团队角色（总监、PM、程序员、美术、UI设计等）映射为专门的AI Agent，通过Team Mode实现异步协作。

当前团队为两个实际项目服务：
- 🐱 **Claw·猫咪大战** — Godot 4.4 回合制卡牌策略游戏（7人子团队）
- ✍️ **AI写作教练** — Electron+React 写作辅助工具（4人子团队）

---

## 目录结构

```
agent-design/
├── README.md                    # 本文件 - 项目概述
├── AGENT_WORKFLOW.md            # Agent工作流设定（权威文档）
├── team_composition_plan.md     # 完整团队构成方案（12人+5预留）
├── team_config.json             # 团队运行时配置
├── agent_prompts/               # 各Agent角色提示词
│   ├── team-lead.md             # 分发层/总协调
│   ├── pm-claw.md               # Claw项目负责人
│   ├── pm-writer.md             # AI写作教练项目负责人
│   ├── programmer-a.md          # 状态机+网格程序员
│   ├── programmer-b.md          # 手牌+交互程序员
│   ├── game-artist.md           # 2D游戏美术
│   ├── godot-ui.md              # Godot UI设计师
│   ├── reviewer.md              # 代码审查
│   ├── programmer-writer.md     # 全栈开发
│   ├── react-dev.md             # React前端开发
│   └── ui-designer.md           # UI/UX设计
└── templates/                   # 模板文件
    └── pm_intake_template.md    # PM启动诊断模板
```

---

## 团队架构

```
用户 (User)
  │
  ▼
team-lead (分发层/总协调)
  ├── 🐱 Claw项目组 (7人)
  │     ├── pm-claw (PM)
  │     ├── programmer-a (状态机+网格)
  │     ├── programmer-b (手牌+交互)
  │     ├── game-artist (2D美术)
  │     ├── godot-ui (UI设计)
  │     └── reviewer (代码审查)
  │
  └── ✍️ AI写作教练 (4人)
        ├── pm-writer (PM)
        ├── programmer-writer (全栈)
        ├── react-dev (前端)
        └── ui-designer (UX设计)
```

---

## 快速开始

### 1. 阅读设计文档
```bash
cat AGENT_WORKFLOW.md        # 工作流设定
cat team_composition_plan.md  # 团队角色定义
```

### 2. 在新项目中应用

```bash
# 在CodeBuddy中创建团队
# 参考 agent_prompts/ 目录下的角色定义
# 使用 Task 工具孵化各Agent到新团队
```

### 3. 适配到你的项目

1. 复制 `agent_prompts/` 中相关的角色提示词
2. 修改提示词中的项目路径和具体任务
3. 参考 `AGENT_WORKFLOW.md` 中的通信协议设置团队

---

## 设计原则

| 原则 | 说明 |
|------|------|
| **单一PM** | 每个项目一个PM，统一管理排程和交付 |
| **共享文件规则** | 明确冲突规则（如状态机优先于手牌） |
| **静默等待** | Team-lead不提前输出，收集全结果后统一汇报 |
| **Shutdown协议** | 工作完成时有序关闭所有Agent |
| **优先级仲裁** | 跨项目冲突由team-lead按优先级裁决 |

---

## 当前团队状态

| 项目 | P0进度 | 下一里程碑 |
|------|:------:|-----------|
| Claw | P0.3 开发中 | 中断恢复 + 地势效果 + 集成测试 |
| AI写作教练 | 产品设计完成 | V1 Phase 1 启动 |

---

## 关联仓库

| 项目 | GitHub |
|------|--------|
| Agent设计（本项目） | `github.com/skyblade47/agent-design` |
| Claw·猫咪大战 | `github.com/skyblade47/claw` |
| AI写作教练 | `github.com/skyblade47/ai-writing-coach` |

---

## 许可

MIT License — 团队设计方案可自由适配重用。
