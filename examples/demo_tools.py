"""
Hermes Agent Framework - 完整工具演示
展示所有工具的功能，包括安全限制、文件编辑、PowerShell执行等
"""

import os
import sys
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import (
    HermesToolkit,
    FileTools,
    EnhancedFileEditor,
    PowerShellExecutor,
    PowerShellSecurityPolicy,
    CommandRiskLevel,
    ToolCategory
)


def print_separator(title: str):
    """打印分隔符"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_file_operations():
    """演示文件操作工具"""
    print_separator("文件操作工具演示")
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo_workspace")
    toolkit = HermesToolkit(base_directory=base_dir, strict_security=True)
    
    # 创建目录
    print("\n[1] 创建测试目录...")
    result = toolkit.file_tools.create_directory("test_project")
    print(f"    结果: {result.success} - {result.message}")
    
    # 写入测试文件
    print("\n[2] 创建测试文件...")
    test_content = """# 测试文件
这是一个由Hermes工具生成的测试文件。
包含多行内容。
"""
    result = toolkit.file_tools.write_file("test_project/test.txt", test_content)
    print(f"    结果: {result.success} - {result.message}")
    
    # 读取文件
    print("\n[3] 读取文件...")
    result = toolkit.file_tools.read_file("test_project/test.txt")
    if result.success:
        print(f"    内容:\n{result.data}")
    
    # 列出目录
    print("\n[4] 列出目录内容...")
    result = toolkit.file_tools.list_directory("test_project")
    if result.success and result.data:
        print("    内容:")
        for item in result.data:
            print(f"      - {item['type']}: {item['name']}")


def demo_enhanced_editing():
    """演示增强的文件编辑工具"""
    print_separator("增强文件编辑工具演示")
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo_workspace")
    toolkit = HermesToolkit(base_directory=base_dir)
    
    # 创建一个Python文件进行编辑
    print("\n[1] 创建示例Python文件...")
    initial_code = """def hello():
    print("Hello World")

# 主函数
if __name__ == "__main__":
    hello()
