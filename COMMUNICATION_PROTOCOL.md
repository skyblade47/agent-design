# 📡 Agent间通信协议设计

> 定义多Agent团队中Agent之间如何高效、结构化地通信。包括消息格式、路由策略、上下文传递和状态同步机制。

---

## 1. 通信架构

### 1.1 通信模式对比

| 模式 | 描述 | 延迟 | 解耦度 | 适用场景 |
|------|------|------|--------|---------|
| 点对点消息 | Agent直接发送消息给另一个Agent | 低 | 低 | Supervisor模式 |
| 发布-订阅 (Pub/Sub) | Agent订阅感兴趣的消息类型 | 中 | 高 | Pipeline模式 |
| 共享黑板 | 所有Agent读写共享状态 | 低 | 中 | Swarm模式 |
| 消息队列 | 通过队列缓冲消息，异步消费 | 高 | 高 | 大规模系统 |

### 1.2 推荐架构：消息总线 + 订阅过滤

```
                  ┌──────────────────────┐
                  │    Message Bus        │
                  │   (消息总线)           │
                  └──┬───┬───┬───┬────┬──┘
                     │   │   │   │    │
          ┌──────────┘   │   │   │    └──────────┐
          ▼              ▼   ▼   ▼               ▼
     ┌─────────┐   ┌─────────┐   ┌─────────┐
     │ Agent A │   │ Agent B │   │ Agent C │
     │ w:[X,Y] │   │ w:[Y,Z] │   │ w:[X,Z] │
     └─────────┘   └─────────┘   └─────────┘
     
     w = 订阅的消息类型
```

---

## 2. 消息格式规范

### 2.1 标准消息结构

```json
{
  "id": "msg_uuid_v4",
  "type": "message_type",
  "from": {
    "role": "product-manager",
    "agent_id": "pm-001"
  },
  "to": {
    "role": "technical-architect",
    "agent_id": "arch-001" 
  },
  "in_reply_to": "msg_parent_uuid",
  "timestamp": "2026-05-23T18:00:00Z",
  "priority": "normal",
  "content": {
    "summary": "一句话摘要",
    "action": "write_prd | review_design | assign_task | report_status | ...",
    "artifacts": [
      {
        "type": "document | code | design | test_report",
        "path": "docs/prd/feature-x.md",
        "mime_type": "text/markdown"
      }
    ],
    "body": "消息主体内容（Markdown格式）",
    "metadata": {
      "project": "project-name",
      "phase": "requirements | design | implementation | testing",
      "task_id": "TASK-042"
    }
  },
  "expects_reply": true,
  "deadline": "2026-05-24T18:00:00Z"
}
```

### 2.2 消息类型枚举

```typescript
enum MessageType {
  // 任务相关
  TASK_ASSIGNMENT = "task_assignment",     // 分配任务
  TASK_STATUS = "task_status",             // 任务状态更新
  TASK_COMPLETION = "task_completion",     // 任务完成
  TASK_BLOCKED = "task_blocked",           // 任务阻塞
  
  // 产出物相关
  ARTIFACT_READY = "artifact_ready",       // 产出物就绪
  ARTIFACT_REVIEW_REQUEST = "review_request", // 请求审查
  ARTIFACT_APPROVED = "artifact_approved", // 审查通过
  ARTIFACT_REJECTED = "artifact_rejected", // 审查拒绝
  
  // 协调相关
  CLARIFICATION_REQUEST = "clarification", // 请求澄清
  DECISION_REQUEST = "decision_request",   // 请求决策
  CONFLICT_RESOLUTION = "conflict",        // 冲突解决
  STATUS_UPDATE = "status_update",         // 状态汇报
  
  // 系统相关
  SYSTEM_ERROR = "system_error",           // 系统错误
  SHUTDOWN_REQUEST = "shutdown",           // 关闭请求
  HEARTBEAT = "heartbeat",                 // 心跳检测
}
```

---

## 3. 结构化产出物传递

### 3.1 核心理念

> **不传递自然语言，传递结构化文档。** MetaGPT的研究表明，结构化中间产物比自然语言摘要能减少约40%的信息损失。

### 3.2 PRD文档传递

```json
{
  "type": "artifact_ready",
  "content": {
    "action": "write_prd",
    "artifacts": [{
      "type": "document",
      "path": "docs/prd/user-auth.json",
      "schema": "prd/v1"
    }]
  }
}
```

**PRD Schema**:
```json
{
  "project": "string",
  "version": "string", 
  "user_stories": [{
    "id": "US-001",
    "as_a": "user role",
    "i_want": "goal",
    "so_that": "benefit",
    "priority": "must | should | nice-to-have",
    "acceptance_criteria": ["string"],
    "edge_cases": ["string"]
  }],
  "non_functional": {
    "performance": "string",
    "security": "string",
    "accessibility": "string"
  }
}
```

