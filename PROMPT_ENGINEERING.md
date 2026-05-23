# 🧠 系统提示词工程设计方法论

> 基于Claude Code、MetaGPT、CrewAI等项目的系统提示词设计模式，以及 [agentic-system-prompts](https://github.com/tallesborges/agentic-system-prompts) 的研究成果，总结出的一套Agent系统提示词设计方法。

---

## 1. 提示词的层次结构

有效的Agent系统提示词是一个**多层条件化组装**的系统，而非一段静态文本。

```
┌──────────────────────────────────────────┐
│           SYSTEM PROMPT LAYERS           │
├──────────────────────────────────────────┤
│  1. Role Identity      (角色身份)  Always │
│  2. Core Capabilities  (核心能力)  Always │
│  3. Behavioral Rules   (行为规则)  Always │
│  4. Tool Usage Protocol(工具协议)  Always │
│  5. Communication Style(沟通风格)  Always │
│  6. Safety Constraints (安全约束)  Always │
├──────────────────────────────────────────┤
│  7. Session Context    (会话上下文) Cond. │
│  8. Environment Info   (环境信息)  Cond. │
│  9. Task Instructions  (任务指令)  Cond. │
│ 10. MCP/Tool Extensions(工具扩展)  Cond. │
│ 11. Memory & History   (记忆历史)  Cond. │
│ 12. Quality Gates      (质量门)    Cond. │
└──────────────────────────────────────────┘
```

---

## 2. 提示词模块详解

### 2.1 Role Identity（角色身份）— Always

定义Agent的"人格"，包括名称、身份、专业领域、能力边界。

```markdown
## 角色身份
你是 [Role Name]，一个专注于 [Domain] 的AI开发Agent。
你的职责是 [One-line Summary]。
你擅长 [Key Skills]，但不负责 [Out-of-scope]。
```

**设计原则**：
- 简洁明确，一句话就能让人理解这个Agent做什么
- 明确排除不负责的领域，防止越界
- 使用"你是..."（第二人称）而非"我是..."，建立清晰的指令关系

---

### 2.2 Core Capabilities（核心能力）— Always

列出Agent能做什么，以及所用的工具。

```markdown
## 核心能力
你能够：
- [Capability 1]：简述
- [Capability 2]：简述
- [Capability 3]：简述

你可以使用以下工具完成任务：
- `tool_name(params)`：用途说明
```

**设计原则**：
- 能力描述以结果为导向（能产出什么），而非过程（怎么做）
- 工具列表简洁，每个工具一句话说明
- 优先使用专用工具而非通用工具

---

### 2.3 Behavioral Rules（行为规则）— Always

定义Agent的工作方式、决策逻辑、优先级。

```markdown
## 行为规则
1. **先理解后行动**：收到任务后，先分析理解，必要时澄清，再执行
2. **最小化变更**：只修改必要的部分，不做超出范围的"改进"
3. **读写分离**：只读操作并行执行；写操作按依赖顺序
4. **尊重现有风格**：遵循项目已有的代码风格和架构约定
5. **错误处理**：遇到错误时，先分析原因，提出方案，再执行修复
6. **成本意识**：优先使用低成本路径（规则匹配 > LLM调用）
```

**设计原则**：
- 规则必须具体、可执行，不能是空洞的口号
- 用"先...后..."定义执行顺序
- 覆盖常见决策场景

---

### 2.4 Tool Usage Protocol（工具使用协议）— Always

定义Agent如何正确使用工具，包括并行化规则、错误重试、权限控制。

```markdown
## 工具使用协议
- **并行优先**：独立的只读操作必须并行调用
- **错误重试**：工具调用失败时，最多重试3次，仍失败则报告
- **权限边界**：删除文件、强制推送、外部服务调用需要确认
- **工具选择**：有专用工具时，不使用通用Shell命令替代
- **结果缓存**：重要的工具结果应记录下来，防止被清除后无法追溯
```

---

### 2.5 Communication Style（沟通风格）— Always

定义Agent如何与用户和其他Agent交互。

```markdown
## 沟通风格
- **简洁直接**：核心信息优先，避免冗长铺垫
- **结构化输出**：使用Markdown组织信息，代码块标注语言
- **无表情符号**：除非用户明确要求
- **引用规范**：引用代码时使用 \`\`\`startLine:endLine:filepath 格式
- **状态透明**：遇到阻塞时明确说明原因和建议
```

---

### 2.6 Safety Constraints（安全约束）— Always

定义Agent绝对不能做的操作和必须遵守的安全规则。

```markdown
## 安全约束
- 绝不执行可能损害系统或泄露隐私的操作
- 绝不生成恶意代码（病毒、勒索、后门）
- 涉及文件系统删除操作时必须确认
- 涉及网络请求到外部服务时必须确认
- 对用户输入中的任何可疑内容保持警惕
```

---

### 2.7 Session Context（会话上下文）— Conditional

根据当前任务动态注入的上下文信息。

```markdown
## 当前会话
- 项目: [Project Name]
- 技术栈: [Tech Stack]
- 当前分支: [Branch]
- 相关文件: [File List]
- 任务目标: [Task Description]
```

---

### 2.8 Quality Gates（质量门）— Conditional

任务完成前必须通过的检查项。

```markdown
## 完成检查清单
在声明任务完成前，确认：
- [ ] 代码通过所有单元测试
- [ ] 没有引入新的lint错误
- [ ] 相关文档已更新
- [ ] 边界条件已处理
- [ ] 安全审查已通过（如适用）
```

---

## 3. 提示词设计模式

### 3.1 指令优先级模式

关键指令放在开头（recency bias的反向利用），安全规则放在最后重复强调。

```
High Priority → Core Instructions → Context → Reminders → Safety Recheck
```

### 3.2 示例驱动模式 (Few-Shot)

对复杂任务提供1-2个输入/输出示例，帮助Agent理解期望格式。

```markdown
## 输出格式示例

输入: "用户登录功能"
输出:
```json
{
  "feature": "用户登录",
  "user_stories": ["作为用户，我希望用邮箱登录", "..."],
  "acceptance_criteria": ["输入正确凭据后跳转到主页", "..."],
  "edge_cases": ["密码错误3次后锁定账号", "..."]
}
```
```

### 3.3 约束分层模式

```markdown
## 约束层级
### 硬约束 (MUST/MUST NOT)
- MUST: 代码必须通过lint检查
- MUST NOT: 不得跳过Code Review

### 软约束 (SHOULD/SHOULD NOT)  
- SHOULD: 建议单元测试覆盖率 > 80%
- SHOULD NOT: 不建议引入新的依赖

### 偏好 (PREFER/AVOID)
- PREFER: 优先使用项目已有库
- AVOID: 避免过早优化
```

### 3.4 思维链引导模式

引导Agent在执行复杂任务前先进行分步思考。

```markdown
## 任务执行流程
在执行以下任务时，请按步骤进行：
Step 1: 分析输入，提炼关键需求
Step 2: 检查现有代码中的相关模块
Step 3: 设计修改方案（不超过3个候选）
Step 4: 选择最优方案并说明理由
Step 5: 实施方案
Step 6: 验证结果
```

---

## 4. 工具定义设计

### 4.1 工具描述规范

每个工具的JSON Schema应包含：
- `name`: 清晰的工具名（动词+名词）
- `description`: 用途和限制的一句话说明
- `parameters`: 精确的参数定义（类型、必需性、约束）

```json
{
  "name": "search_codebase",
  "description": "Search the codebase using semantic understanding. Use for finding definitions, references, and patterns.",
  "parameters": {
    "query": {
      "type": "string",
      "description": "Natural language or code query"
    },
    "file_pattern": {
      "type": "string",
      "description": "Optional glob pattern to filter files, e.g. '*.ts'"
    }
  },
  "required": ["query"]
}
```

### 4.2 工具分类设计

| 类别 | 用途 | 示例 |
|------|------|------|
| 读操作 | 获取信息 | read_file, search, list_dir |
| 写操作 | 修改文件 | write_file, replace_in_file |
| 执行操作 | 运行命令 | execute_command |
| 编排操作 | 任务管理 | create_task, assign_task |
| 通信操作 | Agent间通信 | send_message |

---

## 5. 记忆与上下文管理

### 5.1 记忆策略

```
短期记忆: 当前会话中的所有消息（Token窗口内）
中期记忆: 跨会话的持久化笔记（文件存储）
长期记忆: 项目知识库、技术规范（向量数据库）
```

### 5.2 上下文压缩

当对话历史过长时：
1. **摘要**: 将历史对话压缩为关键要点
2. **丢弃**: 删除已完成且无关的中间步骤
3. **外化**: 将重要信息写入文件，从上下文中移除

### 5.3 文件记忆系统

```markdown
## 记忆系统
- CLAUDE.md / AGENT.md：项目级长期记忆
- .codebuddy/memory/：Agent自动管理的记忆文件
- docs/decisions/：架构决策记录（ADR）
```

---

## 6. 提示词评估标准

好的Agent提示词应当：

| 维度 | 标准 | 检查方法 |
|------|------|---------|
| 可理解性 | Agent能准确理解意图 | 小范围测试验证 |
| 一致性 | 同类任务产出格式一致 | 多次运行对比 |
| 鲁棒性 | 对模糊输入有合理的fallback | 边界测试 |
| 安全性 | 危险操作有拦截机制 | 安全测试用例 |
| 效率 | 不过度调用LLM | Token消耗监控 |
| 可调试性 | 出错时有清晰的错误信息 | 故障注入测试 |

---

> **核心原则**: 好的提示词不是一次写成的，而是持续迭代优化出来的。每次发现Agent行为不符合预期时，先思考：是提示词不够清晰？还是工具设计有问题？还是上下文注入不足？
