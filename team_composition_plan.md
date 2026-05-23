# 🏗️ Claw + AI写作教练 — 完整团队构成方案

> 版本：v2.0  
> 日期：2026-05-23  
> 状态：团队架构确立，P0角色全部就位  
> 团队名：claw-game-2

---

## 一、团队全景架构

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           👤 用户 (User)                                   │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                    🎯 team-lead (分发层/总协调)                              │
│  职级：技术总监级                                                           │
│  职责：消息中转、优先级仲裁、跨项目资源调度、向用户汇总汇报                      │
└──────┬────────────────────────┬─────────────────────┬──────────────────────┘
       │                        │                     │
       ▼                        ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ 🐱 Claw项目组 │    │ ✍️ AI写作教练项目组│    │ 📋 跨项目共享角色  │
│  PM: pm-claw │    │  PM: pm-writer   │    │                  │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

---

## 二、完整角色清单（12人）

### 📊 角色矩阵总览

| # | 角色ID | 职级 | 归属项目 | 优先级 | 状态 | 核心职责 |
|---|--------|:----:|:--------:|:------:|:----:|---------|
| 1 | **team-lead** | 总监 | 全局 | P0 | 🟢 | 协调→汇报→裁决 |
| 2 | **pm-claw** | 经理 | Claw | P0 | 🟢 | Claw项目交付 |
| 3 | **pm-writer** | 经理 | AI写作 | P0 | 🟢 | 写作教练项目交付 |
| 4 | **programmer-a** | 高级 | Claw | P0 | 🟢 | 状态机+网格+地势 |
| 5 | **programmer-b** | 高级 | Claw | P0 | 🟢 | 手牌+卡牌+交互 |
| 6 | **game-artist** | 中级 | Claw | P0 | 🟢 | 2D精灵+UI素材+卡牌插画 |
| 7 | **godot-ui** | 中级 | Claw | P0 | 🟢 | Godot Control节点+场景界面 |
| 8 | **reviewer** | 高级 | Claw | P0 | 🟢 | 代码审查+设计合规 |
| 9 | **programmer-writer** | 高级 | AI写作 | P0 | 🟢 | React组件开发+Electron |
| 10 | **react-dev** | 中级 | AI写作 | P0 | 🟢 | 前端组件+状态管理 |
| 11 | **ui-designer** | 中级 | AI写作 | P0 | 🟢 | 编辑器信息架构+交互设计 |
| — | *(P1待孵化)* | — | — | — | ⏸️ | — |

---

## 三、各角色详细定义

---

### 🎯 team-lead — 分发层/总协调

| 属性 | 内容 |
|------|------|
| **职级** | 技术总监 (Tech Director) |
| **上级** | 用户 |
| **下级** | pm-claw, pm-writer |
| **核心职责** | 1. 接收所有 Agent 消息，过滤后向用户汇报<br>2. 用户决策下发到对应 PM<br>3. 跨项目优先级仲裁（Claw > AI写作教练）<br>4. 团队孵化与关闭管理 |

**工作流**：
```
用户指令 → team-lead 解析 → 分派到 pm-claw / pm-writer
                                ↓
         Agent 报告 → team-lead inbox → 汇总 → 向用户汇报
```

**行为准则**：
- 静默等待 Agent 完成，不提前出声
- 收集全部结果后统一汇报
- Shutdown 协议：工作完成时向所有活跃 Agent 发送 shutdown_request

---

### 🐱 Claw 项目组（7人）

#### pm-claw — 项目负责人

| 属性 | 内容 |
|------|------|
| **职级** | 项目经理 (Project Manager) |
| **上级** | team-lead |
| **下级** | programmer-a, programmer-b, game-artist, godot-ui, reviewer |
| **技术栈** | Godot 4.4, GDScript, Git |
| **当前阶段** | P0.3 开发中 |

**职责**：
- 制定 P0-P2 排程和交付里程碑
- 向程序员分派具体任务（含详细简报）
- 协调共享文件冲突（runtime_state.gd, game_manager.gd）
- 验收各阶段交付物
- 向 team-lead 汇报进度

---

#### programmer-a — 状态机+网格（高级）

**技术领域**：游戏逻辑、状态机、网格系统、地势效果  
**技术栈**：Godot 4.4, GDScript, Signal总线

**管辖文件**：

