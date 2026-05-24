"""
Hermes Agent Framework - 完整Agent协作演示
展示Agent团队如何协作完成项目开发任务
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import HermesToolkit
from src.agents import create_default_team


def print_separator(title: str):
    """打印分隔符"""
    print("\n" + "╔" + "═" * 58 + "╗")
    print(f"║  {title.center(54)}  ║")
    print("╚" + "═" * 58 + "╝")


def print_team_status(team):
    """打印团队状态"""
    print_separator("Agent团队状态")
    status = team.get_status()
    print(f"\n团队名称: {status['team_name']}")
    print(f"Agent数量: {status['agent_count']}")
    print(f"\n各Agent状态:")
    for name, agent_status in status['agents'].items():
        print(f"  🤖 {name:<15} - {agent_status['role']:<20} - {agent_status['status']}")
    print()


async def main():
    """主演示程序"""
    print("🦅 Hermes Agent Framework - 完整协作演示")
    print("=" * 60)
    
    # 1. 初始化工具集
    print_separator("初始化工具集")
    base_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "demo_workspace",
        "hermes_project"
    )
    
    toolkit = HermesToolkit(
        base_directory=base_dir,
        strict_security=True,
        enable_preview=True
    )
    print(f"✅ 工具集已初始化")
    print(f"   工作目录: {base_dir}")
    
    # 2. 创建Agent团队
    print_separator("创建Agent团队")
    team = create_default_team(
        team_name="Hermes Development Team",
        toolkit=toolkit,
        project_name="hermes_demo"
    )
    print_team_status(team)
    
    # 3. 执行工作流 - 简化版本，直接指定agent
    workflow = [
        # 任务1: TeamLead 初始化项目
        {
            "type": "init_project",
            "project_name": "hermes_web_app",
            "project_type": "python_library",
            "description": "一个由Hermes Agent团队创建的演示项目",
        },
        # 任务2: DevLead 分析需求
        {
            "type": "analyze_requirements",
            "requirements": "创建一个简单的Web应用，包含用户管理、API接口和数据存储功能",
            "project_type": "web_app",
        },
        # 任务3: Architect 设计架构
        {
            "type": "design_architecture",
            "project_type": "web_app",
        },
    ]
    
    print_separator("执行协作工作流")
    print(f"📋 工作流包含 {len(workflow)} 个任务")
    
    results = await team.run_workflow(workflow)
    
    # 4. 打印总结
    print_separator("演示总结")
    
    success_count = sum(1 for r in results if r.get("success"))
    print(f"\n任务执行结果: {success_count}/{len(results)} 成功")
    
    print_team_status(team)
    
    print_separator("演示完成")
    print("\n🎉 恭喜！您已经成功运行了Hermes Agent Framework演示！")
    print("\n📖 下一步:")
    print("  1. 查看生成的项目文件: demo_workspace/")
    print("  2. 阅读文档了解更多: docs/")
    print("  3. 继续开发和扩展Agent功能")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 演示已停止。再见！")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
        import traceback
        traceback.print_exc()

