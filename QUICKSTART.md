# 🚀 Hermes Agent Framework 快速入门

欢迎使用 Hermes Agent Framework！本指南将帮助您快速上手。

## 目录

1. [项目概览](#项目概览)
2. [快速开始](#快速开始)
3. [核心功能演示](#核心功能演示)
4. [接下来做什么？](#接下来做什么)

## 项目概览

Hermes Agent Framework 基于您的 agent-design 架构，提供：

- ✅ **专业开发工具封装** - 文件操作、项目生成
- ✅ **Agent行为边界控制** - 安全检查、行为策略
- ✅ **专业Agent角色** - 基于您的12个通用角色设计
- ✅ **项目脚手架生成** - 快速创建标准化项目

## 快速开始

### 1. 查看演示

首先运行演示程序来看看框架的功能：

```bash
cd D:\onedriver\OneDrive\项目\agent-design
python examples/demo.py
```

这个演示会展示：
- 安全检查和行为控制
- 项目脚手架生成

### 2. 浏览项目结构

```
agent-design/
├── src/
│   ├── core/              # 核心引擎（Agent基类、编排器、安全控制）
│   ├── tools/             # 工具模块（文件操作等）
│   ├── agents/            # Agent角色实现
│   └── scaffold/          # 项目脚手架生成
├── examples/              # 示例代码
├── agent_prompts/         # 原设计的Agent提示词
├── ROADMAP.md             # 详细实现路线图
├── EVALUATION_REPORT.md   # 评估报告
└── QUICKSTART.md          # 本文档
```

## 核心功能演示

### 1. 安全和行为控制

框架内置了安全机制来防止Agent执行危险操作：

```python
from src.core.safety import SafetyGuard, AgentBehaviorPolicy

# 安全卫士 - 检查危险命令
safety = SafetyGuard()
result = safety.check_command("rm -rf /")  # ❌ 危险，被阻止
result = safety.check_command("ls -la")   # ✅ 安全

# 行为策略 - 定义什么可以做，什么需要审批
policy = AgentBehaviorPolicy()
allowed, reason = policy.is_allowed("删除重要文件")  # ❌ 需要审批
```

### 2. 项目脚手架生成

一键生成标准化的项目结构：

```python
from src.tools.file_tools import FileTools
from src.scaffold.project_generator import ProjectScaffoldGenerator, ProjectConfig

# 初始化工具
file_tools = FileTools(base_directory="./my_projects")
generator = ProjectScaffoldGenerator(file_tools)

# 创建项目配置
config = ProjectConfig(
    name="my-web-app",
    description="一个全栈Web应用",
    project_type="web_app",  # 可选: python_library, web_app, full_stack, cli
    author="你的名字",
)

# 生成项目！
result = generator.generate_project(config)
```

支持的项目类型：
- `python_library` - Python库项目
- `web_app` - React + FastAPI Web应用
- `full_stack` - 全栈应用
- `cli` - 命令行工具

### 3. 开发规范知识库

框架内置了专业的开发规范：

```python
from src.core.safety import DevelopmentStandards

standards = DevelopmentStandards()

# 获取文件命名规范
convention = standards.get_file_naming_convention("python")
# {"case": "snake_case", "suffix": ".py"}

# 获取项目结构建议
structure = standards.get_project_structure_guide("web_app")
# {"dirs": [...], "files": [...]}
```

## 接下来做什么？

### Phase 1 开发（当前阶段）

根据 [ROADMAP.md](./ROADMAP.md)，Phase 1 还需要：

1. **完善Agent基类和工具集成**
   - 让Agent可以实际使用文件工具
   - 集成LangChain/LangGraph

2. **实现核心Agent角色**
   - 团队负责人
   - 产品经理
   - 架构师
   - 前端/后端开发者

3. **添加更多工具**
   - Git操作工具
   - 代码格式化工具
   - 测试运行工具

### 继续阅读

- 📖 [ROADMAP.md](./ROADMAP.md) - 详细实现路线图
- 📊 [EVALUATION_REPORT.md](./EVALUATION_REPORT.md) - 项目评估报告
- 🏗️ [ARCHITECTURE.md](./ARCHITECTURE.md) - 原架构设计

## 需要帮助？

框架是为了让您即使没有专业开发知识，也能通过Agent自主完成项目！

- 文件操作都有安全边界检查
- 项目生成遵循最佳实践
- Agent角色都有明确的职责定义

祝您开发愉快！🎉

