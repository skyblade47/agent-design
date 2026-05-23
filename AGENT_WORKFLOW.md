# Agent Team 工作流设定文档

> 版本：v2.0（完整12人团队方案）  
> 日期：2026-05-23  
> 关联方案：team_composition_plan.md  
> 用途：多端同步时快速还原 Agent 团队架构和任务分派

---

## 一、团队架构图（v2.0 完整版）

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            👤 用户 (User)                                 │
└─────────────────────────────┬───────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      🎯 team-lead (分发层/总协调)                          │
│  团队：claw-game-2                                                        │
└──────┬──────────────────────┬──────────────────────┬─────────────────────┘
       │                      │                      │
       ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│  🐱 Claw项目组    │  │ ✍️ AI写作教练     │  │  📋 暂停项目          │
│  PM: pm-claw     │  │  PM: pm-writer   │  │  pm-legal ⏸️         │
│  7人团队          │  │  4人团队          │  │  pm-emergence ⏸️     │
└──┬───┬───┬───┬───┘  └──┬───┬───┬───┘  └──────────────────────┘
   │   │   │   │         │   │   │
   ▼   ▼   ▼   ▼         ▼   ▼   ▼
┌────┐┌────┐┌────┐┌────┐ ┌────┐┌────┐┌────┐
│prog││prog││game││godo│ │prog││reac││ui- │
│-A  ││-B  ││-art││t-ui│ │-wri││t-de││desi│
│状态││手牌││美术││UI设│ │ter ││v   ││gner│
│机  ││交互││    ││计  │ │全栈││前端││UX  │
├────┤├────┤├────┤├────┤ ├────┤├────┤├────┤
│revw│     │     │     │     │     │     │
│审查│     │     │     │     │     │     │
└────┘└────┘└────┘└────┘ └────┘└────┘└────┘
```

---

## 二、分发层 (team-lead)

### 职责

| 职能 | 说明 |
|------|------|
| **消息中转** | 所有 Agent 消息进入 team-lead inbox，过滤后向用户汇报 |
| **决策下发** | 用户确认的决策转发给对应 PM |
| **优先级管理** | 决定哪个项目优先，哪个暂停 |
| **团队孵化** | 使用 Task 工具创建 PM 和程序员到团队 |

### 关键行为准则

- **静默等待**：Agent 工作时不出声，不等结果不输出
- **结果汇总**：收集所有 Agent 成果后再统一向用户汇报
- **Shutdown 协议**：工作完成时向所有活跃 Agent 发送 shutdown_request，等待回复后 team_delete

### 当前项目优先级

| 优先级 | 项目 | 状态 |
|:------:|------|:----:|
| 1 | 🎮 Claw（猫咪大战）| 🟢 全速推进 |
| 2 | ✍️ AI写作教练 | 🟢 产品设计→开发过渡 |
| 3 | ⚖️ 法律管理系统 | ⏸️ 暂停 |
| 4 | 🌊 涌现叙事系统 | ⏸️ 暂停 |

---

## 三、项目负责人层 (PM)

### 标准工作流（两阶段模式）

**Phase 1：启动诊断**
1. 读取项目全部设计文档 + 源代码
2. 评估当前完成度 vs 目标
3. 产出诊断报告（含版本、架构、代码健康、风险、阻塞项）
4. 制定开发计划
5. 发送诊断报告 → team-lead inbox

**Phase 2：开发执行**
1. 收到用户确认后启动
2. 孵化程序员子代理（Task 工具，team mode）
3. 编写详细任务简报 → 发送给程序员
4. 协调共享文件冲突
5. 阶段性汇报进度 → team-lead

---

## 四、Claw 项目组（7人）

### pm-claw（Claw项目负责人）

项目：Claw·猫咪大战（Godot 4.4 回合制策略）  
仓库：`github.com/skyblade47/claw`  
当前阶段：P0.3 开发中  
角色：制定排程、任务分派、共享文件协调、交付验收

**管辖执行层**：programmer-a, programmer-b, game-artist, godot-ui, reviewer

**P0.1 验收标准**：
- [x] `git clone` 后 Godot 4.4 可打开运行
- [x] 3×3 九宫格含缺口格，状态机流转正确
- [ ] 手牌5张，点击选卡→目标格打出，费用扣除
- [ ] undo 退费退卡，end_play触发回合流转
- [ ] 3张 .tres 测试卡，地势颜色演示，零 console 报错

---

### programmer-a（状态机+网格，高级）

负责 D2-D8：GameState 8状态枚举 + 3×3网格渲染 + 地势系统

**管辖文件**（共享文件标注 [SHARED]）：

| 文件 | 职责 | 共享 |
|------|------|:----:|
| `scripts/game_manager.gd` | 状态机流转+Signal emit | [SHARED] |
| `scripts/runtime_state.gd` | grid/turn/pending_effects | [SHARED] |
| `scripts/cell_state.gd` | OccupationState+占领规则 | 独占 |
| `scripts/grid_renderer.gd` | 9 Sprite + 地势渲染 | 独占 |
| `scripts/grid_layout_loader.gd` | .tres 布局加载 | 独占 |
| `scripts/battle_setup.gd` | 战斗初始化 | 独占 |
| `scripts/combat_system.gd` | 伤害计算 | 独占 |

**共享规则**：A的状态机逻辑优先于B的手牌逻辑

---

### programmer-b（手牌+交互，高级）

负责 D9-D13：CardData Resource + 手牌渲染 + 点击/拖拽交互

**管辖文件**：

| 文件 | 职责 | 共享 |
|------|------|:----:|
| `scripts/game_manager.gd` | play_card/undo/end_play/draw_cards | [SHARED] |
| `scripts/runtime_state.gd` | hand/draw_pile/discard_pile/energy | [SHARED] |
| `scripts/card_data.gd` | CardData Resource | 独占 |
| `scripts/hand_renderer.gd` | 手牌HBox容器 | 独占 |
| `scripts/card_display.gd` | 单卡渲染+点击/拖拽 | 独占 |

**待验证任务**：D9-D13 手牌系统 + 交互

---

### game-artist（2D游戏美术，中级）

负责：猫/敌人/卡牌/地形精灵、UI素材、概念设计  
工具：image_gen (AI辅助), Godot Sprite2D

**产出清单**：
- P0：3猫精灵 + 6敌人精灵 + 4地形瓦片 + 卡牌素材 + 缺口格素材
- P1：卡牌插画 + UI图标集 + 伙伴精灵
- P2：动画帧 + 特效帧

---

### godot-ui（Godot UI设计师，中级）

负责：Godot Control节点体系，三个场景界面设计  
技术栈：Godot 4.4, Theme/StyleBox, Container节点

**场景UI清单**：
- `title_screen.tscn` — 标题Logo、开始按钮
- `character_select.tscn` — 猫/伙伴选择面板
- `battle_scene.tscn` — 手牌区 + 网格区 + HUD信息栏 + 按钮栏

---

### reviewer（代码审查，高级）

审查维度：类型标注、状态机完整性、数据分层、Signal覆盖、文件行数限制

---

## 五、AI写作教练项目组（4人）

### pm-writer（AI写作教练项目负责人）

项目：AI写作教练（Electron+React 写作辅助工具）  
仓库：`github.com/skyblade47/ai-writing-coach`  
当前阶段：产品设计完成 → V1 Phase 1 待开发

**管辖执行层**：programmer-writer, react-dev, ui-designer

---

### programmer-writer（全栈开发，高级）

负责：WritingLayout→BlockEditor核心组件链、editorStore、Electron IPC、AI接口  
技术栈：React 18, TypeScript, Electron, Tiptap

---

### react-dev（前端开发，中级）

负责：面板组件开发、旧版代码迁移、Tailwind CSS  
技术栈：React 18, TypeScript, Tailwind CSS, Zustand

---

### ui-designer（UI/UX设计，中级）

负责：编辑器信息架构、三栏布局方案、交互流程设计、设计系统  
交付物：线框图、交互流程、组件设计规范

---

## 六、通信协议

### 消息流向

```
programmer → PM → team-lead inbox → 用户
    ↑                      │
    └──────────────────────┘
         (用户决策返程)