"""
    toolkit.file_tools.write_file("test_project/example.py", initial_code)
    
    # 读取带行号
    print("\n[2] 读取文件（带行号）...")
    result = toolkit.file_editor.read_with_line_numbers("test_project/example.py")
    if result.success:
        print(result.data['numbered_content'])
    
    # 在指定行插入
    print("\n[3] 在第2行插入注释...")
    result = toolkit.file_editor.insert_text(
        "test_project/example.py",
        "    # 这是一个插入的注释\n",
        2
    )
    print(f"    结果: {result.success} - {result.message}")
    
    # 替换文本
    print("\n[4] 替换函数名...")
    result = toolkit.file_editor.replace_text(
        "test_project/example.py",
        "hello()",
        "greet(name=\"User\")"
    )
    print(f"    结果: {result.success} - {result.message}")
    
    # 搜索文本
    print("\n[5] 搜索文本...")
    result = toolkit.file_editor.search_text("test_project/example.py", "print")
    if result.success:
        print(f"    找到 {result.data['total']} 个匹配:")
        for match in result.data['matches'][:3]:
            print(f"      第 {match['line_number']} 行: {match['content'][:50]}")
    
    # 显示最终文件
    print("\n[6] 最终文件内容...")
    result = toolkit.file_tools.read_file("test_project/example.py")
    if result.success:
        print(result.data)


def demo_powershell_security():
    """演示PowerShell安全策略"""
    print_separator("PowerShell安全策略演示")
    
    policy = PowerShellSecurityPolicy()
    
    test_commands = [
        # 安全命令
        ("Get-Date", "获取当前日期"),
        ("ls", "列出目录"),
        # 低风险命令
        ("python --version", "Python版本"),
        ("git --version", "Git版本"),
        # 中等风险命令
        ("mkdir test", "创建目录"),
        # 高风险命令（应该被阻止）
        ("Format-Drive C:", "格式化磁盘"),
        ("Remove-Item -Recurse -Force C:\\", "强制删除"),
        ("Invoke-Expression 'malicious code'", "执行表达式"),
        ("reg add HKLM\\System", "修改注册表"),
        ("powershell -ExecutionPolicy Bypass", "修改执行策略"),
    ]
    
    print("\n命令安全检查:")
    print("-" * 50)
    
    for cmd, description in test_commands:
        risk_level, reason = policy.assess_risk(cmd)
        status = "✅ 允许"
        if risk_level == CommandRiskLevel.MEDIUM:
            status = "⚠️  需要审批"
        elif risk_level in [CommandRiskLevel.HIGH, CommandRiskLevel.CRITICAL]:
            status = "❌ 阻止"
        
        print(f"\n{description}:")
        print(f"  命令: {cmd}")
        print(f"  风险: {risk_level.value}")
        print(f"  状态: {status}")
        if reason:
            print(f"  原因: {reason}")


def demo_powershell_execution():
    """演示PowerShell执行（实际执行安全命令）"""
    print_separator("PowerShell执行演示")
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo_workspace")
    executor = PowerShellExecutor(working_dir=base_dir)
    
    # 执行安全命令
    test_cmds = [
        "Get-Date",
        "Get-Location",
        "ls",
        "Write-Host 'Hello from PowerShell'",
    ]
    
    print("\n执行安全命令:")
    print("-" * 50)
    
    for cmd in test_cmds:
        print(f"\n执行: {cmd}")
        result = executor.execute(cmd)
        
        print(f"  成功: {result.success}")
        print(f"  风险: {result.risk_level.value}")
        if result.stdout:
            print(f"  输出:\n{result.stdout.strip()}")
        if result.stderr:
            print(f"  错误:\n{result.stderr.strip()}")
    
    # 测试危险命令（应该被阻止）
    print("\n" + "=" * 50)
    print("测试危险命令阻止:")
    print("-" * 50)
    
    dangerous_cmd = "Format-Drive C:"
    print(f"\n尝试执行: {dangerous_cmd}")
    result = executor.execute(dangerous_cmd)
    print(f"  成功: {result.success}")
    print(f"  阻止: {not result.was_allowed}")
    if result.blocked_reason:
        print(f"  原因: {result.blocked_reason}")


def demo_tool_registry():
    """演示工具注册表"""
    print_separator("工具注册表演示")
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo_workspace")
    toolkit = HermesToolkit(base_directory=base_dir)
    
    # 列出所有工具
    print("\n[1] 所有可用工具:")
    all_tools = toolkit.list_tools()
    for tool in all_tools:
        print(f"  - {tool.name:<20} ({tool.category.value:<15}) - {tool.description}")
    
    # 按分类列出
    print(f"\n[2] 按分类:")
    for category in ToolCategory:
        tools = toolkit.list_tools(category)
        if tools:
            print(f"  {category.value}:")
            for tool in tools:
                print(f"    - {tool.name}: {tool.description}")
    
    # 安全摘要
    print(f"\n[3] 安全摘要:")
    summary = toolkit.get_security_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")


def demo_project_generation():
    """演示项目生成"""
    print_separator("项目脚手架生成演示")
    
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo_workspace")
    toolkit = HermesToolkit(base_directory=base_dir)
    
    # 生成一个Python库项目
    print("\n[1] 生成Python库项目...")
    result = toolkit._generate_project_safe(
        name="hermes_demo_lib",
        description="一个由Hermes工具生成的示例库",
        project_type="python_library",
        author="Hermes Team"
    )
    
    if result['success']:
        print(f"  ✅ 成功!")
        print(f"  创建文件: {len(result['files_created'])}")
        for f in result['files_created'][:5]:
            print(f"    - {f}")
        if len(result['files_created']) > 5:
            print(f"    ... 还有 {len(result['files_created'])-5} 个文件")
    else:
        print(f"  ❌ 失败:")
        for err in result.get('errors', []):
            print(f"    - {err}")
    
    # 查看项目结构
    print("\n[2] 查看项目结构...")
    tree_result = toolkit.file_tools.get_project_tree()
    if tree_result.success:
        print(f"  项目根: {tree_result.data.get('name', '')}")


def main():
    """主演示函数"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 5 + "🦅 Hermes Agent Framework - 工具完整演示" + " " * 18 + "║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        # 1. 文件操作
        demo_file_operations()
        
        # 2. 增强的文件编辑
        demo_enhanced_editing()
        
        # 3. PowerShell安全策略
        demo_powershell_security()
        
        # 4. PowerShell实际执行
        demo_powershell_execution()
        
        # 5. 工具注册表
        demo_tool_registry()
        
        # 6. 项目生成
        demo_project_generation()
        
        print_separator("演示完成!")
        print("\n🎉 所有工具演示完成!")
        print("\n📁 生成的文件在: demo_workspace/")
        print("📚 下一步: 阅读文档并开始使用这些工具!")
        
    except Exception as e:
        print(f"\n❌ 演示出错: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

