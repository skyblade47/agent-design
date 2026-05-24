"""
Hermes Agent Framework - 简单实用演示
展示核心功能的快速演示
"""

import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import HermesToolkit
from src.agents import (
    TeamLeadAgent,
    DevLeadAgent,
    TechnicalArchitectAgent,
    BackendDeveloperAgent,
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


async def main():
    """主演示"""
    print("🦅 Hermes Agent Framework - 快速演示")
    
    # 1. 初始化
    print_section("初始化工具集")
    base_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "demo_workspace",
        "simple_demo"
    )
    toolkit = HermesToolkit(base_directory=base_dir)
    print(f"✅ 工作目录: {base_dir}")
    
    # 2. 创建各个Agent
    print_section("创建Agent")
    
    team_lead = TeamLeadAgent(
        name="Alice",
        toolkit=toolkit,
        description="负责整体项目规划"
    )
    print(f"🤖 创建: {team_lead.name} ({team_lead.role.value})")
    
    dev_lead = DevLeadAgent(
        name="Bob",
        toolkit=toolkit,
        project_name="simple_demo",
        description="负责技术管理"
    )
    print(f"🤖 创建: {dev_lead.name} ({dev_lead.role.value})")
    
    architect = TechnicalArchitectAgent(
        name="Diana",
        toolkit=toolkit,
        description="负责架构设计"
    )
    print(f"🤖 创建: {architect.name} ({architect.role.value})")
    
    backend_dev = BackendDeveloperAgent(
        name="Charlie",
        toolkit=toolkit,
        description="负责后端开发"
    )
    print(f"🤖 创建: {backend_dev.name} ({backend_dev.role.value})")
    
    # 3. 演示各个Agent的功能
    print_section("演示Agent功能")
    
    print("\n[1] 架构师设计架构...")
    arch_result = await architect.execute_task({
        "type": "design_architecture",
        "project_type": "web_app"
    })
    if arch_result.get("success"):
        arch = arch_result["architecture"]
        print(f"   架构设计完成!")
        print(f"   建议技术栈: {arch['recommendations']}")
    
    print("\n[2] DevLead分析需求...")
    req_result = await dev_lead.execute_task({
        "type": "analyze_requirements",
        "requirements": "创建一个简单的待办事项应用",
        "project_type": "web_app"
    })
    if req_result.get("success"):
        print(f"   需求分析完成!")
        print(f"   技术栈建议: {req_result['analysis']['tech_stack']}")
    
    print("\n[3] Backend Developer创建API端点...")
    ep_result = await backend_dev.execute_task({
        "type": "create_endpoint",
        "endpoint_name": "todos",
        "file_path": "todos.py"
    })
    if ep_result.get("success"):
        print(f"   API端点创建完成!")
        print(f"   文件: {ep_result.get('file')}")
    
    print_section("演示完成!")
    print("\n🎉 恭喜！您已成功体验了Hermes Agent Framework的核心功能！")
    print("\n📖 下一步:")
    print("  1. 查看生成的代码文件")
    print("  2. 阅读更多文档")
    print("  3. 继续扩展功能")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n❌ 出错: {e}")
        import traceback
        traceback.print_exc()