```

### 消息类型

| 类型 | 方向 | 用途 |
|------|------|------|
| `message` | Agent → Agent | 诊断报告、简报、进度汇报、指令 |
| `broadcast` | Agent → 全员 | 全局通知 |
| `shutdown_request` | team-lead → Agent | 暂停/关闭 Agent |
| `shutdown_response` | Agent → team-lead | 确认关闭，含存档信息 |

### Inbox 文件结构

```
.codebuddy/teams/{team-name}/
├── config.json              ← 团队成员定义
└── inboxes/
    ├── team-lead.json       ← 分发层，所有 Agent 消息汇聚于此
    ├── pm-claw.json         ← Claw PM
    ├── pm-writer.json       ← AI写作教练 PM
    ├── programmer-a.json    ← Claw 程序员A
    └── programmer-b.json    ← Claw 程序员B
```

---

## 七、多端恢复指南

### 在新终端恢复工作流

```bash
# 1. 克隆主仓库（包含 team 配置）
git clone https://github.com/skyblade47/claw.git
cd Claw

# 2. 阅读工作流文档
cat AGENT_WORKFLOW.md

# 3. 阅读项目设定
cat SETUP.md

# 4. 从 team-lead inbox 了解最新状态
cat .codebuddy/teams/claw-game-2/inboxes/team-lead.json