### 3.3 设计文档传递

```json
{
  "architecture": {
    "tech_stack": { "frontend": "...", "backend": "...", "database": "..." },
    "modules": [{ "name": "string", "responsibility": "string", "dependencies": [] }],
    "data_models": [{ "entity": "string", "fields": [], "relations": [] }],
    "api_endpoints": [{ "method": "GET", "path": "...", "description": "..." }]
  }
}
```

---

## 4. 上下文传递策略

### 4.1 最小上下文原则

Agent之间只传递**当下任务所需的最小上下文**，不传递全局状态。

```python
# ❌ 错误：传递所有历史
send_message(to="architect", content=all_history)

# ✅ 正确：只传递相关上下文
send_message(to="architect", content={
    "prd_summary": "...",
    "key_decisions": ["..."],
    "constraints": ["..."],
    "reference_docs": ["docs/prd/x.md"]
})
```

### 4.2 上下文传递优先级

```
1. 任务目标和约束        （必须）
2. 上游关键产出物引用     （必须）
3. 重要决策记录          （建议）
4. 相关代码/文档路径      （按需）
5. 历史讨论摘要          （按需）
```

---

## 5. 状态同步机制

### 5.1 Agent状态机

```
                  ┌─────────┐
                  │  IDLE   │ ← 初始状态
                  └────┬────┘
                       │ receive task
                  ┌────▼────┐
                  │WORKING  │
                  └────┬────┘
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │BLOCKED   │ │COMPLETED │ │  ERROR   │
    │(等待上游) │ │(任务完成) │ │(异常终止) │
    └────┬─────┘ └──────────┘ └──────────┘
         │ unblocked
         ▼
    ┌──────────┐
    │ RESUME   │
    └──────────┘
```

### 5.2 状态汇报格式

```json
{
  "type": "status_update",
  "content": {
    "agent": "frontend-developer",
    "status": "working | blocked | completed | error",
    "current_task": "TASK-042",
    "progress": "60%",
    "blockers": ["等待后端API TASK-038完成"],
    "next_steps": ["完成组件样式", "编写单元测试"],
    "artifacts_produced": ["src/components/Login.tsx"]
  }
}
```

---

## 6. 冲突解决协议

### 6.1 冲突类型

| 类型 | 描述 | 解决方式 |
|------|------|---------|
| 设计冲突 | 两个Agent的设计方案矛盾 | Supervisor裁决 |
| 资源冲突 | 同时修改同一文件 | 锁定+顺序化 |
| 依赖冲突 | 循环依赖 | 重新分析拆解 |
| 优先级冲突 | 同一任务被不同Agent申领 | 先申领先得+Supervisor仲裁 |

### 6.2 冲突解决流程

```
冲突检测 → 识别冲突类型 → 评估影响范围 → 提出方案 → 决策 → 执行
                                                          │
                                           ┌───────────────┘
                                           ▼
                              ┌──────────────────────┐
                              │ 简单冲突 → Agent协商  │
                              │ 复杂冲突 → Supervisor │
                              │ 高风险 → 升级到人工   │
                              └──────────────────────┘
```

---

## 7. 通信协议最佳实践

### 7.1 DO

- ✅ 使用结构化JSON消息，而非自然语言
- ✅ 消息包含明确的 `action` 和 `artifacts` 引用
- ✅ 大型产出物通过文件路径引用，不嵌入消息体
- ✅ 每条消息都有唯一ID和关联ID
- ✅ 关键决策有书面记录

### 7.2 DON'T

- ❌ 不要在消息中嵌入大段代码（用文件路径引用）
- ❌ 不要发送无结构的自然语言指令
- ❌ 不要假设其他Agent能看到相同的上下文
- ❌ 不要忽略消息确认（ACK）
- ❌ 不要在未确认上游完成时开始下游工作

### 7.3 消息确认机制

```json
// 发送方
{
  "id": "msg-001",
  "type": "task_assignment",
  "content": { ... },
  "require_ack": true
}

// 接收方确认
{
  "id": "msg-002", 
  "type": "acknowledgment",
  "in_reply_to": "msg-001",
  "content": {
    "status": "accepted | rejected | deferred",
    "reason": "optional explanation"
  }
}
```

---

## 8. 通信模式选择指南

```
任务类型诊断：
├─ 简单独立任务 → 点对点直连
├─ 顺序依赖任务 → Pub/Sub + 订阅过滤  
├─ 并行探索任务 → 共享黑板
├─ 需要最终决策 → Supervisor模式
└─ 多轮交互对话 → Handoff模式
```

---

> **核心原则**: Agent间的通信质量决定了团队的协作效率。结构化、可追溯、最小上下文的通信协议是好架构的基础。
