# 🏗️ Hermes Agent Framework — 通用软件开发多Agent协作框架

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-green.svg)]()
[![Implementation](https://img.shields.io/badge/status-Design%20%2B%20MVP%20Code-orange.svg)]()

> 一套通用的、可复用的AI Agent团队设计方案。将软件工程的最佳实践（SOP、Code Review、CI/CD）与多Agent协作架构相结合，让AI Agent像专业软件团队一样工作。
>
> 🚀 **现在包含代码实现！** 基于LangGraph的可执行框架，支持您的Hermes项目开发。

---

## 📦 项目概览

本项目分为两部分：

1. **agent-design** - 完整的设计方案（原内容）
   - 架构模式、角色定义、SOP流程等
2. **Hermes实现** - 可执行的代码框架（新增）
   - 基于LangGraph的编排引擎
   - 三级记忆系统
   - 反射-评估-纠错闭环
   - 低代码可视化编排（路线图中）

### 快速上手Hermes

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的API密钥

# 3. 运行示例
python -m src.main
```

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
- **多架构模式**: 支持Supervisor、Pipeline、Swarm、Router、Handoff、Double-Layer Orchestration **六种**协作模式
- **双层编排 (v2.0)**: 引入 Dev Lead 中间层 + 批量汇报/孵化审批流/异步排序三大机制，支持多项目并行管理
- **模块化提示词**: 分层、条件化的系统提示词设计，可灵活组装
- **完整角色库**: 12+通用角色，覆盖软件开发生命周期
- **质量保障**: 内置Code Review、安全审查、测试验证机制

---

## 📚 文档导航

### Agent Design 设计方案
| 文档 | 内容 | 适合读者 |
|------|------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 5种多Agent协作架构模式 | 架构师、Tech Lead |
| [AGENT_WORKFLOW.md](./AGENT_WORKFLOW.md) | SOP驱动的标准开发流程 | PM、项目经理 |
| [ROLES_SPECIFICATION.md](./ROLES_SPECIFICATION.md) | 角色职责矩阵与选配指南 | 团队组建者 |
| [PROMPT_ENGINEERING.md](./PROMPT_ENGINEERING.md) | 提示词工程方法论 | 提示词工程师 |
| [COMMUNICATION_PROTOCOL.md](./COMMUNICATION_PROTOCOL.md) | Agent间通信协议设计 | 框架开发者 |

### Hermes 实现文档
| 文档 | 内容 | 适合读者 |
|------|------|---------|
| [ROADMAP.md](./ROADMAP.md) | 详细实现路线图，包含Phase1-3计划 | 开发者、架构师 |
| [EVALUATION_REPORT.md](./EVALUATION_REPORT.md) | 与Dify/Coze等平台的对比评估 | 决策者、技术选型 |

### 代码结构
```
src/
├── core/                     # 核心引擎
│   ├── agent_base.py        # 基础Agent类
│   └── orchestrator.py      # Team Lead编排器
├── agents/                   # 具体Agent实现
│   ├── roles/               # 12个通用角色
│   └── special/             # 特殊Agent（反射/评估/纠错）
├── memory/                   # 记忆系统
├── communication/            # 通信协议
├── workflows/                # SOP工作流
└── tools/                    # 工具集成
```

---

## 🔧 技术栈

### Hermes实现技术选择
| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **编排引擎** | LangGraph | 有状态图，内置持久化 |
| **LLM集成** | LangChain | 统一接口，多模型支持 |
| **记忆系统** | ChromaDB + RAG 2.0 | 向量数据库 |
| **API服务** | FastAPI | 高性能，自动文档 |
| **前端** | React + Tailwind | 可视化编排（路线图中） |

### 技术无关性
本设计方案是**框架和语言无关的**。你可以将其应用于：
- **Agent框架**: CodeBuddy Teams, CrewAI, AutoGen, LangGraph, 或自定义编排
- **LLM后端**: Claude, GPT, Gemini, DeepSeek, 或任何支持tool-use的模型
- **技术栈**: React/Vue/Angular, Node/Python/Go/Rust, SQL/NoSQL, 任意组合
- **项目类型**: Web应用, 移动App, 游戏, 数据管道, CLI工具, API服务

---

## 🚀 开始使用Hermes

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
```bash
cp .env.example .env
# 编辑 .env 填入你的API密钥
```

### 3. 运行示例
```bash
python -m src.main
```

### 4. 按照路线图开发
查看 [ROADMAP.md](./ROADMAP.md) 了解详细的开发计划。

---

## 📊 评估与对比

我们已对项目进行了全面评估，主要发现：

✅ **优势**: 架构设计完备，双层编排创新，完整SOP流程

⚠️ **差距**: 需要补充代码实现、记忆系统、成果控制闭环

📈 **建议**: 按照ROADMAP分3个Phase实现，从MVP到低代码平台

详细内容请参考 [EVALUATION_REPORT.md](./EVALUATION_REPORT.md)

---

## 📄 许可证

MIT License — 自由使用、修改和分发。
