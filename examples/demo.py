"""
Hermes Agent Framework - 完整示例
演示如何使用框架创建项目和Agent协作
"""

import asyncio
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools.file_tools import FileTools
from src.scaffold.project_generator import ProjectScaffoldGenerator, ProjectConfig
from src.core.safety import SafetyGuard, AgentBehaviorPolicy, DevelopmentStandards


def print_separator(title: str):
    """打印分隔符"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def demo_safety_and_behavior():
    """演示安全和行为控制"""
    print_separator("安全和行为控制演示")
    
    # 安全卫士
    safety_guard = SafetyGuard()
    
    # 测试危险命令
    test_commands = [
        "ls -la",  # 安全
        "rm -rf /",  # 危险
        "cat ~/.ssh/id_rsa",  # 敏感文件
    ]
    
    for cmd in test_commands:
        result = safety_guard.check_command(cmd)
        status = "✅ 安全" if result.passed else f"❌ {result.message}"
        print(f"命令: '{cmd}' -> {status}")
    
    # 行为策略
    policy = AgentBehaviorPolicy()
    
    test_actions = [
        "读取项目文件",
        "修改代码文件",
        "删除重要文件",
        "部署到生产环境",
    ]
    
    print("\n行为策略检查:")
    for action in test_actions:
        allowed, reason = policy.is_allowed(action)
        status = "✅ 允许" if allowed else f"❌ {reason}"
        print(f"操作: '{action}' -> {status}")
    
    # 开发规范
    standards = DevelopmentStandards()
    print("\n开发规范:")
    print(f"- Python PEP 8: {standards.code_standards['python']}")
    print(f"- 项目结构 (web_app): {standards.get_project_structure_guide('web_app')}")


def demo_project_scaffolding():
    """演示项目脚手架生成"""
    print_separator("项目脚手架生成演示")
    
    # 初始化文件工具
    file_tools = FileTools(base_directory="./demo_workspace")
    
    # 初始化脚手架生成器
    generator = ProjectScaffoldGenerator(file_tools)
    
    # 创建项目配置
    config = ProjectConfig(
        name="my-awesome-project",
        description="一个由Hermes Agent Framework创建的示例项目",
        project_type="python_library",
        author="Hermes Team",
    )
    
    print(f"\n正在生成项目: {config.name}")
    print(f"项目类型: {config.project_type}")
    
    # 生成项目
    result = generator.generate_project(config)
    
    if result["success"]:
        print(f"\n✅ 项目生成成功!")
        print(f"创建了 {len(result['files_created'])} 个文件:")
        for f in result["files_created"][:10]:
            print(f"  - {f}")
        if len(result["files_created"]) > 10:
            print(f"  ... 还有 {len(result['files_created']) - 10} 个文件")
    else:
        print(f"\n❌ 项目生成失败:")
        for error in result["errors"]:
            print(f"  - {error}")
    
    # 查看生成的项目结构
    print("\n项目目录结构:")
    tree_result = file_tools.get_project_tree(max_depth=3)
    if tree_result.success:
        print_tree(tree_result.data, indent=0)


def print_tree(node, indent: int):
    """打印目录树"""
    prefix = "  " * indent
    name = node.get("name", "")
    if node.get("type") == "directory":
        print(f"{prefix}📁 {name}/")
    else:
        print(f"{prefix}📄 {name}")
    
    for child in node.get("children", []):
        print_tree(child, indent + 1)


async def main():
    """主函数"""
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*10 + "🦅 Hermes Agent Framework 演示" + " "*24 + "║")
    print("╚" + "═"*58 + "╝")
    
    # 1. 安全和行为控制演示
    demo_safety_and_behavior()
    
    # 2. 项目脚手架演示
    demo_project_scaffolding()
    
    print_separator("演示完成!")
    print("\n下一步:")
    print("  1. 查看生成的项目: ./demo_workspace/my-awesome-project")
    print("  2. 阅读文档: ./ROADMAP.md, ./EVALUATION_REPORT.md")
    print("  3. 继续开发Phase 1的其他功能")


if __name__ == "__main__":
    asyncio.run(main())

