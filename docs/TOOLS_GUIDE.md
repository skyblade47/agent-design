# Hermes Agent Framework - 工具使用指南

## 概述

Hermes Agent Framework 提供了一套完整的工具集，用于支持Agent进行自主开发任务，同时包含严格的安全限制机制。

## 🛠️ 工具列表

### 1. 文件操作工具 (`FileTools`)

**功能：** 安全的文件和目录操作

**主要方法：**
- `read_file(file_path)` - 读取文件内容
- `write_file(file_path, content, overwrite)` - 写入文件
- `list_directory(dir_path, include_hidden)` - 列出目录内容
- `create_directory(dir_path)` - 创建目录
- `get_project_tree(max_depth)` - 获取项目目录树

**安全特性：**
- 所有操作限制在指定的基础目录内
- 防止路径遍历攻击
- 自动创建必要的目录

**示例：**
```python
from src.tools import FileTools

tools = FileTools(base_directory="./my_project")

# 读取文件
result = tools.read_file("src/main.py")
if result.success:
    print(result.data)

# 写入文件
tools.write_file("test.txt", "Hello World", overwrite=False)
```

### 2. 增强文件编辑工具 (`EnhancedFileEditor`)

**功能：** 高级文件编辑功能，支持精确编辑

**主要方法：**
- `read_with_line_numbers(file_path)` - 读取带行号的文件
- `insert_text(file_path, text, line_number)` - 在指定行插入文本
- `replace_text(file_path, old_text, new_text, count)` - 替换文本
- `replace_lines(file_path, start_line, end_line, new_text)` - 替换行范围
- `append_text(file_path, text, create_missing)` - 追加文本
- `search_text(file_path, search_pattern, case_sensitive)` - 搜索文本

**示例：**
```python
from src.tools import FileTools, EnhancedFileEditor

file_tools = FileTools("./project")
editor = EnhancedFileEditor(file_tools)

# 读取带行号
result = editor.read_with_line_numbers("main.py")
print(result.data['numbered_content'])

# 在第5行插入
editor.insert_text("main.py", "# 新增内容\n", 5)

# 搜索文本
search_result = editor.search_text("main.py", "TODO")
print(f"找到 {search_result.data['total']} 个TODO")
```

### 3. PowerShell执行工具 (`PowerShellExecutor`)

**功能：** 安全执行PowerShell命令，带有严格的安全检查

**主要方法：**
- `execute(command, require_approval, approval_callback)` - 执行命令
- `get_history(limit)` - 获取执行历史

**安全策略：**
- **SAFE (安全):** 允许直接执行
  - Get-ChildItem, Get-Content, Get-Date, 等
- **LOW (低风险):** 允许执行
  - python, pip, git, 等
- **MEDIUM (中风险):** 需要人工审批
  - Remove-Item, New-Item, 等
- **HIGH/CRITICAL (高风险):** 阻止执行
  - Format-Drive, Invoke-Expression, reg, 等

**示例：**
```python
from src.tools import PowerShellExecutor

executor = PowerShellExecutor(
    working_dir="./project",
    require_approval_for_medium_risk=True
)

# 执行安全命令
result = executor.execute("Get-Date")
if result.success:
    print(result.stdout)

# 检查风险
result = executor.execute("Format-Drive C:")
if not result.was_allowed:
    print(f"被阻止: {result.blocked_reason}")
```

### 4. 项目预览服务器 (`PreviewServer`)

**功能：** 本地预览项目

**主要方法：**
- `start()` - 启动服务器
- `stop()` - 停止服务器
- `get_url()` - 获取访问URL

**使用：**
```python
from src.tools import PreviewServer, ProjectPreviewManager

# 单个预览
server = PreviewServer("./my_project", port=8000, auto_open=True)
url = server.start()
print(f"预览地址: {url}")
server.stop()

# 管理多个预览
manager = ProjectPreviewManager()
success, msg, url = manager.start_preview("project1", "./project1")
manager.stop_preview("project1")
```

### 5. 统一工具集 (`HermesToolkit`)

**功能：** 整合所有工具的统一接口

**主要功能：**
- 所有工具一站式访问
- 工具注册和管理
- 安全摘要
- 使用历史记录

**示例：**
```python
from src.tools import HermesToolkit

# 初始化
toolkit = HermesToolkit(
    base_directory="./workspace",
    strict_security=True,
    enable_preview=True
)

# 使用工具
result = toolkit.file_tools.read_file("test.txt")
result = toolkit.powershell.execute("Get-Date")
tools = toolkit.list_tools()

# 获取安全摘要
summary = toolkit.get_security_summary()
print(summary)
```

## 🔒 安全控制机制

### 安全策略要点

1. **路径限制**
   - 所有文件操作限制在指定基础目录
   - 防止 `../../` 路径遍历

2. **命令过滤**
   - 白名单机制允许已知安全命令
   - 黑名单阻止危险模式
   - 参数安全检查

3. **审批流程**
   - 中等风险操作需要人工确认
   - 高风险操作直接阻止

4. **审计日志**
   - 记录所有工具使用
   - 命令执行历史
   - 安全事件追踪

### 风险等级说明

| 等级 | 颜色 | 说明 |
|------|------|------|
| SAFE | ✅ | 完全安全，可直接执行 |
| LOW | ✅ | 低风险，允许执行 |
| MEDIUM | ⚠️ | 需要人工审批 |
| HIGH | ❌ | 高风险，阻止执行 |
| CRITICAL | ❌ | 严重风险，立即阻止 |

## 📋 使用建议

### 对于Agent开发

1. **从 HermesToolkit 开始**
   ```python
   toolkit = HermesToolkit(base_directory="./agent_workspace")
   ```

2. **使用工具注册表**
   ```python
   tool = toolkit.get_tool("read_file")
   if tool:
       # 使用工具
   ```

3. **尊重安全限制**
   - 不要尝试绕过安全检查
   - 需要审批时，暂停等待用户确认
   - 记录所有操作

### 对于用户

1. **配置基础目录**
   - 设置适当的工作空间目录
   - 不要让Agent访问敏感目录

2. **监督中等风险操作**
   - 文件删除、修改配置等操作需要确认

3. **定期检查审计日志**
   - 查看Agent执行了哪些操作
   - 发现异常行为及时阻止

## 🚀 快速开始

### 运行演示

```bash
# 基础演示
python examples/demo.py

# 完整工具演示
python examples/demo_tools.py
```

### 在Agent中集成

```python
from src.tools import HermesToolkit

class MyAgent:
    def __init__(self):
        self.toolkit = HermesToolkit(
            base_directory="./agent_work",
            strict_security=True
        )
    
    def do_something(self):
        # 使用工具
        result = self.toolkit.file_tools.list_directory(".")
        # 处理结果
        pass
```

## 📚 更多文档

- [QUICKSTART.md](../QUICKSTART.md) - 快速入门
- [ROADMAP.md](../ROADMAP.md) - 开发路线图
- [ARCHITECTURE.md](../ARCHITECTURE.md) - 架构设计