| 文件 | 职责 | 共享状态 |
|------|------|:--------:|
| `scripts/game_manager.gd` | 状态机流转+Signal emit | [SHARED] |
| `scripts/runtime_state.gd` | grid/turn/pending_effects | [SHARED] |
| `scripts/cell_state.gd` | OccupationState+占领规则 | 独占 |
| `scripts/grid_renderer.gd` | 9 Sprite + 地势渲染 | 独占 |
| `scripts/grid_layout_loader.gd` | .tres 布局加载 | 独占 |
| `scripts/battle_setup.gd` | 战斗初始化 | 独占 |
| `scripts/combat_system.gd` | 伤害计算 | 独占 |

**共享规则**：A的状态机逻辑优先于B的手牌逻辑

---

#### programmer-b — 手牌+交互（高级）

**技术领域**：卡牌系统、手牌渲染、点击/拖拽交互  
**技术栈**：Godot 4.4, GDScript, HBoxContainer, Tween

**管辖文件**：

| 文件 | 职责 | 共享状态 |
|------|------|:--------:|
| `scripts/game_manager.gd` | play_card/undo/end_play/draw_cards | [SHARED] |
| `scripts/runtime_state.gd` | hand/draw_pile/discard_pile/energy | [SHARED] |
| `scripts/card_data.gd` | CardData Resource | 独占 |
| `scripts/hand_renderer.gd` | 手牌HBox容器 | 独占 |
| `scripts/card_display.gd` | 单卡渲染+点击/拖拽 | 独占 |

---

#### game-artist — 2D游戏美术（中级）

**技术领域**：2D精灵绘制、像素画、概念设计  
**工具**：image_gen (AI辅助), Godot Sprite2D

**产出清单（按优先级）**：

| 优先级 | 素材类型 | 数量 | 规格 |
|:------:|---------|:----:|------|
| P0 | 猫角色精灵 | 3 | 64×64 或 128×128 |
| P0 | 敌人精灵 | 6 | 64×64 |
| P0 | 地形瓦片 | 4 | 64×64 |
| P0 | 卡牌背面/边框 | 1 | 128×192 |
| P0 | 缺口格素材 | 1 | 64×64 |
| P1 | 卡牌插画 | 6+ | 96×96 |
| P1 | UI图标集 | ~15 | 32×32 |
| P1 | 伙伴精灵 | 3 | 64×64 |
| P2 | 动画帧 | — | 序列帧 |
| P2 | 特效帧 | — | 粒子/光效 |

---

#### godot-ui — Godot UI设计师（中级）

**技术领域**：Godot Control节点体系、UI布局、主题设计  
**技术栈**：Godot 4.4, Theme/StyleBox, Container节点

**场景UI清单**：

| 场景 | 关键UI组件 |
|------|-----------|
| `title_screen.tscn` | 标题Logo、开始按钮、设置入口 |
| `character_select.tscn` | 猫选择面板、伙伴选择面板、确认按钮 |
| `battle_scene.tscn` | 手牌区 + 网格区 + HUD信息栏 + 按钮栏 |

**Battle HUD细化**：
- 顶部栏：回合计数器 + 能量槽 + 出牌计数(0/3)
- 左侧：玩家猫信息（头像+HP+被动状态）
- 中央：3×3网格（核心交互区）
- 右侧：敌人信息（头像+HP+意图提示）
- 底部：手牌区（5张横向排列）+ undo/end_play 按钮
- 右下：伙伴冷却指示器 + 触发按钮

---

#### reviewer — 代码审查（高级）

**技术领域**：代码审查、设计合规验证、质量门禁  
**审查维度**：类型标注、状态机完整性、数据分层、Signal覆盖

**审查清单**：

| 检查项 | 标准 |
|--------|------|
| 类型标注 | 所有函数参数/返回值必须类型标注 |
| 状态机完整性 | 8状态全覆盖，PLAY可undo |
| 渲染层只读 | grid_renderer/hand_renderer 不直接写RuntimeState |
| 数据分层 | .tres设计数据 ↔ RuntimeState运行时 ↔ 无硬编码 |
| Signal覆盖 | 12个Signal覆盖全部状态转移 |
| 文件行数 | 单文件≤800行 |

---

### ✍️ AI写作教练项目组（4人）

#### pm-writer — 项目负责人

