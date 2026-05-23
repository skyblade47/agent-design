# 技术规格文档模板

> 🏗️ 供Technical Architect Agent参考的标准技术规格文档格式。

---

# [项目名称] — 技术规格文档

**版本**: 1.0  
**日期**: YYYY-MM-DD  
**作者**: Technical Architect Agent  
**状态**: [Draft / Review / Approved]

---

## 1. 概述

### 1.1 项目背景
[简述项目背景和目标]

### 1.2 文档范围
[本文档覆盖哪些方面的技术设计]

### 1.3 术语表
| 术语 | 说明 |
|------|------|
| ... | ... |

---

## 2. 技术选型

### 2.1 选型总览
| 层次 | 技术 | 版本 | 选型理由 |
|------|------|------|---------|
| 前端框架 | | | |
| UI库 | | | |
| 状态管理 | | | |
| 后端语言 | | | |
| 后端框架 | | | |
| 数据库 | | | |
| 缓存 | | | |
| 消息队列 | | | |
| 对象存储 | | | |
| 容器化 | | | |
| CI/CD | | | |

### 2.2 关键选型对比
**前端框架**: [React vs Vue vs Angular]
| 维度 | React | Vue | Angular | 选择 |
|------|-------|-----|---------|------|
| 学习曲线 | 中 | 低 | 高 | |
| 生态 | 大 | 中 | 中 | |
| TypeScript | 好 | 好 | 原生 | |
| 性能 | 好 | 好 | 中 | |
| **最终选择** | | | | ✅ |

---

## 3. 系统架构

### 3.1 架构图
```
[在此插入架构图 - Mermaid/ASCII]
```

### 3.2 架构模式
- [ ] 单体架构
- [ ] 微服务
- [ ] Serverless
- [ ] 混合

### 3.3 模块划分
| 模块 | 职责 | 技术 | 依赖 |
|------|------|------|------|
| | | | |

---

## 4. 数据模型

### 4.1 ER图
```
[Entity Relationship Diagram]
```

### 4.2 核心表结构

#### users
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| email | VARCHAR(255) | UNIQUE, NOT NULL | |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

---

## 5. API设计

### 5.1 API风格
- [RESTful / GraphQL / gRPC / tRPC]

### 5.2 核心端点
| Method | Path | 描述 | 认证 | 速率限制 |
|--------|------|------|------|---------|
| | | | | |

### 5.3 请求/响应示例
```json
// POST /api/v1/auth/login
// Request
{
  "email": "user@example.com",
  "password": "securepassword"
}

// Response 200
{
  "success": true,
  "data": {
    "token": "eyJhbGci...",
    "user": { "id": "1", "email": "user@example.com" }
  }
}

// Response 401
{
  "success": false,
  "error": { "code": "INVALID_CREDENTIALS", "message": "..." }
}
```

---

## 6. 安全方案

### 6.1 认证流程
```
用户 → 输入凭据 → POST /auth/login → 验证 → 返回JWT → 后续请求带Authorization头
```

### 6.2 授权模型
- [RBAC / ABAC / ReBAC]
- 角色定义: [Admin / User / Guest / ...]

### 6.3 安全措施清单
- [x] HTTPS强制
- [x] 密码bcrypt加密
- [x] JWT过期 + Refresh Token
- [x] CORS白名单
- [x] Rate Limiting
- [x] 输入校验
- [ ] ...

---

## 7. 部署架构

### 7.1 环境规划
| 环境 | 用途 | 配置 |
|------|------|------|
| Development | 本地开发 | Docker Compose |
| Staging | 预发布测试 | 云服务 |
| Production | 生产环境 | 云服务 + 备份 |

### 7.2 部署流程
```
PR Merge → CI Build & Test → Build Docker Image → Push Registry → Deploy Staging → E2E Test → Deploy Production
```

---

## 8. 技术风险

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| | 高/中/低 | 高/中/低 | |

---

## 9. 变更记录
| 版本 | 日期 | 作者 | 变更说明 |
|------|------|------|---------|
| 1.0 | YYYY-MM-DD | | 初始版本 |
