# 🏗️ DevAgent Framework — 通用软件开发多Agent协作框架

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)]()

> 一套通用的、可复用的AI Agent团队设计方案。将软件工程的最佳实践（SOP、Code Review、CI/CD）与多Agent协作架构相结合，让AI Agent像专业软件团队一样工作。

---

## 📖 设计理念

本框架的核心理念受以下项目的启发：

| 参考项目 | 核心贡献 | Stars |
|---------|---------|-------|
| [MetaGPT](https://github.com/geekan/MetaGPT) | SOP驱动的软件公司多Agent协作 | 50k+ |
| [CrewAI](https://github.com/crewAIInc/crewAI) | 角色+工具+目标的轻量编排 | 25k+ |
| [AutoGen](https://github.com/microsoft/autogen) | 多Agent对话式协作 | 40k+ |
| [agentic-design-patterns](https://github.com/zeljkoavramovic/agentic-design-patterns) | 29种Agentic设计模式教程 | — |
| [agentic-system-prompts](https://github.com/tallesborges/agentic-system-prompts) | 生产级Agent系统提示词收集 | — |

**核心公式**: `Software = SOP(Agent Team)` — 将标准化操作流程应用于由AI Agent组成的团队。

---

## 🏛️ 项目结构

```
agent-design/
├── README.md                    # 项目总览（本文件）
├── ARCHITECTURE.md              # 多Agent架构模式详解
├── AGENT_WORKFLOW.md            # SOP驱动的开发工作流
├── ROLES_SPECIFICATION.md       # 通用角色定义与职责矩阵
├── PROMPT_ENGINEERING.md        # 系统提示词工程设计方法论
├── COMMUNICATION_PROTOCOL.md    # Agent间通信协议设计
├── agent_prompts/               # 各角色系统提示词模板
│   ├── team-lead.md             # 技术负责人/团队协调者
│   ├── product-manager.md       # 产品经理
│   ├── technical-architect.md   # 技术架构师
│   ├── project-manager.md       # 项目经理
│   ├── frontend-developer.md    # 前端开发工程师
│   ├── backend-developer.md     # 后端开发工程师
│   ├── fullstack-developer.md   # 全栈开发工程师
│   ├── qa-engineer.md           # 测试/质量工程师
│   ├── devops-engineer.md       # DevOps/基础设施工程师
│   ├── security-reviewer.md     # 安全审查工程师
│   ├── ui-ux-designer.md        # UI/UX设计师
│   └── technical-writer.md      # 技术文档工程师
├── templates/                   # 项目模板
│   ├── project_intake.md        # 项目需求摄入模板
│   ├── tech_spec_template.md    # 技术规格文档模板
│   └── review_checklist.md      # 代码审查检查清单
└── .gitignore
```

---

## 🚀 快速开始

### 1. 理解架构
阅读 [ARCHITECTURE.md](./ARCHITECTURE.md) 了解5种核心多Agent协作模式。

### 2. 配置团队
根据项目类型选择合适的角色组合：

**Web全栈项目**: TeamLead + PM + Architect + Frontend + Backend + QA + DevOps + Designer

**移动端项目**: TeamLead + PM + Architect + Mobile×2 + Backend + QA + Designer

**数据/AI项目**: TeamLead + PM + DataEngineer + MLengineer + Backend + QA

**游戏项目**: TeamLead + PM + GameDesigner + Programmer×2 + Artist + QA

### 3. 套用提示词
从 [agent_prompts/](./agent_prompts/) 选择角色，填入具体技术栈即可。

### 4. 配置工作流
参考 [AGENT_WORKFLOW.md](./AGENT_WORKFLOW.md) 设置SOP流程。

---

## 🎯 核心特性

- **通用化设计**: 不与任何特定项目、语言、框架绑定
- **SOP驱动**: 借鉴软件工程标准操作流程，确保输出质量
- **多架构模式**: 支持Supervisor、Pipeline、Swarm、Router、Handoff五种协作模式
- **模块化提示词**: 分层、条件化的系统提示词设计，可灵活组装
- **完整角色库**: 12+通用角色，覆盖软件开发生命周期
- **质量保障**: 内置Code Review、安全审查、测试验证机制

---

## 📚 文档导航

| 文档 | 内容 | 适合读者 |
|------|------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 5种多Agent协作架构模式 | 架构师、Tech Lead |
| [AGENT_WORKFLOW.md](./AGENT_WORKFLOW.md) | SOP驱动的标准开发流程 | PM、项目经理 |
| [ROLES_SPECIFICATION.md](./ROLES_SPECIFICATION.md) | 角色职责矩阵与选配指南 | 团队组建者 |
| [PROMPT_ENGINEERING.md](./PROMPT_ENGINEERING.md) | 提示词工程方法论 | 提示词工程师 |
| [COMMUNICATION_PROTOCOL.md](./COMMUNICATION_PROTOCOL.md) | Agent间通信协议设计 | 框架开发者 |

---

## 🔧 技术无关性

本设计方案是**框架和语言无关的**。你可以将其应用于：

- **Agent框架**: CodeBuddy Teams, CrewAI, AutoGen, LangGraph, 或自定义编排
- **LLM后端**: Claude, GPT, Gemini, DeepSeek, 或任何支持tool-use的模型
- **技术栈**: React/Vue/Angular, Node/Python/Go/Rust, SQL/NoSQL, 任意组合
- **项目类型**: Web应用, 移动App, 游戏, 数据管道, CLI工具, API服务

---

## 📄 许可证

MIT License — 自由使用、修改和分发。