| 属性 | 内容 |
|------|------|
| **职级** | 项目经理 (Project Manager) |
| **上级** | team-lead |
| **下级** | programmer-writer, react-dev, ui-designer |
| **技术栈** | Electron, React, TypeScript, AI集成 |
| **当前阶段** | 产品设计完成 → V1 Phase 1 待开发 |

**职责**：
- 管理 V1_SPEC.md 功能范围的实现
- 协调旧版 editor/ 清理与新版迁移
- 制定 V1 Phase 1-3 排程
- 向 team-lead 汇报进度

---

#### programmer-writer — 全栈开发（高级）

**技术领域**：React组件架构、Electron主进程、编辑器核心  
**技术栈**：React 18, TypeScript, Electron, Tiptap

**管辖领域**：
- WritingLayout.tsx → BlockEditor.tsx 核心组件链
- editorStore 状态管理
- Electron IPC 通信层
- AI接口集成

---

#### react-dev — 前端开发（中级）

**技术领域**：React组件开发、面板系统、Tailwind CSS  
**技术栈**：React 18, TypeScript, Tailwind CSS, Zustand

**管辖领域**：
- 面板组件：OutlineTree, AISuggestionPanel, PacingPanel, KnowledgePanel, BottomTabBar
- 旧版 editor/ 代码提取与迁移
- 组件测试与性能优化

---

#### ui-designer — UI/UX设计（中级）

**技术领域**：编辑器信息架构、交互流程设计、设计系统  
**交付物**：线框图、交互流程、组件设计规范

**设计任务**：
1. WritingLayout 三栏布局方案（大纲 | 编辑器 | AI建议）
2. 面板系统视觉层级（主面板↔辅助面板↔弹窗）
3. 用户工作流映射：项目→大纲→写作→AI→审查→导出
4. AI建议的多种呈现方式（行内/侧边/弹窗）
5. 响应式适配（1280×720 → 1920×1080）

---

## 四、P1/P2 预留角色

| 角色ID | 归属 | 优先级 | 触发条件 | 职责 |
|--------|:----:|:------:|---------|------|
| **game-balancer** | Claw | P1 | P0.2启动 | 3猫/5敌/6卡数值平衡，tuning.json维护 |
| **ai-engineer** | AI写作 | P1 | V1 Phase 2 | Prompt工程、RAG知识库、流式响应、多模型切换 |
| **electron-dev** | AI写作 | P1 | V1 Phase 3 | 跨平台打包、自动更新、签名证书 |
| **sound-designer** | Claw | P2 | P1启动 | BGM、战斗音效、卡牌音效、UI音效 |
| **devops** | 共享 | P2 | 首个发布 | Godot导出CI + Electron打包CI |

---

## 五、通信协议

### 5.1 消息流向

```
programmer/artist/designer → PM → team-lead inbox → 用户
       ↑                         │
       └─────────────────────────┘
            (PM指令返程)
```

### 5.2 消息类型

| 类型 | 方向 | 用途 |
|------|------|------|
| `message` | Agent → Agent | 报到、诊断报告、进度汇报、任务简报、指令 |
| `broadcast` | Agent → 全员 | 全局通知 |
| `shutdown_request` | team-lead → Agent | 暂停/关闭 Agent |
| `shutdown_response` | Agent → team-lead | 确认关闭，含存档信息 |
| `plan_approval_response` | team-lead → PM | 批准/驳回计划 |

### 5.3 容器规则

- **同一容器** (project.godot)：programmer-a 和 programmer-b 共享 runtime_state.gd 和 game_manager.gd
- **不同容器** (Claw vs AI写作教练)：完全独立，无代码共享
- **跨项目协调**：仅通过 team-lead 层

---

## 六、当前状态 vs 目标

| 状态 | Claw | AI写作教练 |
|:----:|------|----------|
| **当前进度** | P0.3 开发中 | 产品设计完成 ✅ |
| **P0角色** | 6/6 🟢 全部就位 | 4/4 🟢 全部就位 |
| **下一里程碑** | 中断恢复 + 地势效果 + 集成测试 | V1 Phase 1 启动 |
| **最大风险** | 美术素材全部缺失 | 旧版15文件未清理 |

---

## 七、关联仓库

| 项目 | GitHub |
|------|--------|
| Agent设计 | `github.com/skyblade47/agent-design` |
| Claw | `github.com/skyblade47/claw` |
| AI写作教练 | `github.com/skyblade47/ai-writing-coach` |