# 5. 使用 Task 工具创建 team-lead：
#    name: team-lead
#    team_name: claw-game-2
```

### 恢复后首要行动
1. 读完 team-lead inbox 最新消息
2. 确认各项目当前进度
3. 决策下一步行动

---

## 八、P1/P2 预留角色

| 角色 | 归属 | 触发条件 | 职责 |
|------|:----:|---------|------|
| game-balancer | Claw | P0.2 | 3猫/5敌/6卡数值平衡 |
| ai-engineer | AI写作 | V1 Phase 2 | Prompt工程、RAG、多模型 |
| electron-dev | AI写作 | V1 Phase 3 | 跨平台打包、自动更新 |
| sound-designer | Claw | P1 | BGM、战斗/卡牌/UI音效 |
| devops | 共享 | 首个发布 | CI/CD流水线 |

---

## 九、工作流历史时间线

```
2026-05-22 09:10 → claw-game 团队创建
2026-05-22 09:12 → pm-claw 报送 P0.1 启动诊断报告
2026-05-22 09:13 → pm-legal 报送法律管理系统诊断报告
2026-05-22 09:15 → pm-emergence 报送涌现叙事诊断报告
2026-05-22 09:16 → team-lead 决定：法律+叙事暂停，集中 Claw+写作教练
2026-05-22 09:17 → pm-legal shutdown ✅
2026-05-22 09:18 → pm-emergence shutdown ✅
2026-05-22 09:20 → programmer-a + programmer-b 孵化 + 报到
2026-05-22 09:38 → pm-claw D1 完成 (git init + 项目骨架)
2026-05-22 09:40 → programmer-a D2-D8 完成 (状态机+网格)
2026-05-22 10:15 → GitHub 仓库确认 + push
2026-05-22 10:15 → pm-writer shutdown_request 发送
2026-05-22 ~17:00 → AI写作教练产品设计讨论
2026-05-22 18:15 → V1_SPEC.md 完成 + 推送
2026-05-22 18:52 → AGENT_WORKFLOW.md 创建
2026-05-23 16:50 → Claw: 代码审计+修复（类型标注/PUDDLE/敌人.tres）
2026-05-23 16:50 → AI写作教练: 旧版15文件功能评估报告
2026-05-23 17:17 → 团队重组: claw-game-2创建，team-lead+pm-claw+pm-writer就位
2026-05-23 17:22 → 角色缺位评估: 识别并补位4个P0角色
2026-05-23 17:24 → v2.0完整团队: 全部12个P0角色孵化完成
2026-05-23 17:24 → team_composition_plan.md 完整团队方案文档产出
2026-05-23 17:50 → agent-design 独立项目创建 ← 当前
```
